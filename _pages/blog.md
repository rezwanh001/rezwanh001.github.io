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

  <!-- ▼▼▼  WORLD MODELS CONTENT GOES HERE  ▼▼▼ -->
  <div class="blog-placeholder">
    <i class="fa-solid fa-pen-nib"></i>
    <span>Content in progress — writing coming soon.</span>
  </div>
  <!-- ▲▲▲  WORLD MODELS CONTENT GOES HERE  ▲▲▲ -->
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
</style>
