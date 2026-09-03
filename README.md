# Md Rezwanul Haque — Portfolio (`rezwan.xyz`)

A customized [al-folio](https://github.com/alshedivat/al-folio) Jekyll site.
**Live:** <https://rezwan.xyz/> · **Phone admin:** <https://rezwan.xyz/assets/console.html>

> **This README is a control center.** It tells you *where* everything lives and
> the *shortest command* to review or change it. Skim the tables, run a `make`
> target, or open the phone admin — whatever is fastest.

---

## ⚡ Quick commands

Run `make` (or `make help`) to list everything. The common ones:

| Command | What it does |
|---|---|
| `make citations` | Refresh Google Scholar counts → `_data/scholar_citations.yml`, `_data/scholar.yml` |
| `make repos` | Re-bake GitHub repo cards → `_data/repositories.yml` |
| `make monitor` | Check Scholar for changes / new papers, push an ntfy phone alert |
| `make paper id=2508.09362` | Resolve an arXiv id / DOI → a ready `papers.bib` entry (prints it) |
| `make paper-add id=2508.09362` | …same, but **append** it to `papers.bib` (writes a `.bak` first) |
| `make refresh` | The safe maintenance set: `citations` + `repos` + `monitor` |
| `make serve` | Local live preview at <http://localhost:4000> |
| `make build` | Build the static site into `_site/` |
| `make status` | `git status --short` |
| **`make publish m="msg"`** | **Stage everything → commit → push** (live in ~3–5 min) |

> ⚠️ **Don't** run `for f in scripts/*.py; do python "$f"; done` — `add_paper.py`
> needs an argument and `scholar_scraper.py` is legacy. Use `make refresh` instead.

---

## 🚀 Publish your changes

Edited a file, a publication, or a book? Publish it yourself — you never need to ask.

**One-time setup** (so `git push` works as `rezwanh001`):

```bash
gh auth login          # choose  rezwanh001 · GitHub.com · HTTPS
gh auth setup-git      # let git push with that login
```

**Every time — one command:**

```bash
make publish m="what you changed"
```

This stages everything, commits, and pushes. Your change is **live at
<https://rezwan.xyz> in ~3–5 min** (the Deploy Action runs on its own).

**Prefer to do it by hand?**

```bash
git status                        # 1. see what changed
git add -A                        # 2. stage everything
git commit -m "what you changed"  # 3. commit
git push                          # 4. publish
```

> Always push from **`rezwanh001`** (not another GitHub account on the machine).
> If a push is refused, run `gh auth switch --user rezwanh001` and push again.
> Or edit from your phone — the [admin console](#-edit-from-your-phone-no-server-from-anywhere) commits for you.

---

## 📱 Edit from your phone (no server, from anywhere)

`assets/console.html` is an installable web app (Add to Home Screen). It talks
straight to GitHub with a **fine-grained token stored only on your device**:

- **Live site** — your real `rezwan.xyz` embedded, with refresh (watch changes go live)
- **Publications** — add (paste arXiv/DOI → auto-resolves), edit, delete
- **Books** — add (form), delete
- **Editor** — open / edit / create / delete **any** file, with a markdown preview
- **Scholar** — live counts · **Settings** — sign-in / log out

Setup once: create a fine-grained PAT (Contents: Read/Write on this repo) → open the
URL on iPhone → paste the token in the login box (**never in a file**) → Add to Home Screen.

---

## 🗺️ Where everything lives

| To change… | Edit this |
|---|---|
| **Publications** | `_bibliography/papers.bib` (BibTeX; `abbr`, `preview`, `selected`, `google_scholar_id`). Rendered by `_layouts/bib.liquid` on `/publications/` |
| **Citation numbers** | Auto-cached in `_data/scholar_citations.yml` (per paper) + `_data/scholar.yml` (profile). Use `make citations` |
| **Books / reading** | `_pages/books.md` → `reading_list:` block. Author bios: `_data/authors.yml` (keyed by author, `en`+`bn`). Covers: `assets/pdf/books/` |
| **Blog posts** | `_posts/YYYY-MM-DD-title.md`. Series/sections wired in `_pages/blog.md` + `_pages/blog-*.md` |
| **Repo cards** | `_data/repositories.yml` (baked; `make repos`). Templates: `_includes/repository/` |
| **CV** | `_data/cv.yml` and `_pages/cv.md` |
| **Home / About** | `_pages/about.md` (`permalink: /`) |
| **Pages & nav order** | `_pages/*.md` — `nav: true` + `nav_order:` (currently alphabetical, `submenus` last) |
| **Everyday Reading data** | `_data/asma_ul_husna.yml`, images in `assets/img/daily-amal/` |
| **Colors / styling** | `_sass/_variables.scss` (theme `#b509ac`), `_sass/_base.scss` (custom), `_sass/_themes.scss` |
| **Site config** | `_config.yml` |

---

## 🔧 scripts/ reference

| Script | Run | Purpose |
|---|---|---|
| `fetch_citations.py` | `make citations` | Scrapes Scholar → citation cache. Rotating UAs + retry (rides out 403s). |
| `fetch_github.py` | `make repos` | GitHub API → baked repo cards in `_data/repositories.yml`. |
| `add_paper.py` | `make paper id=…` | arXiv/DOI → styled `papers.bib` entry; detects preprint vs venue. `--append` writes it. |
| `scholar_monitor.py` | `make monitor` | Detects citation/paper changes, sends an **ntfy** alert. Read-only; never pushes. Runs daily via the server crontab. |
| `scholar_scraper.py` | — | ⚠️ **Legacy**, superseded by `fetch_citations.py`. Safe to delete. |

State/cache: `~/.scholar_monitor_state.json` (monitor). See [Automation](#-automation) below.

---

## 🔁 Automation

- **Citations** update via `make citations` (run it, or the daily server cron). The
  in-repo GitHub Action `.github/workflows/update-citations.yml` exists but its
  **schedule is disabled** — it's a manual `workflow_dispatch` fallback only.
- **Monitor + phone alerts:** `scholar_monitor.py` runs daily from the server's
  crontab and pushes an **ntfy** notification when your citations change or a new
  paper appears. New papers still need a proper hand-made bib entry (verify before pushing).

---

## 🚀 Deploy

Push to `master` → the **Deploy site** Action (`.github/workflows/deploy.yml`)
builds and publishes to GitHub Pages → served at `rezwan.xyz`. Live in **~3–5 min**.
`[skip ci]` commits (e.g. the citation cache) don't trigger a deploy.

---

## 💻 Local development

```bash
bundle install          # once
make serve              # http://localhost:4000  (live reload)
```

Requires Ruby + Bundler + the Jekyll toolchain (see al-folio docs). Python scripts
need `requests beautifulsoup4 pyyaml` (`pip install requests beautifulsoup4 pyyaml`).

---

## 📝 Notes

- **Push only from `rezwanh001`** (not any other GitHub account on the machine).
- **Never commit secrets.** Tokens go in the phone admin's login box or in
  `~/.git-credentials` on the server — never in a tracked file. `.gitignore` covers
  `__pycache__/`, `*.pyc`, `papers.bib.bak`.
- Based on [al-folio](https://github.com/alshedivat/al-folio) (MIT).
