---
layout: post
title: "Embodied IQA — A Plain Guide: What the Papers Say, What Is Missing, and What I Want to Build"
description: "A simple, jargon-light companion to the deep review. Each paper in four short sentences, a glossary of the abbreviations, the seven gaps that still block progress, and the research pipeline I plan to follow — from a noise-ceiling audit to a task-aware quality metric that tells a robot where to move."
date: 2026-08-10
tags: [world-models, embodied-ai, active-perception, iqa, resources, deep-dives]
categories: world-models
wm_resource: true
giscus_comments: true
related_posts: false
mermaid:
  enabled: true
  zoomable: true
---

<div class="wm-backlink">
  <a href="{{ '/blog/world-models/' | relative_url }}">&larr; Blogs · <strong>World Models</strong> series</a>
</div>

{% raw %}

This is the easy-reading version of my earlier deep review. That post has every table and every number. This one has the story, in plain words.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>এটি আমার আগের গভীর রিভিউয়ের সহজপাঠ্য সংস্করণ। ওই লেখায় প্রতিটি টেবিল ও প্রতিটি সংখ্যা আছে; এখানে আছে সেই গল্পটাই — সহজ ভাষায়।</p>
</div>

---

## The one idea

For fifty years we have measured picture quality by asking people. Does this photo look sharp? Does the compression look ugly? That question built the whole field of **Image Quality Assessment (IQA)**.

But today, most images are never seen by a person. A robot looks at them, and then it acts.

So the question changes. It is no longer *"does this image look good?"* It becomes *"can a robot still do its job with this image?"*

Those two questions have different answers. That gap is the whole research area.

> **The short version.** Two papers show that robots and humans disagree about image quality, and they build the databases to prove it. A third paper shows that a good quality score can be used to decide *where a robot should look next*. Nobody has combined the two. That combination is what I want to build.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>পঞ্চাশ বছর ধরে আমরা ছবির মান মেপেছি মানুষকে জিজ্ঞেস করে — "ছবিটা কি পরিষ্কার দেখাচ্ছে? কম্প্রেশনের দাগ কি চোখে লাগছে?" এই প্রশ্ন থেকেই গড়ে উঠেছে <strong>Image Quality Assessment (IQA)</strong>-এর পুরো ক্ষেত্র। কিন্তু আজকাল বেশিরভাগ ছবি কোনো মানুষ দেখেই না — একটি রোবট ছবিটি দেখে, তারপর সেই অনুযায়ী কাজ করে। তাই প্রশ্নটাও বদলে যায়: এখন আর <em>"ছবিটা কি সুন্দর দেখাচ্ছে?"</em> নয়, বরং <em>"এই ছবি দিয়ে রোবট কি তার কাজটা করতে পারবে?"</em> — এই দুই প্রশ্নের উত্তর আলাদা, আর এই ফাঁকটাই পুরো গবেষণার বিষয়।</p>
  <p><strong>সংক্ষেপে:</strong> দুটি গবেষণাপত্র দেখায় রোবট ও মানুষ ছবির মান নিয়ে একমত নয় (এবং তা প্রমাণে ডেটাবেস বানায়); তৃতীয় একটি দেখায় একটি ভালো মান-স্কোর দিয়ে ঠিক করা যায় <em>রোবট এরপর কোথায় তাকাবে</em>। কেউ এ দুটোকে একসাথে করেনি — সেই সংযোগটাই আমি বানাতে চাই।</p>
</div>

---

## Glossary

Read this once and the rest of the post becomes easy.

| Short form | Full name | What it means here |
|---|---|---|
| **IQA** | Image Quality Assessment | Giving an image a quality score |
| **HVS** | Human Visual System | How people judge an image |
| **MVS** | Machine Visual System | How a normal computer-vision model judges it |
| **RVS** | Robot Visual System | How a robot judges it — because a robot must also *move* |
| **VLM** | Vision-Language Model | Looks at an image and writes text. The "understanding" part |
| **VLA** | Vision-Language-Action model | Looks at an image and outputs a robot movement. The "deciding" part |
| **RL** | Reinforcement Learning | Learning by trial, reward, and error |
| **FR-IQA** | Full-Reference IQA | Scoring needs a clean original to compare against |
| **NR-IQA** | No-Reference IQA | Scoring with no original at all |
| **CR-IQA** | Cross-Reference IQA | Scoring by comparing with *other views of the same scene* |
| **NVS** | Novel View Synthesis | Making a new photo of a scene from an angle you never photographed |
| **3DGS** | 3D Gaussian Splatting | A fast, popular way to store a 3D scene |
| **SRCC / PLCC / KRCC** | Spearman / Pearson / Kendall correlation | How closely a metric agrees with the truth. 1.0 is perfect, 0 is useless |
| **DoF** | Degrees of Freedom | How many numbers describe a robot arm's pose. Usually 7 |
| **MOS / DMOS** | (Difference) Mean Opinion Score | The average quality rating for an image |

One rule of thumb for the numbers below: on normal human-facing IQA, good metrics reach about **SRCC 0.9**. Keep that in mind, because the robot numbers are much lower.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>উপরের সংক্ষিপ্ত রূপগুলো একবার পড়ে নিলে বাকি লেখা সহজ হয়ে যায় — <strong>IQA</strong> (ছবির মান যাচাই), <strong>HVS</strong> (মানুষের দৃষ্টিব্যবস্থা), <strong>MVS</strong> (সাধারণ কম্পিউটার-ভিশন মডেলের বিচার), <strong>RVS</strong> (রোবটের বিচার — কারণ রোবটকে <em>নড়াচড়াও</em> করতে হয়), <strong>VLM</strong> (ছবি দেখে লেখা তৈরি করে — "বোঝার" অংশ), <strong>VLA</strong> (ছবি দেখে রোবটের নড়াচড়া ঠিক করে — "সিদ্ধান্তের" অংশ), <strong>FR/NR/CR-IQA</strong> (মূল ছবি সহ / মূল ছবি ছাড়া / একই দৃশ্যের অন্য ভিউয়ের সাথে তুলনা করে মান নির্ণয়), <strong>SRCC/PLCC/KRCC</strong> (মেট্রিক সত্যের সাথে কতটা মেলে — ১.০ নিখুঁত, ০ অকেজো)।</p>
  <p>একটি নিয়ম মনে রাখুন: সাধারণ মানুষ-কেন্দ্রিক IQA-তে ভালো মেট্রিক প্রায় <strong>SRCC ০.৯</strong> পায়; রোবটের ক্ষেত্রে সংখ্যাগুলো অনেক কম — সেটাই এই লেখার মূল বিষয়।</p>
</div>

---

## Part 1 — The two main papers

### Paper 1 · Image Quality Assessment for Embodied AI (*Embodied-IQA*)

*Shanghai Jiao Tong University, Shanghai AI Lab, and NTU · October 2025*

- **The problem.** A robot has three steps after it sees something: it must *understand* the scene, then *decide* a movement, then *execute* that movement. A tiny mistake in understanding can become a large mistake in movement, so the authors argue that quality must be measured at all three steps, not just the first one.
- **The data.** They took 1,230 clean robot photos, damaged them in 30 different ways at 5 strength levels to make **36,900 damaged images**, asked people to write 5 tasks for each photo in plain English, and then let **15 VLMs, 15 VLAs, and one real UR5 robot arm** score them — about **5.53 million labels** in total.
- **The method.** There is no new neural network here. The contribution is the *recipe*: measure understanding by comparing the model's sentences before and after damage, measure decision by comparing the 7-DoF arm poses, and measure execution by how far the real arm ended up from where it should have been.
- **The result.** The best existing metric reached only **SRCC 0.775**, far below the 0.9 that the same metrics get on human data — and some popular metrics (LPIPS, DISTS, CLIPIQA) scored *worse than plain PSNR*, because their weights are frozen on human taste.

**What stayed with me.** Damage level and damage effect are not the same thing. A very light block-loss that happens to erase the target object dropped the score to 2.98. A very heavy distortion somewhere else in the image still scored 4.52. The robot only cares about the part of the image it needs.

### Paper 2 · Embodied Image Quality Assessment for Robotic Intelligence (*EPD* and *MA-EIQA*)

*Same research family, earlier and smaller · August 2025*

- **The problem.** Ask whether robots and humans simply want different things from an image, and then build a quality database that is scored **by a robot doing a task, with no human involved at all**.
- **The data.** In a simulator, a robot arm tried two jobs — push a box and pick a box — across 100 starting scenes, with 25 kinds of damage at 5 levels, giving **12,500 image pairs**. The clever part: the image's quality score is simply **how much reward the robot earned in that episode**.
- **The method.** They built **MA-EIQA**, a small no-reference model. It reads an image at several zoom levels at once, then uses attention to focus on the regions that matter, then outputs one number. It was deliberately kept small (48.83 million parameters) so it can run on a robot's own limited hardware.
- **The result.** Their model reached **SRCC 0.5755**, slightly ahead of much larger models, but still low. More importantly, human and robot opinions barely agreed at all — **PLCC of only 0.13 to 0.21**.

**What stayed with me.** The ranking of what hurts. Motion blur and noise, which people hate, barely disturbed the robot. Colour distortion and darkening, which people tolerate easily, were the most damaging. Our instincts about "bad images" are simply not the robot's instincts.

### Paper 3 · Active View Selector (*AVS*)

*Oxford, Active Vision Lab and VGG · June 2025 · this one uses quality to act*

- **The problem.** When a robot builds a 3D model of a room, it must choose where to point the camera next. Older methods calculate uncertainty inside the 3D model, which is slow and must be rewritten for every kind of 3D representation.
- **The data.** No human labelling. They fit 3D scenes to hundreds of ordinary videos, and every so often compared a rendered view against the real photo. Those automatic comparisons became the training data.
- **The method.** A small network looks at a rendered view *together with a few real photos of the same scene from other angles* — this is **CR-IQA** — and predicts where the render looks wrong. Then the rule is simply: **go to the view that looks worst.** They call it "boost where it struggles".
- **The result.** Better 3D reconstructions than the previous best method, while running **14 to 33 times faster** and using half the memory — about 0.6 seconds to check roughly 200 candidate viewpoints.

**What stayed with me.** Two things. First, the trick of using *other viewpoints* as a stand-in for the missing original — for a robot this is free, because it already has its own earlier frames. Second, speed is not the obstacle. This runs comfortably inside a control loop.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p><strong>পেপার ১ · Embodied-IQA</strong> (SJTU, Shanghai AI Lab, NTU · অক্টোবর ২০২৫): রোবটের তিনটি ধাপ — দৃশ্য <em>বোঝা</em>, নড়াচড়া <em>ঠিক করা</em>, তা <em>সম্পাদন করা</em> — তাই মান তিন ধাপেই মাপা উচিত, শুধু প্রথমটিতে নয়। ১,২৩০টি পরিষ্কার ছবিকে ৩০ রকমে ও ৫ মাত্রায় নষ্ট করে <strong>৩৬,৯০০</strong> নষ্ট ছবি, এরপর ১৫টি VLM, ১৫টি VLA ও একটি বাস্তব UR5 রোবট-বাহু দিয়ে স্কোর করে প্রায় <strong>৫৫ লক্ষ লেবেল</strong>। সেরা মেট্রিকও মাত্র <strong>SRCC ০.৭৭৫</strong> পায় (মানুষের ডেটায় যা ০.৯); কিছু জনপ্রিয় মেট্রিক (LPIPS, DISTS, CLIPIQA) সাধারণ PSNR-এর চেয়েও খারাপ করে। শিক্ষা: ক্ষতির <em>মাত্রা</em> আর ক্ষতির <em>প্রভাব</em> এক নয় — রোবট কেবল ছবির দরকারি অংশটুকুর পরোয়া করে।</p>
  <p><strong>পেপার ২ · EPD ও MA-EIQA</strong> (আগস্ট ২০২৫): সিমুলেটরে রোবট-বাহু দুটি কাজ (বাক্স ঠেলা ও তোলা) করে, কোনো মানুষ ছাড়াই — ছবির স্কোর = রোবট সেই পর্বে কত <em>রিওয়ার্ড</em> পেল। তাদের ছোট মডেল <strong>MA-EIQA</strong> (৪৮.৮৩M প্যারামিটার) <strong>SRCC ০.৫৭৫৫</strong> পায়; মানুষ ও রোবটের মত প্রায় মেলেই না (<strong>PLCC মাত্র ০.১৩–০.২১</strong>)। মোশন-ব্লার ও নয়েজ, যা মানুষ অপছন্দ করে, রোবটকে তেমন ভোগায় না; অথচ রঙের বিকৃতি ও অন্ধকার সবচেয়ে ক্ষতিকর।</p>
  <p><strong>পেপার ৩ · Active View Selector (AVS)</strong> (Oxford · জুন ২০২৫): রোবট যখন ঘরের 3D মডেল বানায়, পরবর্তীতে ক্যামেরা কোথায় তাক করবে তা বেছে নিতে হয়। এরা একটি রেন্ডার-ভিউকে <em>একই দৃশ্যের কয়েকটি বাস্তব ছবির সাথে</em> তুলনা করে (<strong>CR-IQA</strong>) বোঝে কোথায় রেন্ডার খারাপ, আর নিয়ম সহজ: <strong>যে ভিউ সবচেয়ে খারাপ, সেখানেই যাও</strong>। আগের সেরা পদ্ধতির চেয়ে ভালো ফল, <strong>১৪–৩৩ গুণ দ্রুত</strong>, অর্ধেক মেমরি — প্রায় ২০০টি ভিউ যাচাই মাত্র ০.৬ সেকেন্ডে। মজার কথা: রোবটের কাছে <em>অন্য ভিউ</em> বিনামূল্যে, কারণ তার নিজের আগের ফ্রেমগুলোই আছে।</p>
</div>

---

## Part 2 — Recent related work

Short versions. Full details are in the deep review.

- **MPD** (CVPR 2025) — the same group's earlier database. 30,000 damaged images scored by 15 large multimodal models and 15 specialist models across 7 tasks. Its most useful finding: different downstream tasks *disagree with each other*, so one model is never enough as a judge.
- **MIQD-2.5M and RA-MIQA** (2025) — a completely different group reached the same conclusion with 2.5 million images and 75 models. Two independent confirmations means the premise is solid. They also score quality **per region** rather than for the whole image, which is a direction I like.
- **CrossScore** (ECCV 2024) — the paper that introduced cross-referencing as a new category of IQA, alongside full-reference and no-reference. This is the engine inside AVS.
- **TVVE** (2025-26) — teaches a robot to pick task-relevant camera viewpoints, so the target object and the gripper are both visible. It proves that conditioning on the task helps, but it never produces a quality score.
- **RobustVLA** (ICLR 2026) — tests robot policies under 17 kinds of disturbance. Key finding: making a policy robust to *visual* noise does **not** make it robust to anything else.
- **World-in-World** (2025) — judges world models by whether an agent actually succeeds, not by how pretty the predicted video is. Their headline: **good visuals do not guarantee good task performance.** This is strong outside support for everything above.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>সংক্ষিপ্ত সম্পর্কিত কাজ — <strong>MPD</strong> (CVPR 2025): একই দলের আগের ডেটাবেস; ভিন্ন ডাউনস্ট্রিম কাজ একে অপরের সাথে <em>অমিল</em>, তাই একটিমাত্র মডেল যথেষ্ট বিচারক নয়। <strong>MIQD-2.5M ও RA-MIQA</strong> (2025): সম্পূর্ণ ভিন্ন একটি দল ২৫ লক্ষ ছবি ও ৭৫টি মডেল দিয়ে একই সিদ্ধান্তে পৌঁছায়, এবং পুরো ছবির বদলে <strong>প্রতি-অঞ্চল</strong> মান দেয়। <strong>CrossScore</strong> (ECCV 2024): ক্রস-রেফারেন্সিং ধারণার জন্মদাতা — AVS-এর ভেতরের ইঞ্জিন। <strong>TVVE</strong>: কাজ-প্রাসঙ্গিক ভিউ বেছে নিতে শেখায়, কিন্তু কোনো মান-স্কোর দেয় না। <strong>RobustVLA</strong> (ICLR 2026): <em>দৃশ্যগত</em> নয়েজে শক্ত হওয়া মানে অন্য কিছুতে শক্ত হওয়া নয়। <strong>World-in-World</strong> (2025): সুন্দর ভিডিও ভালো কাজের নিশ্চয়তা দেয় না — উপরের সব যুক্তির জোরালো বাইরের সমর্থন।</p>
</div>

---

## Part 3 — What is still missing

Seven gaps. These are the openings.

| | Gap | Why it matters |
|---|---|---|
| **1** | **No metric knows the task.** | The same photo is excellent for "push the board" and useless for "pick up the small red block". Embodied-IQA *collects* 6,150 task sentences, then tests metrics that only look at pixels. The labels exist and nobody uses them. |
| **2** | **The score is one number, not a map.** | You cannot act on "0.43". You can act on "the left part of the view is unusable". |
| **3** | **Only one frame is ever scored.** | Blur and shake happen *over time*, and they are often caused by the robot's own movement. |
| **4** | **Metrics only diagnose, they never act.** | A score that just rejects an image is worth far less than one that says *move this way*. |
| **5** | **No confidence value.** | A robot needs a decision — act, look again, or stop. A bare number with no uncertainty cannot support that. |
| **6** | **The labels reward consistency, not correctness.** | Quality is measured as "did the model say the same thing before and after damage?" A model that is confidently wrong both times gets a perfect score. |
| **7** | **Nobody has measured the noise ceiling.** | This one is important, so it gets its own paragraph. |

**About gap 7.** In Embodied-IQA, the 15 robot models agree with each other at only about **SRCC 0.25**. Human rating panels usually agree at 0.6 or higher. So the "correct answer" is itself very noisy. The paper reports that the best metric reaches 0.775 and calls this insufficient — but if the maximum reachable score is, say, 0.80, then 0.775 is already near-perfect and there is nothing left to win. **Nobody has checked.** Measuring this is cheap, and the answer decides whether the whole field has room to grow.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>সাতটি ফাঁক — এগুলোই সুযোগ: <strong>(১)</strong> কোনো মেট্রিক <em>কাজটা জানে না</em> — একই ছবি এক কাজে চমৎকার, অন্যটিতে অকেজো; Embodied-IQA ৬,১৫০টি কাজ-বাক্য সংগ্রহ করেও কেবল পিক্সেল দেখে এমন মেট্রিক পরীক্ষা করে। <strong>(২)</strong> স্কোর একটিমাত্র সংখ্যা, <em>মানচিত্র</em> নয় — "০.৪৩" দিয়ে কিছু করা যায় না, কিন্তু "বাঁ পাশটা অকেজো" দিয়ে যায়। <strong>(৩)</strong> একবারে কেবল <em>একটি ফ্রেম</em> স্কোর হয় — ব্লার ও কাঁপুনি <em>সময়ের সাথে</em> ঘটে, প্রায়ই রোবটের নিজের নড়াচড়ায়। <strong>(৪)</strong> মেট্রিক কেবল রোগ নির্ণয় করে, <em>কাজ করে না</em>। <strong>(৫)</strong> কোনো <em>কনফিডেন্স</em> মান নেই। <strong>(৬)</strong> লেবেল <em>সঙ্গতিকে</em> পুরস্কৃত করে, <em>সঠিকতাকে</em> নয় — দুইবারই আত্মবিশ্বাসে ভুল মডেলও পুরো স্কোর পায়।</p>
  <p><strong>ফাঁক ৭ প্রসঙ্গে:</strong> ১৫টি রোবট-মডেল নিজেরাই মাত্র <strong>SRCC ০.২৫</strong>-এ একমত (মানুষের প্যানেল সাধারণত ০.৬+), তাই "সঠিক উত্তর"-ই খুব গোলমেলে। সেরা মেট্রিক ০.৭৭৫ পায় — কিন্তু সর্বোচ্চ সম্ভব যদি ০.৮০ হয়, তবে ০.৭৭৫ ইতিমধ্যেই প্রায় নিখুঁত, জেতার আর কিছু বাকি নেই। <strong>কেউ এটি যাচাই করেনি।</strong> মাপাটা সস্তা, আর উত্তরটাই ঠিক করে দেয় পুরো ক্ষেত্রে আদৌ বাড়ার জায়গা আছে কি না।</p>
</div>

---

## Part 4 — The metric I want to build

I am calling it **TAC-Q**, for *Task-Aware Cross-referenced Quality*.

The idea in one sentence: **given the instruction and the current view, produce a map showing where the robot has enough information to act, plus an honest confidence value.**

Four properties, each closing a gap. **No existing metric has more than two of them.**

| Property | Closes gap | Where the idea comes from |
|---|---|---|
| The instruction is fed into the model, so quality depends on the job | 1 | New — but the labels already exist in Embodied-IQA |
| Other viewpoints act as the missing reference — free, since the robot has its own past frames | the no-reference problem | CrossScore and AVS |
| Output is a map, so the worst region tells the robot where to move | 2 and 4 | AVS plus RA-MIQA |
| Trained on the *disagreement* among 15 robot models, not just their average | 5 | New — treat disagreement as information, not noise |

That last one is the part I like most. Everyone so far has averaged the 15 models together and treated their disagreement as annoying noise. But disagreement is exactly the signal you need: when the models disagree strongly about an image, that *is* the uncertainty, and a robot should look again.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>আমি এটিকে বলছি <strong>TAC-Q</strong> (<em>Task-Aware Cross-referenced Quality</em>)। এক বাক্যে: <em>নির্দেশ ও বর্তমান ভিউ দিলে এটি একটি মানচিত্র দেয় — কোথায় রোবটের কাজ করার মতো যথেষ্ট তথ্য আছে — সাথে একটি সৎ কনফিডেন্স মান</em>।</p>
  <p>চারটি বৈশিষ্ট্য, প্রতিটি একটি ফাঁক বন্ধ করে (<strong>কোনো বিদ্যমান মেট্রিকে দুইয়ের বেশি নেই</strong>): <strong>(ক)</strong> নির্দেশ মডেলে দেওয়া হয়, তাই মান কাজের উপর নির্ভর করে [ফাঁক ১]; <strong>(খ)</strong> অন্য ভিউ অনুপস্থিত রেফারেন্সের কাজ করে — রোবটের কাছে বিনামূল্যে [NR সমস্যা]; <strong>(গ)</strong> আউটপুট একটি মানচিত্র, তাই সবচেয়ে খারাপ অঞ্চল রোবটকে বলে কোথায় যেতে হবে [ফাঁক ২ ও ৪]; <strong>(ঘ)</strong> ১৫টি রোবট-মডেলের <em>অমিল</em>-এর উপর প্রশিক্ষিত, গড়ের উপর নয় [ফাঁক ৫]। শেষেরটাই আমার সবচেয়ে প্রিয়: অমিলকে বিরক্তিকর নয়েজ না ভেবে সেটিকেই অনিশ্চয়তার সংকেত ধরা — মডেলরা যখন জোরালোভাবে একমত নয়, রোবটের তখন <em>আবার দেখা</em> উচিত।</p>
</div>

---

## Part 5 — The plan

Two loops. The offline loop builds the metric. The online loop proves it is useful.

```mermaid
flowchart TB
    subgraph OFF["OFFLINE — build the metric"]
        D1["Embodied-IQA<br/>36.9k pairs, 5.53M labels<br/>plus 6,150 task sentences"]
        D2["EPD<br/>12.5k pairs, reward labels"]
        D3["Self-supervised multi-view<br/>from ordinary posed video<br/>free and unlimited"]
        D1 & D2 & D3 --> TR["Train TAC-Q"]
        TR --> M["TAC-Q model"]
    end

    subgraph ON["ONLINE — close the loop"]
        OBS["Current view"] --> M2["TAC-Q"]
        TASK["Instruction"] --> M2
        MEM["Past views<br/>free cross-reference"] --> M2
        M2 --> MAP["Quality map + confidence"]
        MAP --> GATE{"Good enough?"}
        GATE -->|yes| ACT["Robot acts"]
        GATE -->|no| MOVE["Look again:<br/>move to the worst region"]
        MOVE --> OBS
        ACT --> OUT["Task result"]
        OUT -.->|logged| MEM
    end

    M -.deployed as.-> M2
```

### The stages

**Stage 0 — Check the ceiling first.** *(about 4 weeks)*
Before building anything, measure how much room there actually is. Split the 15 robot models into two halves, check how well one half predicts the other, and use that to estimate the highest score any metric could reach. If the answer is that current metrics are already near the limit, I save myself a year. This is cheap, needs no training, and is worth writing up on its own.

**Stage 1 — Gather the data.** *(about 6 weeks)*
Embodied-IQA and EPD are released. The third source is the interesting one: following the AVS recipe, I can generate unlimited training pairs from ordinary videos with known camera positions, with no labelling and no robot lab. That is what makes this affordable.

**Stage 2 — Build the model.** *(about 10 weeks)*
A light image backbone, a cross-attention layer that compares the current view against past views, the instruction fed in as text, and two outputs: a quality map and a confidence value. One important choice — train it to get the *ranking* right rather than the exact number, because with labels this noisy, exact values are meaningless but order is not.

**Stage 3 — Test it properly.** *(about 6 weeks)*
Compare against the existing metrics, but add three tests nobody currently runs: results reported as a *percentage of the ceiling* from Stage 0; results broken down *by task difficulty*; and results on *robot models never seen during training*.

**Stage 4 — Close the loop.** *(about 10 weeks)*
This is what makes it more than another metric paper. Three versions, from safest to most ambitious: let the robot look again when confidence is low; use the quality map to choose the next viewpoint; and finally use quality as a training reward so the robot learns to position itself well. The last one connects directly to my "moving to see better" idea.

**Stage 5 — Real robot.** *(about 8 weeks)*
A UR5 arm, which is what both main papers used, so the numbers are directly comparable. Kept small on purpose — a few hundred trials for checking, never for bulk training.

*(Timings assume one person with GPU access, and the stages overlap.)*

### What comes out of it

| | Paper | The claim |
|---|---|---|
| **P0** | The ceiling study | The field is comparing against very noisy answers without knowing it |
| **P1** | TAC-Q | The first quality metric that knows the task, produces a map, and reports confidence |
| **P2** | Closing the loop | A quality metric that measurably raises task success, not just correlation |

The order matters. P0 is cheap and buys credibility. P1 gives P2 its instrument.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>দুটি লুপ — <em>অফলাইন</em> লুপ মেট্রিকটি বানায়, <em>অনলাইন</em> লুপ প্রমাণ করে এটি কাজে লাগে। <strong>ধাপসমূহ:</strong> <strong>ধাপ ০ (≈৪ সপ্তাহ)</strong> — আগে <em>সিলিং</em> মাপো: ১৫টি মডেলকে দুই ভাগে ভাগ করে দেখো এক ভাগ অন্যটিকে কতটা অনুমান করে, তাতেই সর্বোচ্চ সম্ভব স্কোর আঁচ করা যায়; কাছাকাছি হলে এক বছর বাঁচে। <strong>ধাপ ১ (≈৬ সপ্তাহ)</strong> — ডেটা জোগাড়; AVS-রেসিপি মেনে সাধারণ ভিডিও থেকে অসীম প্রশিক্ষণ-জোড়া (লেবেল ও ল্যাব ছাড়াই)। <strong>ধাপ ২ (≈১০ সপ্তাহ)</strong> — হালকা ব্যাকবোন + ক্রস-অ্যাটেনশন + টেক্সট-নির্দেশ, দুই আউটপুট (মানচিত্র ও কনফিডেন্স); সঠিক সংখ্যা নয়, <em>ক্রম</em> ঠিক করতে প্রশিক্ষণ (কারণ লেবেল গোলমেলে)।</p>
  <p><strong>ধাপ ৩ (≈৬ সপ্তাহ)</strong> — সিলিং-এর <em>শতাংশ</em> হিসেবে ফল, <em>কাজের কাঠিন্য</em> অনুযায়ী ভাগ করে, এবং <em>অদেখা রোবট-মডেলে</em> পরীক্ষা। <strong>ধাপ ৪ (≈১০ সপ্তাহ)</strong> — লুপ বন্ধ করা: কনফিডেন্স কম হলে আবার দেখা → মানচিত্র দিয়ে পরবর্তী ভিউ বাছা → মানকে রিওয়ার্ড বানিয়ে রোবটকে ভালো অবস্থানে শেখানো। <strong>ধাপ ৫ (≈৮ সপ্তাহ)</strong> — বাস্তব UR5 বাহুতে অল্প পরীক্ষা। <strong>ফলাফল:</strong> P0 (সিলিং স্টাডি), P1 (TAC-Q), P2 (লুপ বন্ধ) — P0 সস্তা ও বিশ্বাসযোগ্যতা দেয়, আর P1 P2-কে তার যন্ত্রটি দেয়।</p>
</div>

---

## Why this is the right moment

- **Scores are low everywhere.** The best results are 0.775 and 0.576. There is room.
- **There is a venue waiting.** The Machine-oriented IQA (MoIQA) Challenge at ACM Multimedia 2026 has exactly two tracks: match VLM behaviour in simulation, and match VLA behaviour in the real world. It comes with data and an evaluation protocol I do not have to defend.
- **Two independent groups agree.** Different labs, different data, same conclusion. The premise is not one lab's opinion.
- **Speed is not the blocker.** AVS already runs inside a control loop.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>এখনই কেন সঠিক সময়: <strong>স্কোর সর্বত্র কম</strong> (সেরা ০.৭৭৫ ও ০.৫৭৬ — বাড়ার জায়গা আছে); <strong>একটি ভেন্যু প্রস্তুত</strong> — ACM Multimedia 2026-এর MoIQA চ্যালেঞ্জে ঠিক দুটি ট্র্যাক (সিমুলেশনে VLM আচরণ ও বাস্তবে VLA আচরণ মেলানো), ডেটা ও মূল্যায়ন-প্রোটোকলসহ; <strong>দুটি স্বাধীন দল একমত</strong> (ভিন্ন ল্যাব, ভিন্ন ডেটা, একই সিদ্ধান্ত); <strong>গতি বাধা নয়</strong> — AVS ইতিমধ্যেই কন্ট্রোল-লুপের ভেতরে চলে।</p>
</div>

## The first two weeks

1. Download the Embodied-IQA release and see what is actually public.
2. Reproduce one published number, to confirm the setup works.
3. Compute the agreement between the robot models — **the single most informative experiment available right now.**
4. Read the CrossScore paper properly. It is the most reusable piece of the whole plan.
5. Check the MoIQA challenge deadlines.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>প্রথম দুই সপ্তাহ: <strong>(১)</strong> Embodied-IQA রিলিজ নামিয়ে দেখা আসলে কী কী পাবলিক; <strong>(২)</strong> একটি প্রকাশিত সংখ্যা পুনরুৎপাদন করে সেটআপ ঠিক আছে কি না নিশ্চিত করা; <strong>(৩)</strong> রোবট-মডেলগুলোর মধ্যে <em>মতৈক্য</em> হিসাব করা — <strong>এই মুহূর্তের সবচেয়ে তথ্যবহুল পরীক্ষা</strong>; <strong>(৪)</strong> CrossScore পেপারটি ভালো করে পড়া — পুরো পরিকল্পনার সবচেয়ে পুনর্ব্যবহারযোগ্য অংশ; <strong>(৫)</strong> MoIQA চ্যালেঞ্জের ডেডলাইন দেখা।</p>
</div>

---

## Closing thought

The most useful sentence I read across all of these papers was not about a network or a dataset. It was the observation, repeated in three separate places, that **a picture looking good and a picture being useful are different things.**

We have spent decades getting very good at the first one. The second one is nearly untouched. And for a robot, only the second one matters.

If you are working on something nearby, I would genuinely like to hear about it.

<div class="bn-block">
  <span class="bn-label">🇧🇩 বাংলা</span>
  <p>এই সব পেপার জুড়ে পড়া সবচেয়ে কাজের বাক্যটি কোনো নেটওয়ার্ক বা ডেটাসেট নিয়ে ছিল না। তিনটি আলাদা জায়গায় বারবার আসা পর্যবেক্ষণটি হলো: <strong>ছবি সুন্দর দেখানো আর ছবি কাজে লাগা — এক জিনিস নয়।</strong> প্রথমটিতে আমরা দশকের পর দশক দক্ষ হয়েছি; দ্বিতীয়টি প্রায় অস্পৃশ্য — আর রোবটের কাছে কেবল দ্বিতীয়টিই গুরুত্বপূর্ণ। কাছাকাছি কিছু নিয়ে কাজ করলে, আপনার কথা শুনতে আমার সত্যিই ভালো লাগবে।</p>
</div>

{% endraw %}

<div class="wm-backlink wm-backlink-bottom">
  <a href="{{ '/blog/world-models/' | relative_url }}">&larr; Back to the <strong>World Models</strong> series</a>
</div>

<style>
.wm-backlink { margin: 0 0 1.2rem; font-size: 0.92rem; }
.wm-backlink-bottom { margin: 2rem 0 0; }
.wm-backlink a { color: var(--global-theme-color); text-decoration: none; }
.wm-backlink a:hover { text-decoration: underline; }

/* Bilingual Bangla blocks — one after each section */
.bn-block {
  border-left: 4px solid var(--global-theme-color);
  background: color-mix(in srgb, var(--global-theme-color) 6%, transparent);
  border-radius: 0 10px 10px 0;
  padding: 13px 16px 4px;
  margin: 16px 0 22px;
}
.bn-block p {
  margin: 0 0 10px;
  line-height: 1.95;
  font-size: 1.02rem;
}
.bn-label {
  display: inline-block;
  margin-bottom: 9px;
  padding: 2px 11px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: #fff;
  background: var(--global-theme-color);
}
</style>
