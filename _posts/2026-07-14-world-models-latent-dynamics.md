---
layout: distill
title: "World Models — Part 1: Inside the Latent (VAEs, RSSM, and Learning in a Dream)"
description: "The machinery, derived from scratch: why we compress pixels into a latent, how the VAE and the ELBO actually work, how a Recurrent State-Space Model turns a single-frame encoder into a simulator, and how Dreamer trains a policy entirely inside its own imagination — with the real systems that run on these ideas today."
date: 2026-07-14
tags: [world-models, vae, rssm, dreamer, latent-dynamics]
categories: world-models
giscus_comments: true
related_posts: false
featured: false

authors:
  - name: Md Rezwanul Haque
    url: "https://rezwan.xyz/"
    affiliations:
      name: CPAMI Lab, University of Waterloo

toc:
  - name: Where Part 0 left off
  - name: Why compress at all?
  - name: The variational autoencoder
  - name: From frames to sequences — the RSSM
  - name: The world-model objective
  - name: Learning in a dream
  - name: What actually made it work
  - name: Real systems running on these ideas
  - name: How to present this in ten minutes
  - name: Where this goes next
  - name: How to cite this post
  - name: References
---

<div class="wm-backlink">
  <a href="{{ '/blog/world-models/' | relative_url }}">&larr; Blogs · <strong>World Models</strong> series</a>
</div>

> **TL;DR.** A world model needs three things: a way to **compress** observations into a small state, a way to **predict** how that state evolves under actions, and a way to **use** those predictions. This part derives all three. We build the VAE and its ELBO from first principles, extend it across time into a **Recurrent State-Space Model (RSSM)**, and then show how **Dreamer** trains an actor–critic entirely on *imagined* trajectories — never touching the environment. We close with the systems that run on this today, and a slide-by-slide skeleton for presenting it.

---

## Where Part 0 left off

In [Part 0]({{ '/blog/2026/world-models-introduction/' | relative_url }}) we established the vocabulary: a world model learns $$p(z_{t+1} \mid z_t, a_t)$$ — the dynamics of an environment conditioned on actions — as opposed to a language model's $$p(x_t \mid x_{<t})$$. We sketched Ha &amp; Schmidhuber's **V–M–C** decomposition<sup class="wm-cite"><a href="#ref-3">3</a></sup> and said the magic was that a trained dynamics model lets you generate experience *in imagination*.

That was the *what*. This part is the *how*. Three questions drive everything below:

1. **Why compress?** Why not predict pixels directly?
2. **How do we learn the compression** when nobody hands us the latent variable?
3. **How do we turn a per-frame encoder into a simulator** you can roll forward, and then plan in?

Each has a clean answer, and each answer is a piece of machinery you will meet in every modern system.

---

## Why compress at all?

Take a modest $$64 \times 64$$ RGB frame. That is $$64 \times 64 \times 3 = 12{,}288$$ numbers per timestep. A one-minute episode at 20 Hz is roughly **15 million numbers**. Predicting the next frame directly means modelling a distribution over a 12,288-dimensional space — and most of those dimensions are things you do not care about: the exact texture of gravel, the flicker of a shadow, sensor noise.

<div class="wm-figure">
<svg viewBox="0 0 760 190" role="img" aria-label="Compressing a high-dimensional observation into a low-dimensional latent state" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;color:var(--global-text-color);">
  <defs>
    <marker id="p1Arrow" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="currentColor"></path>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.75">
    <g>
      <!-- pixel grid -->
      <rect x="30" y="35" width="120" height="120" rx="4" stroke-width="1.6"></rect>
      <path d="M50,35 V155 M70,35 V155 M90,35 V155 M110,35 V155 M130,35 V155
               M30,55 H150 M30,75 H150 M30,95 H150 M30,115 H150 M30,135 H150"></path>
    </g>
  </g>
  <text x="90" y="175" text-anchor="middle" font-size="12" fill="currentColor" opacity="0.85">observation oₜ — 12,288 dims</text>

  <line x1="165" y1="95" x2="255" y2="95" stroke="currentColor" stroke-width="1.6" marker-end="url(#p1Arrow)"></line>
  <text x="210" y="85" text-anchor="middle" font-size="12" fill="currentColor" opacity="0.85">encoder</text>

  <g fill="none" stroke="currentColor" stroke-width="1.6">
    <rect x="270" y="70" width="150" height="50" rx="8"></rect>
  </g>
  <text x="345" y="100" text-anchor="middle" font-size="13" fill="currentColor">latent state zₜ</text>
  <text x="345" y="140" text-anchor="middle" font-size="12" fill="currentColor" opacity="0.85">~32 dims</text>

  <line x1="435" y1="95" x2="520" y2="95" stroke="currentColor" stroke-width="1.6" marker-end="url(#p1Arrow)"></line>
  <text x="477" y="85" text-anchor="middle" font-size="12" fill="currentColor" opacity="0.85">dynamics</text>

  <g fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 4">
    <rect x="535" y="70" width="150" height="50" rx="8"></rect>
  </g>
  <text x="610" y="100" text-anchor="middle" font-size="13" fill="currentColor">predicted zₜ₊₁</text>
  <text x="610" y="140" text-anchor="middle" font-size="12" fill="currentColor" opacity="0.85">cheap to roll forward</text>
</svg>
<figcaption>Roughly a <strong>380×</strong> reduction. Prediction happens in the small space, not the big one — which is what makes rolling the model forward hundreds of steps affordable.</figcaption>
</div>

The bet of latent world models is that a compact $$z_t$$ retains everything **decision-relevant** and discards the rest. Two consequences follow immediately, and both matter in practice:

- **Compute.** Rolling forward 15 steps in a 32-dimensional space is trivial; doing it in pixel space is not. This is the difference between planning at control rates and not planning at all.
- **Generalisation.** A model forced through a narrow bottleneck cannot memorise textures; it has to encode *structure* — where things are, how they move.

The cost is that the latent is **unobserved**. Nobody labels $$z_t$$. We have to learn the encoder and the dynamics jointly, from observations alone. That is precisely the problem the VAE solves.

---

## The variational autoencoder

Assume the data is generated by a latent-variable model: draw a latent from a simple prior, then decode it.

$$
z \sim p(z) = \mathcal{N}(0, I), \qquad x \sim p_\theta(x \mid z).
$$

To train $$\theta$$ by maximum likelihood we would need the marginal

$$
p_\theta(x) = \int p_\theta(x \mid z)\, p(z)\, dz,
$$

which is intractable — it integrates over every possible latent. The variational trick<sup class="wm-cite"><a href="#ref-1">1</a>,<a href="#ref-2">2</a></sup> is to introduce an **inference network** $$q_\phi(z \mid x)$$ that guesses which latents could have produced $$x$$, and then bound the likelihood.

### Deriving the ELBO

Start from the log-likelihood and multiply inside by $$q_\phi(z\mid x)/q_\phi(z\mid x)$$:

$$
\log p_\theta(x) = \log \int q_\phi(z \mid x)\, \frac{p_\theta(x \mid z)\, p(z)}{q_\phi(z \mid x)}\, dz
= \log \mathbb{E}_{q_\phi(z \mid x)}\!\left[\frac{p_\theta(x \mid z)\, p(z)}{q_\phi(z \mid x)}\right].
$$

Since $$\log$$ is concave, Jensen's inequality moves it inside the expectation:

$$
\log p_\theta(x) \;\ge\; \mathbb{E}_{q_\phi(z \mid x)}\big[\log p_\theta(x \mid z)\big] \; - \; D_{\mathrm{KL}}\!\big(q_\phi(z \mid x)\,\|\,p(z)\big) \;=\; \mathcal{L}_{\text{ELBO}}(\theta,\phi).
$$

The gap between the two sides is exactly $$D_{\mathrm{KL}}(q_\phi(z\mid x) \,\|\, p_\theta(z \mid x))$$ — how wrong our guessed posterior is. Maximising the ELBO therefore does two jobs at once: it fits the data **and** tightens the inference network.

Read the two terms plainly:

- **Reconstruction** $$\mathbb{E}_q[\log p_\theta(x\mid z)]$$ — the latent must retain enough to rebuild the observation.
- **Regularisation** $$D_{\mathrm{KL}}(q_\phi \| p)$$ — the latent must stay close to a simple prior, so the space is smooth and samplable.

They pull against each other, and that tension *is* the representation.

<div class="wm-figure">
<svg viewBox="0 0 760 235" role="img" aria-label="Variational autoencoder with the two ELBO terms annotated" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;color:var(--global-text-color);">
  <defs>
    <marker id="p2Arrow" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="currentColor"></path>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="1.6">
    <rect x="20"  y="70" width="90"  height="55" rx="8"></rect>
    <rect x="160" y="70" width="110" height="55" rx="8"></rect>
    <rect x="470" y="70" width="110" height="55" rx="8"></rect>
    <rect x="630" y="70" width="90"  height="55" rx="8"></rect>
    <circle cx="375" cy="97" r="30"></circle>
  </g>
  <text x="65"  y="103" text-anchor="middle" font-size="13" fill="currentColor">x</text>
  <text x="215" y="92"  text-anchor="middle" font-size="12" fill="currentColor">encoder</text>
  <text x="215" y="110" text-anchor="middle" font-size="12" fill="currentColor">q(z | x)</text>
  <text x="375" y="102" text-anchor="middle" font-size="13" fill="currentColor">z</text>
  <text x="525" y="92"  text-anchor="middle" font-size="12" fill="currentColor">decoder</text>
  <text x="525" y="110" text-anchor="middle" font-size="12" fill="currentColor">p(x | z)</text>
  <text x="675" y="103" text-anchor="middle" font-size="13" fill="currentColor">x̂</text>

  <line x1="112" y1="97" x2="156" y2="97" stroke="currentColor" stroke-width="1.6" marker-end="url(#p2Arrow)"></line>
  <line x1="272" y1="97" x2="342" y2="97" stroke="currentColor" stroke-width="1.6" marker-end="url(#p2Arrow)"></line>
  <line x1="408" y1="97" x2="466" y2="97" stroke="currentColor" stroke-width="1.6" marker-end="url(#p2Arrow)"></line>
  <line x1="582" y1="97" x2="626" y2="97" stroke="currentColor" stroke-width="1.6" marker-end="url(#p2Arrow)"></line>

  <text x="307" y="86" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.8">μ, σ</text>

  <!-- KL pull -->
  <g fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 4" opacity="0.8">
    <path d="M375,60 V32" marker-end="url(#p2Arrow)"></path>
  </g>
  <text x="375" y="24" text-anchor="middle" font-size="11.5" fill="currentColor" opacity="0.85">KL( q ‖ N(0, I) )  —  keep the latent space smooth</text>

  <!-- reconstruction span -->
  <g fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 4" opacity="0.8">
    <path d="M65,131 V172 H675 V131"></path>
  </g>
  <text x="370" y="190" text-anchor="middle" font-size="11.5" fill="currentColor" opacity="0.85">E[ log p(x | z) ]  —  keep enough to rebuild x</text>
  <text x="370" y="214" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.7">reparameterise:  z = μ(x) + σ(x) ⊙ ε   —   so gradients flow through the sample</text>
</svg>
<figcaption>The VAE in one picture. The two dashed annotations are precisely the two ELBO terms — one pulling the latent toward fidelity, the other toward a well-behaved prior.</figcaption>
</div>

### The reparameterisation trick

One obstacle remains: we must backpropagate through a *sample* $$z \sim q_\phi(z\mid x)$$, and sampling is not differentiable. The fix<sup class="wm-cite"><a href="#ref-1">1</a></sup> is to push the randomness into a parameter-free variable:

$$
z = \mu_\phi(x) + \sigma_\phi(x) \odot \varepsilon, \qquad \varepsilon \sim \mathcal{N}(0, I).
$$

Now $$z$$ is a deterministic, differentiable function of $$\phi$$ and an external noise draw. Gradients flow to $$\mu_\phi$$ and $$\sigma_\phi$$ cleanly. This single line is what made deep latent-variable models trainable at scale, and it is used unchanged inside every model below.

---

## From frames to sequences — the RSSM

A VAE encodes *one frame*. A world model must answer: **given this state and this action, what is the next state?** The dominant answer is the **Recurrent State-Space Model** introduced with PlaNet<sup class="wm-cite"><a href="#ref-4">4</a></sup> and carried through the whole Dreamer line<sup class="wm-cite"><a href="#ref-5">5</a>,<a href="#ref-6">6</a>,<a href="#ref-7">7</a></sup>.

Its key design decision is to **split the state in two**:

$$
s_t = (h_t,\; z_t)
$$

- $$h_t$$ — a **deterministic** recurrent state, carried by a GRU. It never forgets, and gives the model a stable memory backbone.
- $$z_t$$ — a **stochastic** state, which captures what genuinely could not be predicted (a dice roll, an unseen corridor).

Why both? A purely deterministic model cannot represent uncertainty, so it blurs multiple futures into an average. A purely stochastic model tends to lose long-range information across sampling steps. Splitting gets memory *and* uncertainty. The four learned components are:

$$
\begin{aligned}
\text{recurrence:} &\quad h_t = f_\theta(h_{t-1},\, z_{t-1},\, a_{t-1}) \\[2pt]
\text{prior (transition):} &\quad \hat{z}_t \sim p_\theta(\hat{z}_t \mid h_t) \\[2pt]
\text{posterior (representation):} &\quad z_t \sim q_\phi(z_t \mid h_t,\, o_t) \\[2pt]
\text{heads:} &\quad \hat{o}_t \sim p_\theta(o_t \mid h_t, z_t), \quad \hat{r}_t \sim p_\theta(r_t \mid h_t, z_t)
\end{aligned}
$$

The distinction between **prior** and **posterior** is the entire trick, and it is worth stating slowly:

- The **posterior** $$q_\phi(z_t \mid h_t, o_t)$$ *has seen* the observation. It is the accurate state.
- The **prior** $$p_\theta(\hat z_t \mid h_t)$$ has **not**. It must guess the state from memory and action alone.

Training pushes the prior toward the posterior. Once they agree, you can **drop the observation entirely and run on the prior** — and that is a simulator.

<div class="wm-figure">
<svg viewBox="0 0 760 275" role="img" aria-label="Recurrent State-Space Model unrolled over three timesteps" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;color:var(--global-text-color);">
  <defs>
    <marker id="p3Arrow" markerWidth="8" markerHeight="8" refX="6.5" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="currentColor"></path>
    </marker>
  </defs>

  <!-- deterministic backbone -->
  <g fill="none" stroke="currentColor" stroke-width="1.7">
    <rect x="90"  y="105" width="70" height="42" rx="8"></rect>
    <rect x="320" y="105" width="70" height="42" rx="8"></rect>
    <rect x="550" y="105" width="70" height="42" rx="8"></rect>
  </g>
  <text x="125" y="131" text-anchor="middle" font-size="13" fill="currentColor">hₜ₋₁</text>
  <text x="355" y="131" text-anchor="middle" font-size="13" fill="currentColor">hₜ</text>
  <text x="585" y="131" text-anchor="middle" font-size="13" fill="currentColor">hₜ₊₁</text>
  <line x1="162" y1="126" x2="316" y2="126" stroke="currentColor" stroke-width="1.7" marker-end="url(#p3Arrow)"></line>
  <line x1="392" y1="126" x2="546" y2="126" stroke="currentColor" stroke-width="1.7" marker-end="url(#p3Arrow)"></line>
  <text x="239" y="118" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.8">GRU · aₜ₋₁</text>
  <text x="469" y="118" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.8">GRU · aₜ</text>

  <!-- stochastic states -->
  <g fill="none" stroke="currentColor" stroke-width="1.7">
    <circle cx="125" cy="205" r="24"></circle>
    <circle cx="355" cy="205" r="24"></circle>
    <circle cx="585" cy="205" r="24"></circle>
  </g>
  <text x="125" y="210" text-anchor="middle" font-size="12.5" fill="currentColor">zₜ₋₁</text>
  <text x="355" y="210" text-anchor="middle" font-size="12.5" fill="currentColor">zₜ</text>
  <text x="585" y="210" text-anchor="middle" font-size="12.5" fill="currentColor">zₜ₊₁</text>
  <line x1="125" y1="151" x2="125" y2="177" stroke="currentColor" stroke-width="1.5" marker-end="url(#p3Arrow)"></line>
  <line x1="355" y1="151" x2="355" y2="177" stroke="currentColor" stroke-width="1.5" marker-end="url(#p3Arrow)"></line>
  <line x1="585" y1="151" x2="585" y2="177" stroke="currentColor" stroke-width="1.5" marker-end="url(#p3Arrow)"></line>

  <!-- observations feeding the posterior -->
  <g fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.85">
    <rect x="95"  y="248" width="60" height="22" rx="5"></rect>
    <rect x="325" y="248" width="60" height="22" rx="5"></rect>
    <rect x="555" y="248" width="60" height="22" rx="5"></rect>
    <path d="M125,246 V233"></path>
    <path d="M355,246 V233"></path>
    <path d="M585,246 V233"></path>
  </g>
  <text x="125" y="264" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.85">oₜ₋₁</text>
  <text x="355" y="264" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.85">oₜ</text>
  <text x="585" y="264" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.85">oₜ₊₁</text>

  <!-- legend -->
  <g fill="none" stroke="currentColor" stroke-width="1.5">
    <rect x="640" y="28" width="20" height="13" rx="3"></rect>
    <circle cx="650" cy="58" r="8"></circle>
  </g>
  <text x="670" y="39" font-size="11" fill="currentColor" opacity="0.85">deterministic (memory)</text>
  <text x="670" y="62" font-size="11" fill="currentColor" opacity="0.85">stochastic (uncertainty)</text>

  <text x="60" y="35" font-size="12" fill="currentColor" opacity="0.9">posterior uses oₜ  ·  prior must guess without it</text>
  <text x="60" y="55" font-size="11" fill="currentColor" opacity="0.7">KL(posterior ‖ prior) is what teaches the model to simulate</text>
</svg>
<figcaption>The RSSM unrolled. Solid path = memory that always flows; dashed boxes = observations, which are available during <em>training</em> but deliberately withheld when the model is used as a simulator.</figcaption>
</div>

---

## The world-model objective

Everything above collapses into one loss — a sequential ELBO. Over a sampled trajectory,

$$
\mathcal{L}(\theta,\phi) = \mathbb{E}_{q_\phi}\left[\sum_{t}\underbrace{-\log p_\theta(o_t \mid h_t, z_t)}_{\text{reconstruct observation}} \underbrace{-\log p_\theta(r_t \mid h_t, z_t)}_{\text{predict reward}} + \; \beta\underbrace{D_{\mathrm{KL}}\big(q_\phi(z_t \mid h_t, o_t)\,\big\|\,p_\theta(z_t \mid h_t)\big)}_{\text{make the prior match the posterior}}\right]
$$

Three terms, three jobs:

1. **Reconstruction** forces the latent to carry the scene.
2. **Reward prediction** forces it to carry what matters *for the task* — the single line that turns a generic video model into a control model.
3. **KL** is the simulator term. It penalises the gap between "state given the picture" and "state predicted from memory + action". Drive it down and the model can dream.

That third term deserves emphasis, because it is the one people skim: **the KL is not merely regularisation here** — it is the training signal that makes open-loop rollout possible at all.

---

## Learning in a dream

Now the payoff. With a trained RSSM you can generate trajectories without the environment: start from a real encoded state, then repeatedly sample the **prior** and feed back your own predictions.

Dreamer<sup class="wm-cite"><a href="#ref-5">5</a></sup> trains an actor and a critic purely on these imagined rollouts, typically ~15 steps deep:

$$
\pi_\psi(a_t \mid s_t) \quad\text{(actor)}, \qquad v_\xi(s_t) \approx \mathbb{E}\Big[\textstyle\sum_{k\ge t} \gamma^{\,k-t} r_k\Big] \quad\text{(critic)}
$$

Returns use a $$\lambda$$-weighted mixture<sup class="wm-cite"><a href="#ref-8">8</a>,<a href="#ref-15">15</a></sup> that trades bias against variance:

$$
V^\lambda_t = r_t + \gamma\Big[(1-\lambda)\, v_\xi(s_{t+1}) + \lambda\, V^\lambda_{t+1}\Big]
$$

The critic regresses onto $$V^\lambda_t$$; the actor maximises it. Crucially, because the whole rollout is differentiable, the actor can get gradients **straight through the learned dynamics** — a luxury no model-free method has.

<div class="wm-figure">
<svg viewBox="0 0 760 250" role="img" aria-label="Imagined rollouts branching from a real encoded state" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;color:var(--global-text-color);">
  <defs>
    <marker id="p4Arrow" markerWidth="8" markerHeight="8" refX="6.5" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 Z" fill="currentColor"></path>
    </marker>
  </defs>

  <!-- real segment -->
  <g fill="none" stroke="currentColor" stroke-width="1.9">
    <circle cx="70"  cy="125" r="13"></circle>
    <circle cx="150" cy="125" r="13"></circle>
    <circle cx="230" cy="125" r="13"></circle>
    <path d="M84,125 H136" marker-end="url(#p4Arrow)"></path>
    <path d="M164,125 H216" marker-end="url(#p4Arrow)"></path>
  </g>
  <text x="150" y="95" text-anchor="middle" font-size="12" fill="currentColor" opacity="0.9">real experience (posterior, uses oₜ)</text>
  <text x="150" y="165" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.7">replayed from the buffer</text>

  <!-- branch point -->
  <text x="230" y="98" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.85">start state</text>

  <!-- imagined branches -->
  <g fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.9">
    <path d="M244,120 C300,80 340,66 400,60"  marker-end="url(#p4Arrow)"></path>
    <path d="M244,125 C300,125 340,125 400,125" marker-end="url(#p4Arrow)"></path>
    <path d="M244,131 C300,170 340,186 400,192" marker-end="url(#p4Arrow)"></path>
    <path d="M414,60  H520" marker-end="url(#p4Arrow)"></path>
    <path d="M414,125 H520" marker-end="url(#p4Arrow)"></path>
    <path d="M414,192 H520" marker-end="url(#p4Arrow)"></path>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.6">
    <circle cx="407" cy="60"  r="9"></circle>
    <circle cx="407" cy="125" r="9"></circle>
    <circle cx="407" cy="192" r="9"></circle>
  </g>

  <!-- value readout -->
  <g fill="none" stroke="currentColor" stroke-width="1.6">
    <rect x="527" y="44"  width="105" height="32" rx="7"></rect>
    <rect x="527" y="109" width="105" height="32" rx="7"></rect>
    <rect x="527" y="176" width="105" height="32" rx="7"></rect>
  </g>
  <text x="579" y="65"  text-anchor="middle" font-size="11.5" fill="currentColor">Vλ = 8.2</text>
  <text x="579" y="130" text-anchor="middle" font-size="11.5" fill="currentColor">Vλ = 3.1</text>
  <text x="579" y="197" text-anchor="middle" font-size="11.5" fill="currentColor">Vλ = −1.4</text>

  <text x="420" y="30" text-anchor="middle" font-size="12" fill="currentColor" opacity="0.9">imagined futures (prior only — no environment)</text>

  <g fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="3 3" opacity="0.75">
    <path d="M645,60 C700,60 700,125 660,125" marker-end="url(#p4Arrow)"></path>
  </g>
  <text x="700" y="160" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.85">actor is pushed</text>
  <text x="700" y="176" text-anchor="middle" font-size="11" fill="currentColor" opacity="0.85">toward high Vλ</text>
</svg>
<figcaption>Training happens here. Each dashed branch costs a few matrix multiplies — no simulator step, no robot, no risk. The actor is updated by gradients flowing back <em>through</em> the learned dynamics.</figcaption>
</div>

The practical consequence is stark: Dreamer-style agents are often **one to two orders of magnitude more sample-efficient** than model-free baselines on pixel control, because most of their learning happens in a dream rather than in the world.

---

## What actually made it work

The idea above dates to 2018–2019. What turned it from a promising result into a robust one was a set of unglamorous fixes in **DreamerV3**<sup class="wm-cite"><a href="#ref-7">7</a></sup> — worth knowing, because they are the difference between a demo and a system:

- **Symlog prediction.** Rewards and observations span wildly different scales across tasks. Predicting $$\operatorname{symlog}(x) = \operatorname{sign}(x)\log(|x|+1)$$ compresses the range so one hyperparameter set survives everywhere.
- **Two-hot encoded returns.** Regressing a scalar return is fragile; predicting a *distribution* over a fixed set of bins, with mass split between the two nearest, is far more stable.
- **KL balancing.** The prior and posterior are pulled together at different rates, so the posterior is not dragged toward a still-ignorant prior early in training.
- **Free bits.** The KL term is clipped below ~1 nat, preventing posterior collapse (where the model ignores the latent entirely).
- **Return normalisation** by a percentile range, so sparse-reward and dense-reward tasks can share settings.

The headline result: **one fixed configuration** across more than 150 tasks, and the first agent to **collect diamonds in Minecraft from scratch, with no human data and no curriculum**<sup class="wm-cite"><a href="#ref-7">7</a></sup>. If you present one empirical fact about world models, that is a strong candidate — it is concrete, verifiable, and instantly legible to a non-specialist.

---

## Real systems running on these ideas

The machinery above is not academic. Here is where it shows up, with what each system actually demonstrates:

<div class="wm-systems">
  <div class="wm-sys">
    <span class="wm-sys-name">DreamerV3</span>
    <span class="wm-sys-what">The RSSM + imagination recipe, hardened. One hyperparameter set, 150+ tasks, diamonds in Minecraft from scratch.</span>
    <span class="wm-sys-take">Take-away: latent imagination is now a <em>general</em> method, not a per-task craft.<sup class="wm-cite"><a href="#ref-7">7</a></sup></span>
  </div>
  <div class="wm-sys">
    <span class="wm-sys-name">Genie</span>
    <span class="wm-sys-what">An 11B-parameter model trained on unlabelled internet gameplay video. It infers a <em>latent action space</em> with no action labels, then turns a single image — even a sketch — into a playable world.</span>
    <span class="wm-sys-take">Take-away: actions can be discovered, not supplied. This is the bridge from passive video to interactive simulation.<sup class="wm-cite"><a href="#ref-11">11</a></sup></span>
  </div>
  <div class="wm-sys">
    <span class="wm-sys-name">Sora</span>
    <span class="wm-sys-what">Positioned explicitly as a step toward "world simulators": long-horizon video with emergent 3D consistency and object permanence — alongside well-documented physics failures.</span>
    <span class="wm-sys-take">Take-away: scale buys visual coherence, but <em>coherence is not physics</em>. A useful cautionary example.<sup class="wm-cite"><a href="#ref-12">12</a></sup></span>
  </div>
  <div class="wm-sys">
    <span class="wm-sys-name">GameNGen</span>
    <span class="wm-sys-what">A diffusion model that runs DOOM interactively at ~20 FPS on a single TPU; human raters distinguishing short clips from the real engine perform barely above chance.</span>
    <span class="wm-sys-take">Take-away: a neural network can <em>be</em> the game engine — real-time, interactive, learned.<sup class="wm-cite"><a href="#ref-13">13</a></sup></span>
  </div>
  <div class="wm-sys">
    <span class="wm-sys-name">GAIA-1</span>
    <span class="wm-sys-what">A ~9B generative driving world model that produces plausible future driving video conditioned on past video, text, and actions.</span>
    <span class="wm-sys-take">Take-away: the safety case — generate rare, dangerous scenarios instead of waiting to encounter them.<sup class="wm-cite"><a href="#ref-14">14</a></sup></span>
  </div>
  <div class="wm-sys">
    <span class="wm-sys-name">The JEPA line</span>
    <span class="wm-sys-what">Predicts in <em>representation</em> space rather than pixel space, deliberately refusing to model unpredictable detail.</span>
    <span class="wm-sys-take">Take-away: the main live alternative to reconstruction — and the subject of Part 2.<sup class="wm-cite"><a href="#ref-9">9</a>,<a href="#ref-10">10</a></sup></span>
  </div>
</div>

Notice the split running through this list. DreamerV3 and GAIA-1 **reconstruct**; Genie and GameNGen **generate interactively**; JEPA **refuses to reconstruct at all**. That disagreement — *what should a world model actually predict?* — is the live research question, and it is exactly where Part 2 picks up.

---

## How to present this in ten minutes

Since a stated goal here is to be able to explain this from memory, here is a skeleton that has worked for me. Five slides, one idea each.

1. **The gap.** "A language model predicts what a person would *write* next. A world model predicts what the *world* will do next — given what you do." One sentence, one table (from Part 0). No maths.
2. **The compression.** Show Figure 1. "12,288 numbers become 32. We predict in the small space." The 380× number does the persuading.
3. **The two-part state.** Show Figure 3. "Memory that never forgets, plus a random part for what genuinely can't be predicted." Then the one line that matters: *the posterior sees the picture; the prior has to guess. Train them to agree, and you can throw the picture away.*
4. **The dream.** Show Figure 4. "Now training costs matrix multiplies instead of robot hours." Land it with DreamerV3's diamonds.
5. **The open question.** "Reconstruct pixels, generate interactively, or predict representations?" Name Sora's physics failures against Genie's playability. Finish on the unresolved question — audiences remember tension, not summaries.

Two things to keep in reserve for questions: **why the KL term is the simulator term** (§ the objective), and **why the reward head is what separates a world model from a video model**. Those are the two points specialists probe first.

---

## Where this goes next

**Part 2 — Predicting representations: JEPA, energy-based learning, and the case against pixels.** Why LeCun argues reconstruction is the wrong objective<sup class="wm-cite"><a href="#ref-9">9</a></sup>, how joint-embedding predictive architectures avoid representation collapse<sup class="wm-cite"><a href="#ref-10">10</a></sup>, and what the evidence actually shows when you stop asking a model to draw every pixel.

After that: generative interactive worlds (Genie / Sora / GameNGen) in depth, then evaluation — which, as the [reading &amp; resources hub]({{ '/blog/2026/world-models-reading-and-resources/' | relative_url }}) argues, is where the field is currently rethinking itself hardest.

Comments are open below — corrections and pointers to papers I should cover are very welcome.

---

## How to cite this post

If this is useful for your own work, please cite the **primary sources** in the [References](#references). To reference this post itself:

```bibtex
@misc{haque2026worldmodels1,
  author       = {Md Rezwanul Haque},
  title        = {World Models --- Part 1: Inside the Latent (VAEs, RSSM, and Learning in a Dream)},
  year         = {2026},
  howpublished = {\url{https://rezwan.xyz/blog/2026/world-models-latent-dynamics/}}
}
```

---

## References

<ol class="wm-refs">
  <li id="ref-1">D. P. Kingma and M. Welling. <em>Auto-Encoding Variational Bayes.</em> ICLR, 2014. <a href="https://arxiv.org/abs/1312.6114" target="_blank" rel="noopener">arXiv:1312.6114</a></li>
  <li id="ref-2">D. J. Rezende, S. Mohamed, and D. Wierstra. <em>Stochastic Backpropagation and Approximate Inference in Deep Generative Models.</em> ICML, 2014. <a href="https://arxiv.org/abs/1401.4082" target="_blank" rel="noopener">arXiv:1401.4082</a></li>
  <li id="ref-3">D. Ha and J. Schmidhuber. <em>World Models / Recurrent World Models Facilitate Policy Evolution.</em> NeurIPS, 2018. <a href="https://arxiv.org/abs/1803.10122" target="_blank" rel="noopener">arXiv:1803.10122</a></li>
  <li id="ref-4">D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson. <em>Learning Latent Dynamics for Planning from Pixels (PlaNet).</em> ICML, 2019. <a href="https://arxiv.org/abs/1811.04551" target="_blank" rel="noopener">arXiv:1811.04551</a></li>
  <li id="ref-5">D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi. <em>Dream to Control: Learning Behaviors by Latent Imagination.</em> ICLR, 2020. <a href="https://arxiv.org/abs/1912.01603" target="_blank" rel="noopener">arXiv:1912.01603</a></li>
  <li id="ref-6">D. Hafner, T. Lillicrap, M. Norouzi, and J. Ba. <em>Mastering Atari with Discrete World Models (DreamerV2).</em> ICLR, 2021. <a href="https://arxiv.org/abs/2010.02193" target="_blank" rel="noopener">arXiv:2010.02193</a></li>
  <li id="ref-7">D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap. <em>Mastering Diverse Domains through World Models (DreamerV3).</em> 2023. <a href="https://arxiv.org/abs/2301.04104" target="_blank" rel="noopener">arXiv:2301.04104</a></li>
  <li id="ref-8">J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel. <em>High-Dimensional Continuous Control Using Generalized Advantage Estimation.</em> ICLR, 2016. <a href="https://arxiv.org/abs/1506.02438" target="_blank" rel="noopener">arXiv:1506.02438</a></li>
  <li id="ref-9">Y. LeCun. <em>A Path Towards Autonomous Machine Intelligence.</em> OpenReview, 2022. <a href="https://openreview.net/forum?id=BZ5a1r-kVsf" target="_blank" rel="noopener">openreview.net</a></li>
  <li id="ref-10">M. Assran, Q. Duval, I. Misra, P. Bojanowski, P. Vincent, M. Rabbat, Y. LeCun, and N. Ballas. <em>Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (I-JEPA).</em> CVPR, 2023. <a href="https://arxiv.org/abs/2301.08243" target="_blank" rel="noopener">arXiv:2301.08243</a></li>
  <li id="ref-11">J. Bruce, M. Dennis, A. Edwards, J. Parker-Holder, et al. <em>Genie: Generative Interactive Environments.</em> ICML, 2024. <a href="https://arxiv.org/abs/2402.15391" target="_blank" rel="noopener">arXiv:2402.15391</a></li>
  <li id="ref-12">T. Brooks, B. Peebles, et al. <em>Video Generation Models as World Simulators (Sora).</em> OpenAI technical report, 2024. <a href="https://openai.com/index/video-generation-models-as-world-simulators/" target="_blank" rel="noopener">openai.com</a></li>
  <li id="ref-13">D. Valevski, Y. Leviathan, M. Arar, and S. Fruchter. <em>Diffusion Models Are Real-Time Game Engines (GameNGen).</em> 2024. <a href="https://arxiv.org/abs/2408.14837" target="_blank" rel="noopener">arXiv:2408.14837</a></li>
  <li id="ref-14">A. Hu, L. Russell, H. Yeo, Z. Murez, G. Fedoseev, A. Kendall, J. Shotton, and G. Corrado. <em>GAIA-1: A Generative World Model for Autonomous Driving.</em> Wayve, 2023. <a href="https://arxiv.org/abs/2309.17080" target="_blank" rel="noopener">arXiv:2309.17080</a></li>
  <li id="ref-15">R. S. Sutton and A. G. Barto. <em>Reinforcement Learning: An Introduction</em> (2nd ed.). MIT Press, 2018.</li>
</ol>

<div class="wm-backlink wm-backlink-bottom">
  <a href="{{ '/blog/world-models/' | relative_url }}">&larr; Back to the <strong>World Models</strong> series</a>
</div>

<style>
.wm-backlink { margin: 0 0 1.2rem; font-size: 0.92rem; }
.wm-backlink-bottom { margin: 2rem 0 0; }
.wm-backlink a { color: var(--global-theme-color); text-decoration: none; }
.wm-backlink a:hover { text-decoration: underline; }
.wm-cite a { color: var(--global-theme-color); font-weight: 600; text-decoration: none; }
.wm-cite a:hover { text-decoration: underline; }
.wm-refs { font-size: 0.9rem; line-height: 1.55; padding-left: 1.4rem; }
.wm-refs li { margin-bottom: 0.5rem; scroll-margin-top: 80px; }
.wm-figure { margin: 1.8rem 0; }
.wm-figure figcaption {
  margin-top: 0.6rem; font-size: 0.88rem; opacity: 0.8;
  text-align: center; color: var(--global-text-color);
}
.wm-systems { display: flex; flex-direction: column; gap: 0.8rem; margin: 1.4rem 0; }
.wm-sys {
  display: flex; flex-direction: column; gap: 0.3rem;
  border-left: 3px solid var(--global-theme-color);
  padding: 0.7rem 0 0.7rem 1rem;
}
.wm-sys-name { font-weight: 700; font-size: 1.02rem; }
.wm-sys-what { font-size: 0.95rem; line-height: 1.65; }
.wm-sys-take { font-size: 0.9rem; opacity: 0.82; line-height: 1.6; }
</style>
