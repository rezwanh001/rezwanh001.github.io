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
    <!-- Contributions spanning sign language recognition, multimodal depression detection,
    medical image analysis, and healthcare AI -->
  </p>
  <p class="pub-last-updated">
    Last updated: {{ site.time | date: "%B %-d, %Y" }}
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
      <span class="pub-stat-label">First / Equal Author</span>
    </div>
    <div class="pub-stat-divider"></div>
    <div class="pub-stat">
      <span class="pub-stat-number" id="pub-award-count">--</span>
      <span class="pub-stat-label">Awards</span>
    </div>
  </div>

  <!-- Yearly publication chart -->
  <div class="pub-yearly-chart" id="pub-yearly-chart"></div>
  <div class="pub-breakdown-legend">
    <span class="pub-legend-item"><span class="pub-legend-dot pub-dot-conf"></span>Conference</span>
    <span class="pub-legend-item"><span class="pub-legend-dot pub-dot-journal"></span>Journal<span class="pub-journal-icon">&#9733;</span></span>
  </div>

  <div class="pub-hero-links">
    <a href="https://scholar.google.com/citations?user=HaI-oFUAAAAJ&hl=en" target="_blank" class="pub-hero-btn">
      <i class="ai ai-google-scholar"></i> Google Scholar
    </a>
    <a href="https://www.researchgate.net/profile/Md-Haque-66" target="_blank" class="pub-hero-btn pub-hero-btn-outline">
      <i class="ai ai-researchgate"></i> ResearchGate
    </a>
  </div>

  <!-- ─── Citation Impact Section ─── -->
  <div class="pub-citation-section">
    <h3 class="pub-citation-title"><i class="fas fa-chart-line"></i> Citation Impact</h3>
    {% assign total_citations = 0 %}
    {% assign highly_cited_papers = 0 %}
    {% for pair in site.data.scholar_citations %}
      {% assign total_citations = total_citations | plus: pair[1] %}
      {% if pair[1] >= 100 %}
        {% assign highly_cited_papers = highly_cited_papers | plus: 1 %}
      {% endif %}
    {% endfor %}

    <div class="pub-citation-cards">
      <div class="pub-citation-card">
        <span class="pub-citation-value">{{ total_citations }}</span>
        <span class="pub-citation-label">Total Citations</span>
        <span class="pub-citation-since">Across publications listed on this page</span>
      </div>
      <div class="pub-citation-card">
        <span class="pub-citation-value">{{ site.data.scholar_citations | size }}</span>
        <span class="pub-citation-label">Cited Papers</span>
        <span class="pub-citation-since">Papers with citation data available</span>
      </div>
      <div class="pub-citation-card pub-citation-card-highlight">
        <span class="pub-citation-value">{{ highly_cited_papers }}</span>
        <span class="pub-citation-label">100+ Citation Papers</span>
        <span class="pub-citation-since">Marked with a star badge in the list below</span>
      </div>
      <div class="pub-citation-card">
        {% assign top_cited = 0 %}
        {% for pair in site.data.scholar_citations %}
          {% if pair[1] > top_cited %}
            {% assign top_cited = pair[1] %}
          {% endif %}
        {% endfor %}
        <span class="pub-citation-value">{{ top_cited }}</span>
        <span class="pub-citation-label">Top Paper Citations</span>
        <span class="pub-citation-since">Highest citation count for a listed paper</span>
      </div>
    </div>

    <div class="pub-cite-chart-label">
      <i class="fas fa-quote-left"></i> Citation counts shown per paper below &middot; Source: <a href="https://scholar.google.com/citations?user=HaI-oFUAAAAJ&hl=en" target="_blank">Google Scholar</a>
    </div>
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

  // Count conference vs journal + build yearly data
  var confCount = 0, journalCount = 0;
  var yearData = {}; // { year: { conf: N, journal: N } }
  items.forEach(function(li) {
    var periodical = li.querySelector('.periodical');
    var isConf = false, isJournal = false;
    if (periodical) {
      var text = periodical.textContent.trim();
      if (text.match(/^In\s/i)) { confCount++; isConf = true; }
      else if (text.length > 0) { journalCount++; isJournal = true; }
    }
    // Extract year from periodical text (last 4-digit number)
    if (periodical) {
      var yearMatch = periodical.textContent.match(/(\d{4})/);
      if (yearMatch) {
        var y = yearMatch[1];
        if (!yearData[y]) yearData[y] = { conf: 0, journal: 0 };
        if (isConf) yearData[y].conf++;
        if (isJournal) yearData[y].journal++;
      }
    }
  });
  var confEl = document.getElementById('pub-conf-count');
  if (confEl) confEl.textContent = confCount;
  var journalEl = document.getElementById('pub-journal-count');
  if (journalEl) journalEl.textContent = journalCount;

  // Count first-author + equal contribution papers
  var firstAuthor = 0;
  items.forEach(function(li) {
    var authorDiv = li.querySelector('.author');
    if (authorDiv) {
      var html = authorDiv.innerHTML.trim();
      // First author: starts with <em> (highlighted name is first)
      if (html.match(/^<em\b/i)) {
        firstAuthor++;
      }
      // Equal contribution: annotation contains "Equal contribution" and user name is in author list
      else {
        var annotation = li.querySelector('.annotation');
        if (annotation && annotation.textContent.indexOf('Equal contribution') !== -1) {
          // Check if user's highlighted name (<em>) appears in authors
          if (authorDiv.querySelector('em')) {
            firstAuthor++;
          }
        }
      }
    }
  });
  var firstEl = document.getElementById('pub-first-author');
  if (firstEl) firstEl.textContent = firstAuthor;

  // Count awards
  var awardCount = document.querySelectorAll('ol.bibliography a.award').length;
  var awardEl = document.getElementById('pub-award-count');
  if (awardEl) awardEl.textContent = awardCount;

  // Build yearly publication chart
  var chartContainer = document.getElementById('pub-yearly-chart');
  if (chartContainer && Object.keys(yearData).length > 0) {
    var years = Object.keys(yearData).sort();
    var maxCount = 0;
    years.forEach(function(y) {
      var t = yearData[y].conf + yearData[y].journal;
      if (t > maxCount) maxCount = t;
    });

    var chartHTML = '<div class="pub-chart-bars">';
    years.forEach(function(y) {
      var total = yearData[y].conf + yearData[y].journal;
      var confPct = maxCount > 0 ? (yearData[y].conf / maxCount) * 100 : 0;
      var journalPct = maxCount > 0 ? (yearData[y].journal / maxCount) * 100 : 0;
      chartHTML += '<div class="pub-chart-col">';
      chartHTML += '<span class="pub-chart-count">' + total + '</span>';
      chartHTML += '<div class="pub-chart-bar-wrapper">';
      if (yearData[y].journal > 0) {
        chartHTML += '<div class="pub-chart-bar pub-chart-bar-journal" style="height:' + journalPct + '%" title="' + yearData[y].journal + ' journal paper' + (yearData[y].journal > 1 ? 's' : '') + '"><span class="pub-chart-bar-label">&#9733;</span></div>';
      }
      if (yearData[y].conf > 0) {
        chartHTML += '<div class="pub-chart-bar pub-chart-bar-conf" style="height:' + confPct + '%" title="' + yearData[y].conf + ' conference paper' + (yearData[y].conf > 1 ? 's' : '') + '"></div>';
      }
      chartHTML += '</div>';
      chartHTML += '<span class="pub-chart-year">' + y + '</span>';
      chartHTML += '</div>';
    });
    chartHTML += '</div>';
    chartContainer.innerHTML = chartHTML;

    // Animate bars in
    setTimeout(function() {
      chartContainer.classList.add('pub-chart-visible');
    }, 200);
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

  // Animate citation chart bars
  var citeBars = document.querySelectorAll('.pub-cite-chart-bar');
  if (citeBars.length > 0) {
    setTimeout(function() {
      citeBars.forEach(function(bar, idx) {
        setTimeout(function() {
          bar.style.height = bar.getAttribute('data-height') + '%';
        }, idx * 60);
      });
    }, 400);
  }
});
</script>
