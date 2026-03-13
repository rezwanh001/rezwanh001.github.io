#!/usr/bin/env python3
"""
Fetch per-paper Google Scholar citation counts and cache them in _data/scholar_citations.yml.

Usage:
    python scripts/fetch_citations.py

This script reads google_scholar_id values from _bibliography/papers.bib,
fetches citation counts from Google Scholar, and writes them to
_data/scholar_citations.yml so the Jekyll plugin can use cached values
instead of live-scraping (which gets blocked on CI servers).
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
