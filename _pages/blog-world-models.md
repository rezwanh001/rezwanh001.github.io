---
layout: page
permalink: /blog/world-models/
title: world models
description: "Notes and deep-dives on world models — learned simulators, predictive representations, and visual cognition for embodied agents."
nav: false
---

<div class="blog-backlink"><a href="{{ '/blog/' | relative_url }}">&larr; All blogs</a></div>

<!-- ═══════════════════════════ World Models ═══════════════════════════ -->
<section id="world-models" class="blog-section">
  <h2 class="blog-section-title"><i class="fa-solid fa-globe"></i> World Models</h2>
  <p class="blog-section-sub">
    Notes and deep-dives on world models — learned simulators, predictive representations, and visual cognition for embodied agents.
  </p>

  {% assign wm_all = site.posts | where_exp: "post", "post.tags contains 'world-models'" | sort: "date" %}
  {% assign wm_parts = wm_all | where_exp: "post", "post.wm_resource != true" %}
  {% assign wm_resources = wm_all | where_exp: "post", "post.wm_resource == true" %}
  {% if wm_parts.size > 0 %}
  <div class="wm-series">
    {% for post in wm_parts %}
    <a class="wm-entry" href="{{ post.url | relative_url }}">
      <span class="wm-num">{{ forloop.index0 | prepend: "0" | slice: -2, 2 }}</span>
      <span class="wm-text">
        <span class="wm-entry-title">{{ post.title }}</span>
        {% if post.description %}<span class="wm-entry-desc">{{ post.description }}</span>{% endif %}
        <span class="wm-entry-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
      </span>
      <i class="fa-solid fa-arrow-right wm-arrow"></i>
    </a>
    {% endfor %}
  </div>
  {% else %}
  <div class="blog-placeholder">
    <i class="fa-solid fa-pen-nib"></i>
    <span>Content in progress — writing coming soon.</span>
  </div>
  {% endif %}

  {% if wm_resources.size > 0 %}
  <h3 class="wm-subhead"><i class="fa-solid fa-book-open"></i> Reading &amp; resources</h3>
  <div class="wm-series wm-resources">
    {% for post in wm_resources %}
    <a class="wm-entry" href="{{ post.url | relative_url }}">
      <span class="wm-num wm-num-icon"><i class="fa-solid fa-book"></i></span>
      <span class="wm-text">
        <span class="wm-entry-title">{{ post.title }}</span>
        {% if post.description %}<span class="wm-entry-desc">{{ post.description }}</span>{% endif %}
        <span class="wm-entry-meta">{{ post.date | date: "%b %-d, %Y" }}</span>
      </span>
      <i class="fa-solid fa-arrow-right wm-arrow"></i>
    </a>
    {% endfor %}
  </div>
  {% endif %}
</section>

{% include blog_styles.liquid %}
