---
layout: page
permalink: /publications/
title: publications
description: Research publications across computer vision, deep learning, healthcare AI, and NLP. Also available on <a href='https://scholar.google.com/citations?user=HaI-oFUAAAAJ&hl=en'><b>Google Scholar</b></a>.
nav: true
nav_order: 2
---

<!-- ═══════════════════════  Hero Section  ═══════════════════════ -->
<div class="pub-hero">
  <div class="pub-hero-icon">
    <i class="fas fa-book-open"></i>
  </div>
  <h2 class="pub-hero-title">Research Publications</h2>
  <p class="pub-hero-subtitle">
    Contributions spanning sign language recognition, multimodal depression detection,
    medical image analysis, and healthcare AI
  </p>
  <div class="pub-hero-stats">
    <div class="pub-stat">
      <span class="pub-stat-number" id="pub-total-count">--</span>
      <span class="pub-stat-label">Publications</span>
    </div>
    <div class="pub-stat-divider"></div>
    <div class="pub-stat">
      <span class="pub-stat-number" id="pub-venue-count">--</span>
      <span class="pub-stat-label">Venues</span>
    </div>
    <div class="pub-stat-divider"></div>
    <div class="pub-stat">
      <span class="pub-stat-number" id="pub-year-span">--</span>
      <span class="pub-stat-label">Years Active</span>
    </div>
  </div>
  <div class="pub-hero-links">
    <a href="https://scholar.google.com/citations?user=HaI-oFUAAAAJ&hl=en" target="_blank" class="pub-hero-btn">
      <i class="ai ai-google-scholar"></i> Google Scholar
    </a>
    <a href="https://www.researchgate.net/profile/Md-Rezwanul-Haque" target="_blank" class="pub-hero-btn pub-hero-btn-outline">
      <i class="ai ai-researchgate"></i> ResearchGate
    </a>
  </div>
</div>

<!-- ═══════════════════════  Search  ═══════════════════════ -->
{% include bib_search.liquid %}

<!-- ═══════════════════════  Publication List  ═══════════════════════ -->
<div class="publications">
{% bibliography %}
</div>

<!-- ═══════════════════════  Stats Counter JS  ═══════════════════════ -->
<script>
document.addEventListener('DOMContentLoaded', function() {
  // Count publications
  const items = document.querySelectorAll('ol.bibliography > li');
  const totalEl = document.getElementById('pub-total-count');
  if (totalEl) totalEl.textContent = items.length;

  // Count unique venues
  const venues = new Set();
  document.querySelectorAll('ol.bibliography .abbr abbr').forEach(function(el) {
    venues.add(el.textContent.trim());
  });
  const venueEl = document.getElementById('pub-venue-count');
  if (venueEl) venueEl.textContent = venues.size;

  // Calculate years active
  const yearHeaders = document.querySelectorAll('h2.bibliography');
  const years = [];
  yearHeaders.forEach(function(h) {
    const y = parseInt(h.textContent.trim());
    if (!isNaN(y)) years.push(y);
  });
  const spanEl = document.getElementById('pub-year-span');
  if (spanEl && years.length > 0) {
    const minY = Math.min(...years);
    const maxY = Math.max(...years);
    spanEl.textContent = (maxY - minY + 1);
  }

  // Fade-in animation for publication entries
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('pub-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  items.forEach(function(item, i) {
    item.style.transitionDelay = (i % 4) * 0.08 + 's';
    observer.observe(item);
  });
});
</script>
