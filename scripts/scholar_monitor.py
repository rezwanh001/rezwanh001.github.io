#!/usr/bin/env python3
"""
Local Google Scholar monitor for the lab server.

Unlike GitHub's shared runners (which Scholar 403-blocks), this machine can
reach Google Scholar reliably, so citation updates are driven from here.

What it does on each run:
  1. Fetch the Scholar profile (stats + the full works list).
  2. Compare against the last-seen state (~/.scholar_monitor_state.json).
  3. If the citation total / h-index / i10 changed, or a NEW paper appeared
     that is not yet in _bibliography/papers.bib, send an ntfy push so you get
     it on your phone.
  4. Save the new state.

Modes:
  (default)   detect + notify only. Read-only w.r.t. the repo — never pushes.
  --apply     also refresh the cached count files (scholar.yml /
              scholar_citations.yml) via fetch_citations.py so an update is
              staged locally. It still does NOT git-push; committing/pushing to
              the public repo stays a human-approved step.
  --once-quiet  initialise the baseline state without sending any notification
                (use on first setup).

Env:
  NTFY_TOPIC   ntfy topic to notify (default: the baked topic below).

Intended to be run periodically from the server's own crontab, e.g.:
  0 */6 * * *  cd /path/to/repo && /usr/bin/python3 scripts/scholar_monitor.py >> ~/scholar_monitor.log 2>&1
"""

import os
import re
import sys
import json
import time
import random
import subprocess

import requests
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")
BIB_FILE = os.path.join(ROOT_DIR, "_bibliography", "papers.bib")
STATE_FILE = os.path.expanduser("~/.scholar_monitor_state.json")

SCHOLAR_USER_ID = "HaI-oFUAAAAJ"
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "rezwan-scholar-af8aafafff")
PUBLICATIONS_URL = "https://rezwan.xyz/publications/"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
]
_SESSION = requests.Session()


def http_get(url, timeout=20, retries=3):
    last = None
    for attempt in range(retries):
        ua = USER_AGENTS[attempt % len(USER_AGENTS)]
        try:
            r = _SESSION.get(
                url,
                headers={"User-Agent": ua, "Accept-Language": "en-US,en;q=0.9"},
                timeout=timeout,
            )
            if r.status_code in (403, 429, 500, 502, 503):
                last = r
                time.sleep(random.uniform(3, 8) * (attempt + 1))
                continue
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            last = e
            time.sleep(random.uniform(2, 5) * (attempt + 1))
    if isinstance(last, requests.Response):
        last.raise_for_status()
    raise last if last is not None else RuntimeError(f"request failed: {url}")


def fetch_profile():
    """Return dict: {citations, h_index, i10, works: {id: title}}."""
    url = (
        f"https://scholar.google.com/citations?user={SCHOLAR_USER_ID}"
        f"&hl=en&cstart=0&pagesize=100"
    )
    soup = BeautifulSoup(http_get(url).text, "html.parser")

    stats = {"citations": None, "h_index": None, "i10": None}
    table = soup.find("table", id="gsc_rsb_st")
    if table:
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True).lower()
                val = cells[1].get_text(strip=True)
                if "citations" in label:
                    stats["citations"] = val
                elif "h-index" in label:
                    stats["h_index"] = val
                elif "i10-index" in label:
                    stats["i10"] = val

    works = {}
    for a in soup.find_all("a", class_="gsc_a_at"):
        href = a.get("href", "")
        m = re.search(r"citation_for_view=[^:]+:([A-Za-z0-9_-]+)", href)
        if m:
            works[m.group(1)] = a.get_text(strip=True)

    if stats["citations"] is None and not works:
        raise RuntimeError("Scholar page had no stats/works — likely blocked.")
    return stats, works


def bib_ids():
    """Uncommented google_scholar_id values currently in papers.bib."""
    ids = set()
    with open(BIB_FILE) as f:
        for line in f:
            if line.lstrip().startswith("%"):
                continue
            m = re.search(r"google_scholar_id\s*=\s*\{([A-Za-z0-9_-]+)\}", line)
            if m:
                ids.add(m.group(1))
    return ids


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def ntfy(title, message, tags="chart_with_upwards_trend", priority="default"):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode("utf-8"),
            headers={
                "Title": title,
                "Tags": tags,
                "Priority": priority,
                "Click": PUBLICATIONS_URL,
            },
            timeout=15,
        )
        print(f"  notified: {title} — {message}")
    except Exception as e:
        print(f"  ! ntfy failed: {e}")


def main():
    apply_mode = "--apply" in sys.argv
    quiet_baseline = "--once-quiet" in sys.argv

    stats, works = fetch_profile()
    known_bib = bib_ids()
    new_papers = {aid: t for aid, t in works.items() if aid not in known_bib}

    state = load_state()
    first_run = not state
    prev_cit = state.get("citations")
    prev_seen_new = set(state.get("seen_new_papers", []))

    print(
        f"Scholar: citations={stats['citations']} h={stats['h_index']} "
        f"i10={stats['i10']} | works={len(works)} | not-in-bib={len(new_papers)}"
    )

    # --- Notifications (skip on first-run baseline / --once-quiet) ---
    if not first_run and not quiet_baseline:
        if stats["citations"] and stats["citations"] != prev_cit:
            try:
                delta = int(stats["citations"]) - int(prev_cit)
                arrow = f"(+{delta})" if delta > 0 else f"({delta})"
            except (TypeError, ValueError):
                arrow = ""
            ntfy(
                "📈 Citations updated",
                f"{prev_cit} → {stats['citations']} {arrow} · "
                f"h-index {stats['h_index']} · i10 {stats['i10']}. "
                f"Approve an update to publish.",
                tags="chart_with_upwards_trend,books",
            )

        for aid, title in new_papers.items():
            if aid not in prev_seen_new:
                ntfy(
                    "🆕 New paper on Google Scholar",
                    f"“{title}” is on your Scholar profile but not yet in your "
                    f"portfolio. Reply to add it (needs a proper BibTeX entry).",
                    tags="new,memo",
                    priority="high",
                )
    else:
        print("  (baseline run — no notifications sent)")

    # --- Optional: stage a local count refresh (never pushes) ---
    if apply_mode:
        print("  --apply: refreshing cached counts via fetch_citations.py ...")
        subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, "fetch_citations.py")],
            check=False,
        )
        print("  counts refreshed locally; commit & push is a separate approved step.")

    # --- Persist state ---
    state.update(
        {
            "citations": stats["citations"],
            "h_index": stats["h_index"],
            "i10": stats["i10"],
            "works": works,
            "seen_new_papers": sorted(prev_seen_new | set(new_papers)),
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    )
    save_state(state)
    print(f"State saved to {STATE_FILE}")


if __name__ == "__main__":
    main()
