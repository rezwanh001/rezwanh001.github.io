---
layout: post
title: "World Models — Reading Map: Recent Literature (2024–2026)"
description: "A curated, annotated guide to the active-perception, world-model, and embodied-agent literature — organized by theme and meant as raw material for generating research ideas."
date: 2026-06-26 12:00:00
tags: [world-models, resources, reading-list, embodied-ai]
categories: world-models
wm_resource: true
giscus_comments: true
related_posts: false
---

<div class="wm-backlink">
  <a href="{{ '/blog/#world-models' | relative_url }}">&larr; Blogs · <strong>World Models</strong> series</a>
</div>

This is a **living reading map** for the World Models series — a curated, thematically organized guide to the recent literature on world models, active perception, and agentic embodied AI. I treat these papers as the best raw material for *idea generation*: read across a cluster, find the gap, build there.

It pairs with the conceptual primer in **[Part 0: From Language Models to World Models]({{ '/blog/2026/world-models-introduction/' | relative_url }})**. Annotations are paraphrased in my own words; many entries are fast-moving preprints, so **open each link and confirm title/authors/venue before citing in a formal document**.

<div class="rm-callout">
  <strong>⭐ Start here (four high-leverage reads):</strong>
  <ol>
    <li><a href="https://arxiv.org/abs/2506.22355" target="_blank" rel="noopener">Embodied AI Agents: Modeling the World</a> — the position paper that makes the world model the <em>core</em> of embodied agents.</li>
    <li><a href="https://arxiv.org/abs/2510.18135" target="_blank" rel="noopener">World-in-World</a> — closed-loop evidence that visual realism ≠ task success.</li>
    <li><a href="https://arxiv.org/abs/2506.04363" target="_blank" rel="noopener">WorldPrediction</a> — a benchmark showing high-level procedural planning is largely unsolved.</li>
    <li><a href="https://arxiv.org/abs/2312.14135" target="_blank" rel="noopener">V*</a> — "where to look" as a learnable skill inside a multimodal model.</li>
  </ol>
</div>

---

## 1 · Foundations & framing

The classics that define the vocabulary, plus the position papers that set today's agenda.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/1803.10122" target="_blank" rel="noopener">World Models</a><span class="paper-meta">Ha &amp; Schmidhuber · NeurIPS 2018</span>The canonical V–M–C blueprint: compress observations, learn latent dynamics, train a tiny controller — and learn inside the model's "dream".</div>
  <div class="paper"><a href="https://openreview.net/forum?id=BZ5a1r-kVsf" target="_blank" rel="noopener">A Path Towards Autonomous Machine Intelligence</a><span class="paper-meta">LeCun · 2022</span>The JEPA manifesto: a modular, predictive, world-model-centric architecture as a route past pure text prediction.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2506.22355" target="_blank" rel="noopener">Embodied AI Agents: Modeling the World</a><span class="paper-meta">Fung et al. · Meta · 2025</span>Argues perception + reasoning-for-action + memory should be unified inside a world model, and adds a "mental world model" (Theory-of-Mind) layer.</div>
</div>

## 2 · World models for embodied agents

Surveys that organize the field, and the two method families that dominate: video-generation vs. latent-prediction world models.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/2605.00080" target="_blank" rel="noopener">World Model for Robot Learning: A Comprehensive Survey</a><span class="paper-meta">Survey · 2026</span>Stresses <em>action-conditioned</em> world models — visually plausible but action-inconsistent futures are of limited value for control.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2510.16732" target="_blank" rel="noopener">A Comprehensive Survey on World Models for Embodied AI</a><span class="paper-meta">Survey · 2025</span>A taxonomy across functionality, temporal modeling, and spatial representation.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2602.22208" target="_blank" rel="noopener">Solaris: Building a Multiplayer Video World Model in Minecraft</a><span class="paper-meta">Savva, …, Xie · NYU · 2026</span>A multiplayer video world model predicting consistent shared views — directly relevant to multi-agent / shared visual understanding.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2506.01182" target="_blank" rel="noopener">Humanoid World Models</a><span class="paper-meta">2025</span>Open foundation world models for humanoid robotics.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2509.21790" target="_blank" rel="noopener">LongScape: Long-Horizon Embodied World Models with Context-Aware MoE</a><span class="paper-meta">2025</span>Tackles long-horizon generation with a context-aware mixture of experts.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2601.15282" target="_blank" rel="noopener">Rethinking Video Generation Model for the Embodied World</a><span class="paper-meta">2026</span>Reconsiders what video generators need in order to be useful as world models for embodiment.</div>
</div>

## 3 · Active perception — "moving to see better"

Agents that choose where to look or move in order to perceive better — increasingly trained with RL rather than hand-designed next-best-view rules.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/2507.18484" target="_blank" rel="noopener">Reinforced Embodied Active Defense (Rein-EAD)</a><span class="paper-meta">TPAMI 2025 · Tsinghua</span>An RL "take a second look" policy with uncertainty-aware dense rewards — the closest existing mechanism to "move to see better".</div>
  <div class="paper"><a href="https://arxiv.org/abs/2312.14135" target="_blank" rel="noopener">V*: Guided Visual Search as a Core Mechanism in Multimodal LLMs</a><span class="paper-meta">Wu &amp; Xie · CVPR 2024</span>The SEAL framework decides <em>where to look</em> in an image before answering — the model-side analog of active perception.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2506.15666" target="_blank" rel="noopener">Vision in Action: Learning Active Perception from Human Demonstrations</a><span class="paper-meta">2025</span>Learns active viewpoint behaviors from human demos.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2512.01188" target="_blank" rel="noopener">Real-World Reinforcement Learning of Active Perception Behaviors</a><span class="paper-meta">2025</span>Trains active-sensing behaviors directly in the real world.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2602.04600" target="_blank" rel="noopener">Act, Sense, Act: Non-Markovian Active Perception from Egocentric Human Data</a><span class="paper-meta">2026</span>Learns non-Markovian active-perception strategies at scale from egocentric video.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2603.12193" target="_blank" rel="noopener">SaPaVe: Active Perception and Manipulation in VLA Models</a><span class="paper-meta">2026</span>Adds active perception + manipulation into vision-language-action models.</div>
</div>

## 4 · Agentic &amp; multi-agent embodied AI

Agents that reason, plan, and coordinate — often LLM/VLM-driven, increasingly as multi-agent systems.

<div class="paper-list">
  <div class="paper"><a href="https://arxiv.org/abs/2405.10292" target="_blank" rel="noopener">RL4VLM: Fine-Tuning VLMs as Decision-Making Agents via RL</a><span class="paper-meta">Zhai et al. (incl. Xie) · NeurIPS 2024</span>The "VLM as an RL agent" recipe — the cleanest template for attaching a reward to a perception-capable agent.</div>
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
  <div class="paper"><a href="https://arxiv.org/abs/2510.18135" target="_blank" rel="noopener">World-in-World: World Models in a Closed-Loop World</a><span class="paper-meta">Zhang et al. · ICLR 2026 (Oral)</span>The first closed-loop platform; finds visual quality does not track task success, and controllability + action-observation post-training matter more.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2506.04363" target="_blank" rel="noopener">WorldPrediction: High-level World Modeling &amp; Long-horizon Procedural Planning</a><span class="paper-meta">Chen et al. · Meta · 2025</span>Frontier models reach only ~57% (WM) / ~38% (planning) vs. near-perfect humans — high-level planning is largely unsolved.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2502.20694" target="_blank" rel="noopener">WorldModelBench: Judging Video Generation Models as World Models</a><span class="paper-meta">2025</span>A benchmark for evaluating video generators specifically as world models.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2606.03920" target="_blank" rel="noopener">VSTAT: Benchmarking Visual State Tracking</a><span class="paper-meta">NYU (incl. Xie) · 2026</span>Best model ~44% vs. humans ~90% — models describe frames but can't track state over time.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2601.10592" target="_blank" rel="noopener">Action100M: A Large-scale Video Action Dataset</a><span class="paper-meta">Meta FAIR · 2026</span>~100M hierarchically labeled segments via an automated pipeline — a data substrate for perception/world-model work.</div>
  <div class="paper"><a href="https://arxiv.org/abs/2204.08958" target="_blank" rel="noopener">MANIQA: Multi-dimension Attention Network for No-Reference IQA</a><span class="paper-meta">Yang et al. · CVPRW 2022</span>A template for scoring human-perceived quality from a single image (SRCC/PLCC vs. MOS) — useful for perception-aligned reward design.</div>
</div>

---

## How to use this map for idea generation

A simple recipe I follow: (1) pick a **cluster** above; (2) read the surveys to get the taxonomy; (3) read 2–3 methods and their **evaluation**; (4) look for a *mismatch* — e.g. metrics that don't predict task success ([World-in-World](https://arxiv.org/abs/2510.18135)), or a capability humans have that models lack (state tracking, spatial recall); (5) propose the smallest experiment that closes that gap. The recurring theme across the 2025–2026 literature — *visual realism is not utility* — is itself a fertile source of problems.

> **Verification note.** Links point to real, recent papers; the Saining Xie / NYU and Meta entries are taken from official pages, and the four "start here" IDs were independently confirmed. Several other entries are preprints that may later change venue or version — confirm before formal citation.

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
</style>
