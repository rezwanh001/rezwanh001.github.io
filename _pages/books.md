---
layout: page
permalink: /reading/
title: reading shelf
description: "A collection of books I have recently completed."
nav: true
nav_order: 8 # Or any order you prefer

# -----------------------------------------------------------------
# Reading List Data
# -----------------------------------------------------------------
reading_list:
  - title: Far from the Madding Crowd
    author: Thomas Hardy
    image: /assets/pdf/books/book_far_from_madding.png
    tags: ["British Literature", "Classic Novel", "Romance"]
    summary: "Follows the fiercely independent Bathsheba Everdene as she navigates the affections of three distinct suitors: the loyal shepherd Gabriel Oak, the obsessive farmer William Boldwood, and the dashing Sergeant Troy."
    summary_bangla: "এক স্বাধীনচেতা নারী বাথশেবা এভারডিন ও তার তিন প্রেমিকের গল্প, যা গ্রামীামীণ ইংল্যান্ডের পটভূমিতে প্রেম, ত্যাগ এবং নিয়তির অন্বেষণ করে।"

  - title: Sense and Sensibility
    author: Jane Austen
    image: /assets/pdf/books/book_sense_and_sensibility.png
    tags: ["British Literature", "Regency Romance", "Satire"]
    summary: "The story of the Dashwood sisters, Elinor and Marianne. One guided by reason and the other by passion, they navigate love, heartbreak, and fortune in Regency society."
    summary_bangla: "দুই বোন এলিনর ও ম্যারিয়েন—একজন যুক্তিবাদী, অন্যজন আবেগপ্রবণ। তাদের প্রেম ও জীবনের নানা প্রতিকূলতার মধ্য দিয়ে পথচলার কাহিনী।"

  - title: The Adventures of Huckleberry Finn
    author: Mark Twain
    image: /assets/pdf/books/book_huckleberry_finn.png
    tags: ["American Literature", "Adventure", "Classic Novel"]
    summary: "The young outcast Huckleberry Finn and the runaway slave Jim journey down the Mississippi River, seeking freedom in a groundbreaking tale of friendship and morality."
    summary_bangla: "হাকলবেরি ফিন ও জিমের মুক্তির সন্ধানে মিসিসিপি নদীতে ভেসে যাওয়া, যা বন্ধুত্ব, সমাজ এবং নৈতিকতার এক অবিস্মরণীয় পাঠ দেয়।"

  - title: Wuthering Heights
    author: Emily Brontë
    image: /assets/pdf/books/book_wuthering_heights.png
    tags: ["British Literature", "Gothic Fiction", "Tragedy"]
    summary: "A story of the turbulent and destructive love between Catherine Earnshaw and the enigmatic Heathcliff, and how its unresolved passion ultimately destroys them and many around them."
    summary_bangla: "ক্যাথরিন ও হিথক্লিফের তীব্র, ধ্বংসাত্মক প্রেমের এক মর্মস্পর্শী কাহিনী, যা প্রজন্মের পর প্রজন্ম ধরে প্রতিশোধের আগুন জ্বেলে রাখে।"

  - title: The Merchant of Venice
    author: William Shakespeare
    image: /assets/pdf/books/book_merchant_of_venice.png
    tags: ["Play", "Tragicomedy", "English Literature"]
    summary: "A tale of love, prejudice, and justice where Bassanio's quest to win the hand of Portia leads his friend Antonio to make a dangerous bargain with the moneylender Shylock."
    summary_bangla: "প্রেম, প্রতিশোধ এবং ন্যায়বিচারের এক জটিল কাহিনী, যেখানে এক পাউন্ড মাংসের চুক্তিকে ঘিরে নাটকীয়তা আবর্তিত হয়।"

  - title: Hamlet
    author: William Shakespeare
    image: /assets/pdf/books/book_hamlet.png
    tags: ["Play", "Tragedy", "English Literature"]
    summary: "Prince Hamlet of Denmark seeks revenge on his uncle Claudius, who has murdered his father and married his mother, Gertrude, driving him to the edge of madness and moral conflict."
    summary_bangla: "প্রতিশোধের দ্বন্দ্বে জর্জরিত ডেনমার্কের রাজপুত্র হ্যামলেটের গল্প, যা অস্তিত্ব, পাগলামি এবং নৈতিকতার প্রশ্ন তোলে।"

  - title: Othello
    author: William Shakespeare
    image: /assets/pdf/books/book_othello.png
    tags: ["Play", "Tragedy", "English Literature"]
    summary: "The tragic downfall of the Moorish general Othello, whose mind is poisoned by the master manipulator Iago, leading him to doubt the fidelity of his beloved wife, Desdemona."
    summary_bangla: "ইয়াগোর ষড়যন্ত্রে ঈর্ষার আগুনে পুড়ে যাওয়া মহান সেনাপতি ওথেলো এবং তার স্ত্রী ডেসডিমোনার করুণ পরিণতি।"

  - title: Macbeth
    author: William Shakespeare
    image: /assets/pdf/books/book_macbeth.png
    tags: ["Play", "Tragedy", "English Literature"]
    summary: "A story of unchecked ambition, where the Scottish general Macbeth, spurred by a prophecy and his wife Lady Macbeth, murders his way to the throne, only to be consumed by guilt and paranoia."
    summary_bangla: "ক্ষমতার লোভে এক স্কটিশ জেনারেল ম্যাকবেথের নৈতিক পতনের এক অন্ধকার এবং রক্তক্ষয়ী কাহিনী।"
---

<!-- This part of the file is the main content that will be displayed on the page -->

<div class="intro-text" style="margin-bottom: 2rem; text-align: center;">
  <p><strong>Here are some of the books I've had the pleasure of reading. Each offers a unique window into different worlds and ideas.</strong></p>
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
        
        <!-- Tags Section with Golden Color -->
        <div class="tags-container mb-3">
        {% for tag in book.tags %}
          <span class="badge badge-pill badge-golden">{{ tag }}</span>
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