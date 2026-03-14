---
layout: page
permalink: /teaching/
title: teaching
nav: true
nav_order: 6
---

<h3 style="margin-bottom: 0.25rem;"><i class="fa-solid fa-graduation-cap"></i> University of Waterloo</h3>
<p style="color: var(--global-text-color-light, #6c757d); font-size: 0.9rem; margin-bottom: 2rem;">
  My teaching journey — click any course to see the full details.
</p>

<div class="teaching-timeline">

  <!-- ═══ PhD Section ═══ -->
  <div class="timeline-degree-section">
    <div class="timeline-degree-badge phd">
      <i class="fa-solid fa-user-graduate"></i> PhD · Electrical &amp; Computer Engineering
    </div>
  </div>

  <div class="timeline-item">
    <div class="timeline-card timeline-placeholder" style="--timeline-accent: #6610f2;">
      <div class="timeline-header">
        <h4 class="timeline-course-title">
          <span class="timeline-course-icon">🎓</span>
          PhD TA — Coming Soon
        </h4>
        <span class="timeline-term-badge" style="background: #6610f2;">
          🗓️ Spring 2026
        </span>
      </div>
      <div style="font-size: 0.9rem; color: var(--global-text-color-light, #6c757d);">
        Teaching Assistant (TA) · University of Waterloo
      </div>
      <div class="timeline-meta">
        <span class="timeline-stat" style="font-style: italic;">
          <i class="fa-solid fa-clock"></i>&nbsp; Course assignment pending
        </span>
      </div>
    </div>
  </div>

  <!-- ═══ MASc Section ═══ -->
  <div class="timeline-degree-section">
    <div class="timeline-degree-badge masc">
      <i class="fa-solid fa-microchip"></i> MASc · Electrical &amp; Computer Engineering
    </div>
  </div>

  {% assign sorted_courses = site.teaching | sort: "order" %}
  {% for course in sorted_courses %}
  <div class="timeline-item">
    <div class="timeline-card" style="--timeline-accent: {{ course.color }};">
      <div class="timeline-header">
        <h4 class="timeline-course-title">
          <span class="timeline-course-icon">{{ course.icon }}</span>
          <a href="{{ course.url | relative_url }}">{{ course.title }}</a>
        </h4>
        <span class="timeline-term-badge" style="background: {{ course.color }};">
          🗓️ {{ course.term }}
        </span>
      </div>
      <div style="font-size: 0.9rem; color: var(--global-text-color-light, #6c757d);">
        {{ course.role }} · {{ course.university }}
      </div>
      <div class="timeline-meta">
        <span class="timeline-stat">👥 <strong>{{ course.enrollment }}</strong> students</span>
        <span class="timeline-stat">
          <span class="timeline-stars">{{ course.rating_stars }}</span>
          <span>{{ course.rating_type }}: {{ course.rating }}</span>
        </span>
        <a href="{{ course.url | relative_url }}" class="timeline-arrow-link" style="color: {{ course.color }};">
          View Details <i class="fa-solid fa-arrow-right"></i>
        </a>
      </div>
    </div>
  </div>
  {% endfor %}
  <div class="timeline-end">
    <i class="fa-solid fa-flag-checkered"></i> Beginning of TA journey
  </div>
</div> 