---
layout: page
permalink: /reading/
title: reading shelf
description: "A collection of books I have recently engaged with."
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
    tags: ["British Literature", "Classic Novel", "Romance"]
    summary: "A fiercely independent woman in pastoral England finds her life entangled with three very different suitors—a story of love, obsession, and the brutal choices that define a life."
    summary_bangla: "এক স্বাধীনচেতা নারী ও তার তিন প্রেমিকের গল্প, যা গ্রামীণ ইংল্যান্ডের পটভূমিতে প্রেম, ত্যাগ এবং নিয়তির অন্বেষণ করে।"

  - title: Sense and Sensibility
    author: Jane Austen
    image: /assets/pdf/books/book_sense_and_sensibility.png
    tags: ["British Literature", "Regency Romance", "Satire"]
    summary: "Two sisters, one guided by reason and the other by passion, navigate the treacherous waters of love, heartbreak, and fortune in Regency society."
    summary_bangla: "দুই বোনের গল্প—একজন যুক্তিবাদী, অন্যজন আবেগপ্রবণ। তাদের প্রেম ও জীবনের নানা প্রতিকূলতার মধ্য দিয়ে পথচলার কাহিনী।"

  - title: The Adventures of Huckleberry Finn
    author: Mark Twain
    image: /assets/pdf/books/book_huckleberry_finn.png
    tags: ["American Literature", "Adventure", "Classic Novel"]
    summary: "A young outcast and a runaway slave journey down the Mississippi River, seeking freedom from a 'civilized' world in a groundbreaking tale of friendship and morality."
    summary_bangla: "এক কিশোরের মুক্তির সন্ধানে মিসিসিপি নদীতে ভেসে যাওয়া, যা বন্ধুত্ব, সমাজ এবং নৈতিকতার এক অবিস্মরণীয় পাঠ দেয়।"

  - title: Wuthering Heights
    author: Emily Brontë
    image: /assets/pdf/books/book_wuthering_heights.png
    tags: ["British Literature", "Gothic Fiction", "Tragedy"]
    summary: "A story of the turbulent and destructive love between Catherine Earnshaw and Heathcliff, and how its unresolved passion ultimately destroys them and many around them."
    summary_bangla: "ক্যাথরিন ও হিথক্লিফের তীব্র, ধ্বংসাত্মক প্রেমের এক মর্মস্পর্শী কাহিনী, যা প্রজন্মের পর প্রজন্ম ধরে প্রতিশোধের আগুন জ্বেলে রাখে।"
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
      <div class="card-body d-flex flex-column">
        <h5 class="card-title font-weight-bold">{{ book.title }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
        
        <!-- Tags Section -->
        <div class="tags-container mb-3">
        {% for tag in book.tags %}
          <span class="badge badge-pill">{{ tag }}</span>
        {% endfor %}
        </div>
        
        <!-- English Summary -->
        <p class="card-text">{{ book.summary }}</p>
        
        <!-- Bangla Summary -->
        {% if book.summary_bangla and book.summary_bangla != "" %}
          <p class="card-text bangla-summary mt-auto">{{ book.summary_bangla }}</p>
        {% endif %}
      </div>
    </div>
  </div>
{% endfor %}
</div>