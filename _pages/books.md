---
layout: page
permalink: /reading/
title: reading
description: "A collection of books I have recently completed."
nav: true
nav_order: 8 # Or any order you prefer

# -----------------------------------------------------------------
# Reading List Data
# The 'category' field is used to create the sections.
# -----------------------------------------------------------------
reading_list:
  - title: The Picture of Dorian Gray
    author: Oscar Wilde
    published_date: 1890
    category: English Literature
    image: /assets/pdf/books/book_dorian_gray.png
    youtube_id: "RD31qRg8XY4"
    gdrive_id: ""
    tags: ["Gothic Fiction", "Philosophical Novel"]
    summary: "The story of the handsome Dorian Gray, who sells his soul for eternal youth. As he indulges in a life of amoral pleasure, his magical portrait, painted by Basil Hallward and influenced by Lord Henry Wotton, bears the scars of his sins and ages in his place."
    summary_bangla: "এক যুবকের গল্প যে তার আত্মার বিনিময়ে চিরযৌবন লাভ করে। তার প্রতিকৃতিতে বয়সের ছাপ পড়ে, আর সে নিজে ডুবে যায় নৈতিক অবক্ষয়ের গভীরে।"

  - title: White Nights
    author: Fyodor Dostoevsky
    published_date: 1848
    category: Russian Literature
    image: /assets/pdf/books/book_white_nights.png
    youtube_id: "yY7YngQE7gI"
    gdrive_id: ""
    tags: ["Short Story", "Romance"]
    summary: "A lonely, unnamed narrator, a dreamer wandering the streets of St. Petersburg, meets the young Nastenka over four nights. He falls deeply in love, only to discover she is waiting for another man, leading to a poignant tale of hope and heartbreak."
    summary_bangla: "এক নিঃসঙ্গ স্বপ্নদর্শী যুবকের সাথে তরুণী নাস্তেনকার সেন্ট পিটার্সবার্গের চারটি রাতের আলাপচারিতার গল্প। এটি একতরফা প্রেম, আশা এবং হৃদয়ভাঙার এক মর্মস্পর্শী আখ্যান।"
    
  - title: Pride and Prejudice
    author: Jane Austen
    published_date: 1813
    category: English Literature
    image: /assets/pdf/books/book_pride_and_prejudice.png
    youtube_id: "GvGb2G1Ft5c"
    gdrive_id: ""
    tags: ["Regency Romance", "Classic Novel"]
    summary: "The classic tale of the spirited Elizabeth Bennet and the proud Mr. Darcy. Through a series of witty encounters and misunderstandings, they must overcome their own pride and prejudices to find love and understanding in the rigid society of Regency England."
    summary_bangla: "গর্বিত মিঃ ডার্সি এবং প্রাণবন্ত এলিজাবেথ বেনেটের গল্প, যারা সামাজিক শ্রেণি ও নিজেদের অহংকারকে জয় করে অবশেষে প্রেমে পড়ে।"

  - title: The Adventures of Huckleberry Finn
    author: Mark Twain
    published_date: 1884
    category: American Literature
    image: /assets/pdf/books/book_huckleberry_finn.png
    youtube_id: "Qhm95D7tdDw"
    gdrive_id: "1kuo2Q4Kw-nLFs5FMDWabPtAG2O4hQD3W"
    tags: ["Adventure", "Classic Novel"]
    summary: "The young outcast Huckleberry Finn and the runaway slave Jim journey down the Mississippi River, seeking freedom in a groundbreaking tale of friendship and morality."
    summary_bangla: "হাকলবেরি ফিন ও জিমের মুক্তির সন্ধানে মিসিসিপি নদীতে ভেসে যাওয়া, যা বন্ধুত্ব, সমাজ এবং নৈতিকতার এক অবিস্মরণীয় পাঠ দেয়।"

  - title: Jane Eyre
    author: Charlotte Brontë
    published_date: 1847
    category: English Literature
    image: /assets/pdf/books/book_jane_eyre.png
    youtube_id: "dgELvs7uM94"
    gdrive_id: ""
    tags: ["Gothic Fiction", "Classic Novel"]
    summary: "The story of the orphaned Jane Eyre, who overcomes a harsh childhood to become a governess at Thornfield Hall. There, she falls for her mysterious employer, Mr. Rochester, but uncovers a terrible secret that tests her love, morality, and quest for independence."
    summary_bangla: "এক অনাথ মেয়ের ভালোবাসা, স্বাধীনতা এবং আত্মমর্যাদা খুঁজে পাওয়ার এক শক্তিশালী ও কালজয়ী কাহিনী।"
---

<!-- This part of the file is the main content that will be displayed on the page -->

<div class="intro-text" style="margin-bottom: 2rem; text-align: center;">
  <p><strong>Here are some of the books I've had the pleasure of reading. Each offers a unique window into different worlds and ideas.</strong></p>
</div>

<!-- =================== DYNAMIC GROUPING LOGIC ===================== -->
{% assign grouped_books = page.reading_list | group_by: "category" %}

{% for group in grouped_books %}
  <h2 class="category-title mt-4 pt-4">{{ group.name }}</h2>
  <hr class="mt-0 mb-4">
  <div class="row">
    {% for book in group.items %}
      <div class="col-md-4 mb-4 d-flex align-items-stretch">
        <div class="card w-100">
          <img src="{{ book.image | relative_url }}" class="card-img-top" alt="{{ book.title }} cover" style="height: 400px; object-fit: cover;">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title font-weight-bold">{{ book.title }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ book.author }}</h6>
            <div class="tags-container mb-3">
              <span class="badge badge-pill badge-date">Published: {{ book.published_date }}</span>
              {% for tag in book.tags %}
                <span class="badge badge-pill badge-genre">{{ tag }}</span>
              {% endfor %}
            </div>
            <p class="card-text">{{ book.summary }}</p>
            {% if book.summary_bangla and book.summary_bangla != "" %}
              <p class="card-text bangla-summary mt-auto">{{ book.summary_bangla }}</p>
            {% endif %}
          </div>
          <div class="card-footer bg-transparent border-top-0 text-center">
            {% if book.youtube_id and book.youtube_id != "" %}
              <button type="button" class="btn btn-outline-primary btn-sm m-1" data-toggle="modal" data-target="#videoModal-{{ book.title | slugify }}">
                <i class="fab fa-youtube"></i> Watch Audiobook
              </button>
            {% endif %}
            {% if book.gdrive_id and book.gdrive_id != "" %}
              <button type="button" class="btn btn-outline-danger btn-sm m-1" data-toggle="modal" data-target="#pdfModal-{{ book.title | slugify }}">
                <i class="fas fa-book-open"></i> Read PDF
              </button>
            {% endif %}
          </div>
        </div>
      </div>
    {% endfor %}
  </div>
{% endfor %}


<!-- =================== MODALS FOR VIDEO AND PDF ===================== -->
{% for book in page.reading_list %}
  <!-- Video Modal -->
  {% if book.youtube_id and book.youtube_id != "" %}
  <div class="modal fade" id="videoModal-{{ book.title | slugify }}" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ book.title }}</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        </div>
        <div class="modal-body">
          <div class="embed-responsive embed-responsive-16by9">
            <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/{{ book.youtube_id }}" allowfullscreen></iframe>
          </div>
        </div>
      </div>
    </div>
  </div>
  {% endif %}

  <!-- PDF Modal -->
  {% if book.gdrive_id and book.gdrive_id != "" %}
  <div class="modal fade" id="pdfModal-{{ book.title | slugify }}" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-xl modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ book.title }}</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        </div>
        <div class="modal-body p-0" style="height: 85vh;">
          <iframe src="https://drive.google.com/file/d/{{ book.gdrive_id }}/preview" width="100%" height="100%" frameborder="0"></iframe>
        </div>
      </div>
    </div>
  </div>
  {% endif %}
{% endfor %}

<!-- JavaScript to stop video when modal is closed -->
<script>
  $(document).ready(function() {
    $('.modal').on('hidden.bs.modal', function (e) {
      var iframe = $(this).find('iframe');
      if (iframe.length > 0) {
        var originalSrc = iframe.attr('src');
        iframe.attr('src', '');
        iframe.attr('src', originalSrc);
      }
    });
  });
</script>