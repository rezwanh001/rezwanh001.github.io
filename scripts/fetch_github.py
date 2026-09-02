#!/usr/bin/env python3
"""
Re-bake GitHub repository/profile metadata into _data/repositories.yml.

The /repositories/ page renders native, self-contained cards from the baked
values in that file — it does NOT depend on the third-party
`github-readme-stats` service (which is shared, rate-limited, and often
returns broken images). Star/fork counts are also refreshed live in the
browser from the public GitHub API; these baked values are the always-works
fallback.

Usage:
    python scripts/fetch_github.py            # unauthenticated (60 req/hr)
    GITHUB_TOKEN=<token> python scripts/fetch_github.py   # higher rate limit

The script reads the existing `github_users` and the `repo:` slugs under
`github_repos`, fetches fresh metadata, and writes the file back. Curated
descriptions are preserved; empty ones are filled from the API.
"""

import os
import sys
import datetime
import requests
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "_data", "repositories.yml")
API = "https://api.github.com"

# GitHub's linguist language colors (extend as needed).
LANG_COLORS = {
    "Python": "#3572A5",
    "Jupyter Notebook": "#DA5B0B",
    "C++": "#f34b7d",
    "C": "#555555",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Shell": "#89e051",
    "Java": "#b07219",
    "Cuda": "#3A4E3A",
    "MATLAB": "#e16737",
    "PHP": "#4F5D95",
}


def headers():
    h = {"Accept": "application/vnd.github+json", "User-Agent": "rezwanh001-site"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def get(path):
    r = requests.get(f"{API}{path}", headers=headers(), timeout=20)
    r.raise_for_status()
    return r.json()


def main():
    with open(DATA_FILE) as f:
        data = yaml.safe_load(f)

    # --- Profile ---
    login = data["github_users"][0]
    u = get(f"/users/{login}")
    gu = data.setdefault("github_user", {})
    gu["login"] = u["login"]
    gu.setdefault("name", u.get("name") or u["login"])
    gu.setdefault("bio", u.get("bio") or "")
    gu.setdefault("avatar", "/assets/img/github_avatar.jpg")
    gu["html_url"] = u["html_url"]
    gu["public_repos"] = u["public_repos"]
    gu["followers"] = u["followers"]
    gu["following"] = u["following"]

    # --- Repositories ---
    for entry in data.get("github_repos", []):
        slug = entry["repo"]
        try:
            r = get(f"/repos/{slug}")
        except requests.HTTPError as e:
            print(f"  ! skip {slug}: {e}", file=sys.stderr)
            continue
        entry["name"] = r["name"]
        if not entry.get("description"):
            entry["description"] = r.get("description") or ""
        lang = r.get("language")
        if lang:
            entry["language"] = lang
            entry["lang_color"] = LANG_COLORS.get(lang, "#8b8b8b")
        entry["stars"] = r.get("stargazers_count", 0)
        entry["forks"] = r.get("forks_count", 0)
        entry["homepage"] = r.get("homepage") or None
        print(f"  {slug}: ★{entry['stars']} ⑂{entry['forks']}")

    header = (
        "# " + "=" * 71 + "\n"
        "#  Repositories page data  (/repositories/)\n"
        "#  Native cards render from the baked metadata below — no dependency\n"
        "#  on github-readme-stats. Re-bake with: python scripts/fetch_github.py\n"
        f"#  Last refreshed: {datetime.date.today().isoformat()}\n"
        "# " + "=" * 71 + "\n\n"
    )
    with open(DATA_FILE, "w") as f:
        f.write(header)
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=100)
    print(f"Wrote {DATA_FILE}")


if __name__ == "__main__":
    main()
