# N1 + Our Field: turning "is the defense deployed?" into "what would the quantum attack cost?"

> **Why this file exists.** Our faculty liked N1 (the post-quantum app gap) but said it drifts away from our field: **quantum cryptanalysis**, meaning Shor and Grover attacks, quantum circuits for ciphers, resource estimates, toy ciphers like S-AES, and defenses. He asked us to **merge** the field's ideas (attack, defense, mechanism, toy set, algorithms) into the empirical study.
> **Short answer:** keep the N1 measurements, but **turn every measured connection into a quantum attack problem with a price tag**, measure the deployment habits that **multiply or divide** that price, and **demonstrate the whole attack at toy scale** with Shor and Grover.
> Written 1 Oct 2026. Prior work was checked the same day; **(verify)** marks what we must re-check.

---

## 0. The problem in one picture

```
   What N1 measures now               What our field (the faculty's papers) studies
   ─────────────────────              ─────────────────────────────────────────────
   "Did this app connection           "How many qubits / Toffoli gates / how much depth
    use the post-quantum lock?"        does Shor or Grover need to break cipher X?"
         (yes / no)                          (S-AES, AES S-box, AEAD, GFSPX,
                                              binary-curve ECC, hash collisions)

                         THE BRIDGE (this file)
   "For each real connection we measured: WHICH quantum attack breaks it, HOW MUCH it
    costs, and HOW MANY recorded sessions ONE run of that attack opens."
```

Right now N1 uses the field only as **motivation** ("Shor breaks ECC, so migrate"). The faculty wants the field **inside the method**. The routes below do that.

---

## 1. What each paper gives us, and where it enters N1

| Faculty's paper | What it gives (in plain words) | Where it plugs into N1 |
|---|---|---|
| **Putranto et al., IEEE Access 2025** and **Taguchi & Takayasu, CT-RSA 2023** (Shor on binary elliptic curves) | Qubit, Toffoli and depth counts for breaking elliptic curves with Shor; how arithmetic tricks (inversion, point addition) change the cost | **M2:** the price of breaking each curve we see. **M5:** are legacy curves still accepted? The same *style* of estimate exists for **Curve25519** (the curve inside X25519): Song & Seo, ICISC 2024; Ed25519 circuits, QIP 2025 |
| **Chen et al., arXiv 2503.06097** (AES S-box circuit) and **Wang et al., npj QI 2025** (S-AES Grover oracle: 160 → 120 Toffoli, plus VQAA) | The cost of the Grover oracle for AES; S-AES as the standard **toy** | **M4:** the Grover price of each session's AES-128 / AES-256. **M3:** S-AES becomes the record cipher of our toy handshake |
| **Mandal et al., Sci Rep 2024** (Grover on AES-based AEAD) and **Ulgen et al., Phys Scr 2026** (GFSPX) | The *method*: build the cipher as a quantum circuit, then cost Grover under NIST's **MAXDEPTH** limit (2^40, 2^64, 2^96) | **M4:** judge sessions by MAXDEPTH-aware cost, not the slogan "128 becomes 64". **M6:** if apps use an uncosted cipher inside the app, we cost it this way |
| **Bernstein 2009** (hash collisions) | Count the **real** cost of an attack (hardware × time), not just the number of steps | **M1/M2:** our "sessions per quantum run" and "defender cost vs attacker cost" figures are Bernstein-style cost accounting |

**Numbers we can already cite for the price tags** (re-check the latest versions):

| What real apps use | Quantum attack | Published cost (examples) |
|---|---|---|
| X25519 key exchange (Curve25519) | Shor, elliptic-curve discrete log | Curve25519 circuit: Song & Seo 2024. Generic 256-bit ECC: ~2,330 logical qubits, 1.26×10¹¹ Toffoli (Roetteler et al. 2017) → **< 1,200 logical qubits, < 90 M Toffoli** (Google 2026) |
| P-256 key exchange or certificates | Shor, elliptic-curve discrete log | Same as above |
| RSA-2048 (TLS 1.2 key transport, RSA inside apps) | Shor factoring | **< 1 million noisy qubits, < 1 week** (Gidney 2025) |
| AES-128-GCM / AES-256-GCM records | Grover key search | Jaques et al., EUROCRYPT 2020; improved AES-128 circuit: Chen et al. 2025 (faculty's paper) |
| ChaCha20-Poly1305 records (common on phones) | Grover key search | **1.233 × 2^251 gates at MAXDEPTH 2^40** (Bathe, Anand et al., QIP 2021; Anand also co-wrote the faculty's AEAD paper) |
| SHA-256 in certificates | BHT collision search | No real quantum advantage over classical (Bernstein 2009) |

---

## 2. The merge routes (ranked)

| # | Route | Faculty's word | New? | Effort | Verdict |
|---|---|---|---|---|---|
| **M1** ⭐⭐ | **"Sessions per Shor run"**: deployment shortcuts that let ONE quantum run decrypt MANY recorded sessions | **mechanism + attack** | **Yes** (lab-only prior work; our live data already shows it) | 3–4 person-weeks | **Lead contribution** |
| **M2** ⭐ | **"From packets to qubits"**: a quantum price tag for every measured connection and every app | attack (cost) + defense | Partly (a new lens; the costs are published) | 2 person-weeks | Core analysis chapter |
| **M3** ⭐ | **Toy-TLS**: a toy hybrid handshake (toy ECC + S-AES + baby ML-KEM), attacked with simulated Shor and Grover | **toy set + new model + algorithms** | The combination is new; each piece exists | 3–5 person-weeks | The faculty's "new toy model" requirement, tied to N1 |
| **M4** | **Grover view done properly** (G15 upgraded): each session's symmetric cipher judged by MAXDEPTH-aware Grover cost | attack (Grover) | Small | 1 person-week | Easy add-on |
| **M5** | **Legacy-curve residue**: do Bangladeshi servers still accept the binary / small curves costed in the faculty's Shor papers? | attack (Shor) | Small (classical scans exist; expected near zero) | 3 days | Side row only |
| **M6** | **Cost an uncosted cipher found inside apps** (Mandal / Ulgen style circuit + Grover) | algorithms (circuits) | Yes, *if* we find one | 4–6 person-weeks | Conditional |

The details follow.

---

### M1 ⭐⭐ "Sessions per Shor run": quantum amortization in the wild

**The idea in plain words.**
A quantum computer will be slow and expensive, so an attacker must pay for **every single run** of Shor's algorithm. Forward secrecy is supposed to force **one run per recorded session**: every connection gets a fresh key.
> 📦 *Example:* a thief with a very slow master-key machine. If every door has its own new lock, one key opens one door. If a building uses the same lock on 1,000 doors, one key opens all of them.

Real servers take **shortcuts** that break this rule. Each shortcut changes the number that matters to a quantum attacker: **how many recorded sessions ONE quantum run opens**.

| Shortcut (what we measure) | Quantum consequence | How we measure it |
|---|---|---|
| **(a) Server reuses its "ephemeral" key share** across connections | One **Shor** run on that key decrypts **every** session that used it | Connect several times and compare the server's `key_share` (**tool ready**: `n1_tools.py shortcuts`) |
| **(b) TLS 1.2 RSA key transport** (no forward secrecy) | One **Shor** factoring run on the certificate's RSA key decrypts **every** session ever recorded that used it | Server probe (**tool ready**); whether apps *actually* negotiate it: from our pcaps (cipher suite column) |
| **(c) Resumption without a fresh key exchange** (`psk_ke`, 0-RTT) | One Shor run on the first handshake also opens every resumed session in the chain | `psk_modes` column, already in `n1_tools.py pcap` |
| **(d) Long-lived session-ticket keys (STEK)** | The ticket travels **in plaintext** in the next ClientHello. One **Grover** run on the STEK opens all tickets it protected. With an AES-256 STEK that is hopeless; with AES-128 it is "only" 2^64 Grover iterations (still enormous; see M4) | Ticket key-name prefix over time: `openssl s_client -sess_out` + `openssl sess_id -text` **(verify)** |

**Headline metric:** the **amortization factor**, i.e. sessions exposed per quantum run (1 = ideal forward secrecy). Combined with M2's price tag, this gives the **quantum cost per decrypted user session**, a number both a bank and our faculty understand.

**What already exists (checked 1 Oct 2026):**
- **Springall, Durumeric & Halderman, IMC 2016** measured these shortcuts **classically** for TLS 1.2 on the Alexa top million (key reuse, session tickets), *before* TLS 1.3 and before the quantum framing. **Hebrok et al., USENIX Security 2023** measured session-ticket weaknesses (classical).
- **Blanco-Romero et al., arXiv 2603.01091 (2026)** model the per-session Shor cost of harvest-now-decrypt-later, but **only in a loopback lab testbed**: they measure **no real servers**, **don't consider Grover on ticket keys**, and write that "the economics of partial PQC deployment also deserve study".
- **Nobody has measured how real deployments change the number of quantum runs**, and certainly not for mobile-app API servers in a mobile-first country. That is our gap. **(Re-search before claiming; especially TLS 1.3 key-share-reuse measurements.)**

**Our first result (1 Oct 2026, 02:40 BST, this laptop):**

| Server | Group used | Distinct server key shares | TLS 1.2 RSA key transport |
|---|---|---|---|
| cloudflare.com | X25519MLKEM768 | 5 of 5 (fresh every time ✅) | accepted (AES128-GCM-SHA256) |
| www.google.com | X25519MLKEM768 | 5 of 5 ✅ | accepted (AES128-GCM-SHA256) |
| **www.bb.org.bd** | **X25519 only** | **4 distinct in 10 handshakes**, repeating in a fixed cycle A-B-C-D-A-B-C-D…; **the same 4 keys were still in use at 02:45** (≥ 5 min) ❗ | refused ✅ |

**What this means:** the Bangladesh Bank site seems to sit behind **4 servers, each reusing one X25519 key** instead of making a fresh one per connection. If that holds over time, **four Shor runs** would decrypt every recorded session in that window, not one run per session. Combined with the missing post-quantum group, this is the worst case for harvest-now-decrypt-later. (Cloudflare and Google accepting RSA key transport matters less: modern clients never pick it. That's why (b) must be checked against what apps *actually negotiate*.)

> ⚠️ **Handle with care.** This is a live finding about a real institution. It is also a **classical** forward-secrecy weakness, because anyone who steals a server's memory can decrypt past traffic.
> 1. **Don't post it anywhere** (no social media, no public repo, no public slides).
> 2. Measure **how long** each key lives (re-probe every hour for a day).
> 3. Tell the faculty first, then disclose privately (bank IT or BGD e-GOV CIRT) under N1's disclosure plan, **before** any paper.

**Research questions (open and two-sided, so every outcome is a result):**
- RQ-M1a: How often do Bangladeshi finance and government **app API servers** reuse key shares, accept RSA key transport, or issue long-lived tickets, compared with their websites and with global CDNs?
- RQ-M1b: What is the **amortization factor** per organization, and how much does it change the quantum cost of decrypting a user's recorded traffic?
- RQ-M1c: Does deploying hybrid ML-KEM **neutralize** these shortcuts (reusing the X25519 half doesn't matter if ML-KEM is fresh), or do they survive in the classical fallback?

*If nobody reuses keys:* "Forward secrecy holds, so the attacker pays per session. Here's the price (M2)." *If many do:* a direct, fixable, disclosure-worthy finding. **Both are papers.**

---

### M2 ⭐ "From packets to qubits": a quantum price tag for every connection

**Idea.** For every connection row N1 produces, add columns that say **which quantum algorithm breaks it and what that costs**, using the numbers in §1.

```
 app       sni              kex            cipher        app-layer   cheapest quantum break            cost
 ───────── ──────────────── ────────────── ───────────── ─────────── ───────────────────────────────── ─────────────────────
 bank-X    api.bank-x.bd    X25519         AES_128_GCM   RSA-2048    Shor-ECDLP on X25519 (per session) ~1.2k lq, ~9e7 Toffoli
 wallet-Y  api.wallet-y.bd  X25519MLKEM768 AES_256_GCM   none        Grover on AES-256 (per session)    beyond any MAXDEPTH
```
*(Illustrative rows, not measurements. lq = logical qubits.)*

**What it produces:**
1. **An attack tree per app:** the key exchange (Shor), app-layer RSA (Shor, G6), record cipher (Grover), certificates (Shor, active attacks only, not harvest-now-decrypt-later). The app's exposure is its **weakest link**.
2. **The "defender vs attacker" figure (Bernstein-style):** our measured cost of the defense on Bangladeshi networks (+ms, +bytes, G11) against the published cost of the attack (qubits × time). One picture: "the defense costs 12 ms; the attack it stops costs 10⁸ Toffoli per session".
3. **A Mosca-style deadline per data type** (G7): *data shelf-life + migration time > time until a quantum computer* means trouble. We don't predict the quantum date; we show the result under **three published hardware scenarios**.

**New?** Industry "crypto inventory" tools and conceptual banking papers (e.g. "Evaluating Quantum Threats to Mobile Banking Applications in SMEs") assign quantum risk **without measurement**. Tying **measured** app flows to **concrete** resource estimates is new, but it is a *lens*, not a standalone paper. Use it as the analysis chapter.

---

### M3 ⭐ Toy-TLS: the faculty's "new toy model", built from N1's real handshake

**Idea.** Build a **miniature TLS 1.3** that keeps the real structure but uses toy-size pieces, then attack it with the real quantum algorithms on a simulator (Qiskit 2.5 is already installed).

```
 Client ──ClientHello (toy ECDH share + toy ML-KEM key)──▶ Server
        ◀─ServerHello (toy ECDH share + ML-KEM ciphertext)─
 key = KDF(ECDH secret [+ ML-KEM secret if hybrid])
 records encrypted with S-AES (16-bit key)  ◀── same S-AES as the faculty's npj paper (already in n2_tools.py)

 Attacker records everything ("harvest"), then later ("decrypt"):
   Attack 1  Shor-ECDLP on the toy curve   → ECDH secret → session key → read records
   Attack 2  Grover on S-AES               → session key directly (npj paper's 120-Toffoli oracle)
   Defense   hybrid ML-KEM                 → Attack 1 recovers only half the secret: records stay locked
   Shortcut  server key reuse (M1)         → ONE Shor run opens ALL toy sessions (M1's claim, shown quantumly)
```

**Why this is exactly what the faculty asked for:** it is a **structural change to toy systems** that creates a **new model** (S-AES inside a toy hybrid handshake), and it contains the **attack** (Shor, Grover), the **defense** (hybrid ML-KEM), the **mechanism** (amortization) and the **algorithms**, all tied to what N1 measures in real apps.

**Measurable outputs:** qubits, gates and depth of each toy attack, how they grow as the toy sizes grow (curve size, S-AES rounds), and success probability on the noisy simulator (and, optionally, IBM hardware).

**What already exists:** Shor on a 5-bit elliptic-curve key ran on IBM's 133-qubit ibm_torino (Tippeconnic et al., arXiv 2507.10592, 2025). Grover and VQAA on S-AES: the faculty's npj paper. Browser simulators of the hybrid handshake exist but are purely **classical** (e.g. crypto-lab-pq-tls-handshake). **We found no toy model that runs the complete harvest-now-decrypt-later chain with real quantum algorithms, including the hybrid defense and the reuse shortcut (verify).** Honest limit: toy results don't predict real costs; they **demonstrate mechanisms**. Say so in the paper.

**Plug-in to N2:** any toy cipher from the N2 family can replace S-AES as the record cipher. That is how the second team member's work joins the same thesis.

---

### M4 "Grover view done properly" (G15 upgraded)

N1 already records whether each session uses **AES-128-GCM, AES-256-GCM or ChaCha20-Poly1305**. Instead of the slogan "AES-128 becomes 64-bit", classify each session with **MAXDEPTH-aware** Grover costs (Jaques 2020; Chen 2025; Bathe 2021 for ChaCha20), the method of the faculty's AEAD and GFSPX papers.
- It tests the faculty's own statement ("AES-256 is safer") on **real Bangladeshi traffic**: what share of sessions actually get a 256-bit key?
- Phone-specific twist: phones without AES hardware often choose **ChaCha20** (256-bit key). Does Android vs iPhone change the Grover view?
- **Honest note:** even AES-128 under realistic MAXDEPTH is far beyond any foreseeable machine. This is a supporting table, not the headline.

---

### M5 Legacy-curve residue (a direct link to the two Shor papers)

Probe Bangladeshi bank/API servers in **TLS 1.2** for the curves they still accept: binary curves (sect163k1 … sect571r1, exactly the ones Putranto et al. and Taguchi & Takayasu cost), small prime curves (secp192/224) and brainpool. Then map each accepted curve to the qubit counts in those papers.
- **Expect near zero**, since classical scans already found binary curves rare (Valenta et al., "In search of CurveSwap", EuroS&P 2018). Include only as a side row: "the curves the faculty's papers break are (or aren't) still reachable here".
- Tooling: the same child-process trick as `n1_tools.py timing` (set `Groups = sect283k1` etc.). **(Verify that Python's OpenSSL build includes binary curves.)**

---

### M6 Conditional: cost a cipher we discover inside apps

If the app-layer crypto scan (G6) finds an **uncosted** primitive inside Bangladeshi finance apps (e.g. 3DES for PIN blocks, a custom or lightweight cipher), write its **quantum circuit and Grover estimate** exactly like Ulgen et al. (GFSPX) or Mandal et al. (AEAD). That is a pure "field" paper, motivated by measurement. Only do this if G6 finds something **and** a prior-art search shows no estimate exists. **Occupied already, so don't redo:** Grover on ChaCha20 (Bathe et al. 2021), Shor circuits for Curve25519 (Song & Seo 2024) and Ed25519 (QIP 2025).

---

## 3. The merged project (what to tell the faculty)

**New umbrella question:**
> *How many quantum operations would it take to decrypt a Bangladeshi app user's recorded traffic, which deployment choices multiply or divide that number, and does the post-quantum defense remove it?*

**Three layers: Measure → Price → Demonstrate**

| Layer | What | Gaps / routes | Field content |
|---|---|---|---|
| **Measure** | N1 as planned: apps, frameworks, servers, cost of the defense | G1–G15 | Defense deployment |
| **Price** | Map every connection to its quantum attack and cost; measure the shortcuts that multiply the damage | **M1, M2, M4** (+ M5) | Shor/Grover resource estimates, amortization, MAXDEPTH |
| **Demonstrate** | Toy-TLS: run the full harvest-now-decrypt-later chain with Shor and Grover, show that hybrid ML-KEM stops it and that key reuse amplifies it | **M3** (+ N2 ciphers) | Toy systems, quantum circuits, simulation |

**How this answers each word of the faculty's feedback:**

| Faculty said | Our answer |
|---|---|
| **Attack** | Shor (ECDLP, factoring) and Grover priced for every real connection (M2, M4), and run for real at toy scale (M3) |
| **Defend** | Hybrid ML-KEM: where it's missing (N1), what it costs (G11), and a demonstration that it blocks Shor (M3) |
| **Mechanism** | Quantum amortization: shortcuts that turn one quantum run into many decrypted sessions (M1) |
| **Toy set** | Toy-TLS with S-AES records, a toy curve and baby ML-KEM (M3) |
| **Algorithms** | Shor-ECDLP and Grover circuits in Qiskit, with resource counts (M3); an optional new cipher circuit (M6) |

**Papers (updated):**
1. **Paper A (lead):** *"Sessions per Shor run: measuring how deployment shortcuts amortize quantum attacks on a mobile-first financial sector"* (M1 + M2 + a G4 subset). Targets: *Computers & Security*, *JISA*, *IEEE Access*; or ACM WiSec / ACSAC.
2. **Paper B:** *"The post-quantum platform divide"* (N1's G1 + G3, unchanged).
3. **Paper C (field / toy):** *"Toy-TLS: a quantum-simulable model of harvest-now-decrypt-later and its hybrid defense"* (M3). Targets: *Quantum Information Processing*, *Physica Scripta*, *EPJ Quantum Technology*, or an education venue.

**Team split (3 people):** P1 measurement (N1 captures + `shortcuts` probe); P2 pricing (M2/M4 table + M1 analysis); P3 quantum toy (M3 in Qiskit). All three share one dataset and one thesis.

---

## 4. The 30-second version for the faculty

> "Sir, you said our work must be about Shor and Grover. So we'll turn every app connection we measure into a quantum attack problem. We'll say which algorithm breaks it and how many qubits and gates it needs, using the resource estimates from the papers you gave us. We also found something new: servers take shortcuts that let **one** Shor run decrypt **many** recorded sessions. The Bangladesh Bank site cycled through the same 4 elliptic-curve keys in our test, so a few Shor runs would open all of its traffic in that time window. Finally, we'll build a **toy TLS** (toy curve + S-AES + baby ML-KEM) and run Shor and Grover on it in Qiskit, to show the full harvest-now-decrypt-later attack and how the hybrid defense stops it. So the thesis has attack, defense, a mechanism and a toy model, all tied to real measurements."

**Likely questions:**

| He asks | We answer |
|---|---|
| "Isn't the key reuse just a classical problem?" | "Classically it breaks forward secrecy. Quantumly it's worse: the attacker needs *no* stolen memory, only recorded packets and one Shor run per reused key. We measure both views." |
| "Your toy results won't scale to real sizes." | "Correct. The toy shows **mechanisms** (reuse amplifies Shor; hybrid blocks it). Real **costs** come from published estimates (M2). We keep the two separate." |
| "Isn't Grover on AES-128 practical, then?" | "No. Under NIST's MAXDEPTH limit it's still astronomically expensive. That's why our Grover analysis is a supporting table, and it confirms your AES-256 point." |
| "Did someone do this?" | "Classical shortcut scans (2016) and a lab-only quantum cost model (2026) exist. Nobody has measured real servers for quantum amortization, and not for mobile-app backends." |

---

## 5. Next 3 actions

1. **Re-probe `www.bb.org.bd` every hour for 24 h** to see how long each of the 4 keys lives (that turns one observation into a result). Run `python n1_tools.py shortcuts www.bb.org.bd`, at most once an hour. Keep the output private.
2. **Build the price table (M2):** one CSV `quantum_costs.csv` (primitive, algorithm, logical qubits, Toffoli, depth, source, year) from the sources in §1. Two days.
3. **Toy-TLS v0 (M3):** a toy curve with group order about 2^4–2^5, Shor-ECDLP on a Qiskit statevector simulator, S-AES from `n2_tools.py`. Goal: "recorded toy session decrypted" in two weeks.

---

## Sources checked for this file
- Blanco-Romero et al., *On the Practical Feasibility of HN-DL Attacks*, arXiv 2603.01091 (2026): https://arxiv.org/abs/2603.01091
- Springall, Durumeric, Halderman, *Measuring the Security Harm of TLS Crypto Shortcuts*, IMC 2016: https://www.semanticscholar.org/paper/Measuring-the-Security-Harm-of-TLS-Crypto-Shortcuts-Springall-Durumeric/44c355d537340a3842e743cb116d2bf44e6c6df8
- Hebrok et al., *We really need to talk about session tickets*, USENIX Security 2023: https://dl.acm.org/doi/10.5555/3620237.3620510
- Bathe, Anand et al., *Evaluation of Grover's algorithm toward quantum cryptanalysis on ChaCha*, QIP 2021: https://link.springer.com/article/10.1007/s11128-021-03322-7
- Song & Seo, *Quantum Circuit for Curve25519 with Fewer Qubits*, ICISC 2024: https://link.springer.com/chapter/10.1007/978-981-96-5566-3_12
- *Improved quantum circuits for ECDLP on Ed25519*, QIP 2025: https://link.springer.com/article/10.1007/s11128-025-04916-1
- Roetteler et al., *Quantum Resource Estimates for Computing ECDLs*, ASIACRYPT 2017: https://arxiv.org/pdf/1706.06752
- Google Quantum AI, *Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities*, arXiv 2603.28846 (2026): https://arxiv.org/abs/2603.28846
- Tippeconnic et al., *Breaking a 5-Bit Elliptic Curve Key using a 133-Qubit Quantum Computer*, arXiv 2507.10592: https://arxiv.org/pdf/2507.10592
- Classical hybrid-handshake simulator: https://github.com/systemslibrarian/crypto-lab-pq-tls-handshake
- *Evaluating Quantum Threats to Mobile Banking Applications in SMEs* (conceptual, no measurement): https://www.researchgate.net/publication/395387142_Evaluating_Quantum_Threats_to_Mobile_Banking_Applications_in_SMEs
- Faculty's papers: see `Papers/`.
