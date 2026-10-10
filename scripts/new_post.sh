#!/usr/bin/env bash
# Scaffold a new blog post with proper front matter.
# Usage:  make new-post title="My Post Title"   (or)   bash scripts/new_post.sh "My Post Title"
set -euo pipefail

title="${1:-}"
if [ -z "$title" ]; then
  echo 'Usage: make new-post title="My Post Title"'
  exit 1
fi

root="$(cd "$(dirname "$0")/.." && pwd)"
today="$(date +%F)"

# slug: lowercase, non-alphanumerics -> hyphens, trim/squeeze hyphens
slug="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"
slug="${slug:-post}"

file="$root/_posts/${today}-${slug}.md"
if [ -e "$file" ]; then
  echo "Already exists: ${file#$root/}"
  exit 1
fi

cat > "$file" <<EOF
---
layout: post
title: "${title}"
date: ${today} 09:00:00
description: ""
tags: []
categories: []
giscus_comments: true
related_posts: false
---

Write your post here.
EOF

echo "Created: ${file#$root/}"
echo "Edit it, then publish:  make publish m=\"new post: ${title}\""
