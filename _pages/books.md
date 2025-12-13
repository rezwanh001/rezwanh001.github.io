---
layout: page
permalink: /reading/
title: reading shelf
description: "A collection of books I have recently completed."
nav: true
nav_order: 8 # Or any order you prefer

# -----------------------------------------------------------------
# Reading List Data
# Add new books here. The page will automatically update.
# -----------------------------------------------------------------
reading_list:
  - title: Far from the Madding Crowd
    author: Thomas Hardy
    image: /assets/pdf/books/book_far_from_madding.png
    summary: "A fiercely independent woman in pastoral England finds her life entangled with three very different suitors—a story of love, obsession, and the brutal choices that define a life."

  - title: Sense and Sensibility
    author: Jane Austen
    image: /assets/pdf/books/book_sense_and_sensibility.png
    summary: "Two sisters, one guided by reason and the other by passion, navigate the treacherous waters of love, heartbreak, and fortune in Regency society."

  - title: The Adventures of Huckleberry Finn
    author: Mark Twain
    image: /assets/pdf/books/book_huckleberry_finn.png
    summary: "A young outcast and a runaway slave journey down the Mississippi River, seeking freedom from a 'civilized' world in a groundbreaking tale of friendship and morality."
---

<!-- This part of the file is the main content that will be displayed on the page -->

<div class="intro-text" style="margin-bottom: 2rem; text-align: center;">
  <p>Here are some of the books I've had the pleasure of reading. Each offers a unique window into different worlds and ideas.</p>
</div>

<!-- =============================================================== -->
<!-- =================== READING SHELF SECTION ===================== -->
<!-- =============================================================== -->

<div class="row">
{% for book in page.reading_list %}
  <div class="col-md-4 mb-4 d-flex align-items-stretch">
    <div class="card w-100">
      <img src="{{ book.image | relative_url }}" class="card-img-top" alt="{{ book.title }} cover" style="height: 450px; object-fit: cover;">
      <div class="card-body">
        <h5 class="card-title font-weight-bold">{{ book.title }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
        <p class="card-text">{{ book.summary }}</p>
      </div>
    </div>
  </div>
{% endfor %}
</div>
