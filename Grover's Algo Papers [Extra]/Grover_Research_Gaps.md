# Grover research gaps, v2: the verified map and the one question worth a Q1 paper

*2 Oct 2026. Replaces v1 (still in git history: `git show a31603f:"Path_3 (Grover's)/Grover_Research_Gaps.md"`). Built from v1, the papers in `Papers/`, the faculty note (`Papers/Fac_opinion.md`), the critiques in `OLD IDEAS/`, a new literature sweep, and three small experiments (`grover_guessing_checks.py` in this folder, runs in ~2 min).*

**Evidence tags:**
- **[V]** = I read the source text (or the stated section) in this session.
- **[V, v1]** = read in the v1 session, not re-read today.
- **[S]** = search result or abstract only.
- **[K]** = from my own knowledge, not re-checked today.
- **[E]** = computed by `grover_guessing_checks.py` in this session.
- **[I]** = my inference or derivation. Treat it as a hypothesis until you check it.

---

## 0. The short answer (what changed from v1)

**1. v1's core is real but probably an "expensive confirmation".** v1 bet on G1/G2: price memory-hard password hashing (scrypt, Argon2id) against Grover. The new reading shows why that is weak as a headline:
- The National Academies' 2019 report already prices a Grover attack on PBKDF2 (10,000 iterations, 66-bit passwords) at **2.3 × 10⁷ years** [V].
- Fault-tolerant cost studies of Grover keep reaching the same "not practical" verdict: AES (NCSC 2024 [S]) and Bitcoin mining ("Kardashev-scale", March 2026 [S]).
- My own bracket [I]: once you add a wall-clock or depth limit, **the depth of the KDF kills Grover before memory-hardness even matters.**
- So G1/G2 would most likely end in "no threat, ranking unchanged". That changes nobody's decision. It becomes an application chapter (§4), not the core.

**2. The notable gap is somewhere else: the "super-quadratic" quantum guessing claims.** Three works say a quantum attacker gains **more than** a square root when the secret is not uniform:
- **Montanaro (TQC 2010):** "exponential" average-case speedups for power-law advice [S].
- **Glaser–May–Nowakowski (GMN):** s > 2.04 for LinkedIn passwords, plus Kyber and LPN cases [V]. ePrint 2023/797, Springer LNCS 2026.
- **Schubert et al. (TU Berlin / Fraunhofer, arXiv 2609.28226, 23 Sept 2026):** exponents **up to 3.97** for side-channel posteriors on ML-KEM/ML-DSA [V].

All three measure **expected cost with unlimited sequential time**. None uses a fixed budget, a depth limit, parallel machines or the cost of loading the prior [V].

**3. My checks [E] + [I] say these speedups do not survive the constraints a real attacker faces:**
- **Fixed success target.** For *every* prior, the quantum queries needed for success α lie between **½√B_α and (π/4)√B_α**, where B_α is the classical budget [I, from Zalka 1999 + He–Zhang–Sun 2020].
  - That is exactly quadratic.
  - Reading "quantum cost = classical^(1/s)" predicts attacks **below a provable minimum**, by 2⁴–2⁸ in my examples [E].
- **Depth limit.** Cap each Grover run at k sequential iterations, with k = MAXDEPTH / oracle depth.
  - In two heavy-tailed toy priors I built, the expected-cost exponent falls from **2.51 to 1.25** and from **3.23 to 1.72** at NIST's MAXDEPTH = 2⁴⁰ with a cipher-sized oracle [E].
  - Full super-quadratic gains need **k ≥ 2⁵⁰–2⁸²** sequential iterations in these priors [E].
  - Schubert's and GMN's own cases are **not yet recomputed**. That is the week-1 kill test (§8).

**The core research question (★):**
> **Do super-quadratic quantum speedups for guessing non-uniform secrets survive the constraints a real attacker faces (a success target, a depth or wall-clock limit, parallel machines, and the cost of loading the prior)? Where exactly is the boundary, and what is the correct quantum security discount for passwords, leaked keys and LWE/LPN secrets?**

**Both outcomes are publishable:**
- **No region survives at security-relevant sizes:** this corrects how a fresh, actively cited line of results is used to set parameters.
- **A region survives** (my numbers hint at one: moderate sizes, strong skew, deep runs): this is the first map of where super-quadratic quantum cryptanalysis is *operationally real*.

| # | Gap | Role | Status |
|---|---|---|---|
| **Q★1** | Super-quadratic guessing under a budget, a depth limit and parallelism: theorems + phase diagram + recomputation of every published case | **Core (paper 1)** | Not found in the literature (§2) |
| **Q★2** | The "loader": the circuit that prepares the prior runs **twice per Grover iteration**. What is the cheapest near-optimal loader for Markov/PCFG/product priors, and how much speedup does it cost? | **Core (algorithmic)** | Open for Markov/PCFG; product priors use QRAM (Martin et al. 2017) |
| A1 | Passwords (the faculty's scenario): quantum guess numbers + the **depth defence** (key stretching caps the quantum speedup at ~k). Includes v1 G1/G2/G5 | Application chapter, paper 2 | Partly priced (NAP 2019); memory-hard part unpriced |
| A2 | Leakage (side channel, cold boot) on AES / ML-KEM: quantum residual security under depth limits | Application chapter | Schubert 2026 gives exponents only |
| T | Toy model: exact Qiskit simulation of prior-advised, depth-capped search with real loaders (the faculty's "new toy model") | Instrument | Nearest: JRC ePrint 2026/2085 (uniform prior, no depth cap) |
| O1–O6 | Hard open problems with no known way out (§7) | For intensive study | Open |

**What v1 gaps became:**
- **G1 and G2** → A1, as sub-sections.
- **G3** → Q★2. Its "quantum strength meter" is now a corollary (§4.1).
- **G4** (exact exponents for dependent priors) → dropped as a core item. It computes the moment exponent, which §2 shows is the wrong security metric. Kept as O6.
- **G5** → part of A1.
- **G6** → T.

---

## 1. Why the target moved: what the new reading showed

| Finding | Evidence | Consequence |
|---|---|---|
| GMN: classical cost ≈ 2^H₁/₂, quantum (Montanaro) ≈ 2^(H₂/₃ / 2). Speedup s ≥ 2·H₁/₂ / H₂/₃ > 2. The algorithm assumes **black-box GetKey_D** (the i-th likeliest key). Multi-key per-key cost is **Shannon H classically, H/2 quantumly**, i.e. exactly quadratic | arXiv 2509.06549 [V] | The single-key super-quadratic number is an **expected-cost** statement. The realistic "crack many accounts" setting is already plain quadratic in their own theorem |
| Schubert et al. define s = ln E[G] / ln E[√G]. They say Jensen gives s ≥ 2. They treat **only** product priors. **No** budget, depth, parallelism or state-preparation analysis | arXiv 2609.28226 [V] | The per-instance quantum cost is √(rank). s > 2 comes from averaging a heavy tail |
| He–Zhang–Sun 2020 (arXiv only; it did not appear in what I read of GMN or Schubert, so check their reference lists) prove the **optimal success probability with exactly T queries** for any prior: ESP_T = max Σ pᵢ sin²((2T+1)·asin√qᵢ) over Σqᵢ ≤ 1 | arXiv 2009.08721 [V] | This is the budgeted counterpart. Combined with Zalka 1999 it gives the sandwich in §2.1 |
| Martin–Montanaro–Oswald–Shepherd (SAC 2017): quantum key search with side-channel advice, run to an **enumeration budget**. Result: **quadratic**. Assumes QRAM. No depth limit | ePrint 2017/171 [V] | The budgeted view was the community's own framing in 2017; the expected-cost exponents came later |
| Dürmuth et al. (CANS 2021): quantum password guessing, cost = number of hash calls, **"ignored their individual run times"**. Square-root speedups. "Further research is necessary to focus on the quantum-hardness of memory-hard password hash functions" | ePrint 2021/1299 [V] | No depth or wall-clock analysis exists for quantum password guessing |
| NAP 2019 Table 4.1: password hashing (PBKDF2, 10,000 iterations, 66-bit), 2,403 logical / 2.23×10⁶ physical qubits, **2.3×10⁷ years** (surface code, 10⁻⁵ errors, 200 ns gates; from Mosca–Gheorghiu 2018) | nationalacademies.org [V] | "Grover can't crack stretched random passwords" is already on record, so v1's G1/G2 headline is weak |
| Bindel–Bonnetain–Tiepelt–Virdia (CRYPTO 2024): **quantum lattice enumeration in limited depth** | ePrint 2023/1423 [S] | Precedent: a "limited depth" re-analysis of a quantum speedup is accepted at top venues. Q★1 is the same move for guessing with advice |
| Blanc–Docter–Strassle–Tan (arXiv 2608.19158, Aug 2026): every t-query d-round quantum algorithm can be simulated classically with t^O(d²) queries on most inputs. **"Superpolynomial speedups would require quantum circuits of superconstant depth"** | [S] | Complexity-theory support: big unstructured speedups need depth. Q★1 is its concrete cryptographic version |
| NCSC (NIST PQC 2024): MAXDEPTH 2⁴⁸ = **8.92 years at a 1 µs logical cycle**, 3.26 days at 1 ns | [S] | Realistic MAXDEPTH is 2⁴⁰–2⁴⁸ (days to years at µs cycles). 2⁶⁴ means ~585,000 years at 1 µs |
| Local `Papers/`: Mandal et al. (Sci. Rep. 2024) Grover oracles for AEGIS/Rocca-S/Tiaoxin: full depth **10,190–17,038**, width 6,496–14,880 | [V] | A cipher-sized oracle has depth ≈ 2¹³–2¹⁴, so k = MAXDEPTH/D ≈ 2²⁶ at 2⁴⁰. These are the k values used in §2.2 |
| Bernstein 2009 (in `Papers/`): the "2^(b/3) quantum collision" belief "rests on a nonsensical notion of cost" | [V] | Q★1 is the same kind of correction for guessing. Your faculty already gave you the template paper |

---

## 2. Q★1 (core): does super-quadratic quantum guessing survive real constraints?

### 2.1 The fixed-budget sandwich [I]: a derivation, check it yourself

**Setup:** a secret x is drawn from a prior p₁ ≥ p₂ ≥ …. Let λ(B) = p₁ + … + p_B (the classical success with B guesses), and let B_α be the classical budget for success α.

**Upper bound (no quantum algorithm does better):**
1. Zalka (1999) proved Grover optimal for the *average* success over a uniformly random target [K]. So for any T-query algorithm, the per-target success probabilities sₓ satisfy Σₓ sₓ ≤ N·sin²((2T+1)·asin(1/√N)) ≤ (2T+1)².
2. The success under prior p is Σ pₓ sₓ, with 0 ≤ sₓ ≤ 1 and Σ sₓ ≤ (2T+1)².
3. The best allocation is greedy (a fractional knapsack). So **success ≤ λ((2T+1)²)**.

**Lower bound (an algorithm that achieves it):** Grover over the B_α likeliest keys reaches success ≈ α after ≈ (π/4)√B_α queries. He–Zhang–Sun's optimal state is never worse.

**Result:** **(√B_α − 1)/2 ≤ T_α ≤ (π/4)√B_α + 1, for every prior and every α.** The quantum discount is a square root, within a factor of about 1.6, with no dependence on the skew.

**Check against the published examples** (`grover_guessing_checks.py`, part 1) [E]:

| Prior | Moment exponent s | Success | Classical B_α | Quantum needs | "B_α^(1/s)" predicts |
|---|---|---|---|---|---|
| Zipf LinkedIn (N = 1.6×10⁸, a = 0.777), GMN's model | 2.08 | 0.5 | 2²²·⁹ | 2¹⁰·⁴ – 2¹¹·¹ | 2¹¹·⁰ (fine: s ≈ 2) |
| Bernoulli key bits, n = 256, p = 0.05 | 2.51 | 0.5 | 2⁶⁸·⁷ | 2³³·⁴ – 2³⁴·⁰ | **2²⁷·⁴, below the minimum by 2⁶** |
| same | 2.51 | 0.9 | 2⁸⁶·⁸ | 2⁴²·⁴ – 2⁴³·¹ | **2³⁴·⁶, below by 2⁷·⁸** |
| Bernoulli, n = 256, p = 0.01 | 3.23 | 0.9 | 2³¹·⁰ | 2¹⁴·⁵ – 2¹⁵·² | **2⁹·⁶, below by 2⁴·⁹** |

**Plain words:**
- The expected classical cost is dominated by very rare keys that no attacker would ever pay for. For example, E[G] = 2¹²⁸·⁸ while the 90% budget is only 2⁸⁶·⁸.
- The "super-quadratic" exponent compares two different tails. It is not a speedup at any fixed success level.
- This is Bonneau's (IEEE S&P 2012) critique of guessing entropy [K], carried over to the quantum setting.

### 2.2 The depth cap [I + E]

**The model:**
- One Grover run may make at most k sequential oracle calls, with k = MAXDEPTH / depth per iteration.
- A key of rank G ≤ k² costs ~√G queries.
- A key with G > k² needs ~G/k² parallel runs of k calls each, so ~G/k queries.

**The open part:** a matching lower bound for parallel/depth-limited search *with a prior*. It is plausible from Zalka's parallel bound and Jeffery–Magniez–de Wolf (2017, parallel query complexity) [K], but **I have not seen it proved for priors**. Proving it is part of Q★1.

Expected-cost exponent log E[G] / log E[cost_k] (`grover_guessing_checks.py`, part 2) [E]:

| Prior (classical E[G]) | k = 2⁸ | 2¹⁶ | **2²⁶** | 2³² | **2⁵⁰** | **2⁸²** | unlimited |
|---|---|---|---|---|---|---|---|
| Zipf LinkedIn (2²⁴·⁸) | 1.48 | 2.08 | 2.08 | 2.08 | 2.08 | 2.08 | 2.08 |
| Bernoulli p = 0.05 (2¹²⁸·⁸) | 1.07 | 1.14 | **1.25** | 1.33 | **1.63** | 2.51 | 2.51 |
| Bernoulli p = 0.01 (2⁶²·³) | 1.15 | 1.35 | **1.72** | 2.06 | **3.23** | 3.23 | 3.23 |

**How to read the k columns:** with a cipher-sized oracle (depth ≈ 2¹⁴), k = 2²⁶ / 2⁵⁰ / 2⁸² corresponds to MAXDEPTH 2⁴⁰ / 2⁶⁴ / 2⁹⁶.

**Plain words:**
- Super-quadratic gains live in the tail, where Grover runs are longest. So the tail is the **first** thing a depth limit cuts.
- They survive only when k² covers the ranks that dominate E[G]. In the table that holds for the small problem (2⁶² expected) with deep runs, but not for the large one at any realistic depth.
- **Passwords are the opposite case:** the prior is mild, but the oracle (the KDF) is very deep, so k is tiny. See A1.

### 2.3 The research questions

- **RQ1 (budget).** Prove the sandwich of §2.1 rigorously, including adaptive algorithms and unknown numbers of solutions. Quantify the overstatement Δ(α) for every prior used in GMN (Kyber's centered binomial, LPN, Zipf) and in Schubert et al. (cold boot, template attacks, Keccak SCA on ML-KEM/ML-DSA).
- **RQ2 (depth and parallelism).** Prove matching upper and lower bounds for depth-capped expected cost with a prior. Find the threshold k*(p) above which s > 2 survives. Draw the **phase diagram (skew × problem size × MAXDEPTH) → {sub-quadratic, quadratic, super-quadratic}**. Recompute every published example at MAXDEPTH ∈ {2⁴⁰, 2⁴⁸, 2⁶⁴, 2⁹⁶}, using real oracle depths (AES, Keccak, ML-KEM decapsulation check, KDFs).
- **RQ3 (synthesis).** Give a one-page "quantum discount" recipe: which number an evaluator should report for a leaked key, a password or an LWE secret, under which attacker model. Also answer when, if ever, expected cost is the right metric (see O3).

**Why this is not an afternoon calculation** (the lesson from OLD IDEAS doc 1):
- My script uses toy priors and continuous approximations, and assumes the depth-capped lower bound.
- The paper needs:
  - a real lower-bound proof with priors (RQ2);
  - exact computation for the published, non-toy priors (Kyber over many coordinates; real template posteriors, e.g. from the public ASCAD dataset);
  - real oracle and loader depths (Q★2);
  - the phase diagram.
- **The afternoon bracket only tells you the project is worth starting. That is what a week-1 bracket is for.**

### 2.4 What each outcome means

- **Every security-relevant case collapses below 2 under realistic MAXDEPTH:** "super-quadratic quantum guessing is a sequential-depth artefact". This corrects how GMN/Schubert-style exponents are quoted in lattice-hybrid and side-channel security claims.
- **Some cases survive** (e.g. moderate-rank, strongly skewed leakage): the first operationally real super-quadratic quantum cryptanalysis, with the exact conditions. Evaluators would then know where to worry.
- **The lower bound turns out false** (some clever parallel strategy beats G/k): a new quantum algorithm for depth-limited prior search. That is also notable.

### 2.5 Critic's pass (the OLD IDEAS "idea assassin" protocol, run on myself)

- **Semantic disguise.** Without the vocabulary, Q★1 is "Zalka's optimality and parallel Grover, plus Bonneau's critique of guessing entropy, applied to Montanaro's algorithm". The mechanisms are known. The contribution is the **load-bearing application** (correcting live 2025–2026 claims), the **depth-limited lower bound with priors**, and the **phase diagram**. That is the "known mechanism + new, load-bearing application" pattern the doc-4 critic accepted, and the same pattern as Bindel et al. (CRYPTO 2024) for lattice enumeration.
- **So what (who acts?).**
  - Authors and users of super-quadratic exponents: GMN note their multi-key algorithm "already found application in a recent lattice-based hybrid attack" [V].
  - Side-channel evaluators of ML-KEM/ML-DSA, which is Schubert's stated application.
  - Anyone writing "quantum halves password entropy" guidance.
  - Strength: moderate to strong. It changes how numbers are reported. It does not break a standard.
- **Pre-mortem.**
  1. **"Folklore."** A referee says the budget case is obvious. Mitigation: the depth-limited lower bound with priors is not obvious, and neither is the recomputed table or the phase diagram. Lead with those and keep §2.1 as a lemma.
  2. **Scoop.** The Bochum (May) or Berlin (Seifert/Margraf) groups add a depth section. Mitigation: post an ePrint within ~8 weeks of starting.
  3. **The published cases are all small.** Then nothing collapses and the paper becomes the "positive region" result. Still publishable, but weaker.
  4. **The lower-bound proof stalls.** Fall back to upper bounds plus numerical evidence and state the lower bound as a conjecture (O1).
- **Verdict:** **[PROCEED WITH CAUTION].** Run the week-1 kill test (§8) before committing.

**Difficulty:** medium. Probability theory, Grover analysis and careful numerics. One mathematically comfortable member is needed for RQ2.

**Possible venues (check SJR quartiles yourself) [K]:**
- IEEE TIFS
- Designs, Codes and Cryptography
- Quantum
- IACR Communications in Cryptology (fast and open; quartile unknown)
- Journal of Cryptology (stretch)

---

## 3. Q★2 (core, algorithmic): the loader problem

**What it is (plain words):**
- Amplitude amplification with a prior starts from a state Σ√qₓ|x⟩ prepared by a circuit A.
- **Every Grover iteration applies A and A† once more.** So per-iteration depth = oracle + 2·loader. A deep loader shrinks k and costs speedup.
- Classical crackers generate candidates almost for free (priority queues on a GPU). **Quantum attackers must do it coherently, every iteration.**

**What exists:**
- **GMN** assume black-box GetKey_D [V].
- **Martin et al. 2017** build coherent enumeration for *product* priors using **QRAM** [V].
- **JRC (ePrint 2026/2085)** loads a toy dictionary with generic state preparation, costing up to ~2ⁿ gates [V, v1].
- **He–Zhang–Sun** give the optimal qₓ but not a circuit for structured priors [V].

**First numbers** (`grover_guessing_checks.py`, part 3; Zipf N = 2×10⁵, success probability) [E]:

| Queries T | Classical | Tilted state qₓ ∝ pₓ^a (product form: cheap for Markov/product priors) | Uniform over top-K (needs coherent ranking) | He–Zhang–Sun optimum |
|---|---|---|---|---|
| 3 | 0.031 | 0.052 (61%) | 0.081 (95%) | 0.086 |
| 30 | 0.088 | 0.190 (59%) | 0.306 (95%) | 0.322 |
| 300 | 0.188 | 0.960 (98%) | 0.952 (97%) | 0.978 |

At T = 300 the budget covers almost the whole support, so all states converge. With N = 10⁶ the tilted state reached 76% at T = 300 [E].

**Reading:**
- The cheap tilted state loses roughly 40% at realistic budgets.
- The near-optimal top-K state needs a coherent ranker, which nobody has built for Markov/PCFG models.

**Research questions:**
- **RQ4.** For Markov (OMEN-style) and PCFG password models, and for product posteriors *without* QRAM, what is the cheapest loader (depth, T-count, qubits) within a constant factor of the He–Zhang–Sun optimum? Candidate building blocks [I]:
  - tilted chains via conditional rotations, normalized with transfer-matrix or backward-DP partition functions;
  - a coherent log-probability threshold ("pₓ ≥ τ") plus amplitude amplification onto that set;
  - a hybrid "explicit top-L list in QROM + tilted tail".
- **RQ5.** When does the loader cost more than the oracle? Expectation [I]: negligible against slow KDFs, dominant against fast hashes (NTLM/MD4, unsalted SHA-1). If so, prior-weighted quantum search may be *worse* than plain Grover over a mask for fast hashes. That would be a surprising and citable result.

**Difficulty:** medium-high (reversible circuits, dynamic programming). This is the most "builder" part. It is the natural home for the team member who likes algorithms.

---

## 4. A1 (application, the faculty's scenario): passwords, priced honestly

### 4.1 Quantum guess numbers come for free [I]

By §2.1, a password's quantum guess number lies between ½√G and (π/4)√G, where G is its classical guess number.
- Classical guess numbers already exist at scale: Monte Carlo strength estimation (Dell'Amico & Filippone, CCS 2015) [K], and the zxcvbn-style meters.
- **So a "quantum-aware strength meter" (v1 G3's promised output) is a square root of what we already compute.** Say this explicitly in the thesis. It is a useful negative and saves everyone the work.

### 4.2 The depth defence: key stretching caps Grover at ~k [I]

**The rule:**
- k = MAXDEPTH / D_iter, where D_iter ≈ 2·D_KDF + 2·D_loader.
- Quantum guessing saves at most a factor ≈ k in oracle calls (§2.2), *before* paying the fault-tolerance premium per call.
- Under a depth limit, total quantum cost grows like D² (the standard N·D²·W / MAXDEPTH form for parallel Grover; Jaques et al. 2020 [K]), while classical cost grows like D. **So stretching hurts a Grover attacker quadratically.**

**Rough numbers [I]** (order of magnitude only; assumes ≈2¹³ depth per SHA-1/SHA-256 compression, from ePrint 2025/1415's SHA-1: 985 qubits, depth 9,026 [S]):

| Target | Sequential work | D_iter (≈) | k at MAXDEPTH 2⁴⁰ | k at 2⁴⁸ (~9 years at 1 µs) |
|---|---|---|---|---|
| NTLM (MD4, unsalted) | 1 block | 2¹²–2¹³ | ~2²⁷ | ~2³⁵ |
| WPA2-PSK (PBKDF2-HMAC-SHA1, 4096 iterations, 2 blocks) | ~2¹⁴ compressions | ~2²⁸ | ~2¹² | ~2²⁰ |
| PBKDF2-HMAC-SHA256, 600,000 iterations (OWASP) | ~2²⁰ compressions | ~2³⁴⁺ (plus a reversible-pebbling overhead, Blocki–Holman–Lee 2022) | **~2⁶** | ~2¹⁴ |
| bcrypt cost 12 | ~2²⁶ Blowfish rounds, each with password-dependent S-box reads (QRAQM) | ≳ 2³¹ | ≲ 2⁹ | ≲ 2¹⁷ |
| scrypt N = 2¹⁷ / Argon2id (OWASP) | ~2¹⁸ block ops + data-dependent reads | ≳ 2³⁰, plus 2³⁰ qubits of memory | ≲ 2¹⁰ | ≲ 2¹⁸ |

**Message to test:** for stretched passwords, depth (iterations, wall-clock) is the Grover defence and memory is secondary. The speedup is capped at ~2⁶–2¹⁸ even with a decade-long run, and each quantum oracle call costs vastly more than a GPU hash. **The only plausible quantum exposure is fast, unsalted hashes (NTLM) attacked over very long horizons.** Price exactly that window. The economic framing is Harsha–Blocki (WEIS 2020) [S] plus Babbush et al. (PRX Quantum 2021, "Focus beyond quadratic speedups") [S].

### 4.3 The parts of v1 G1/G2 that remain genuinely unpriced

- **Data-dependent memory (scrypt, Argon2id, bcrypt):** each read needs QRAQM (quantum addresses, quantum data).
  - Under gate count, a circuit QRAM costs O(memory) gates per read. Argon2id is then ~m times costlier than Argon2i (data-independent) for a quantum attacker [I].
  - Under depth × width, the penalty is only ~log m [I].
  - Jaques–Rattew (Quantum 9, 1922, 2025) argue that active QRAM erases most quantum advantage [S]. **This adds a third, quantum axis to the Argon2i/d/id choice.**
- **bcrypt has no quantum circuit at all** (searched again today [S]).
  - Its 4 KB state is overwritten in place, so it is irreversible. A reversible version must store history or recompute.
  - Its S-box reads are password-dependent (QRAQM).
- **Formats (v1 G5):** archives, LUKS2/VeraCrypt, KeePass/Bitwarden, BIP-39 passphrases, WPA2. Each is "AES-256, but only as quantum-safe as its KDF and password". Make it a table in the thesis, not a paper.

**Ethics:** use published frequency lists or models trained on public research datasets, ask your faculty about approval, and never use live credentials.

---

## 5. A2 (application): leakage-assisted key search under depth limits

- **Object:** side-channel posteriors (template attacks; the public ASCAD dataset), cold-boot priors (AES keys, ML-KEM seeds), and Keccak-SCA residual ranks on ML-KEM/ML-DSA. These are the cases Schubert et al. compute.
- **Task:**
  - Report **budgeted** quantum residual security (the √ of the classical rank curve, §2.1).
  - Report the **depth-capped expected cost** (§2.2) with real oracle depths: AES ≈ 2¹²–2¹⁴; Keccak-f[1600] and an ML-KEM re-encryption check are deeper, so k is smaller.
- **Dependent priors:** cold-boot leakage is coupled through the AES key schedule, so it is not a product prior. GMN and Schubert both exclude this case [V]. Under the budget metric you only need the classical rank curve. Computing that curve for dependent leakage is a known classical problem, which is easier than v1's G4.
- **Who acts:** certification labs (FIPS 140-3 / Common Criteria side-channel testing of PQC implementations) and the PQC side-channel literature.

---

## 6. T (instrument, the faculty's "structural change to a toy system"): a prior-advised, depth-capped toy benchmark

- **Build:**
  - a toy keyed check (a 4-bit S-box toy cipher, or JRC's Keccak-f[25]);
  - a toy prior: either i.i.d. skewed key bits, or a 2-gram Markov "password" over 3–4 symbols × 4 positions;
  - three loaders: Hadamard (uniform), tilted (conditional RY rotations), and top-K (with a coherent comparator).
- **Simulate exactly in Qiskit (≤ ~22 qubits)** and check:
  - the success curves against He–Zhang–Sun's formula;
  - the §2.1 sandwich;
  - the depth-capped strategies of §2.2;
  - the loader gate counts (Q★2);
  - that every ancilla is cleanly uncomputed (the doc-6 lesson).
- **The structural knobs** (prior skew, loader type, depth cap, number of parallel machines) *are* the "new toy model" the faculty asked for.
- **It is the instrument, not the result.** That keeps you out of the killed "Grover resource estimate for toy cipher X" genre.
- **Starting point:** `Learning Files/learning_exercises/ex1_grover.py` and `ex3_prior.py` already exist.

---

## 7. Hard open problems: I do not know the way out

These are stated precisely so you can study them. Any one of them, solved, is a strong result by itself.

**O1. Optimal depth-limited search with a prior.**
- **Question:** given a prior p, P parallel machines and at most k queries per machine, what is the exact maximum success probability, and which states and allocation achieve it?
- **What I believe:** "top-K per machine" is near-optimal, but there is no proof.
- **Known pieces:** Zalka (exact for uniform, one machine), He–Zhang–Sun (exact for a prior, one machine), parallel query lower bounds (Jeffery–Magniez–de Wolf).
- **Missing:** the combination. The polynomial or adversary method with a prior is the likely tool.

**O2. A computational vs information-theoretic gap for loaders.**
- **Question:** is there a poly-size circuit family that gets within a constant factor of He–Zhang–Sun's optimum for *every* Markov prior? Or does near-optimality require something like coherent ranking, which may be #P-hard in general (counting strings likelier than x)?
- **Either answer is notable:** a poly-size family would be a new loader construction; a hardness result would show a real gap between computational and information-theoretic quantum guessing.

**O3. Which cost does a rational attacker actually minimize?**
- **Question:** expected cost (where s > 2 lives), budgeted success (exactly quadratic), or cost per success over many targets (GMN multi-key: quadratic)? Is there *any* natural cryptographic attacker model where the expected-cost exponent is the decision-relevant number?
- **Why it matters:** if not, super-quadratic guessing speedups are a measurement artefact, not a threat model.
- **Starting point:** formalize with Harsha–Blocki's economic model.

**O4. Quantum memory-hardness in the QROM.**
- **Question:** prove that any quantum circuit evaluating scrypt or Argon2i on a superposition of passwords needs cumulative qubit-memory × time Ω(n²)/polylog.
- **Known pieces:**
  - the classical proof (scrypt is maximally memory-hard, Alwen et al. EUROCRYPT 2017 [K]);
  - quantum cumulative-memory lower bounds for sorting and collisions (Beame–Kornerup ICALP 2023 [S]);
  - quantum sequentiality of hash chains (Chung–Fehr–Huang–Liao EUROCRYPT 2021 [S]);
  - parallel reversible pebbling (Blocki–Holman–Lee TCC 2022 [V]). It is a *model*, not a QROM proof.
- **Difficulty:** hard, TCC/CRYPTO-level theory. **Only attempt it with strong maths support.**

**O5. Does data-dependence change the Argon2 recommendation for quantum attackers?**
- **Question:** under the active-QRAM cost model (Jaques–Rattew), is Argon2id asymptotically costlier to Grover than Argon2i, while classically Argon2i is the weaker one against time-memory trade-offs?
- **Difficulty:** moderate and concrete, a good master's sub-question.

**O6 (demoted v1 G4). Exact finite-size exponents for Markov priors.**
- **Method:** Schubert's method with tilted transfer matrices (Malone–Sullivan 2004 [K]).
- **Why demoted:** solvable, but it computes the moment exponent, which §2 argues is the wrong security metric. Do it only as a theory exercise, or redo it for budget curves.

---

## 8. Kill tests before committing (2 weeks)

| Week | Test | Continue if… | Stop or reshape if… |
|---|---|---|---|
| 1 | **Recompute Schubert et al.'s published cases** at MAXDEPTH 2⁴⁰ / 2⁴⁸ / 2⁶⁴ with oracle depth 2¹²–2¹⁴. Get their exact parameters from the arXiv HTML | Some exponents fall below 2 at realistic MAXDEPTH, *or* some clearly survive (then you write the "positive region" version) | All their cases are so small that the cap never binds *and* nothing interesting survives. Then lead with Q★2 + A2 |
| 1 | **Check §2.1 against the sources:** Zalka's exact statement (average success, adaptive algorithms); whether He–Zhang–Sun appeared in a journal; Google Scholar "cited by" for He–Zhang–Sun and GMN, to see whether anyone already connected them | Nobody states the budget sandwich against GMN/Schubert | It is published. Cite it and lead with RQ2 (depth) and the phase diagram, which are still open |
| 1 | **Read GMN's Kyber/LPN section:** which metric does the lattice-hybrid application [KKNM25] use, and how large are the guessed parts? | The hybrid uses expected-cost exponents at sizes where k binds | The guessed parts are tiny. Drop the Kyber angle and keep passwords + leakage |
| 2 | **Toy prototype (T):** a 10–14-qubit prior-advised search with tilted vs top-K loaders. Check the He–Zhang–Sun formula against simulation | It matches | Debug; shrink the toy |
| 2 | **Faculty memo (2 pages):** the §2 tables, the 2.51 → 1.25 collapse, and the password depth defence (§4.2) | The faculty accepts "Grover with priors and limits" as the Grover thesis | Fall back to A1 as the core (v1 plan, with the honest framing of §0) |

**Unresolved reference:** Schubert et al. credit the entropy bound to "Bashiri et al. (2026)", which I could not resolve. It may be GMN under another name, or a separate paper. Find it in week 1; it may be closer prior work.

---

## 9. How it fits together, timeline and publication plan

```
            THE PRIOR (how guessable)                    THE ORACLE (how deep / wide per guess)
   Q★1 budget + depth: is s > 2 real?   ◄───────┐   ┌──►  A1 KDFs: depth caps k; memory/QRAQM (O5)
   Q★2 loader: cost of preparing the prior ──────┤   │     A2 cipher / Keccak / ML-KEM check depths
   O1 optimal depth-limited search, O2 loaders  ▼   ▼
              phase diagram: where is quantum guessing sub-quadratic / quadratic / super-quadratic?
                                               │
              A1 passwords (faculty) · A2 leakage (side-channel / cold boot) · Kyber/LPN check
                                               │
              T: exact Qiskit toy model (prior × loader × depth cap) validates every formula
```

**Plan [I]:**
- **Months 1–2:** RQ1 + RQ2 proofs; recompute the published cases; the phase diagram. **Post an ePrint early.**
- **Month 3:** Q★2 loaders for Markov/PCFG + the toy model (T).
- **Month 4:** A1 (passwords: guess numbers, depth defence, the NTLM window) + A2 (ASCAD / cold boot).
- **Months 5–6:** write.
  - **Paper 1:** Q★1 (+ Q★2 numbers). Target IEEE TIFS, DCC or Quantum.
  - **Paper 2:** A1 + T, "What Grover can and cannot do to passwords". Target Computers & Security or IEEE TDSC.
- **Thesis:** both papers + A2 + the format table.

**Faculty mapping:**

| Faculty ask | Where |
|---|---|
| "Work on/around Grover" | Everything is Grover / amplitude amplification with priors, limits and costs |
| "Password cracking scenarios" | A1. Also: the theory (Q★1) is exactly about guessing human-chosen secrets |
| "Defence mechanisms" | The depth defence (§4.2): key stretching caps Grover; the quantum axis of Argon2i/id (O5); quantum-aware reporting rules (RQ3) |
| "Structural changes to toy systems → new model" | T: the prior-advised, depth-capped toy benchmark |
| "AES-256 is safer" | A1 and A2: AES-256 is only as Grover-safe as the password or leakage behind its key. And Grover against the key itself is impractical (NCSC 2024, NAP 2019) |

---

## 10. Occupied areas (don't go there; checked)

| Area | Who already did it |
|---|---|
| "Grover on cipher X" resource estimates | Large literature: the Hansung/Seo group (ASCON, KLEIN 2026, Argon2 G, scrypt Salsa20/8, …), GFSPX (Phys. Scr. 2026), the AEAD paper in `Papers/`, MIBS (ePrint 2025/2090), SHA-1 (ePrint 2025/1415). Killed in OLD IDEAS |
| AES Grover cost models, MAXDEPTH, fault-tolerant cost | Jaques et al. EUROCRYPT 2020; NCSC 2024; Harsha–Blocki 2020 (economic) |
| Fault-tolerant Grover for mining | Dallaire-Demers / BTQ, arXiv 2603.25519 (2026) |
| "Grover can't crack stretched random passwords" | NAP 2019, Table 4.1 (Mosca–Gheorghiu 2018 data) |
| Grover under noise / dirty oracles | Reitzner–Hillery 2019; Vrana et al. 2014; Biham et al. 1999. Killed in OLD IDEAS |
| Quantum password guessing (hash-call cost), multi-user | Dürmuth et al., CANS 2021 |
| Super-quadratic exponents, product priors | GMN (ePrint 2023/797); Schubert et al. 2026. **Their depth/budget side is the open part, not their exponents** |
| Optimal fixed-budget search with a prior (single machine) | He–Zhang–Sun 2020 |
| Limited-depth quantum lattice enumeration | Bindel–Bonnetain–Tiepelt–Virdia, CRYPTO 2024 |
| "Quantum-annoying" PAKE | Eaton–Stebila 2021; Hhan 2023; SoK on PQC PAKEs 2025 |
| Reversible pebbling of data-independent MHFs | Blocki–Holman–Lee, TCC 2022 |
| QFT/Walsh linear key recovery | Active specialist race (ePrint 2026/2171; CAST). See `Path_2/` |

---

## 11. Lessons from OLD IDEAS that shaped v2

| Lesson | How v2 obeys it |
|---|---|
| "An answer you can bracket in an afternoon is not a thesis" | I bracketed v1's core and it mostly settled (§0). I also bracketed Q★1: the bracket *opens* questions (lower bound with priors, phase diagram, loaders) instead of closing them |
| "Correct, novel and inert" | Q★1 changes how live 2025–2026 numbers are reported. A1 gives a defence rule |
| Search the adjacent field's words | Found He–Zhang–Sun (quantum search with prior knowledge) and Blanc et al. (structure or depth) outside the crypto vocabulary |
| Don't mix units | MAXDEPTH and k are logical depth / iteration counts. Physical numbers appear only via NAP and NCSC, and are labelled |
| "Known mechanism + new, load-bearing application" is acceptable | Stated openly in §2.5 |
| Strawman risk | The claims are quoted from the papers [V]. Schubert *themselves* note the Jensen origin of s ≥ 2. Q★1 targets how s is *used*, not their mathematics |
| Treat "nobody is doing this" as an alarm | Checked the closest neighbours: Martin et al. (budgeted, quadratic), He–Zhang–Sun (single machine), Bindel et al. (lattices). The gap is the combination with priors, depth and the published super-quadratic cases |

---

## 12. Sources

**Read in this session [V]:**
- Glaser, May, Nowakowski, *Super-Quadratic Quantum Speed-ups and Guessing Many Likely Keys*: https://arxiv.org/abs/2509.06549 · https://eprint.iacr.org/2023/797
- Schubert, Paskarbeit, Kramer, Seifert, Margraf, *Pinpointing Super-Quadratic Quantum Enumeration Speedups* (23 Sept 2026): https://arxiv.org/abs/2609.28226
- He, Zhang, Sun, *Quantum Search with Prior Knowledge* (2020): https://arxiv.org/abs/2009.08721
- Martin, Montanaro, Oswald, Shepherd, *Quantum Key Search with Side Channel Advice* (SAC 2017): https://eprint.iacr.org/2017/171
- Dürmuth, Golla, Markert, May, Schlieper, *Towards Quantum Large-Scale Password Guessing on Real-World Distributions* (CANS 2021): https://eprint.iacr.org/2021/1299
- National Academies, *Quantum Computing: Progress and Prospects* (2019), ch. 4, Table 4.1: https://www.nationalacademies.org/read/25196/chapter/6
- Local `Papers/`: Bernstein 2009 (SHARCS); Mandal et al., Sci. Rep. 2024 (AEAD Grover); Ulgen et al., Phys. Scr. 2026 (GFSPX); Kiran et al., npj QI 2026 (SPN); Wang et al., npj QI 2025 (S-AES); Chen et al., arXiv 2503.06097 (AES S-box); two Shor/ECC papers (not Grover)

**Read in the v1 session [V, v1]:**
- Song et al., Argon2 circuits (ePrint 2023/1150)
- Song & Seo, *Grover on Scrypt* (Electronics 2024)
- Chenu & Chizzini (JRC), Keccak-f[25] (ePrint 2026/2085): https://eprint.iacr.org/2026/2085
- Blocki–Holman–Lee, TCC 2022: https://arxiv.org/abs/2110.04191 (abstract re-read today)

**Search or abstract level [S]:**
- Montanaro, *Quantum Search with Advice* (TQC 2010): https://arxiv.org/abs/0908.3066
- Bindel, Bonnetain, Tiepelt, Virdia, *Quantum Lattice Enumeration in Limited Depth* (CRYPTO 2024): https://eprint.iacr.org/2023/1423
- Blanc, Docter, Strassle, Tan, *Quantum Speedups Require Structure or Depth* (Aug 2026): https://arxiv.org/abs/2608.19158
- NCSC, *On the practical cost of Grover for AES key recovery* (NIST PQC 2024): https://csrc.nist.gov/csrc/media/Events/2024/fifth-pqc-standardization-conference/documents/papers/on-practical-cost-of-grover.pdf
- Dallaire-Demers et al., *Kardashev scale Quantum Computing for Bitcoin Mining* (2026): https://arxiv.org/abs/2603.25519
- Harsha & Blocki, *An Economic Model for Quantum Key-Recovery Attacks against Ideal Ciphers* (WEIS 2020): https://arxiv.org/abs/2005.05911
- Babbush et al., *Focus beyond quadratic speedups for error-corrected quantum advantage* (PRX Quantum 2021): https://arxiv.org/abs/2011.04149
- Cade, Folkertsma, Niesen, Weggemans, *Quantifying Grover speed-ups beyond asymptotic analysis* (Quantum 2023): https://quantum-journal.org/papers/q-2023-10-10-1133/
- Jaques & Rattew, *QRAM: A Survey and Critique* (Quantum 9, 1922, 2025): https://quantum-journal.org/papers/q-2025-12-02-1922/
- Chung, Fehr, Huang, Liao, *On the Compressed-Oracle Technique, and Post-Quantum Security of Proofs of Sequential Work* (EUROCRYPT 2021): https://eprint.iacr.org/2020/1305
- Beame & Kornerup, *Cumulative Memory Lower Bounds for Randomized and Quantum Computation* (ICALP 2023): https://arxiv.org/abs/2301.05680
- Blocki & Holman, data-dependent MHFs in the PROM (CRYPTO 2026): https://eprint.iacr.org/2026/1724
- *Quantum Implementation of SHA-1* (ePrint 2025/1415): https://eprint.iacr.org/2025/1415
- Eaton & Stebila, quantum-annoying PAKE: https://eprint.iacr.org/2021/696

**From memory, verify before citing [K]:**
- Zalka, *Grover's quantum searching algorithm is optimal*, PRA 60, 2746 (1999)
- Jeffery, Magniez, de Wolf, *Optimal parallel quantum query algorithms* (Algorithmica 2017)
- Bonneau, *The science of guessing* (IEEE S&P 2012)
- Arikan (IEEE TIT 1996)
- Malone & Sullivan, *Guesswork and entropy* (IEEE TIT 2004)
- Dell'Amico & Filippone, Monte Carlo strength evaluation (CCS 2015)
- Alwen et al., *Scrypt is maximally memory-hard* (EUROCRYPT 2017)
- Jaques, Naehrig, Roetteler, Virdia (EUROCRYPT 2020)
