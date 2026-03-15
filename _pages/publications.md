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
      <span class="pub-stat-number" id="pub-conf-count">--</span>
      <span class="pub-stat-label">Conference</span>
    </div>
    <div class="pub-stat-divider"></div>
    <div class="pub-stat">
      <span class="pub-stat-number" id="pub-journal-count">--</span>
      <span class="pub-stat-label">Journal</span>
    </div>
    <div class="pub-stat-divider"></div>
    <div class="pub-stat">
      <span class="pub-stat-number" id="pub-first-author">--</span>
      <span class="pub-stat-label">First Author</span>
    </div>
    <div class="pub-stat-divider"></div>
    <div class="pub-stat">
      <span class="pub-stat-number" id="pub-q1-count">--</span>
      <span class="pub-stat-label">Q1 Journals</span>
    </div>
    <div class="pub-stat-divider"></div>
    <div class="pub-stat">
      <span class="pub-stat-number" id="pub-award-count">--</span>
      <span class="pub-stat-label">Awards</span>
    </div>
  </div>

  <!-- Visual breakdown bar -->
  <div class="pub-breakdown">
    <div class="pub-breakdown-bar">
      <div class="pub-bar-segment pub-bar-conf" id="pub-bar-conf" title="Conference Papers"></div>
      <div class="pub-bar-segment pub-bar-q1" id="pub-bar-q1" title="Q1 Journal Papers"></div>
      <div class="pub-bar-segment pub-bar-journal" id="pub-bar-journal" title="Other Journal Papers"></div>
    </div>
    <div class="pub-breakdown-legend">
      <span class="pub-legend-item"><span class="pub-legend-dot pub-dot-conf"></span>Conference</span>
      <span class="pub-legend-item"><span class="pub-legend-dot pub-dot-q1"></span>Q1 Journal</span>
      <span class="pub-legend-item"><span class="pub-legend-dot pub-dot-journal"></span>Other Journal</span>
    </div>
  </div>

  <div class="pub-hero-links">
    <a href="https://scholar.google.com/citations?user=HaI-oFUAAAAJ&hl=en" target="_blank" class="pub-hero-btn">
      <i class="ai ai-google-scholar"></i> Google Scholar
    </a>
    <a href="https://www.researchgate.net/profile/Md-Haque-66" target="_blank" class="pub-hero-btn pub-hero-btn-outline">
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
  var items = document.querySelectorAll('ol.bibliography > li');
  var totalEl = document.getElementById('pub-total-count');
  if (totalEl) totalEl.textContent = items.length;

  // Count conference vs journal
  var confCount = 0, journalCount = 0;
  items.forEach(function(li) {
    var periodical = li.querySelector('.periodical');
    if (periodical) {
      var text = periodical.textContent.trim();
      if (text.match(/^In\s/i)) {
        confCount++;
      } else if (text.length > 0) {
        journalCount++;
      }
    }
  });
  var confEl = document.getElementById('pub-conf-count');
  if (confEl) confEl.textContent = confCount;
  var journalEl = document.getElementById('pub-journal-count');
  if (journalEl) journalEl.textContent = journalCount;

  // Count first-author papers (user's name is in <em> tag in .author)
  var firstAuthor = 0;
  items.forEach(function(li) {
    var authorDiv = li.querySelector('.author');
    if (authorDiv) {
      // Check if the first author element is <em> (self)
      var firstChild = authorDiv.firstElementChild;
      if (firstChild && firstChild.tagName === 'EM') {
        firstAuthor++;
      }
    }
  });
  var firstEl = document.getElementById('pub-first-author');
  if (firstEl) firstEl.textContent = firstAuthor;

  // Count awards
  var awardCount = document.querySelectorAll('ol.bibliography .award').length;
  var awardEl = document.getElementById('pub-award-count');
  if (awardEl) awardEl.textContent = awardCount;

  // Count Q1 journal papers (abbr badge contains "Q1")
  var q1Count = 0;
  items.forEach(function(li) {
    var abbrEl = li.querySelector('.abbr abbr');
    if (abbrEl && abbrEl.textContent.indexOf('Q1') !== -1) {
      q1Count++;
    }
  });
  var q1El = document.getElementById('pub-q1-count');
  if (q1El) q1El.textContent = q1Count;

  var otherJournal = journalCount - q1Count;

  // Visual breakdown bar (3 segments)
  var total = confCount + journalCount;
  if (total > 0) {
    var confBar = document.getElementById('pub-bar-conf');
    var q1Bar = document.getElementById('pub-bar-q1');
    var journalBar = document.getElementById('pub-bar-journal');
    if (confBar) confBar.style.width = ((confCount / total) * 100) + '%';
    if (q1Bar) q1Bar.style.width = ((q1Count / total) * 100) + '%';
    if (journalBar) journalBar.style.width = ((otherJournal / total) * 100) + '%';
  }

  // Add publication count badge to each year heading
  var yearHeaders = document.querySelectorAll('h2.bibliography');
  yearHeaders.forEach(function(h2) {
    var nextEl = h2.nextElementSibling;
    while (nextEl && !nextEl.matches('ol.bibliography')) {
      nextEl = nextEl.nextElementSibling;
    }
    if (nextEl) {
      var count = nextEl.querySelectorAll(':scope > li').length;
      if (count > 0) {
        var badge = document.createElement('span');
        badge.className = 'pub-year-count';
        badge.textContent = count + (count === 1 ? ' paper' : ' papers');
        h2.appendChild(badge);
      }
    }
  });

  // Fade-in animation for publication entries
  var observer = new IntersectionObserver(function(entries) {
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
