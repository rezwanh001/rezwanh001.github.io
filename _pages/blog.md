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

  {% assign exp_locs = "niagara,quebec" | split: "," %}
  <div class="exp-gallery">
    {% for loc in exp_locs %}
      {% assign needle = "/assets/img/exploring/" | append: loc | append: "/" %}
      {% assign loc_files = site.static_files | where_exp: "f", "f.path contains needle" | sort: "path" %}
      {% case loc %}
        {% when 'niagara' %}
          {% assign loc_name = "Niagara" %}{% assign loc_region = "Ontario · Canada" %}
          {% assign loc_tag = "Where the river falls off the edge of the world." %}
          {% assign loc_intro = "On the Canadian side the Horseshoe Falls curve in a thundering crescent — millions of litres a minute plunging into a canyon of rising mist that catches the sun in sudden rainbows, and glows in shifting colour after dark." %}
        {% when 'quebec' %}
          {% assign loc_name = "Québec" %}{% assign loc_region = "Québec · Canada" %}
          {% assign loc_tag = "Old-World Europe on the banks of the St. Lawrence." %}
          {% assign loc_intro = "Inside the stone ramparts of Vieux-Québec — the only walled city north of Mexico and a UNESCO World Heritage site — cobblestone lanes climb past the copper-roofed Château Frontenac through four centuries of French-Canadian history." %}
      {% endcase %}
      {% if loc_files.size > 0 %}
      <section class="exp-location">
        <div class="exp-loc-head">
          <h3 class="exp-loc-title"><i class="fa-solid fa-location-dot"></i> {{ loc_name }} <span class="exp-loc-region">{{ loc_region }}</span></h3>
          <p class="exp-loc-tag">{{ loc_tag }}</p>
          <p class="exp-loc-intro">{{ loc_intro }}</p>
        </div>
        <div class="exp-grid" data-location="{{ loc }}">
          {% for f in loc_files %}
            {% assign ext = f.extname | downcase %}
            {% if ext == '.mp4' or ext == '.webm' %}
              <button type="button" class="exp-thumb is-video" data-type="video" data-src="{{ f.path | relative_url }}" onclick="openExp(this)" aria-label="Play {{ loc_name }} video">
                <video class="exp-media" muted preload="metadata" playsinline tabindex="-1"><source src="{{ f.path | relative_url }}#t=0.1" type="video/mp4"></video>
                <span class="exp-play" aria-hidden="true"><i class="fa-solid fa-play"></i></span>
              </button>
            {% elsif ext == '.jpg' or ext == '.jpeg' or ext == '.png' or ext == '.webp' %}
              <button type="button" class="exp-thumb" data-type="image" data-src="{{ f.path | relative_url }}" onclick="openExp(this)" aria-label="View {{ loc_name }} photo">
                <img class="exp-media" src="{{ f.path | relative_url }}" loading="lazy" alt="{{ loc_name }} — photo">
              </button>
            {% endif %}
          {% endfor %}
        </div>
      </section>
      {% endif %}
    {% endfor %}
  </div>
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

/* ── Exploring gallery ── */
.exp-gallery { display: flex; flex-direction: column; gap: 2.75rem; }
.exp-location { scroll-margin-top: 80px; }
.exp-loc-head { margin-bottom: 0.5rem; }
.exp-loc-title {
  display: flex; align-items: baseline; gap: 0.5rem; flex-wrap: wrap;
  font-weight: 700; margin: 0 0 0.35rem;
}
.exp-loc-title i { color: var(--global-theme-color); }
.exp-loc-region { font-size: 0.78rem; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; opacity: 0.55; }
.exp-loc-tag { font-style: italic; color: var(--global-theme-color); margin: 0 0 0.4rem; font-size: 1.02rem; }
.exp-loc-intro { max-width: 760px; opacity: 0.85; line-height: 1.7; margin: 0; }
.exp-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.6rem; margin-top: 1.1rem;
}
@media (min-width: 576px) { .exp-grid { grid-template-columns: repeat(auto-fill, minmax(185px, 1fr)); gap: 0.75rem; } }
.exp-thumb {
  position: relative; display: block; padding: 0; border: none; cursor: pointer;
  border-radius: 12px; overflow: hidden; background: var(--global-card-bg-color);
  aspect-ratio: 1 / 1; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.exp-thumb:hover, .exp-thumb:focus-visible { transform: translateY(-3px) scale(1.01); box-shadow: 0 8px 22px rgba(0, 0, 0, 0.18); outline: none; }
.exp-media { width: 100%; height: 100%; object-fit: cover; display: block; }
.exp-play { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; pointer-events: none; }
.exp-play i {
  width: 46px; height: 46px; border-radius: 50%; background: rgba(0, 0, 0, 0.55); color: #fff;
  display: flex; align-items: center; justify-content: center; font-size: 1rem; padding-left: 3px;
  transition: background 0.2s ease, transform 0.2s ease;
}
.is-video::after { content: ""; position: absolute; inset: 0; background: linear-gradient(transparent 55%, rgba(0, 0, 0, 0.35)); pointer-events: none; }
.exp-thumb:hover .exp-play i { background: var(--global-theme-color); transform: scale(1.08); }
/* Lightbox */
.exp-lightbox {
  position: fixed; inset: 0; z-index: 3000; display: none; align-items: center; justify-content: center;
  background: rgba(8, 8, 10, 0.94); backdrop-filter: blur(4px);
}
.exp-lightbox.open { display: flex; animation: expFade 0.2s ease; }
@keyframes expFade { from { opacity: 0; } to { opacity: 1; } }
.exp-lb-stage { max-width: 92vw; max-height: 86vh; display: flex; align-items: center; justify-content: center; }
.exp-lb-media { max-width: 92vw; max-height: 86vh; border-radius: 8px; box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5); }
.exp-lb-close { position: absolute; top: 18px; right: 22px; z-index: 3; background: none; border: none; color: #fff; font-size: 2.4rem; line-height: 1; cursor: pointer; opacity: 0.8; }
.exp-lb-close:hover { opacity: 1; }
.exp-lb-nav {
  position: absolute; top: 50%; transform: translateY(-50%); z-index: 3; background: rgba(255, 255, 255, 0.1);
  border: none; color: #fff; width: 52px; height: 52px; border-radius: 50%; font-size: 1.5rem; cursor: pointer;
  display: flex; align-items: center; justify-content: center; transition: background 0.2s ease;
}
.exp-lb-nav:hover { background: var(--global-theme-color); }
.exp-lb-prev { left: 18px; } .exp-lb-next { right: 18px; }
.exp-lb-counter {
  position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: #fff; font-size: 0.9rem;
  letter-spacing: 0.05em; opacity: 0.85; background: rgba(0, 0, 0, 0.4); padding: 0.25rem 0.8rem; border-radius: 999px;
}
@media (max-width: 575px) {
  .exp-lb-nav { width: 42px; height: 42px; font-size: 1.2rem; }
  .exp-lb-prev { left: 6px; } .exp-lb-next { right: 6px; }
}
</style>

<!-- Exploring media lightbox -->
<div class="exp-lightbox" id="expLightbox" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Media viewer">
  <button class="exp-lb-close" onclick="closeExp()" aria-label="Close">&times;</button>
  <button class="exp-lb-nav exp-lb-prev" onclick="expNav(-1)" aria-label="Previous">&#10094;</button>
  <div class="exp-lb-stage" id="expStage"></div>
  <button class="exp-lb-nav exp-lb-next" onclick="expNav(1)" aria-label="Next">&#10095;</button>
  <div class="exp-lb-counter" id="expCounter"></div>
</div>

<script>
(function () {
  var items = [], idx = 0;
  var lb = document.getElementById('expLightbox');
  var stage = document.getElementById('expStage');
  var counter = document.getElementById('expCounter');
  function render() {
    var b = items[idx];
    var type = b.getAttribute('data-type'), src = b.getAttribute('data-src');
    stage.innerHTML = '';
    if (type === 'video') {
      var v = document.createElement('video');
      v.src = src; v.controls = true; v.autoplay = true; v.playsInline = true; v.className = 'exp-lb-media';
      stage.appendChild(v);
    } else {
      var im = document.createElement('img');
      im.src = src; im.alt = ''; im.className = 'exp-lb-media';
      stage.appendChild(im);
    }
    counter.textContent = (idx + 1) + ' / ' + items.length;
  }
  window.openExp = function (btn) {
    var grid = btn.closest('.exp-grid');
    items = Array.prototype.slice.call(grid.querySelectorAll('.exp-thumb'));
    idx = items.indexOf(btn); if (idx < 0) idx = 0;
    render();
    lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };
  window.closeExp = function () {
    lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true');
    stage.innerHTML = ''; document.body.style.overflow = '';
  };
  window.expNav = function (d) { if (!items.length) return; idx = (idx + d + items.length) % items.length; render(); };
  lb.addEventListener('click', function (e) { if (e.target === lb) closeExp(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') closeExp();
    else if (e.key === 'ArrowLeft') expNav(-1);
    else if (e.key === 'ArrowRight') expNav(1);
  });
})();
</script>
