---
layout: page
permalink: /repositories/
title: repositories
description: Open-source projects and research code repositories.
nav: true
nav_order: 4
---

<!-- ═══════════════════════  Hero Section  ═══════════════════════ -->
<div class="repo-hero">
  <div class="repo-hero-icon">
    <i class="fa-brands fa-github"></i>
  </div>
  <h2 class="repo-hero-title">Open Source & Research Code</h2>
  <p class="repo-hero-subtitle">
    Publicly available implementations of research papers, tools, and experiments
  </p>
  <div class="repo-hero-stats">
    <div class="repo-stat">
      <span class="repo-stat-number" id="repo-total-count">--</span>
      <span class="repo-stat-label">Repositories</span>
    </div>
    <div class="repo-stat-divider"></div>
    <div class="repo-stat">
      <span class="repo-stat-number"><i class="fas fa-code-branch" style="font-size:0.9em"></i></span>
      <span class="repo-stat-label">Active Development</span>
    </div>
  </div>
  <a href="https://github.com/rezwanh001" target="_blank" class="repo-hero-btn">
    <i class="fa-brands fa-github"></i> View GitHub Profile
  </a>
</div>

{% if site.data.repositories.github_users %}

<!-- ═══════════════════════  GitHub Profile  ═══════════════════════ -->
<div class="repo-section">
  <div class="repo-section-header">
    <i class="fas fa-user-circle"></i>
    <h3>GitHub Profile</h3>
  </div>
  <div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
    {% for user in site.data.repositories.github_users %}
      {% include repository/repo_user.liquid username=user %}
    {% endfor %}
  </div>
</div>

---

{% if site.repo_trophies.enabled %}
{% for user in site.data.repositories.github_users %}
{% if site.data.repositories.github_users.size > 1 %}
<h4>{{ user }}</h4>
{% endif %}
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo_trophies.liquid username=user %}
</div>

---

{% endfor %}
{% endif %}
{% endif %}

{% if site.data.repositories.github_repos %}

<!-- ═══════════════════════  Repositories Grid  ═══════════════════════ -->
<div class="repo-section">
  <div class="repo-section-header">
    <i class="fas fa-code"></i>
    <h3>Research & Project Repositories</h3>
  </div>
  <div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
    {% for repo in site.data.repositories.github_repos %}
      {% include repository/repo.liquid repository=repo %}
    {% endfor %}
  </div>
</div>
{% endif %}

<!-- ═══════════════════════  Stats Counter JS  ═══════════════════════ -->
<script>
document.addEventListener('DOMContentLoaded', function() {
  var repoCards = document.querySelectorAll('.repo');
  var countEl = document.getElementById('repo-total-count');
  // Count only repo pin cards (not the user overview card)
  var repoCount = 0;
  repoCards.forEach(function(c) {
    var imgs = c.querySelectorAll('img');
    imgs.forEach(function(img) {
      if (img.src && img.src.indexOf('/pin/') !== -1) repoCount++;
    });
  });
  // Each repo has light+dark img, divide by 2
  repoCount = Math.round(repoCount / 2);
  if (countEl && repoCount > 0) countEl.textContent = repoCount;

  // Fade-in animation for repo cards
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('repo-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  repoCards.forEach(function(card, i) {
    card.style.transitionDelay = (i % 3) * 0.1 + 's';
    card.classList.add('repo-animate');
    observer.observe(card);
  });
});
</script>
