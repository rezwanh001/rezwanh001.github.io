#!/usr/bin/env python3
"""
Fetch per-paper Google Scholar citation counts and profile stats,
then cache them in _data/scholar_citations.yml and _data/scholar.yml.

Usage:
    python scripts/fetch_citations.py

This script reads google_scholar_id values from _bibliography/papers.bib,
fetches citation counts from Google Scholar, and writes them to
_data/scholar_citations.yml so the Jekyll plugin can use cached values
instead of live-scraping (which gets blocked on CI servers).

It also scrapes profile-level statistics (total citations, h-index,
i10-index, and yearly citation counts) and saves them to _data/scholar.yml.
"""

import re
import time
import random
import yaml
import os
import requests
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, '..')
BIB_FILE = os.path.join(ROOT_DIR, '_bibliography', 'papers.bib')
CACHE_FILE = os.path.join(ROOT_DIR, '_data', 'scholar_citations.yml')
SCHOLAR_FILE = os.path.join(ROOT_DIR, '_data', 'scholar.yml')
SCHOLAR_USER_ID = 'HaI-oFUAAAAJ'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def extract_article_ids(bib_path):
    """Extract all google_scholar_id values from the .bib file."""
    ids = []
    pattern = re.compile(r'^\s*google_scholar_id\s*=\s*\{(.+?)\}', re.MULTILINE)
    with open(bib_path, 'r') as f:
        content = f.read()
    for match in pattern.finditer(content):
        article_id = match.group(1).strip()
        if article_id not in ids:
            ids.append(article_id)
    return ids


def fetch_citation_count(user_id, article_id):
    """Fetch citation count for a single article from Google Scholar."""
    url = (
        f"https://scholar.google.com/citations?view_op=view_citation&hl=en"
        f"&user={user_id}&citation_for_view={user_id}:{article_id}"
    )
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Try meta description first
        for meta in soup.find_all('meta'):
            content = meta.get('content', '')
            match = re.search(r'Cited by (\d[\d,]*)', content)
            if match:
                return int(match.group(1).replace(',', ''))

        # Try the citation count field on the page
        cited_by = soup.find('a', string=re.compile(r'Cited by'))
        if cited_by:
            match = re.search(r'Cited by (\d[\d,]*)', cited_by.text)
            if match:
                return int(match.group(1).replace(',', ''))

        return 0
    except Exception as e:
        print(f"  Error fetching {article_id}: {e}")
        return None


def fetch_profile_stats(user_id):
    """
    Fetch profile-level Google Scholar statistics:
    total citations, h-index, i10-index (all-time and recent),
    plus yearly citation counts.
    """
    url = f"https://scholar.google.com/citations?user={user_id}&hl=en"
    stats = {
        'citations': {'all': '0', 'recent': '0'},
        'h_index': {'all': '0', 'recent': '0'},
        'i10_index': {'all': '0', 'recent': '0'},
        'since_year': '2021',
        'cites_per_year': {},
    }
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')

        # --- Table stats (citations, h-index, i10-index) ---
        table = soup.find('table', id='gsc_rsb_st')
        if table:
            # Detect the "Since XXXX" year from table header
            header_row = table.find('tr')
            if header_row:
                headers = header_row.find_all('th')
                for th in headers:
                    year_match = re.search(r'Since\s+(\d{4})', th.get_text())
                    if year_match:
                        stats['since_year'] = year_match.group(1)
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    label = cells[0].get_text(strip=True).lower()
                    val_all = cells[1].get_text(strip=True)
                    val_recent = cells[2].get_text(strip=True)
                    if 'citations' in label:
                        stats['citations'] = {'all': val_all, 'recent': val_recent}
                    elif 'h-index' in label:
                        stats['h_index'] = {'all': val_all, 'recent': val_recent}
                    elif 'i10-index' in label:
                        stats['i10_index'] = {'all': val_all, 'recent': val_recent}

        # --- Yearly citation histogram ---
        chart_div = soup.find('div', class_='gsc_md_hist_b')
        if chart_div:
            years_row = soup.find('div', class_='gsc_md_hist_w')
            if years_row:
                year_spans = years_row.find_all('span', class_='gsc_g_t')
                bar_spans = chart_div.find_all('a', class_='gsc_g_a')
                years = [s.get_text(strip=True) for s in year_spans]
                counts = []
                for bar in bar_spans:
                    span = bar.find('span', class_='gsc_g_al')
                    if span:
                        counts.append(span.get_text(strip=True))
                    else:
                        counts.append('0')
                for y, c in zip(years, counts):
                    stats['cites_per_year'][y] = c

        print(f"Profile stats: citations={stats['citations']['all']}, "
              f"h-index={stats['h_index']['all']}, "
              f"i10-index={stats['i10_index']['all']}")
        print(f"Yearly citations: {stats['cites_per_year']}")
        return stats
    except Exception as e:
        print(f"Error fetching profile stats: {e}")
        return stats


def save_scholar_stats(scholar_path, stats):
    """Save profile-level scholar stats to _data/scholar.yml."""
    with open(scholar_path, 'w') as f:
        yaml.dump(stats, f, default_flow_style=False, sort_keys=True)
    print(f"Profile stats saved to {scholar_path}")


def load_cache(cache_path):
    """Load existing cache if available."""
    if os.path.exists(cache_path):
        with open(cache_path, 'r') as f:
            data = yaml.safe_load(f) or {}
        return data
    return {}


def save_cache(cache_path, data):
    """Save citation cache to YAML file."""
    with open(cache_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=True)


def main():
    # --- Fetch profile-level stats ---
    print("Fetching Google Scholar profile stats...")
    time.sleep(random.uniform(1.0, 3.0))
    profile_stats = fetch_profile_stats(SCHOLAR_USER_ID)
    save_scholar_stats(SCHOLAR_FILE, profile_stats)
    print()

    # --- Fetch per-paper citation counts ---
    print(f"Reading article IDs from {BIB_FILE}...")
    article_ids = extract_article_ids(BIB_FILE)
    print(f"Found {len(article_ids)} articles with google_scholar_id.\n")

    cache = load_cache(CACHE_FILE)
    updated = 0
    failed = 0

    for i, article_id in enumerate(article_ids, 1):
        print(f"[{i}/{len(article_ids)}] Fetching citations for {article_id}...", end=' ')

        # Random delay to avoid rate limiting
        time.sleep(random.uniform(2.0, 5.0))

        count = fetch_citation_count(SCHOLAR_USER_ID, article_id)
        if count is not None:
            cache[article_id] = count
            updated += 1
            print(f"=> {count}")
        else:
            failed += 1
            print("=> FAILED (keeping old value if exists)")

    save_cache(CACHE_FILE, cache)
    print(f"\nDone! Updated {updated} articles, {failed} failed.")
    print(f"Cache saved to {CACHE_FILE}")


if __name__ == '__main__':
    main()
