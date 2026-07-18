---
layout: page
permalink: /blog/exploring/
title: exploring
description: "A visual log — photos and videos from places I have visited, gathered by spot."
nav: false
---

<div class="blog-backlink"><a href="{{ '/blog/' | relative_url }}">&larr; All blogs</a></div>

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
      {% assign vids = loc_files | where_exp: "f", "f.extname == '.mp4'" %}
      {% assign nvid = vids | size %}
      {% assign nimg = loc_files.size | minus: nvid %}
      <details class="exp-fold" open>
        <summary class="exp-fold-summary">
          <span class="exp-fold-title"><i class="fa-solid fa-location-dot"></i> {{ loc_name }} <span class="exp-loc-region">{{ loc_region }}</span></span>
          <span class="exp-fold-meta">
            {% if nimg > 0 %}<span class="exp-count"><i class="fa-solid fa-image"></i> {{ nimg }}</span>{% endif %}
            {% if nvid > 0 %}<span class="exp-count"><i class="fa-solid fa-video"></i> {{ nvid }}</span>{% endif %}
            <i class="fa-solid fa-chevron-down exp-fold-chevron" aria-hidden="true"></i>
          </span>
        </summary>
        <div class="exp-fold-body">
          <p class="exp-loc-tag">{{ loc_tag }}</p>
          <p class="exp-loc-intro">{{ loc_intro }}</p>
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
        </div>
      </details>
      {% endif %}
    {% endfor %}
  </div>
</section>

{% include blog_styles.liquid %}
{% include media_lightbox.liquid %}
