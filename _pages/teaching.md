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