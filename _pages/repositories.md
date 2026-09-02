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
      <span class="repo-stat-number" id="repo-total-count">{{ site.data.repositories.github_repos | size }}</span>
      <span class="repo-stat-label">Paper Repositories</span>
    </div>
    <div class="repo-stat-divider"></div>
    <div class="repo-stat">
      <span class="repo-stat-number" id="repo-github-count">{{ site.data.repositories.github_user.public_repos }}</span>
      <span class="repo-stat-label">Public Repos on GitHub</span>
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
    <h3>Research Paper Repositories</h3>
  </div>
  <div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
    {% for repo in site.data.repositories.github_repos %}
      {% include repository/repo.liquid repository=repo %}
    {% endfor %}
  </div>
</div>
{% endif %}

<!-- ═══════════════════════  Stats + Live-Refresh JS  ═══════════════════════ -->
<!--
  Cards render from baked data (see _data/repositories.yml), so nothing ever
  appears broken. This script only *enhances* them: it counts the cards for
  the hero, and opportunistically refreshes star / fork / follower counts from
  the public GitHub API. Every network call fails silently — on rate-limit or
  offline the baked numbers simply stay. No third-party image service involved.
-->
<script>
document.addEventListener('DOMContentLoaded', function () {
  var repoCards = document.querySelectorAll('.repo');
  var paperCards = document.querySelectorAll('.repo-card[data-repo]');

  // Hero: number of paper repositories shown on this page.
  var countEl = document.getElementById('repo-total-count');
  if (countEl) countEl.textContent = paperCards.length;

  // Hero: total public repos — live-refresh over the baked fallback.
  var ghCountEl = document.getElementById('repo-github-count');

  function setNum(el, value) {
    if (el && typeof value === 'number' && !isNaN(value)) el.textContent = value;
  }

  // --- Live refresh: user profile (repos / followers / following) ---
  var userCard = document.querySelector('.repo-card-user[data-user]');
  if (userCard) {
    fetch('https://api.github.com/users/' + userCard.getAttribute('data-user'))
      .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
      .then(function (d) {
        setNum(ghCountEl, d.public_repos);
        var map = { repos: d.public_repos, followers: d.followers, following: d.following };
        Object.keys(map).forEach(function (k) {
          var span = userCard.querySelector('[data-stat="' + k + '"] .repo-card-num');
          setNum(span, map[k]);
        });
      })
      .catch(function () { /* keep baked values */ });
  }

  // --- Live refresh: each repo card (stars / forks) ---
  paperCards.forEach(function (card) {
    fetch('https://api.github.com/repos/' + card.getAttribute('data-repo'))
      .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
      .then(function (d) {
        var s = card.querySelector('[data-stat="stars"] .repo-card-num');
        var f = card.querySelector('[data-stat="forks"] .repo-card-num');
        setNum(s, d.stargazers_count);
        setNum(f, d.forks_count);
      })
      .catch(function () { /* keep baked values */ });
  });

  // --- Fade-in animation ---
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('repo-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  repoCards.forEach(function (card, i) {
    card.style.transitionDelay = (i % 3) * 0.1 + 's';
    card.classList.add('repo-animate');
    observer.observe(card);
  });
});
</script>
