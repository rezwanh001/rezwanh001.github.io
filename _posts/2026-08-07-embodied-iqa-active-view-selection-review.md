---
layout: post
title: "Embodied IQA & Active View Selection — Deep Paper Review"
description: "A full deep review of three papers (Embodied-IQA, EPD/MA-EIQA, Active View Selector): per-paper task/dataset/method/evaluation, cross-paper synthesis, a new-metric opportunity analysis, gaps and future directions, and a 2024–2026 related-work map."
date: 2026-08-07
tags: [world-models, embodied-ai, active-perception, iqa, resources, deep-dives]
categories: world-models
wm_resource: true
giscus_comments: true
related_posts: false
---

<div class="wm-backlink">
  <a href="{{ '/blog/world-models/' | relative_url }}">&larr; Blogs · <strong>World Models</strong> series</a>
</div>

{% raw %}
**Papers covered**

| # | Title | Venue / arXiv | Code / Page |
|---|---|---|---|
| 1 | Image Quality Assessment for Embodied AI | arXiv:2505.16815v2 (14 Oct 2025), preprint under review | https://github.com/lcysyzxdxc/EmbodiedIQA |
| 2 | Embodied Image Quality Assessment for Robotic Intelligence | arXiv:2412.18774v3 (18 Aug 2025), IEEE-style (TCSVT-track) | https://github.com/Jianbo-maker/EPD_benchmark |
| 3 | Active View Selector: Fast and Accurate Active View Selection with Cross Reference IQA | arXiv:2506.19844v1 (24 Jun 2025) | https://avs.active.vision/ |

**Groups.** Papers 1 and 2 come from the *same lab lineage* (SJTU Institute of Image Communication — Chunyi Li, Jianbo Zhang, Guangtao Zhai; Weisi Lin at NTU). Paper 2 (EPD) is the earlier, smaller work and is literally cited as reference [15] inside Paper 1. Paper 3 is from Oxford's Active Vision Lab + VGG (Zirui Wang, Yash Bhalgat, Ruining Li, Victor Prisacariu) and is a direct follow-up to their own CrossScore (ECCV 2024).

**How to read this doc.** Sections 1–3 are per-paper deep dives (Task / Dataset / Methods / Evaluation). Section 4 synthesises the three. Section 5 is the *new metric* opportunity analysis. Section 6 is gaps & future directions. Section 7 is recent related work (2024–2026). Section 8 holds appendices and flagged discrepancies. Section 9 is the append log — add new queries and follow-up analysis there so the per-paper sections stay clean.

---

## 0. One-paragraph summary of the three together

Papers 1 and 2 attack the same question from the *measurement* side: **existing IQA metrics score images for humans, but robots are the ones consuming the pixels, and robot preferences do not match human preferences.** Paper 2 (EPD) is the first small proof of this with an RL agent in simulation; Paper 1 (Embodied-IQA) is the large-scale, theoretically framed successor that decomposes robot "perception quality" into Cognition (VLM), Decision (VLA), and Execution (real robot arm). Paper 3 attacks a different question from the *use* side: **if you already have a good no-ground-truth quality score, you can use it to decide where a robot should look next**, replacing expensive 3D uncertainty/information-gain machinery with a cheap 2D cross-reference IQA forward pass. Together they define a loop that nobody has closed yet: a *task-conditioned, reference-free quality signal* that is both (a) predictive of downstream embodied success and (b) cheap enough to drive online action selection. That un-closed loop is where the new-metric opportunity lives (§5).

---

## 1. Paper 1 — Image Quality Assessment for Embodied AI (Embodied-IQA)

### 1.1 Task — what problem did they actually address?

**Problem.** Embodied AI works in the lab but fails in the wild because real-world images are distorted (defocus, shake, compression, lighting). There is no IQA metric that tells you *whether a given distorted image is still usable by a robot for a given task*. Traditional IQA predicts human preference; that is the wrong target.

**Core claim — three visual systems, not two.** They separate:
- **HVS** (Human Visual System) — sensitive to noise, compression, aesthetics.
- **MVS** (Machine Visual System) — a general machine; quality = performance of detection/segmentation, i.e. **Cognition only**.
- **RVS** (Robot Visual System) — has **Decision** and **Execution** *after* Cognition. High fidelity at one step does not guarantee the next.

**Theoretical framing (Mertonian vs Newtonian systems).** Borrowed from Fei-Yue Wang's "Newton, Merton and analytics intelligence". Newtonian systems are deterministic and predictable; Mertonian systems involve feedback between belief and action so the next state cannot be solved for exactly. HVS and MVS are treated as Newtonian (after you decide, execution is reliable). RVS is Mertonian — a one-character difference in the VLM caption can flip the VLA pose; a 1 cm path offset can cause a collision. **Therefore the three steps must be scored separately.** This is the paper's main conceptual contribution.

**Objective.** Define the topic "IQA for Embodied AI": build a Perception → Cognition → Decision → Execution pipeline, collect a database of robot subjective preferences over distorted images, and show that current IQA metrics cannot predict them.

### 1.2 Dataset — Embodied-IQA

| Property | Value |
|---|---|
| Reference images | 1,230 high-quality samples |
| Distorted images | 36,900 (30 distortion types × 5 intensity levels, randomly sampled per reference) |
| Resolution | ~1k |
| Perception tasks | 6,150 (5 natural-language tasks per reference image, increasing difficulty) |
| Cognition annotations | 2,767,500 labels (15 VLMs) |
| Decision annotations | 2,767,500 labels (15 VLAs) |
| Execution annotations | 1,500 labels (real UR5 robot) |
| **Total annotations** | **5.53 M**, across **3+3+1 = 7 score dimensions** |
| Train / val split | 29,520 / 7,380 pairs (8:2), repeated 10× and averaged |

**How the references were collected.** 1,230 samples drawn from **seven robotics databases**: DROID, QT-Opt, self-supervised visuo-tactile (Kerr et al.), Jacquard, CLIP-based referring grasp synthesis, ManiSkill2, and Latent Plans (Rosete-Beas et al.). Pre-filtered with **Q-Align** to remove pre-existing distortion. Stratified along four axes to guarantee coverage:
- **Sim2Real**: real / simulation
- **Perspective**: first-person (wrist) / third-person (top, side)
- **Main object** (5 classes): mechanical, daily, electronic, tools, other
- **Background** (5 classes): home, industrial, software, lab, other

**Distortions.** 30 types in 7 categories — Blur, Luminance, Chrominance, Noise, Compression, Spatial, Others — each at 5 levels **calibrated so that HVS-perceived degradation is aligned across types at the same level** (this is what later lets them show that RVS sensitivity does *not* follow HVS levels). Distribution roughly: Spatial 23%, Noise 20%, Luminance 13%, Blur 10%, Chrominance 17%, Compression 10%, Others 7%.

**Task annotation (the human-in-the-loop part).** Five PhD candidates form a panel; each image goes to all five in random order; each writes a task, seeing previous ones, and must make it *harder* and test a *different* ability than the previous. Verbs restricted to `[Cover, Insert, Move, Pick, Place, Pour, Press, Pull, Push, Twist]`. A professional robotics engineer then re-ranks difficulty and fixes unreasonable tasks. NSFW / broken images removed.

**Cognition labels (VLM).** 15 VLMs, all <8B for real-time inference: Mini-InternVL, InternLM-XComposer2 / 2.5, InternVL2 / 2.5 / 3, mPLUG-Owl3, Ovis1.5-Gemma, Ovis1.6-Llama, Ovis2, Phi3-Vision, Phi3.5-Vision, Phi4-Multimodal, Qwen2-VL, Qwen2.5-VL. Each solves the task in ~10 words on the reference and on the distorted image. Score = difference between the two output sentences on **three dimensions**: **precision (BLEU), recall (ROUGE), semantics (CIDEr)**, weighted 1 : 1 : 0.1 (because CIDEr maxes at 10), summed over the 5 tasks.

**Decision labels (VLA).** 15 VLAs, ~8B: CogACT, Embodied-CoT, Octo, OpenVLA (+ Libero / Goal / Libero-Object / Libero-Spatial variants), π0 (Aloha-Pen / Aloha-Towel / Aloha-Tupperware / Base / Droid / Fast), RT-X-1. The **7-DoF pose** output is parsed into **three dimensions**:
- **Position** (3, mm) → spatial Euclidean distance between reference and distorted coordinate points
- **Rotation** (3, rad) → cosine similarity of direction vectors
- **State** (1, gripper open/close ∈ [0,1]) → absolute difference

0–1 normalised, averaged, summed over 5 tasks. Depth and anything beyond 7-DoF is discarded for cross-VLA alignment; for two-arm VLAs only the arm with the larger movement range is used.

**Execution labels (real world).** UR5 arm + Robotiq 2F-140 gripper, 85 cm working radius; Intel RealSense D455 array for first-person (wrist) and third-person (top, side). Scoring rule:
1. **Success** → 100.
2. **Failure** → Euclidean distance between reference-result and distorted-result final pose, points deducted per centimetre.
3. **Emergency stop** (hits table/wall) → 0.

Only the **easiest of the 5 tasks** is executed, so that the reference image always succeeds and any failure is attributable to the distortion. 1,500 executions total.

### 1.3 Methods — what did they propose?

This is a **database + benchmark paper, not a new-model paper**. There is no new IQA architecture. What is "proposed" is:

1. The **Perception–Cognition–Decision–Execution pipeline** as the definition of embodied perceptual quality.
2. The **7-dimension scoring scheme** (Precision/Recall/Semantic for Cognition; Position/Rotation/State for Decision; Euclidean-distance-with-penalty for Execution).
3. A **JND-based distortion-sensitivity partition for machines** — mild / medium / severe, each one-third of samples by Cognition/Decision score, replacing HVS-calibrated intensity levels.
4. A protocol for benchmarking existing IQA metrics against robot preference.

### 1.4 Evaluation

**Metrics evaluated (15):**
- *Zero-shot (5)*: PSNR, SSIM, BRISQUE, Q-Align, Q-Align+ (aesthetic weights)
- *Full-Reference, fine-tuned (5)*: AHIQ, CKDN, DISTS, LPIPS, TOPIQ-FR
- *No-Reference, fine-tuned (5)*: CLIPIQA, CNNIQA, DBCNN, QualiCLIP, TOPIQ-NR

**Correlation measures:** SRCC and KRCC (monotonicity), PLCC (accuracy). LR 1e-5, 50 epochs, `pyiqa` defaults, 10 repeats averaged. Annotation compute: 2 servers × 16 A800 80GB.

**Evaluation slices:** 3 scoring dimensions × {3 JND sensitivity bands, first/third person, real/sim, 5 distortion levels}. Main tables report Decision (VLA); Cognition (VLM) is in the supplementary.

**Headline results (Decision / VLA, main table):**

| Group | Best metric | Position SRCC | Rotation SRCC | State SRCC |
|---|---|---|---|---|
| Zero-shot | Q-Align | 0.5325 | 0.5387 | 0.3791 |
| FR | TOPIQ-FR | **0.7748** | 0.6428 | 0.6684 |
| FR (2nd) | AHIQ | 0.7481 | **0.6454** | 0.6465 |
| NR | TOPIQ-NR | 0.7496 | 0.5981 | **0.7036** |

**Key findings:**
- FR SRCC < 0.65 overall, NR < 0.6 — versus ≈0.9 for the same methods on human-oriented IQA. **The gap is the result.**
- Difficulty ordering: **Position easiest to predict, then State, Rotation hardest.**
- **LPIPS, DISTS, CLIPIQA are worse than the zero-shot baseline even after fine-tuning**, because their main parameters are frozen on HVS priors. Strong evidence that HVS-pretrained perceptual backbones actively hurt.
- Distortion level (HVS-calibrated) barely changes metric performance → **HVS intensity levels are the wrong axis; use RVS JND.**
- Metrics do better on **third-person** and **real** images than first-person / simulation.
- Sensitivity is non-monotonic and counterintuitive: Gaussian *denoise* (Dis16) is severe at level 1; block interpolation (Dis25) is harmless even at level 5. Lens blur mainly hurts VLM; multiplicative noise mainly hurts VLA.
- **Inter-subject agreement is very low**: average SRCC among VLMs ≈ 0.30–0.31 (Precision/Recall/Semantic), among VLAs ≈ 0.23–0.28 (Position/Rotation/State). Human IQA panels typically exceed 0.6. → *One model is not a valid "subject"; you must pool many.*
- **Robustness ranking is surprising**: mPLUG-Owl3 is the most reference/distorted-consistent VLM, Qwen2.5-VL among the least. Octo is robust in Position/Rotation; CogACT and OpenVLA more faithful in State. Rotation is the most distortion-fragile dimension overall.
- **Score distributions**: real > simulation, third-person ≫ first-person (VLA training data rarely includes the actuator/sampling tools in frame).

**Cross-database validation (§5.3).** Train on Embodied-IQA VLA-Decision, test on LIVE, TID2013, and VLM-Cognition:

| Method | LIVE SRCC | TID SRCC | VLM SRCC |
|---|---|---|---|
| AHIQ | 0.5746 | 0.2477 | **0.7240** |
| TOPIQ-FR | 0.7285 | 0.4510 | 0.7115 |
| DISTS | 0.7074 | **0.7106** | 0.4307 |
| CLIPIQA | 0.0472 | 0.0222 | 0.0245 |

→ Fine-tuning on embodied data **destroys human-oriented capability** (SRCC < 0.4 on LIVE for several), but a Decision-trained model **does transfer to Cognition** (AHIQ 0.72). Cognition and Decision are internally linked but neither is human quality.

**Real-world validation (§5.4).** 5 multi-step VLAs × 10 tasks × 30 distortions:
- **Cognition ↔ Execution: SRCC < 0.5** → VLM alone is an inadequate proxy for real robot success.
- **Decision ↔ Execution: SRCC > 0.6** → VLA is a decent but insufficient proxy; real-robot trials remain necessary.

### 1.5 Limitations (as stated + as observed)

*Stated:* (L1) Perception simplified to vision only, Execution to a robot arm only — no tactile, no legged/mobile embodiment. (L2) Only 1,500 real-world Execution labels vs millions of simulated ones, because real-machine data is expensive.

*Observed (not stated by the authors):*
- **Circularity of "subjective" scores.** The "ground truth" is agreement between a model's output on reference vs distorted input. A model can be *consistently wrong* on both and score 5/5. The metric measures **stability, not correctness**.
- **Very low inter-subject SRCC (0.23–0.31)** caps the achievable correlation. An IQA model at SRCC 0.75 against a pooled label whose own subjects agree at 0.25 may already be near the noise ceiling — the paper never estimates this ceiling.
- **Cognition scoring uses BLEU/ROUGE/CIDEr on ~10-word strings.** These are weak, brittle text metrics at that length; "move toward the green board" vs "move toward the black board" is a *task-critical* semantic error that BLEU barely penalises.
- Distortions are **synthetic and global**; real embodied failures are local, temporally correlated, and often geometric (occlusion, motion blur coupled to the robot's own motion).
- **Single frame, no temporal dimension.** Real embodied perception is a video stream in a closed loop.
- The database was to be **released in stages**, non-commercial.

---

## 2. Paper 2 — Embodied Image Quality Assessment for Robotic Intelligence (EPD + MA-EIQA)

### 2.1 Task

**Problem.** IQA for User-Generated Content (UGC) serves human Quality of Experience. Does **Robot-Generated Content (RGC)** behave the same way — or does it show a *Moravec-paradox*-like inversion where what is easy/pleasant for humans is not what matters for robots? Framed as: robots prioritise **texture and structural consistency** and are relatively insensitive to semantic change, the reverse of humans.

**Objective.** (i) Build the first embodied preference database where images are scored **by a robot doing a task, with no human in the loop**; (ii) show HVS-based IQA fails on it; (iii) propose the first **no-reference IQA model designed for embodied robots**, subject to real-time / edge compute constraints.

### 2.2 Dataset — EPD (Embodied Preference Database)

| Property | Value |
|---|---|
| Reference/distorted pairs | 12,500 |
| Episodes (initial scenes) | 100 per task |
| Tasks | 2 — **push** (box to centre of sign) and **pick** (pick up box) |
| Distortions | 25 types × 5 intensity levels, in 7 categories |
| Annotating subjects | 6 embodied "experts" (3 RL algorithms × 2 tasks) |
| Image resolution | 128 × 128 (limited by the RL models' compute) |
| Camera | monocular RGB, mounted on the robot |
| Train/val | 8:2 |

**Distortion categories (7):** Blurs (Gaussian, lens, motion), Color distortions (color diffusion, color shift, color quantization, HSV saturation, Lab saturation), Compression (JPEG2000, JPEG), Noise (white, color, impulse, multiplicative, Gaussian denoise), Brightness change (brighten, darken, mean shift), Spatial distortions (jitter, non-eccentricity patch, pixelate, quantization, color block), Sharpness & contrast (high sharpen, contrast change).

**Simulator & agents.** SAPIEN via the **ManiSkill** benchmark. Three RL algorithms act as the annotators: **PPO**, **SAC**, and **TD-MPC2** (a world-model / MPC method — note this for your world-models agenda). 50 action steps per episode; reward given per step.

**How the score is produced (the key idea).** Only the **initial frame** of an episode is distorted-and-evaluated (distortion type/level held constant across the episode). The **episode's cumulative RL reward** *is* the image's quality label. Reward is preferred over success rate or accuracy because it grades each step rather than giving a binary outcome. Rewards are normalised to **DMOS ∈ (0, 5)**.

**Human comparison.** 15 experienced experts scored the same images to produce a human MOS. **PLCC(human, robot) = 0.2116 (All), 0.1778 (Pick), 0.1297 (Push)** — near-zero agreement. This is the paper's central empirical claim.

**Internal consistency.** Cross-task SRCC is low (push vs pick differ in difficulty and reward scale) but each subtask correlates with the overall score at SRCC > 0.5; all three distributions are approximately normal.

### 2.3 Methods — MA-EIQA

**Design constraints driving the architecture:** robots have limited on-board compute and need real-time scoring; robot-relevant cues are texture detail, edge outline, structural integrity, motion blur — *not* aesthetics; and **CNNs deploy better than Transformers on current edge NPUs**. Hence a deliberately lightweight CNN.

**Architecture (No-Reference):**

```
Input I → ResNet50 backbone (C2,C3,C4,C5)
        → Multi-Scale Feature Encoder (PANet-style bidirectional fusion) → F_E
        → Embodied Attention Module (CBAM-style: Channel Attn → Spatial Attn) → F_A
        → Flatten → 2× FC → quality score y
```

- **Multi-Scale Feature Encoder.** Top-down FPN path `P_i = f_up(P_{i+1}) + T_i(C_i)`, i ∈ {2,3,4} (T_i = 1×1 conv), then a bottom-up enhancement path `N_i = f_down(N_{i-1}) + P_i`, i ∈ {3,4}, with N₂ = P₂ and f_down a stride-2 3×3 conv. Rationale: embodied manipulation needs macro layout **and** micro texture/edge cues simultaneously; a single-scale map cannot serve both.
- **Embodied Attention Module.** CBAM. Channel: `M_c = σ(MLP(AvgPool(F_E)) + MLP(MaxPool(F_E)))`, `F' = M_c ⊗ F_E`. Spatial: `M_s = σ(f^{7×7}([AvgPool_ch(F'); MaxPool_ch(F')]))`, `F_A = M_s ⊗ F'`.
- **Loss:** MSE against the robot-derived DMOS.
- **Size:** 48.83 M params, CNN-based.

### 2.4 Evaluation

**Baselines (16):** PSNR, SSIM (BL); PieAPP, LPIPS, CKDN, IQT, AHIQ, DISTS, TOPIQ-FR (FR); HyperIQA, DBCNN, MANIQA, CLIPIQA, TempQT, TOPIQ-NR, QualiCLIP (NR). Trained on the EPD train split via IQA-PyTorch; 8× RTX 3090 24G. Metrics: SRCC, KRCC, PLCC on three subsets (All / Push / Pick).

**Main results (All Tasks):**

| Type | Method | SRCC | KRCC | PLCC | Params |
|---|---|---|---|---|---|
| BL | PSNR | 0.1660 | 0.1107 | 0.1651 | — |
| BL | SSIM | 0.2347 | 0.1572 | 0.2407 | — |
| FR | **IQT** | 0.5123 | 0.3568 | 0.5315 | 57.72 M |
| FR | DISTS | 0.0737 | 0.0495 | 0.0641 | 14.72 M |
| NR | **MANIQA** | 0.5526 | 0.3855 | 0.5716 | 135.75 M |
| NR | TempQT | 0.5500 | 0.3840 | 0.5620 | 87.45 M |
| NR | **MA-EIQA (ours)** | **0.5755** | **0.4032** | **0.5836** | **48.83 M** |

- Everything is **below 0.6 SRCC** — including the proposed model. The paper is honest about this ("significant optimization space").
- **NR > FR** on average. Interpretation offered: NR extracts features more useful from the robotic viewpoint; also FR reference-comparison is misaligned with an RL reward label.
- **Transformer architectures dominate the strong baselines** (IQT, MANIQA, TempQT), but MA-EIQA matches/beats them as a CNN with 64.03% fewer params than MANIQA and 44.16% fewer than TempQT.
- Per-task: **Pick > Push** in achievable correlation; All Tasks highest.

**Ablation (10 runs averaged, average over 3 subsets):**

| Variant | SRCC | KRCC | PLCC |
|---|---|---|---|
| Baseline (ResNet50 only) | 0.4887 | 0.3394 | 0.5008 |
| + Multi-Scale (MS) | 0.5207 | 0.3641 | 0.5339 |
| + Embodied Attention (EA) | 0.5075 | 0.3527 | 0.5181 |
| **MA-EIQA (MS + EA)** | **0.5475** | **0.3841** | **0.5616** |

MS contributes +6.55 / 7.28 / 6.61 %, EA contributes +3.85 / 3.92 / 3.45 %, combined +12.03 / 13.17 / 12.14 % over baseline.

**Distortion-level findings (Table II/III, level-wise DMOS, 6 EAI subjects):**
- **Colour distortion is the most damaging** to embodied tasks (colour diffusion mean 2.09; colour block 2.16) and most reduces robustness.
- **Motion blur is the least damaging** (mean 2.73) — the opposite of human expectation.
- **Noise is the least damaging category overall** (means 2.65–2.71).
- Most *sensitive to intensity change*: **JPEG2000 compression** and **colour diffusion**; least sensitive: **multiplicative noise**.
- Different EAI subjects disagree with each other, mirroring inter-human variance (D.1 range 2.38–2.73 across the 6 subjects).

**Real-world experiment.** UR5 + ROS, variable desktop background and lighting; first-person distorted input, third-person view of the outcome; error = Euclidean distance from an expert human's successful end-effector position. Reported cases: native camera 4.10 → 2.3 cm; obstruction block 3.64 → 5.8 cm; lens blur 2.34 → 8.7 cm; brighten 2.83 → 10.5 cm; darken 1.58 → 19.3 cm; noise 3.84 → 1.4 cm; motion blur 2.26 → 7.5 cm; JPEG 1.89 → 13.9 cm. **Compression and darkening hurt most; noise and blocking hurt least — while severely hurting human aesthetics.**

### 2.5 Limitations

- **Tiny task space**: 2 tasks (push, pick), one embodiment, 128×128 images. Generalisation to other tasks/embodiments is unestablished.
- **Reward as label is confounded.** RL reward depends on the policy's own competence, its seed, its exploration noise, and reward shaping — not just image quality. Three algorithms with different reward scales are pooled and normalised. This is a noisier label than it appears.
- **Only the initial frame is scored**, but the episode consumes 50 frames — the label is attributed to one image that only partly determines the outcome.
- Ceiling around SRCC 0.58 is unexplained: is it model capacity or label noise? No noise-ceiling analysis.
- MA-EIQA is architecturally conventional (ResNet50 + PANet + CBAM); the novelty is in the *target*, not the network. "Embodied Attention" is CBAM by another name.
- Human MOS collected from only **15 experts on 128×128 images** — a weak human reference against which to declare HVS/RVS divergence.

---

## 3. Paper 3 — Active View Selector (AVS)

### 3.1 Task

**Problem.** In active 3D reconstruction / novel view synthesis (NVS), the system must choose the **next best view** to capture, given a limited budget. Prior art — **ActiveNeRF** (posterior variance minimisation) and **FisherRF** (Fisher-information gain) — computes uncertainty *in 3D*. Two consequences: (a) it is slow (FisherRF needs a Hessian dimensioned by scene parameters, >200 M for 3DGS; 5–8 s per selection over ~200 candidates), and (b) it is **architecture-dependent** — porting between NeRF, 3DGS, SDF and voxel representations needs substantial rework.

**Key observation → reframing.** Whatever informativeness measure prior methods use, they end up picking views where the *current rendering looks bad*. So: **skip 3D uncertainty; just score the 2D rendering's quality and pick the worst one.** They name the strategy **"boost where it struggles."**

**Formal setup.** Given initial posed views `I_init = {(I_i, p_i)}` and a candidate pose pool `P = {p̂_j}` with budget `m < M`, select the m-set `Q ⊆ P` maximising reconstruction quality `R(I_init ∪ {(p̂_j, Î_j)}_{j∈Q})`, adaptively during reconstruction rather than all at once. In active-learning terms this is **estimated error reduction** (Roy & McCallum), as opposed to uncertainty sampling / query-by-committee / expected model change.

**Why plain IQA is not enough.** FR metrics (PSNR, SSIM) need ground truth for the candidate view — unavailable by definition. NR metrics (MUSIQ, MANIQA, NIQE…) work but **lack multi-view context** — they cannot tell "this render is blurry because the scene is under-observed there" from "this is a legitimately soft image."

### 3.2 Datasets

| Dataset | Use | Details |
|---|---|---|
| **Map-Free Relocalisation (MFR)** | training the CR-IQA scorer + eval | 460 outdoor videos, 540×960; **348 train videos, 11 held-out** for eval |
| **Mip-NeRF360** | eval (active NVS) | 9 360° scenes, downscaled 4K → 1066×1600 |
| **RealEstate10K (RE10K)** | eval (active NVS + SfM coverage) | 10-video subset, 960×540 |
| **Habitat / Gibson** | eval (Active-SLAM coverage) | robot exploration with frontier-based path proposals |

**Self-supervised label generation (the dataset *creation* method — important).** No human annotation at all. They fit radiance fields — **3DGS, NeRF, and TensoRF** — to many scene captures; *during* optimisation they periodically render views `{Î_j}` and compare against the real ground-truth images `{I_j}`, producing training triplets:

```
( Î_j ,  {I_i}_{i≠j} ,  SSIM(Î_j, I_j) )
```

i.e. **(query render, K reference real views excluding its own GT, target SSIM map)**. Because renders are captured at many optimisation checkpoints and across three different radiance-field families, the model sees a wide spectrum of artefact types and severities and generalises to unseen scenes. GT is used *only at training time*; at selection time it is unavailable.

### 3.3 Methods

**Component 1 — Cross-Reference IQA model `f_θ`.** Built on **CrossScore** (ECCV 2024, same lab). Input: a query render `Î ∈ R^{3×H×W}` plus K real reference images from other viewpoints of the same scene. Output: a **per-pixel predicted SSIM map** — a full-reference-style score without the reference.

Two variants:
- **Ours-DINOv2** — the pretrained CrossScore model as-is (DINOv2 backbone).
- **Ours-RepViT (default)** — low-latency redesign: DINOv2 replaced by **RepViT** (`m0_9`, 26 layers, ImageNet-pretrained). Features from layers 2, 6, 22, 25 → projected to 256 ch → resized to (h/14, w/14) → summed. Then a **2-layer Transformer decoder** (256 hidden) for cross-referencing, and a **2-layer MLP with sigmoid** for pixel-wise scores in [0,1].

*Training:* 518×518 crops, 5 reference views per query, 20,000 steps, AdamW, constant LR 5e-4, batch 64 per GPU on 2×24GB GPUs, ~13 hours total.

**Component 2 — Active view selection loop (Algorithm 1).**

```
Initialize g_w (random Gaussians), Q = ∅
while |Q| < m:
    optimize reconstruction g_w on I_cur = I_init ∪ {(p̂_j, Î_j)}_{j∈Q}
    Q ← Q ∪ argmin_{p ∈ P\Q}  f_θ( render(g_w, p), I_cur )       # lowest predicted SSIM
return Q, g_w
```

One **single batched forward pass** of a light image network per selection. Crucially, runtime is a function of image count/size, **not scene complexity** — unlike FisherRF, whose cost grows with the number of Gaussian primitives.

**Experimental protocol.** 3DGS trained 30k iterations (default config); start from **4 views chosen by farthest-viewpoint sampling (FVS)**, add views at iterations `[400, 900, 1500, 2200, 3000, 3900, 4900, 6000, 7200, 8500, 9900, 11400, 13000, 14700, 16500, 18400]` (schedule adapted from FisherRF) → **20 training views total**. All 2D baselines share the identical pipeline, differing only in the IQA metric; images resized to long side 518; CrossScore uses 5 reference views.

### 3.4 Evaluation

**Baselines.** *3D-based*: ActiveNeRF (re-implemented on 3DGS; numbers taken from FisherRF), FisherRF, FisherRF4 (batched, 4 views at a time). *2D NR-IQA*: BRISQUE, NIQE, PIQE, TOPIQ, TRES, MANIQA, MUSIQ, NIMA (via PyIQA). *Oracle*: FVS. *Floor*: Random.

**Task A — Active NVS (Mip-NeRF360):**

| | Method | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|
| Oracle | FVS | 20.92 | 0.69 | 0.34 |
| 3D | ActiveNeRF | 17.89 | 0.53 | 0.41 |
| 3D | FisherRF | 20.34 | 0.60 | 0.37 |
| 2D NR | MUSIQ | 19.62 | 0.58 | 0.38 |
| 2D NR | MANIQA | 19.54 | 0.59 | 0.37 |
| 2D NR | TOPIQ | 19.52 | 0.58 | 0.38 |
| 2D NR | Random | 17.91 | 0.56 | 0.43 |
| **CR** | **Ours-DINOv2** | **21.11** | **0.65** | **0.32** |
| **CR** | **Ours-RepViT** | 20.97 | 0.62 | 0.34 |

**RE10K / MFR:**

| Method | RE10K PSNR / SSIM / LPIPS | MFR PSNR / SSIM / LPIPS |
|---|---|---|
| MANIQA | 18.65 / 0.65 / 0.32 | 17.05 / 0.49 / 0.34 |
| MUSIQ | 18.32 / 0.64 / 0.33 | 17.39 / 0.49 / 0.34 |
| FisherRF | 18.86 / 0.66 / 0.32 | 17.21 / 0.48 / 0.35 |
| **Ours** | **19.29 / 0.68 / 0.29** | **17.56 / 0.50 / 0.33** |

**Task B — Scene coverage.**
*SfM with MASt3R (RE10K)* — Surface Coverage Ratio (fraction of reference-model surface within τ = 0.01 × scene extent) and F-score (thresholds 0.001/0.01/0.1, averaged):

| Method | SCR (%) ↑ | F-score ↑ |
|---|---|---|
| FisherRF | 50.88 | 0.52 |
| MANIQA | 51.87 | 0.52 |
| MUSIQ | 44.08 | 0.47 |
| **Ours** | **53.89** | **0.54** |

*Active-SLAM with SplaTAM on Habitat/Gibson* (frontier-based exploration; SCR at 5 cm threshold per FisherRF convention; Depth MAE from 1000 uniformly sampled poses):

| Method | SCR (%) ↑ | Depth MAE (m) ↓ | PSNR ↑ |
|---|---|---|---|
| FisherRF | 92.89 | 0.092 | 22.58 |
| **Ours** | **93.71** | **0.076** | **23.9** |

**Runtime (Garden scene, RTX 4090):**

| Method | PSNR ↑ | Time (s) ↓ | GPU Mem (GB) ↓ |
|---|---|---|---|
| FVS (oracle) | 23.15 | 0.00 | — |
| FisherRF | 21.33 | 8.34 | 15.8 |
| FisherRF4 | 22.31 | 19.70 | — |
| TOPIQ | 21.24 | 0.50 | — |
| TRES | 21.77 | 7.17 | — |
| MANIQA | 21.61 | 11.21 | — |
| **Ours-DINOv2** | **23.05** | 1.21 | 20.1 |
| **Ours-RepViT** | 22.96 | **0.59** | **8.3** |

→ **14× faster than FisherRF, 33× faster than FisherRF4, ~half the memory**, with higher PSNR. Selection time grows over training for *all* methods (more Gaussians → slower rendering and slower 3D analysis).

### 3.5 Limitations

- The scorer is **trained to predict SSIM**, so it inherits SSIM's blind spots and is a *reconstruction-fidelity* proxy, not a *task-utility* proxy. Nothing here knows what the robot is trying to do.
- Selection is **greedy per step**; no lookahead, no batch diversity — two adjacent bad views can both be picked.
- Requires **rendering every candidate view** at every step (~200 for Mip-NeRF360). Cheap per view, but linear in candidate count; the paper does not prune the candidate set.
- Evaluated on **static scenes**; no dynamics, no manipulation, no moving objects.
- Even the best method does not beat the **FVS oracle** on the Garden scene (23.15 vs 23.05) — geometric coverage heuristics remain very strong on 360° captures.
- Motion cost is ignored: the "next best view" may be far away, which matters for a real robot but not for a dataset replay.

---

## 4. Cross-paper synthesis

### 4.1 Where they agree

1. **HVS-trained IQA does not transfer.** Paper 1: fine-tuned LPIPS/DISTS/CLIPIQA fall *below* zero-shot baselines. Paper 2: PLCC(human, robot) ≈ 0.13–0.21. Paper 3: NR-IQA metrics are usable but plateau well below a task-adapted cross-reference model.
2. **Reference-free is the operational regime.** Robots never have a clean reference at deployment time. Paper 1 shows FR still beats NR *when a reference exists*; Paper 2 finds NR > FR on RL-reward labels; Paper 3 dissolves the dichotomy with **cross-reference** — full-reference-quality signal from other viewpoints instead of the missing GT.
3. **Compute matters.** Paper 2 argues for CNNs on edge NPUs (48.83 M params); Paper 3 swaps DINOv2 → RepViT for 2× speed and ⅓ memory. Any deployable embodied metric has a latency budget.
4. **Distortion severity as perceived by humans is the wrong axis.** Paper 1 replaces it with machine JND bands; Paper 2 finds motion blur harmless and colour distortion catastrophic — inverted relative to human intuition.

### 4.2 Where they diverge — and the gap this exposes

| Axis | Paper 1 (Embodied-IQA) | Paper 2 (EPD) | Paper 3 (AVS) |
|---|---|---|---|
| Quality *defined as* | fidelity of VLM/VLA output vs reference-image output, + real execution error | cumulative RL episode reward | predicted SSIM vs (unavailable) GT render |
| Label source | 15 VLMs + 15 VLAs + UR5 | 3 RL algos × 2 tasks in SAPIEN | self-supervised SSIM from radiance-field fitting |
| Reference regime | FR and NR | NR | **cross-reference (multi-view)** |
| Task-conditioned? | **Yes** (5 NL tasks per image) | Weakly (2 fixed tasks) | **No** |
| Purpose of the score | *diagnose / filter* bad images | *diagnose / filter* bad images | ***act*** — choose the next viewpoint |
| Closed-loop? | No (one-shot scoring) | No (initial frame only) | **Yes** (score → move → re-score) |
| Best correlation achieved | ~0.75 SRCC (TOPIQ-FR, Position) | ~0.58 SRCC (MA-EIQA) | n/a (evaluated by downstream PSNR/SCR) |

**The gap in one sentence:** Papers 1–2 have the *right target* (task utility for a robot) but a **passive, single-frame, non-actionable** metric; Paper 3 has the *right mechanism* (cheap, reference-free, multi-view, closed-loop, drives an action) but the **wrong target** (SSIM fidelity, task-agnostic).

---

## 5. Research scope — is there room for a new, comprehensive metric?

**Yes, and the space is unusually well-defined right now.** Three independent signals say so: (a) every metric in Paper 1 tops out at SRCC ≈ 0.75 and most below 0.65; (b) Paper 2's own proposed model reaches only 0.58; (c) the community has just formalised the problem into a challenge (MoIQA at ACM MM 2026, §7), which means benchmarks, baselines and reviewers now exist for exactly this contribution. This is a rare window where the problem is agreed on but unsolved.

### 5.1 What is missing from every existing metric

| # | Missing property | Why it matters | Who is closest |
|---|---|---|---|
| G1 | **Task conditioning** | The same image is 5/5 for "push the board" and 1/5 for "pick the small red block." Paper 1 collects per-task labels but the *metrics* it benchmarks ingest only pixels — the task string is thrown away. | nobody |
| G2 | **Spatially localised, actionable quality** | A global scalar cannot say *where* the problem is; Paper 1's own case study shows a level-1 block-loss on the target object scores 2.98 while a level-5 distortion elsewhere scores 4.52. Paper 3 produces per-pixel maps but ignores tasks. | AVS (maps), RA-MIQA (regions) |
| G3 | **Temporal / closed-loop scoring** | All three score a single frame. Embodied perception is a stream, and blur/jitter are inherently temporal. | nobody |
| G4 | **Actionability** | A number that only *rejects* an image is far less valuable than one whose gradient tells the robot **where to move to get a better one**. | AVS (but SSIM-targeted) |
| G5 | **Calibration / uncertainty** | No metric reports "quality 0.4 ± 0.3". With inter-subject SRCC of 0.25, a point estimate is misleading. Downstream a robot needs a *decision* (proceed / re-observe / abort), which needs calibrated risk. | nobody |
| G6 | **Correctness, not just stability** | Papers 1's label = agreement between reference-output and distorted-output. A confidently wrong model scores perfectly. | partially, Paper 2 (reward is grounded in task success) |
| G7 | **Cross-embodiment transfer** | Labels are tied to specific VLAs / RL policies / arms. Does the metric transfer to a new policy without re-annotation? | untested by all three |

### 5.2 Concrete proposal — a metric worth building

**Working name: TAC-Q — Task-Aware Cross-referenced Quality (or "Actionable Embodied Quality").**

**Definition.** For a task instruction `T`, current observation `I_t`, and a set of recent/neighbouring views `{I_k}`, predict a **spatial utility map** `U(x, y | T, I_t, {I_k}) ∈ [0,1]` and a calibrated scalar `q = agg(U)` with predictive interval, where `U` estimates *the probability that the task-relevant information at that location is sufficient for the downstream policy to act correctly*.

**Four properties, mapping onto G1–G5:**

1. **Task-conditioned** — cross-attend the CLIP/VLM embedding of the instruction `T` into the quality head. Directly fills G1. Paper 1's dataset **already has 6,150 task strings** paired with per-image, per-task VLM/VLA scores — the labels exist; nobody has trained on the (image, task) pair.
2. **Cross-referenced, not no-reference** — steal Paper 3's mechanism: use other viewpoints of the same scene as the implicit reference. In an embodied setting these are *free* — the robot's own previous frames. This is the single most transferable idea across the three papers and it is currently used only for static NVS.
3. **Dense and actionable** — output a map, not a scalar, and define the view-selection / re-observation action as `argmin` over the map's task-relevant region (Paper 3's "boost where it struggles", now task-weighted). Fills G2 + G4.
4. **Calibrated to downstream success** — train against a *distribution* of downstream outcomes (Paper 1's 15 VLAs are a ready-made ensemble; their pairwise SRCC of 0.25 is not noise to be averaged away, it is **epistemic spread to be predicted**). Fills G5. Report expected task success and its variance, not an opinion score.

**Training data — assembled, not collected from scratch.** Embodied-IQA (36.9k pairs, 5.53 M labels, tasks included) + EPD (12.5k, RL-reward labels) + AVS-style self-supervised multi-view SSIM triplets from any posed video (MFR, DROID, RE10K) + MoIQA-Sim/Real when released. The self-supervised part is what makes scale achievable without a robot lab.

**Evaluation — where you can beat the current numbers.**
- Primary: SRCC/PLCC/KRCC against Paper 1's Decision and Execution scores, **stratified by task string** (this stratification is itself new — nobody has reported per-task-difficulty correlation).
- Secondary: **decision quality**, not just correlation — precision/recall of "should the robot re-observe before acting?" at a fixed budget. This reframes IQA as a detection problem with an operating point, which is what a deployed system actually needs.
- Tertiary: plug it into Paper 3's Algorithm 1 in place of the SSIM predictor and report NVS PSNR + SCR + *task* success. **A metric that improves both a passive benchmark and a closed-loop task is a much stronger paper than one that improves either alone.**
- Cross-embodiment held-out: train with 12 VLAs, test on 3 unseen. Nobody has reported this; it is cheap and it is the reviewer's first question.

**Why this is publishable rather than incremental:** it is the first metric that is simultaneously *task-conditioned*, *reference-free-but-multi-view*, *dense*, and *validated in a closed loop*. Each of the three papers has exactly one or two of those properties.

### 5.3 Alignment with your existing agenda

This connects directly to `Possible_Project_Ideas.md`:
- **Idea 2 "Moving to see better"** — TAC-Q *is* the reward function that idea needs. Your note says "reward it according to how good the incoming view is, judged without needing a clean reference image, balanced against the task reward so it does not chase nice-looking but useless views." A **task-conditioned** quality score removes exactly that failure mode by construction: pretty-but-useless views score low because the task token says so. Paper 3 is the proof that a cross-reference score is fast enough to sit inside a control loop (0.59 s, and that includes rendering 200 candidates).
- **Idea 1 "Better future-prediction for agents"** — Paper 1's finding that HVS-frozen perceptual metrics (LPIPS/DISTS) *underperform PSNR* on robot preference is a direct, citable warning for using LPIPS as a world-model training loss. Combined with *World-in-World* (§7), you have two independent 2025 results that pixel/perceptual metrics do not track embodied usefulness. That is a strong motivation paragraph.
- **Idea 4/5 (bandwidth, shared scene)** — a *dense task-conditioned utility map* is precisely the "spatial confidence map" that Where2comm-style methods need, but grounded in downstream task success rather than detection confidence.

### 5.4 Risks to plan around

- **Label-noise ceiling.** With inter-subject SRCC ≈ 0.25 (VLA), you may be near the achievable maximum already. *Mitigation:* estimate the ceiling explicitly (split-half reliability / Spearman–Brown on the 15 subjects) and report performance **as a fraction of ceiling**. This alone would be a useful contribution and would reframe Paper 1's "0.75 is not good enough" claim.
- **Circularity of "quality = output stability."** *Mitigation:* weight Execution (grounded, real) labels far more heavily than Cognition/Decision (self-consistency) labels, or train on stability but validate on execution success.
- **Real-robot data cost.** Paper 1 got only 1,500 execution labels for exactly this reason. *Mitigation:* lean on the self-supervised multi-view branch for scale and use real-robot data only for calibration/validation.
- **Compute for annotation.** Paper 1 used 2×16 A800s. You do not need to reproduce it — use their released database (staged release, non-commercial).

---

## 6. Research gaps and future directions

**From the papers' own stated limitations**
1. Perception beyond vision — vision-tactile fusion, depth, audio (Paper 1 L1).
2. Embodiments beyond a fixed arm — quadrupeds, mobile manipulators, drones (Papers 1 L1, 2).
3. Scale of real-world execution labels; an automated real-world annotation pipeline (Paper 1 L2).

**Gaps neither paper states**

4. **No video / temporal IQA for embodied AI.** Every dataset here is single-frame. Motion blur, rolling shutter, exposure hunting and jitter are *temporal* phenomena, and the robot's own motion causes them. An embodied VQA (video quality) benchmark is wide open.
5. **No noise-ceiling analysis.** See §5.4. The field is reporting raw SRCC against labels whose subjects agree at 0.25.
6. **Synthetic-distortion bias.** All 30 (Paper 1) / 25 (Paper 2) distortions are synthetic and global. Real embodied failure modes — occlusion by the robot's own arm, specularity, motion blur correlated with the trajectory, out-of-focus at close manipulation range, sensor saturation — are local, structured and *self-induced*. A **naturally-distorted, in-the-wild embodied IQA set** is missing.
7. **First-person perspective is under-served.** Both papers report first-person performs markedly worse (Paper 1: VLA training data rarely contains the actuator in frame). But first-person *is* the deployment condition for wrist cameras. This is a concrete, narrow, publishable gap.
8. **Quality metrics are not yet used as control signals in manipulation.** Paper 3 does it for reconstruction; nobody does it for a VLA policy deciding to re-observe.
9. **No standard for "quality-aware VLA".** Should the VLA consume the quality score as input? Abstain? Request a new view? Today the metric sits outside the policy. A policy with a *learned abstention/re-observation head* conditioned on quality is unexplored.
10. **Metric ↔ restoration co-design.** If darkening and compression are the worst distortions for robots (Paper 2) and Gaussian denoise is severe even at level 1 (Paper 1 — i.e. *denoising hurts robots*), then robot-oriented restoration/enhancement is misaligned with human-oriented restoration. Nobody has built a restoration model optimised for a robot-preference metric.
11. **Cross-embodiment / cross-policy generalisation of the metric** — untested (§5.1 G7).
12. **Economics of the loop.** Paper 3 ignores motion cost. A real "next best view" trades information gain against travel time, energy and collision risk. A quality metric with a *cost-aware* selection rule is an obvious and missing extension.

---

## 7. Related recent work (2024–2026)

> Links below come from literature search; arXiv IDs from 2026 are recent and should be confirmed before formal citation.

### 7.1 Direct lineage — machine / embodied IQA

| Work | Year | Relevance |
|---|---|---|
| [Image Quality Assessment: From Human to Machine Preference (MPD)](https://openaccess.thecvf.com/content/CVPR2025/papers/Li_Image_Quality_Assessment_From_Human_to_Machine_Preference_CVPR_2025_paper.pdf) | CVPR 2025 | Same group; the **MPD** database (1k ref / 30k distorted / 2.25 M annotations, 5 machine subjects). The direct predecessor of Embodied-IQA on the *machine* (Cognition-only) side; ref [14] of Paper 1. |
| [Image Quality Assessment for Machines: Paradigm, Large-scale Database, and Models (MIQD-2.5M / RA-MIQA)](https://arxiv.org/abs/2508.19850) | 2025 | Independent group (Wang, Zhang, Lin). **2.5 M** degraded images from ImageNet + COCO, 10 distortions × 5 severities × **3 spatial patterns** (uniform / ROI-dominated / background-dominated), labelled by **75 vision models** across classification, detection, segmentation. Proposes **RA-MIQA**, a *region-aware* Transformer. Reports HVS metrics at SRCC 0.24–0.54 on machine labels — corroborates Paper 1 independently. **The spatial-pattern axis is the closest existing work to gap G2.** |
| [Machine-oriented Image Quality Assessment (MoIQA) Challenge, ACM MM 2026](https://openreview.net/forum?id=594Zi8w9SZ) | 2026 | **The most actionable item here.** Two tracks: **MoIQA-Sim** (agreement with VLM performance in simulation) and **MoIQA-Real** (agreement with VLA results in the real world). Releases MoIQA-Sim / MoIQA-Real datasets plus MachineIQA/EmbodiedIQA under CC BY-NC-SA. A ready-made venue and benchmark for a new metric. |
| [ML-CLIPSim: Multi-Layer CLIP Similarity for Machine-Oriented Image Quality](https://arxiv.org/abs/2605.09479) | 2026 | Machine-aligned distortion measure used as the **distortion term in learned image compression**, improving rate–task trade-offs. Shows the metric-as-loss direction (relevant to gap 10). |
| [R-Bench: Are your Large Multimodal Models Robust to Real-world Corruptions?](https://arxiv.org/abs/2410.05474) | JSTSP 2024/25 | Same group; robustness of MLLMs under real corruptions. Ref [10] of Paper 1. |
| [Q-Align: Teaching LMMs for Visual Scoring via Discrete Text-Defined Levels](https://arxiv.org/abs/2312.17090) | ICML 2024 | Used by Paper 1 both as a pre-filter and a zero-shot baseline. |
| [LoViF 2026 Challenge on Human-oriented Semantic IQA](https://arxiv.org/abs/2604.11207) | 2026 | The human-oriented counterpart; useful as the contrast case for a human/machine dual-target metric. |

### 7.2 Cross-reference & NVS quality assessment

| Work | Year | Relevance |
|---|---|---|
| [CrossScore: Towards Multi-View Image Evaluation and Scoring](https://arxiv.org/abs/2404.14409) | ECCV 2024 | The mechanism Paper 3 builds on. Cross-attention over multi-view references to predict SSIM without GT. **Read this before building anything cross-reference.** |
| [NOVA: Non-Aligned Reference IQA for Novel View Synthesis](https://stootaghaj.github.io/nova-project/) | WACV 2026 | Direct competitor/successor to CrossScore — quality assessment with *non-aligned* references. Relevant to whether "reference from another viewpoint" needs alignment. |

### 7.3 Active view selection / next-best-view (post-AVS)

| Work | Year | Relevance |
|---|---|---|
| [Peering into the Unknown: Active View Selection with Neural Uncertainty Maps](https://arxiv.org/abs/2506.14856) | 2025 | Contemporary to AVS; learned 2D uncertainty maps for view selection — the "uncertainty" analogue of AVS's "quality". |
| [SA-ResGS: Self-Augmented Residual 3DGS for Next Best View Selection](https://arxiv.org/abs/2601.03024) | 2026 | Stabilised uncertainty quantification for NBV — the 3D-side rebuttal to AVS's "skip 3D" argument. |
| [OUGS: Active View Selection via Object-aware Uncertainty Estimation in 3DGS](https://onlinelibrary.wiley.com/doi/10.1111/cgf.70363) | 2026 (CGF) | Uncertainty derived from the *physical parameters* of Gaussian primitives; object-aware. |
| [Informative Object-centric Next Best View for 3DGS in Cluttered Scenes](https://arxiv.org/abs/2602.08266) | 2026 | Object-centric NBV — closer to manipulation than scene-level NVS. |
| [Hestia: Voxel-Face-Aware Hierarchical Next-Best-View Acquisition](https://arxiv.org/abs/2508.01014) | 2025 | Efficient hierarchical NBV. |
| [ObjSplat: Geometry-Aware Gaussian Surfels for Active Object Reconstruction](https://arxiv.org/abs/2601.06997) | 2026 | Active object-level reconstruction. |
| [VISTA: Open-Vocabulary, Task-Relevant Robot Exploration with Online Semantic Gaussian Splatting](https://arxiv.org/abs/2507.01125) | 2025 | **Task-relevant** exploration — the semantic/task conditioning that AVS lacks (gap G1), applied to exploration rather than quality. |
| [Multi-Agent Next-Best-View Optimization for Risk-Averse Planning](https://arxiv.org/abs/2606.04158) | 2026 | Multi-agent NBV with risk — connects to your Idea 4/5. |
| [Next Best Sense: Guiding Vision and Touch with FisherRF for 3DGS](https://arm.stanford.edu/next-best-sense) | 2025 | Extends FisherRF to **vision + touch** — the multimodal perception gap Paper 1 flags as future work. |
| [FisherRF: Active View Selection and Mapping with Radiance Fields using Fisher Information](https://arxiv.org/abs/2311.17874) | ECCV 2024 | The baseline AVS dethrones. |

### 7.4 Active perception in VLA / manipulation

| Work | Year | Relevance |
|---|---|---|
| [ActiveVLA: Injecting Active Perception into VLA Models for Precise 3D Robotic Manipulation](https://arxiv.org/abs/2601.08325) | 2026 | Adaptive viewpoint **and camera resolution** selection inside a VLA; active 3D zoom-in. The closest existing system to "quality-aware VLA" (gap 9) — but it optimises task success directly, not a quality metric. |
| [Learning to See and Act: Task-Aware View Planning for Robotic Manipulation (TAVP)](https://arxiv.org/abs/2508.05186) | 2025 | Task-aware view planning + MoE visual encoder. **Task conditioning of viewpoint choice** — the G1 idea, applied to planning rather than to a metric. |
| [Act, Sense, Act: Learning Non-Markovian Active Perception Strategies from Large-Scale Egocentric Human Data](https://arxiv.org/abs/2602.04600) | 2026 | Non-Markovian active perception from egocentric human data. |
| [Observe Then Act: Asynchronous Active Vision-Action Model for Robotic Manipulation](https://arxiv.org/abs/2409.14891) | 2024/25 | Camera-NBV policy serially connected to a gripper-NBP policy. |
| [Viewpoint-Agnostic Manipulation Policies with Strategic Vantage Selection](https://arxiv.org/abs/2506.12261) | 2025 | Vantage selection for robust manipulation. |
| [UniviewVLA: A Unified Multiview VLA Model with World Modeling](https://arxiv.org/abs/2606.21501) | 2026 | Multiview + world modelling in one VLA — bridges your world-models agenda with the multi-view idea. |
| [GCNGrasp-VP: Affordance-Guided View Planning for Task-Oriented Grasping](https://arxiv.org/abs/2606.19091) | 2026 | Affordance-guided (i.e. task-guided) view planning. |

### 7.5 VLA robustness under perturbation — the "why this metric matters" evidence

| Work | Year | Relevance |
|---|---|---|
| [On Robustness of Vision-Language-Action Model against Multi-Modal Perturbations](https://arxiv.org/abs/2510.00037) | 2025 | Systematic VLA robustness under multi-modal perturbation — independent confirmation of Paper 1's premise. |
| [Benchmarking VLA Models on SO-101: Failure and Recovery Analysis](https://arxiv.org/abs/2606.08881) | 2026 | Structured **failure taxonomy**, semantic- vs execution-level failure decomposition, recovery-aware metrics. Directly useful for defining what "quality" should predict (gap G6). |
| [RoboDojo: A Unified Sim-and-Real Benchmark for Generalist Robot Manipulation Policies](https://arxiv.org/abs/2607.04434) | 2026 | Sim-and-real evaluation harness — a candidate testbed for closed-loop validation of a new metric. |

### 7.6 Closed-loop evaluation of world models (your adjacent agenda)

| Work | Year | Relevance |
|---|---|---|
| [World-in-World: World Models in a Closed-Loop World](https://arxiv.org/abs/2510.18135) | 2025 | Evaluates world models by embodied interaction; reports **large gaps between visual quality metrics and task success**. The strongest single citation for "pixel metrics ≠ usefulness". Already in your `Literature_Review_Recent.md`. |
| [WorldModelBench: Judging Video Generation Models as World Models](https://arxiv.org/abs/2502.20694) | 2025 | Benchmark-design precedent for judging generative models by embodied criteria. |

### 7.7 IQA as a reward / reasoning signal

| Work | Year | Relevance |
|---|---|---|
| [VisualQuality-R1: Reasoning-Induced IQA via Reinforcement Learning to Rank](https://arxiv.org/abs/2505.14460) | 2025 | RL-to-rank for IQA; a template for training a metric with ranking rather than regression objectives (useful given noisy DMOS labels). |
| [Zoom-IQA: IQA with Reliable Region-Aware Reasoning](https://arxiv.org/abs/2601.02918) | 2026 | Region-aware reasoning for IQA — the spatial-localisation direction (G2). |
| [Q-DeepSight: Incentivizing Thinking with Images for IQA and Refinement](https://arxiv.org/abs/2604.16858) | 2026 | Assess-and-refine loop; translates localised quality diagnoses into targeted edits. Analogous to "diagnose → re-observe" for robots. |

---

## 8. Appendices

### 8.1 Flagged discrepancies (check before citing)

1. **Embodied-IQA size is reported three ways.** Abstract: "over 30k reference/distorted image pairs". Contributions: "over 36k". Table 1 / §3.1: **1,230 reference + 36,900 distorted**, 5.53 M annotations. Use the Table 1 / §3.1 numbers.
2. **EPD is described differently by the two papers.** Paper 2 (its own paper): **12,500** reference/distorted pairs, 12.5k labels, 6 EAI subjects, 100 episodes × 25 distortions × 5 levels. Paper 1's Table 1 lists EPD as **100 reference / 2.5k distorted / 30k annotations / 2 subjects / 256 resolution**. Paper 2 also states 128×128 images, not 256. Cite Paper 2's own numbers for EPD.
3. **Paper 1 §5.3 refers to "Table 8(a)"** for cross-database validation, but the content is in **Figure 8(a)**.
4. **Paper 1 supplementary Figure 12** is captioned "Low-level feature distribution of **MPD**" inside the Embodied-IQA paper — likely a copy-over from the earlier MPD paper (CVPR 2025). Verify which database that figure actually describes.
5. **Paper 1 supplementary** misspells "Mortonian" for "Mertonian" once.
6. **Paper 1 reference [40]** is used for both ROUGE and CIDEr; only the CIDEr entry (Vedantam et al.) is present in the bibliography. The ROUGE citation is missing.
7. **Paper 2 Table IV caption** says "Comparison of 14 IQA methods for BL/FR/NR" but the table is the **4-variant ablation study**. Caption is copy-pasted from Table I.

### 8.2 Reusable resources

| Resource | Where | Note |
|---|---|---|
| Embodied-IQA database | github.com/lcysyzxdxc/EmbodiedIQA | Staged release, non-commercial |
| EPD benchmark | github.com/Jianbo-maker/EPD_benchmark | |
| Active View Selector | avs.active.vision | |
| `pyiqa` / IQA-PyTorch | github.com/chaofengc/IQA-PyTorch | Used by **both** Papers 1 and 2 — the standard harness for reproducing these baselines |
| MoIQA-Sim / MoIQA-Real | via ACM MM 2026 grand challenge | CC BY-NC-SA |
| MIQD-2.5M | arXiv 2508.19850 | 2.5 M images, 75 models |

### 8.3 Hardware used (for planning your own experiments)

- Paper 1: annotation on 2 × (16 × A800 SXM4 80GB); IQA training on 1 GPU. UR5 + Robotiq 2F-140, RealSense D455 array.
- Paper 2: 8 × RTX 3090 24G. UR5 + ROS. SAPIEN/ManiSkill.
- Paper 3: training on 2 × 24GB GPUs, ~13 h. Evaluation on 1 × RTX 4090. → **Paper 3's setup is reproducible on your hardware; Paper 1's annotation stage is not (use their released labels).**

---

## 9. Append log

> Add new queries, follow-up analyses, and per-paper deep dives below. Keep sections 1–8 as the stable base.

### Entry 1 — 2026-08-07 — initial compilation
Full read of all three PDFs (Paper 1: 21 pp incl. supplementary; Paper 2: 13 pp; Paper 3: 13 pp incl. supplementary). Related-work sweep for 2024–2026. Open threads left deliberately unresolved, for a later pass:
- [ ] Read CrossScore (ECCV 2024) in full — it is the actual mechanism behind Paper 3 and the most reusable component for a new metric.
- [ ] Read the MPD paper (CVPR 2025) — the missing middle between EPD and Embodied-IQA, and the source of Paper 1's methodology.
- [ ] Pull MIQD-2.5M / RA-MIQA (2508.19850) in full — the region-aware angle overlaps most with proposed gap G2.
- [ ] Check MoIQA challenge deadlines/tracks at 2026.acmmm.org/site/grand-challenges.html.
- [ ] Estimate the label noise ceiling on Embodied-IQA (split-half over the 15 VLAs) — cheap to compute from the released database, and potentially a contribution on its own.
{% endraw %}


<div class="wm-backlink wm-backlink-bottom">
  <a href="{{ '/blog/world-models/' | relative_url }}">&larr; Back to the <strong>World Models</strong> series</a>
</div>

<style>
.wm-backlink { margin: 0 0 1.2rem; font-size: 0.92rem; }
.wm-backlink-bottom { margin: 2rem 0 0; }
.wm-backlink a { color: var(--global-theme-color); text-decoration: none; }
.wm-backlink a:hover { text-decoration: underline; }
</style>
