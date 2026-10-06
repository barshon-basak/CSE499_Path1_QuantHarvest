# N1 Master Plan v3: "The Quantum Harvest Economics of a Mobile-First Financial Sector"

> **One-sentence contribution.** We define and measure a new security metric — the **harvest amortization factor** (how many recorded sessions one quantum key-recovery run would decrypt) — build a **measurement-to-qubits cost model** that turns observed TLS deployment into a concrete per-session quantum attack price, instantiate both on the **mobile apps of a mobile-first, Android-dominated financial sector (Bangladesh)**, and **demonstrate the whole mechanism end-to-end at toy scale with real Shor and Grover circuits**.
>
> **Umbrella research question (RQ0).** *How cheaply could a future quantum adversary decrypt a mobile-first population's harvested app traffic, which deployment choices multiply or divide that cost, and does the deployed hybrid defence actually remove it?*
>
> **Why this file replaces v2.** v2 (`N1_Implementation_Plan.md`) was an excellent empirical study, but the supervisor's objection stands: *an assessment/empirical study alone is not a research contribution.* This version keeps every v2 measurement but re-centres the project on a **theory + metric + framework** (Part B) that the measurements *instantiate*, and a **demonstration** (Part D) that *realises* the mechanism with quantum algorithms. The empirical census becomes the **evaluation of a model**, not the contribution itself. It also folds in `N1_Field_Merge.md` (M1–M6) and `N1_Gap_Portfolio.md` (G1–G15), and corrects every claim the 60-paper literature synthesis flagged (`Literature_Review/Path1_Literature_Synthesis.md` §0.4).
>
> **Dates and verification.** Facts were checked for the synthesis on 6 Oct 2026. **(verify)** marks things an experiment or a re-search must confirm in the week you write them. Re-check all "first/novel" claims the week you submit.

---

## 0. How to use this file

| When | Read |
|---|---|
| **To understand the point** | Part A (the contribution) → Part B (the theory) |
| **Before building anything** | Part C (design) and Part D (toy) |
| **Every Monday** | Part H2 (timeline) and Part H4 (gates) |
| **When data surprises you** | Part H5 (which story the data tells) |
| **When writing** | Part G (papers, venues, claim ledger, related work) |

The thesis has three layers that map to the three contributions: **Measure → Price → Demonstrate**. One shared dataset, one thesis, up to three papers.

---

# PART A: THE CONTRIBUTION (why this is not "just an assessment")

## A1. The gap, stated precisely

The 60-paper synthesis exposes one seam that no paper crosses (synthesis §1.0, "the pattern across themes"):

- **The quantum-cost literature prices attacks precisely but never asks which real connections those prices apply to.** Shor on 256-bit ECC now costs ≈1,200–1,450 logical qubits and ≈7–9×10⁷ Toffoli gates (F06, F08); RSA-2048 needs <1M qubits in <1 week (F05); Grover on AES-128 costs ≈2⁹³–2¹¹⁷ gates under realistic depth limits (G02). None of these papers measures a single deployed connection.
- **The deployment-measurement literature measures real systems but never prices them in quantum terms.** A01/A02/A03 count hybrid adoption; E02/E05 measured key reuse (classically, pre-TLS 1.3); B01/B04 measured app TLS. Only one paper (E01) converts deployment into quantum cost — and it is **loopback-lab only, measures no real servers, ignores mobile and Grover-on-ticket-keys, and explicitly names its own open problem**: *"the economics of partial PQC deployment also deserve study: because TLS and SSH negotiate key-exchange parameters in cleartext, an adversary can discard quantum-resistant sessions and concentrate harvesting on the shrinking classical remainder."*

So the open problem is: **the harvest economics of a *real, partially migrated* ecosystem — the size of the "shrinking classical remainder", how deployment choices amplify or shrink the cost of attacking it, and whether the hybrid defence removes it — has never been measured, modelled, or demonstrated, and least of all for the mobile apps where a mobile-first economy's sensitive traffic actually flows.**

That is a *mechanism* question, not a *how-much-is-deployed* question. It is what lifts N1 above an assessment paper.

## A2. Research question and sub-questions

**RQ0 (umbrella).** How cheaply could a future quantum adversary decrypt a mobile-first population's harvested app traffic, which deployment choices multiply or divide that cost, and does the deployed hybrid defence actually remove it?

| ID | Sub-question | Answered by | Contribution |
|---|---|---|---|
| **RQ1** | Can the harvest cost of an ecosystem be expressed as a single, measurable quantity, and how does each deployment choice change it? | **Part B** (theory) | **C1**: the amortization-factor metric and its propositions |
| **RQ2** | What is the quantum attack cost per decrypted session for real measured connections, under current resource estimates? | **Part B5 + C2** | **C2**: the measurement-to-qubits cost model |
| **RQ3** | For Bangladeshi finance/government apps, how large is the classical remainder, which layer (platform, framework, SDK, server, hosting) decides it, and how large is the amortization factor in the wild? | **Part C** (measurement) | **C3**: the empirical instantiation |
| **RQ4** | Does the transcript-bound hybrid KEM provably and observably collapse the amortization factor to 1, even when the classical half is reused? | **Part B3 + C2 + D** | **C1/C4**: the neutralization result, measured and demonstrated |
| **RQ5** | Can the full harvest-now-decrypt-later chain — amplification by reuse and neutralization by hybrid — be realised end-to-end with real Shor and Grover circuits? | **Part D** (Toy-TLS) | **C4**: the demonstration |

Every sub-question is **two-sided**: each outcome is a publishable result (Part H5).

## A3. The four contributions and their novelty

| # | Contribution | Type | Precise novelty claim (re-verify before submitting) |
|---|---|---|---|
| **C1** | **The harvest amortization factor** A = sessions decrypted per quantum key-recovery run, with a cost model, a set of propositions linking each deployment variable to A, and a **neutralization theorem** for transcript-bound hybrids | **metric + small theory** | First *defined, measurable* amortization metric for the quantum-harvest setting. E01 models per-session cost but defines no reusable amortization metric and proves no neutralization result. E02/E04/E05 measure the underlying shortcuts only classically and pre-TLS-1.3. |
| **C2** | **Packets → qubits → sessions**: a pipeline that attaches published resource estimates to each measured connection and outputs cost-per-decrypted-session under three hardware scenarios | **framework / instrument** | First application of concrete quantum resource estimates to *measured, in-the-wild* connections. Industry "crypto-inventory" tools and conceptual banking papers assign quantum risk **without measurement**; E01 costs only a lab. |
| **C3** | **The classical remainder of a mobile-first financial sector**: first measurement of the amortization variables (key-share reuse, RSA key transport, psk_ke/0-RTT, ticket lifetime, hybrid coverage) in the TLS-1.3/hybrid era, and first for **mobile-app API hosts**, with full client×server layer attribution | **empirical evaluation of C1/C2** | First wild measurement of E01's "shrinking classical remainder"; first app-level PQ census in a mobile-first developing economy; first same-app iOS-vs-Android PQ comparison after iOS 26. |
| **C4** | **Toy-TLS**: an end-to-end harvest-now-decrypt-later model (toy ECDH + baby ML-KEM + S-AES) attacked with real Shor and Grover circuits, showing amplification-by-reuse and neutralization-by-hybrid | **toy model + algorithms** | First toy model to run the *complete* HNDL chain with real quantum algorithms **including** the hybrid defence and the reuse shortcut. (Shor on a 5-bit curve and Grover on S-AES exist separately; no one has joined them into a hybrid handshake with the amortization mechanism.) |

The empirical "firsts" (C3) are **supporting** novelty. The **headline** is C1+C2: a metric and a model the field can reuse, evaluated on a real ecosystem and demonstrated with algorithms. This is the difference between "we measured the app gap" and "we define how to price the harvest, measure it, and prove when the defence removes it."

## A4. Why this clears the Q1 bar (anticipating the reviewer)

Modelled on the N2 Q1-positioning exercise: the objections a Q1 reviewer raises, and how this plan answers each. (A Q1 target here means *Computers & Security* / *IEEE TIFS* / *ACM TOPS* / PoPETs for the main paper; see Part G3.)

| # | Likely objection | Answer built into this plan |
|---|---|---|
| W1 | "This is a measurement study; measurement studies are not contributions." | The contribution is the **metric and cost model** (C1/C2, Part B). The measurement (C3) *evaluates* them. The paper's claims are theorems and a reusable instrument, not a dataset. |
| W2 | "The theory is trivial — reuse obviously means one key opens many sessions." | The non-trivial parts are (a) the **neutralization theorem**: transcript-bound hybrid collapses A to 1 *even under classical-half reuse*, which follows from combiner robustness (D02 C2PRI; D01 CcQ) plus downgrade resistance (D05), not from the reuse observation; and (b) the **lifetime-weighted effective-exposure** formulation and its composition rules (Part B3). These turn a folk observation into a measurable, provable standard — the same move that lifts a correction into a contribution. |
| W3 | "Toy results don't scale; why should I believe the cost numbers?" | The cost numbers come from published, peer-reviewed resource estimates (F05/F06/F08/G02), reported as **ranges under three hardware scenarios**, never a single date. The toy (C4) demonstrates **mechanism**, not cost; the plan states this separation explicitly (Part D4). |
| W4 | "Fragmented into small papers." | One flagship paper = C1 + C2 + the C3 subset that evaluates them (Part G1). C3's platform-divide angle and C4's toy are separate papers only if they stand alone. |
| W5 | "Single country, single vantage; external validity?" | The **model (C1/C2) is country-independent**; Bangladesh is the evaluation case chosen because it maximises the phenomenon (91% Android, app-first finance). The empirical limits are stated; the framework travels. |
| W6 | "You can't run a real quantum attack, so where is the 'attack'?" | The attack is (a) priced for real connections from published circuits (C2) and (b) **executed** on the toy model in Qiskit with real Shor/Grover circuits (C4). The faculty's "attack + algorithms" requirement is met concretely. |
| W7 | "Isn't the reuse finding just a classical forward-secrecy bug?" | Classically it needs stolen server memory; quantumly it needs only recorded packets and one key-recovery run — a strictly different and larger threat. The plan reports **both views** and proves the quantum one is governed by A (Part B2). |

## A5. How this answers the faculty, word by word

| Faculty's word | Where this plan delivers it |
|---|---|
| **Attack** (Shor, Grover) | C2 prices Shor-ECDLP/factoring and MAXDEPTH-aware Grover for every measured connection; C4 runs both as real circuits on Toy-TLS. |
| **Defend** | C1's neutralization theorem and C3's hybrid-coverage measurement show *where* the hybrid defence works and *where the classical remainder survives*; G11 measures its cost on local networks. |
| **Mechanism** | The **amortization factor** is the mechanism: deployment shortcuts that turn one quantum run into many decrypted sessions (C1). |
| **Toy set / structural change to toy systems** | Toy-TLS = a structural composition of toy ECDH + baby ML-KEM + S-AES into a miniature TLS 1.3 (C4). |
| **Algorithms** | Shor-ECDLP and Grover circuits in Qiskit with resource counts (C4); the AES-S-box/S-AES/AEAD circuits from the faculty's own papers (G03–G06) feed the Grover cost model (M4). |
| *"AES-256 is safer (Grover)"* | M4/G15 tests this on real traffic with **MAXDEPTH-aware** costs (not the "128→64" slogan, which the synthesis shows is wrong, §0.4 #9), and reports it honestly as a supporting result: even AES-128 is far out of reach, so AES-256 is prudent policy (CNSA 2.0), not a present necessity. |
| *"Threat is real for RSA/ECC"* | The whole project is about the ECC (X25519/P-256) key exchange that Shor breaks and the migration to hybrid ML-KEM. |

## A6. Corrections carried over from the literature synthesis (do not repeat v2's errors)

These replace the corresponding "evidence facts" in v2 (`N1_Implementation_Plan.md` §A3). Full list: synthesis §0.4.

| v2 statement | Corrected statement to use |
|---|---|
| "IMC 2026 (A01) *explicitly excludes* mobile apps and API endpoints." | A01 **never mentions** apps; they are outside its design (Top-1M web domains, HTTPS, cloud vantage points, server-side). Say: *"its sample is web domains from cloud vantage points; client stacks, mobile apps and app back ends are outside its design."* |
| "Mobile traffic is ~52% TLS 1.3 and ~45% QUIC" (cited as general fact, E8). | This is **PARROT's** figure (B09): a *packet* share during *first launch* of 50 Vietnamese apps in an *emulator in Spain* with mitmproxy partly on. Not a population statistic. B08 found QUIC = 0.22% of flows. Cite B09 with its conditions; treat the QUIC share as **to be measured**, not assumed (synthesis Debate 2). |
| "AES-128 becomes 64-bit under Grover." | Under NIST MAXDEPTH, AES-128 key search ≈ 2⁹³–2¹¹⁷ gates (G02). Use MAXDEPTH-aware costs (M4). |
| Resource-estimate motivation leaned on RSA timelines (E06). | E06's experts answer about **RSA-2048 in <24 h**, which *understates* the key-exchange threat. Use F06/F08 (ECC-256) for key exchange and F05 for RSA; E06 only as a conservative proxy (synthesis Debate 8). |
| (v2 cited a 5-bit hardware "break" as momentum.) | Do **not** cite F12 (Tippeconnic) as progress: it runs index arithmetic mod 32, not EC arithmetic, and the key only appears in the top-100 of 1,024 outcomes (synthesis §0.4 #12, Debate 8). |
| Capture method under-specified about interception/QUIC. | **Capture without interception for key exchange** (mitmproxy terminates TLS at the proxy and suppresses QUIC — B09: only Instagram worked fully). Use interception only in a separate pinning pass. Capture **QUIC and IPv6** and parse QUIC Initial packets (synthesis §3.3(d), Debate 2; A09's blind spot). |
| Stats mostly descriptive. | Adopt A03-style statistics: Wilson CIs, **McNemar** for paired web-vs-API and iOS-vs-Android, logistic regression with **provider and sector predictors**, **HHI** for concentration (synthesis §3.3(b) rule 5). |

---
# PART B: THE THEORY — the harvest amortization model (contribution C1)

> This is the part that makes N1 a research paper rather than a survey. It is deliberately **modest and provable**, in the spirit of the N2 "reference bounds" upgrade: take a folk observation, define it precisely, prove how the measurable variables move it, and prove when the defence removes it. Everything here must be written up as definitions + propositions + one theorem, with the proofs either given or cited to D01/D02/D05/E01.

## B1. Definitions

- **Harvest unit (session).** One recorded TLS session's application data, identified on the wire by its handshake. Sessions linked by resumption form a **chain**.
- **Harvest value.** Each session *i* carries a weight *wᵢ* ≥ 0 for its sensitivity × data lifetime (Part C, G7). Lifetime classes follow E07's sector table and E01: payments/credentials ≈ 5–10 yr, identity/e-KYC and health ≫ 10 yr, telemetry < 1 yr. Short credential/API sessions are the highest-value-per-byte targets (E01).
- **Key-recovery run.** One execution of the cheapest quantum algorithm that yields a session's traffic key:
  - Shor-ECDLP on an (ephemeral or static) Curve25519/P-256 public value;
  - Shor-factoring on a certificate's RSA key (only where RSA key transport is used);
  - Grover on a symmetric key (a ticket STEK, or a record key) — in practice never the cheapest (C16), carried only for completeness.
- **Recoverable session.** A harvested session whose traffic key can be derived from the output of one or more key-recovery runs, given the adversary's recorded packets. By the neutralization theorem (B3), a session that negotiated a sound transcript-bound hybrid with a fresh ML-KEM encapsulation is **not** recoverable while ML-KEM stands (C17).

## B2. The amortization factor and the harvest-cost function

**Per-key amortization.** For a recovered key *x*, define
> **A(x) = number of distinct recoverable sessions whose traffic key is derived from the single run that recovers *x*.**

Ideal forward secrecy gives A(x) = 1 for every session. Shortcuts raise it (B3).

**Per-organization amortization.** Over a capture window, let 𝒮 be the harvested sessions of organization O, partitioned by the key each depends on. Let R(O) = number of distinct key-recovery runs needed to cover the **recoverable** subset 𝒮ᵣ ⊆ 𝒮. Then

> **A(O) = |𝒮ᵣ| / R(O)**  (mean recoverable sessions per run), and
> **weighted exposure** Xᵥ(O) = (Σ_{i∈𝒮ᵣ} wᵢ) / (Σ_{i∈𝒮} wᵢ)  — the lifetime-weighted fraction of O's harvest that is recoverable at all.

**Harvest cost (the C2 output).** Under hardware scenario *h* (B5), with per-run cost κ_alg,h (logical qubits, Toffoli, depth, physical qubits, wall-clock — reported as a vector, and as a scalar "run-equivalents" for ranking):

> **Cost_h(O) = Σ_{runs r} κ_{alg(r),h}** , and **cost per decrypted session** = Cost_h(O) / |𝒮ᵣ|.

The amortization factor is exactly the divisor that a shortcut inflates: a server reusing one ECDH share across *r* harvested sessions pays **one** run to decrypt all *r*, so its cost per session falls by *r*. This is the number a bank and a cryptographer both understand.

**The policy figure (Bernstein-style, G07).** Plot the **defender's measured cost** of enabling the hybrid (median/p90 +ms, +bytes, +mJ on Bangladeshi networks; G11) against the **attacker's cost per decrypted session** it removes (Cost_h / |𝒮ᵣ|). One picture: "the defence costs X ms and Y bytes; the harvest it prevents costs Z run-equivalents per session, and A(O) sessions would otherwise fall per run."

## B3. Propositions (how each measurable variable moves A) and the neutralization theorem

Each proposition is elementary but must be stated and proved from the session-key derivation; together they are the reusable standard. Anchors in brackets.

- **P1 (fresh ephemeral).** If every session uses a freshly generated ephemeral (EC)DH share and psk_dhe_ke (or a full handshake), then A(x)=1 for all x. [E01 E=1 case]
- **P2 (ephemeral reuse).** If a server reuses one ephemeral share across *r* harvested full-handshake sessions, A=*r* for that share. [E02 15.5% ECDHE reuse; E05 22.9% P-256 reuse — both pre-TLS-1.3; **unmeasured for hybrid era** → C3]
- **P3 (RSA key transport).** Under TLS 1.2 RSA key transport with a certificate key used by *s* harvested sessions, one factoring run recovers all *s*; A=*s*, and *s* can span the whole certificate lifetime. [E01 TLS 1.2 case; A05 28.9% configs permit it — permitted ≠ negotiated → C3]
- **P4 (resumption without fresh exchange).** A psk_ke or 0-RTT chain of length *c* rooted at one full handshake contributes A=*c* to the root key; breaking the root opens the chain. psk_dhe_ke resumptions each reset to A=1. [E03; E01 cascade result; C06 resumption is the majority CDN mode]
- **P5 (KeyUpdate).** TLS 1.3 KeyUpdate is a deterministic HKDF chain, so it adds no new runs (E=1); it does **not** help the defender against a quantum harvester. [E01]
- **P6 (composition).** A composes multiplicatively across independent shortcuts applied to the same key material and additively across distinct keys; R(O) is the number of distinct recoverable keys after composition. [new, provable from the partition]
- **P7 (symmetric last resort).** Recovering a session via Grover on its record key or a ticket STEK costs ≈2⁹³–2¹¹⁷ gates (MAXDEPTH), dominating any Shor route by ≥17 orders of magnitude; hence alg(r) is Shor whenever a public-key path exists, and the STEK matters only through P4-style inheritance and *classical* theft, not as a cheap quantum target. [G02, C16; synthesis Debate 6]

**Theorem (neutralization).** *Let a session negotiate a transcript-bound hybrid KEM (X25519MLKEM768 in TLS 1.3) with a freshly generated ML-KEM encapsulation, and assume ML-KEM-768 remains IND-CCA secure (C17). Then no quantum run on any classical value — reused or static — makes the session recoverable: the session's contribution to 𝒮ᵣ is 0 and to R(O) is effectively ∞ (it is never recoverable by the priced attacks). Consequently classical-half reuse (P2) is irrelevant to the exposure of hybrid sessions; it only amplifies A for sessions that are classical or fell back to classical.*

*Proof sketch.* The traffic key derives from the combiner output, which is IND-CCA as long as either component is secure (D01 CcQ for the HNDL/"future-quantum" adversary; D02 C2PRI robustness of the X25519+ML-KEM construction; in TLS the transcript hash binds the ciphertexts). A Shor run recovers the X25519 secret but not the ML-KEM shared secret, so the combiner output is unrecovered. Transcript binding (Finished MAC; D05) prevents the adversary from having forced a classical-only session by stripping the PQ option, so "negotiated hybrid" is an on-wire-verifiable fact. ∎

**Three consequences that drive the measurement (Part C):**
1. **The exposure metric must be computed over the classical / classical-fallback subset only** (the "shrinking classical remainder", E01). Hybrid coverage of that subset is the single most important policy lever.
2. **RQ-M1c is answered:** measuring classical-half reuse is meaningful *only* for sessions that are classical; for hybrid sessions it is a non-finding by the theorem. Report reuse **split by hybrid vs classical** (synthesis §3.3(b) rule 9).
3. **Fallback is the live risk, not cryptographic downgrade.** TLS 1.3 blocks a forced downgrade (D05/E05), so the classical remainder comes from *legitimate* causes: client never offered PQ (platform/framework), HRR to X25519, server preference, library gaps, resumption of a classical session (synthesis T3, E07 §6.5). Each is measurable (Part C).

## B4. What must be proven vs assumed (honesty ledger for the theory)

| Statement | Status | How to defend it |
|---|---|---|
| P1–P6 | Provable from key derivation; elementary | Write full proofs; they are short |
| Neutralization theorem | Follows from D01/D02/D05 given C17 | Cite the combiner proofs; state the ML-KEM assumption as a named hypothesis, not a fact |
| ML-KEM stays secure | **Assumption** | Cite E07's cost model (break needs an undiscovered dimension collapse) and F06 (Regev/DQI open); mark as the one load-bearing assumption |
| Per-run κ numbers | **External**, scenario-dependent | Use published estimates with ranges (B5); never a single date |
| A(O) in the wild | **To be measured** (C3) | The empirical core |

## B5. The three hardware scenarios (sourced per-run costs)

Report every cost under all three; never collapse to one. (Numbers from the synthesis F/G groups; re-verify latest versions at write-up.)

| Scenario | Target primitive | Per-run cost (logical qubits; gates; physical; wall-clock) | Source |
|---|---|---|---|
| **S-fast** (superconducting/photonic, minutes/key) | 256-bit ECDLP (X25519, P-256) | ≈1,200–1,450 lq; ≤70–90 M Toffoli; <500k physical; ~18–23 min | F06 |
| **S-slow** (neutral-atom/ion, days–weeks/key) | 256-bit ECDLP | ~10,000–26,000 physical; ~10 days (F07) / ~19,397 ions, ~26 days (F08) | F07, F08 |
| **S-RSA** (factoring) | RSA-2048 | <1M physical; <1 week (F05); 20M/~8 h (F04) | F05, F04 |
| (context) space-optimised ECDLP | 256-bit ECDLP | 835 lq, ~2×10⁹ Toffoli | F09 |
| (Grover, supporting) | AES-128 / AES-256 key | 2⁸³–2¹¹⁷ / 2¹⁹⁰–2¹⁵¹ gates under MAXDEPTH 2⁹⁶–2⁴⁰ | G01, G02, G05 |

**Fast vs slow matters for the story:** slow-clock machines (days–weeks/key) make **high-A targets first** — a reused static key or an RSA cert key with A in the thousands is worth a 26-day run; a fresh per-session share (A=1) is not. So the amortization factor is not just a number, it is the **ranking of what falls first** (synthesis T5 point 3).

**Timeline framing (Mosca inequality, never a date).** Shelf-life + migration time > threat time ⇒ exposure (E06). Use finance shelf-lives (≥7–10 yr; E01, E07) and present the result under all three scenarios; do not predict Q-Day. Cite F05's stance: migrate "because I prefer security to not be contingent on progress being slow."

---

# PART C: RESEARCH DESIGN — the measurement that instantiates the model (contribution C3)

## C1. Measurement model and definitions

- **Unit:** one TLS/QUIC connection (one row from `n1_tools.py pcap`). Headline numbers use **first-party** connections; third parties feed the SDK analysis (G5).
- **Client offers PQ** = `client_offers_pq_keyshare = True`; `client_supports_pq_group` without a key share means PQ only via a retry.
- **Server accepts PQ** = captured `pq_negotiated = True`, or the `f2_starter.py` probe shows `pq_hybrid_handshake = ok`.
- **Per-app × device outcome** (`n1_tools.py analyze`): ✅ protected (offers+accepts); 🟠 server bottleneck (offers, not accepted); 🟠 app-side bottleneck (doesn't offer, server accepts); 🔴 both missing.
- **Layer attribution** for app-side bottlenecks: (1) lab (G1) says this framework×OS doesn't offer PQ → **framework/OS layer**; (2) lab says it does but the app doesn't → **app-config layer**; (3) framework not in the lab → **unknown**.
- **Always log both sides of the handshake** (synthesis A08 lesson): ClientHello offered groups + key_shares, ServerHello chosen group, HRR, PSK mode, cipher, TLS version, transport (TCP/QUIC), IP version.

## C2. The amortization variables and how each is measured (the corrected M1 table)

This operationalises Part B. Every variable is logged per connection or per host; A(O) and Cost_h(O) are then computed by the C2 pipeline.

| Variable (Part B) | What we measure | Tool / method | Corrected caveat |
|---|---|---|---|
| **P2 ephemeral reuse** | distinct server `key_share` values across *k* rapid handshakes; lifetime of each | `n1_tools.py shortcuts` (repeat handshakes, compare key_share) | Report **split by hybrid vs classical** (neutralization theorem). No prior hybrid-era data exists → this is the novel measurement. |
| **P3 RSA key transport** | whether apps *negotiate* it (not just whether servers permit it) | pcap cipher-suite column for what apps pick; `f2_starter.py` for what servers permit | A05's 28.9% is *permitted* in configs; the wild-negotiated rate is unknown → measure it. |
| **P4 resumption mode** | psk_ke vs psk_dhe_ke vs 0-RTT share; chain length | `psk_modes`, `resumption_offered/accepted` columns | No paper reports the psk_ke/psk_dhe_ke split for real clients (synthesis Debate 7) → novel. |
| **ticket lifetime (P4 root, classical theft)** | STEK key-name prefix over time | `openssl s_client -sess_out` + `sess_id -text` **(verify)** | STEK is a Grover target only in principle (P7); its real role is psk_ke inheritance + classical theft. |
| **hybrid coverage** | fraction of first-party sessions negotiating X25519MLKEM768 | pcap `pq_negotiated` | This is the **denominator** of the classical remainder; the key policy lever. |
| **fallback / HRR** | HRR to X25519; retry-without-PQ after failure; classical-only despite PQ-capable client | pcap `hello_retry`; repeated captures on lossy operators (G10) | The live risk per the theorem; E07 §6.5 left it out of scope. |
| **hosting / provider** | ASN, CDN vs cloud vs own network, per host | Team Cymru DNS; CNAME/PTR (A01/A03 attribution) | Explains A(O): CDNs give fresh keys + hybrid; own networks are where high A lives. |
| **data lifetime (wᵢ)** | flow step → lifetime class | session log (`flow_step`) + SNI | E07 sector shelf-lives; E01 value-per-byte. |

## C3. Sampling and the experiment matrix

- **Apps (~50):** mobile money (bKash, Nagad, Rocket, Upay), banks (12–15: CellFin, Astha, City Touch, EBL Skybanking, …), telecom self-care (MyGP, My Robi, MyBL), e-commerce/ride (Daraz, Chaldal, Pathao, Foodpanda), government/health. Inclusion: ≥100k downloads, Bangladesh-focused, handles personal/financial data. Verify every package, version, date. Optional 20 global apps for context.
- **Android devices:** real phones on **11/12** (old) and **15/16** (new) — Bangladesh's biggest versions (StatCounter); emulators 10–17 on **Google Play** images.
- **iOS subset (G3):** 1 iPhone on **iOS 26** (and iOS 18 if available), ~20 same-app pairs. This is the first post-iOS-26 same-app PQ comparison.
- **Networks:** Grameenphone, Robi, Banglalink, Teletalk mobile data; home broadband; campus Wi-Fi. Full campaign on 1 network; G10/G11 repeat a subset on all four operators.
- **Web↔API pairs (G8):** for each organization, pair its website host(s) with the API hosts seen in captures; probe both with `f2_starter.py`. This is the direct test of "web studies overestimate readiness."
- **Session protocol:** 5 min per app per device (stable after 5 min, B01); steps logged to `data/sessions.csv` to label `flow_step` without decryption. Background calibration: 30 min idle device to subtract OS traffic (B01).
- **Capture method:** PCAPdroid (per-app, no root) **or** laptop-hotspot + Wireshark. **No interception for key exchange** (synthesis correction). QUIC captured and parsed (`quic && tls.handshake.type == 1`); IPv6 included.

## C4. Hypotheses (pre-register before the big runs; two-sided)

| ID | Hypothesis (from synthesis §3.3(c)) | Falsified if | Then report |
|---|---|---|---|
| H1 (layer) | For the same app, hybrid share is explained more by client stack than by server support | server dominates | "servers, not clients, are the bottleneck" |
| H2 (platform) | iOS builds negotiate hybrid more than Android builds of the same app | no difference | "frameworks neutralize OS defaults" |
| H3 (API gap) | App API hosts negotiate hybrid less than the org's website; gap shrinks on shared CDN | APIs lead/equal | "web measurements represent apps" |
| H4 (SDK) | SDK connections lead first-party API connections | SDKs lag | "data leaks via side doors" |
| H5 (shortcuts) | Key reuse / RSA transport / psk_ke / long tickets are more frequent on owner-managed BD hosts than global CDNs | equal | "forward secrecy holds; attacker pays per session" |
| H6 (neutralization, the theorem's empirical check) | Where hybrid is negotiated, classical-half reuse does not raise exposure; it does for classical-fallback | reuse matters for hybrid too | a flaw in the combiner/transcript binding in the wild — a strong finding |
| H7 (cost) | Median hybrid overhead ≤15 ms on BD operators; heavier p95 tail and higher failure rate on lossy/low-end | much larger | network-specific bottlenecks (G10) |
| H8 (pinning hazard) | Most finance pins are CA-level; a minority are leaf/SPKI that PQ/MTC certs would break | pins rare/dynamic | "pinning won't block the PQ cert migration" |

## C5. Statistics (A03 as the template)

Wilson 95% CIs on every proportion; **McNemar** exact test for paired old-vs-new Android, iOS-vs-Android (G3), and website-vs-API (G8); **logistic regression** of PQ outcome on {client stack, OS version, sector, provider} with grouped cross-validation and reported AUC per predictor set (A03's provider-vs-sector AUC is the model to imitate); **HHI** for provider concentration; bootstrap CIs for latency (resample per-run times 1,000×). Report M per instance for reuse (number of distinct keys). ≥1,000 handshakes for headline reuse cells where feasible. Never report a sector cell with n < ~50 (A03 rule).

## C6. Ethics, legal and disclosure

- ✅ Own devices, own accounts only; read only unencrypted handshake metadata; no decryption, no MitM, no pinning bypass; a few handshakes per host for probes.
- ❌ No APK redistribution; no device IPs published; G2 survey / G14 interviews collect no IP (strip `ip=`) and need IRB.
- ✅ Disclose to affected providers (and BGD e-GOV CIRT for government apps) ≥60–90 days before publishing (Phase 9 template).
- ⚠️ **The private pilot finding** (a named institution's key-reuse pattern; see `N1_Field_Merge.md` §M1) stays out of all public artefacts until private disclosure, exactly as that file instructs. Keep probe outputs out of the public repo. Tell the faculty first. The synthesis file already excludes it; the papers must too until cleared.
- ✅ Show Parts A–C to the faculty before Phase 3.

---
# PART D: THE DEMONSTRATION — Toy-TLS (contribution C4)

> This is the faculty's "structural change to a toy system / new model / algorithms" requirement, bound to N1's measurements. It **demonstrates the mechanism** of Part B; it does **not** estimate real costs (those come from Part B5). Keep the two separate in writing.

## D1. Design

A miniature TLS 1.3 that keeps the real structure but uses toy-size pieces, run on a simulator (Qiskit, already installed).

```
 Client ──ClientHello ( toy-ECDH share  [+ baby-ML-KEM public key] )──▶ Server
        ◀─ServerHello ( toy-ECDH share  [+ baby-ML-KEM ciphertext]  )──
 transcript τ = all of the above
 key = KDF( label ‖ ECDH_secret [‖ ML-KEM_secret] ‖ H(τ) )   ← transcript-bound combiner (D05)
 records encrypted with S-AES (16-bit key)                    ← the faculty's npj oracle (G04), already in n2_tools.py
```

Pieces:
- **Toy ECDH:** a curve with group order ≈ 2⁴–2⁶ (the F13 ladder's low rungs, but with *real* EC arithmetic, unlike F12). Reuse F13's reproducible small-curve recipe so the toy is principled.
- **Baby ML-KEM:** FIPS-203 structure scaled down (small n, q), keeping the **FO transform** so the hybrid demonstration is faithful (D04). Do not use a toy so small the FO step disappears.
- **S-AES:** 16-bit record cipher from the faculty's npj paper (G04), already in `n2_tools.py`, with the 120-Toffoli Grover oracle.
- **Transcript-bound combiner:** key = KDF(… ‖ H(τ)) exactly as D05, so the toy can also demonstrate downgrade resistance.

## D2. The four runs (each produces resource counts + success probability)

| Run | What it shows | Algorithm | Expected outcome |
|---|---|---|---|
| **Attack 1 (harvest → decrypt, classical path)** | record a toy session, later recover the key | Shor-ECDLP on the toy curve → ECDH secret → KDF → read S-AES records | session decrypted; qubits/gates/depth grow with curve order |
| **Attack 2 (symmetric path)** | direct key search | Grover on S-AES (npj 120-Toffoli oracle) | session decrypted; confirms Grover is the dearer route even at toy scale (P7) |
| **Defence (neutralization, the theorem shown)** | hybrid blocks Attack 1 | run Shor on the classical half only | key **not** recovered (ML-KEM half unknown) → records stay locked |
| **Mechanism (amortization, M1 shown quantumly)** | reuse amplifies | reuse one toy-ECDH share across *r* toy sessions, run Shor **once** | all *r* sessions decrypt from one run → A = r, matching Part B2 |

Optional 5th run: strip the PQ option in-flight and show the transcript-bound KDF makes the Finished check fail (downgrade resistance, D05).

## D3. Outputs

- Per attack: logical qubits, Toffoli/T count, depth, success probability on a noisy simulator (optionally a few IBM-hardware shots).
- Scaling curves: cost vs curve order, cost vs S-AES rounds, A vs *r*.
- A single figure that overlays the **toy mechanism** (A=r; hybrid→locked) with the **real cost ranges** (Part B5) — the paper's bridge between demonstration and measurement.

## D4. Honest limits (state them in the paper)

- Toy sizes do **not** predict real costs; the toy shows **mechanisms** (reuse amplifies Shor; hybrid blocks it; Grover is dearer). Real costs come from Part B5's published estimates.
- Simulable scale is tiny; report what runs on a statevector/noisy simulator and what (if anything) ran on hardware.
- The baby ML-KEM is not ML-KEM-768; it demonstrates the *combiner structure*, not ML-KEM's security.
- No existing toy runs the full HNDL chain **with the hybrid defence and the reuse shortcut** together (verify at write-up); F12 is not a counterexample (it runs no EC arithmetic).

## D5. Reuse across the thesis

Any toy cipher from N2's family can replace S-AES as the record cipher — that is how a second team member's work joins the same thesis (shared `n2_tools.py`).

---

# PART E: THE JOURNEY (phases)

> Two semesters: CSE499A = weeks 0–12, CSE499B = weeks 13–24. Phases overlap. The order front-loads the **theory + lab + toy** (the contribution) so that even a weak measurement harvest still yields a contribution paper.

### Phase 0 (week 0–1): setup, baseline, theory draft, approval
1. Private repo: `captures/ apks/(git-ignored) data/ lab/ toy/ analysis/ paper/`.
2. Toolchain: Python ≥3.13 on OpenSSL ≥3.5 (`ssl.OPENSSL_VERSION`); Wireshark, Android Studio (adb + emulators), jadx, apktool, Qiskit. Run `python n1_tools.py selftest` and `timing cloudflare.com 20`.
3. **Baseline record** (`data/baseline.md`): each phone's Android version, patch, Play system-update date, WebView + Chrome versions; the iPhone's iOS version; today's date. (Enables the O1–O4 natural experiments.)
4. **Draft Part B as a 2-page note** (definitions + P1–P7 + theorem). This is the spine of the flagship paper; writing it now forces the contribution to be concrete.
5. Read the 5 anchor sources (Part I). Meet faculty: show Part A's pitch; agree the Measure→Price→Demonstrate framing; ask about IRB for G2/G14.

**Done when:** selftest passes, baseline exists, Part B note drafted, faculty approved.

### Phase 1 (weeks 1–2): pilot → Gate 1
Capture Chrome (control), bKash, one bank app, Pathao/Daraz, one WebView app, 5 min each with PCAPdroid (PCAP mode). `n1_tools.py pcap` → `pilot.csv`; `f2_starter.py` on 5 first-party hosts. If a bank app refuses the VPN: laptop hotspot + Wireshark. **Gate 1:** ≥4/5 parse and Chrome shows `client_offers_pq_keyshare=True`.

### Phase 2 (weeks 2–6): framework lab (G1 + G3-lab) → arXiv note
Each test app fetches `https://www.cloudflare.com/cdn-cgi/trace` and prints `kex=`. Stacks: HttpURLConnection, OkHttp, WebView, Cronet, Chrome Custom Tabs, Flutter (`dart:io`, both platforms), React Native (both), iOS URLSession (if a Mac is available; else Safari + WKWebView via prebuilt apps), optionally .NET MAUI/Unity. Matrix: stacks × Android 10–17 emulators (Play images) × 2 real phones × iPhone. Output `lab/lab_results.csv`. If a major stack lacks PQ (e.g. Dart), open a polite evidence-backed GitHub issue (public, dated record). **Output:** an arXiv note by ~week 6, *"Which mobile networking stacks negotiate post-quantum TLS by default?"* **Gate 2:** ≥6 stacks × 3 Android versions + iOS.

### Phase 3 (weeks 4–10): capture campaign (G4, G5, G7, G15; G3 subset)
Build `data/apps.csv`. Per app × device, 5-min protocol: force-stop → open → login (own account) → balance/history → statement → profile/KYC (view only) → idle; log step start-times to `data/sessions.csv`. Parse `pcap *.pcap > connections_raw.csv`; add `app, device, platform, os_version, network, first_party, flow_step, transport, ip_version`. Label SNIs first- vs third-party. Add QUIC rows from Wireshark. iOS subset ~20 pairs via hotspot. **Gate 3:** ≥40 apps × 2 Android phones + ≥15 iOS pairs.

### Phase 3′ (weeks 4–10, parallel): the amortization probe (C2/C3 — the novel data)
Run `n1_tools.py shortcuts` on every first-party **and API** host and on web↔API pairs: repeated handshakes to log distinct `key_share`s and their lifetimes (P2), RSA-key-transport acceptance (P3), ticket key-name prefixes over time (P4 root), hybrid coverage. Record everything **split by hybrid vs classical** (the theorem). Keep the private-institution probe outputs out of the repo (C6).

### Phase 4 (weeks 6–10): static analysis (G1 link, G6, G9)
`adb pull` all APK splits → `n1_tools.py apk` (frameworks; `spki_pins`, `rsa_cipher_strings`, `pem_*`, `network_security_config`). Pinning (G9): `apktool d` → `<pin-set>` digests → hex → crt.sh `?spkisha256=` → CA vs leaf, RSA vs ECDSA. App-layer crypto (G6): jadx on flagged apps; note *what* is encrypted (PIN? token? payload?) for the P3/M6 cost. Output `data/static.csv`.

### Phase 5 (weeks 8–10): server + hosting (G8)
Pairs of website + API hosts per org → `f2_starter.py` → `servers.csv`; hosting owner via `gethostbyname` + Team Cymru DNS (`origin.asn.cymru.com`, `ASxxxx.asn.cymru.com`) → classify CDN / cloud / own network → `hosting.csv`. Note the CDN-edge-vs-origin nuance (E6): report "PQ at the edge" separately.

### Phase 6 (weeks 10–12): network path + cost (G10, G11)
`n1_tools.py timing` (100 runs, hybrid vs X25519) on each operator, morning/evening/night → `timing.csv` (median, p90, n). Re-capture 10 apps on all four operators for resets/retries/missing ServerHellos (fallback, per the theorem). Optional OkHttp-vs-Cronet request-time + battery on a low-end phone — the unmeasured gap (synthesis C7).

### Phase 7 (weeks 6–14, parallel): Toy-TLS (C4) — the contribution's demonstration
Build Toy-TLS v0 (toy curve, Shor-ECDLP on a statevector simulator, S-AES from `n2_tools.py`) → "recorded toy session decrypted" in ~2 weeks. Add baby ML-KEM and the combiner → the four runs (D2). This runs in parallel with capture so a measurement setback never sinks the thesis.

### Phase 8 (weeks 8–14, parallel, IRB): update-lag survey (G2)
Participants open the trace page in their browser and in an in-app (WebView) browser; paste only `uag=` + `kex=` + model + Android version into a form (no IP). Target 100+ phones; combine with StatCounter.

### Phase 9 (weeks 12–15): analysis + the price pipeline (C2)
Build `quantum_costs.csv` (primitive, algorithm, logical qubits, Toffoli, depth, physical, wall-clock, source, year, scenario) from Part B5. Run the C2 pipeline: attach per-run costs to each recoverable key; compute A(O), Xᵥ(O), Cost_h(O) and cost-per-session under S-fast/S-slow/S-RSA. Produce every table/figure in Part G4. Freeze `data/` (git tag).

### Phase 10 (weeks 14–26): disclosure + notification experiment (G13) + interviews (G14, optional)
Disclosure emails + 1-page fix guide (server: enable X25519MLKEM768; app: WebView/Custom Tabs or Cronet, watch Conscrypt/Flutter; pinning: pin CA keys with backups). G13: if >20 orgs, notify a random half at week 14, the rest at week 20; re-measure at 20 and 26 (expect ≈+10 pts, synthesis H03). G14 (IRB): 30–60 developer/bank survey + 8–12 interviews.

### Phase 11 (weeks 14–22): writing and submission
Flagship (C1+C2+C3 subset) drafted from the Part B note outward; thesis draft by ~week 22. See Part G.

### Phase 12 (months 6–9+): longitudinal / opportunistic (O1–O5)
Re-run the lab + a 15-app capture monthly. If Conscrypt/Flutter ship PQ (O1/O2), Chrome ships PQ WebRTC (O3), or PQ/Merkle-Tree certs go live (O4) → the baseline makes a before/after paper.

---

# PART F: GAP → CONTRIBUTION MAP (G1–G15 and M1–M6, reorganised under the contributions)

The old gaps (G) and merge routes (M) are **not discarded** — they are the work items. Here is how each slots under the new contribution structure, with the synthesis anchor.

| Old ID | Work item | Serves contribution | Synthesis anchor |
|---|---|---|---|
| **M1** | amortization variables in the wild (reuse, RSA transport, psk_ke, tickets) | **C1 + C3** (the lead data) | E01 open problem; E02/E05 pre-1.3 |
| **M2** | packets→qubits price pipeline | **C2** (the lead framework) | E01 lab-only; F05/F06/F08/G02 costs |
| **M3** | Toy-TLS | **C4** | D04, D01/D02/D05, G04, F13 |
| **M4 / G15** | MAXDEPTH-aware cipher view + resumption mode | **C1(P7) + C3**, supporting table | G02, G05; synthesis Debate 6 |
| **M5** | legacy-curve residue (expect ≈0) | side row of **C3** | E05 (no ec2n negotiated) |
| **M6** | cost an uncosted in-app cipher (conditional) | spin-off of **C4** if G6 finds one | G05/G06 method; B06/B07 app crypto |
| **G1** | framework default matrix | **C3 layer attribution** (+ standalone Paper B) | B04, A07, A08, B05 |
| **G2** | device update lag | **C3** context | B04, A07 |
| **G3** | iOS-vs-Android same app | **C3** (+ Paper B) | B02; iOS-26 fact |
| **G4** | app PQ census + 2×2 | **C3 backbone** | B01, A07, A01 (web-only) |
| **G5** | SDK layer | **C3** | B04, B08, B01 future work |
| **G6** | app-layer RSA/ECC | **C1(P3) + C3**; feeds M6 | B03, B06, B07, A04 (OIDC) |
| **G7** | data-lifetime weighting (wᵢ) | **C1(B1) + C3** | E06/E07 shelf-life; E01 value |
| **G8** | API-vs-website + hosting | **C3** (explains A(O)) | B04 future work; A01/A03 attribution |
| **G9** | pinning as a PQ-cert blocker | **C3** side result | B02, B05, C06, D03 |
| **G10** | network path / fallback | **C1 (fallback) + C3** | A06, C01; E07 §6.5 |
| **G11** | cost of the defence on BD networks/phones | **C1 policy figure** (defender cost) | C01, C03, C05, A06 |
| **G12** | static→dynamic prediction (stretch) | **C3** scaling method | B05, B03, B08 |
| **G13** | notification experiment | **C3** intervention (Paper C) | H03, B08 |
| **G14** | developer/bank human layer | context (Paper C) | H01, B03 |

**Opportunistic gaps (record a baseline now):** O1 Conscrypt ships PQ; O2 Flutter/Dart; O3 Chrome PQ WebRTC in WebView; O4 PQ/Merkle-Tree certs live (tests G9's prediction); O5 a global app study appears (keep the Bangladesh / amortization / toy angles).

---
# PART G: WRITING, PAPERS AND VENUES

## G1. Papers (one flagship, two optional satellites)

| Paper | Contents | Why it stands alone | Target venues |
|---|---|---|---|
| **Flagship — "The Quantum Harvest Economics of a Mobile-First Financial Sector"** | **C1** (metric + propositions + neutralization theorem) + **C2** (price pipeline) + the **C3** subset that evaluates them (amortization variables, hybrid coverage, A(O), cost-per-session) + the **C4** toy as the demonstration figure | It is a *model + metric + evaluation + demonstration*, not a measurement. The reviewer's W1 ("just a survey") fails because the deliverable is a reusable standard proved and demonstrated. | **Computers & Security** (Elsevier), **ACM TOPS**, **IEEE TIFS** (ambitious), **PoPETs/PETS** |
| **Paper B — "The Post-Quantum Platform Divide"** | **G1 + G3 (+ G2, G15)**: framework default matrix; same-app iOS-vs-Android after iOS 26; update lag | A clean systems-measurement result with a sharp question ("which layer decides?"), independently publishable | ACM **WiSec**, **PETS**, **Computers & Security**, **IEEE Access** |
| **Paper C (field/toy) — "Toy-TLS: a quantum-simulable model of harvest-now-decrypt-later and its hybrid defence"** | **C4 (M3)** in full, + optional **M6** | The faculty's toy-model contribution; stands as a quantum-info paper | **EPJ Quantum Technology** (Q1), **Quantum Science and Technology** (Q1), **Quantum Information Processing** (Q2), **Physica Scripta** |
| Thesis | RQ0 with chapters = Measure / Price / Demonstrate | — | CSE499 report |

**Submit order:** arXiv note (wk 6) → Flagship (wk 18–22) → Paper B or C as time allows.

## G2. Venue reality check (honest, like the N2 positioning)

- **Flagship Q1 targets.** *Computers & Security* is JCR **Q1** (Information Systems) and the natural home for measurement-plus-defence with a model; it is the realistic Q1 target. *ACM TOPS* is prestigious, lower volume, slower. *IEEE TIFS* is top-tier Q1 but very competitive — attempt only if C1/C2 land cleanly and C3 is strong. *PoPETs* is a strong venue counted as Q1 by many departments (verify your department counts it).
- **IEEE Access caveat** (same as N2): SJR **Q1**, JCR **Q2**. If your department counts Clarivate JCR, Access is *not* Q1 — use it only as a fallback.
- **Paper C.** *EPJ Quantum Technology* and *Quantum Science and Technology* are Q1; *QIP* and *Physica Scripta* are Q2 (the faculty's own GFSPX paper is in Physica Scripta).
- **Check which list your department uses (SJR vs JCR)** before promising "Q1" to the supervisor. Put the chosen journal's current quartile in the proposal.

## G3. Claim ledger (claim only what you measure; re-search the week you submit)

Primary (the contribution):
- "We define the **harvest amortization factor** and prove a **neutralization theorem** for transcript-bound hybrids; to our knowledge the first measurable amortization metric and the first such theorem for the quantum-harvest setting." (C1)
- "The first mapping of **measured, in-the-wild** connections to concrete quantum resource estimates (cost per decrypted session under three hardware scenarios)." (C2)
- "The first toy model to run the **complete HNDL chain with real Shor and Grover circuits, including the hybrid defence and the reuse amplification**." (C4 — verify against F12 and the classical simulators)

Secondary (empirical firsts):
- "The first wild measurement of the amortization variables in the **TLS-1.3/hybrid era** and the first for **mobile-app API hosts**." (C3; E02/E05 were pre-1.3, web-only)
- "The first app-level PQ-key-exchange census of a mobile-first developing economy, with client×server layer attribution." (G4)
- "The first same-app **iOS-vs-Android** PQ comparison after iOS 26." (G3)

Do **not** claim: that you broke anything; a CRQC date; that AES-128 is near-breakable; any number from F12.

## G4. Figures and tables (build these)

1. The **packets→qubits→sessions** schematic (C2).
2. **A(O)** per organization, split hybrid vs classical, with CIs (C1/C3).
3. **Cost per decrypted session** under S-fast / S-slow / S-RSA (C2/B5).
4. **Defender-vs-attacker** policy figure: measured +ms/+bytes/+mJ vs run-equivalents per session (B2/G11).
5. Classical-remainder funnel: offered → accepted → hybrid, by layer (C3).
6. Framework × OS-version heatmap (G1); iOS-vs-Android paired dot plot (G3).
7. Website-vs-API scatter by hosting class (G8).
8. Toy-TLS scaling: cost vs curve order; A vs r; hybrid→locked (C4/D3).
9. Lifetime-weighted exposure Xᵥ (G7); cipher/MAXDEPTH table (M4); pinning CA-vs-leaf (G9); latency CDFs per operator (G11).

## G5. Related-work paragraph (adapt; do not copy)

> Quantum resource estimates price Shor on 256-bit ECC at ≈1,200–1,450 logical qubits and <10⁸ Toffoli gates [F06, F08, F09] and RSA-2048 at under a million qubits [F05], while Grover on AES stays beyond reach under realistic depth limits [G02]. Deployment studies, in parallel, measure post-quantum TLS on web servers and browsers [A01, A02, A03] and, historically, the forward-secrecy shortcuts that weaken it [E02, E04, E05]. These two literatures do not meet: the cost estimates name no deployed connection, and the deployment studies assign no quantum cost. The one paper that bridges them models harvest-now-decrypt-later economics only in a loopback lab, measures no real servers, and names the open problem of "the economics of partial PQC deployment" [E01]. App-side work stops short of the post-quantum question: TLS usage before deployment [B01], pinning [B02], and static crypto-API scans [B03]. We close the seam: we define a measurable amortization metric and a measurement-to-qubits cost model, prove when the hybrid defence collapses the metric, evaluate both on the mobile apps and API back ends of a mobile-first financial sector, and demonstrate the full mechanism with real Shor and Grover circuits at toy scale.

## G6. Threats to validity (write early)
Sample size and selection; single capture location (CDN edges vary by geography); point-in-time (apps update — re-capture 10 apps at the end and report drift); emulator vs real device; unexercised code paths (lower bound, as in B02); origin links hidden behind CDNs; QUIC parsed manually; survey self-selection; the one load-bearing assumption (ML-KEM stays secure, B4); toy results demonstrate mechanism not cost (D4).

---

# PART H: TEAM, TIMELINE, GATES, RISKS

## H1. Roles (3 people, mapped to the three layers)

| Member | Owns | Also |
|---|---|---|
| **A — Measure** | Phases 1, 3, 3′ (captures, sessions, QUIC, iOS, the amortization probe) | flow labels (G7) |
| **B — Price + lab** | Phases 2, 4, 9 (framework lab, static, the C2 price pipeline, stats) | arXiv note; flagship writing |
| **C — Demonstrate + servers** | Phases 5, 6, 7 (hosting, timing, Toy-TLS in Qiskit) | disclosure; Paper C |

The **Part B theory note is written jointly in week 0** — it is the shared spine.

## H2. Timeline (24 weeks)

| Week | 0 | 1–2 | 3–4 | 5–6 | 7–8 | 9–10 | 11–12 | 13–15 | 16–18 | 19–22 | 23–24 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Setup + **Part B note** (P0) | ■ | | | | | | | | | | |
| Pilot (P1) → Gate 1 | | ■ | | | | | | | | | |
| Framework lab (P2) → arXiv wk6 | | ■ | ■ | ■ | | | | | | | |
| Captures + amortization probe (P3/3′) | | | ■ | ■ | ■ | ■ | | | | | |
| Static (P4) | | | | ■ | ■ | ■ | | | | | |
| Servers/hosting (P5) | | | | | ■ | ■ | | | | | |
| Cost/network (P6) | | | | | | | ■ | | | | |
| **Toy-TLS (P7)** | | | | ■ | ■ | ■ | ■ | | | | |
| Survey (P8, IRB) | | | | | ■ | ■ | ■ | | | | |
| Analysis + price pipeline (P9) → Gate 4 | | | | | | | ■ | ■ | | | |
| Disclosure/G13 (P10) | | | | | | | | ■ | ■ | ■ | ■ |
| Writing: flagship + thesis (P11) | | | | | | | | ■ | ■ | ■ | ■ |

## H3. Gates

| Gate | Week | Pass | If it fails |
|---|---|---|---|
| G-0 | 1 | Part B note drafted (defs + P1–P7 + theorem) + selftest + faculty sign-off | The contribution isn't concrete yet — fix before any data |
| G-1 | 2 | ≥4/5 pilot apps parse; Chrome control offers PQ | hotspot method; else lab+toy+static route (H5-D) |
| G-2 | 6 | lab ≥6 stacks × 3 Android + iOS; **Toy-TLS v0 decrypts a toy session** | cut Unity/.NET; keep the 6 core stacks; Toy-TLS is the fallback contribution |
| G-3 | 10 | ≥40 apps × 2 phones + ≥15 iOS pairs; amortization probe on ≥20 orgs | drop to 30 apps; keep the probe (it's the novel data) |
| G-4 | 15 | data frozen; A(O)/cost pipeline runs; story chosen (H5) | minimum thesis: Part B + lab + toy + a 25-app subset |

## H4. Minimum viable thesis (if the harvest goes badly)
**Part B (theory) + C4 (Toy-TLS) + G1 (lab) + a 25-app subset of C3.** This still contains a metric, a theorem, a demonstration with real quantum algorithms, and an evaluation — a contribution, not an assessment — on just emulators, 1–2 phones, `n1_tools.py`, `f2_starter.py` and Qiskit.

## H5. Which story does the data tell? (decide wk 6 and wk 12)

| If… | Lead with |
|---|---|
| **A** Most classical because of framework/OS | C1 layer attribution + G3 platform divide + the neutralization theorem (what *would* fix it) |
| **B** Mostly hybrid (WebView/Cronet/CDNs) | the **amortization angle**: "protection exists but the classical remainder is high-A" + G5/G7 |
| **C** Servers/API hosts are the bottleneck with **high A** (reuse, RSA transport) | C1/C2 as the headline: "one run, many sessions" + G8 + disclosure |
| **D** Capture blocked | Part B + Toy-TLS + lab + static (the contribution survives) |
| **E** A global app study appears | the **model + Bangladesh evaluation + toy** — the metric and theorem are not scooped by a census |

## H6. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| "It's still just a measurement" (the supervisor's worry) | Medium | High | The contribution is Part B's metric+theorem and C2's model, written first (G-0); measurement evaluates them |
| A global app PQ census appears | Medium | Medium | arXiv note wk6; the metric/theorem/toy are the moat, not the census |
| Google/Flutter ship PQ mid-project | Medium | **Positive** | baseline recorded → before/after (O1/O2) |
| Apps block capture | Medium | Medium | hotspot; lab+toy+static (H4) |
| Scarce iPhone | Medium | Medium | borrow 2 days; in-app-browser method; G3 → future work |
| IRB delay | Medium | Low | G2/G14 optional; start paperwork wk1 |
| ML-KEM assumption questioned | Low | Medium | it's named as the one assumption (B4), backed by E07/F06 |
| Member drops out | Low–Med | High | shared CSVs + git; each phase self-contained |

---

# PART I: READING GUIDE (anchored to the 60-paper synthesis)

Read `Literature_Review/Path1_Literature_Synthesis.md` first — it already distils all 60. Then, for the five things this plan most depends on:

| # | Read | Extract |
|---|---|---|
| 1 | **E01** Blanco-Romero 2026 (synthesis App. B) | the HNDL cost model (storage α × E × T_q), the E=1 cases, and the stated open problem — the seed of Part B |
| 2 | **D01** Bindel 2019 + **D02** Barbosa 2024 + **D05** Gupta 2026 | the CcQ adversary, C2PRI robustness, transcript binding — the neutralization theorem's proof inputs |
| 3 | **F06** Babbush 2026 + **F05** Gidney 2025 + **F08** Häner 2026 + **G02** Jaques 2020 | the per-run costs for Part B5 (fast/slow ECDLP; RSA; MAXDEPTH Grover) |
| 4 | **E02** Springall 2016 + **E05** Valenta 2018 | the amortization variables and how to measure reuse (the methods C2/C3 modernise) |
| 5 | **B01** Mankowski 2023 + **B04** Razaghpanah 2017 + **A07** Holz 2019 + **A08** Ibrahim 2026 | app-capture method, the 84%-OS-default layer mechanism, the TLS-1.3 precedent, the "measure with a PQ-capable client, log both sides" rule |

Plus the live-fact sources (re-verify the week you cite): Apple PQ-TLS (iOS 26), Google Android PQ blog + conscrypt#1452, Cloudflare PQ 2025, RFC 10024 (codepoints), Bangladesh Bank ICT Security Guideline v4.0 (does it mention PQ?), StatCounter BD, and notification best practices (for G13).

---

## The very next 5 actions
1. **Write the Part B note** (definitions + P1–P7 + neutralization theorem, 2 pages). This *is* the contribution; everything else evaluates it.
2. `python n1_tools.py selftest`; write `data/baseline.md` for your phones.
3. **Toy-TLS v0** in Qiskit: toy curve (order ≈2⁴–2⁵) + Shor-ECDLP on a statevector simulator + S-AES from `n2_tools.py` → "recorded toy session decrypted" (the fallback contribution, in hand early).
4. Pilot capture (Chrome + bKash + one bank), run `n1_tools.py pcap` and `shortcuts`.
5. Send the faculty Part A's pitch + this plan; confirm the Measure→Price→Demonstrate framing and the Q1 venue; ask about IRB for G2/G14.

> **The one-paragraph pitch for the supervisor.** *"We're not just measuring whether apps are post-quantum. We define a new, measurable security metric — how many recorded sessions one quantum attack run would decrypt — and prove a theorem for when the hybrid defence drives it to one. We build a model that turns each measured connection into a concrete quantum attack cost using the resource estimates from the papers you gave us, evaluate it on Bangladesh's app-based financial sector (the worst case: 91% Android, money in apps), and demonstrate the whole harvest-now-decrypt-later mechanism — amplification by key reuse, neutralization by hybrid — end-to-end with real Shor and Grover circuits on a toy TLS. So the paper has a metric, a theorem, a model, a real-world evaluation and a running attack+defence demonstration — a contribution to quantum cryptanalysis, not an assessment."*
