---
layout: page
title: blogs
permalink: /blog/
nav: true
nav_order: 3
description: Longer-form deep-dives and a visual log of things I'm exploring — from world models to hands-on experiments.
---

<div class="blogs-intro">
  This is where I share longer-form thoughts: technical deep-dives into the ideas I work on, and a more visual log of experiments and things that catch my attention. Two threads to start — more will follow.
</div>

<nav class="blogs-section-nav" aria-label="Blog sections">
  <a href="#world-models"><i class="fa-solid fa-globe"></i> World Models</a>
  <a href="#exploring"><i class="fa-solid fa-compass"></i> Exploring</a>
</nav>

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

<!-- ═══════════════════════════ Exploring ═══════════════════════════ -->
<section id="exploring" class="blog-section">
  <h2 class="blog-section-title"><i class="fa-solid fa-compass"></i> Exploring</h2>
  <p class="blog-section-sub">
    A visual log — images, demos, and short videos from experiments and things worth sharing.
  </p>

  <!-- ▼▼▼  EXPLORING MEDIA (images / videos) GO HERE  ▼▼▼ -->
  <div class="exploring-grid">
    <!-- Each media item will look like:
    <figure class="exploring-item">
      <img src="/assets/img/EXAMPLE.png" loading="lazy" alt="caption">
      <figcaption>Short caption</figcaption>
    </figure>
    -->
  </div>
  <div class="blog-placeholder">
    <i class="fa-solid fa-images"></i>
    <span>Gallery in progress — images & videos coming soon.</span>
  </div>
  <!-- ▲▲▲  EXPLORING MEDIA (images / videos) GO HERE  ▲▲▲ -->
</section>

<style>
.blogs-intro {
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--global-text-color);
  max-width: 760px;
  margin: 0 0 1.5rem;
}
.blogs-section-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-bottom: 2.5rem;
}
.blogs-section-nav a {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.9rem;
  border: 1px solid var(--global-divider-color);
  border-radius: 999px;
  font-size: 0.9rem;
  color: var(--global-text-color);
  text-decoration: none;
  transition: all 0.2s ease;
}
.blogs-section-nav a:hover {
  background: var(--global-theme-color);
  border-color: var(--global-theme-color);
  color: #fff;
}
.blog-section {
  margin-bottom: 3.5rem;
  scroll-margin-top: 80px;
}
.blog-section-title {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  font-weight: 700;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid var(--global-theme-color);
}
.blog-section-title i {
  color: var(--global-theme-color);
}
.blog-section-sub {
  color: var(--global-text-color);
  opacity: 0.8;
  margin: 0.75rem 0 1.5rem;
  max-width: 760px;
}
.exploring-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}
.exploring-item {
  margin: 0;
  border-radius: 10px;
  overflow: hidden;
  background: var(--global-card-bg-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.exploring-item img,
.exploring-item video {
  display: block;
  width: 100%;
  height: 180px;
  object-fit: cover;
}
.exploring-item figcaption {
  padding: 0.55rem 0.75rem;
  font-size: 0.85rem;
  color: var(--global-text-color);
}
.blog-placeholder {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1.5rem;
  border: 1px dashed var(--global-divider-color);
  border-radius: 10px;
  color: var(--global-text-color);
  opacity: 0.7;
  font-size: 0.95rem;
}
.blog-placeholder i {
  color: var(--global-theme-color);
}
/* World Models series list */
.wm-series {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.wm-entry {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.1rem;
  border: 1px solid var(--global-divider-color);
  border-radius: 12px;
  background: var(--global-card-bg-color);
  text-decoration: none;
  color: var(--global-text-color);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.wm-entry:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
  border-color: var(--global-theme-color);
}
.wm-num {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--global-theme-color);
  min-width: 2.2rem;
  text-align: center;
  font-variant-numeric: tabular-nums;
}
.wm-text { display: flex; flex-direction: column; flex: 1; }
.wm-entry-title { font-weight: 600; line-height: 1.35; }
.wm-entry-desc { font-size: 0.9rem; opacity: 0.8; margin-top: 0.15rem; }
.wm-entry-meta { font-size: 0.78rem; opacity: 0.6; margin-top: 0.35rem; }
.wm-arrow { color: var(--global-theme-color); opacity: 0.6; transition: transform 0.18s ease; }
.wm-entry:hover .wm-arrow { transform: translateX(4px); opacity: 1; }
.wm-num-icon { font-size: 1.1rem; }
.wm-subhead {
  display: flex; align-items: center; gap: 0.5rem;
  margin: 2rem 0 1rem; font-size: 1.05rem; font-weight: 600; opacity: 0.9;
}
.wm-subhead i { color: var(--global-theme-color); }
</style>
