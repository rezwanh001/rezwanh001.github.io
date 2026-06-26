---
layout: distill
title: "World Models — Part 0: From Language Models to World Models"
description: "A ground-up introduction: why next-token prediction is not enough, what a world model actually is, and why learning to predict the future of an environment may be the next step toward grounded, agentic intelligence."
date: 2026-06-26
tags: [world-models, introduction, llm, jepa]
categories: world-models
giscus_comments: true
related_posts: false
featured: false

authors:
  - name: Md Rezwanul Haque
    url: "https://rezwan.xyz/"
    affiliations:
      name: CPAMI Lab, University of Waterloo

bibliography: world_models.bib

toc:
  - name: Why this series
  - name: The triumph (and the ceiling) of language models
  - name: So what is a world model?
  - name: The anatomy of a world model
  - name: Why world models matter
  - name: Predicting pixels vs. predicting representations
  - name: A quick tour of the landscape
  - name: Where this series is going
  - name: How to cite this post
---

<div class="wm-backlink">
  <a href="{{ '/blog/#world-models' | relative_url }}">&larr; Blogs · <strong>World Models</strong> series</a>
</div>

> **TL;DR.** A language model learns the statistics of *text*. A **world model** learns the dynamics of an *environment* — given where you are and what you do, what happens next. This post starts from the familiar next-token objective, shows precisely where it stops being enough for agents that must *act*, and builds up the idea of a world model from first principles. It is **Part 0** of a step-by-step series that will go from these basics down into the contemporary research literature.

---

## Why this series

I'm writing this series the way I wish someone had written it for me: starting at the very beginning and going deep, one step at a time. Each part is a standalone Markdown post — I'll fold in formal definitions, intuition, figures, and, where relevant, my own proposals and notes. Everything is **properly referenced** so that if any of this helps your own paper, you can cite the primary sources directly (and this post too — see the [last section](#how-to-cite-this-post)).

If you prefer to *watch* an excellent framing of the same shift — from large language models toward joint-embedding world models — the talk *"From LLM to JEPA"* is a great companion to this post <d-cite key="amilabs2026fromllm"></d-cite>:

<div class="wm-video">
  <iframe src="https://www.youtube.com/embed/UaHwJeCMzso" title="From LLM to JEPA — AMI Labs" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

---

## The triumph (and the ceiling) of language models

A modern large language model (LLM) is, at heart, an autoregressive next-token predictor <d-cite key="vaswani2017attention"></d-cite><d-cite key="brown2020gpt3"></d-cite>. Given a sequence of tokens $$x_{1}, \dots, x_{t-1}$$, it models the probability of the next one,

$$
p_\theta(x_t \mid x_{1:t-1}),
$$

and the probability of an entire sequence factorizes by the chain rule:

$$
p_\theta(x_{1:T}) = \prod_{t=1}^{T} p_\theta(x_t \mid x_{1:t-1}).
$$

Training minimizes the negative log-likelihood (equivalently, cross-entropy) of the next token,

$$
\mathcal{L}_{\text{LM}}(\theta) = - \, \mathbb{E}_{x \sim \mathcal{D}} \sum_{t=1}^{T} \log p_\theta(x_t \mid x_{1:t-1}).
$$

This single objective, scaled up, produces astonishing competence. But notice *what* is being modeled: the distribution of **human-generated text**. An LLM is a model of *what a person is likely to write next* — not a model of *what the world will do next*. Those coincide only to the extent that text faithfully describes reality, which is often loosely, sometimes not at all.

For an agent that must **perceive, decide, and act**, three gaps open up:

1. **No grounded dynamics.** Text rarely encodes the precise physical consequences of actions. "I pushed the glass" does not contain the trajectory, the friction, or the shatter.
2. **No native notion of action.** The LM conditions on past *tokens*, not on an agent's *actions* $$a_t$$ and their effect on a *state*.
3. **Planning is implicit and ungrounded.** "Reasoning" emerges as more token generation, with no internal simulator to roll out and compare candidate futures.

This is the ceiling. To cross it we need a model whose variables are **states and actions**, not just words.

---

## So what is a world model?

Informally, a **world model** is an internal, predictive model of how an environment evolves — a learned simulator you can query: *"if the state is this and I do that, what happens?"* The idea is old: self-supervised recurrent predictors of the environment <d-cite key="schmidhuber1990making"></d-cite> and model-based planning in reinforcement learning <d-cite key="sutton1991dyna"></d-cite><d-cite key="sutton2018reinforcement"></d-cite> are its direct ancestors.

Formally, most agentic settings are **partially observed**: the agent never sees the true state $$s_t$$, only observations $$o_t$$ (pixels, sensors). A world model introduces a compact **latent state** $$z_t$$ and learns three pieces:

$$
\underbrace{z_t \sim q_\phi(z_t \mid z_{t-1}, a_{t-1}, o_t)}_{\text{(1) encoder / inference}}, \qquad
\underbrace{z_{t} \sim p_\theta(z_t \mid z_{t-1}, a_{t-1})}_{\text{(2) latent transition (the "dynamics")}},
$$

$$
\underbrace{\hat{o}_t \sim p_\theta(o_t \mid z_t), \quad \hat{r}_t \sim p_\theta(r_t \mid z_t)}_{\text{(3) decoders: reconstruct observation \& reward}}.
$$

The contrast with an LLM is now sharp and worth stating side by side:

| | Language model | World model |
|---|---|---|
| Predicts | next **token** $$x_t$$ | next **state/observation** $$z_{t+1}, o_{t+1}$$ |
| Conditioned on | past tokens $$x_{<t}$$ | past state **and action** $$z_t, a_t$$ |
| Models the statistics of | human text | environment **dynamics** |
| "Reasoning" = | more token generation | **rolling out futures** in latent space |
| Native to | dialogue, code, retrieval | perception, planning, control |

The key new ingredient is the **action** $$a_t$$: a world model is *conditional on what the agent does*. That is exactly the variable a language model lacks, and exactly the variable an agent needs.

---

## The anatomy of a world model

The cleanest starting blueprint is Ha &amp; Schmidhuber's **V–M–C** decomposition <d-cite key="ha2018worldmodels"></d-cite>:

- **V — Vision.** An encoder (classically a variational autoencoder <d-cite key="kingma2014vae"></d-cite>) compresses each high-dimensional observation $$o_t$$ into a small latent code $$z_t$$.
- **M — Memory.** A recurrent (or, today, Transformer) dynamics model predicts the next latent given the current latent and action, $$p_\theta(z_{t+1}\mid z_t, a_t, h_t)$$, carrying history in its hidden state $$h_t$$.
- **C — Controller.** A small policy $$\pi(a_t \mid z_t, h_t)$$ chooses actions from the *compressed* state. Because V and M did the heavy lifting, C can be tiny.

<div class="wm-figure">
<svg viewBox="0 0 760 230" role="img" aria-label="The perceive–model–imagine–act loop of a world model" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;color:var(--global-text-color);">
  <defs>
    <marker id="wmArrow" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="currentColor"></path>
    </marker>
  </defs>
  <!-- boxes -->
  <g fill="none" stroke="currentColor" stroke-width="1.6">
    <rect x="20"  y="90" width="120" height="50" rx="8"></rect>
    <rect x="200" y="90" width="120" height="50" rx="8"></rect>
    <rect x="380" y="90" width="150" height="50" rx="8"></rect>
    <rect x="590" y="90" width="150" height="50" rx="8"></rect>
  </g>
  <g fill="currentColor" font-size="13" text-anchor="middle" font-family="inherit">
    <text x="80"  y="112">Environment</text>
    <text x="80"  y="129">obs o&#8348;</text>
    <text x="260" y="112">Encoder (V)</text>
    <text x="260" y="129">o&#8348; &#8594; z&#8348;</text>
    <text x="455" y="112">Dynamics (M)</text>
    <text x="455" y="129">z&#8348;,a&#8348; &#8594; z&#8348;&#8330;&#8321;</text>
    <text x="665" y="112">Controller (C)</text>
    <text x="665" y="129">&#960;(a&#8348;|z&#8348;)</text>
  </g>
  <!-- arrows forward -->
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#wmArrow)">
    <line x1="140" y1="115" x2="198" y2="115"></line>
    <line x1="320" y1="115" x2="378" y2="115"></line>
    <line x1="530" y1="115" x2="588" y2="115"></line>
  </g>
  <!-- action feedback loop C -> Environment -->
  <g stroke="currentColor" stroke-width="1.6" fill="none" marker-end="url(#wmArrow)" stroke-dasharray="5 4">
    <path d="M665,140 L665,195 L80,195 L80,142"></path>
  </g>
  <text x="372" y="212" fill="currentColor" font-size="12" text-anchor="middle" font-style="italic">action a&#8348; closes the loop — and can also be rolled out purely in imagination (z&#8348; &#8594; z&#8348;&#8330;&#8321; &#8594; &#8943;)</text>
</svg>
<figcaption>The perceive → encode → predict → act loop. Once <em>Dynamics (M)</em> is trained, the agent can roll the loop forward <strong>without touching the real environment</strong> — "dreaming" trajectories to plan or to train the controller.</figcaption>
</div>

That last point is the magic: a trained dynamics model lets you generate experience **in imagination**, decoupling learning from expensive real-world interaction.

---

## Why world models matter

**1. Sample efficiency — learning in a dream.** If $$p_\theta(z_{t+1}\mid z_t,a_t)$$ is accurate, the controller can be optimized on *imagined* rollouts instead of real ones. This is exactly the Dreamer line of work, which learns behaviors "by latent imagination" and scales across hundreds of tasks from a single configuration <d-cite key="hafner2020dreamer"></d-cite><d-cite key="hafner2021dreamerv2"></d-cite><d-cite key="hafner2023dreamerv3"></d-cite>. Concretely, the controller maximizes imagined return

$$
\max_{\pi}\; \mathbb{E}_{p_\theta,\,\pi}\!\left[\sum_{\tau=t}^{t+H} \gamma^{\,\tau-t}\, \hat{r}_\tau \right],
$$

with the *whole rollout* synthesized by the model over a horizon $$H$$.

**2. Planning &amp; reasoning that is grounded.** With a simulator inside its head, an agent can search over action sequences, compare outcomes, and choose — model-predictive control, rather than reflex.

**3. Generalization &amp; grounding.** Forcing a network to predict consequences pressures it to discover the *causal structure* of its environment (objects, physics, agency) — representations that transfer.

**4. A candidate path to autonomous machine intelligence.** This is the thesis behind LeCun's proposal for a modular, predictive, world-model-centric architecture as a route past the limits of pure text prediction <d-cite key="lecun2022path"></d-cite>.

---

## Predicting pixels vs. predicting representations

There is a subtle but crucial design choice hiding in decoder (3) above. Do we predict the **raw future observation** (every pixel), or only a **representation** of it?

- **Generative world models** reconstruct observations: great for visualization and interpretability, but they spend capacity modeling unpredictable, irrelevant detail (every leaf, every texture).
- **Joint-Embedding Predictive Architectures (JEPA)** instead predict in a *learned latent space*: given a context embedding $$s_x$$ and a target embedding $$s_y$$, a predictor $$P$$ with latent variable $$v$$ minimizes an energy

$$
E(x, y) = \big\| \, s_y - P(s_x, v) \, \big\|^2 ,
$$

so the model is rewarded for capturing *predictable structure* and free to *discard* unpredictable noise <d-cite key="lecun2022path"></d-cite><d-cite key="assran2023ijepa"></d-cite>. This is the "From LLM to JEPA" shift in one equation: stop predicting every token/pixel, start predicting the *abstract state* that actually matters for acting.

---

## A quick tour of the landscape

A non-exhaustive map of where the field is, to orient the rest of the series:

- **Foundational latent world models for control** — Ha &amp; Schmidhuber <d-cite key="ha2018worldmodels"></d-cite>; the Dreamer family <d-cite key="hafner2020dreamer"></d-cite><d-cite key="hafner2021dreamerv2"></d-cite><d-cite key="hafner2023dreamerv3"></d-cite>.
- **Joint-embedding / non-generative prediction** — the JEPA program <d-cite key="lecun2022path"></d-cite><d-cite key="assran2023ijepa"></d-cite>.
- **Generative interactive environments** — Genie learns *action-controllable* worlds from unlabeled video <d-cite key="bruce2024genie"></d-cite>.
- **Video generators as world simulators** — large video models exhibiting emergent simulation of physics and persistence <d-cite key="openai2024sora"></d-cite>.

The contemporary literature here is *vast* and moving fast; throughout the series I'll treat recent papers as the best raw material for generating new research ideas, and I'll keep adding them to the [series bibliography](#how-to-cite-this-post).

---

## Where this series is going

This was Part 0 — the *why* and the vocabulary. Upcoming parts (added one by one) will go deep, with derivations and code, into: latent-variable models and the VAE/ELBO; recurrent vs. Transformer dynamics; the full Dreamer objective; JEPA and energy-based learning; generative interactive worlds (Genie / Sora); evaluation; and open problems and proposals. Each will live in its own post under the **World Models** section of the [blog]({{ '/blog/#world-models' | relative_url }}).

Comments are open at the bottom of every post — feedback, corrections, and pointers to papers I should cover are very welcome.

---

## How to cite this post

If this series is useful for your work, please cite the **primary sources** in the bibliography below (rendered automatically from `world_models.bib`). To reference this post itself:

```bibtex
@misc{haque2026worldmodels0,
  author = {Md Rezwanul Haque},
  title  = {World Models --- Part 0: From Language Models to World Models},
  year   = {2026},
  howpublished = {\url{https://rezwan.xyz/blog/2026/world-models-introduction/}},
  note   = {Blog post, CPAMI Lab, University of Waterloo}
}
```

<div class="wm-backlink wm-backlink-bottom">
  <a href="{{ '/blog/#world-models' | relative_url }}">&larr; Back to the <strong>World Models</strong> series</a>
</div>

<style>
.wm-backlink { margin: 0 0 1.2rem; font-size: 0.92rem; }
.wm-backlink-bottom { margin: 2rem 0 0; }
.wm-backlink a { color: var(--global-theme-color); text-decoration: none; }
.wm-backlink a:hover { text-decoration: underline; }
.wm-video {
  position: relative; width: 100%; padding-bottom: 56.25%; height: 0;
  margin: 1.2rem 0; border-radius: 10px; overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.12);
}
.wm-video iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
.wm-figure { margin: 1.5rem 0; }
.wm-figure figcaption {
  margin-top: 0.6rem; font-size: 0.88rem; opacity: 0.8;
  text-align: center; color: var(--global-text-color);
}
</style>
