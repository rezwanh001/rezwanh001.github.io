---
layout: page
permalink: /blog/
title: blogs
description: Longer-form threads — a daily reading collection, deep-dives on world models, and a visual log of places I have explored.
nav: true
nav_order: 3
---

<div class="blogs-intro">
  This is where I keep the threads I return to: a daily-reading collection, technical deep-dives on the ideas I work on, and a visual log of places and experiments. Pick a thread below.
</div>

{% assign wm_posts = site.posts | where_exp: "post", "post.tags contains 'world-models'" %}
{% assign amal_pages = site.static_files | where_exp: "f", "f.path contains '/assets/img/daily-amal/'" %}
{% assign exp_media = site.static_files | where_exp: "f", "f.path contains '/assets/img/exploring/'" %}

<div class="hub-grid">
  <a class="hub-card" href="{{ '/blog/everyday-reading/' | relative_url }}">
    <span class="hub-icon"><i class="fa-solid fa-book-open"></i></span>
    <span class="hub-title">Everyday Reading</span>
    <span class="hub-desc">A daily <em>amal</em> — short surahs, the 99 Names of Allah, and du'as, presented with Arabic, transliteration, English and Bangla, alongside the scanned source pages.</span>
    <span class="hub-meta"><i class="fa-solid fa-file-lines"></i> {{ amal_pages.size }} source pages <i class="fa-solid fa-arrow-right"></i></span>
  </a>

  <a class="hub-card" href="{{ '/blog/world-models/' | relative_url }}">
    <span class="hub-icon"><i class="fa-solid fa-globe"></i></span>
    <span class="hub-title">World Models</span>
    <span class="hub-desc">Notes and deep-dives on world models — learned simulators, predictive representations, and visual cognition for embodied agents.</span>
    <span class="hub-meta"><i class="fa-solid fa-pen-nib"></i> {{ wm_posts.size }} posts <i class="fa-solid fa-arrow-right"></i></span>
  </a>

  <a class="hub-card" href="{{ '/blog/exploring/' | relative_url }}">
    <span class="hub-icon"><i class="fa-solid fa-compass"></i></span>
    <span class="hub-title">Exploring</span>
    <span class="hub-desc">A visual log — photos and short videos from the places I have visited, gathered spot by spot in collapsible folds.</span>
    <span class="hub-meta"><i class="fa-solid fa-images"></i> {{ exp_media.size }} photos &amp; videos <i class="fa-solid fa-arrow-right"></i></span>
  </a>
</div>

{% include blog_styles.liquid %}
