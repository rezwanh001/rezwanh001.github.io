---
layout: post
title: "World Models — Deep Dives: Ten Key Papers"
description: "Beyond a reading list: each key paper read for its gist, pipeline, benchmark & dataset, results, and — most importantly — where the scope for improvement and unique research ideas lie."
date: 2026-06-26 13:00:00
tags: [world-models, resources, deep-dives, embodied-ai]
categories: world-models
wm_resource: true
giscus_comments: true
related_posts: false
---

<div class="wm-backlink">
  <a href="{{ '/blog/#world-models' | relative_url }}">&larr; Blogs · <strong>World Models</strong> series</a>
</div>

A reading list tells you *what* exists; this page tells you *why each paper matters*. For ten key papers I read each one along the same axes — **gist · pipeline · benchmark & dataset · results · scope & unique ideas** — so the page doubles as an idea-generation worksheet. Full plain-text citations are at the [bottom](#references); the companion broad index is the **[Reading Map]({{ '/blog/2026/world-models-reading-map/' | relative_url }})**, and the concepts are introduced in **[Part 0]({{ '/blog/2026/world-models-introduction/' | relative_url }})**.

> These notes are paraphrased from my own reading; several entries are fast-moving preprints — confirm details at the source before formal citation.

---

# Group A — World models & the data/agenda layer

## 1 · WorldPrediction
<span class="dd-meta">Chen, Chung, Bang, Ji &amp; Fung · Meta FAIR · 2025 · <a href="https://arxiv.org/abs/2506.04363" target="_blank" rel="noopener">arXiv:2506.04363</a></span>

**Gist.** Visual realism ≠ planning ability — high-level, abstract-action planning is largely unsolved, and the authors suspect *perception* is the bottleneck.

- **Problem &amp; pipeline.** Do models have a world model good enough for *high-level, long-horizon* procedural planning (not just low-level motion)? Formalized as a partially observable semi-MDP. Given initial and final visual states, the model must pick the correct action (WM track) or the correctly ordered action sequence (PP track) from counterfactual distractors. The clever trick: "action equivalents" (the same action in a different context) as distractors, so models can't cheat using low-level background continuity; heavy human filtering.
- **Benchmark / dataset / metrics.** Two tracks (WM, PP) scored by discriminative accuracy; data drawn from procedural-video sources (COIN, CrossTask, EgoExo4D, IKEA-ASM).
- **Results.** Best models ≈ **57%** (world modeling) and **38%** (procedural planning) versus humans near-perfect; bigger models barely help planning.
- **Scope &amp; unique ideas.** A ready-made target to test whether *better perception lifts planning*. The "action-equivalents" construction is a clean, reusable way to force semantic over pixel reasoning — worth copying for any new benchmark.

## 2 · Action100M
<span class="dd-meta">Meta FAIR · 2026 · <a href="https://arxiv.org/abs/2601.10592" target="_blank" rel="noopener">arXiv:2601.10592</a></span>

**Gist.** Automated, hierarchical annotation can replace manual labeling at scale, and predictive (JEPA) representations keep improving with more data.

- **Problem &amp; pipeline.** Action understanding needs huge, open-vocabulary, hierarchically labeled video, but manual labeling doesn't scale. They build ~100M labeled segments from 1.2M instructional videos with a fully automated pipeline: (i) hierarchical temporal segmentation using **V-JEPA 2** embeddings; (ii) multi-level captions arranged as a *Tree-of-Captions*; (iii) aggregation by a reasoning model (GPT-OSS-120B) under multi-round **Self-Refine** to reduce hallucinations and emit structured fields (action, actor, captions).
- **Benchmark / dataset / metrics.** The dataset itself (~100M segments / 1.2M videos); evaluated by zero-shot action-recognition transfer and data-scaling curves. Descends from HowTo100M and the JEPA representation line.
- **Results.** A trained VL-JEPA model shows consistent data-scaling gains and strong zero-shot action recognition.
- **Scope &amp; unique ideas.** A data substrate for perception / world-model work; the motion→task hierarchy suits multi-level reasoning. Practical caveat: only a 10% preview is public; the full set is gated.

## 3 · Embodied AI Agents: Modeling the World
<span class="dd-meta">Fung et al. · Meta · 2025 · <a href="https://arxiv.org/abs/2506.22355" target="_blank" rel="noopener">arXiv:2506.22355</a></span>

**Gist.** Perception, planning, and memory should be unified *inside a world model*; embodiment plus social/mental modeling is the agenda.

- **Problem &amp; pipeline.** How should embodied agents (avatars, wearables, robots) be built to learn and act like humans? A research-vision paper, not an experiment. Proposes unifying multimodal perception + reasoning-for-action + memory inside a world model, and adds *mental world models* that infer user intentions and social context (a Theory-of-Mind layer).
- **Benchmark / dataset / metrics.** None of its own; it organizes the field and references existing benchmarks, contributing a virtual/wearable/robotic agent taxonomy.
- **Results.** No single model, no accuracy number — its value is the framing.
- **Scope &amp; unique ideas.** The umbrella that legitimizes a perception-quality-inside-world-models direction. Its Theory-of-Mind thread is itself a possible project (user-intention modeling).

---

# Group B — "Moving to see better" (active perception)

## 4 · World-in-World
<span class="dd-meta">Zhang et al. · ICLR 2026 (Oral) · <a href="https://arxiv.org/abs/2510.18135" target="_blank" rel="noopener">arXiv:2510.18135</a></span>

**Gist.** Judge world models by closed-loop *task success*, not pixels — the most direct evidence for a task-coupled metric.

- **Problem &amp; pipeline.** Do generative world models actually help agents *succeed*, or do we only measure visual quality? They build the first closed-loop platform with a unified online planner and a standardized action API, across four environments (perception, navigation, manipulation) where task success is the primary metric.
- **Benchmark / dataset / metrics.** Task success rate (primary) plotted against visual-quality scores (FID/FVD-style), revealing weak correlation.
- **Results.** High visual quality does **not** translate into task success; scaling post-training on action-observation data beats upgrading the generator; more inference-time planning compute helps.
- **Scope &amp; unique ideas.** Cite as the empirical backbone of a perception-aligned, task-coupled reward; reuse its closed-loop, task-success evaluation philosophy to show a quality reward improves outcomes.

## 5 · MANIQA
<span class="dd-meta">Yang et al. · CVPRW 2022 · <a href="https://arxiv.org/abs/2204.08958" target="_blank" rel="noopener">arXiv:2204.08958</a></span>

**Gist.** A single image can be scored for human-perceived quality with *no reference*, and attention across both channel and space matters.

- **Problem &amp; pipeline.** No-reference image quality assessment (score perceptual quality from the image alone) was weak on GAN-type distortions. Extract features with a ViT, then a **Transposed Attention Block** (channel dimension) and a **Scale Swin Transformer Block** (spatial dimension), with a dual-branch patch-weighted score head.
- **Benchmark / dataset / metrics.** LIVE, TID2013, CSIQ, KADID-10K; correlation with human MOS via **SRCC/PLCC**.
- **Results.** State-of-the-art on those datasets and first place in the NTIRE 2022 no-reference challenge.
- **Scope &amp; unique ideas.** A concrete starting architecture for a "view-quality" metric *Q*; learn its MOS-regression recipe and adapt it from "image quality" to "view usefulness for a task."

## 6 · Rein-EAD (Reinforced Embodied Active Defense)
<span class="dd-meta">TPAMI 2025 · <a href="https://arxiv.org/abs/2507.18484" target="_blank" rel="noopener">arXiv:2507.18484</a></span>

**Gist.** Moving to re-observe, driven by a dense uncertainty reward, beats single-shot perception — the closest existing mechanism to "move to see better."

- **Problem &amp; pipeline.** Passive perception is fragile to adversarial and 3D attacks. A recurrent feedback loop takes multiple looks; an **uncertainty-aware guided dense reward** shapes where to move and observe; scene understanding is rebuilt over steps rather than judged from one frame.
- **Benchmark / dataset / metrics.** Adversarial robustness / defense metrics under patch and 3D attacks (not perceptual-quality indices).
- **Results.** Improves robustness while staying computationally efficient.
- **Scope &amp; unique ideas.** Its RL loop and dense-reward design are directly reusable — swap the uncertainty/defense reward for a human-aligned quality reward.

## 7 · RL4VLM
<span class="dd-meta">Zhai et al. (incl. Xie) · NeurIPS 2024 · <a href="https://arxiv.org/abs/2405.10292" target="_blank" rel="noopener">arXiv:2405.10292</a></span>

**Gist.** Attach an RL reward to a perception-capable model and you get an agent — the recipe for turning *any* reward into behavior.

- **Problem &amp; pipeline.** VLMs perceive well but decide poorly. Treat the VLM as a policy that reasons step-by-step (chain-of-thought) and then emits actions, trained end-to-end with task reward in gym-like multimodal environments.
- **Benchmark / dataset / metrics.** Interactive decision tasks (card games, embodied / ALFWorld-style), scored by success/reward.
- **Results.** Improves decision-making over prompting and supervised baselines.
- **Scope &amp; unique ideas.** The practical template for wiring a custom (e.g. perceptual-quality) reward into a perception-capable agent; study how they balance reasoning and action.

## 8 · V\*
<span class="dd-meta">Wu &amp; Xie · CVPR 2024 · <a href="https://arxiv.org/abs/2312.14135" target="_blank" rel="noopener">arXiv:2312.14135</a></span>

**Gist.** Deciding *where to attend*, rather than consuming everything at once, is itself a learnable, performance-critical skill — the model-side analog of active perception.

- **Problem &amp; pipeline.** Multimodal LLMs miss small details in high-resolution images because they look once, globally. The **SEAL** framework uses context to guide an iterative search that zooms to the relevant region before answering.
- **Benchmark / dataset / metrics.** Introduces **V\*Bench** for fine-detail visual-QA accuracy.
- **Results.** Accurate on fine-detail visual questions where standard MLLMs fail.
- **Scope &amp; unique ideas.** Conceptual grounding for "where to look"; even with a moving robot, the search-then-decide structure transfers.

---

# Group C — Multi-agent & state tracking

## 9 · Solaris
<span class="dd-meta">Savva, Michel, …, Xie · NYU · 2026 · <a href="https://arxiv.org/abs/2602.22208" target="_blank" rel="noopener">arXiv:2602.22208</a></span>

**Gist.** World models can be multi-agent and *must* keep shared views consistent — directly relevant to shared visual understanding.

- **Problem &amp; pipeline.** Can a video world model serve *multiple* agents with consistent shared views (a "multiplayer" world model)? Built in Minecraft, predicting consistent first-person views for two players via a staged single→multiplayer pipeline (bidirectional, causal, and Self-Forcing training), backed by a multiplayer data system (~12.6M multiplayer frames).
- **Benchmark / dataset / metrics.** Co-observation consistency, grounding, memory, movement, and building metrics.
- **Results.** A technical report — treat the numbers as preliminary.
- **Scope &amp; unique ideas.** If you keep a multi-agent strand, this is *the* reference for cross-agent visual consistency, and its consistency metric is reusable.

## 10 · VSTAT
<span class="dd-meta">NYU (incl. Xie) · 2026 · <a href="https://arxiv.org/abs/2606.03920" target="_blank" rel="noopener">arXiv:2606.03920</a></span>

**Gist.** Models can describe a frame but cannot *track state over time* — a concrete, quantified gap that motivates world-model and memory work.

- **Problem &amp; pipeline.** Can video MLLMs track fine-grained visual state over time (counts, attributes, order)? A benchmark of procedural videos with state-tracking questions: 834 clips and ~1,500 questions across synthetic, self-recorded, and real videos, forcing a running mental model of object states.
- **Benchmark / dataset / metrics.** VSTAT accuracy, with the large human–model gap as the headline index.
- **Results.** Best model (~Gemini-3.1 Pro) ≈ **44.4** versus humans ≈ **90.5**.
- **Scope &amp; unique ideas.** Motivation and a possible evaluation axis for world-model / memory work; its human-vs-model gap framing mirrors the broader "metrics don't equal usefulness" argument.

---

## A cross-cutting idea seed

Three of these papers — WorldPrediction, World-in-World, and VSTAT — independently report the same thing from different angles: **today's models look good but act, plan, and remember poorly, and our pixel-level metrics fail to predict task usefulness.** The clean research opening is a *perception-aligned, task-coupled* signal (a learned view-quality reward in the spirit of MANIQA) wired into an active agent (à la Rein-EAD / RL4VLM) and judged in closed loop (à la World-in-World). That is a single, defensible thread the newest literature is pointing toward.

---

## References

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

<div class="wm-backlink wm-backlink-bottom">
  <a href="{{ '/blog/#world-models' | relative_url }}">&larr; Back to the <strong>World Models</strong> series</a>
</div>

<style>
.wm-backlink { margin: 0 0 1.2rem; font-size: 0.92rem; }
.wm-backlink-bottom { margin: 2rem 0 0; }
.wm-backlink a { color: var(--global-theme-color); text-decoration: none; }
.wm-backlink a:hover { text-decoration: underline; }
.dd-meta {
  display: block;
  font-size: 0.82rem;
  opacity: 0.7;
  margin: -0.4rem 0 0.6rem;
}
.dd-meta a { font-weight: 500; }
</style>
