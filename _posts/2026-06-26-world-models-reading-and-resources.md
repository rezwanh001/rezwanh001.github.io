---
layout: post
title: "World Models — Reading & Resources: Deep Dives + Annotated Idea Map"
description: "One place for the World Models literature: in-depth read-throughs of the key papers (gist, pipeline, results, stated future work, and idea openings) followed by a broad, thematically organized index. 🎯 marks the work closest to my active-perception research direction."
date: 2026-06-26 12:00:00
tags: [world-models, resources, reading-list, deep-dives, embodied-ai]
categories: world-models
wm_resource: true
giscus_comments: true
related_posts: false
---

<div class="wm-backlink">
  <a href="{{ '/blog/#world-models' | relative_url }}">&larr; Blogs · <strong>World Models</strong> series</a>
</div>

This is the single **reading-and-resources hub** for the World Models series. It has two halves: **Part I — Deep Dives** reads each key paper along the same axes (*gist · pipeline · benchmark &amp; dataset · results · stated future work · scope &amp; unique ideas*) so the page doubles as an idea-generation worksheet; **Part II — Thematic Index** is the broader, faster annotated map across the active-perception, world-model, and embodied-agent literature. The concepts behind all of this are introduced in **[Part 0: From Language Models to World Models]({{ '/blog/2026/world-models-introduction/' | relative_url }})**.

Throughout, a 🎯 marks the papers closest to my current research direction — **active, task-aligned perception for embodied agents ("moving to see better")**. Annotations are paraphrased in my own words; several entries are fast-moving preprints, so **open each link and confirm title/authors/venue before citing in a formal document**. Full plain-text citations are in the [References](#references).

<div class="rm-callout">
  <strong>⭐ Start here (four high-leverage reads):</strong>
  <ol>
    <li><a href="https://arxiv.org/abs/2506.22355" target="_blank" rel="noopener">Embodied AI Agents: Modeling the World</a> — the position paper that makes the world model the <em>core</em> of embodied agents.</li>
    <li><a href="https://arxiv.org/abs/2510.18135" target="_blank" rel="noopener">World-in-World</a> — closed-loop evidence that visual realism ≠ task success.</li>
    <li><a href="https://arxiv.org/abs/2506.04363" target="_blank" rel="noopener">WorldPrediction</a> — a benchmark showing high-level procedural planning is largely unsolved.</li>
    <li><a href="https://arxiv.org/abs/2312.14135" target="_blank" rel="noopener">V*</a> — "where to look" as a learnable skill inside a multimodal model.</li>
  </ol>
  <span class="rm-callout-note">If active perception is your angle, jump to <a href="#group-d">Group D — Quality + active perception for embodied AI</a>: three 2024–2026 papers that sit directly on the idea.</span>
</div>

<nav class="dd-nav" aria-label="On this page">
  <a href="#deep-dives">Part I · Deep Dives</a>
  <a href="#group-d">🎯 Group D (project-aligned)</a>
  <a href="#idea-seed">Idea seed</a>
  <a href="#thematic-index">Part II · Thematic Index</a>
  <a href="#how-to-use">How to use this</a>
  <a href="#references">References</a>
</nav>

---

# Part I · Deep Dives {#deep-dives}

A reading list tells you *what* exists; this part tells you *why each paper matters*. Papers are grouped; reference numbers in the [References](#references) follow this order.

## Group A — World models &amp; the data/agenda layer {#group-a}

### 1 · WorldPrediction
<span class="dd-meta">Chen, Chung, Bang, Ji &amp; Fung · Meta FAIR · 2025 · <a href="https://arxiv.org/abs/2506.04363" target="_blank" rel="noopener">arXiv:2506.04363</a></span>

**Gist.** Visual realism ≠ planning ability — high-level, abstract-action planning is largely unsolved, and the authors suspect *perception* is the bottleneck.

- **Problem &amp; pipeline.** Do models have a world model good enough for *high-level, long-horizon* procedural planning (not just low-level motion)? Formalized as a partially observable semi-MDP. Given initial and final visual states, the model must pick the correct action (WM track) or the correctly ordered action sequence (PP track) from counterfactual distractors. The clever trick: "action equivalents" (the same action in a different context) as distractors, so models can't cheat using low-level background continuity; heavy human filtering.
- **Benchmark / dataset / metrics.** Two tracks (WM, PP) scored by discriminative accuracy; data drawn from procedural-video sources (COIN, CrossTask, EgoExo4D, IKEA-ASM).
- **Results.** Best models ≈ **57%** (world modeling) and **38%** (procedural planning) versus humans near-perfect; bigger models barely help planning.
- **Scope &amp; unique ideas.** A ready-made target to test whether *better perception lifts planning*. The "action-equivalents" construction is a clean, reusable way to force semantic over pixel reasoning — worth copying for any new benchmark.

### 2 · Action100M
<span class="dd-meta">Meta FAIR · 2026 · <a href="https://arxiv.org/abs/2601.10592" target="_blank" rel="noopener">arXiv:2601.10592</a></span>

**Gist.** Automated, hierarchical annotation can replace manual labeling at scale, and predictive (JEPA) representations keep improving with more data.

- **Problem &amp; pipeline.** Action understanding needs huge, open-vocabulary, hierarchically labeled video, but manual labeling doesn't scale. They build ~100M labeled segments from 1.2M instructional videos with a fully automated pipeline: (i) hierarchical temporal segmentation using **V-JEPA 2** embeddings; (ii) multi-level captions arranged as a *Tree-of-Captions*; (iii) aggregation by a reasoning model (GPT-OSS-120B) under multi-round **Self-Refine** to reduce hallucinations and emit structured fields (action, actor, captions).
- **Benchmark / dataset / metrics.** The dataset itself (~100M segments / 1.2M videos); evaluated by zero-shot action-recognition transfer and data-scaling curves. Descends from HowTo100M and the JEPA representation line.
- **Results.** A trained VL-JEPA model shows consistent data-scaling gains and strong zero-shot action recognition.
- **Scope &amp; unique ideas.** A data substrate for perception / world-model work; the motion→task hierarchy suits multi-level reasoning. Practical caveat: only a 10% preview is public; the full set is gated.

### 3 · Embodied AI Agents: Modeling the World
<span class="dd-meta">Fung et al. · Meta · 2025 · <a href="https://arxiv.org/abs/2506.22355" target="_blank" rel="noopener">arXiv:2506.22355</a></span>

**Gist.** Perception, planning, and memory should be unified *inside a world model*; embodiment plus social/mental modeling is the agenda.

- **Problem &amp; pipeline.** How should embodied agents (avatars, wearables, robots) be built to learn and act like humans? A research-vision paper, not an experiment. Proposes unifying multimodal perception + reasoning-for-action + memory inside a world model, and adds *mental world models* that infer user intentions and social context (a Theory-of-Mind layer).
- **Benchmark / dataset / metrics.** None of its own; it organizes the field and references existing benchmarks, contributing a virtual/wearable/robotic agent taxonomy.
- **Results.** No single model, no accuracy number — its value is the framing.
- **Scope &amp; unique ideas.** The umbrella that legitimizes a perception-quality-inside-world-models direction. Its Theory-of-Mind thread is itself a possible project (user-intention modeling).

## Group B — "Moving to see better" (active perception) {#group-b}

### 4 · World-in-World <span class="dd-flag">🎯 Core to the project</span>
<span class="dd-meta">Zhang et al. · ICLR 2026 (Oral) · <a href="https://arxiv.org/abs/2510.18135" target="_blank" rel="noopener">arXiv:2510.18135</a></span>

**Gist.** Judge world models by closed-loop *task success*, not pixels — the most direct evidence for a task-coupled metric.

- **Problem &amp; pipeline.** Do generative world models actually help agents *succeed*, or do we only measure visual quality? They build the first closed-loop platform with a unified online planner and a standardized action API, across four environments (perception, navigation, manipulation) where task success is the primary metric.
- **Benchmark / dataset / metrics.** Task success rate (primary) plotted against visual-quality scores (FID/FVD-style), revealing weak correlation.
- **Results.** High visual quality does **not** translate into task success; scaling post-training on action-observation data beats upgrading the generator; more inference-time planning compute helps.
- **Scope &amp; unique ideas.** Cite as the empirical backbone of a perception-aligned, task-coupled reward; reuse its closed-loop, task-success evaluation philosophy to show a quality reward improves outcomes.

### 5 · MANIQA <span class="dd-flag">🎯 Core to the project</span>
<span class="dd-meta">Yang et al. · CVPRW 2022 · <a href="https://arxiv.org/abs/2204.08958" target="_blank" rel="noopener">arXiv:2204.08958</a></span>

**Gist.** A single image can be scored for human-perceived quality with *no reference*, and attention across both channel and space matters.

- **Problem &amp; pipeline.** No-reference image quality assessment (score perceptual quality from the image alone) was weak on GAN-type distortions. Extract features with a ViT, then a **Transposed Attention Block** (channel dimension) and a **Scale Swin Transformer Block** (spatial dimension), with a dual-branch patch-weighted score head.
- **Benchmark / dataset / metrics.** LIVE, TID2013, CSIQ, KADID-10K; correlation with human MOS via **SRCC/PLCC**.
- **Results.** State-of-the-art on those datasets and first place in the NTIRE 2022 no-reference challenge.
- **Scope &amp; unique ideas.** A concrete starting architecture for a "view-quality" metric *Q*; learn its MOS-regression recipe and adapt it from "image quality" to "view usefulness for a task." (Note: Group D shows human-MOS quality transfers *poorly* to robots — so adapt the architecture, not the labels.)

### 6 · Rein-EAD (Reinforced Embodied Active Defense) <span class="dd-flag">🎯 Core to the project</span>
<span class="dd-meta">TPAMI 2025 · <a href="https://arxiv.org/abs/2507.18484" target="_blank" rel="noopener">arXiv:2507.18484</a></span>

**Gist.** Moving to re-observe, driven by a dense uncertainty reward, beats single-shot perception — the closest existing mechanism to "move to see better."

- **Problem &amp; pipeline.** Passive perception is fragile to adversarial and 3D attacks. A recurrent feedback loop takes multiple looks; an **uncertainty-aware guided dense reward** shapes where to move and observe; scene understanding is rebuilt over steps rather than judged from one frame.
- **Benchmark / dataset / metrics.** Adversarial robustness / defense metrics under patch and 3D attacks (not perceptual-quality indices).
- **Results.** Improves robustness while staying computationally efficient.
- **Scope &amp; unique ideas.** Its RL loop and dense-reward design are directly reusable — swap the uncertainty/defense reward for a human-aligned quality reward.

### 7 · RL4VLM <span class="dd-flag">🎯 Core to the project</span>
<span class="dd-meta">Zhai et al. (incl. Xie) · NeurIPS 2024 · <a href="https://arxiv.org/abs/2405.10292" target="_blank" rel="noopener">arXiv:2405.10292</a></span>

**Gist.** Attach an RL reward to a perception-capable model and you get an agent — the recipe for turning *any* reward into behavior.

- **Problem &amp; pipeline.** VLMs perceive well but decide poorly. Treat the VLM as a policy that reasons step-by-step (chain-of-thought) and then emits actions, trained end-to-end with task reward in gym-like multimodal environments.
- **Benchmark / dataset / metrics.** Interactive decision tasks (card games, embodied / ALFWorld-style), scored by success/reward.
- **Results.** Improves decision-making over prompting and supervised baselines.
- **Scope &amp; unique ideas.** The practical template for wiring a custom (e.g. perceptual-quality) reward into a perception-capable agent; study how they balance reasoning and action.

### 8 · V\* <span class="dd-flag">🎯 Core to the project</span>
<span class="dd-meta">Wu &amp; Xie · CVPR 2024 · <a href="https://arxiv.org/abs/2312.14135" target="_blank" rel="noopener">arXiv:2312.14135</a></span>

**Gist.** Deciding *where to attend*, rather than consuming everything at once, is itself a learnable, performance-critical skill — the model-side analog of active perception.

- **Problem &amp; pipeline.** Multimodal LLMs miss small details in high-resolution images because they look once, globally. The **SEAL** framework uses context to guide an iterative search that zooms to the relevant region before answering.
- **Benchmark / dataset / metrics.** Introduces **V\*Bench** for fine-detail visual-QA accuracy.
- **Results.** Accurate on fine-detail visual questions where standard MLLMs fail.
- **Scope &amp; unique ideas.** Conceptual grounding for "where to look"; even with a moving robot, the search-then-decide structure transfers.

## Group C — Multi-agent &amp; state tracking {#group-c}

### 9 · Solaris
<span class="dd-meta">Savva, Michel, …, Xie · NYU · 2026 · <a href="https://arxiv.org/abs/2602.22208" target="_blank" rel="noopener">arXiv:2602.22208</a></span>

**Gist.** World models can be multi-agent and *must* keep shared views consistent — directly relevant to shared visual understanding.

- **Problem &amp; pipeline.** Can a video world model serve *multiple* agents with consistent shared views (a "multiplayer" world model)? Built in Minecraft, predicting consistent first-person views for two players via a staged single→multiplayer pipeline (bidirectional, causal, and Self-Forcing training), backed by a multiplayer data system (~12.6M multiplayer frames).
- **Benchmark / dataset / metrics.** Co-observation consistency, grounding, memory, movement, and building metrics.
- **Results.** A technical report — treat the numbers as preliminary.
- **Scope &amp; unique ideas.** If you keep a multi-agent strand, this is *the* reference for cross-agent visual consistency, and its consistency metric is reusable.

### 10 · VSTAT
<span class="dd-meta">NYU (incl. Xie) · 2026 · <a href="https://arxiv.org/abs/2606.03920" target="_blank" rel="noopener">arXiv:2606.03920</a></span>

**Gist.** Models can describe a frame but cannot *track state over time* — a concrete, quantified gap that motivates world-model and memory work.

- **Problem &amp; pipeline.** Can video MLLMs track fine-grained visual state over time (counts, attributes, order)? A benchmark of procedural videos with state-tracking questions: 834 clips and ~1,500 questions across synthetic, self-recorded, and real videos, forcing a running mental model of object states.
- **Benchmark / dataset / metrics.** VSTAT accuracy, with the large human–model gap as the headline index.
- **Results.** Best model (~Gemini-3.1 Pro) ≈ **44.4** versus humans ≈ **90.5**.
- **Scope &amp; unique ideas.** Motivation and a possible evaluation axis for world-model / memory work; its human-vs-model gap framing mirrors the broader "metrics don't equal usefulness" argument.

## Group D — Quality + active perception for embodied AI {#group-d}

> The trio most directly on the "moving to see better" idea: each uses **image quality** to guide or judge embodied perception. Two of them carry a finding that reshapes the framing — read the [idea seed](#idea-seed) after this group.

### 11 · Active View Selector (AVS) <span class="dd-flag">🎯 Core to the project</span>
<span class="dd-meta">Wang, Bhalgat, Li &amp; Prisacariu · University of Oxford · 2025 · <a href="https://arxiv.org/abs/2506.19844" target="_blank" rel="noopener">arXiv:2506.19844</a></span>

**Gist.** Reframes *where to capture next* for 3D reconstruction / novel-view synthesis as **2D image-quality assessment** — go where the current rendering looks worst ("boost where it struggles") — making active view selection fast and representation-agnostic.

- **Problem &amp; pipeline.** Given a partial reconstruction, where should the camera go next? Prior methods (ActiveNeRF, FisherRF) compute 3D uncertainty / information gain — slow (FisherRF builds a Hessian over 200M+ parameters, ~5–8 s per view) and tied to a specific 3D representation. AVS instead scores each candidate viewpoint by the *predicted quality* of its rendering. Since there is no ground-truth image for a candidate view, they train a **cross-reference IQA network** (inspired by CrossScore) that predicts the SSIM map of a rendering from the rendering plus several real reference views. A lightweight RepViT-backbone variant runs in ~0.5 s.
- **Benchmark / dataset / metrics.** Reconstruction / NVS quality versus selection cost; zero-shot generalization to egocentric ARIA smart-glasses data it was never trained on; compared against FisherRF and no-reference IQA baselines (MANIQA, MUSIQ).
- **Results.** Beats FisherRF on reconstruction quality while running **14–33× faster** with less than half the GPU memory; notably, plain no-reference metrics (MANIQA, MUSIQ) are already *strong* baselines for view selection.
- **Stated future work.** Integrate the low-latency selector into real-time SLAM and AR/VR; use it to guide a user or robot to capture images that achieve an objective (better synthesis or coverage); fine-tune on egocentric data.
- **Scope &amp; unique ideas.** The closest published thing to "moving to see better," but the quality it optimizes is *reconstruction fidelity (SSIM)*, not *task usefulness* — swapping that objective for a task-aligned reward is open space. Selection here is greedy and passive (score all candidates, pick the worst); there is **no learned movement policy** — an RL agent that learns *where to go* is unclaimed. The cross-reference trick ("is this view good given the views I already have") maps neatly onto an agent with **memory**.

### 12 · Image Quality Assessment for Embodied AI (Embodied-IQA) <span class="dd-flag">🎯 Core to the project</span>
<span class="dd-meta">Chunyi Li et al. · SJTU / Shanghai AI Lab / NTU · 2025 · <a href="https://arxiv.org/abs/2505.16815" target="_blank" rel="noopener">arXiv:2505.16815</a></span>

**Gist.** Proposes the topic *IQA for Embodied AI*: predict how **usable** an image is for a robot's task rather than how pretty it looks to a human — and shows a large human–robot vision gap.

- **Problem &amp; pipeline.** Builds a **Perception–Cognition–Decision–Execution** pipeline (framed via the Mertonian system) and a large database: 1,230 reference images, 30 distortion types at 5 levels (~36,900 distorted images), with 5M+ annotations. Cognition is scored by 15 VLMs, Decision by 15 VLAs (on 7-DoF pose), and Execution by 1,500 real-world robot-arm runs (success = 100; failure deducts centimeters of error; collision = 0).
- **Benchmark / dataset / metrics.** Correlation of IQA metrics with embodied scores via **SRCC/PLCC**; Decision-versus-Execution correlation.
- **Results.** Standard IQA metrics that correlate ~0.9 with human opinion drop to ~**0.75** at best (TOPIQ) on embodied data, and no-reference methods fall below **0.6**. Distortion sensitivity differs from humans (a denoise can hurt a robot badly, while strong block-interpolation barely matters if it misses the target object). Decision correlates with real Execution above 0.6, but Cognition alone correlates below 0.5 — a VLM's judgment is not enough.
- **Stated future work.** Develop more accurate quality indicators for embodied AI; integrate the human, VLM, and VLA paradigms and pick the right one per use case; extend Perception to vision–tactile fusion and Execution to legged / quadruped robots; build an automated real-world pipeline to scale execution labels.
- **Scope &amp; unique ideas.** Direct evidence that *human-aligned quality is the wrong target for a robot*. Everything here is **static scoring of given images** — there is no agent that *moves* to raise the score; the active-perception loop is missing entirely. They also show no single VLM or VLA is a reliable judge (subject correlations of ~0.25–0.3), an argument for a *learned, aggregated* quality / reward model.

### 13 · Embodied IQA for Robotic Intelligence (EPD / MA-EIQA) <span class="dd-flag">🎯 Core to the project</span>
<span class="dd-meta">Jianbo Zhang et al. · SJTU · 2025 · <a href="https://arxiv.org/abs/2412.18774" target="_blank" rel="noopener">arXiv:2412.18774</a></span>

**Gist.** Builds robot-quality labels **purely from task performance** (no human in the loop) and ships the first no-reference IQA model designed for robots.

- **Problem &amp; pipeline.** Same core thesis as Embodied-IQA (robot quality ≠ human quality, invoking the Moravec paradox), but the labels come from RL reward, not opinion. The **EPD** database has 12,500 reference/distorted pairs from 100 episodes across two tasks (push, pick) in the SAPIEN/ManiSkill simulator, with 25 distortions at 5 levels. The label for each image is the **RL episode reward** (from PPO, SAC, and TDMPC2 agents) normalized to a 0–5 score. They also propose **MA-EIQA**: a ResNet-50 backbone, a multi-scale (PANet-style) encoder that fuses semantic and texture detail, and a CBAM-style embodied-attention module — kept lightweight (48.83M parameters, far smaller than MANIQA).
- **Benchmark / dataset / metrics.** Human-MOS versus embodied-MOS correlation; SRCC/PLCC across 16 IQA methods.
- **Results.** Human and embodied MOS barely correlate (PLCC ~**0.13–0.21**); across 16 IQA methods none exceeds ~0.6 SRCC; MA-EIQA reaches SOTA among no-reference models and beats the full-reference ones. Color distortion hurts tasks most; motion blur and noise least — the opposite of human sensitivity.
- **Stated future work.** Expand the embodied-preference database; add vision–tactile sensing; cover more robot body types.
- **Scope &amp; unique ideas.** They already use RL reward as the quality label, but only *offline*, to build a static dataset. Using a learned quality model as a **live dense reward that drives an agent's movement** is the step they do not take. The label is task-specific (push, pick); a quality signal that *generalizes across tasks* — or that an agent can use before it knows the exact task — is open. They vary *distortion* on fixed viewpoints; you care about *viewpoint* — nobody has unified distortion-robustness and viewpoint-usefulness under one task-aligned signal.

## A cross-cutting idea seed {#idea-seed}

Read together, these papers point one direction.

**Five of them report the same thing from different angles.** WorldPrediction, World-in-World, and VSTAT show that today's models *look* good but **act, plan, and remember poorly, and pixel-level metrics fail to predict task usefulness**. Embodied-IQA and EPD sharpen this with hard numbers: **human perceptual quality correlates poorly with embodied task success** (PLCC as low as 0.13–0.21; human-trained metrics that hit ~0.9 on people fall to ~0.5–0.75 on robots). So a *human-aligned* view-quality reward — an intuitive first pitch — is probably the wrong target for a robot doing a task.

**Three honest ways to respond** (picking one sharpens the contribution):
1. **Pivot the reward** from human-aligned to *task-aligned* view usefulness (what Embodied-IQA and EPD argue for), and make the novelty the *active movement* none of them do.
2. **Keep human alignment but scope it** to *human-facing* agents (wearables, assistive glasses), where AVS-style capture guidance and human preference genuinely matter.
3. **Make the human-versus-task quality gap itself the research question**: when do they agree, when do they diverge, can one model serve both.

**The unclaimed center.** AVS *moves the camera* but optimizes reconstruction quality with no learned policy; Embodied-IQA and EPD *define task-aligned quality* but only score static images — nothing moves. Stated precisely, the open problem is: *an agent that learns a **movement policy** whose reward is a learned, **task-aligned** (not pretty) **view-quality** signal, evaluated in **closed loop** by task success.* Each half exists in the literature; the combination does not. Concrete openings: a task-aligned view-usefulness model used as a **dense intrinsic reward** for an active-perception RL policy (EPD's reward-as-label × AVS's move-to-improve); a **cross-reference usefulness** signal for an agent with memory ("is this new viewpoint more useful than the ones I already hold"); a new **active-perception benchmark** where an agent moves and each viewpoint is labeled by downstream task success (filling the static-only gap in Embodied-IQA / EPD); and a **lightweight-by-design** reward model (both AVS's RepViT and MA-EIQA's 48M-parameter CNN exist because the loop must run in real time).

---

# Part II · Thematic Index {#thematic-index}

The broader, faster map — organized by theme, meant as raw material for *idea generation*: read across a cluster, find the gap, build there. Entries already covered above link back to their deep dive.

## 1 · Foundations &amp; framing

The classics that define the vocabulary, plus the position papers that set today's agenda.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/1803.10122" target="_blank" rel="noopener">World Models</a><span class="paper-meta">Ha &amp; Schmidhuber · NeurIPS 2018</span>The canonical V–M–C blueprint: compress observations, learn latent dynamics, train a tiny controller — and learn inside the model's "dream".</div>
  <div class="paper"><a href="https://openreview.net/forum?id=BZ5a1r-kVsf" target="_blank" rel="noopener">A Path Towards Autonomous Machine Intelligence</a><span class="paper-meta">LeCun · 2022</span>The JEPA manifesto: a modular, predictive, world-model-centric architecture as a route past pure text prediction.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2506.22355" target="_blank" rel="noopener">Embodied AI Agents: Modeling the World</a><span class="paper-meta">Fung et al. · Meta · 2025 · <a href="#group-a">deep dive ↑</a></span>Argues perception + reasoning-for-action + memory should be unified inside a world model, and adds a "mental world model" (Theory-of-Mind) layer.</div>
</div>

## 2 · World models for embodied agents

Surveys that organize the field, and the two method families that dominate: video-generation vs. latent-prediction world models.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/2605.00080" target="_blank" rel="noopener">World Model for Robot Learning: A Comprehensive Survey</a><span class="paper-meta">Survey · 2026</span>Stresses <em>action-conditioned</em> world models — visually plausible but action-inconsistent futures are of limited value for control.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2510.16732" target="_blank" rel="noopener">A Comprehensive Survey on World Models for Embodied AI</a><span class="paper-meta">Survey · 2025</span>A taxonomy across functionality, temporal modeling, and spatial representation.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2602.22208" target="_blank" rel="noopener">Solaris: Building a Multiplayer Video World Model in Minecraft</a><span class="paper-meta">Savva, …, Xie · NYU · 2026 · <a href="#group-c">deep dive ↑</a></span>A multiplayer video world model predicting consistent shared views — directly relevant to multi-agent / shared visual understanding.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2506.01182" target="_blank" rel="noopener">Humanoid World Models</a><span class="paper-meta">2025</span>Open foundation world models for humanoid robotics.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2509.21790" target="_blank" rel="noopener">LongScape: Long-Horizon Embodied World Models with Context-Aware MoE</a><span class="paper-meta">2025</span>Tackles long-horizon generation with a context-aware mixture of experts.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2601.15282" target="_blank" rel="noopener">Rethinking Video Generation Model for the Embodied World</a><span class="paper-meta">2026</span>Reconsiders what video generators need in order to be useful as world models for embodiment.</div>
</div>

## 3 · Active perception — "moving to see better"

Agents that choose where to look or move in order to perceive better — increasingly trained with RL rather than hand-designed next-best-view rules.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/2506.19844" target="_blank" rel="noopener">Active View Selector (AVS)</a><span class="paper-meta">🎯 Oxford · 2025 · <a href="#group-d">deep dive ↑</a></span>Reframes next-best-view as 2D image-quality assessment ("boost where it struggles") — fast, representation-agnostic, 14–33× faster than FisherRF.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2507.18484" target="_blank" rel="noopener">Reinforced Embodied Active Defense (Rein-EAD)</a><span class="paper-meta">🎯 TPAMI 2025 · Tsinghua · <a href="#group-b">deep dive ↑</a></span>An RL "take a second look" policy with uncertainty-aware dense rewards — the closest existing mechanism to "move to see better".</div>
  <div class="paper"><a href="https://arxiv.org/abs/2312.14135" target="_blank" rel="noopener">V*: Guided Visual Search in Multimodal LLMs</a><span class="paper-meta">🎯 Wu &amp; Xie · CVPR 2024 · <a href="#group-b">deep dive ↑</a></span>The SEAL framework decides <em>where to look</em> in an image before answering — the model-side analog of active perception.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2506.15666" target="_blank" rel="noopener">Vision in Action: Learning Active Perception from Human Demonstrations</a><span class="paper-meta">2025</span>Learns active viewpoint behaviors from human demos.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2512.01188" target="_blank" rel="noopener">Real-World Reinforcement Learning of Active Perception Behaviors</a><span class="paper-meta">2025</span>Trains active-sensing behaviors directly in the real world.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2602.04600" target="_blank" rel="noopener">Act, Sense, Act: Non-Markovian Active Perception from Egocentric Human Data</a><span class="paper-meta">2026</span>Learns non-Markovian active-perception strategies at scale from egocentric video.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2603.12193" target="_blank" rel="noopener">SaPaVe: Active Perception and Manipulation in VLA Models</a><span class="paper-meta">2026</span>Adds active perception + manipulation into vision-language-action models.</div>
</div>

## 4 · Agentic &amp; multi-agent embodied AI

Agents that reason, plan, and coordinate — often LLM/VLM-driven, increasingly as multi-agent systems.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/2405.10292" target="_blank" rel="noopener">RL4VLM: Fine-Tuning VLMs as Decision-Making Agents via RL</a><span class="paper-meta">🎯 Zhai et al. (incl. Xie) · NeurIPS 2024 · <a href="#group-b">deep dive ↑</a></span>The "VLM as an RL agent" recipe — the cleanest template for attaching a reward to a perception-capable agent.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2402.03310" target="_blank" rel="noopener">V-IRL: Grounding Virtual Intelligence in Real Life</a><span class="paper-meta">Yang et al. (incl. Xie) · ECCV 2024</span>Grounds virtual agents in real-world data — a bridge between simulation and reality.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2505.05108" target="_blank" rel="noopener">Multi-agent Embodied AI: Advances and Future Directions</a><span class="paper-meta">Survey · 2025</span>Frames the perception–action loop across multiple cooperating agents.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2508.05294" target="_blank" rel="noopener">Towards Embodied Agentic AI: Review &amp; Classification of LLM/VLM-Driven Robot Autonomy</a><span class="paper-meta">Survey · 2025</span>Architectures where the model acts as coordinator, planner, perception actor, or generalist interface.</div>
</div>

## 5 · Advanced MI — foundation models, spatial cognition &amp; VLAs

The generalist layer: models that unify perception, language, and action, and increasingly reason about space and time.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/2511.04670" target="_blank" rel="noopener">Cambrian-S: Towards Spatial Supersensing in Video</a><span class="paper-meta">Yang, …, Fei-Fei, Xie · ICLR 2026</span>Perceiving and reasoning about space over time — "moving to see better" at the model level.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2412.14171" target="_blank" rel="noopener">Thinking in Space: How Multimodal LLMs See, Remember and Recall Spaces</a><span class="paper-meta">Yang et al. (incl. Xie) · CVPR 2025</span>Studies spatial memory — how models build and recall a mental map.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2401.06209" target="_blank" rel="noopener">Eyes Wide Shut? Visual Shortcomings of Multimodal LLMs</a><span class="paper-meta">Tong et al. (incl. Xie) · CVPR 2024</span>Documents concrete perception failures — motivation that current models still see poorly.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2406.16860" target="_blank" rel="noopener">Cambrian-1: A Fully Open, Vision-Centric Exploration of Multimodal LLMs</a><span class="paper-meta">Tong et al. (incl. Xie) · NeurIPS 2024</span>A strong vision-centric MLLM baseline.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2405.14093" target="_blank" rel="noopener">A Survey on Vision-Language-Action Models for Embodied AI</a><span class="paper-meta">Survey · continuously updated</span>The reference VLA survey.</div>
</div>

## 6 · Evaluation &amp; benchmarks

The most important recent shift: judging world models by closed-loop *task success* and state-tracking, not pixels.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/2510.18135" target="_blank" rel="noopener">World-in-World: World Models in a Closed-Loop World</a><span class="paper-meta">🎯 Zhang et al. · ICLR 2026 (Oral) · <a href="#group-b">deep dive ↑</a></span>The first closed-loop platform; finds visual quality does not track task success, and controllability + action-observation post-training matter more.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2506.04363" target="_blank" rel="noopener">WorldPrediction: High-level World Modeling &amp; Long-horizon Procedural Planning</a><span class="paper-meta">Chen et al. · Meta · 2025 · <a href="#group-a">deep dive ↑</a></span>Frontier models reach only ~57% (WM) / ~38% (planning) vs. near-perfect humans — high-level planning is largely unsolved.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2502.20694" target="_blank" rel="noopener">WorldModelBench: Judging Video Generation Models as World Models</a><span class="paper-meta">2025</span>A benchmark for evaluating video generators specifically as world models.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2606.03920" target="_blank" rel="noopener">VSTAT: Benchmarking Visual State Tracking</a><span class="paper-meta">NYU (incl. Xie) · 2026 · <a href="#group-c">deep dive ↑</a></span>Best model ~44% vs. humans ~90% — models describe frames but can't track state over time.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2601.10592" target="_blank" rel="noopener">Action100M: A Large-scale Video Action Dataset</a><span class="paper-meta">Meta FAIR · 2026 · <a href="#group-a">deep dive ↑</a></span>~100M hierarchically labeled segments via an automated pipeline — a data substrate for perception/world-model work.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2204.08958" target="_blank" rel="noopener">MANIQA: Multi-dimension Attention Network for No-Reference IQA</a><span class="paper-meta">🎯 Yang et al. · CVPRW 2022 · <a href="#group-b">deep dive ↑</a></span>A template for scoring human-perceived quality from a single image (SRCC/PLCC vs. MOS) — useful for perception-aligned reward design.</div>
</div>

## 7 · Quality as a task-aligned signal for embodied perception <span class="dd-flag">🎯 Project-aligned cluster</span>

The newest, most directly relevant thread: using **image quality** to *guide* or *judge* embodied perception — and the finding that human-perceived quality transfers poorly to robot task success.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/2506.19844" target="_blank" rel="noopener">Active View Selector (AVS)</a><span class="paper-meta">🎯 Oxford · 2025 · <a href="#group-d">deep dive ↑</a></span>Move-to-improve view selection driven by predicted (cross-reference) image quality — but optimizes reconstruction fidelity, not task usefulness, and uses no learned policy.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2505.16815" target="_blank" rel="noopener">Image Quality Assessment for Embodied AI</a><span class="paper-meta">🎯 Li et al. · SJTU · 2025 · <a href="#group-d">deep dive ↑</a></span>Defines IQA-for-robots over a Perception–Cognition–Decision–Execution pipeline; shows human IQA metrics drop sharply on embodied data (static scoring only — no moving agent).</div>
  <div class="paper"><a href="https://arxiv.org/abs/2412.18774" target="_blank" rel="noopener">Embodied IQA for Robotic Intelligence (EPD / MA-EIQA)</a><span class="paper-meta">🎯 Zhang et al. · SJTU · 2025 · <a href="#group-d">deep dive ↑</a></span>Labels image quality by RL episode reward (no human), and ships a lightweight (48.83M-param) no-reference IQA model for robots; human vs. embodied MOS barely correlate (~0.13–0.21).</div>
</div>

## How to use this map for idea generation {#how-to-use}

A simple recipe I follow: (1) pick a **cluster** above; (2) read the surveys to get the taxonomy; (3) read 2–3 methods and their **evaluation**; (4) look for a *mismatch* — e.g. metrics that don't predict task success ([World-in-World](https://arxiv.org/abs/2510.18135)), or a capability humans have that models lack (state tracking, spatial recall), or a quality signal that ignores movement (Group D); (5) propose the smallest experiment that closes that gap. The recurring theme across the 2025–2026 literature — *visual realism is not utility* — is itself a fertile source of problems.

> **Verification note.** Links point to real, recent papers; the Saining Xie / NYU and Meta entries are taken from official pages, and the four "start here" IDs were independently confirmed. Several other entries — including the Group D trio — are preprints that may later change venue, title, or version. The reframing and the idea openings are my own analysis, not claims from the papers. **Confirm title/authors/venue at the source before formal citation.**

---

## References {#references}

1. D. Chen, W. Chung, Y. Bang, Z. Ji, and P. Fung. *WorldPrediction: A Benchmark for High-level World Modeling and Long-horizon Procedural Planning.* arXiv:2506.04363, Meta FAIR, 2025. <https://arxiv.org/abs/2506.04363>
2. Meta FAIR. *Action100M: A Large-scale Video Action Dataset.* arXiv:2601.10592, 2026. <https://arxiv.org/abs/2601.10592>
3. P. Fung et al. *Embodied AI Agents: Modeling the World.* arXiv:2506.22355, Meta, 2025. <https://arxiv.org/abs/2506.22355>
4. J. Zhang et al. *World-in-World: World Models in a Closed-Loop World.* arXiv:2510.18135, ICLR 2026 (Oral). <https://arxiv.org/abs/2510.18135>
5. S. Yang et al. *MANIQA: Multi-dimension Attention Network for No-Reference Image Quality Assessment.* CVPR Workshops, 2022. arXiv:2204.08958. <https://arxiv.org/abs/2204.08958>
6. *Reinforced Embodied Active Defense (Rein-EAD).* IEEE TPAMI, 2025. arXiv:2507.18484. <https://arxiv.org/abs/2507.18484>
7. Y. Zhai et al. *Fine-Tuning Large Vision-Language Models as Decision-Making Agents via Reinforcement Learning (RL4VLM).* NeurIPS, 2024. arXiv:2405.10292. <https://arxiv.org/abs/2405.10292>
8. P. Wu and S. Xie. *V\*: Guided Visual Search as a Core Mechanism in Multimodal LLMs.* CVPR, 2024. arXiv:2312.14135. <https://arxiv.org/abs/2312.14135>
9. G. Savva, O. Michel, …, S. Xie. *Solaris: Building a Multiplayer Video World Model in Minecraft.* arXiv:2602.22208, NYU, 2026. <https://arxiv.org/abs/2602.22208>
10. *VSTAT: Benchmarking Visual State Tracking in Multimodal Video Understanding.* arXiv:2606.03920, NYU, 2026. <https://arxiv.org/abs/2606.03920>
11. R. Wang, Y. Bhalgat, C. Li, and V. A. Prisacariu. *Active View Selector: Fast and Accurate Active View Selection with Cross-Reference Image Quality Assessment.* arXiv:2506.19844, University of Oxford, 2025. <https://arxiv.org/abs/2506.19844>
12. C. Li et al. *Image Quality Assessment for Embodied AI.* arXiv:2505.16815, 2025. <https://arxiv.org/abs/2505.16815>
13. J. Zhang et al. *Embodied Image Quality Assessment for Robotic Intelligence (EPD / MA-EIQA).* arXiv:2412.18774, Shanghai Jiao Tong University, 2025. <https://arxiv.org/abs/2412.18774>

<div class="wm-backlink wm-backlink-bottom">
  <a href="{{ '/blog/#world-models' | relative_url }}">&larr; Back to the <strong>World Models</strong> series</a>
</div>

<style>
.wm-backlink { margin: 0 0 1.2rem; font-size: 0.92rem; }
.wm-backlink-bottom { margin: 2rem 0 0; }
.wm-backlink a { color: var(--global-theme-color); text-decoration: none; }
.wm-backlink a:hover { text-decoration: underline; }
.rm-callout {
  border: 1px solid var(--global-divider-color);
  border-left: 4px solid var(--global-theme-color);
  background: var(--global-card-bg-color);
  border-radius: 10px;
  padding: 1rem 1.2rem;
  margin: 1.5rem 0;
}
.rm-callout ol { margin: 0.5rem 0 0; padding-left: 1.2rem; }
.rm-callout li { margin-bottom: 0.35rem; }
.rm-callout-note { display: block; margin-top: 0.7rem; font-size: 0.85rem; opacity: 0.8; }
.dd-nav { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1.4rem 0 0.5rem; }
.dd-nav a {
  font-size: 0.82rem;
  padding: 0.3rem 0.75rem;
  border: 1px solid var(--global-divider-color);
  border-radius: 999px;
  text-decoration: none;
  color: var(--global-text-color);
  transition: all 0.18s ease;
}
.dd-nav a:hover { background: var(--global-theme-color); color: #fff; border-color: var(--global-theme-color); }
.dd-meta {
  display: block;
  font-size: 0.82rem;
  opacity: 0.7;
  margin: -0.4rem 0 0.6rem;
}
.dd-meta a { font-weight: 500; }
.dd-flag {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: var(--global-theme-color);
  border: 1px solid var(--global-theme-color);
  border-radius: 999px;
  padding: 0.05rem 0.55rem;
  margin-left: 0.4rem;
  vertical-align: middle;
  white-space: nowrap;
}
.paper-list { display: flex; flex-direction: column; gap: 0.6rem; margin: 1rem 0 2rem; }
.paper {
  border-left: 3px solid var(--global-divider-color);
  padding: 0.55rem 0 0.55rem 0.9rem;
  font-size: 0.95rem;
  line-height: 1.5;
  transition: border-color 0.15s ease;
}
.paper:hover { border-left-color: var(--global-theme-color); }
.paper > a { font-weight: 600; }
.paper-meta {
  display: block;
  font-size: 0.8rem;
  opacity: 0.65;
  margin: 0.1rem 0 0.25rem;
}
.paper-meta a { font-weight: 500; }
</style>
