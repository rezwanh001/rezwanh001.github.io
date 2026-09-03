# ─────────────────────────────────────────────────────────────────────────
#  Portfolio control center — short commands.  Run `make` to see everything.
#  Override the interpreter if needed:  make citations PY=python3
# ─────────────────────────────────────────────────────────────────────────
PY ?= python
m ?= update

help:            ## Show this list of commands
	@echo "Portfolio commands (make <target>):"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[35m%-12s\033[0m %s\n",$$1,$$2}'

citations:       ## Refresh Google Scholar citation counts -> _data/scholar*.yml
	$(PY) scripts/fetch_citations.py

repos:           ## Re-bake GitHub repo cards -> _data/repositories.yml
	$(PY) scripts/fetch_github.py

monitor:         ## Check Scholar for changes / new papers and send an ntfy alert
	$(PY) scripts/scholar_monitor.py

paper:           ## Resolve a paper to a bib entry:  make paper id=2508.09362
	$(PY) scripts/add_paper.py $(id)

paper-add:       ## Same, but append it to papers.bib:  make paper-add id=2508.09362
	$(PY) scripts/add_paper.py $(id) --append

new-post:        ## Scaffold a blog post:  make new-post title="My Post Title"
	@bash scripts/new_post.sh "$(title)"

refresh:         ## Run the safe maintenance set (citations + repos + monitor)
	$(MAKE) citations repos monitor

serve:           ## Local live preview at http://localhost:4000
	bundle exec jekyll serve --livereload

build:           ## Build the static site into _site/
	bundle exec jekyll build

status:          ## Show what has changed (git)
	git status --short

publish:         ## Commit ALL changes and push:  make publish m="what you changed"
	@git add -A
	@git commit -m "$(m)" || echo "(nothing new to commit)"
	@gh auth switch --hostname github.com --user rezwanh001 2>/dev/null || true
	@git push
	@echo "Pushed. Live at https://rezwan.xyz in ~3-5 min."

.PHONY: help citations repos monitor paper paper-add new-post refresh serve build status publish
