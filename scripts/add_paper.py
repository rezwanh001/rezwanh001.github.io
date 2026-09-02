#!/usr/bin/env python3
"""
Resolve a paper from an arXiv id/URL (or a DOI) into a papers.bib entry that
matches this repo's style. This is the "you paste a link, it auto-fills" engine
— reusable by CLI now and by the phone admin app later.

Usage:
    python scripts/add_paper.py 2607.25091
    python scripts/add_paper.py https://arxiv.org/abs/2508.09362
    python scripts/add_paper.py 10.1109/SMC.2026.12345           # DOI via Crossref
    python scripts/add_paper.py 2607.25091 --key haque2026towards --append

By default it PRINTS the entry for review (never auto-commits). --append adds it
to _bibliography/papers.bib (a .bak copy is written first). google_scholar_id and
preview are left as TODO comments to fill in after review — see [check citations
before push] guidance.
"""

import os
import re
import sys
import argparse
import xml.etree.ElementTree as ET
import requests

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BIB = os.path.join(ROOT, "_bibliography", "papers.bib")
UA = {"User-Agent": "rezwanh001-portfolio/1.0 (mailto:r.haque.249.rh@gmail.com)"}


def surname_first(name):
    """'Md Rezwanul Haque' -> 'Haque, Md Rezwanul' (BibTeX author form)."""
    name = " ".join(name.split())
    if "," in name:
        return name
    parts = name.split(" ")
    if len(parts) == 1:
        return name
    return f"{parts[-1]}, {' '.join(parts[:-1])}"


def venue_abbr(text, year):
    """Extract a short venue code (e.g. 'ICCV 2025') from free venue text."""
    if not text:
        return "TODO-VENUE"
    m = re.search(r"\(([A-Z][A-Za-z]{1,9})\)", text)
    if not m:
        m = re.search(
            r"\b(ICCV|CVPR|ECCV|NeurIPS|ICML|ICLR|AAAI|IJCAI|KDD|SMC|IJCNN|ICDAR|"
            r"EMNLP|ACL|NAACL|COLING|LREC|WACV|BMVC|MICCAI|ATC|ICCIT|INTERSPEECH)\b",
            text,
        )
    return f"{m.group(1)} {year}".strip() if m else "TODO-VENUE"


def suggest_key(first_author, year, title):
    last = surname_first(first_author).split(",")[0].strip().lower()
    last = re.sub(r"[^a-z]", "", last) or "paper"
    word = re.sub(r"[^a-z]", "", (title.split() or ["paper"])[0].lower()) or "paper"
    return f"{last}{year}{word}"


def resolve_arxiv(arxiv_id):
    arxiv_id = arxiv_id.strip()
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", arxiv_id)
    if not m:
        raise SystemExit(f"Could not parse an arXiv id from: {arxiv_id}")
    aid = m.group(1)
    url = f"https://export.arxiv.org/api/query?id_list={aid}"
    r = requests.get(url, headers=UA, timeout=25)
    r.raise_for_status()
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    e = ET.fromstring(r.text).find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        raise SystemExit(f"No arXiv record found for {aid}")

    def gx(tag, p="a"):
        n = e.find(f"{p}:{tag}", ns)
        return n.text.strip() if n is not None and n.text else None

    title = " ".join(gx("title").split())
    authors = [a.find("a:name", ns).text for a in e.findall("a:author", ns)]
    year = (gx("published") or "0000")[:4]
    abstract = " ".join((gx("summary") or "").split())
    journal_ref = gx("journal_ref", "x")
    doi = gx("doi", "x")
    comment = gx("comment", "x")

    return {
        "source": "arxiv",
        "arxiv_id": aid,
        "title": title,
        "authors": authors,
        "year": year,
        "abstract": abstract,
        "journal_ref": journal_ref,
        "doi": doi,
        "comment": comment,
        "html": f"https://arxiv.org/abs/{aid}",
        "pdf": f"https://arxiv.org/pdf/{aid}",
    }


def resolve_doi(doi):
    doi = doi.strip().replace("https://doi.org/", "")
    r = requests.get(f"https://api.crossref.org/works/{doi}", headers=UA, timeout=25)
    r.raise_for_status()
    m = r.json()["message"]
    authors = [
        f"{a.get('given','')} {a.get('family','')}".strip()
        for a in m.get("author", [])
    ]
    year = str((m.get("issued", {}).get("date-parts", [[None]])[0] or [None])[0] or "")
    return {
        "source": "doi",
        "doi": doi,
        "title": " ".join((m.get("title") or [""])[0].split()),
        "authors": authors,
        "year": year,
        "abstract": re.sub(r"<[^>]+>", "", m.get("abstract", "") or "").strip(),
        "journal_ref": (m.get("container-title") or [None])[0],
        "container": (m.get("container-title") or [None])[0],
        "type": m.get("type", ""),
        "volume": m.get("volume"),
        "issue": m.get("issue"),
        "pages": m.get("page"),
        "html": m.get("URL"),
    }


def to_bibtex(meta, key=None):
    authors = " and ".join(surname_first(a) for a in meta["authors"])
    key = key or suggest_key(meta["authors"][0] if meta["authors"] else "paper",
                             meta["year"], meta["title"])

    # Decide venue: published (journal_ref/doi) vs still-a-preprint.
    published = bool(meta.get("journal_ref") or meta.get("doi"))
    is_conf = False
    venue = meta.get("journal_ref") or ""
    if not published and meta.get("comment"):
        # arXiv comment often names the target venue for an accepted preprint.
        if re.search(r"proceed|conference|workshop|accepted", meta["comment"], re.I):
            venue = meta["comment"]
            is_conf = True

    lines = [f"@{'inproceedings' if (published and is_conf) else 'article'}{{{key},"]
    lines.append(f"  abbr={{{venue_abbr(venue, meta['year'])}}},")
    lines.append("  bibtex_show={true},")
    lines.append(f"  title={{{meta['title']}}},")
    lines.append(f"  author={{{authors}}},")
    if published and is_conf:
        lines.append(f"  booktitle={{{meta.get('journal_ref') or venue}}},")
    elif published:
        lines.append(f"  journal={{{meta.get('journal_ref') or meta.get('container') or ''}}},")
        for f in ("volume", "issue", "pages"):
            if meta.get(f):
                lines.append(f"  {('number' if f=='issue' else f)}={{{meta[f]}}},")
    else:
        aid = meta.get("arxiv_id", "")
        lines.append(f"  journal={{arXiv preprint arXiv:{aid}}},")
    lines.append(f"  year={{{meta['year']}}},")
    if meta.get("abstract"):
        lines.append(f"  abstract={{{meta['abstract']}}},")
    if meta.get("html"):
        lines.append(f"  html={{{meta['html']}}},")
    if meta.get("pdf"):
        lines.append(f"  pdf={{{meta['pdf']}}},")
    if meta.get("doi"):
        lines.append(f"  doi={{{meta['doi']}}},")
    lines.append("  % google_scholar_id={TODO after it appears on your Scholar profile},")
    lines.append("  % preview={TODO-image.png},")
    lines.append("}")

    note = []
    if not published and is_conf:
        note.append(f"NOTE: still a preprint, but arXiv comment names a venue "
                    f"→ set abbr accordingly; update to @inproceedings when published.")
    elif not published:
        note.append("NOTE: preprint (no journal_ref/doi yet). Update venue when published.")
    return "\n".join(lines), note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("identifier", help="arXiv id/URL or DOI")
    ap.add_argument("--key", help="BibTeX citation key (default: auto)")
    ap.add_argument("--append", action="store_true", help="append to papers.bib")
    args = ap.parse_args()

    ident = args.identifier
    if re.search(r"10\.\d{4,9}/", ident) and "arxiv" not in ident.lower():
        meta = resolve_doi(ident)
    else:
        meta = resolve_arxiv(ident)

    entry, notes = to_bibtex(meta, args.key)
    print("\n" + entry + "\n")
    for n in notes:
        print("  " + n)

    if args.append:
        with open(BIB) as f:
            cur = f.read()
        with open(BIB + ".bak", "w") as f:
            f.write(cur)
        with open(BIB, "a") as f:
            f.write("\n" + entry + "\n")
        print(f"\nAppended to {BIB} (backup at papers.bib.bak). REVIEW before pushing.")


if __name__ == "__main__":
    main()
