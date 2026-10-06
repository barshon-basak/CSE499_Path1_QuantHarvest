# Path 1 Literature Synthesis: Themes, Consensus and Debate, Research Gaps

**Project:** N1, "Post-Quantum App Gap" (Bangladeshi finance apps and their back ends), plus its merge with quantum cryptanalysis (`N1_Field_Merge.md`: M1–M6).
**Corpus:** the 60 PDFs in `papers/` (groups A–H, listed in `papers.csv`). **Date:** 6 Oct 2026.

This report gives three analyses of the Path 1 literature, followed by detailed notes on every paper:

1. **Thematic extraction and pattern mapping** (Part 1): six themes that connect the 60 papers. For each theme it gives the core concept, every paper that addresses it, and what the evidence says taken together.
2. **Consensus and debate finder** (Part 2): where authors reach the same conclusion, where they contradict each other, and *why* their results differ (sample, method, unit of measure, vantage point, geography, period, assumptions, conflicts of interest).
3. **Research gap exposer** (Part 3): what the authors overlooked (variables, populations, contexts), what they say should come next, and how N1 can build on the missing pieces. The gaps are mapped to N1's gap list (G1–G15, `N1_Gap_Portfolio.md`) and to the field-merge directions (M1–M6, `N1_Field_Merge.md`).

The appendices give the paper key (Appendix A) and full per-paper notes (Appendix B): question, method, data, every key number, stated limitations, stated future work, quality flags, and relevance to N1.

---

## 0. Scope and method

### 0.1 What was analysed and how

- **All 60 PDFs were downloaded** (`download.py`, 60/60 valid PDFs) and their full text was extracted with `pdftotext`. Reference lists were stripped and the text was read section by section: abstract, introduction, method, all results tables, discussion, limitations, future work and appendices with results.
- **Very long papers.** Six papers are very long (E06 ~75 pp., E07 ~60 pp., F06 ~57 pp. plus appendix, F07, F08 ~65 pp., F09). For these, the main body was read in full and the long proof, circuit or compiler appendices were skimmed for numbers and conclusions. The blockchain-specific sections of F06 (III, V, VI, VIII) were skimmed for structure only; its sections I–IV, VII and IX were read in full.
- **Checking numbers.** Each headline number was checked against the paper's own tables. Where a paper contradicts itself, both numbers are reported and the inconsistency is flagged (Appendix B, "Quality flags").
- **Running notes.** Notes were written paper by paper while reading (Appendix B), and the three analyses were then built from those notes.

### 0.2 Composition of the corpus

| Group | Topic | Papers | Years |
|---|---|---|---|
| A | Post-quantum TLS deployment measurement | A01–A09 (9) | 2019–2026 |
| B | Mobile-app TLS, pinning, finance apps, capture tools | B01–B09 (9) | 2015–2026 |
| C | Cost and performance of PQ-TLS | C01–C06 (6) | 2020–2026 |
| D | Hybrid key exchange and PQ protocol design | D01–D05 (5) | 2019–2026 |
| E | Forward secrecy in practice, HNDL, threat timelines, agility | E01–E08 (8) | 2015–2026 |
| F | Shor resource estimates and demonstrations (ECC, RSA) | F01–F13 (13) | 2017–2026 |
| G | Grover on AES and cost accounting | G01–G07 (7) | 2009–2026 |
| H | Migration, crypto-agility, vulnerability notification | H01–H03 (3) | 2016–2024 |

- **Recency:** 38 of the 60 papers are from 2023 or later, and 27 are from 2026. The older papers (2009–2019) are kept because later work still builds on them or uses them as baselines: B04, A07, E02, E04, F01, G01, G07.
- **Faculty papers:** nine of the papers come from the project's faculty set (F10, F11, G03–G07, plus E06/E07 context).

### 0.3 Conventions

- Papers are cited by ID plus first author and year, e.g., **A01 (Wickramasinghe 2026)**. Appendix A lists all 60.
- **[calc]** marks a number I derived with simple arithmetic from a paper's own figures. The paper does not state it.
- **[N1]** marks a link to this project's gap list (G1–G15) or field-merge directions (M1–M6). It is not a claim made by the literature.
- **HNDL** = harvest-now-decrypt-later. **CRQC** = cryptographically relevant quantum computer. **Hybrid** = X25519MLKEM768 (TLS codepoint 0x11EC) unless stated otherwise.
- "PQ adoption" always says *what* was measured: server support, server default, negotiated group, or configuration file. These are different quantities (see Debate 3).

### 0.4 Corrections to N1's claim ledger found while reading

These matter because N1's planning documents cite some of these papers. Re-check every claim before submitting a paper.

| # | Claim as used in N1 planning | What the paper actually says | Fix |
|---|---|---|---|
| 1 | "A01 explicitly excludes mobile apps and custom API endpoints" | A01 **never mentions** mobile apps or APIs. They fall outside its design: Top-1M web domains, HTTPS only, server-side probes from 11 cloud vantage points. | Write: "its sample is web domains measured from cloud vantage points; client stacks, mobile apps and app back ends are outside its design." |
| 2 | "Mobile traffic is ~52% TLS 1.3 and ~45% QUIC" (as quoted by E01) | The figure originates in **B09 (PARROT 2025)**. It is a share of *packets* during the *first launch* of 50 Vietnamese apps in an *emulator in Spain*, with mitmproxy partly on. It is not a population statistic. | Cite B09 directly and give its conditions. B08 found UDP/QUIC was only 0.22% of flows (Debate 2). |
| 3 | B03 "781 apps use RSA" | B03's table shows 781 instances in 781 apps, but its text says 589 apps. | Report "≈600–780 apps (internally inconsistent)". |
| 4 | A06 results on CECPQ2 | A06 is a **4-page experiment design**. Its results appeared only later, on the Cloudflare blog. | Cite A06 for the design and questions; cite Langley's 2018 note (via A06) for the "~5% of clients see outsized latency" result. |
| 5 | A04 as a source of numbers | A04 contains a stray LLM string ("Opus 4.6Extended") and stale figures. It also lists SIKE and Rainbow as candidates without noting that they are broken. | Cite A04 only for its cross-protocol framing ("key exchange is easier to migrate than authentication"). |
| 6 | A05's "hybrid" performance test | A05 deploys X25519MLKEM768 but benchmarks ML-KEM-512. It also contains a "TODO" reference and swapped contribution numbering. | Give A05's +23% connect-time figure with these caveats. |
| 7 | A08's survey ("38 UK endpoints all classical") | This is an **artefact**: A08's client (stock OpenSSL 3.0.13) never offered PQ groups. A08 also says hybrid ServerHellos "may reach 2 MB", which is wrong (≈+1.1 KB; A01, D04). | Cite A08 for the lesson "measurement needs a PQ-capable client" and for its group-ID table, not for its survey. |
| 8 | A09's certificate-lifetime figures | A09 reports ≤90-day certificates as 40% vs 50% in Fig. 7 but "10%" in its conclusion. It also misses QUIC entirely (IPv4/TCP only). | Use A09's TLS 1.3 / hybrid split (Korea 40%/0% vs global 90%/40%) only, with n = 10 vs 10. |
| 9 | "AES-128 = 64-bit security against Grover" (A02, A05, A09; echoed by G01's conclusion and E07) | Under NIST's MAXDEPTH cost model, AES-128 key search costs ≈2⁹³–2¹¹⁷ gates (G02). NIST *lowered* its Category-1 thresholds after G02, and they remain astronomically high (G05). | Use MAXDEPTH-aware costs (M4/G15). |
| 10 | E06 as "the" CRQC timeline | E06 asks experts about **RSA-2048 in under 24 h**, not about breaking ECC-256. ECC-256 is estimated to be cheaper (F01–F09). | Call E06 a conservative proxy for the threat to ECDH key exchange. |
| 11 | E07 crossover dates | E07 is a scenario model whose couplings are "chosen rather than measured". Its figures were rendered by an AI model, and its authors have a commercial conflict of interest. Only its RSA/ECC tier rests on a known mechanism (Shor). | Use E07 for policy facts and for its §6.5 statement that downgrade via negotiation, resumption caches or libraries is "out of scope". |
| 12 | F12 "breaking a 5-bit ECC key on IBM hardware" | F12 replaces elliptic-curve arithmetic with index arithmetic mod 32. The correct key appears only "in the top 100" of 1,024 outcomes. | Do not use F12 as evidence of progress (Debate 8). |

> **Handling of N1's own pilot data.** N1's planning documents mention a pilot server-probe finding about a real Bangladeshi institution. Per `N1_Field_Merge.md`, it must stay private until responsible disclosure. This report therefore does **not** name or describe it. Where Part 3 needs to refer to N1's own measurements, it speaks only of "N1 pilot probes".

---

## Paper list (60 papers, grouped)

(Full bibliographic key in Appendix A; detailed notes in Appendix B.)

**A. Post-quantum TLS deployment measurement**
- A01 Wickramasinghe, Li, Jha, Shaghaghi 2026: *Mind the Gap: Policy vs Reality in Post-Quantum TLS Deployment* (ACM IMC 2026)
- A02 Dubey, Varshney 2026: *Measurement Study of Post-Quantum Readiness of Internet: 2026* (arXiv)
- A03 Loizou, Ghadafi 2026: *Measuring Post-Quantum TLS Deployment Across UK Internet Sectors* (arXiv)
- A04 Mallick, Kundu, Kompella 2026: *Study of Post Quantum status of Widely Used Protocols* (arXiv)
- A05 Balaji et al. 2026: *Operationalising Post Quantum TLS… in Financial Infrastructure* (arXiv / ePrint 2026/959)
- A06 Kwiatkowski, Sullivan, Langley, Levin, Mislove 2019: *Measuring TLS key exchange with post-quantum KEM* (NIST PQC Conf.)
- A07 Holz, Amann, Razaghpanah, Vallina-Rodriguez 2019: *The Era of TLS 1.3* (arXiv)
- A08 Ibrahim, Ajith, Haroon 2026: *Detecting Post-Quantum and Hybrid TLS Deployments via Raw TLS Record Inspection* (ePrint 2026/834)
- A09 Cho et al. 2025: *Toward Crypto Agility: Automated Analysis of Quantum-Vulnerable TLS via Packet Inspection* (ePrint 2025/1549)

**B. Mobile-app TLS, pinning, finance apps and capture tools**
- B01 Mankowski, Wiggers, Moonsamy 2023: *TLS → Post-Quantum TLS on Android* (EuroS&P Workshops)
- B02 Pradeep et al. 2022: *A Comparative Analysis of Certificate Pinning in Android & iOS* (IMC)
- B03 Strauss et al. 2025: *Assessing and Enhancing Quantum Readiness in Mobile Apps* (IEEE S&P poster)
- B04 Razaghpanah et al. 2017: *Studying TLS Usage in Android Apps* (CoNEXT)
- B05 Oltrogge et al. 2021: *Why Eve and Mallory Still Love Android* (USENIX Security)
- B06 Reaves et al. 2015: *Mo(bile) Money, Mo(bile) Problems* (USENIX Security)
- B07 Mickey, Yanhaona 2024: *An investigation of the Online Payment and Banking System Apps in Bangladesh* (arXiv)
- B08 Yang et al. 2026: *Okara: Detection and Attribution of TLS MitM Vulnerabilities in Android Apps* (ACISP 2026)
- B09 Jimenez-Berenguel et al. 2025: *PARROT: Portable Android Reproducible traffic Observation Tool* (arXiv)

**C. Cost and performance of PQ-TLS**
- C01 Paquin, Stebila, Tamvada 2020: *Benchmarking Post-Quantum Cryptography in TLS* (PQCrypto)
- C02 Sikeridis, Kampanakis, Devetsikiotis 2020: *Post-Quantum Authentication in TLS 1.3* (NDSS)
- C03 Gómez-Cambronero, Munteanu, González-Tablas 2026: *Layered Performance Analysis of TLS 1.3 Handshakes* (SPIQE @ EuroS&P)
- C04 Kempf et al. 2024: *A Quantum of QUIC* (IFIP Networking)
- C05 Hoque, Aydeger 2026: *Energy-Aware… Post-Quantum TLS on Embedded User Equipment over… 5G* (arXiv / LCN)
- C06 Chou, Cao 2026: *Network Impact of Post-Quantum Certificate Chain sizes on Time to First Byte* (arXiv)

**D. Hybrid key exchange and PQ protocol design**
- D01 Bindel, Brendel, Fischlin, Goncalves, Stebila 2019: *Hybrid KEMs and Authenticated Key Exchange* (PQCrypto)
- D02 Barbosa et al. 2024: *X-Wing: The Hybrid KEM You've Been Looking For* (IACR CiC)
- D03 Schwabe, Stebila, Wiggers 2020: *KEMTLS* (CCS)
- D04 NIST 2024: *FIPS 203 (ML-KEM)*
- D05 Gupta, Rana 2026: *Transcript-Bound Combiners for Downgrade-Resilient Hybrid PQ Key Establishment* (arXiv)

**E. Forward secrecy in practice, HNDL, timelines and agility**
- E01 Blanco-Romero et al. 2026: *On the Practical Feasibility of Harvest-Now, Decrypt-Later Attacks* (arXiv)
- E02 Springall, Durumeric, Halderman 2016: *Measuring the Security Harm of TLS Crypto Shortcuts* (IMC)
- E03 Hebrok et al. 2023: *We Really Need to Talk About Session Tickets* (USENIX Security)
- E04 Adrian et al. 2015: *Imperfect Forward Secrecy (Logjam)* (CCS)
- E05 Valenta, Sullivan, Sanso, Heninger 2018: *In search of CurveSwap* (EuroS&P)
- E06 Mosca, Piani 2026: *Quantum Threat Timeline Report 2025* (Global Risk Institute)
- E07 Grover N. et al. 2026: *A Scenario-Based Evaluation of CRQC+AI Vulnerability Spectrum for TLS 1.3* (arXiv)
- E08 Wilson-Shah 2026: *Quantifying quantum risk: a measure of crypto agility* (arXiv)

**F. Shor resource estimates and demonstrations**
- F01 Roetteler, Naehrig, Svore, Lauter 2017: *Quantum resource estimates for computing elliptic curve discrete logarithms* (ASIACRYPT)
- F02 Häner, Jaques, Naehrig, Roetteler, Soeken 2020: *Improved quantum circuits for ECDLP* (PQCrypto)
- F03 Litinski 2023: *How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates* (arXiv)
- F04 Gidney, Ekerå 2021: *How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits* (Quantum)
- F05 Gidney 2025: *How to factor 2048 bit RSA integers with less than a million noisy qubits* (arXiv)
- F06 Babbush et al. 2026: *Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities* (arXiv)
- F07 Cain et al. 2026: *Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits* (arXiv)
- F08 Häner et al. 2026: *Computing 256-bit ECDLP in 26 days on a fault-tolerant trapped-ion quantum computer with 20,000 qubits* (arXiv)
- F09 Luo et al. 2026: *Quantum Algorithm for ECDLP with Space-Efficient Point Addition* (arXiv)
- F10 Putranto, Wardhani, Kim 2025: *Enhancing Quantum Cryptanalysis of Binary Elliptic Curves…* (IEEE Access; faculty)
- F11 Taguchi, Takayasu 2023: *Concrete Quantum Cryptanalysis of Binary Elliptic Curves via Addition Chain* (CT-RSA; faculty)
- F12 Tippeconnic 2025: *Breaking a 5-Bit Elliptic Curve Key using a 133-Qubit Quantum Computer* (arXiv)
- F13 Dallaire-Demers, Doyle, Foo 2025: *Brace for impact: ECDLP challenges for quantum cryptanalysis* (arXiv)

**G. Grover on AES and cost accounting**
- G01 Grassl, Langenberg, Roetteler, Steinwandt 2016: *Applying Grover's algorithm to AES* (PQCrypto)
- G02 Jaques, Naehrig, Roetteler, Virdia 2020: *Implementing Grover oracles for quantum key search on AES and LowMC* (EUROCRYPT)
- G03 Chen, Cai, Gao, Lin 2025: *Quantum circuit for implementing AES S-box with low costs* (arXiv; faculty)
- G04 Wang, Zheng et al. 2025: *Reducing quantum resources for attacking S-AES on quantum devices* (npj QI; faculty)
- G05 Mandal, Anand, Rahman, Sarkar, Isobe 2024: *Implementing Grover's on AES-based AEAD schemes* (Sci. Rep.; faculty)
- G06 Ulgen, Cildiroglu, Yayla 2026: *Quantum circuit realization and Grover cryptanalysis of… GFSPX* (Physica Scripta; faculty)
- G07 Bernstein 2009: *Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete?* (SHARCS; faculty)

**H. Migration, agility and notification**
- H01 Näther et al. 2024: *Migrating Software Systems towards Post-Quantum Cryptography: A Systematic Literature Review* (arXiv / IEEE Access)
- H02 Näther et al. 2024/2026: *Toward a Common Understanding of Cryptographic Agility: A Systematic Review* (arXiv / IEEE Access)
- H03 Li F. et al. 2016: *You've Got Vulnerability: Exploring Effective Vulnerability Notifications* (USENIX Security)

---

# PART 1: Thematic Extraction and Pattern Mapping

## 1.0 Theme map at a glance

| # | Theme | Papers | One-line verdict of the collective evidence |
|---|---|---|---|
| T1 | **Server-side PQ deployment is decided by infrastructure providers, not by sector or policy** | A01, A02, A03, A05, A07, A08, A09, C06 (+A06, E02, E03 on concentration) | About half of popular web domains now default to X25519MLKEM768, almost all of it via CDNs. Owner-managed servers, mail, finance back ends and domestic firms lag. There are 0% PQ certificates. |
| T2 | **The client stack decides what a mobile app actually gets** | A07, A08, B01, B02, B03, B04, B05, B06, B07, B08, B09 (+A02's device observation, E05's API clients) | Most apps inherit their platform's TLS defaults. Only big companies ship their own stacks. Developer customisation usually *lowers* security. Finance apps pin the most and add their own crypto on top of TLS. **No study has measured PQ key exchange inside mobile apps.** |
| T3 | **Paying for and designing the defence: PQ key exchange is cheap; certificates, lossy tails, and negotiation/fallback are the real risks** | A06, C01, C02, C03, C04, C05, C06, B01, D01, D02, D03, D04, D05 (+A01 RQ4, A04, E05) | ML-KEM-768 hybrid adds ~1.1–1.2 KB per direction and ~0 ms median over the Internet. The cost shows up in client CPU, lossy links and big PQ certificates. Hybrid combiners are provably robust if either half holds, but the *negotiation* must be protected. |
| T4 | **Forward secrecy in practice: shortcuts that let one key break open many sessions** | E01, E02, E03, E04, E05 (+A05 RSA transport, A07/C06/B01 resumption, B04 apps without FS, E08) | "Forward secrecy is a gradient, not binary" (E02). Key-share reuse, long-lived ticket keys, resumption without a fresh exchange, RSA key transport and shared secrets across domains multiply the sessions exposed per key. Only lab work (E01) has put this in quantum terms. |
| T5 | **Quantum price tags and timelines** | F01–F13, G01–G07, E06, E07 | The cost of breaking 256-bit ECDH has fallen ~1,000× in Toffoli count since 2017 (≈10¹¹ → ≈10⁷–10⁸), to ~1,200–1,450 logical qubits (835 for space-optimised variants). Grover on AES-128 stays at ≈2⁸³–2¹¹⁷ gates. Experts put a CRQC within 10 years at ~28–49% (for RSA-2048). |
| T6 | **Migration governance: agility, regulation, disclosure** | H01, H02, H03, E08 (+A05, B05, B06, B07, B08, A01 policy table, E06/E07 mandates, F06 disclosure model) | Migration practice is immature: no shared framework, ill-defined cryptographic inventories, few real migrations. Agility is a property of *layers*. Store and platform policy moves behaviour; notifications help only modestly. |

**The pattern across themes.** The literature splits along two seams:

1. **Measurement vs cryptography.**
   - T1, T2 and T4 *measure* deployed systems. Apart from E01, they never price what they find in quantum terms.
   - T5 *prices* attacks precisely. It never asks which real connections those prices apply to.
   - T3 *designs* defences and benchmarks them in labs.
   - Nobody joins the three: "this measured connection, from this app, costs a quantum attacker this much".
2. **Server vs client.**
   - T1 shows the server side moving fast, because a few providers flip a switch.
   - T2 shows clients, especially mobile apps, are governed by platform defaults and store policy.
   - The last time a TLS feature arrived (TLS 1.3, A07), Android apps lagged browsers and servers until the OS shipped it.
   - Nobody has checked whether the same lag is now happening for PQ key exchange.

This double seam (measurement × pricing, server × client) is where N1 sits.

---

## Theme 1 (T1): Server-side post-quantum deployment is provider-driven

### Core concept
Whether a TLS server offers or defaults to a PQ hybrid group depends mostly on **who terminates TLS**:
- a CDN or cloud edge (Cloudflare, Fastly, AWS CloudFront, Google), or
- the organisation's own servers ("owner-managed").

Providers can enable a hybrid group for millions of domains in one change. Owners must upgrade their libraries (e.g., to OpenSSL ≥3.5), configure groups, and test middleboxes. Measured adoption therefore tracks hosting composition more than sector, country or policy deadlines.

### Who addresses it

| ID | Authors, year | Method | Population / data | Headline |
|---|---|---|---|---|
| A01 | Wickramasinghe et al. 2026 | Custom TLS 1.3 client, 11 cloud vantage points, 3 rounds (Jul 2025, Nov 2025, Mar 2026), >2 billion handshakes | Stable panel of 684,494 Top-1M domains; per-country ccTLD/gov lists | Hybrid default 31.26% → 47.37% → 49.22%. **93.92% of PQ deployments infra-managed.** Cloudflare 57.34% of PQ defaults. Finance 59%, gov 38%. Policy deadlines do not predict adoption. |
| A02 | Dubey & Varshney 2026 | Selenium + Chrome DevTools (negotiated values), openssl, cURL | 32,011 domains (Tranco + 127 RBI-listed Indian banks) | X25519MLKEM768 49.30%. TLS 1.2 15.70%. 0% PQ certificates. BFSI "Low" (qualitative). Same bank negotiates differently on two devices. |
| A03 | Loizou & Ghadafi 2026 | OpenSSL probes offering 4 PQ groups, HTTPS + SMTP; logistic regression; HHI | 4,665 UK organisations, sector-stratified; snapshot 30 Jun 2026 | HTTPS 44.0% vs SMTP 6.4% (matched OR 16.89). **Provider AUC 0.957 vs sector 0.573.** Cloudflare 95.05% PQ; Microsoft mail 0%; Google mail 100%. |
| A05 | Balaji et al. 2026 | Configuration parser (nginx/Apache/Spring); bank proof of concept at OCBC | 8,443 GitHub nginx configs; one bank's 3-tier app | **0.0% PQ in configs; 28.9% allow RSA key transport.** Only 4 contexts set X25519MLKEM768. Java JSSE is classical by default. |
| A07 | Holz et al. 2019 | Active scans + passive (ICSI Notary, campus) + Lumen app data | Alexa 1M, 164M com/net/org, 88M ccTLD names | Historical analogue: Cloudflare hosted 59.8% of TLS 1.3 Alexa domains. ccTLD spread explained by dominant local hosters. |
| A08 | Ibrahim et al. 2026 | Raw ServerHello key_share inspection | 38 UK endpoints + testbed | "PQC deployment measurement requires OQS-capable client tooling". App-layer PQC can sit behind classical TLS. |
| A09 | Cho et al. 2025 | Live packet analyser, H/M/L scoring | 10 Korean vs 10 global companies | TLS 1.3 40% vs 90%; **hybrid 0% vs 40%**. Korean banks on TLS 1.2 + ECDHE_RSA. |
| C06 | Chou & Cao 2026 | netem + Zeek logs (NCSA) | Research-network traffic, 24 h + 16 months | Resumption on CDNs 80.30% (94.16% for TLS 1.3) vs 35.44% non-CDN. CDNs trim chains. |
| E02/E03 | Springall 2016; Hebrok 2023 | Repeated scans | Alexa 1M; Tranco/IPv4 | Concentration cuts both ways: one Cloudflare STEK group covered 62,176 domains (E02). An AWS load-balancer bug exposed ≥1.9% of the Tranco top 100k (E03). |
| A06 | Kwiatkowski et al. 2019 | Experiment design | Cloudflare edge + Chrome Canary (incl. Android) | The first PQ-TLS deployment experiments were run *by providers that control both ends* (Google client + Cloudflare server). |

### What the collective evidence says

1. **Adoption is about half of popular sites, and it is all one group.**
   - A01 (Mar 2026: 49.22% default) and A02 (49.30% negotiated) agree almost exactly. A03 finds 44.0% for UK organisations' primary websites.
   - Every PQ default in A01 is **X25519MLKEM768**. SecP256r1MLKEM768 is supported by 5.53% and never the default. Pure ML-KEM is essentially absent (ML-KEM-1024 0.66%).
   - 88.76% of PQ domains support exactly one PQ group, so there is no diversity to fall back on.
2. **Providers, not sectors, explain who has it.**
   - A01: >75% of infra-managed domains are PQ vs <10% of owner-managed.
   - A03: provider alone predicts HTTPS PQ status with AUC 0.957, sector alone 0.573. For SMTP the figures are 0.994 vs 0.156.
   - A01's policy test is decisive. Countries with earlier deadlines show *lower* mean adoption (32.4% vs 45.7%), but the difference vanishes within owner-managed domains (9.6% vs 8.4%) and within Cloudflare (93.5% vs 94.1%).
   - A07 found the same mechanism for TLS 1.3 in 2019: ccTLD differences were explained by dominant local hosters and Cloudflare.
3. **Concentration is extreme.**
   - Cloudflare + Fastly ≈ 70% of PQ defaults (A01).
   - Cloudflare = 69.7% of PQ HTTPS endpoints; top-3 = 86.9%; HHI 1,378 for HTTPS vs 2,797 for SMTP (A03).
   - Concentration is a double-edged sword. E02 showed that one secret can cover tens of thousands of domains (Cloudflare STEK group 62,176 domains; Google's two keys per 28 h covered all its ticket sessions). E03 showed that one provider bug can expose thousands of hosts (AWS ALB all-zero STEK on 1,903 Tranco-100k hosts).
4. **Where providers are not in charge, adoption collapses.**
   - Mail (A03: SMTP 6.4%; Microsoft 1,714 endpoints at 0%).
   - Owner-managed web servers (A01: 4.58% of PQ deployments).
   - Configuration templates (A05: 0.0% PQ; 28.9% still permit RSA key transport; 21.6%/19.4% permit TLS 1.1/1.0).
   - Domestic firms in Korea (A09: 0% hybrid vs 40% for global firms).
   - Bank internal Java stacks (A05: JSSE classical by default; the bank had to register BouncyCastle PQC providers explicitly).
5. **PQ coexists with legacy.** A01 RQ5: provider-managed PQ domains retain *more* legacy features than owner-managed PQ domains (TLS 1.0/1.1 18.0% vs 14.7%; deprecated ciphers 73.6% vs 49.9%). A PQ default does not mean a hardened configuration.
6. **Authentication has not started.** A01, A02, A03 and A09 all find **0% PQ or hybrid certificates**. D01's theory explains why this is not yet a confidentiality failure (T3).
7. **The measurement instrument shapes the number.** A08 shows that a client which does not *offer* PQ groups sees every server as classical. A02 measures what Chrome negotiates (client × server). A03 and A01 probe servers with PQ-capable clients. A05 reads configuration files. A09 inspects live packets. These quantities are not interchangeable (Debate 3).
8. **What T1 never measured.**
   - Mobile apps and app API endpoints (A01 by design).
   - Developing countries: A01's vantage points include Mumbai but nothing in Bangladesh, and A01's policy table has no South Asian jurisdiction except India.
   - Non-web services, except A03's SMTP.
   - Resumption modes and key-share reuse in the PQ era.
   - The client side, apart from A02's two-device anecdote.

**[N1] implications.**
- N1 can borrow A03's design: sector-stratified sampling, Wilson CIs, provider vs sector logistic regression, HHI.
- It can borrow A01's infra- vs owner-managed attribution for G8 (API vs website, hosting).
- It must probe with a PQ-capable client (A08's lesson).
- It should expect Bangladeshi finance *websites* to follow their hosting (CDN or own data centre), and must measure app **API hosts** separately, because no sampled list includes them.

---

## Theme 2 (T2): The client stack decides what a mobile app actually gets

### Core concept
- **Protection is a joint client × server property.** A server that supports X25519MLKEM768 protects a session only if the client *offers* it (A08). So for apps, the question is which TLS stack builds the ClientHello:
  - the platform default (Android Conscrypt/BoringSSL via OkHttp/HttpsURLConnection; iOS Network.framework),
  - a WebView,
  - a bundled stack (Cronet, Facebook Fizz, OpenSSL, Flutter/Dart BoringSSL), or
  - a third-party SDK's stack.
- **Defaults, platform APIs and store policy shape that ClientHello far more than developer intent does.**
- Finance apps add a second layer of their own cryptography on top of TLS (pinning, app-layer RSA/PIN encryption), and that layer has its own quantum exposure.

### Who addresses it

| ID | Authors, year | Method | Population | Headline |
|---|---|---|---|---|
| A07 | Holz et al. 2019 | Lumen on-device VPN capture (11.8M TLS connections, 56,221 apps) + passive | Global Android users | "Android does not provide native TLS 1.3 support to Android apps… only… apps from large companies… can use TLS 1.3." App support lagged servers; TLS 1.3 apps used their own stacks. |
| B04 | Razaghpanah et al. 2017 | Lumen + ClientHello cipher-list fingerprints | 7,258 apps, ~1.4M handshakes | **84% of app versions use OS-default TLS**. SDKs use OS defaults. ALPN was not exposed by the Android API, so apps needing it bundled their own TLS. Pinning 2.0%. |
| B05 | Oltrogge et al. 2021 | Static NSC analysis of 96,400 apps; Play safeguard experiments | 1.34M Play apps | 88.87% of custom NSC files *downgrade* security. NSC pinning 0.67% (finance 6%). Play safeguards accepted vulnerable code. NSC adoption followed target-SDK *policy*. "Customization is harmful." |
| B02 | Pradeep et al. 2022 | Static + dynamic MitM differential, Android vs iOS | 5,079 apps | Pinning: Popular 6.7% (Android) / 11.4% (iOS). **Finance is the top pinning category** (~21–23%). <½ of cross-platform apps pin consistently. iOS advertises weak ciphers ~93% vs Android 8% (platform default). |
| B01 | Mankowski et al. 2023 | Hotspot capture + tshark, 5 min per app | 90 German top apps, Android 11 | Median 94 handshakes per app, TLS 1.3 69%, ~31% of repeat connections resume. PQ auth would cost >8× bytes. The banking app made only 4 handshakes (no account). |
| B08 | Yang et al. 2026 (Okara) | LLM GUI agents + per-app VPN + MitM tests + ART hooks | 37,349 apps (Play + AppChina) | 22.42% MitM-vulnerable (Play 3.19% vs AppChina 39.40%). Third-party libraries cause 41% of vulnerable code. Median lifetime of a vulnerability 1,384 days. 726 disclosure emails, **0 replies**. |
| B09 | Jimenez-Berenguel et al. 2025 (PARROT) | Dockerised emulator + mitmproxy + key logging | 50–80 Vietnamese apps, launch-time | QUIC 45.3% of packets. TLS 1.3 = 90% of TCP-encrypted traffic. With mitmproxy only Instagram worked fully. |
| B03 | Strauss et al. 2025 | Static crypto-API analysis + LLM migration | 4,018 apps | App-layer RSA in ≈600–780 apps. No PQC. LLMs failed to produce correct PQC migrations. |
| B06 | Reaves et al. 2015 | Manual teardown + Qualys server tests | 7 mobile-money apps in 5 developing countries | 6 of 7 broken. DIY app-layer crypto (static keys, unauthenticated RSA key fetch). **RBI guidance drove app-layer PIN encryption.** |
| B07 | Mickey & Yanhaona 2024 | MASVS + AARDroid static analysis | 17 Bangladeshi finance APKs + SSLCommerz SDK | bKash flagged CRYPTO1–4. Two bank apps flagged for TLS validation. SDK worst. **No transport/PQ analysis.** |
| A08 | Ibrahim et al. 2026 | ServerHello inspection | Testbed | A client without PQ support makes every server look classical. |
| A02 | Dubey & Varshney 2026 | Chrome-negotiated values | One Indian bank on two devices | QUIC + TLS 1.3 + X25519 on one device, TLS 1.2 + ECDHE-RSA on another: "depends on both client and server". |
| E05 | Valenta et al. 2018 | Cloudflare ClientHello sample (4.19M) | Global clients | **API/app clients (okhttp/3.2.0, Python-urllib, uservoice-android) advertised long, weak curve lists**; >16% offered 80-bit curves, unlike browsers. |

### What the collective evidence says

1. **Apps inherit platform TLS.**
   - B04's 84% OS-default figure is the anchor.
   - A07 shows the consequence for a new TLS feature: TLS 1.3 reached Android apps through the OS release (Android Q) or through bundled stacks, so apps lagged both servers and browsers. Lumen's TLS 1.3 share was 4% in Mar 2019, while 39.8% of Notary clients offered TLS 1.3.
   - B02 shows the same mechanism across platforms: iOS apps advertised weak ciphers ~93% of the time vs Android 8%. That is a platform-default effect, not a developer effect.
2. **The API surface sets the ceiling.** B04 documents that Android exposed only SNI, cipher suites and protocol versions, so apps that needed ALPN had to bundle their own TLS library. **[N1]** This is the exact analogue of today's missing named-group knob on Android: if the platform API cannot request X25519MLKEM768, only apps with their own stack (Cronet, Fizz) can.
3. **When developers customise, security usually drops.**
   - B05: 88.87% of custom NSC files downgrade security, mostly by re-enabling cleartext; copy-paste of SDK snippets (MoPub); malformed pins.
   - B08: third-party libraries cause 41% of MitM-vulnerable code; one SDK's default-verifier override silently breaks the host app.
   - B06/B07: DIY app-layer crypto in finance apps is weak (static keys, 17-bit Blowfish keys, RSA keys fetched over HTTP; scanner flags in bKash and bank apps).
4. **Policy levers work; voluntary ones do not.**
   - B05: NSC adoption jumped only when the Android 9 / Play target-SDK requirement forced it.
   - B08: Google Play apps are 12× less MitM-vulnerable than AppChina apps (3.19% vs 39.40%).
   - B06: regulator text (RBI 2008) shaped app-layer crypto design.
5. **Finance apps are special in two ways.**
   - They pin the most: B02 finance ~21–23% of apps; B05 finance 6% via NSC; B04 32 finance apps pin, but 271 neither pin nor bundle CAs.
   - They layer their own crypto: B06 app-layer PIN encryption, B03 RSA in ≈600–780 apps, B07 crypto flags.
   - **[N1]** Pinning can break or block a PQ certificate migration (leaf/SPKI pins hard-code the server key; G9). App-layer RSA is HNDL-exposed even if TLS becomes PQ (G6).
6. **Mobile measurement methods are mature but have traps.**
   - The options:
     - hotspot + tshark (B01);
     - on-device VPN with per-app attribution (A07/B04 Lumen; B08 WireGuard per-app VPN incl. QUIC);
     - emulator + key logging (B09);
     - static APK analysis (B02, B03, B05, B07).
   - The traps:
     - Interception (mitmproxy) breaks pinned apps and suppresses QUIC (B09: only Instagram worked fully; QUIC usage fell from 50/50 to 35/50 apps).
     - Interception also replaces the server's key exchange with the proxy's, so it cannot measure the server-negotiated group.
     - Without login, finance flows are under-observed (B01, B02).
     - QUIC is half the traffic in some captures (B09) but almost absent in others (B08). See Debate 2.
7. **What T2 never measured:**
   - which key-exchange *group* apps negotiate in the PQ era;
   - Android vs iOS differences for PQ (iOS 26 enables X25519MLKEM768 system-wide per A02's software list);
   - framework attribution of PQ behaviour (OkHttp vs Cronet vs Flutter vs WebView);
   - SDK vs first-party PQ status;
   - real-account finance flows;
   - any South Asian app beyond B07's static scan.

**[N1] implications.** T2 supplies N1's core hypothesis ("app protection is decided by the platform/framework layer, not by the app or the server alone") and its methods (ClientHello fingerprinting for attribution; per-app VPN for QUIC; non-interception capture for key-exchange measurement; NSC/SPKI static analysis for pinning). It also supplies a historical precedent (TLS 1.3, A07) that turns N1's question into a testable prediction: *apps will lag servers and browsers until the platform default changes.*

---

## Theme 3 (T3): Paying for and designing the defence

### Core concept
The deployed defence is a **hybrid key exchange**: X25519 combined with ML-KEM-768. Two questions follow:

- **(a) What does it cost?** Bytes, round trips, CPU and energy, especially for clients on lossy mobile links.
- **(b) Is it designed correctly?**
  - Is the combiner robust if one half breaks?
  - Can an attacker strip the PQ option during negotiation?
  - What happens when clients fall back?

The authentication side (PQ certificates) is separate, more expensive, and theoretically less urgent for HNDL.

### Who addresses it

| ID | Authors, year | Setting | Headline |
|---|---|---|---|
| D04 | NIST 2024 (FIPS 203) | Standard | ML-KEM-768 ek 1,184 B, ct 1,088 B; category 3; recommended default. Combiners must be designed with care (SP 800-227). |
| D02 | Barbosa et al. 2024 (X-Wing) | Proofs + benchmarks | X25519 + ML-KEM-768 hybrid: pk 1,216 B, ct 1,120 B. **Secure if either half is secure** (C2PRI lets the big ciphertext stay out of the KDF). TLS relies on the transcript hash instead. |
| D01 | Bindel et al. 2019 | Theory | Two-stage adversaries. **CcQ = HNDL attacker.** For CcQ security, a quantum-safe KEM plus KDF suffices and signatures may stay classical. XOR-then-MAC and dualPRF combiners are robust. |
| D05 | Gupta & Rana 2026 | Theory + modelled embedded cost | Without transcript binding, a MitM downgrades a hybrid to classical with **probability 1** (2,000/2,000). Binding costs +11.8% compute but +1.5% energy. TLS 1.3 already binds; custom protocols may not. |
| D03 | Schwabe et al. 2020 (KEMTLS) | Protocol + netem | KEM-based authentication: −39% public-key bytes, server CPU −75–90%. KEMTLS-PDK suits apps with known servers. Some instantiations used schemes later broken (SIKE, Rainbow). |
| C01 | Paquin et al. 2020 | netem RTT/loss + data centres | Median dominated by compute at low loss. **Above 3–5% loss, big-message schemes degrade** (Frodo 16 packets vs 5–6). Kyber-class ≈ ECDH. |
| C02 | Sikeridis et al. 2020 | Real WAN, PQ certificate chains | Dilithium II +6.6% median. **Dilithium IV +110% (extra RTT past initcwnd).** Server signing speed matters. |
| C03 | Gómez-Cambronero et al. 2026 | LAN, 5-layer pcap decomposition | **Client ClientHello build 0.29 → 1.7–1.9 ms (~6×)**; end-to-end +18.7% in the lab; client CPU ~2×. key_share 1,216 B. |
| C04 | Kempf et al. 2024 | QUIC bare-metal | Kyber barely changes QUIC TTFB. PQ certificates collide with anti-amplification (3×) and implementation limits (LSQUIC failed >30 KB). AES-256 ≈ AES-128 cost. |
| C05 | Hoque & Aydeger 2026 | Raspberry Pi 5 over emulated 5G | ML-KEM swap ≈ zero latency/energy cost. **Signature choice dominates** (SLH-DSA ≈2× latency/energy). |
| C06 | Chou & Cao 2026 | netem + padded certificates | One extra RTT at chain sizes ~10 KB and ~40 KB. ML-DSA chains fit; SLH-DSA adds an RTT; Merkle Tree Certificates help. |
| B01 | Mankowski et al. 2023 | App traffic + size model | Full PQ (KEM + signatures) ≈ 11.5 KB per handshake, >8× today. Resumption and KEMTLS-PDK recommended for apps. |
| A06 | Kwiatkowski et al. 2019 | Design (+Langley 2018) | **~5% of clients saw outsized latency** with larger keys (middleboxes, lossy wireless). Android was part of the experiment. |
| A01 | Wickramasinghe et al. 2026 (RQ4) | 328,290 domains, matched pairs | **Median ΔT = 0 ms** (IQR ±5; p90 14 ms). +1,176 / +1,088 B. Fragmentation errors <0.16% of failures. |
| A04 / E05 / E07 §6.5 | Surveys / scans | Context | Key exchange migrates before authentication (A04). TLS 1.3 transcript signing blocks curve downgrades (E05). Middleboxes, resumption caches and libraries can cause "silent downgrade to a classical exchange" (E07, called out of scope). |

### What the collective evidence says

1. **The key-exchange defence is cheap on the wire.**
   - Sizes are fixed by D04/D02: +1,184 B client share and +1,088 B server share, i.e., +1,216/+1,120 B for the hybrid. A01 measured +1,176/+1,088 B medians in the wild.
   - Over real Internet paths, the median latency difference is 0 ms (A01).
   - In QUIC, Kyber barely moves TTFB (C04: Kyber768 4.23 vs X25519 3.91 ms on LSQUIC [calc +8%, ~0.3 ms]).
   - On an ARM board over emulated 5G, swapping to ML-KEM costs ~nothing (C05: 106 vs 106 ms).
2. **Where the cost lands.**
   - **On the client CPU:** keygen + decapsulation ~6× ClientHello build time; client CPU ~2× (C03).
   - **In the lossy tail:** C01 (loss >3–5%); A06/Langley (~5% of clients with outsized delays).
   - **In PQ certificates:** C02, C04, C06 (extra RTTs past ~10 KB/~40 KB; QUIC anti-amplification).
   - **In bespoke protocols that do not bind the transcript:** D05.
   - Lab overheads (C03 +18.7%; A05's internal test +23% connect time) are ~2–6 ms absolute and disappear behind 30+ ms RTTs. That reconciles the lab numbers with A01's 0 ms (Debate 1).
3. **The hybrid is robust by design, but only if it is negotiated.**
   - D01/D02 prove that a well-built combiner stays secure if X25519 falls (Shor) as long as ML-KEM holds (and vice versa).
   - D01 adds that for the HNDL attacker (CcQ), **only the KEM and KDF need to be quantum-safe**. Classical certificates today do not expose recorded traffic later.
   - D05 and E05 show that negotiation must be authenticated. TLS 1.3 does this (Finished MAC; transcript-signed CertificateVerify), so a *cryptographic* downgrade is blocked.
   - What remains is **legitimate fallback**: a client that retries without PQ after a middlebox failure, a HelloRetryRequest to X25519, a server preferring X25519, a library that does not recognise the group, or a resumption from a classical session. E07 §6.5 names these explicitly and leaves them out of scope. H02 also warns that coexistence periods raise downgrade risk "if negotiation and fallback behavior are not carefully controlled".
4. **Authentication is the expensive, later problem.** Signatures dominate cost (C05) and RTT penalties (C02, C06). The proposed fixes are KEMTLS (D03), KEMTLS-PDK for apps with hard-coded hosts (B01, D03), Merkle Tree Certificates (C06), and mixed chains (C02). None of them is deployed: 0% PQ certificates (T1).
5. **What T3 never measured:**
   - PQ key-exchange cost on low-end phones over real cellular radios, in Bangladesh or anywhere (C05 used a Pi with an emulated RAN; A01 used cloud vantage points);
   - the frequency of fallback and HRR in app traffic;
   - battery cost;
   - operator middleboxes in South Asia;
   - how pinning interacts with PQ certificates.

**[N1] implications.**
- G11 (cost on Bangladeshi networks): N1's pilot +12 ms median (n = 15, per `N1_Gap_Portfolio.md`) is consistent with C01/C03/A06. The expected cost is small at the median and visible in the tail and on weak devices.
- G10 (network path) and fallback/HRR logging come directly from D05/E07 §6.5.
- M3 (Toy-TLS) should keep the FO transform (D04) and a transcript-bound combiner (D01/D05) so the "hybrid survives Shor" demo is faithful.
- RQ-M1c is answered *theoretically* by D01/D02: classical-half key reuse does not expose a session whose ML-KEM half is fresh. It still matters for every session that fell back to classical.

---

## Theme 4 (T4): Forward secrecy in practice: shortcuts that make one key open many sessions

### Core concept
Ephemeral (EC)DHE is supposed to give **one key per session**, so stealing or breaking one key exposes one session. Real deployments take shortcuts:
- reusing "ephemeral" key shares,
- RSA key transport,
- session-ID caches,
- session tickets encrypted under long-lived STEKs,
- TLS 1.3 resumption without a fresh exchange (psk_ke) and 0-RTT,
- secrets shared across domains through common terminators.

Each shortcut stretches the **vulnerability window** and raises the number of sessions exposed per compromised key. A classical attacker would get that key by theft, legal compulsion or a bug. A future quantum attacker could compute it (Shor for public keys; Grover, in principle, for symmetric ticket keys). The classical literature measured the shortcuts; only E01 put them in HNDL terms, and only in a lab.

### Who addresses it

| ID | Authors, year | Method | Population | Headline |
|---|---|---|---|---|
| E02 | Springall et al. 2016 | 9-week ZMap scans incl. resumption | Alexa Top-1M (291,643 stable trusted domains) | ECDHE value reuse 15.5% (≥2× in 10 connections), 3.0% ≥7 days. **STEK reused ≥7 days 22%, ≥30 days 10%.** 38% have vulnerability windows >24 h. Cloudflare STEK group 62,176 domains. Jack Henry: 79 bank domains on one STEK for 59 days. |
| E03 | Hebrok et al. 2023 | Online + offline ticket tests | Tranco 1M/100k, IPv4 100k, full IPv4 | TLS 1.2 ticket compromise exposes issuing + resumed sessions. In TLS 1.3, **psk_ke and 0-RTT are exposed, psk_dhe_ke is not**. AWS ALB all-zero STEK (≥1.9% of Tranco-100k); 189 weak STEKs in IPv4. STEK algorithms: AES-128-CBC (BoringSSL/Apache/RFC) to AES-256. "Unauditability" of tickets. |
| E04 | Adrian et al. 2015 (Logjam) | NFS discrete log + scans | Top-1M, IPv4, IKE, SSH | **Precomputation per shared group amortises cost** across millions of servers. 17% of DHE hosts reused g^b; SChannel caches g^b for 2 h. One 1024-bit group → 17.9% HTTPS, 66% IKE, 25.7% SSH. Downgrade via an unsigned ciphersuite. |
| E05 | Valenta et al. 2018 | 10% IPv4 scans, Cloudflare client data | TLS/SSH/IKE | **22.9% of HTTPS hosts repeated the same P-256 share across two rapid scans.** TLS 1.3/SSH transcript signing blocks curve downgrade. 0.77% HTTPS fail point validation. |
| E01 | Blanco-Romero et al. 2026 | Loopback testbed (patched OpenSSL/OpenSSH) + cost model | Lab only | E (keys to break per session) × T_q. **0-RTT/psk_ke chains cascade from one ECDHE break.** KeyUpdate gives E = 1. TLS 1.2 RSA: one key → all sessions. Storage ≈ $1.1B/yr for a 1% harvest. Open problem: "economics of partial PQC deployment… concentrate harvesting on the shrinking classical remainder". |
| A05 | Balaji et al. 2026 | Configs | 8,443 nginx configs | **28.9% allow RSA key transport**; session cache shared 47.6%. |
| A07 / C06 / B01 | 2019 / 2026 / 2023 | Passive / Zeek / app capture | Notary / NCSA / 90 apps | Resumption: 9.7% of TLS 1.3 connections carry PSK, 0-RTT 6.8% (A07); **80.30% of CDN connections resume** (C06); ~31% of app repeat connections resume (B01). |
| B04 | Razaghpanah et al. 2017 | App fingerprints | 7,258 apps | Some messaging apps (BBM, Viber, Wire, Jio4GVoice) offered **only non-forward-secret suites**. |
| E08 | Wilson-Shah 2026 | Poisson model + NVD | 12 crypto libraries | Hybrid + agility needs rotation in hours to days. A live-attack model; rotation cannot rescue already-harvested traffic. |

### What the collective evidence says

1. **Forward secrecy is a gradient, not a switch.** 90.2% of trusted Top-1M sites used FS suites, yet 38% had vulnerability windows >24 h and 10% >30 days once shortcuts were counted (E02).
2. **Every shortcut is common.**
   - Key reuse: 15.5% ECDHE (E02, 10 connections), 22.9% of P-256 hosts (E05, two scans), 17% of DHE hosts (E04, 20 handshakes).
   - Ticket keys: 22% ≥7 days (E02).
   - RSA key transport: still allowed by 28.9% of configs (A05).
   - Resumption: majority behaviour on CDNs (C06: 80–94%) and common in browsers (E02: 50% of Firefox sessions).
3. **Shortcuts concentrate risk across organisations.** Shared session caches, STEKs and DH values link thousands of domains (E02: Cloudflare 30,163 / 62,176 domains; one ECDHE value seen on 179 domains). Banks on a shared provider shared one STEK for 59 days (E02, Jack Henry). Provider bugs propagate (E03, AWS/Stackpath).
4. **TLS 1.3 fixed some shortcuts and kept others.**
   - Fixed: RSA key transport removed; issuing session protected because tickets carry a derived resumption secret; NewSessionTicket encrypted (E03).
   - Kept: **psk_ke and 0-RTT still inherit the earlier handshake's exposure** (E03, E01). KeyUpdate is a deterministic hash chain, so it adds no new keys to break (E = 1, E01). Server key-share reuse is still possible in principle (E02/E05 measured it pre-1.3).
   - E02 criticised TLS 1.3 draft 15 for setting a 7-day PSK maximum "without discussion".
5. **Amortised cryptanalysis is the economic lens.**
   - E04's Logjam is the classical precedent: one expensive precomputation per shared group, then cheap per-target work.
   - E01 recasts HNDL as storage cost (α) × keys to break (E) × time per key (T_q), and notes that rekeying multiplies quantum work only where fresh key exchange happens.
   - **[calc, illustrative]** In E01's terms, a TLS 1.3 session with a fresh ephemeral share and no psk_ke resumption is exposed only by a key computation dedicated to that session. If a server reuses one X25519 share for 10,000 connections, a single computation exposes all 10,000. The exposure per compromised key rises by four orders of magnitude. This is the "amortisation factor" N1's M1 proposes to measure as a risk metric.
   - For quantum attacks there is no group-wide precomputation for a fixed curve analogous to NFS (E04/F-group). Amortisation therefore comes from **deployment shortcuts**, not from shared parameters. The F-group "state reuse" ideas (F03, F06) concern the attacker's algorithm and do not change this point.
6. **Symmetric ticket keys are not a cheap quantum target.** E03 shows STEKs are AES-128 or AES-256 and, being symmetric, are "unauditable" by clients. G02 shows Grover on AES-128 costs ~2⁹³–2¹¹⁷ gates under depth limits. Ticket keys therefore matter mainly through *classical* compromise (theft, bugs, compulsion) and through psk_ke inheritance, not as a Grover target (Debate 6).
7. **What T4 never measured:**
   - key-share reuse in the TLS 1.3 / hybrid era;
   - resumption modes (psk_ke vs psk_dhe_ke) actually used by apps;
   - ticket lifetimes and STEK rotation for app API hosts;
   - RSA key transport *negotiated* (not just allowed) by app clients;
   - any of this outside the US/EU top lists;
   - shortcuts quantified as "sessions per Shor run" on real servers (E01 explicitly lists real-network validation as open).

**[N1] implications.** T4 is the foundation for **M1** ("sessions per Shor run"). The literature gives the shortcut list (E02, E03, E05), the measurement method (repeated handshakes comparing key_share; ticket key-name prefix over time; psk_modes from captures) and the quantum cost unit (E01's E × T_q; F-group prices). It also gives a precise prediction for RQ-M1c from D01/D02 (T3): **server key reuse matters for classical and fallback connections, and is neutralised wherever the hybrid with a fresh ML-KEM share is negotiated.**

---

## Theme 5 (T5): Quantum price tags and timelines

### Core concept
Shor's algorithm breaks RSA and ECC in polynomial time, and Grover gives at most a quadratic speed-up against symmetric keys. Policy and risk depend on **concrete costs** (logical qubits, Toffoli/T gates, depth, physical qubits, runtime) and on **when** a machine of that size might exist. This theme collects the resource estimates, the cost-accounting rules that make them comparable (MAXDEPTH, area × time), the expert and model-based timelines, and the claims of hardware demonstration.

### Who addresses it

**(a) Shor against 256-bit ECC (the TLS key-exchange threat)**

| ID | Year | Logical qubits | Toffoli / T gates | Physical / runtime | Note |
|---|---|---|---|---|---|
| F01 Roetteler et al. | 2017 | **2,330** (P-256) | **1.26×10¹¹ Toffoli** | — | First simulated full point-addition circuit. ECC easier than RSA-3072 (6,146 q / 1.86×10¹³). |
| F02 Häner et al. | 2020 | 2,124 (low-width) / 2,871 (low-depth) | ~7.4×10⁹ T (low-W); T-depth down to ~1.9×10⁷ | (2,330 q ≈ 6.8×10⁷ physical, cited) | ×119 T-count, ×54–6,000 T-depth vs F01. |
| F03 Litinski | 2023 | ~6,000 (overestimate) | 44–109 M Toffoli per key | 9.4 M physical (baseline); minutes–hours with active volume | Photonic active-volume architecture (author's employer). |
| F06 Babbush et al. | 2026 | **1,200 / 1,450** | **≤90 M / ≤70 M Toffoli** | **<500,000 physical; ~18–23 min** (fast clock) | Circuits withheld; zero-knowledge proof of the cost. |
| F07 Cain et al. | 2026 | (uses F06 circuits) | 7–9×10⁷ | **~10,000–26,000 neutral atoms; ~1,000 → 10 days** | Slow clock, high-rate codes. |
| F08 Häner et al. | 2026 | ~1,450 | ~39–40 M Toffoli | **19,397 trapped ions; ~25.7 days; 63% success** | Full compiler with routing and loss. |
| F09 Luo et al. | 2026 | **835** (space-optimised) | ~2^30.88 ≈ 2×10⁹ Toffoli | — | Space–time trade-off. |
| F13 Dallaire-Demers et al. | 2025 | — | — | millions (conservative surface code) → <4×10⁴ cat qubits | Challenge ladder; 256-bit window **2027–2033**. |

**(b) Shor against RSA-2048 (certificates, legacy RSA key transport)**

| ID | Year | Headline |
|---|---|---|
| F04 Gidney & Ekerå | 2019/2021 | **20 M physical qubits, ~8 h** (0.1% gate error, 1 µs cycle). ~100× smaller volume than prior estimates. |
| F05 Gidney | 2025 | **<1 M physical qubits, <1 week**, ~1,409 logical. Endorses deprecating vulnerable systems after 2030 and disallowing them after 2035. |
| F07 Cain et al. | 2026 | ~11,000–14,000 atoms over ~10⁴ days; ~102,000 atoms ~97 days. |

**(c) Binary curves and small demonstrations**
- F10, F11 (faculty): binary-field ECC inversion and point-addition optimisations (FLT addition chains; out-of-place point addition). These give constant-factor gains on curves that TLS 1.3 removed.
- F12: a "5-bit key" run on IBM hardware using index arithmetic mod 32 (no EC arithmetic). Weak evidence.
- F13: a reproducible 6–256-bit ladder.

**(d) Grover against AES and cost accounting**

| ID | Year | Headline |
|---|---|---|
| G01 Grassl et al. | 2016 | AES-128 Grover **1.19·2⁸⁶ T gates, T-depth 2⁸⁰, 2,953 qubits**; AES-256 2¹⁵¹ T, 6,681 q. Conclusion: "prudent to move away from 128-bit keys". |
| G02 Jaques et al. | 2020 | Depth-optimised Q# oracles. AES-128 **1.34·2⁸³ gates without a depth limit; 1.07·2¹¹⁷ at MAXDEPTH 2⁴⁰; 1.07·2⁹³ at 2⁶⁴**. NIST category costs lowered by 11–13 bits. Multi-target attacks left open. |
| G03 Chen et al. | 2025 | Composite-field S-box. AES-128 circuit DW(T) = 102,800 (lowest to date). |
| G04 Wang, Zheng et al. | 2025 | S-AES (16-bit toy) oracle at 120 Toffolis. Variational attacks hard to train. "Significant challenges remain" for AES. |
| G05 Mandal et al. | 2024 | AEADs Rocca-S / AEGIS-128 / Tiaoxin under MAXDEPTH: 2²⁵³ / 2¹²⁴ / 2¹²⁴ at 2⁴⁰. Compared against NIST's updated thresholds 2¹¹⁷/2⁹³/2⁸⁴. |
| G06 Ulgen et al. | 2026 | Lightweight GFSPX: 1.12·2¹⁵⁹ gates; "below NIST Level 1 (2¹⁷⁰)" but astronomically costly. |
| G07 Bernstein | 2009 | Cost = machine size × time with communication. BHT quantum collision search is worse than classical parallel rho. |

**(e) Timelines and scenarios**

| ID | Headline |
|---|---|
| E06 Mosca & Piani 2026 | 26 experts; RSA-2048 in under 24 h. Within 10 years: 19/26 say >5%, 13/26 say ~50%+. **Average 28–49% within 10 years (≈2035)**; pessimistic 51% by 15 years, 69% by 20 years. Covert research could shift the timeline by ≥2 years. |
| E07 Grover N. et al. 2026 | Scenario model. RSA-2048 crossover 2029.9–2032.5 by track. Monte Carlo no-AGI median 2033, P(≤2035) = 0.95. Lattice breaks only under an undiscovered "dimension collapse" (ρ ≥ 0.52 for the TLS hybrid). |
| F13 Dallaire-Demers et al. 2025 | 2027–2033 window for 256-bit. |

### What the collective evidence says

1. **ECC-256 is the cheapest important target, and it keeps getting cheaper.**
   - F01 → F06/F08 cut the Toffoli count from 1.26×10¹¹ to ~4–9×10⁷ (≈1,400–3,000× fewer) [calc]. Logical qubits fell from 2,330 to 1,200–1,450 (835 in F09's space-optimised variant).
   - Physical requirements fell from tens of millions (F02's cited 6.8×10⁷) to <500,000 (fast clock, F06) and to 10⁴–2×10⁴ for slow-clock atoms and ions (F07, F08), at the cost of days to weeks per key.
   - F01, F02, F03 and F06 all state that **ECC falls before RSA** at equal classical security (e.g., F03: 256-bit ECC is 100–300× cheaper than RSA-2048 in active volume).
   - **[N1]** The X25519/P-256 part of today's TLS, which HNDL targets, is therefore the first to go. A RSA-2048-based survey (E06) understates the urgency for key exchange.
2. **Estimates converge across independent groups.** Google (F06), Oratomic/Caltech (F07), IonQ (F08) and Chinese academia (F09) all land at ~10³ logical qubits and ~10⁷–10⁹ Toffolis. Each is vendor- or group-specific, and the hardware is unbuilt, but the convergence across competitors is itself evidence.
3. **Fast-clock vs slow-clock changes who is targeted first** (F06, F07, F08).
   - Slow-clock machines (days–weeks per key) favour a few high-value, long-lived keys: RSA server keys used for key transport, CA keys, reused ephemeral keys.
   - Fast-clock machines (minutes per key) make per-session attacks practical.
   - **[N1]** This ranks HNDL exposures: long-lived and reused keys first, fresh per-session shares later.
4. **Symmetric crypto is not the weak point.** Under realistic depth limits, Grover on AES-128 costs ≈2⁹³–2¹¹⁷ gates (G02), vs ≈10⁸ (≈2²⁶–2²⁷) Toffolis to break one 256-bit ECDH key (F06). [calc: the gap is ~17 orders of magnitude with no depth limit (2⁸³ ≈ 10²⁵), ~20 at MAXDEPTH 2⁶⁴ (2⁹³ ≈ 10²⁸), and ~27 at MAXDEPTH 2⁴⁰ (2¹¹⁷ ≈ 10³⁵).]
   - Better AES oracles (G03) and toy-scale demonstrations (G04) do not change this.
   - NIST's categories are defined by AES key search. NIST lowered them after G02, and AEADs built from AES rounds still meet them (G05).
   - G07's discipline (count machine-time, including communication) is why "Grover halves the key length" is misleading as a *cost* statement (Debate 6).
5. **Timelines are uncertain but cluster in the 2030s.**
   - E06's experts: 28–49% within 10 years.
   - F13: 2027–2033.
   - E07's mechanism-backed RSA crossover: ~2030–2033.
   - F05 and E07 justify the 2030/2035 policy dates by risk management, not by a predicted date. F05: "because I prefer security to not be contingent on progress being slow".
   - The Mosca inequality (shelf life + migration time > threat time; E06, E07) turns any substantial probability inside a data shelf life into a reason to migrate now. E07's sector table puts payments/card data at X ≈ 5–10 years; E01 cites finance audit data at >7 years.
6. **Demonstrations are poor progress indicators.**
   - F06: progress is threshold-like, and "a public demonstration of Shor's algorithm on a 32-bit elliptic curve should not be seen as a wake-up call… [but] a potential signal that PQC adoption has already failed".
   - F12 shows how weak a "break" claim can be.
   - F13 offers a careful ladder but concedes canaries are imperfect.
   - Disclosure norms are shifting: F06 withholds circuits and publishes a zero-knowledge proof instead.
7. **Lattice PQC holds under current knowledge.**
   - E07's cost model: even at the conjectured sieving floor, ML-KEM-1024 costs ~2¹⁸²; a 2030s break would need an undiscovered structural collapse; HHL/annealing/VQE give no standalone break.
   - F06: the Regev/DQI and Kikuchi lines of work could eventually matter or boost confidence.
   - Implementation and side-channel attacks are rated more probable than structural breaks (E07).
8. **What T5 never addresses:**
   - which deployed connections the prices apply to;
   - how deployment shortcuts change the number of runs needed (T4);
   - multi-target Grover costs (G02's open question);
   - quantum costs for app-layer RSA/ECC inside apps (B03/B06/B07);
   - any toy end-to-end "hybrid TLS vs quantum attacker" model joining Shor on the classical half with the ML-KEM half surviving.

**[N1] implications.**
- **M2** ("from packets to qubits") can attach F06/F08 prices to every classical X25519/P-256 connection N1 measures, and F05 prices to RSA key transport. G02's MAXDEPTH costs go to the AES choice (M4/G15).
- **M3** (Toy-TLS) fills the "no end-to-end toy" gap, using a baby ML-KEM (D04), toy ECC (as in F12/F13's small curves, but with real EC arithmetic) and S-AES (G04).
- **M5** (legacy curves) is linked to F10/F11 but expected to find ~zero (E05: no server negotiated ec2n curves in 2016–17).

---

## Theme 6 (T6): Migration governance: agility, regulation and disclosure

### Core concept
Moving from classical to PQ cryptography is an **organisational process**: inventory, prioritise, migrate, maintain (H01). It is bounded by **agility**, i.e., how easily each layer (library, application, platform, OS, device, organisation) can change its cryptography (H02).

It is triggered and shaped by:
- **mandates and regulators**: NIST IR 8547, the US Executive Order, the Canadian/EU roadmaps, the RBI precedent;
- **platform and store policy**: Android target-SDK rules;
- **disclosure and notification** by researchers.

### Who addresses it

| ID | Authors, year | Method | Headline |
|---|---|---|---|
| H01 | Näther et al. 2024 | PRISMA SLR, 21 papers | Four phases (Diagnosis, Planning, Execution, Maintenance). **Cryptographic inventory ill-defined.** Only 10/21 report real migrations (Nginx, Db2, PostgreSQL, CA, …). Challenges: expertise, effort/cost, immature libraries, downgrade risk, legacy code. No mobile, finance or developing-country cases. |
| H02 | Näther et al. 2024/2026 | PRISMA review, 48 sources | Agility = "**changeability of cryptographic entities**". Layer model (primitive → … → organisation). OpenSSL provider/EVP agility, but no central cross-application policy. Coexistence raises downgrade risk. Agility cannot be universally quantified. |
| E08 | Wilson-Shah 2026 | Poisson model, NVD (12 libraries) | Required rotation time hours–days (λ OpenSSL 10.2/yr). Practice lags (>50% cannot patch critical vulnerabilities in 72 h). |
| H03 | Li F. et al. 2016 | Randomised notification experiments, ~310k vulnerable hosts | **Detailed direct emails → +11% remediation.** CERTs weak; US-CERT ≈ control. Translations worse. Repeat notices useless. Many countries lack a CERT. |
| B05 | Oltrogge et al. 2021 | Policy natural experiment | Target-SDK enforcement drove NSC adoption. Play's static checks failed. |
| B06 | Reaves et al. 2015 | Regulation reading | RBI 2008 guidance shaped app crypto. Vague "strong encryption" text may have contributed to failures. Most vendors never replied to disclosure. |
| B08 | Yang et al. 2026 | Disclosure | 726 developer emails, 0 replies. Calls for reliable app-store contact channels. |
| A05 | Balaji et al. 2026 | Bank practice | Visibility of configurations is the bottleneck. Migrate the outermost TLS termination first; Java providers need explicit registration. |
| A01 / E06 / E07 | 2026 | Policy context | 8-jurisdiction policy table (no Bangladesh). Canada plans by Apr 2026, high-priority systems by 2031. EU starts 2026, critical infrastructure by 2030. US: key establishment 31 Dec 2030, signatures 2031. NIST: deprecate 2030, disallow 2035. |
| E02, E03, E04, F06 | Various | Disclosure practice | Notifying named companies (E02); AWS fixed promptly, others silent (E03); browsers changed after Logjam (E04); withhold circuits + ZK proof (F06). |

### What the collective evidence says

1. **Migration is immature and inventory is the bottleneck.** H01 finds no agreed framework, mostly experimental implementations and few real migrations. A05 says banks cannot even see what each TLS termination point *permits*. **[N1]** N1's external measurement (which app endpoints and clients negotiate hybrid) is in effect a "cryptographic identification and assessment" instrument, i.e., H01's Diagnosis phase, for organisations and regulators that lack one.
2. **Agility lives in layers, and apps sit near the top.** H02's layer model explains T2. An app (application layer) is enabled *and constrained* by the platform and OS libraries beneath it. Apps that bundle their own TLS (B04, A07) trade inherited agility for self-maintenance. E08's rotation time adds the time dimension: server/CDN changes take hours, platform updates months, app updates depend on users.
3. **Policy works when it binds the layer that decides.**
   - Store and platform rules (B05) and provider decisions (T1) move behaviour.
   - National deadlines do not visibly move web adoption (A01) because most domains are not owner-managed.
   - Regulator text shapes app-layer crypto design for better or worse (B06).
   - Mandates are proliferating (A01's table; E06; E07). Bangladesh appears in none.
4. **Notification helps, a little.**
   - Best case +11% remediation with detailed, direct notices (H03).
   - Developer outreach often gets no reply (B08: 0/726; B06: most never replied).
   - Providers sometimes fix quickly (E03: AWS).
   - National CERTs vary from useful to inert (H03).
   - Effects are short-lived; re-notification does not help (H03).
5. **What T6 never addresses:**
   - migration readiness and regulator guidance in South Asia;
   - notification efficacy for *readiness* issues (not yet vulnerabilities), for finance apps, or in Bangladesh (BGD e-GOV CIRT, sector CIRTs);
   - developer/bank knowledge of PQ in developing countries (B03 only shows LLMs failing at migration);
   - agility measured empirically for mobile apps (H02's future work: beyond software exemplars).

**[N1] implications.**
- G13 (notification experiment) has a clear prior: modest effects, direct and detailed messages, randomised halves, a short response window (H03), low developer response (B08).
- G14 (human layer) fills the knowledge gap.
- N1's regulator recommendations can cite B05 (store policy) and B06 (RBI precedent) to argue for platform-level and Bangladesh Bank–level levers rather than reliance on individual app developers.

---

# PART 2: Consensus and Debate Finder

## 2.1 Major points of agreement

Each row is a conclusion that several independent papers reach. Where two of them use different methods, populations or years, the agreement is stronger, and the "Why it is robust" column says so.

| # | Point of agreement | Papers that reach it | Why it is robust |
|---|---|---|---|
| C1 | **X25519MLKEM768 is the only PQ key exchange deployed at scale**; other hybrids and pure ML-KEM are marginal | A01 (every PQ default), A02 (49.30%), A03 (1,787 of ~2,010 PQ endpoints), A09, A05 (4 configs), E07 (Cloudflare: >½ of human traffic PQ) | Three countries, three methods (server probe, browser negotiation, packet inspection) |
| C2 | **About half of popular web domains now default to hybrid PQ key exchange** | A01 49.22% (Mar 2026), A02 49.30%, A03 44.0% (UK orgs) | Independent samples and vantage points within months of each other |
| C3 | **0% PQ or hybrid certificates in the wild**; authentication migration has not started | A01, A02, A03, A09, A05 (certificates unchanged), A04 | Every measurement paper, every sample |
| C4 | **Infrastructure providers, not sectors or national policies, explain server-side adoption** | A01 (infra-managed 93.92%; policy test), A03 (AUC 0.957 vs 0.573), A07 (TLS 1.3 analogue), A02 (Cloudflare 37.97% of domains), A09 (global vs domestic) | Statistical test (A03), natural experiment (A01), historical replication (A07) |
| C5 | **Key exchange is migrated first; authentication is harder and later** | A04 (all 9 protocols), D01 (theory: CcQ needs only KEM+KDF), C02/C05/C06 (signature costs), C1/C3 above | Theory, survey and measurement agree |
| C6 | **PQ key exchange (ML-KEM) is cheap; PQ signatures/certificates are the expensive part** | C04 (Kyber barely moves TTFB), C05 (KEM swap ≈ 0; signature choice dominates), A01 (0 ms median), C02, C06, B01, D03 | Lab, WAN, QUIC, ARM board and Internet-wide data |
| C7 | **Where PQ costs do appear, they appear in the tail**: lossy links, middleboxes, big messages, slow clients | C01 (>3–5% loss), A06/Langley (~5% of clients), C03 (client CPU), C02/C06 (initcwnd), C04 (anti-amplification), D05 (radio energy) | Different decades and setups converge |
| C8 | **A well-built hybrid combiner is secure if either component is** | D01 (XtM, dualPRF), D02 (X-Wing), D05 (strongest-link bound), D04 (combiners need care) | Formal proofs from separate groups |
| C9 | **Negotiation must be authenticated, or hybrids can be downgraded** | D05 (downgrade probability 1 without binding), E04 (Logjam: unsigned ciphersuite), E05 (TLS 1.3 transcript signing blocks CurveSwap), H01/H02 (downgrade risk during coexistence), E07 §6.5 | Attacks (E04, D05) plus theory (E05) |
| C10 | **Mobile apps mostly inherit platform TLS defaults; only large firms ship their own stacks** | B04 (84% OS default), A07 (TLS 1.3 via OS or own stack), B02 (iOS vs Android cipher gap), B05 (defaults and policy drive NSC), A02 (device-dependent negotiation) | 2017–2022, Android and iOS, static and dynamic |
| C11 | **When developers customise TLS, security usually gets worse** | B05 (88.87% of custom NSC files downgrade), B08 (SDK overrides; 41% third-party), B06/B07 (DIY app crypto), B04 (weird custom suite lists) | Large-scale static analysis plus manual teardown |
| C12 | **Finance apps pin more than other categories and add their own crypto layer** | B02 (finance top on both platforms), B05 (finance 6% via NSC), B04 (32 finance apps pin), B06 (app-layer PIN encryption), B03 (RSA in apps), B07 (Bangladeshi bank-app crypto flags) | Several datasets and methods |
| C13 | **Forward secrecy is weakened in practice by reuse, tickets, caches and resumption** | E02, E03, E04, E05, E01, A05 (RSA transport configs), B04 (no-FS apps) | Measured 2015–2023, theory 2026 |
| C14 | **ECC-256 is a cheaper quantum target than RSA at equal classical security** | F01, F02, F03, F06, F07, F09, E07 | Every resource-estimate paper that compares the two |
| C15 | **Quantum resource estimates fall steadily ("attacks always get better")** | F04 → F05 (20M → <1M qubits), F01 → F06/F08 (10¹¹ → ~10⁷–10⁸ Toffoli), F06 Fig. 3, F08 intro, E07 Fig. 5, E06 | Independent groups' estimates over a decade |
| C16 | **Grover does not make AES-256 (or, realistically, AES-128) a practical target** | G01 (depth is the obstacle), G02 (MAXDEPTH), G03, G04, G05, G06, E07 (AES hypothesis-only), A04, F06 | Circuit work from several countries plus scenario work |
| C17 | **Lattice PQC (ML-KEM) has no known break; implementation/side-channel risk is more likely than a structural break** | E07 (cost model; ρ collapse required), F06 (Regev/DQI open), D04, D02, H01 (implementation immaturity) | Theory and survey agree |
| C18 | **Migration must start before a CRQC exists (HNDL / Mosca inequality)** | E06, E07, F05, F06, F13, E01, D01 (CcQ), H01 | Experts, modellers and resource estimators agree, with different motives |
| C19 | **Notification and developer outreach have limited effect; policy levers work better** | H03 (+11% best case), B08 (0/726 replies), B06 (vendors silent), B05 (target-SDK policy worked; Play checks failed), E03 (providers act) | Randomised experiment plus large field outcomes |
| C20 | **Cryptographic inventory and visibility are the practical bottleneck for organisations** | H01 (inventory ill-defined), A05 (banks lack configuration visibility), H02 (agility hard to assess), E07 §6.1 (agility = governance) | SLRs plus bank case study |

---

## 2.2 Major debates and contradictions

Each debate gives the positions, explains **why** the results differ, and says what N1 should do about it.

### Debate 1: Does post-quantum key exchange add noticeable latency?

| Position | Paper(s) | Number |
|---|---|---|
| No measurable cost | A01 | Median ΔT **0 ms** (IQR ±5; p90 14 ms), 328,290 domains |
| No cost at the median, cost in the tail | A06/Langley 2018; C01 | ~5% of clients see much larger delays; loss >3–5% hurts big messages |
| Small but clear cost | C03 | +18.7% end-to-end (16.54 → 19.63 ms); client ClientHello 6× |
| Moderate cost in production-like internal setup | A05 | Connect time **+23%** (24.7 → 30.4 ms), request time +1.3% |
| Negligible on an ARM device | C05 | ML-KEM-512 106 ms = P-256 106 ms; energy 151 vs 176 mJ |
| Barely visible in QUIC | C04 | Kyber768 4.23 vs X25519 3.91 ms TTFB [calc +0.3 ms] |
| Measured in N1's pilot | [N1] | +12 ms median (n = 15) |

**Why they differ:**
- **What the timer covers.** C03 and A05 time on sub-millisecond LANs, so ~2–6 ms of client CPU is a large fraction. A01 times over 30+ ms Internet RTTs, where the same few ms vanish in noise (its p90 of 14 ms is the tail).
- **Which group is compared.** A05 benchmarks ML-KEM-512 against X25519, not the hybrid it deploys. A01 compares the hybrid against its own X25519 half (matched pairs). C05 swaps KEMs with fixed certificates.
- **Network conditions.** C01 and Langley show that loss and middleboxes create the tail. A01 uses only well-provisioned cloud paths (its own stated limitation). C05's RAN is emulated, with no radio.
- **Device class.** C03's cost is client-side compute. On low-end ARM phones without AVX2 it could matter more than on cloud VMs. Nobody has measured low-end phones.

**Verdict:** consistent once you separate absolute from relative cost and median from tail: a few ms of client CPU plus ~1 KB per direction. **[N1]** G11 must measure on Bangladeshi operators and low-end devices and report tails (p90/p99) and failures, not just medians.

### Debate 2: How much mobile app traffic is QUIC?

| Position | Paper | Number and unit |
|---|---|---|
| About half | B09 (PARROT) | **QUIC 45.3% of packets** (50 apps, 2025) |
| Almost none | B08 (Okara) | **UDP/QUIC 0.22% of flows** (37k apps) |
| A minority | B01 | Median **9 QUIC handshakes** vs 94 TLS handshakes per app [calc ≈9%] |
| About a third of sites offer it | A02 | QUIC/HTTP3 on 31.89% of domains (server support) |

**Why they differ:**
- **Unit of measure:** packets (B09; bulk video and data inflate them) vs flows (B08) vs handshakes (B01) vs server support (A02).
- **Interception mode:** B08 routes traffic through mitmproxy for its MitM tests, and B09 shows interception suppresses QUIC (50/50 apps use QUIC without the proxy, 35/50 with it). B08's 0.22% is therefore likely depressed by design.
- **App set and stage:** B09 captures first launch of Vietnamese apps (Google and Facebook-heavy); B01 captures 5 minutes of German top apps; B08 drives GUIs with LLM agents across Play and AppChina.
- **Year:** B01 (Jan 2023) vs B09 (2024–25).

**Verdict:** QUIC is substantial for big-platform apps and small elsewhere. The headline depends on the unit. **[N1]** Capture QUIC without interception (per-app VPN or hotspot), report both flow share and handshake share, and parse QUIC Initial packets for key_share. Never quote B09's 45% as a population figure (Correction 2).

### Debate 3: What does "PQ adoption" measure, and who decides it?

| Approach | Paper | What it really measures |
|---|---|---|
| Server probe with PQ-capable client | A01, A03 | Server *support* and server *default* |
| Browser-negotiated values | A02 | Client (Chrome) × server outcome for one browser |
| Raw ServerHello inspection | A08, A09 | Negotiated group for whatever client was used |
| Configuration files | A05 | What servers are *configured to permit* (incl. unused fallbacks) |
| App traffic capture | B01 (pre-PQ), [N1] | What apps actually negotiate |

**Why they differ:**
- A03 criticises A02 for conflating client and server. A08 shows a non-PQ client reports 100% classical. A05 argues scans miss permitted-but-unused fallbacks (TLS 1.0, weak ciphers) that configs reveal.
- Each is right about a different quantity:
  - Server probes answer "could a modern client get PQ?"
  - Captures answer "did this app get PQ?"
  - Configs answer "what could an attacker downgrade to?"

**Verdict:** these are three layers of one property. **[N1]** N1's design combines them by construction: server probes for API hosts (G8), app captures (G4), and static APK/NSC signals (G9, G12). Layer attribution is the contribution. Always log both ClientHello offers and the ServerHello choice (A08).

### Debate 4: How ready is the finance sector?

| Paper | Population | Finance readiness |
|---|---|---|
| A01 | Finance domains in Top-1M (n = 24,563) | **59%** hybrid default, *above* the average |
| A03 | UK Finance & Insurance organisations (n = 425) | **177/425 ≈ 41.6%**, *below* government (~56%) |
| A02 | 183 BFSI domains incl. 127 Indian banks | **"Low"** (qualitative heatmap); one bank TLS 1.2 on some devices |
| A09 | Korean banks/finance (Shinhan, Toss, Kiwoom) | **0% hybrid**; TLS 1.2 + ECDHE_RSA |
| A05 | Bank-like nginx configs on GitHub; OCBC internal stack | **0.0%** PQ in configs; internal stack classical until manually upgraded |
| B-group | Finance apps | **Never measured** for PQ |

**Why they differ:**
- **Sampling frame:** A01's "finance" is popular finance *websites* (fintech, payment and media sites on CDNs). A03's is registered UK companies by SIC code (many small firms on small hosts). A02's is a short list of Indian banks. A09's is 3–4 Korean firms.
- **Hosting composition (C4):** CDN-fronted finance sites inherit PQ; banks on their own data centres or domestic hosts do not.
- **Layer:** A05 looks at internal and back-end stacks, where nothing is PQ by default (Java JSSE).
- **Geography:** domestic finance lags global firms (A09). A02 hints the same for India.

**Verdict:** "finance readiness" is not one number. Front-end websites on CDNs look good; domestic banks, internal stacks and (unmeasured) app back ends probably do not. **[N1]** G4/G8 should stratify by hosting and report website vs API host for the *same* organisation. That is the cleanest test of "web studies overestimate readiness".

### Debate 5: How common is certificate pinning, and does it matter for PQ?

| Paper | Measure | Number |
|---|---|---|
| B04 (2017) | Dynamic, first-party pins | 2.0% of apps; finance: 32 pin, 271 don't |
| B05 (2021) | NSC pin-sets only | **0.67%**; finance 6% |
| B02 (2022) | Static + dynamic differential | Popular 6.7% (Android) / 11.4% (iOS); finance ~21–23% |
| B08 (2026) | Pinning bypass with attacker CA installed (T3 test) | ~75% of apps / 98.6% of FQDNs bypassable |

**Why they differ:**
- **Detection method:** NSC-only (B05) misses code and library pinning, so B02 finds up to 4× more.
- **Sample:** popular vs random apps (B02: Random 0.9–2.5%).
- **Platform:** iOS pins more.
- **Year.**
- **Definition:** B08 measures whether pinning *holds*, not whether it exists.
- B02 also finds 80/110 matched pins are CA-level and 24/30 leaf pins are SPKI hashes.

**Verdict:** pinning is rare overall but concentrated in finance and payment SDKs. Most pins are CA-level, which survives a CA's key migration only if the CA keeps its key. Leaf/SPKI pins hard-code the server key, so **a PQ certificate (or a Merkle Tree Certificate) forces an app update**. None of the four papers asks this question. **[N1]** G9 is uncontested territory.

### Debate 6: How much does Grover weaken AES-128, and should apps use AES-256?

| Position | Paper(s) | Claim |
|---|---|---|
| "AES-128 offers 64-bit quantum security" (naive k/2) | A02, A05, A09; G01's conclusion; E07 (AES-256 "only level" meeting 128-bit) | Treat AES-128 as quantum-weak; prefer AES-256. A09 even labels NIST level-1 PQC "vulnerable". |
| Depth-limited cost is astronomically high | G02 (2⁹³–2¹¹⁷ under MAXDEPTH), G05 (NIST's updated thresholds), G06 (2¹⁵⁹ "below Level 1" yet infeasible), G07 (count machine × time), E07 (AES "hypothesis-only"; Grover parallelises poorly) | AES-128 is not a realistic target. AES-256 is conservative policy (CNSA 2.0), not a necessity. |
| Performance is no excuse either way | C04 | AES-256 ≈ AES-128 throughput on servers with AES-NI; ChaCha20 better on phones without AES hardware |

**Why they differ:**
- **Cost model:** query count (2⁶⁴ iterations) vs circuit cost with depth limits and parallelisation (√S penalty).
- **Purpose:** compliance labelling (CNSA 2.0 requires AES-256) vs cryptanalytic feasibility.
- **Audience:** measurement papers adopt the simple label for a dashboard; cryptanalysts cost the full circuit.
- **Policy categories:** NIST defines Category 1 *as* AES-128 key search, so calling AES-128 "quantum-vulnerable" is circular in NIST's own framework.

**Verdict:** for HNDL, AES-128 record keys and STEKs are not the weak point; the (EC)DH key exchange is (C14, C16). AES-256 is a reasonable policy choice that costs nothing on servers. **[N1]** M4/G15 should report the cipher with MAXDEPTH-aware cost (G02/G05), not a 64-bit label, and should say plainly that the finding is about policy alignment (CNSA 2.0), not imminent breakability.

### Debate 7: How prevalent is session resumption, and what does it mean for HNDL?

| Paper | Population | Resumption measure |
|---|---|---|
| E02 (2016) | Alexa 1M servers | 83% support session IDs, 76% tickets; Firefox 50% of sessions resumed |
| A07 (2019) | ICSI Notary TLS 1.3 connections | PSK in 9.7%; 0-RTT in 6.8% (70% of resumption attempts) |
| B01 (2023) | 90 Android apps | ~31% of repeat connections resumed (median); Candy Crush 900/917 |
| C06 (2026) | NCSA research network | **CDN 80.30% (TLS 1.3: 94.16%)**; non-CDN 35.44% |
| E03 (2023) | Tranco/IPv4 | 82% of Tranco-100k servers issue tickets; ~95% of issuers resume |

**Why they differ:**
- **Unit:** server capability (E02, E03) vs share of connections (A07, C06) vs share of repeat connections (B01).
- **Population:** browsers and campus vs research-network users vs apps.
- **Period:** TLS 1.3 was new in 2019.
- **Destination:** CDNs keep resumption state and share ticket keys across edges, while owner-managed servers often do not (C06).

**What it means:**
- Resumption is common and is the *majority* mode toward CDNs. Its quantum relevance depends on the PSK mode.
- **psk_dhe_ke** runs a fresh (EC)DHE or hybrid exchange, so each resumption is independently protected.
- **psk_ke** and 0-RTT inherit the original handshake's key, so the resumed sessions share its exposure (E03, E01).
- None of the five papers reports the psk_ke vs psk_dhe_ke split for real clients. **[N1]** G15/M1(c) measures exactly this split for apps.

### Debate 8: When will a CRQC arrive, and how should progress be tracked?

| Source | Basis | Estimate |
|---|---|---|
| E06 | Survey of 26 experts (RSA-2048 in <24 h) | 28–49% within 10 years (≈2035); ~51–69% by 15–20 years (pessimistic interpretation) |
| E07 | Scenario model (vendor authors) | RSA-2048 50% crossover ~2030–2033; no-AGI Monte Carlo median 2033 |
| F13 | Resource estimates × public roadmaps | 256-bit ECDLP window 2027–2033 |
| F05 | Resource estimate author's view | No date predicted; supports deprecate 2030 / disallow 2035 as risk management |
| F06 | Resource estimates + architecture analysis | First CRQC may be "detected rather than announced"; time remaining "still exceeds" migration time, "margin… increasingly narrow" |
| F12 | Hardware "demonstration" | Claims Shor "continues to scale" from a 5-bit toy |

**Why they differ:**
- **Target problem:** RSA-2048 (E06, E07) vs ECC-256 (F13, F06). ECC-256 is cheaper (C14), so ECC-based windows are earlier.
- **Method:** expert opinion with coarse, uneven bins and a changing panel (E06) vs parameterised models with chosen couplings (E07) vs roadmap overlays (F13).
- **Incentives:** E06 (evolutionQ) and E07 (EnQuanta) sell quantum-safe products; F06, F07 and F08 are hardware vendors. Each states its interest.
- **Progress metric:**
  - qubit counts (criticised by F06 as "era of ferment" thinking);
  - small-curve ladders (F13: "imperfect canaries");
  - demonstrations (F12: weak);
  - threshold milestones (F06: below-threshold error correction, interconnects; E06: 5–10 logical qubits with non-Clifford gates by mid-2026).

**Verdict:** the sources agree on the *decision* (migrate key exchange now; C18) and differ on the date by roughly ±5 years. **[N1]** Use E06 as a conservative RSA-based proxy, F06/F08/F13 for the ECC-256 threat to key exchange, and the Mosca inequality with finance data shelf lives (≥7–10 years; E01, E07) rather than any single date. Do not cite F12 as progress.

### Debate 9: Does policy drive PQ adoption?

| Position | Paper(s) | Evidence |
|---|---|---|
| No, hosting composition does | A01, A03 | Earlier-deadline countries adopt *less* overall but equally within the same hosting class; provider AUC ≫ sector AUC |
| Yes, policy must drive it because the public will not | E07 (public awareness ~25–30%; "pressure… must be driven primarily by regulation"), E06/E07/F05 (deadlines), H01 (adoption expected to follow NIST standards) | Arguments and mandates, not outcome measurements |
| Yes, when the policy binds the deciding layer | B05 (target-SDK rule drove NSC adoption), B06 (RBI text shaped app crypto), B08 (store governance: Play 3.19% vs AppChina 39.40% vulnerable) | Natural experiments on platforms and stores |

**Why they differ:** A01 tests *national* deadlines against *web servers*, most of which are run by global CDNs that do not answer to national deadlines. B05 tests a *store* policy against *apps* that must comply to be published.

**Reconciliation:** policy works when it binds the layer that actually decides (provider, platform, store or regulator of a specific sector). **[N1]** For Bangladeshi finance apps the deciding layers are the platform (Android/iOS defaults), the app's framework, and the bank's own API gateway. That points to Bangladesh Bank guidance aimed at API gateways and app frameworks, and to platform defaults, rather than general national deadlines.

### Debate 10: Do bigger groups or more rekeying protect recorded traffic?

| Position | Paper | Claim |
|---|---|---|
| Yes, partially | E01 | Larger groups (P-384) raise the per-instance quantum time T_q. Rekeying (e.g., SSH RekeyLimit) multiplies the keys an attacker must break (E = 37 for 5 MB at 64 KB). |
| Little or none | F06 | Larger curves give "at best partial and temporary, at worst nearly non-existent" protection: a 1024-bit curve needs only ~5,000 logical qubits, and early CRQCs trade memory for time. |
| Not available in TLS 1.3 | E01 | TLS 1.3 KeyUpdate is a deterministic chain (E = 1); fresh-DH rekeying needs new connections (psk_dhe_ke); Extended Key Update drafts are not deployed. |
| Historical analogue | E04 | Moving from 1024- to 2048-bit DH raised precomputation ~10⁹×. That worked classically because NFS scales sub-exponentially. Shor does not. |

**Why they differ:** E01 reasons about cost multipliers for a *given* machine. F06 reasons about how quickly machines scale. E04's lesson does not transfer, because Shor's cost grows only polynomially with key size.

**Verdict:** bigger classical groups are not a PQ defence; hybrid ML-KEM is. Fresh key exchange per connection (psk_dhe_ke, no 0-RTT, no key reuse) keeps the attacker paying per session. **[N1]** Recommend hybrid plus psk_dhe_ke, not P-384.

### Debate 11: How common is ephemeral key-share reuse?

| Paper | Population / year | Measure | Result |
|---|---|---|---|
| E04 | IPv4 DHE hosts, 2015 | Same g^b at least once in 20 handshakes | 17% (15% used one value only) |
| E02 | Alexa 1M, 2016 | ≥2 identical values in 10 connections; ≥7 days in daily scans | ECDHE 15.5% / 3.0%; DHE 7.2% / 1.2% |
| E05 | 10% IPv4 HTTPS, 2016 | Same secp256r1 share in two rapid scans | **22.9%**; 2.7% shared across hosts |
| E05 | Other ports | Same | LDAPS 65%, NNTPS 83%, 8443 22% |
| E01 | Lab | Assumes fresh shares | — |

**Why they differ:**
- **Definition and window:** "ever repeated in 10 or 20 connections" vs "same in two rapid scans" vs "same across days".
- **Population:** Alexa sites vs all IPv4 hosts (more embedded devices and appliances).
- **Software defaults:** OpenSSL without SINGLE_DH_USE, SChannel 2 h caching, F5 settings (E04).
- **Year:** OpenSSL removed DHE reuse in Jan 2016 (E02).

**Verdict:** key reuse was common pre-TLS 1.3 (≈15–23% of hosts in short windows). **No measurement exists for TLS 1.3 / X25519 / hybrid servers**, and none for app API hosts. **[N1]** M1(a) re-measures it for Bangladeshi finance and API hosts versus global CDNs. Because of D01/D02, it should report reuse separately for connections that negotiated hybrid and connections that fell back to classical.

### Debate 12: Does disclosure and notification work, and how much should be disclosed?

| Position | Paper(s) |
|---|---|
| Notification helps, modestly | H03 (+11% with detailed, direct notices) |
| Developers rarely respond | B08 (0/726), B06 (most never replied) |
| Providers fix fast when told | E03 (AWS fixed promptly; Stackpath silently) |
| CERT relays are unreliable | H03 (US-CERT ≈ control; many countries have no CERT) |
| Withhold attack details, prove costs | F06 (circuits withheld; zero-knowledge proof) vs the earlier full-disclosure norm (F01–F05 published circuits) |

**Why they differ:** recipient type (network operators vs app developers vs large providers), issue type (exploitable vulnerability vs readiness gap), channel (WHOIS abuse vs app-store contact vs CERT), and era.

**[N1]:**
- G13 should send direct, detailed notices to the responsible operator (bank IT, API gateway owner), randomise, and re-measure within weeks.
- It should expect low developer response.
- It should handle sensitive pilot findings privately before publication (as N1's own plan requires).

## 2.3 Summary: recurring reasons results diverge

| Reason | Debates where it matters |
|---|---|
| **Unit of measure** (packets vs flows vs handshakes vs domains vs configs vs connections) | 2, 3, 7, 11 |
| **Vantage point** (cloud VPs vs residential/mobile; server probe vs client capture; interception vs not) | 1, 2, 3, 4 |
| **Which client offers what** (non-PQ client sees no PQ; Chrome vs app stack) | 3, 4 |
| **Sampling frame** (Top-1M sites vs registered companies vs bank lists vs app stores) | 4, 5, 9 |
| **Hosting composition** (CDN vs owner-managed) | 4, 7, 9 |
| **Lab vs Internet; median vs tail** | 1 |
| **Cost model** (query count vs depth-limited circuit cost vs area × time) | 6, 8, 10 |
| **Target problem** (RSA-2048 vs ECC-256) | 8 |
| **Period** (pre-/post-TLS 1.3; 2016 vs 2026) | 2, 5, 7, 11 |
| **Incentives and conflicts of interest** (vendors, consultancies) | 8 |
| **Definition** (pinning exists vs holds; reuse within 10 connections vs days) | 5, 11 |

---

# PART 3: Research Gap Exposer

## 3.1 Variables, populations and contexts these authors overlooked

### (a) Populations never studied

| Overlooked population | Evidence that it is missing | Closest work |
|---|---|---|
| **Mobile apps in the PQ era** (what group apps negotiate) | No paper measures key-exchange groups in app traffic after the hybrid rollout. B01 (Jan 2023) is pre-PQ and records no groups. A01 never mentions apps. | B01, A07, B04 |
| **Finance apps with real accounts** | B01's banking app made 4 handshakes (no account). B02 had no logins. B09: pinned apps failed under mitmproxy. B08: authentication flows 4.06%, financial 0.75% of vulnerable flows. | B06 (accounts in India, 2015) |
| **Bangladesh / South Asia** | No measurement paper samples Bangladesh. A01's vantage points include Mumbai, not Dhaka. A01's policy table includes India only. A02 covers Indian banks. A07's 54 ccTLDs exclude .bd. B06 covers no Bangladeshi app. B07 is static only. | B07 (static scan of 17 APKs), A02 (India) |
| **App API back ends** | All server scans use web-domain lists (Top-1M, Tranco, ccTLD, FAME, GOV.UK). B04's own future work asks for "active server-side measurements of mobile app servers vs web servers". | B04 (future work), A05 (bank internal stack) |
| **iOS vs Android for the same app (PQ)** | B02 compares pinning/ciphers, not key exchange. iOS 26 enables X25519MLKEM768 system-wide (A02's list), Android's platform API does not expose groups (B04 analogue). No PQ comparison exists. | B02 |
| **Low-end Android phones on real cellular radio** | C03: LAN VMs. C05: Raspberry Pi + emulated RAN. A01: cloud VPs. A06's design planned mobile analysis, but its results were never published in the paper. | C05, A06 |
| **Third-party SDK traffic (PQ status)** | B04/B08 show SDKs follow OS defaults and cause many TLS bugs. B01 lists "attribute connections to ad/analytics libraries" as future work. Nobody measured SDK vs first-party PQ status. | B04, B08, B01 (future work) |
| **Mobile money (MFS) platforms** | B06 (2015, 7 apps, no Bangladesh) is the only teardown. bKash/Nagad/Rocket are scanned statically only in B07. | B06, B07 |
| **Domestic vs global firms in a developing country** | A09 does this for Korea only (n = 10 vs 10, desktop, IPv4/TCP). | A09 |
| **Developers and bank security teams in developing countries** | No interview or survey study. B03 shows LLMs fail at PQ migration. H01 finds "education & expertise" a top challenge, but in European cases. | H01, B03 |

### (b) Variables rarely or never controlled

| Variable | Why it matters | Who comes closest | Status |
|---|---|---|---|
| **Client stack / framework** (OkHttp, Cronet, WebView, Flutter, React Native, platform version) | Decides whether X25519MLKEM768 is *offered* (A08; B04 analogue) | B04 (fingerprints, 2017), A07 | Not measured for PQ |
| **ClientHello offers vs ServerHello choice** | Separates "client didn't offer" from "server didn't pick" (layer attribution) | A08 (method), A02 (anecdote) | Not measured at scale |
| **Resumption PSK mode** (psk_ke vs psk_dhe_ke) and 0-RTT | psk_ke/0-RTT inherit exposure; psk_dhe_ke does not (E03, E01) | A07 (PSK/0-RTT counts), C06 (rates), B01 (rates) | Mode split never reported |
| **Ephemeral key-share reuse in TLS 1.3 / hybrid** | Multiplies sessions exposed per key (E02, E05) | E02/E05 (pre-1.3) | No TLS 1.3/hybrid data |
| **Fallback / HelloRetryRequest / downgrade-by-failure** | "PQ-capable" ≠ "PQ-negotiated" (D05, E07 §6.5, H02) | A07 (HRR 4%), A01 (failure taxonomy) | Never measured for PQ in apps |
| **RSA key transport actually negotiated** (not merely allowed) | One key exposes all recorded sessions (E01) | A05 (configs allow 28.9%) | Never measured in traffic |
| **Ticket lifetime / STEK rotation for API hosts** | Classical theft window; psk_ke chains | E02, E03 (web) | Not for API hosts |
| **QUIC key exchange in apps** | QUIC is a large share of some app traffic (B09); A09 ignored it | C04 (lab), B08 (VPN captures) | Not measured for PQ in apps |
| **App-layer public-key crypto** (RSA PIN encryption, JWT RS256, embedded keys) | Exposed even if TLS is PQ; some needs no interception (A04 OIDC) | B03, B06, B07, A04 | Never quantum-costed per app |
| **Data lifetime of flows** (e-KYC, statements vs telemetry) | Mosca X differs by flow (E06, E07) | E07 (sector table), B08 (flow functions) | Not linked to PQ status |
| **Operator network path** (middleboxes, MTU, loss) in South Asia | Tail costs and failures (A06, C01) | A06 (design), A01 (cloud paths only) | Not measured |
| **Pinning type × PQ certificate size** | Leaf/SPKI pins block key migration; big chains add RTTs (C06) | B02, B05, C06 | Interaction never studied |
| **Quantum cost per measured connection** | Turns deployment data into risk | E01 (lab model) | Never done on real data |

### (c) Contexts left unexamined

1. **Regulatory context in Bangladesh.**
   - Bangladesh Bank's ICT guidelines are not discussed by any paper. B06 shows regulator text shapes app crypto (RBI 2008).
   - A01's policy table and E06/E07's mandate lists have no Bangladeshi entry.
2. **Platform/store policy as a PQ lever.** B05 shows target-SDK rules worked for NSC. Nobody has examined whether Play/App Store requirements could force PQ-capable stacks.
3. **Notification for "readiness" issues** (not exploitable today) and in countries with weak or no CERT coverage. H03 found 8–19% of vulnerable hosts in countries without a CERT, and its experiments are all US-led and about vulnerabilities.
4. **Partial-deployment economics.** E01 states it outright: "an adversary can discard quantum-resistant sessions and concentrate harvesting on the shrinking classical remainder". The *defensive* reading is that the classical remainder (which apps and endpoints still negotiate classical) is what needs measuring and fixing.
5. **Agility of app-bundled vs platform-provided stacks.** H02 validates agility only for OpenSSL, NGINX and GitLab. E08's rotation-time metric has never been applied to mobile apps.
6. **End-to-end "toy" models joining measurement and cryptanalysis.** T5 costs attacks on primitives; T3 benchmarks defences; nobody builds a small, fully worked hybrid handshake showing Shor on the classical half and the ML-KEM half surviving (M3).

### (d) Methodological gaps

- **Interception-based capture distorts key-exchange measurement.** It terminates TLS at the proxy (B09) and suppresses QUIC. Studies that need the server-negotiated group must capture without interception and then attribute flows to apps. No paper makes this distinction explicit.
- **Non-PQ clients produce false "classical" results** (A08). Any reuse of older scanners (e.g., stock OpenSSL 3.0) is invalid for PQ measurement.
- **Statistics are often missing.** A02, A08 and A09 report no confidence intervals. A03 is the model to follow (Wilson CIs, McNemar, logistic regression with grouped CV, HHI).
- **Naive Grover labels.** A02, A05 and A09 label AES-128 as "64-bit". MAXDEPTH costing (G02/G05) should replace this.
- **Pre-registered hypotheses are rare.** H03 (a randomised design) and A03 (stated RQs with tests) are the exceptions.

---

## 3.2 Unanswered questions and explicit future work stated by the authors

| ID | What the authors say should come next (stated) |
|---|---|
| A01 | Guidance and tooling for owner-managed systems; engaging providers; continuous measurement. Stated limitations: public Top-1M only; HTTPS only; cloud VPs "may not fully capture… residential networks… constrained network conditions… device heterogeneity". |
| A02 | PQC certificates; fully PQ handshakes; performance and interoperability of PQ authentication; deployment strategies. |
| A03 | Longitudinal study; combine protocol measurement with provider attribution "to separate provider-driven from organisation-driven migration"; opt-out page for scans. |
| A04 | (Survey) QUIC: PQ interaction with congestion control, connection migration and **0-RTT resumption "not yet well understood"**. |
| A05 | More technologies (HAProxy, Envoy, IIS, Tomcat, cloud TLS); longitudinal GitHub tracking; ML-DSA certificates. |
| A06 | How key size vs speed affects clients; how OSes, architectures and **network connectivity** respond; which networks host problematic middleboxes; long-tail performance per AS/device. |
| A07 | (Implied) more passive vantage points; new-extension checks; Android TLS 1.3 support awaited from the OS. |
| A08 | Internet-scale measurement with **OQS-capable clients**; QUIC; continuous monitoring; symbolic verification links. |
| A09 | Benchmark vs commercial tools; internal systems; **QUIC** (with AI). |
| B01 | Attribute connections to **ad/analytics/logging libraries**; large-scale real-user telemetry for mobile. Recommends HTTP/3 + resumption defaults in Android's HTTPS library; KEMTLS(-PDK). |
| B02 | Developer survey on why pinning differs across platforms; automated exploration **including sign-up/login**; better unpinning. |
| B03 | (Poster) extend analysis; improve LLM-assisted migration. |
| B04 | **Active server-side measurements of mobile app servers vs web servers**; attack resilience; separate the TLS library from the OS (later realised as Conscrypt/Mainline). |
| B05 | Integrate CryptoGuard/LibScout into Play review; better Android Studio NSC support. |
| B06 | OS-level enforcement of sane TLS configurations; better regulatory guidance. |
| B07 | Proofs of concept for the potential vulnerabilities; obfuscation/XAPK analysis; open-source scanner. |
| B08 | Better GUI coverage; native-code TLS; app stores need reliable contact channels. |
| B09 | More apps and categories; impact of the capture environment on traffic patterns. |
| C01 | More algorithms and levels; multi-path emulation; certificate chain sizes; server throughput; SSH/IPsec/WireGuard. |
| C02 | PQ auth in VPN, QUIC, DTLS; combined PQ KEM + signatures; **lossy networks**; SCT/OCSP; hybrid certificates. |
| C03 | **Real networks with commercial load balancers and MitM inspection devices**; >100 TPS; PQ signatures; native OpenSSL 3.5. |
| C04 | (Implied) PQ certificate handling within anti-amplification limits; larger MTUs. |
| C05 | Hardware acceleration; broader devices; **over-the-air effects**; dynamic network conditions; external power analysers. |
| C06 | Fragmentation and loss; real CDN experiments. |
| D01 | Fully quantum (QqQ) AKE. |
| D02 | (Implied) aligning HPKE and TLS hybrid constructions. |
| D03 | KEMTLS-PDK (pre-distributed keys); more primitives and levels. |
| D04 | (Standard) combiner guidance via SP 800-227. |
| D05 | Measured board implementation; QROM proof; DoS (forced aborts). |
| E01 | E = 1 problem in TLS/QUIC (fresh-DH rekeying); **real-network validation**; **"economics of partial PQC deployment"**; interception cost. |
| E02 | Better communication of FS caveats to operators; standards attention (TLS 1.3 PSK lifetimes). |
| E03 | White-box analysis of more (closed-source) implementations; libraries should self-audit STEKs. |
| E04 | Better 1024-bit estimates; standardised verifiable group generation. |
| E05 | Defence in depth; fewer supported curves. |
| E06 | Monitor QEC milestones (logical processors with non-Clifford gates; horizontal scale). |
| E07 | Annual recalibration with tracking indicators; falsification conditions; **negotiation and interoperability layer (out of scope)**; trust anchors; entropy. |
| E08 | Weight by exploit likelihood (EPSS); three or more controls. |
| F01 | Register sharing; lower-qubit reversible inversion; other curve models. |
| F02 | Recursive GCD; projective/Edwards coordinates; physical layer. |
| F03 | Low-footprint regime; depth optimisation for reaction limits; 2D-local special-purpose architectures. |
| F04 | (Implied) low end of qubit estimates depends on QEC advances. |
| F05 | Extension to other cryptographic cases (ECC; done later in F06). |
| F06 | (Policy) digital salvage frameworks; immediate PQC migration; better ECC estimates on other curves. |
| F07 | Higher-rate codes; parallel surgery; faster hardware (µs readout, constant-velocity transport). |
| F08 | Better loss models; runtime and footprint co-optimisation. |
| F09 | (Implied) physical estimates; other curve models. |
| F10 | (Implied) practical multi-controlled gate decomposition at scale. |
| F11 | Full depth optimisation (parallel analysis); better qubit clearing. |
| F12 | (Claims scaling; no credible future-work programme.) |
| F13 | Public reporting of ladder rungs with logical/physical metrics. |
| G01 | Fixed-point Grover; quantum linear/differential cryptanalysis costs. |
| G02 | Other cost metrics; **multi-target Grover under MAXDEPTH**; compiler improvements. |
| G03 | (Implied) full Grover integration. |
| G04 | Structure-aware ansatz design for variational attacks. |
| G05 | (Implied) other AEADs. |
| G06 | 192/256-bit key variants; better adders. |
| G07 | (Implied) price-performance analysis of other quantum attacks. |
| H01 | Validate the migration framework on real migrations; define the cryptographic inventory (CBOM); mature implementations. |
| H02 | Empirical validation of agility beyond software (hardware, organisational); context-specific assessment approaches. |
| H03 | Why operators don't remediate; standard security point of contact; better centralised mechanisms; usable remediation tools. |

### Unanswered questions that emerge from the whole corpus

1. **Do mobile apps lag servers and browsers in PQ key exchange, as they did for TLS 1.3?** (A07 precedent + B04 mechanism; not tested.)
2. **Which layer decides an app connection's PQ status:** platform, framework, SDK, app code, or server? (A08 joint property; B04 defaults.)
3. **Are app API hosts less PQ-ready than the same organisation's websites?** (B04's future work; A01/A03 web-only.)
4. **For the same app, does PQ status differ between iOS and Android?** (B02 cross-platform inconsistency; iOS 26 system-wide hybrid.)
5. **How many recorded app sessions does one compromised key expose in practice** (key reuse, psk_ke, 0-RTT, RSA transport), and how much does hybrid deployment neutralise it? (E01 open problem; E02/E05 pre-1.3; D01/D02 theory.)
6. **What is the quantum price tag of a measured app connection or app**, given F06/F08 costs and the exposure multipliers? (E01 lab-only.)
7. **How often do PQ-capable clients fall back to classical in the field** (HRR, middleboxes, library gaps)? (D05, E07 §6.5.)
8. **Would PQ or Merkle Tree certificates break pinned finance apps?** (B02/B05 pinning; C06 sizes; no joint study.)
9. **What do PQ handshakes cost on low-end phones over South Asian cellular networks?** (A06, C01, C03, C05 gaps.)
10. **Does a notification plus fix guide move Bangladeshi operators, compared with H03's +11% in the US/EU?** (H03, B08.)
11. **What do Bangladeshi developers and bank teams know about PQ, and what blocks them?** (H01 challenges; B03 LLM failure.)

---

## 3.3 How N1 can build on the missing elements

### (a) Gap → contribution map

| Gap (from 3.1–3.2) | Literature anchor | N1 item | What N1 adds |
|---|---|---|---|
| No PQ measurement of app traffic | B01, A07, A01 (web only) | **G4** (core) | First PQ key-exchange census of a country's finance apps, with first-party vs third-party and web vs app split |
| Which stack decides | B04, A07, A08, B05 | **G1**, **G4** layer attribution | Framework default matrix (OkHttp/Cronet/WebView/Flutter × Android versions); ClientHello fingerprints to attribute each connection |
| iOS vs Android | B02, A02's software list | **G3** | Same-app platform divide for PQ |
| Device update lag | B04 (61.7% ≤ Android 5 in 2017), A07 | **G2** | Share of Bangladeshi devices with PQ-capable WebView/Chrome/Play services |
| SDK layer | B04, B08, B01 future work | **G5** | SDK vs first-party PQ status |
| App-layer crypto | B03, B06, B07, A04 (OIDC) | **G6**, **M6** | Quantum exposure of RSA/ECC inside apps; cost of any uncosted cipher found (G05/G06-style) |
| Data lifetime weighting | E06, E07 (sector X), B08 (flow function) | **G7** | Exposure weighted by flow type (e-KYC, statements vs telemetry) |
| API hosts vs websites; hosting | B04 future work, A01/A03 attribution | **G8** | Same-organisation web vs API comparison with provider attribution |
| Pinning × PQ certificates | B02, B05, C06, D03 | **G9** | Hazard list: leaf/SPKI pins that would block PQ/MTC certificate migration; KEMTLS-PDK recommendation |
| Network path and middleboxes | A06, C01, A01 (cloud only) | **G10** | Capture across Bangladeshi operators; failure/HRR/fallback logging |
| Cost on local networks and phones | C01, C03, C05, A06 | **G11** | Latency/data/battery tails on low-end phones over real operators |
| Static → dynamic prediction | B05, B03, B07 (static), B08 (dynamic) | **G12** | Classifier from APK features to measured behaviour; scale via AndroZoo |
| Notification efficacy | H03, B08 | **G13** | Randomised notification + fix guide, re-measure after 3–6 months |
| Human layer | H01, B03 | **G14** | Survey/interviews of Bangladeshi fintech developers and bank teams |
| Cipher and resumption mode | A07, C06, E03, G02 | **G15**, **M4** | AES-128/256 share with MAXDEPTH-aware cost; psk_ke vs psk_dhe_ke split |
| Sessions exposed per key in the wild | E01 (open problem), E02, E03, E05 | **M1** (lead) | Measured "amortisation factor" for Bangladeshi finance/API hosts vs global CDNs, split by hybrid vs classical-fallback connections |
| Quantum price per measured connection | E01, F01–F09, F05, G02 | **M2** | Price tag per connection and per app (Shor for classical ECDH/RSA; MAXDEPTH Grover for symmetric) |
| No end-to-end toy model | D04, D01/D05, G04, F13 | **M3** | Toy-TLS: toy ECC + S-AES + baby ML-KEM with simulated Shor/Grover, showing why hybrid survives |
| Legacy curves | E05, F10, F11 | **M5** | Residual binary/small-curve support on Bangladeshi servers (expected ≈0) |

### (b) Design rules the corpus itself justifies

1. **Measure with a PQ-capable client and log both sides of the handshake** (A08). Store the ClientHello groups and key_shares, the ServerHello group, HRR, and the PSK mode.
2. **Do not intercept when measuring key exchange** (B09). Use hotspot or per-app VPN capture (B01, B08), attribute flows by SNI/IP and ClientHello fingerprints (B04), and use interception only in a separate pass for pinning tests (B02).
3. **Capture QUIC and IPv6** (A09's blind spot; B09 QUIC share) and parse QUIC Initial packets for key_share.
4. **Stratify by hosting and by layer** (A01, A03): CDN vs owner-managed; website vs API; first-party vs SDK.
5. **Use A03-style statistics:** Wilson CIs, paired tests (McNemar) for web vs API, logistic regression with provider and sector predictors, HHI for concentration.
6. **Report tails and failures, not just medians**, for cost (A06, C01, A01 failure taxonomy).
7. **Use real accounts for finance flows** (B01/B02 limitations), with ethics approval and without touching other users' data.
8. **Price with published estimates and state their assumptions.** Use F06/F08 for 256-bit ECC, F05 for RSA-2048, G02/G05 for Grover. Give ranges (fast vs slow clock), never a single date (Debate 8).
9. **Separate classical and hybrid connections in every exposure metric.** D01/D02 imply that reuse of the classical half is harmless for hybrid sessions and harmful for classical ones.
10. **Disclose responsibly and privately first** (E02, E03, H03), especially for live findings about named institutions. This includes N1's own pilot data (§0.4 note).

### (c) Testable hypotheses (write them down before collecting data)

- **H1 (layer):** For the same Bangladeshi finance app, the share of connections negotiating X25519MLKEM768 is explained more by the client stack (platform version, framework) than by the server's support. Prediction from B04, A07, A08.
- **H2 (platform divide):** iOS builds of the same apps negotiate hybrid more often than Android builds, because iOS 26 enables it system-wide (A02's list) while Android's platform API does not expose groups (B04 analogue).
- **H3 (API gap):** App API hosts negotiate hybrid less often than the same organisation's website, and the gap shrinks when both sit on the same CDN (A01, A03 provider effect).
- **H4 (SDK):** SDK connections (analytics, ads) negotiate hybrid more often than first-party API connections, because SDK back ends sit on global CDNs (B04/B08: SDKs on big infrastructure).
- **H5 (shortcuts):** Key-share reuse, RSA key-transport acceptance, psk_ke resumption and long ticket lifetimes are more frequent on owner-managed Bangladeshi finance/API hosts than on global CDNs (E02, E05; A01 owner-managed lag).
- **H6 (hybrid neutralises reuse):** Where the hybrid is negotiated, measured classical-share reuse does not raise the exposure metric; it does for classical-fallback connections (D01, D02).
- **H7 (cost):** Median PQ handshake overhead on Bangladeshi operators is small (≤15 ms), but the p95 tail and failure rate are higher on lossy or low-end conditions (A06, C01, C03).
- **H8 (pinning hazard):** Most finance-app pins are CA-level, but a non-trivial minority are leaf/SPKI pins that would require app updates under PQ/MTC certificates (B02, B05).
- **H9 (notification):** Direct, detailed notifications increase remediation modestly (≈10 percentage points) relative to controls within 3–6 months (H03).

*Two-sided framing:* each hypothesis yields a publishable result either way, in line with N1's "every outcome is a result" plan.

### (d) What *not* to spend time on (already occupied or low-value according to the corpus)

- **Another web-only Top-1M PQ census** (A01, A02, A03 already cover this). Use them as baselines.
- **Lab latency benchmarks of KEMs on servers** (C01, C03, C04, C05 are thorough). Spend the effort on phones and real operators instead.
- **Grover on AES-128 as a "threat"** (G01–G07): settled as infeasible under MAXDEPTH. Report it only as a policy-alignment metric.
- **New ECC resource estimates.** F06–F09 are state of the art; N1 should cite them, not compete.
- **Small-scale hardware "demonstrations"** (F12 genre). F06 explains why they are poor indicators.
- **Lattice break scenarios** (E07's contingency tier) beyond one sentence of context.

### (e) Threats to validity the literature warns about

| Threat | Source | Mitigation for N1 |
|---|---|---|
| Client artefacts (non-PQ client sees no PQ) | A08 | Use PQ-capable tooling; validate against cloudflare.com/cdn-cgi/trace (`kex=`) |
| Interception distortion | B09, B08 | Capture without interception for key exchange |
| Background OS traffic mixed into app captures | B01 (calibration), B09 | Calibrate with an idle device; attribute by SNI/fingerprint |
| Login-gated flows missed | B01, B02, B09 | Real test accounts; scripted flows; LLM GUI agents (B08) as an option |
| Single device / single network | B01, A01 | Multiple devices and operators (G10, G11) |
| Stale or vendor-biased cost figures | E07, F06–F08 | Give ranges, state assumptions and conflicts of interest |
| Over-reading small samples | A09, A02 | Report CIs; avoid sector claims below ~50 per cell (A03 rule) |
| Ethics of naming institutions | B07, E02, H03 | Private disclosure first; aggregate reporting |

---

# Appendix A: Paper key (60 papers)

| ID | Year | Authors | Title | Venue | File in `papers/` |
|---|---|---|---|---|---|
| A01 | 2026 | Wickramasinghe, Li, Jha, Shaghaghi | Mind the Gap: Policy vs Reality in Post-Quantum TLS Deployment | ACM IMC 2026 (arXiv:2607.29005) | `A01_Wickramasinghe2026_Mind_the_Gap_Policy_vs_Reality.pdf` |
| A02 | 2026 | Dubey, Varshney | Measurement Study of Post-Quantum Readiness of Internet: 2026 | arXiv:2606.16473 | `A02_Dubey2026_Measurement_Study_of_PostQuantum_Readiness_of.pdf` |
| A03 | 2026 | Loizou, Ghadafi | Measuring Post-Quantum TLS Deployment Across UK Internet Sectors | arXiv:2608.02147 | `A03_Loizou2026_Measuring_PostQuantum_TLS_Deployment_Across_UK.pdf` |
| A04 | 2026 | Mallick, Kundu, Kompella | Study of Post Quantum status of Widely Used Protocols | arXiv:2603.28728 | `A04_Mallick2026_Study_of_Post_Quantum_status_of.pdf` |
| A05 | 2026 | Balaji, Varshney, Ravi, Jain, Foe, Seet et al. | Operationalising Post Quantum TLS: Automated Configuration Profiling and Hybrid PQC Deployment in Financial Infrastructure | arXiv:2605.17955 (ePrint 2026/959) | `A05_Balaji2026_Operationalising_Post_Quantum_TLS_Automated_Configuration.pdf` |
| A06 | 2019 | Kwiatkowski, Sullivan, Langley, Levin, Mislove | Measuring TLS key exchange with post-quantum KEM | 2nd NIST PQC Standardization Conference 2019 | `A06_Kwiatkowski2019_Measuring_TLS_key_exchange_with_postquantum.pdf` |
| A07 | 2019 | Holz, Amann, Razaghpanah, Vallina-Rodriguez | The Era of TLS 1.3: Measuring Deployment and Use with Active and Passive Methods | arXiv:1907.12762 | `A07_Holz2019_The_Era_of_TLS_13_Measuring.pdf` |
| A08 | 2026 | Ibrahim, Ajith, Haroon | Detecting Post-Quantum and Hybrid TLS Deployments via Raw TLS Record Inspection | IACR ePrint 2026/834 | `A08_Ibrahim2026_Detecting_PostQuantum_and_Hybrid_TLS_Deployments.pdf` |
| A09 | 2025 | Cho, Hyoung, Kim, Sim, Chattopadhyay, Seo, Kim | Toward Crypto Agility: Automated Analysis of Quantum-Vulnerable TLS via Packet Inspection | IACR ePrint 2025/1549 | `A09_Cho2025_Toward_Crypto_Agility_Automated_Analysis_of.pdf` |
| B01 | 2023 | Mankowski, Wiggers, Moonsamy | TLS → Post-Quantum TLS: Inspecting the TLS landscape for PQC adoption on Android | EuroS&P Workshops 2023 | `B01_Mankowski2023_TLS_PostQuantum_TLS_Inspecting_the_TLS.pdf` |
| B02 | 2022 | Pradeep, Paracha, Bhowmick, Davanian, Razaghpanah, Chung et al. | A Comparative Analysis of Certificate Pinning in Android & iOS | ACM IMC 2022 | `B02_Pradeep2022_A_Comparative_Analysis_of_Certificate_Pinning.pdf` |
| B03 | 2025 | Strauss, Upadhyay, Siddique, Baggili, Farooq | Assessing and Enhancing Quantum Readiness in Mobile Apps | IEEE S&P 2025 Poster (arXiv:2506.00790) | `B03_Strauss2025_Assessing_and_Enhancing_Quantum_Readiness_in.pdf` |
| B04 | 2017 | Razaghpanah, Niaki, Vallina-Rodriguez, Sundaresan, Amann, Gill | Studying TLS Usage in Android Apps | ACM CoNEXT 2017 | `B04_Razaghpanah2017_Studying_TLS_Usage_in_Android_Apps.pdf` |
| B05 | 2021 | Oltrogge, Huaman, Amft, Acar, Backes, Fahl | Why Eve and Mallory Still Love Android: Revisiting TLS (In)Security in Android Applications | USENIX Security 2021 | `B05_Oltrogge2021_Why_Eve_and_Mallory_Still_Love.pdf` |
| B06 | 2015 | Reaves, Scaife, Bates, Traynor, Butler | Mo(bile) Money, Mo(bile) Problems: Analysis of Branchless Banking Applications in the Developing World | USENIX Security 2015 | `B06_Reaves2015_Mobile_Money_Mobile_Problems_Analysis_of.pdf` |
| B07 | 2024 | Mickey, Yanhaona | An investigation of the Online Payment and Banking System Apps in Bangladesh | arXiv:2407.07766 | `B07_Mickey2024_An_investigation_of_the_Online_Payment.pdf` |
| B08 | 2026 | Yang, Huang, Fang, Zhang, Guo, Wu et al. | Okara: Detection and Attribution of TLS Man-in-the-Middle Vulnerabilities in Android Apps with Foundation Models | ACISP 2026 (arXiv:2601.22770) | `B08_Yang2026_Okara_Detection_and_Attribution_of_TLS.pdf` |
| B09 | 2025 | Jimenez-Berenguel, Campo, Moure-Garrido, Garcia-Rubio, Diaz-Sanchez, Almenares | PARROT: Portable Android Reproducible traffic Observation Tool | arXiv:2509.09537 | `B09_JimenezBerenguel2025_PARROT_Portable_Android_Reproducible_traffic_Observation.pdf` |
| C01 | 2020 | Paquin, Stebila, Tamvada | Benchmarking Post-Quantum Cryptography in TLS | PQCrypto 2020 | `C01_Paquin2020_Benchmarking_PostQuantum_Cryptography_in_TLS.pdf` |
| C02 | 2020 | Sikeridis, Kampanakis, Devetsikiotis | Post-Quantum Authentication in TLS 1.3: A Performance Study | NDSS 2020 | `C02_Sikeridis2020_PostQuantum_Authentication_in_TLS_13_A.pdf` |
| C03 | 2026 | Gomez-Cambronero, Munteanu, Gonzalez-Tablas | Layered Performance Analysis of TLS 1.3 Handshakes: Classical, Hybrid, and Pure Post-Quantum Key Exchange | SPIQE @ EuroS&P 2026 (arXiv:2603.11006) | `C03_GomezCambronero2026_Layered_Performance_Analysis_of_TLS_13.pdf` |
| C04 | 2024 | Kempf, Gauder, Jaeger, Zirngibl, Carle | A Quantum of QUIC: Dissecting Cryptography with Post-Quantum Insights | IFIP Networking 2024 (arXiv:2405.09264) | `C04_Kempf2024_A_Quantum_of_QUIC_Dissecting_Cryptography.pdf` |
| C05 | 2026 | Hoque, Aydeger | Energy-Aware System-Level Evaluation of Post-Quantum TLS on Embedded User Equipment over a Disaggregated 5G Network | arXiv:2607.03988 | `C05_Hoque2026_EnergyAware_SystemLevel_Evaluation_of_PostQuantum_TLS.pdf` |
| C06 | 2026 | Chou, Cao | Network Impact of Post-Quantum Certificate Chain sizes on Time to First Byte in TLS Deployments | arXiv:2604.24869 | `C06_Chou2026_Network_Impact_of_PostQuantum_Certificate_Chain.pdf` |
| D01 | 2019 | Bindel, Brendel, Fischlin, Goncalves, Stebila | Hybrid Key Encapsulation Mechanisms and Authenticated Key Exchange | PQCrypto 2019 | `D01_Bindel2019_Hybrid_Key_Encapsulation_Mechanisms_and_Authenticated.pdf` |
| D02 | 2024 | Barbosa, Connolly, Duarte, Kaiser, Schwabe, Varner, Westerbaan | X-Wing: The Hybrid KEM You've Been Looking For | IACR Communications in Cryptology 1(1) 2024 | `D02_Barbosa2024_XWing_The_Hybrid_KEM_Youve_Been.pdf` |
| D03 | 2020 | Schwabe, Stebila, Wiggers | Post-Quantum TLS Without Handshake Signatures (KEMTLS) | ACM CCS 2020 | `D03_Schwabe2020_PostQuantum_TLS_Without_Handshake_Signatures_KEMTLS.pdf` |
| D04 | 2024 | NIST | FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) | NIST FIPS 203 (Aug 2024) | `D04_NIST2024_FIPS_203_ModuleLatticeBased_KeyEncapsulation_Mechanism_Standard.pdf` |
| D05 | 2026 | Gupta, Rana | Transcript-Bound Combiners for Downgrade-Resilient Hybrid Post-Quantum Key Establishment: Definition, Proof, and Embedded-Device Cost | arXiv:2609.21273 | `D05_Gupta2026_TranscriptBound_Combiners_for_DowngradeResilient_Hybrid_PostQuantum.pdf` |
| E01 | 2026 | Blanco-Romero, Almenares Mendoza, Garcia Rubio, Campo, Diaz Sanchez | On the Practical Feasibility of Harvest-Now, Decrypt-Later Attacks | arXiv:2603.01091 | `E01_BlancoRomero2026_On_the_Practical_Feasibility_of_HarvestNow.pdf` |
| E02 | 2016 | Springall, Durumeric, Halderman | Measuring the Security Harm of TLS Crypto Shortcuts | ACM IMC 2016 | `E02_Springall2016_Measuring_the_Security_Harm_of_TLS.pdf` |
| E03 | 2023 | Hebrok, Nachtigall, Maehren, Erinola, Merget, Somorovsky, Schwenk | We Really Need to Talk About Session Tickets: A Large-Scale Analysis of Cryptographic Dangers with TLS Session Tickets | USENIX Security 2023 | `E03_Hebrok2023_We_Really_Need_to_Talk_About.pdf` |
| E04 | 2015 | Adrian, Bhargavan, Durumeric, Gaudry, Green, Halderman et al. | Imperfect Forward Secrecy: How Diffie-Hellman Fails in Practice | ACM CCS 2015 | `E04_Adrian2015_Imperfect_Forward_Secrecy_How_DiffieHellman_Fails.pdf` |
| E05 | 2018 | Valenta, Sullivan, Sanso, Heninger | In search of CurveSwap: Measuring elliptic curve implementations in the wild | IEEE EuroS&P 2018 | `E05_Valenta2018_In_search_of_CurveSwap_Measuring_elliptic.pdf` |
| E06 | 2026 | Mosca, Piani | Quantum Threat Timeline Report 2025 | Global Risk Institute (Mar 2026) | `E06_Mosca2026_Quantum_Threat_Timeline_Report_2025.pdf` |
| E07 | 2026 | Grover, Haile, Pedersen, Uner, Erickson | A Scenario-Based Evaluation of CRQC+AI Vulnerability Spectrum for TLS 1.3 Cryptographic Dependencies | arXiv:2608.23785 | `E07_Grover2026_A_ScenarioBased_Evaluation_of_CRQCAI_Vulnerability.pdf` |
| E08 | 2026 | Wilson-Shah | Quantifying quantum risk: a measure of crypto agility | arXiv:2606.17116 | `E08_WilsonShah2026_Quantifying_quantum_risk_a_measure_of.pdf` |
| F01 | 2017 | Roetteler, Naehrig, Svore, Lauter | Quantum resource estimates for computing elliptic curve discrete logarithms | ASIACRYPT 2017 (arXiv:1706.06752) | `F01_Roetteler2017_Quantum_resource_estimates_for_computing_elliptic.pdf` |
| F02 | 2020 | Haner, Jaques, Naehrig, Roetteler, Soeken | Improved quantum circuits for elliptic curve discrete logarithms | PQCrypto 2020 (arXiv:2001.09580) | `F02_Haner2020_Improved_quantum_circuits_for_elliptic_curve.pdf` |
| F03 | 2023 | Litinski | How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates | arXiv:2306.08585 | `F03_Litinski2023_How_to_compute_a_256bit_elliptic.pdf` |
| F04 | 2021 | Gidney, Ekera | How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits | Quantum 5:433 (2021) | `F04_Gidney2021_How_to_factor_2048_bit_RSA.pdf` |
| F05 | 2025 | Gidney | How to factor 2048 bit RSA integers with less than a million noisy qubits | arXiv:2505.15917 | `F05_Gidney2025_How_to_factor_2048_bit_RSA.pdf` |
| F06 | 2026 | Babbush, Zalcman, Gidney, Broughton, Khattar, Neven et al. | Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations | arXiv:2603.28846 | `F06_Babbush2026_Securing_Elliptic_Curve_Cryptocurrencies_against_Quantum.pdf` |
| F07 | 2026 | Cain, Xu, King, Picard, Levine, Endres et al. | Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits | arXiv:2603.28627 | `F07_Cain2026_Shors_algorithm_is_possible_with_as.pdf` |
| F08 | 2026 | Haner, Tripier, Young, Naehrig, Maksymov, Alam et al. | Computing 256-bit elliptic curve discrete logarithms in 26 days on a fault-tolerant trapped-ion quantum computer with 20,000 qubits | arXiv:2609.05625 | `F08_Haner2026_Computing_256bit_elliptic_curve_discrete_logarithms.pdf` |
| F09 | 2026 | Luo, Yang, Luo, Wang, Su, Sun et al. | Quantum Algorithm for Elliptic Curve Discrete Logarithms with Space-Efficient Point Addition | arXiv:2607.13816 | `F09_Luo2026_Quantum_Algorithm_for_Elliptic_Curve_Discrete.pdf` |
| F10 | 2025 | Putranto, Wardhani, Kim et al. | Enhancing Quantum Cryptanalysis of Binary Elliptic Curves Through Optimized Out-of-Place Point Addition and ECPM Integration | IEEE Access 2025 (faculty paper) | `F10_Putranto2025_Enhancing_Quantum_Cryptanalysis_of_Binary_Elliptic.pdf` |
| F11 | 2023 | Taguchi, Takayasu | Concrete Quantum Cryptanalysis of Binary Elliptic Curves via Addition Chain | CT-RSA 2023 (faculty paper) | `F11_Taguchi2023_Concrete_Quantum_Cryptanalysis_of_Binary_Elliptic.pdf` |
| F12 | 2025 | Tippeconnic | Breaking a 5-Bit Elliptic Curve Key using a 133-Qubit Quantum Computer | arXiv:2507.10592 | `F12_Tippeconnic2025_Breaking_a_5Bit_Elliptic_Curve_Key.pdf` |
| F13 | 2025 | Dallaire-Demers, Doyle, Foo | Brace for impact: ECDLP challenges for quantum cryptanalysis | arXiv:2508.14011 | `F13_DallaireDemers2025_Brace_for_impact_ECDLP_challenges_for.pdf` |
| G01 | 2016 | Grassl, Langenberg, Roetteler, Steinwandt | Applying Grover's algorithm to AES: quantum resource estimates | PQCrypto 2016 (arXiv:1512.04965) | `G01_Grassl2016_Applying_Grovers_algorithm_to_AES_quantum.pdf` |
| G02 | 2020 | Jaques, Naehrig, Roetteler, Virdia | Implementing Grover oracles for quantum key search on AES and LowMC | EUROCRYPT 2020 (arXiv:1910.01700) | `G02_Jaques2020_Implementing_Grover_oracles_for_quantum_key.pdf` |
| G03 | 2025 | Chen, Cai, Gao, Lin | Quantum circuit for implementing AES S-box with low costs | arXiv:2503.06097 (faculty paper) | `G03_Chen2025_Quantum_circuit_for_implementing_AES_Sbox.pdf` |
| G04 | 2025 | Wang, Zheng, Wu, Wen, Wei, Long | Reducing quantum resources for attacking S-AES on quantum devices | npj Quantum Information 2025 (faculty paper) | `G04_Wang2025_Reducing_quantum_resources_for_attacking_SAES.pdf` |
| G05 | 2024 | Mandal, Anand, Rahman, Sarkar, Isobe | Implementing Grover's on AES-based AEAD schemes | Scientific Reports 2024 (faculty paper) | `G05_Mandal2024_Implementing_Grovers_on_AESbased_AEAD_schemes.pdf` |
| G06 | 2026 | Ulgen, Cildiroglu, Yayla | Quantum circuit realization and Grover cryptanalysis of the hybrid ARX-SPN cipher GFSPX | Physica Scripta 101 (2026) (faculty paper) | `G06_Ulgen2026_Quantum_circuit_realization_and_Grover_cryptanalysis.pdf` |
| G07 | 2009 | Bernstein | Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? | SHARCS 2009 (faculty paper) | `G07_Bernstein2009_Cost_analysis_of_hash_collisions_Will.pdf` |
| H01 | 2024 | Nather, Herzinger, Gazdag, Steghofer, Daum, Loebenberger | Migrating Software Systems towards Post-Quantum-Cryptography: A Systematic Literature Review | arXiv:2404.12854 | `H01_Nather2024_Migrating_Software_Systems_towards_PostQuantumCryptography_A.pdf` |
| H02 | 2024 | Nather, Herzinger, Steghofer, Gazdag, Hirsch, Loebenberger | Toward a Common Understanding of Cryptographic Agility: A Systematic Review | arXiv:2411.08781 | `H02_Nather2024_Toward_a_Common_Understanding_of_Cryptographic.pdf` |
| H03 | 2016 | Li, Durumeric, Czyz, Karami, Bailey, McCoy, Savage, Paxson | You've Got Vulnerability: Exploring Effective Vulnerability Notifications | USENIX Security 2016 | `H03_Li2016_Youve_Got_Vulnerability_Exploring_Effective_Vulnerability.pdf` |

---

# Appendix B: Paper-wise detailed notes

These notes were written paper by paper while reading the full texts. Each one records: the question; method and data; every key number; stated limitations; stated future work; quality flags (marked *mine* where they are my assessment rather than the authors'); and relevance to N1 (G1–G15, M1–M6).
Notes are grouped A→H in the order of the paper key.
### A01 Wickramasinghe, Li, Jha, Shaghaghi 2026, Mind the Gap (IMC 2026, arXiv 2607.29005v1)
- **Q:** How does PQ-TLS deployment compare to national PQC policies? RQ1 configuration landscape; RQ2 deployment agency (infra-provider vs owner); RQ3 policy alignment (sector, country); RQ4 operational viability (latency, failures, geography); RQ5 security co-evolution.
- **Policy survey (Table 1), 8 jurisdictions:** Australia (ML-KEM-768/1024 prefer 1024; hybrid allowed, not recommended; complete 2030), Canada (ML-KEM 512/768/1024; 2031/2035), EU (2030/2035; advisory), France (Kyber + FrodoKEM; hybrid recommended; 2030), Germany (ML-KEM, FrodoKEM, Classic McEliece; hybrid recommended; 2030), India (ML-KEM-768/1024 prefer 1024; hybrid recommended; 2035), UK (ML-KEM-768; hybrid transitional; 2035), USA (ML-KEM-1024/ML-DSA-87 CNSA 2.0; hybrid allowed not recommended; classical deprecated 2030, disallowed 2035). Convergence on ML-KEM but divergence on parameters, hybrid stance, timelines. **Bangladesh not in the survey; no South Asian policy except India.**
- **Method:** custom TLS 1.3-only client with NIST PQC; DomCop Top-10M list (Top-1M for main analysis; per-country Top-10K ccTLD + Top-1K gov domains); 11 cloud vantage points (incl. Mumbai, no Bangladesh); 3 rounds Jul 2025, Nov 2025, Mar 2026; >2 billion handshakes; local DNS resolution per vantage point, lowest-RTT IP. Two baseline handshakes per domain (unconstrained → default_KE/SA; classical-only → default classical KE/SA); then iterate supported groups/signatures. Differential latency: hybrid vs its own classical half (X25519MLKEM768 vs X25519), 5 matched pairs per config spaced 4 h. Attribution of who manages TLS: IP ranges of CDNs, CNAME, PTR, HTTP metadata, WHOIS, AS fallback; "potentially infra-managed" vs "potentially owner-managed" vs unknown (probabilistic). Robustness replicated with Tranco and CrUX (49.74/51.55/52.75% default PQ).
- **Stable panel:** 684,494 domains (68.44%) completed TLS 1.3 from every VP in all rounds; 315,506 (31.55%) failed at least once.
- **Findings RQ1:** 0 PQ signatures anywhere. Default hybrid PQ: 31.26% (Jul 2025) → 47.37% (Nov 2025) → 49.22% (Mar 2026). **Every PQ default is X25519MLKEM768.** SecP256r1MLKEM768 supported by 5.53%, SecP384r1MLKEM1024 1.95%, never default. Pure ML-KEM essentially absent (ML-KEM-1024 0.66% support). 88.76% of PQ domains support exactly one PQ group. Monotonic: no domain reverted to classical; "support but not default" gap 73 domains → 2.
- **RQ2:** 60.87% of panel infra-managed, 30.09% owner-managed, 9.04% unknown. 93.92% of PQ deployments are infra-managed; only 4.58% owner-managed. >75% of infra-managed domains are PQ vs <10% of owner-managed. Cloudflare 57.34% of PQ-default domains, Amazon 14.01%, Fastly 13.14%, Squarespace 3.52%, Automattic 2.37%, Google 1.67%. Cloudflare + Fastly ≈70%.
- **RQ3 sectors (Mar 2026):** e-commerce ~68%, social networks ~62%, **finance 59% (n=24,563)**, health 51%, file storage 46%, webmail 41%, **government 38% (n=18,178)**, chats & messengers 27%. Countries (top-10K ccTLD): USA 57%, Australia 53%, UK 45%, India 40%, France 27%, Germany 16%. Gov domains: Australia 57%, UK 47%, Canada/Germany/India <7%. Earlier-deadline jurisdictions have *lower* mean adoption (32.4% vs 45.7%), but restricted to owner-managed domains adoption is ~equal (9.6% vs 8.4%) and within Cloudflare equal (93.5% vs 94.1%): **composition of hosting explains the differences, not policy**.
- **RQ4:** 328,290 domains: median ΔT = 0 ms, IQR [−5, +5] ms, p90 = 14 ms; 45.90% negative; 13.02% >10 ms. Absolute median 32 ms for both; p90 456 vs 451 ms. Bytes: +1,176 B client→server, +1,088 B server→client (median). Failures: 57.08% before crypto (DNS 33.34%, TCP 23.74%), 23.64% reject TLS 1.3, 19.28% handshake-phase (80.7% of those "no common cipher suite"); decode/packet-length errors <0.16% of handshake failures → MTU/fragmentation not a barrier. 468 domains (0.05%) region-dependent in Jul 2025 (CloudFront propagation), converged by Mar 2026.
- **RQ5:** provider-managed PQ domains *retain more legacy* (TLS1.0/1.1 18.0% vs 14.7%; deprecated ciphers 73.6% vs 49.9%; BEAST 17.2 vs 14.3; BREACH 50.6 vs 31.7) but better certs (OCSP stapling 18.2 vs 3.9%, hostname mismatch 0.7 vs 10.4%). Owner-managed PQ domains modestly stricter (legacy 10.5 vs 11.9; deprecated ciphers 46.9 vs 52.6; Sweet32 6.8 vs 4.5 worse).
- **Discussion claims:** CDNs are "deployment multipliers"; software availability (OpenSSL 3.5.0 Apr 2025) is insufficient; TLS 1.1→1.2 took ~5 years to 15%, TLS 1.3 reached 48% in 2y4m, PQ-TLS reached 47.37% in 1y3m. Long-tail inertia is a growing risk. Recommends guidance/tooling for owner-managed systems, engaging providers, continuous measurement.
- **Stated limitations:** public Top-1M only; no intranets/VPNs/internal; HTTPS only (not email, messaging, "custom services"); cloud VPs → "may not fully capture the experience of end users operating from residential networks, enterprise environments, or constrained network conditions… last-mile latency, congestion, device heterogeneity". Viability = well-provisioned paths only.
- **CORRECTION for N1 claim ledger:** the paper **never mentions mobile apps or app API endpoints** (grep: no "mobile", no "API"). N1_Implementation_Plan E7 says it "explicitly excludes mobile apps and custom API endpoints"; actually the exclusion is by construction (Top-1M web domains, HTTPS, server-side only, cloud VPs). Rephrase as "its sample is web domains from cloud vantage points; client stacks, mobile apps and app back-ends are outside its design".
- **Relevance:** G4/G8 baseline numbers (finance 59%, gov 38%); attribution method (infra- vs owner-managed) reusable for G8 hosting; differential latency method for G11; RQ5 shows PQ coexists with legacy (cf. Cloudflare/Google accepting RSA key transport in our M1 probe).

### A02 Dubey & Varshney 2026, Measurement Study of Post-Quantum Readiness of Internet: 2026 (arXiv 2606.16473v1; IIT Jammu)
- **Q:** PQ readiness of real TLS deployments across sectors: TLS versions, cipher suites, key exchange, certificates, CDN/web server, sector heatmap, HNDL risk label.
- **Data:** 32,011 domains = 31,884 Tranco + 127 Indian banks from the RBI list. Sector table is skewed: BFSI 183, FinTech 128, Insurance 112, Government 921, Defence 328, … **"Others" 27,118** (85%). Single vantage (India, implied), single snapshot.
- **Method:** Python pipeline: Selenium + Chrome DevTools Protocol (securityDetails of Network.responseReceived) → negotiated TLS version/cipher/group; `openssl s_client` for handshake + `openssl x509` for cert algorithms; cURL headers for Alt-Svc (h3), server, CDN header heuristics; 50 threads; Wireshark + Chrome Security panel for spot validation. HNDL risk rule: PQ/hybrid → LOW, classical → HIGH.
- **Results:** TLS 1.3 52.41% (16,779), TLS 1.2 15.70% (5,024), QUIC/HTTP3 31.89% (10,208). Key exchange: **X25519MLKEM768 49.30%**, X25519 38.15%, P-256 10.33%, P-384 1.40%, P-521 0.71%, RSA 0.09%, X448 0.01%. Cipher: AES-256-GCM 19,837 domains, AES-128-GCM 6,319, ChaCha20 127; TLS 1.2 suites: ECDHE-RSA-AES128-GCM 2,305, ECDHE-RSA-AES256-GCM 2,031, etc. **Certificates: RSA 56.9% (SHA256-RSA 54.05%), ECDSA 43.1%; 0% PQ or hybrid certificates.** CDN: Cloudflare 37.97%, CloudFront 7.71%, Fastly 3.17%, Akamai 2.39%, Google 1.76%, hidden 45.37%. Web server: Nginx 19.37%, Apache 16.25%, Cloudflare edge 35.93%, hidden 35.56%.
- **Client-side fallback observation (important for N1):** the same bank, icici.bank.in, negotiated QUIC + TLS 1.3 + X25519 + AES-256-GCM on one device but TLS 1.2 + ECDHE-RSA + AES-128-GCM on another device → "negotiated values depend on both client (browser, OS, crypto library) and server". They conclude quantum resilience "requires client-side modernization", but only show two devices, no systematic client study.
- **Sector heatmap (qualitative):** BFSI "Low" PQ adoption/High risk; Government, Defence, Telecom, Energy "None"/High; Cloud/CDN, Social, Search "High"/Low risk. No sector percentages or confidence intervals given; heatmap labels are judgment.
- **Lists of PQ-default software (useful facts):** X25519MLKEM768 default in Chrome 131+, Firefox 132+ desktop / 145+ Android, Safari 26+, Edge 131+, Tor Browser 15+, iOS 26/macOS 26 system-wide; libraries Go 1.24+, OpenSSL 3.5.0+, Node 24.5/22.20, BoringSSL, rustls 0.23.22+, Botan 3.7; servers NGINX (with OpenSSL 3.5), Caddy 2.10; Windows Server 2025/Windows 11/.NET 10 add ML-KEM/ML-DSA. "PQC support is not implemented at the application layer but inherited from libraries" (supports N1's layer-attribution idea).
- **Framing to note:** uses the naive "AES-128 → Grover 64-bit" label for every suite (no MAXDEPTH, contrast G02/G05). Treats hybrid as "quantum resistant"; lists hybrid limitations (new PQC, implementation complexity/side channels, downgrade attacks).
- **Future work (stated):** PQC certificates, fully PQ handshakes, performance/interoperability of PQ authentication, deployment strategies.
- **Weaknesses I see:** Chrome-negotiated values conflate client and server; tiny BFSI sample; no longitudinal; no statistics; India-centric bank list; HNDL risk is a binary label, not a cost.
- **Relevance:** independent confirmation of ~49% hybrid default (same as A01 Mar 2026); the device-dependent fallback at an Indian bank is anecdotal evidence for N1's "client stack decides" thesis (G1/G3); certificate 0% → G9/O4.

### A03 Loizou & Ghadafi 2026, Measuring PQ TLS Deployment Across UK Internet Sectors (arXiv 2608.02147v1; Newcastle Univ.)
- **Q:** RQ1 prevalence of observable PQC over HTTPS vs SMTP STARTTLS; RQ2 sector variation; RQ3 sector vs infrastructure provider as predictor; RQ4 provider concentration. Secondary: leaf-certificate signature algorithms.
- **Data:** 4,665 UK organisations, 10 sectors, sector-stratified (≤500 per sector): 8 commercial sectors from Moody's FAME by primary SIC code (Finance & Insurance = SIC 64/65/66), GOV.UK domain list (500), all 165 HE institutions. Police dropped (<50 threshold). One domain per organisation (primary website). Single snapshot: **30 June 2026**.
- **Method:** OpenSSL TLS 1.3 handshakes offering 4 groups (X25519MLKEM768, SecP256r1MLKEM768, MLKEM1024, SecP384r1MLKEM1024) on 443; SMTP STARTTLS on 25 to highest-priority MX (deduplicated MX). Provider attribution with open-source `whohosts` (CNAME, PTR, AS, WHOIS, HTTP headers); MX pattern matching for mail. Stats: Wilson 95% CIs; McNemar for paired HTTPS vs SMTP; chi-square + Cramér's V for sector; logistic regression (sector / provider / both) with 5-fold CV (grouped by MX host for SMTP), AUC; concentration via top-1/top-3 share and HHI. Ethics: Menlo Report, minimal handshakes, pseudonymised identifiers, ≥50 per reported cell.
- **Results:** reachability HTTPS 87.10% (4,063), SMTP 82.70% (3,858). **HTTPS PQC 44.0% (CI 42.5–45.5%), SMTP 6.4% (5.6–7.2%).** X25519MLKEM768 1,787 endpoints; SecP256r1MLKEM768 161; SecP384r1MLKEM1024 59; MLKEM1024 3. **Finance & Insurance: 177 of 425 HTTPS (~41.6%)**; Government 255/455 (~56%); Retail 230/454; Technology 212/437; University 39/148 (~26%). Paired (3,510 orgs): both 144, HTTPS-only 1,419, SMTP-only 84, neither 1,863; McNemar χ²=1184, **matched OR 16.89 (13.56–21.05)**. Sector association significant but small (Cramér's V 0.145 HTTPS, 0.207 SMTP). **AUC: HTTPS sector-only 0.573 vs provider-only 0.957 (both 0.962); SMTP sector-only 0.156 (grouped CV) vs provider-only 0.994.** Cloudflare 1,247/1,312 = 95.05% PQ; Fastly 96.30%; Amazon AWS 37.62%; Microsoft 1.53%; Google (web) 6.82%; Akamai 1.40%; small UK hosts (20i, Krystal) 0%. Cloudflare = 69.7% of PQ HTTPS endpoints; top-3 (Cloudflare, AWS, Fastly) 86.9%. SMTP: Microsoft 1,714 endpoints 0% PQ; Google 242/242 = 100% and 98.4% of all PQ SMTP. HHI 1,378 (HTTPS) vs 2,797 (SMTP). Certificates: SHA256-RSA 2,561 HTTPS / 3,824 SMTP; ECDSA-SHA256 940; ECDSA-SHA384 540; **0 PQ signatures**.
- **Interpretation:** "observable PQC support … reflects infrastructure-provider deployment decisions … should not be interpreted as a comprehensive measure of organisational migration readiness"; single-protocol scans overstate readiness. Mentions UK NCSC roadmap (discovery/planning by 2028), Google and Cloudflare targeting 2029 for full PQ migration.
- **Compared to A02:** criticises A02 for browser-negotiated values (client+server interaction) vs their server-side probing; A02 not stratified.
- **Limitations (stated):** UK only; HTTPS+SMTP only, no internal systems or other protocols; attribution approximate; only OpenSSL-supported groups; FAME "first 500" not a probability sample; single snapshot, no trends; SMTP orgs not independent; suggests opt-out page for future scans.
- **Future work:** longitudinal; combine protocol measurement with provider attribution to separate provider-driven from organisation-driven migration.
- **Relevance:** the design N1 should mirror for Bangladesh (sector-stratified sample, Wilson CIs, provider-vs-sector logistic regression, HHI). Strong evidence for "who decides = the provider", which N1 extends to the **client** side (OS/framework). App API hosts are not in any sampled list → G8.

### A04 Mallick, Kundu, Kompella 2026, Study of Post Quantum status of Widely Used Protocols (arXiv 2603.28728v1; Cisco Research, summer-2025 internship)
- **Type:** survey (no measurement). 9 protocols: TLS, SSH, QUIC, IPsec/IKEv2, OpenVPN, BGP/RPKI, DNSSEC, OpenID Connect, Signal. Per protocol: current crypto, quantum safety, migration efforts, challenges. Snapshot "as of 2025".
- **Key claims:** TLS and Signal lead (hybrid deployed at scale); IPsec (RFC 8784 PPK, RFC 9370 multiple key exchanges) and SSH (OpenSSH sntrup761x25519 since 8.5) standardised but limited production; DNSSEC and BGP face structural size barriers (1,232-byte UDP limit; Dilithium 2–3 KB vs 64-byte ECDSA per AS hop). **"Across all protocols, key exchange proves consistently easier to migrate than authentication"; "protocol-level limitations such as message size and fragmentation often dominate over raw algorithm performance."** NIST IR 8547 draft: deprecate RSA/ECDSA/EdDSA/DH/ECDH by 2030, disallow 2035; HQC selected Mar 2025.
- **TLS section facts:** TLS 1.3 mandates ephemeral (EC)DHE; HNDL circumvents forward secrecy; symmetric AEAD "considered safe … Grover quadratic speedup not practical at scale"; cites Sikeridis (1–300% latency for PQ auth), KEMTLS (fewer bytes, +1 RTT for server data), Sosnowski (hybrid negligible; PQ keys can trigger extra round trips on constrained networks), Gonzalez & Wiggers (KEMTLS −38% handshake time on Cortex-M4 over LTE-M/NB-IoT).
- **QUIC:** byte size (not computation) dominates; UDP fragmentation + middleboxes; PQ changes interact with congestion control, connection migration and **0-RTT resumption — "not yet well understood"**.
- **IPsec:** long-lived tunnels → one broken DH exposes the whole tunnel lifetime (an amortisation argument); Twardokus et al. 400–1000× data overhead on lossy wireless links.
- **OIDC (relevant to G6, app-layer crypto):** ID tokens are JWT RS256/ES256; IdP keys are public via JWKS and long-lived → "a quantum adversary would not even need to intercept traffic; they could simply download the public key and compute the private key offline"; blast radius = every user of that IdP. Schardong et al.: PQ OIDC feasible but network latency amplifies PQ sizes.
- **Signal:** PQXDH (X25519 + Kyber-1024) since late 2023; KEMs not naturally secure under prekey reuse (Brendel split-KEMs); SPQR.
- **Quality flags (important if cited):** a stray "Opus 4.6Extended" string appears inside the TLS section text (LLM-assistance artefact); stale numbers ("as of early 2024, 2% of Cloudflare TLS 1.3 connections" in a 2026 paper); describes Rainbow/SIKE as finalists without noting they are broken (SIKE break is mentioned). Cite for the cross-protocol framing only, not for numbers.
- **Relevance:** supports "key exchange first, authentication later" (why N1 measures key exchange); OIDC/JWT point maps to G6 (app-layer RSA/ECDSA in finance apps) and suggests a "no interception needed" class for public-key material embedded in APKs; QUIC 0-RTT gap relates to G15/M1(c).

### A05 Balaji, Varshney, Ravi, Jain, Foe, Seet, Wang, Lam, Chattopadhyay 2026, Operationalising PQ TLS … Financial Infrastructure (arXiv 2605.17955v1 = ePrint 2026/959; NTU Singapore, PQStation, OCBC Bank)
- **Thesis:** the bottleneck is **operational, not algorithmic**: banks terminate TLS at dozens–hundreds of heterogeneous points (web servers, API gateways, load balancers, reverse proxies, DB servers); teams lack visibility of what each is *configured* to allow. Network scanners see only negotiated behaviour, not permitted-but-unused fallbacks (TLS 1.0, weak ciphers), HSM key references, session policy.
- **C1 tool:** deterministic config parser PARSE → NORMALIZE (Unified TLS Model, 8 sections, every field with `derived_from` provenance) → COMPARE against NIST SP 800-52r2, PCI-DSS v4.0, CIS, Mozilla profiles and a quantum-readiness policy that flags Shor/Grover-vulnerable components. Supports nginx (crossplane), Apache (apacheconfig), Spring Boot (YAML profile merge). Detects HSM via PKCS#11 URIs. Five-phase loop: Discover → Assess → Prioritise → Migrate → Verify.
- **C3 (called C2 in places) measurement:** 8,443 unique nginx configs from GitHub (5,524 active, 2,919 archived repos) → 12,875 server blocks → 5,982 TLS contexts. TLS 1.2 95.8%, TLS 1.3 73.5%, TLS 1.1 21.6%, TLS 1.0 19.4% (21.8% permit 1.0/1.1). 37.6% of explicit cipher lists contain a weak token. **Key exchange: ECDHE/DHE 71.1%, RSA key transport 28.9%, PQ hybrid 0.0%.** Of 625 contexts setting `ssl_ecdh_curve`: secp384r1 528, X25519 96, prime256v1 67, secp521r1 63, auto 49, **X25519MLKEM768 4 (0.8%)**. HSTS 38.2%; mTLS 6.2%; session cache default 50.9% / shared 47.6%; Let's Encrypt 34.4%; leaf-only chains 53.3%; 29.7% delegate to framework defaults; archived repos worse (legacy presets 47.3% vs 30.8%). **42.6% of contexts use non-production hostnames → corpus is mostly templates/tutorials.**
- **C2 OCBC proof-of-concept:** 3-tier internal banking app: Apache reverse proxy (OpenSSL + OQS provider → X25519MLKEM768, fallback X25519) → Java/Spring Boot API gateway (BouncyCastle JSSE + PQC providers registered at JVM start; JSSE is classical by default) → internal app. Zero application code changes. h2load, 100 concurrent clients, 30 s, **X25519 vs ML-KEM-512**: time-for-connect 24.7 → 30.4 ms (+23%); time-for-request 779.3 → 789.2 ms (+1.3%); throughput −1.6%; 0 errors. Certificates unchanged (RSA/ECDSA).
- **Lessons:** migrate the outermost termination layer first; Java needs explicit provider registration ("not enabled by default"); assess HSM firmware for ML-KEM first; certificate migration later.
- **Limitations (stated):** GitHub corpus over-represents dev/templates; production bank configs not public; only nginx/Apache/Spring Boot (no HAProxy, Envoy, IIS, Tomcat, cloud-managed TLS); key exchange only; single institution.
- **Future work:** more technologies; longitudinal GitHub tracking; ML-DSA certificates.
- **Quality flags:** performance test uses ML-KEM-512 (called "hybrid") rather than the X25519MLKEM768 it deploys; C2/C3 numbering swapped between intro and discussion; reference [17] literally "TODO"; 21.6/19.4 vs 21.8% figures. Treat numbers with care.
- **Relevance:** only bank-side PQ deployment report; directly supports N1's G8/G13 framing that *server side* (API gateway, Java stack) needs explicit action; config-vs-negotiated distinction parallels N1's static (APK) vs dynamic (pcap) layers (G12). Java default classical ↔ JEP 527 for Java servers (N1 reading item 12). The 28.9% RSA key transport in templates is evidence for M1(b).

### A06 Kwiatkowski, Sullivan, Langley, Levin, Mislove 2019, Measuring TLS key exchange with post-quantum KEM (2nd NIST PQC Standardization Conference; Cloudflare, Google, UMD, Northeastern)
- **Type:** 4-page **experiment design** (results not in this paper; later published on the Cloudflare blog). Keep this in mind when citing: cite it for the design and questions, not for findings.
- **Design:** CECPQ2 (X25519 + NTRU-HRSS; pk = ct = 1,138 B; fast: keygen 3,952/s, encaps 76,035/s, decaps 21,906/s) vs CECPQ2b (X25519 + SIKE/p434; pk 330 B, ct 346 B; slow: ~200–370 ops/s) vs classical control. Server: all Cloudflare TLS-terminating edges; logs handshake duration, ServerHello→client Finished time (isolates client-side + network delay), handshake size, client IP, ASN, User-Agent (browser/OS/CPU) and **device type (mobile vs desktop)**. Client: Chrome Canary on x86-64 (Windows, Linux, macOS, ChromeOS) and **aarch64 Android**; 6 groups {SIKE, HRSS, control} × {x86-64, aarch64}; only aggregate histograms (no PII). Hybrid by concatenating X25519 and PQ outputs (draft-stebila-tls-hybrid-design); TLS 1.3 only; client always also sends an X25519 share to avoid an extra round trip.
- **Motivating prior result (Langley 2018 dummy-extension experiment):** small-key PQ gives a latency benefit to ~5% of devices, but **~5% of clients see much larger latency increases than expected**. Hypothesis: middleboxes and buffer-bloated/lossy wireless links. Follow-up: traceroutes from near servers to slow clients' ASes; obtain machines inside problematic networks; TTL-limited probes, MTU probing.
- **Research questions they posed (still relevant):** how key size vs speed affects clients; how different OSes/architectures/**network connectivity** respond; which networks host problematic middleboxes; long-tail performance per AS/device; can a client pick an algorithm from properties known before connecting.
- **Relevance:** the template for N1's G10 (network path/operators) and G11 (cost on Bangladeshi networks): the original concern that PQ cost concentrates in the long tail (mobile, lossy, middlebox-laden networks) — precisely the networks A01 says it did not measure. Shows Android was part of the Chrome-side experiment from the start (browser stack), which contrasts with Android's platform TLS today.

### A07 Holz, Amann, Razaghpanah, Vallina-Rodriguez 2019, The Era of TLS 1.3: Measuring Deployment and Use with Active and Passive Methods (arXiv 1907.12762v2)
- **Q:** first study of TLS 1.3 deployment (servers) and use (clients), incl. mobile apps, ~9 months after RFC 8446.
- **Three data sources:** (1) active scans 1–5 May 2019 from an Australian university: Alexa 1M, com/net/org 164M, 1,120 new gTLDs 23.4M, **54 ccTLDs 87.9M** (no .uk, no .bd); massdns → zmap 443 → modified goscanner with TLS 1.3 first preference; full PCAP + Zeek; IPv4 only. (2) Passive: ICSI SSL Notary (since 2012, >400 B connections, 5–8 N. American sites) + 4 days (9–13 May 2019) at an Australian campus (379.7 M connections). (3) **Lumen Privacy Monitor** (Android VPN-permission app, user-space stack, maps flows to app package/process; 22,000 users in 100+ countries, Nov 2015–Apr 2019; browsers excluded): **11.8 M TLS connections from 56,221 apps to 149,389 SNIs**. Hosting attribution via published IP ranges (Cloudflare, AWS, Azure), bgp.he.net, NS records.
- **Deployment:** TLS 1.3 on 18.5% Alexa domains (21.7% of TLS domains), ~5% com/net/org and ccTLDs. Huge ccTLD spread: cf 80.1%, tk 75.0% (free domains on Cloudflare), ua 42.3%, sk 40.0%, pl 28.0% … in 6.8%, de 3.8%, fr 3.2%, jp 2.8% — explained by dominant local hosters (e.g., Inhosted, websupport.sk, nazwa.pl, value-domain.com) and Cloudflare. **Cloudflare hosts 59.8% of TLS 1.3-enabled Alexa domains** (up to 82.9% in mid ranks); Amazon almost none. Incomplete handshakes: 4% Alexa, 17–19% zones, cn 44%, de 39%. Server cipher choice (client order AES128, ChaCha20, AES256): AES-128-GCM ~90%; ccTLDs AES-256 29.6%.
- **Use (passive):** Notary: TLS 1.3 negotiated in 4.6% of connections (Apr 2019) while **39.8% of clients offer it** (client-ahead). Facebook servers terminate 60.78% of TLS 1.3 connections (custom FB23/FB26 drafts from its apps); Cloudflare owns 70.45% of TLS 1.3 IPs but few connections. Australia: Google 52.46% of TLS 1.3 connections. **Ciphers in TLS 1.3 connections: AES-128-GCM 79.2%, AES-256-GCM 14.4%, ChaCha20-Poly1305 6.4%** (useful pre-PQ baseline for G15/M4). **Resumption: 9.7% of TLS 1.3 connections carry pre_shared_key (Aus 12.6%), 92% accepted; 0-RTT early_data in 6.8% of TLS 1.3 connections = 70% of resumption attempts (Aus 33%). HelloRetryRequest in 4% (Australia).** 93.4% of clients still list TLS 1.0/1.1 in supported_versions; GREASE 56.7%.
- **Android (the key precedent for N1):** "**As of today, Android does not provide native TLS 1.3 support to Android apps** (only Android Q beta since Mar 2019) … most Android apps use native OS libraries with default configurations for their TLS needs … only users of Android Q beta and apps from large companies like Google, Facebook and Mozilla can use TLS 1.3." Lumen TLS 1.3 share rose 0.01% (Jan 2018) → 4% (Mar 2019); TLS 1.2 still 94.9%. **Client support in apps lags server support**; pre-Q, TLS 1.3 apps used their own stacks (Facebook Fizz, bundled OpenSSL 1.1). "Given developers' reliance on platform-provided TLS libraries, it seems unlikely that we will observe a massive support of TLS 1.3 in Android applications until Android Q is officially released."
- **Discussion:** fast uptake caused by few providers who control both ends (Google: Chrome + services; Facebook: apps + servers); providers controlling only one end (Amazon, Azure) are disadvantaged; middleboxes forced protocol redesigns (supported_versions, GREASE); TLS 1.3 encrypts more → passive measurement gets harder.
- **Limitations:** IPv4 only; Notary best-effort with drops; Lumen excludes browsers; no new-extension checks.
- **Relevance (high):** (i) exact historical analogue of N1's hypothesis: a new TLS feature reached Android apps only via the OS release or app-bundled stacks; (ii) Lumen-style on-device VPN capture with per-app attribution is a method option for N1 (vs hotspot capture); (iii) baseline numbers for resumption/0-RTT/HRR/cipher shares to compare with PQ-era app traffic (G15, M1(c)).

### A08 Ibrahim, Ajith, Haroon 2026, Detecting PQ and Hybrid TLS Deployments via Raw TLS Record Inspection (IACR ePrint 2026/834; Ulster Univ. London)
- **Idea:** classify endpoints from wire evidence, not config: open TCP socket, capture records, keep ContentType 0x16, parse ServerHello, find key_share (ext 0x0033), read 16-bit group → CLASSICAL_ONLY {0x001d X25519, 0x0017 secp256r1…}, PQC_ONLY {0x0200/0x0201/0x0202 ML-KEM-512/768/1024}, HYBRID_CONFIRMED {0x11EB SecP256r1MLKEM768, 0x11EC X25519MLKEM768}, UNKNOWN. Evidence tuple W=(node, target, group, class). Fragmentation (ClientHello > MTU) as auxiliary signal.
- **Findings:** (1) **False-positive trap:** their OpenSSL-subprocess fallback merged stderr+stdout and regex-matched "X25519MLKEM768"; stock OpenSSL 3.0.13 prints "group 'X25519MLKEM768' cannot be set" → 100% false HYBRID on 19 endpoints; fixed by separating streams and gating on exit code 0. (2) **Survey of 38 UK endpoints (7 Apr 2026, 8 sectors incl. CDN, Big Tech, finance) all CLASSICAL_ONLY — an artefact: their client (stock OpenSSL 3.0.13) never offered PQ groups.** Their own conclusion: "**PQC deployment measurement requires OQS-capable client tooling** — a requirement not explicitly addressed by prior measurement studies." nhs.uk negotiated real TLS 1.2 (no supported_versions ext). (3) Testbed: Node-C's application initialised ML-KEM-768/ML-DSA/Falcon (app-layer PQC) but its nginx 1.18/OpenSSL 3.0.2 front end was classical → **application-layer vs transport-layer mismatch invisible to config audits**; after an OQS front-end upgrade it negotiated 0x11EC. Compliance pipeline with KAT self-tests (ACVP vectors), PQC-only policy verdicts, Lean 4 proof obligations.
- **Quality flags:** tiny n; claims "ServerHello may reach 2 MB for hybrid" (wrong; ~1.1 KB extra per A01); unresolved citations "[?]"; no statistics.
- **Future work:** Internet-scale with OQS-capable clients; QUIC; continuous monitoring; link to symbolic verification.
- **Relevance (high for N1 tooling):** (i) N1's `n1_tools.py pcap` uses the same ServerHello-group method; cite as concurrent work and adopt their 4-state labels + group-ID table; (ii) the "client must offer PQ" lesson is N1's thesis in miniature — **measured protection is a joint client×server property**, so app measurements must log both ClientHello offers and ServerHello choice; (iii) app-layer PQC ≠ transport PQC (G6 vs G4); (iv) guard n1_tools against the stderr false-positive.

### A09 Cho, Hyoung, Kim, Sim, Chattopadhyay, Seo, Kim 2025, Toward Crypto Agility: Automated Analysis of Quantum-Vulnerable TLS via Packet Inspection (IACR ePrint 2025/1549; Hansung Univ. Korea + NTU)
- **Tool:** open-source (github.com/kpqc-cryptocraft/Crypto-Agility) live packet analyser (WinPcap/libpcap, OQS + OpenSSL). Hierarchical filtering: interface → SNI → Ethernet (IPv4 only, 0x0800) → IPv4 (TCP only, proto 6) → TCP → TLS record → handshake types ClientHello/ServerHello/Certificate → ports 443, 8443, 4450. Extracts SNI, TLS version (via supported_versions), cipher suite, key_share group, certificate public-key algorithm/issuer CN/expiry. **TLS 1.3 certificates are encrypted → they open a second connection to the SNI with OpenSSL to fetch the chain**; OID byte-matching instead of full X.509 parse (179.14 vs 182.57 ms/cert, only 1.88% faster).
- **Scoring:** H/M/L per element (weakest-link): H = TLS 1.3, AES-256, PQ levels 2–5 (ML-KEM-1024, ML-DSA); M = TLS 1.2, AES-128, SHA-256; L = ≤TLS 1.1 and quantum-vulnerable public-key (RSA/ECDHE). **They label NIST level-1 PQC (≈AES-128) as quantum-vulnerable** "due to limited margin". Certificate T/F = expires within 90 days (migration timing).
- **Evaluation:** 192 TLS sessions from 20 enterprises on Windows 11 + Kali; recall TLS version 96.35% (185/192), cipher 94.27%, migration flag 98.44%.
- **Domestic (Korea: Naver, Coupang, Kakao, Samsung, Hyundai, Yes24, Kiwoom, SK Telecom, Toss, Shinhan Bank) vs global (Google, Instagram, YouTube, Netflix, Amazon, Microsoft, Apple, PayPal, Tesla, Mastercard):** TLS 1.3 40% vs 90%; **hybrid ML-KEM key exchange 0% vs 40%** (Google, Instagram, YouTube, PayPal); cipher readiness 100% both; PQ/ECC cert 0% both; ≤90-day certs 40% vs 50% in Fig. 7 but "10%" in the conclusion (inconsistent). Korean banks/finance (Shinhan, Toss, Kiwoom) on TLS 1.2 + ECDHE_RSA. Conclusion: domestic services lag; certificates ~1 year vs 90 days limits agility.
- **Limitations I see:** IPv4/TCP only → **misses QUIC/HTTP3 entirely** (and IPv6); desktop browser traffic, not mobile apps; n = 10 vs 10; certificate fetched out-of-band may differ from the one served to the app; "ECC certificate = readiness" contradicts their own L label for ECC. Future work: benchmark vs Palo Alto/PQStation/SandboxAQ; internal systems; QUIC with AI.
- **Relevance:** the closest "domestic vs global" design to N1 (Bangladeshi finance vs global CDNs), done in another Asian country with domestic finance lagging; reusable open-source pcap analyser; warns N1 to include QUIC and IPv6 in captures and to record the app's own certificate rather than refetching.

### B01 Mankowski, Wiggers, Moonsamy 2023, TLS → Post-Quantum TLS: Inspecting the TLS landscape for PQC adoption on Android (EuroS&P Workshops 2023; RUB, PQShield/Radboud)
- **Q:** how do top Android apps use TLS (handshake counts, resumption, TLS 1.3, QUIC, session length), and what will PQ cost given that usage?
- **Method:** top-45 free "Apps" + top-45 "Games" in German Play Store chart (23 Jan 2023), 90 apps (downloads 100K+–5B+, median 10M+); Selenium scraper → Raccoon APK downloader → ADB install on **one Nokia G11, Android 11**; hotspot capture with tshark; **5 minutes** of manual interaction per app (pre-test on 10 apps showed no change after 5 min); one pcap per app; Python reconstructs TCP/UDP streams. **No decryption** → cannot separate OS background traffic: calibration with the calculator app for 60 min gave 44 handshakes (median 3, max 12 per 5 min) → "negligible". Dataset public (Zenodo 7950522).
- **Results (Table 1):** handshakes per app median 94 (mean 144) [Apps 57, Games 135]; resumptions median 14 (mean 36); unique servers median 37; traffic median 6.2 MB; session time median 1.8 s (Apps 1.1 s, Games 2.3 s); **TLS 1.3 share median 69% (mean 66%)** despite Android 10+ support; QUIC handshakes median 9 (mostly Google/Facebook servers). Only ~31% (median) of repeat connections to the same host use resumption. Extremes: Candy Crush 917 handshakes / 900 resumptions to 9 servers; Klarna TLS 1.3 in only 11% of 56 handshakes; PayPal 75%; Instagram 94%. **Banking app S-pushTAN: only 4 handshakes (no bank account)**; WhatsApp/Telegram low (no SIM); ElsterSecure (German tax) 40% TLS 1.3. X25519 used in "the vast majority" of handshakes.
- **PQ impact estimate:** assumes every full handshake = 2 ephemeral key shares + 3 signatures + 2 certificate public keys; X25519 + RSA-2048 ≈ 1,376 B → Kyber-512 + Dilithium2 = 1,586 B KEX + 9,984 B auth ≈ 11.5 KB (**>8×**). Examples (Table 4): Klarna 51 full handshakes 70.2 KB → 584.1 KB; Lighter Simulation 353.6 KB → 2.94 MB; Haircut prank 440.3 KB → 3.66 MB. Dilithium3 auth 13,783 B would exceed TCP initcwnd → extra RTTs (Sikeridis). Candy Crush's 900 resumptions saved ~1.13 MiB (~20%).
- **Recommendations:** fewer handshakes, connection reuse, resumption; **Android's standard HTTPS library could default to HTTP/3 + resumption**; OS profilers for developers; server operators must share session DBs/ticket keys across servers (which are themselves sensitive, MitM risk); **KEMTLS** (−2,164 B auth) and **KEMTLS-PDK** for apps with hard-coded hosts (bundle the server's long-term KEM key in the APK; with McEliece only a 96-B ciphertext → handshake ≈ psk_dhe size) (Table 5: TLS 11,452 B; KEMTLS 9,288 B; PDK-Kyber 2,336 B; PDK-McEliece 1,664 B).
- **Limitations (stated/implicit):** one device, one OS version, one country; no decryption; 5-min manual sessions; accounts/SIM missing → finance and messaging under-exercised; **measures no key-exchange groups (pre-PQ) and no framework attribution; no iOS**.
- **Future work:** attribute connections to ad/analytics/logging libraries; large-scale real-user telemetry for mobile (like Firefox telemetry study).
- **Relevance (very high):** the closest prior work to N1 and the method N1 copies (hotspot + tshark + 5 min). N1's openings: post-deployment PQ negotiation, framework/OS attribution, iOS vs Android, finance apps with real accounts, developing country, SDK attribution (their own future work = N1 G5). Their cost model gives N1 a G11 baseline; their "resumption saves bytes" point is the flip side of N1's M1(c) (resumption without fresh key exchange inherits HNDL exposure).

### B02 Pradeep, Paracha, Bhowmick, Davanian, Razaghpanah, Chung, Lindorfer, Vallina-Rodriguez, Levin, Choffnes 2022, A Comparative Analysis of Certificate Pinning in Android & iOS (ACM IMC 2022)
- **Q (RQ1–5):** detect pinning platform-agnostically; who pins (popular vs random, categories, destinations); consistency across Android/iOS for the same app; how pinning is implemented (PKI, CA vs leaf, cert vs key, which code); connection security and what pinned flows carry.
- **Data (2021, US stores, from North America):** Common 575 (same app on both stores via AlternativeTo), Popular 1,000 per platform, Random 1,000 per platform (from 1.35 M Android IDs / 1.25 M iOS IDs) = 5,079 unique apps. iOS download via automated iTunes 12.6 (semi-manual, limits scale).
- **Static:** Android NSC `<pin-set>`; embedded certificates (.der/.pem/.crt/.cer, "BEGIN CERTIFICATE"); SPKI hash regex `sha(1|256)/[a-zA-Z0-9+/=]{28,64}`; apktool, Flexdecrypt/Frida-iOS-Dump, ripgrep, radare2 for native libs; crt.sh lookup of SPKI hashes; manual attribution of code paths appearing in >5 apps to third parties. **Dynamic:** Pixel 3 Android 11 and jailbroken iPhone X iOS 13.6, mitmproxy CA installed, Wi-Fi hotspot; each app 30 s (15/30/60 s gave 20.78/23.5/24.62 handshakes), **no UI interaction** (random interaction did not change domains); differential non-MITM vs MITM run → a destination is pinned if used without MITM but always fails with MITM; TLS 1.3 "used connection" heuristic (>2 encrypted records or 2nd ≠ alert length); 99% of TLS has SNI. Frida unpinning succeeded for 51.51% (Android) / 66.15% (iOS) destinations. iOS "associated domains" traffic excluded (OS-triggered; 2-min wait in re-run).
- **Results:** dynamic pinning: Common 8.17% Android / 8.52% iOS; **Popular 6.7% / 11.4%**; Random 0.9% / 2.5%. Static potential pinning up to 26.96% / 33.4%. NSC-only method (prior work) finds just 0.6–2.78% → up to **4× more** pinning than prior studies. **Finance is the top pinning category on both** (Android 22.99% of finance apps, n=20; iOS 20.63%, n=26). Of 69 Common apps that pin somewhere: 27 pin on both, 20 Android-only, 22 iOS-only; of the 27, only 15 consistent and **13 pin the same domains** → "fewer than half consistent". Pinning is selective; most pinned destinations are **third-party** (Twitter, Braintree, PayPal, PerimeterX, mParticle on Android; Amplitude, Stripe, Weibo, FraudForce, Adobe on iOS) — payment, social, analytics SDKs. Default PKI used by nearly all (Android 163 default / 4 custom; iOS 238 / 1). **Of 110 certificates matched statically+dynamically: 80 CA, 30 leaf; 24 of the 30 leaf pins are SPKI hashes** (key reuse across renewals). Two self-signed pinned certs valid 27 and 10 years. No expired certs accepted. **Weak ciphers advertised: iOS overall 93.39% (Common) / 95.2% (Popular) / 82.6% (Random) vs Android 8.35% / 18.3% / 3.1%** — a platform-default effect; pinned connections usually stronger. PII: only iOS advertiser ID significantly higher in pinned traffic.
- **Limitations (stated):** obfuscation/runtime certs missed; partial code coverage; no login → pinned flows behind login missed (finance under-observed); iOS associated domains excluded (underestimate); ~3,000 apps; official stores and free apps only.
- **Future work:** developer survey on why pinning differs across platforms; automated app exploration incl. sign-up/login; better unpinning.
- **Relevance:** G9 method (NSC + SPKI regex + crt.sh + MITM differential); finance pins most → **the PQ certificate migration (ML-DSA/MTC) could break pinned finance apps**, a question this paper never asks; leaf-SPKI pinning means the server key is fixed in the app — a PQ key change forces an app update; cross-platform inconsistency supports G3 (same company, different behaviour on Android vs iOS); the iOS-vs-Android weak-cipher gap shows **platform TLS defaults shape every app's ClientHello**, the mechanism N1's G1/G3 relies on.

### B03 Strauss, Upadhyay, Siddique, Baggili, Farooq 2025, Assessing and Enhancing Quantum Readiness in Mobile Apps (IEEE S&P 2025 poster, 2 pp.; arXiv 2506.00790; LSU, U. Kentucky)
- **Method:** static analysis of **4,018 Android apps (Google Play + F-Droid)** with CryptoAPI-Bench-inspired rules; backward data-flow to resolve `Cipher.getInstance()` / `KeyPairGenerator.getInstance()` strings (e.g., AES/CBC/PKCS5Padding, RSA/ECB/PKCS1Padding); label safe/vulnerable. Phase 2: LLM migration (GPT-4o, Claude Sonnet 3.7, Gemini Flash 2.0, DeepSeek; edit and agentic modes).
- **Threat model:** HNDL on app-layer encrypted data: capture traffic/storage, reverse-engineer APK to learn the scheme, store, decrypt later with a quantum computer.
- **Results:** MD5 28,994 instances / 2,531 apps; SHA-256 22,110 / 3,293; SHA-1 18,200 / 2,454; AES/CBC 10,219 / 2,071 ("safe with 256-bit keys"); **RSA 781 instances / 781 apps (the text says 589 apps — internal inconsistency)**. **No PQC adoption** in production APKs; some F-Droid apps import PQC classes but never use them. LLMs succeed at SHA-1→SHA-256, **none produced a correct, compilable PQC migration** (multi-file changes, missing BouncyCastle PQC imports, placeholders).
- **Weaknesses:** 2-page poster, no transport/TLS analysis, no per-category (finance) breakdown, labels MD5/SHA-1 as "broken by quantum algorithms" (they are classically broken; Grover/BHT give little extra), no dynamic validation, no key sizes.
- **Relevance:** the only app-wide crypto-API scan with a quantum lens → baseline for N1 G6 (app-layer RSA in finance apps); its gap (no TLS layer, no sector, no joint view) is N1's opening; LLM-migration failure is a side data point for G14 (developer capacity).

### B04 Razaghpanah, Niaki, Vallina-Rodriguez, Sundaresan, Amann, Gill 2017, Studying TLS Usage in Android Apps (ACM CoNEXT 2017)
- **Data:** Lumen Privacy Monitor (VPN-permission user-space capture, flow→app/process attribution, local MITM proxy with user consent; periodically skips proxying to see untouched handshakes); >5,000 users in >100 countries, Nov 2015–Jun 2017: **1,364,420–1,486,082 TLS handshakes/connections from 7,258 apps to 34,176 SNIs**, 891 (SDK, vendor, model) tuples, 684,209 proxy exceptions from 4,268 apps. Covers 87 of top-100 free apps. Browsers excluded. Dataset public (haystack.mobi).
- **Method:** **ClientHello cipher-suite-list fingerprints** (set + order) built with a custom app on stock Android 4.0–7.1 using native TLS, OpenSSL and GnuTLS (default and supported lists; validated vs SSL Labs) → each OS version/library has a unique fingerprint; security patches can change lists without changing OS version.
- **Results:** **84% of app-versions use OS-default TLS APIs with default settings; 2.3% OpenSSL; 13% other/modified** (Facebook family uses OpenSSL; Firefox NSS; VLC/SoundCloud GnuTLS; Twitter, Dropbox, Spotify, Uber, game engines, Microsoft have custom lists for first-party domains). **Third-party ad/analytics SDKs (Crashlytics, Google Analytics, Flurry, AppsFlyer) use OS defaults** (except Facebook Graph API). Twitter: after Sep 2016 first-party flows have a custom list but Crashlytics flows still OS default → one app, two TLS stacks. BlackBerry Messenger, Viber, Wire, Jio4GVoice offered only 1–3 suites **without forward secrecy** (nation-state HNDL risk with server-key access). 31 app-versions announce SSLv3 on OSes that don't; null ciphers 32 app-versions (TuneIn, K-9 Mail, F-Secure VPN); anonymous ciphers 32 (Super Mario Run); EXPORT 50; RC4 in 872 app-versions of 311 apps on newer OSes. GREASE 0%→65% of flows (Oct 2016→Jun 2017) via OS default; ALPN 28%→83%. Certificates: 99% ≥2048-bit RSA-equivalent, 0.7% weaker; 166 self-signed. **Pinning 150 apps (2.0%) to first parties, 94 (1.3%) third parties; CA bundling 52 / 20; 32 finance apps pin (PayPal, Venmo, Chase, Capital One, BofA, BBVA) but 271 finance/banking apps neither pin nor bundle.**
- **Discussion/recommendations:** apps inherit the security of the OS version they run on; **61.7% of devices (May 2017) ran Android ≤5.x**; TLS library updates tied to OS updates → propose vendor update policy or **separating TLS library from the OS (like Play Services)** (later realised as Conscrypt via Project Mainline). **Android exposes only SNI, cipher suites and protocol versions; e.g., ALPN cannot be set → apps needing it (Facebook) must bundle their own TLS library** and maintain it. Developer education.
- **Limitations:** Android only (no Lumen for iOS); crowd-sourced, uncontrolled app set; TCP only; pinning analysis limited to SDK <24 (user CAs untrusted after Android 7).
- **Future work (stated):** combine with **active server-side measurements of mobile app servers vs web servers** (= N1 G8), attack resilience.
- **Relevance (very high):** the empirical basis for N1's layer-attribution hypothesis: most app TLS = platform default; the exceptions are big companies that bundle stacks. The ALPN case is a perfect analogue of today's missing named-group API on Android (conscrypt#1452): **if the API does not expose the knob, only apps that ship their own TLS (Cronet/BoringSSL, Fizz) can enable X25519MLKEM768.** ClientHello fingerprinting = the method to attribute app connections to OS/OkHttp/Cronet/Flutter/WebView (G1, G5). SDKs follow OS defaults (G5).

### B05 Oltrogge, Huaman, Klivan, Amft, Acar, Backes, Fahl 2021, Why Eve and Mallory Still Love Android: Revisiting TLS (In)Security in Android Applications (USENIX Security 2021; CISPA, Leibniz Univ. Hannover)
- **Q:** did Google's countermeasures work: Network Security Configuration (NSC, Android 7, 2016) and Google Play safeguards (2016–17) against insecure TrustManager/HostnameVerifier/WebView onReceivedSslError?
- **Data/method:** 1,335,322 free Play apps updated since Aug 2016 (crawled to Mar 2020 from Germany); **99,212 with custom NSC**, 2,812 obfuscated excluded → 96,400 analysed statically (XML parse of base-config/domain-config/debug-overrides, pin-sets, trust-anchors, cleartext flags; pins matched to fetched chains and Android system roots); manual MitM on 40 apps (20 random + 20 privacy-sensitive); **controlled experiments publishing deliberately vulnerable apps to Google Play**; CryptoGuard on 15,000 random apps (10-min cap, no reachability).
- **Timeline (Table 1):** Android 6 usesCleartextTraffic flag (2015); Play blocks unsafe X509TrustManager (May 2016); Android 7 NSC + user CAs distrusted (Aug 2016); Play blocks unsafe WebView handler (Nov 2016) and HostnameVerifier (Mar 2017); Android 9 cleartext off by default (Aug 2018); target-SDK floors (new apps ≥8 from Aug 2018, updates ≥8 Nov 2018, new ≥9 Aug 2019, updates ≥9 Nov 2019). **NSC adoption jumped only when Android 9 + Play target-SDK requirements forced it (early 2019)** — defaults and store policy drive behaviour.
- **Results:** **88.87% (88,174) of custom NSC files downgrade security vs defaults**, mostly re-enabling cleartext: 89,686 apps use cleartextTrafficPermitted, 88,769 (98.98%) set it true; of 565,910 apps targeting Android ≥9, 84,060 (14.85%) re-allow HTTP; in 8,935 apps the HTTP-downgraded hosts actually served HTTPS (often redirecting); top downgraded "domains" 127.0.0.1 (11,689 apps) and localhost. **Pinning via NSC: only 663 apps (0.67%)**, most common in **Finance (6%)**; 1,121 pins for 2,781 domains; pinned 483 leaf, 542 intermediate, 289 root certificates; 566 apps set backup pins but many fake ("AAAA…", empty-string hash in 12 apps); 130 set pin expiration (mean 947 days). Custom trust anchors 38,628 apps; **8,606 (8.67%) re-trust user CAs**; 10,085 use debug-overrides correctly, 41 ship MitM-proxy (Charles) roots in production. Malformed: 1,310 apps put URLs instead of hostnames (silently ignored), 210 wildcard domains (non-functional), 129 pin + permit cleartext. Copy-paste: 1,609 apps include MoPub's snippet permitting cleartext globally. WhatsApp, YouTube, Gmail use NSC to re-enable cleartext. Manual: 13/20 random and 11/20 sensitive apps sent data over HTTP, incl. credentials. **Play safeguards:** empty/insecure TrustManagers, always-true HostnameVerifiers, debug-flag WebView handlers all **accepted**; only trivial always-proceed WebView blocked; CryptoGuard: 5,202 (34.7%) vulnerable TrustManagers, 2,232 (14.8%) HostnameVerifiers, **5,511 (36.7%) vulnerable apps** — same as 2012.
- **Discussion:** "**customization is harmful**": when developers touch TLS settings, security usually drops; pinning didn't grow even after NSC made it easy (complexity isn't the only reason); Android Studio support for NSC is weak; recommend integrating CryptoGuard/LibScout into Play review.
- **Limitations:** free apps only; German crawl location (77,676 geo-blocked); one NSC per app (cannot split app vs library); static only (no runtime/reflection).
- **Relevance:** strong evidence for N1's core premise: **app security follows platform defaults and store policy, not developer initiative** — so if Android's default stack lacks X25519MLKEM768, almost no app will add it, and any NSC-style knob would be rarely and often wrongly used (G1, G12, G13: policy levers > notification). Pinning numbers (finance 6%, many leaf pins) feed G9. The target-SDK mechanism is a concrete lever N1 can recommend (e.g., a Play requirement for PQ-capable stacks).

### B06 Reaves, Scaife, Bates, Traynor, Butler 2015, Mo(bile) Money, Mo(bile) Problems: Analysis of Branchless Banking Applications in the Developing World (USENIX Security 2015; Univ. Florida)
- **Scope:** GSMA Mobile Money Tracker (Aug 2014: 246 services, 88 countries, >203 M accounts) → 46–48 Android mobile-money apps in 28 countries; Mallodroid on all (flags 24); **manual teardown of 7 apps (15%)** from Brazil, India, Indonesia, Thailand, Philippines: Airtel Money, mPAY, Oxigen Wallet, GCash, Zuum, MoneyOnMobile (MOM), mCoin. **No Bangladeshi app (bKash) appears in their list.**
- **Method:** apktool manifest + permission/exported-component report; baksmali + regex for networking/crypto/ad/ClassLoader libraries; JEB decompilation following the app lifecycle (registration → login → transfer); **Qualys SSL Server Test on each backend**; accounts obtained in India for MOM, Oxigen, Airtel → MitM verification in an emulator; ToS liability review; disclosure to all (most never replied).
- **Results:** 28 significant vulnerabilities; **6 of 7 apps fail transaction integrity** (only Zuum, Telefónica+MasterCard, OK). Broken certificate validation (empty X509TrustManager) in several; **mCoin's server cert was self-signed, expired and issued to "localhost" — app must disable validation to work** (client and server flaws coupled). Qualys grades: Airtel A- (SHA1withRSA), mPAY F (SSLv2, insecure renegotiation)/F (POODLE), Oxigen F (SSLv2, MD5), Zuum A-, GCash C (POODLE). **DIY app-layer crypto:** MOM uses no TLS at all, sends data + static key over HTTP to an "encryption proxy"; Oxigen Wallet: Blowfish key with only 17 random bits (java.util.Random), key sent in plaintext with the message; **RSA server key fetched over unauthenticated HTTP → trivially MitM-able**; GCash: static symmetric key `enc.key` shipped in every APK encrypts PIN + session ID; session ID = IMEI + time; Airtel Money: PIN encrypted with key "j7zgy1yv"+phone#+account# (inside TLS that doesn't validate certs). Access control: MOM's PINs only gate UI activities — backend APIs need just the phone number; SMS-based PIN/password reset; 4-digit PINs; logging of PINs/card numbers (READ_LOGS pre-4.1 = 20.7% of devices); prefs storing PINs.
- **Regulation insight:** **Reserve Bank of India 2008 mobile-payment guidelines (12 pages) recommend "digital-certificate based" transactions and PIN encryption on the wire → explains app-layer PIN encryption inside TLS (Airtel) and Oxigen's flawed public-key design**; vague "strong encryption" guidance may have contributed to failures; MOM, the worst app, displayed RBI authorisation. ToS: 6 of 7 put fraud liability entirely on customers.
- **Discussion:** smartphone money apps were *less* secure than the legacy USSD/SMS channels they replaced (attacks need only a laptop); recommend OS-level enforcement of sane TLS configs.
- **Limitations:** 7 apps, 5 countries, Android only, client-side only (server software unaudited).
- **Relevance:** the developing-country mobile-finance framing for N1; concrete precedent that **regulator guidance shapes app-layer crypto** (RBI → app-layer PIN encryption; Bangladesh Bank ICT Guideline v4.0 may do the same → G6 and N1's regulator recommendations); shows finance apps add RSA/static-key crypto on top of TLS — exactly the "second layer" G6 must cost quantumly (an RSA-encrypted PIN recorded today is HNDL-exposed even if TLS becomes PQ). Method template: app teardown + backend server grading + responsible disclosure.

### B07 Mickey & Yanhaona 2024, An investigation of the Online Payment and Banking System Apps in Bangladesh (arXiv 2407.07766v2, Nov 2024; BRAC University; not peer-reviewed)
- **Scope (Table I):** 17 APKs + 1 SDK: MFS wallets **bKash (1), Nagad (2), Rocket (3)**; bank apps City DRF-SCF (4), CityRemit (5), Southeast Bank (6), NexusPay (7), Islamic Wallet (8), Astha/BRAC Bank (9), IFIC Amar Bank (10), ibbl-ismart/Islami Bank (11), UniON Bank (12), ONE Bank (13), Upay (14); recharge MyGP (15); utilities DWASA (16), DESCO (17); **SSLCommerz payment SDK (AAR, 18)**. Context: Bangladesh Bank heist 2016 (US$81 M lost); MFS monthly transactions ~TK 1.29 trillion (Jan 2024).
- **Method:** OWASP MASVS (STORAGE, CRYPTO, NETWORK, PLATFORM); apktool/JADX/Androguard/MobSF; **customised AARDroid** (Amandroid + CryptoGuard; extended to APKs; code public on GitHub); emulators (Google APIs, rootAVD), smali log/exception injection to trace call graphs. Set A (not analysable: 4, 6, 9, 13, 14 — XAPK/obfuscated), Set B partial (2, 12, 16, 17), Set C full (1, 5, 8, 10, 11, 18). Only 4 apps obfuscated.
- **Scanner findings (unverified unless stated):** **bKash (1) violates CRYPTO1–4** (hard-coded keys, weak crypto config e.g. ECB/static IV/low PBE iterations, deprecated algorithms, insecure PRNG) and local-persistence rules; CityRemit (5) CRYPTO3–4; **IFIC Amar Bank (10) CRYPTO3–4 + TLS2 (broken TLS config) + TLS3 (improper certificate validation)**; **ibbl-ismart (11) CRYPTO1–2 + TLS1–3** (HTTP use, broken TLS, improper validation) + no Keystore + external storage; **SSLCommerz SDK (18): TLS4 (no pinning), CRYPTO2–4, WebView JavaScript bridge, overlay, many storage issues — the worst**; Nagad (2) and Islamic Wallet (8) WebView/URL-scheme/IPC issues; almost all allow auto-backup (DS8). Manual: some apps skip client-certificate (mutual) auth; OTP auto-read via SMS Retriever API with no device binding (registered from emulator). Vendors' frequent updates and XAPK format broke their tooling. Recommendation: publish app-signing public keys for verification.
- **Limitations:** scanner-driven, many findings unverified; no network capture, **no TLS version/cipher/key-exchange/PQ analysis**, no server-side scan; small sample; arXiv only.
- **Future work:** PoCs of the potential vulnerabilities; obfuscation/XAPK analysis; open-source scanner/bytecode parser.
- **Relevance (high, local):** the **only security study of Bangladeshi finance apps**; gives N1 the app list and evidence of app-layer crypto weaknesses (G6) and TLS-validation problems in two bank apps; leaves the whole transport/PQ question, server side and iOS open → N1 is clearly additive. Responsible-disclosure care needed (they name apps).

### B08 Yang, Huang, Fang, Zhang, Guo, Wu, Mi 2026, Okara: Detection and Attribution of TLS MitM Vulnerabilities in Android Apps with Foundation Models (arXiv 2601.22770v2; abridged in ACISP 2026; USTC, Ocean Univ. China, Monash)
- **Tools:** TMV-Hunter = foundation-model GUI agent (random / Qwen2.5-VL-32B / UI-TARS-1.5-7B; Gemini 2.5 Flash best) + **per-app VPN forwarding (WireGuard, Android VpnService allowlist, no root; TCP and UDP incl. HTTP/3)** + mitmproxy add-on running 3 tests: T1 untrusted self-signed CA, T2 trusted cert for wrong hostname, T3 pinning (attacker CA installed); retest policies. TMV-ORCA = ART Tooling Interface class-load hooks (forced via Frida for non-debuggable apps) on X509TrustManager/HostnameVerifier/WebViewClient, correlation to vulnerable flows (hostname or cert CN/SAN), LLM classifier (DeepSeek-V3) into a new taxonomy (T0–T2F, W0–W2C, H0–H2B).
- **Evaluation:** 100 top AppChina apps with manual ground truth (567 activities, 2,341 TLS flows; 69 vulnerable apps / 487 vulnerable flows); LLM agents beat random; ~50 steps sufficient; ART-TI beats API hooking (flow coverage 71.88% vs 10.77% without MitM).
- **Deployment (Apr 2025, redroid emulators on ARM cloud):** 20K Google Play (AndroZoo, latest Mar 2025) + 20K AppChina → 37,349 analysed (144.75 s/app, 8 days): **8,374 vulnerable apps (22.42%)**; AppChina 39.40% vs **Google Play 3.19%**; vulnerable flows 5.25% (AppChina 9.94%, Play 0.77%); not correlated with popularity (r_pb ≈ 0) or category. **Flows: TLS 1.3 78.98% of vulnerable flows; UDP/QUIC only 0.22% of all flows in their capture.** Manual labelling of 100 popular vulnerable apps: vulnerable flows by function — content 61.28%, telemetry 27.70%, executable code 6.19%, **authentication 4.06% (in 39% of apps)**, **financial transactions 0.75% (13% of apps)**. Longitudinal (1,720 APKs of 100 apps, 5 years): median vulnerable span 1,384 days, span ratio 92.10%, only 13% ever fixed, median fix delay 330 days, 39% reintroduced. Pinning bypass (T3) affects ~75% of apps and 98.6% of FQDNs.
- **Attribution:** 8,065 vulnerable code instances (51.28% of vulnerable apps located); H1 (always-true verifier) and T1 (empty TrustManager) dominate; W1 (ignore all SSL errors) common in AppChina, rare on Play. **Third-party libraries = 41% of vulnerable snippets, present in 48.98% of vulnerable apps, 28.90% of FQDNs**; top libs JPush, UMeng, Baidu Map SDK, Tencent Bugly, JVerification, OkGo … top-5 = 81.65% of third-party share. Default-verifier override by one SDK silently breaks "secure" delegating code.
- **Disclosure:** emailed 726 developers; **zero responses** at submission. Lessons: app stores need reliable contact channels.
- **Limitations:** GUI coverage incomplete; only MitM-exploitable validation errors; anti-instrumentation apps; native-code TLS not analysable.
- **Relevance:** newest large-scale Android TLS study → method parts reusable for N1 (per-app VPN capture incl. UDP/QUIC without root; LLM GUI agents to reach login/payment flows; attribution of flows to SDK packages for G5). The 726-emails-0-replies result is a sobering prior for N1's G13 notification experiment. Google Play apps are far better than a Chinese third-party store → app-store governance matters (cf. B05).

### B09 Jimenez-Berenguel, Campo, Moure-Garrido, Garcia-Rubio, Díaz-Sánchez, Almenares 2025, PARROT: Portable Android Reproducible traffic Observation Tool (arXiv 2509.09537; UC3M Madrid — same group as E01)
- **Tool:** one Docker container with an Android Studio emulator (Android 15/API 35, Pixel 7 profile, Google APIs, no Play Store), `-http-proxy` to mitmproxy (optional), tcpdump on all interfaces except proxy port, **SSLKEYLOGFILE** key export, Google DNS, adb automation (root, disable-verity, system CA install, final step manual), human-in-the-loop interaction, auto-labelled PCAP + key files. Public on GitHub; dataset PARROT2025_mitmproxy.
- **Review of datasets/capture systems:** only 4 public PCAP datasets with >50 apps (MAppGraph 2021 Vietnam 101 apps; NUDT 350 Chinese apps; **Mankowski et al. 2023 (B01) 90 apps**; Jiang 2023 53); capture systems mostly ad hoc (MIRAGE, NetLog, PCAPdroid VPN — PCAPdroid non-root alters L3/L4 headers and can't decrypt QUIC).
- **Dataset:** 80 of MAppGraph's 101 Vietnamese apps (APKs from APKMirror/APKPure/Uptodown), 4 captures × ~5 min each = 320 captures, >25 h, Dec 2024–Jul 2025, **app first-launch behaviour**, mitmproxy on. Background calibration: clean emulator → TLS 1.3 489 packets, DoT 19, DNS 14, HTTP 4 (connectivity checks).
- **Results (50 common apps, 2021 vs 2025):** UDP 45.4% vs 11.4% of traffic; **QUIC 45.3% of packets (vs 10.8%)**; TLS 1.3 52.0% of all traffic, TLS 1.2 2.5%; **within TCP-encrypted traffic TLS 1.3 = 90.0% (vs 6.7% in 2021)**, TLS 1.2 9.6% (vs 77.7%), legacy SSL 0 (vs 14.2%); DNS: DoT 81.1% (vs Do53 91.0% in 2021). Without mitmproxy all 50 apps use QUIC (vs 29–30 in 2021); with mitmproxy only 35 do. Packet rates 4,019 vs 21,288 ppm (their captures = launch only).
- **Limitations (stated):** mitmproxy breaks pinned apps — **of 80 apps only Instagram worked fully** (Chess offline); most froze, closed, or failed login → traffic mostly launch-time; QUIC suppressed under interception; DoH/Private-DNS failures; emulator x86_64, Spain vantage; app versions from third-party mirrors.
- **Future work:** more apps/categories; impact of capture environment on patterns.
- **Relevance:** (i) **source of the "mobile traffic ≈52% TLS 1.3 + 45% QUIC" figure** quoted by E01 and by N1's E8 — note it is a *packet share during first launch in an emulator in Spain with mitmproxy*, not a population statistic; (ii) a ready, reproducible capture rig with key logging for N1's lab (G1) — but its mitmproxy mode would distort exactly what N1 measures (it terminates TLS at the proxy, so the negotiated group is the proxy's, not the server's) → N1 must use the **non-interception mode** for key-exchange measurements; (iii) QUIC must be captured and parsed (half the traffic).

### C01 Paquin, Stebila, Tamvada 2020, Benchmarking Post-Quantum Cryptography in TLS (PQCrypto 2020; Microsoft Research, U. Waterloo)
- **Method:** Linux network namespaces + veth + **netem** to control RTT (5.6, 31.2, 78.7, 195.7 ms) and independent packet loss 0–20%; OQS-OpenSSL 1.1.1 nginx server, modified `s_timer` client measuring handshake-only time (4,500 samples per KEX point, 6,000 per signature point; 40 client processes, Azure D64s). Plus real Internet data-centre experiments (Azure East US 2 → 6.2/30.9/70.3/198.7 ms RTT; page sizes 1 kB–1 MB, Apache Bench). Code/data: github.com/xvzcf/pq-tls-benchmark.
- **Algorithms:** KEX hybrids ecdh-p256 + {SIKE p434 (pk 330 B, ~60 ms compute), Kyber512-90s (pk 800/ct 736 B, ~0.01 ms), FrodoKEM-640-AES (9,616/9,720 B)}; signatures ECDSA-P256, Dilithium2 (pk 1,184, sig 2,044), qTESLA-p-I, Picnic-L1-FS (sig 34,036 B).
- **Results:** median at ≤1% loss → computation dominates (SIKE floor); **as loss rises above 3–5%, big-message schemes degrade**: Frodo hybrid needs **16 client packets vs 5 for ECDH and 6 for Kyber hybrid** → at 5% loss P(≥1 loss) = 1−0.95^16 ≈ 58%; 95th percentile hides compute differences until ~15% loss for Frodo. Signatures similar; Picnic degrades fast; Dilithium2 ≈ ECDSA at low loss. Internet: overhead shrinks with page size and RTT (P-256 3.12× faster than SIKE for 1 kB at 6.2 ms, but only 1.07×/1.03× at 198.7 ms). Mozilla telemetry: 95% of desktop samples <4.3% packet loss.
- **Design notes:** hybrid = concatenated key shares and secrets; only IND-CCA KEMs used (whether IND-CPA suffices for ephemeral TLS is open); PQ-only authentication argued sufficient because authentication need only hold at connection time (no hybrid certs needed in TLS 1.3).
- **Future work:** more algorithms/levels; NetMirage/Mininet multi-path; chain sizes and mixed-algorithm chains; server throughput; SSH/IPsec/WireGuard.
- **Relevance:** the template for N1's G11/G10 thinking: **cost of PQ appears in the lossy tail, not the median** — the kind of mobile network A01 did not test. ML-KEM-768 hybrid (~1.2 KB client share) adds ~1 packet vs X25519, so with Kyber-class KEMs the effect is small; the big risk is PQ certificates (later). Use netem-style emulation of Bangladeshi operator loss/RTT in the lab.

### C02 Sikeridis, Kampanakis, Devetsikiotis 2020, Post-Quantum Authentication in TLS 1.3: A Performance Study (NDSS 2020; UNM + Cisco)
- **Q:** cost of PQ certificates/signatures (Round-2 candidates) in TLS 1.3 handshakes and server throughput; X25519 key exchange fixed.
- **Method:** OQS-OpenSSL 1.1.1c; client in N. Carolina, GCP servers (N. Virginia, Oregon, Zurich, São Paulo, Sydney, Singapore; +11 to +225 ms RTT); chains with 1 or 2 intermediate CAs (77% of real chains); 1,000 handshakes per point; 3,000 handshakes over a day for global percentiles; nginx + Siege load test (20–1,000 clients). Unoptimised implementations (no AVX2).
- **Sizes (Table III, 1 ICA chain / CertificateVerify):** RSA-3072 1.63 KB/0.38; ECDSA-384 1.34/0.05; **Dilithium II 6.90 KB/2.04**; Falcon-512 3.54/0.69; MQDSS 42.24/20.85; Picnic 66.20/30.03; SPHINCS+-128f 34.46/16.98; Rainbow Ia 116.86 KB (client rejected: "excessive message size"); Dilithium IV 10.70/3.37; Falcon-1024 6.56/1.33.
- **Results:** Dilithium II and Falcon-512 add <5 ms certificate transfer locally (no extra RTT); MQDSS/Picnic/SPHINCS+ +35–55 ms and **extra round trips once data exceed TCP initcwnd** (can exceed 0.5 s at distance). Global 50th/95th percentile over RSA-3072 (131.5/227.3 ms): Dilithium II +6.6%/+2.3%, Falcon-512 +8.1%/+3.5%, **Dilithium IV +110%/+98% (extra RTT; ~+145 ms median)**, Falcon-1024 +16%/+6%, Falcon+Dilithium mixed chain +7%/+0.5%. Server: Dilithium II gives ~25% more transactions/s than RSA-3072 at saturation (fast signing); Falcon saturates early (slow signing without FPU). Mixed chain (Falcon root/ICA + Dilithium IV leaf) cuts handshake 25–33% vs single schemes. Extrapolated full TCP+TLS PQ handshake ≈ 122–135 ms vs Firefox median 111 ms. "Combining with KEM results, total slowdown ~10–25%".
- **Discussion:** long-lived tunnels (VPN) tolerate slow auth; short web connections don't (70 requests/page). OCSP/SCT add 3+ signatures → could push Dilithium over initcwnd. Proposals: ICA suppression/caching, certificate dictionaries, batch signing, Falcon message recovery, KEM-based auth (KEMTLS-like, +1 RTT), out-of-band cert retrieval.
- **Future work:** PQ auth in VPN, QUIC, DTLS; combined PQ KEM + signatures; lossy networks; SCT/OCSP; hybrid certificates.
- **Relevance:** grounds N1's G9/O4 (when PQ certificates arrive, sizes can trigger extra RTTs on mobile and break pinning/size limits); also confirms the key-exchange-first logic (authentication can't be attacked retroactively — HNDL applies to key exchange only; impersonation needs a live CRQC).

### C03 Gómez-Cambronero, Munteanu, González-Tablas 2026, Layered Performance Analysis of TLS 1.3 Handshakes: Classical, Hybrid, and Pure PQ Key Exchange (SPIQE @ EuroS&P 2026; arXiv 2603.11006v2; Telefónica, Keysight, UC3M)
- **Method:** 3 VMs on local network: Keysight CyPerf client (native ML-KEM) → nginx 1.27.3 + OpenSSL 3.4.0 + liboqs 0.12 + oqs-provider 0.8 (RSA-2048 cert) → CyPerf backend; 100 TPS for 5 min (30K requests per test, >30 tests, ~1 M requests); backend body direct/4 KB/40 KB; pcaps + SSLKEYLOGFILE; public `pcap_layer_analysis.py` splits each connection into 5 layers: TCP (SYN→SYN-ACK), TCP→TLS (SYN-ACK→ClientHello = client key generation + ClientHello build), TLS (ClientHello→Finished), TLS→App, App. Effect size Glass's Δ vs X25519 SD. Groups: x25519, x25519_MLKEM512, x25519_MLKEM768, MLKEM512, MLKEM1024. Full handshakes only (no resumption/0-RTT).
- **Results:** TCP layer unchanged at median (0.36–0.40 ms). **Client ClientHello construction 0.294 → 1.73–1.90 ms (~6×, Δ ≈ 7.7)** — the only clearly significant cost. TLS exchange "algorithm-neutral": 5.55 (x25519) vs 6.50 ms (x25519MLKEM768), Δ ≤ 0.33. TLS→App +0.4 ms (Δ ~1, small absolute). App unchanged. **E2E median 16.54 ms (x25519) → 19.63 ms (x25519MLKEM768, +18.7%), 20.26 (hybrid-512, +22.5%), 18.92/19.16 (pure ML-KEM)**; absolute +2.4–3.7 ms, fixed per connection, diluted by payload (40 KB: +12%). COS (crypto share of E2E) 6–14%. **Client CPU ~doubles (3.72% → 8.71%)**, server +5.8% relative. key_share sizes: x25519 32 B, hybrid-512 832 B, **hybrid-768 1,216 B**, MLKEM512 800 B, MLKEM1024 1,568 B; traffic 5.18 → 6.14 Mb/s.
- **Insight:** the cost lands on the **client** (keygen + decaps); suggests precomputing ephemeral key-share pools off the critical path. Warns that TLS-intercepting middleboxes (both client and server roles) will feel the largest impact.
- **Limitations:** virtualised LAN (sub-ms RTT makes compute visible), single node, 100 TPS only, software capture, RSA certs only; AI-assisted writing disclosed.
- **Future work:** real networks with commercial load balancers and MitM inspection devices; >100 TPS stress; PQ signatures; more groups; per-primitive profiling; native OpenSSL 3.5 stacks.
- **Relevance:** explains why A01 saw 0 ms median over the Internet while labs see +15–20%: the overhead is a ~1.5–3.5 ms client-side compute cost that disappears in 30+ ms RTTs. For N1 G11: on **low-end Android phones** (ARM, no AVX2) the client keygen cost and CPU doubling could matter for battery and slow devices — a gap no paper has measured on Bangladeshi-typical handsets.

### C04 Kempf, Gauder, Jaeger, Zirngibl, Carle 2024, A Quantum of QUIC: Dissecting Cryptography with Post-Quantum Insights (IFIP Networking 2024; TU Munich)
- **Method:** bare-metal testbed (AMD EPYC, 10 GbE, RTT <0.1 ms), extended QUIC Interop Runner; LSQUIC, quiche, MsQuic vs nginx/curl TCP+TLS; 8 GiB downloads ×25; NOOP AEAD cipher patched into BoringSSL/OpenSSL (published) to isolate symmetric crypto; OQS BoringSSL for PQ handshakes; TTFB = ClientHello → client can send HTTP/3 request.
- **Symmetric findings:** AES-128 ≈ AES-256 throughput (hardware AES); ChaCha20 9–16% slower on AES-NI servers (but better without acceleration — the phone case); removing packet protection +10–20% goodput; AES header protection virtually free; larger MTU (3000 B) +~40% goodput.
- **PQ KEM (Table II, LSQUIC/quiche TTFB ms; packets client/server):** X25519 3.91/3.57 (3/3); **Kyber512 4.08/3.39 (3/3)**; Kyber768 4.23/3.78 (4/3–4/5); Kyber1024 4.43/3.81 (4/4–4/5); BIKE and HQC slower (BIKE-L5 22.27 ms); hybrids with P-256 ≈ PQ KEM cost; P-384/P-521 hybrids add their (slow) ECDH. **Major bottleneck = bytes, not compute; Kyber barely moves TTFB.**
- **PQ signatures (Table III):** Falcon-512 cert 1,793 B, TTFB ≈ +0.6 ms vs RSA-1024; Dilithium3 cert 5,508 B (4.26/2.14 ms, 4/10 packets); Dilithium5 7,449 B; SPHINCS+ certs 8–50 KB → hundreds of ms, up to 92 server packets; **LSQUIC failed with >30 KB certificates (mini-connection 64-packet limit)**; **QUIC anti-amplification (server may send ≤3× bytes received before address validation) → big PQ certificates force a Retry/extra RTT** unless ClientHello is padded.
- **Relevance:** QUIC carries ~45% of mobile traffic (B09), and PQ key exchange in QUIC is cheap (Kyber); the risk is again PQ certificates (anti-amplification, implementation limits) → G9/O4. Also confirms AES-256 costs nothing extra on servers (relevant to M4/G15: there is no performance excuse for AES-128) while ChaCha20 suits phones without AES hardware.

### C05 Hoque & Aydeger 2026, Energy-Aware System-Level Evaluation of PQ TLS on Embedded User Equipment over a Disaggregated 5G Network (IEEE LCN 2026; arXiv 2607.03988; Florida Tech)
- **Testbed:** two Raspberry Pi 5 (8 GB) as UEs (client and server) attached via UERANSIM (emulated gNB, **no over-the-air radio**) to Open5GS core (GTP-U/UPF path); BoringSSL + liboqs; PMIC on-board power telemetry (±5–10%, 100 ms sampling); concurrency C ∈ {1, 4, 10, 20, 40} client UEs × 50 handshakes; 16 KEM×signature combos: KEM {P-256, X25519, ML-KEM-512, HQC} × signature {P-256 ECDSA, ML-DSA-44, Falcon-512, SLH-DSA-SHA2-128f}.
- **Results (C=1):** classical P-256+P-256 106 ms / 176 mJ per conn; X25519+P-256 110 ms; **ML-KEM-512+P-256 106 ms / 151 mJ** (KEM change ≈ no cost); ML-KEM+ML-DSA 108 ms / 180 mJ; ML-KEM+Falcon 104 ms / 143 mJ; any+SLH-DSA ~195–205 ms / 213–250 mJ (≈2× latency, up to 2× energy); HQC adds ~30 ms. At C=40: lattice ~1,260–1,600 ms; SLH-DSA ~4,500–4,800 ms with incomplete handshakes (1,315/2,000). RTT 4.7–18 ms independent of scheme → **CPU-bound, not network-bound**; energy ∝ latency; client peak power up to 7.5–8 W; temperatures 60–70 °C (no throttling); memory ~6 MB.
- **Conclusions:** signature choice >> KEM choice; lattice schemes ≈ classical; hash-based signatures hit a "computational wall".
- **Limitations:** Pi 5 is not a phone (no mobile SoC power management, no radio); emulated RAN; PMIC accuracy; two repeats; key-exchange ML-KEM-512 not the deployed X25519MLKEM768.
- **Future work:** hardware acceleration, broader devices, over-the-air effects, dynamic network conditions, external power analysers.
- **Relevance:** the nearest thing to a "phone energy" measurement for PQ key exchange: switching the KEM to ML-KEM adds ~nothing in latency/energy on an ARM device — supporting N1's expectation that **the defence is cheap for clients**; but true phone battery cost on real cellular radios remains unmeasured (G11 gap).

### C06 Chou & Cao 2026, Network Impact of Post-Quantum Certificate Chain sizes on Time to First Byte in TLS Deployments (arXiv 2604.24869; UIUC + NCSA)
- **Method:** two AWS EC2 Ohio servers, OpenSSL s_server (+OQS in Docker), tc netem RTT 0–200 ms; certificate sizes emulated by **padding certificates with non-critical extensions** (ECDSA padded to match ML-DSA-44/SLH-DSA-192s/MTC sizes); 100 runs per point; chains 0–2 intermediates; 4–80 KB sweep (step 2 KB). Real data: **Zeek logs from NCSA (US HPC centre) network, 24 h (14 Apr 2026) + 16-month trend**, CDN vs non-CDN by ASN.
- **Results:** TTFB jumps by one RTT when the chain crosses **~10 KB and ~40 KB** (TCP initial window 14 KB / slow start); ML-DSA chains (leaf 3.9 KB + int 8.0 KB) fit in one flight like ECDSA; SLH-DSA (16.6 + 32.1 KB) adds a full RTT (+50% TTFB). OQS stack itself added ~50 ms vs plain OpenSSL (implementation, not size). MTC (Merkle Tree Certificates, ~0.7–0.9 KB proof) lets chains be ~2–3× bigger before a penalty; CDN chain trimming ~1.3–1.67×. **Session resumption (NCSA): CDN 80.30% of all TLS connections (94.16% of TLS 1.3), non-CDN 35.44% (46.09%); TLS 1.3 share CDN 84.74% vs non-CDN 75.73%.**
- **Limitations:** padded certificates are not real PQ signatures (no verify cost); MTC/CDN optimisations only approximated; no loss/failures; ASN classification coarse; resumption measured at a research network, not mobile.
- **Future work:** fragmentation/loss; real CDN experiments.
- **Relevance:** (i) quantifies when PQ certificates will add an RTT (G9/O4; mobile RTTs make that RTT expensive); (ii) **resumption is the majority mode on CDNs (80–94%)** — so the resumption mode matters for HNDL: `psk_dhe_ke` resumptions run a fresh (EC)DHE/hybrid exchange, `psk_ke` resumptions inherit the original handshake's key → N1's M1(c)/G15 resumption-mode measurement is not a corner case.

### D01 Bindel, Brendel, Fischlin, Goncalves, Stebila 2019, Hybrid Key Encapsulation Mechanisms and Authenticated Key Exchange (PQCrypto 2019; ePrint 2018/903; TU Darmstadt, McMaster, Waterloo)
- **Type:** theory/provable security. First formal treatment of hybrid KEMs and hybrid AKE against adversaries whose quantum power changes over time.
- **Two-stage adversary notions (XyZ):** CcC classical; **CcQ "future-quantum" = classical while interacting, quantum later — exactly the harvest-now-decrypt-later attacker**; QcQ post-quantum (quantum locally, classical oracle access); QqQ fully quantum. Strict hierarchy (Props. 1–5): e.g., RSA-OAEP KEM is CcC-secure but not CcQ (Shor later recovers keys).
- **Combiners (standard-model proofs, robust if one component is secure):** XtM XOR-then-MAC (k = k1⊕k2 plus a one-time MAC over (c1,c2); first KEM combiner proven against fully quantum QqQ; plain XOR is *not* IND-CCA robust — mix-and-match attack); dualPRF k = PRF(dPRF(k1,k2), c1‖c2) (models concatenate-then-KDF as in TLS 1.3 hybrid drafts); nested N (Schanck–Stebila key schedule). Including ciphertexts/transcript in the derivation blocks mix-and-match.
- **Hybrid AKE (SigMA compiler, Theorem 5):** KEM (IND-CPA) + signatures + MAC + KDF → BR-secure with forward secrecy. Key result: **for security against future-quantum (CcQ/HNDL) adversaries it suffices that the KEM is quantum-resistant (Q-ind-cpa) and the KDF ≥ CcQ — signatures and MACs may remain classical**, because authentication only has to hold while the attacker is still classical; full QcQ security needs every component PQ. The "weakest primitive" intuition is wrong for partially quantum attackers.
- **Open problem:** fully quantum (QqQ) AKE.
- **Relevance:** the formal basis for (i) prioritising key exchange over certificates (why N1 measures key_share, and why A01/A02/A03 finding 0% PQ certificates is not a confidentiality failure today); (ii) RQ-M1c: in a hybrid, breaking or reusing the classical half (X25519 key reuse) does not expose the session if the ML-KEM half is fresh and secure — robustness of the combiner; (iii) the CcQ notion gives N1 precise language for "HNDL adversary".

### D02 Barbosa, Connolly, Duarte, Kaiser, Schwabe, Varner, Westerbaan 2024, X-Wing: The Hybrid KEM You've Been Looking For (IACR Communications in Cryptology 1(1); Porto/INESC, MPI-SP, Radboud, Rosenpass, SandboxAQ, Cloudflare)
- **Construction:** concrete hybrid KEM X25519 + ML-KEM-768 + SHA3-256: k = SHA3-256("\.//^\" ‖ k_MLKEM ‖ k_X25519 ‖ ct_X25519 ‖ pk_X25519). Sizes: public key 1,216 B (1,184 + 32), ciphertext 1,120 B (1,088 + 32), private key 2,464 B, shared key 32 B. Generalised as the "QSF" framework (nominal group + KEM).
- **Security:** (1) classical IND-CCA from Strong Diffie–Hellman in the X25519 nominal group (ROM), even if ML-KEM is broken, using a new property **C2PRI (ciphertext second-preimage resistance)** that ML-KEM-768 has (from its FO transform with explicit rejection) — so the big ML-KEM ciphertext can be left out of the KDF; (2) post-quantum IND-CCA from ML-KEM-768 IND-CCA + SHA3-256 as PRF (standard model). "Secure if either X25519 or ML-KEM-768 is secure."
- **Context noted by the authors:** generic KDF(k1‖k2) is not robustly IND-CCA (Giacon–Heuer–Poettering mix-and-match attack); TLS's X25519Kyber768Draft00 relies on the TLS transcript hash for this instead — two different hybrids with one name (HPKE vs TLS) is "undesirable". ML-KEM-768 chosen over 512 to hedge cryptanalysis.
- **Benchmarks (i7-11700K AVX2):** keygen ~70.9K cycles, encaps ~116.9K, decaps ~139.4K; omitting ML-KEM ct from hashing saves 8–9%.
- **Relevance:** the defence N1 measures (X25519MLKEM768 in TLS) is the TLS-transcript variant of this design; the paper explains why the hybrid stays confidential if X25519 falls to Shor — the formal statement behind M3's "hybrid defence" demo and RQ-M1c. Also a good source for exact key-share sizes used in G11 cost tables.

### D03 Schwabe, Stebila, Wiggers 2020, Post-Quantum TLS Without Handshake Signatures — KEMTLS (ACM CCS 2020; full version Jan 2022; MPI-SP/Radboud, Waterloo)
- **Idea:** replace the server's handshake signature (CertificateVerify) with KEM-based implicit authentication: client sends ephemeral KEM pk; server returns ct_e + certificate holding a long-term KEM pk; client encapsulates to it (ct_s); keys from ss_e‖ss_s; explicit key confirmation one flight later. Same round trips until the client can send application data as TLS 1.3 (client speaks first, as in HTTPS); server can no longer send data in its first flight; early client data is implicitly (not explicitly) authenticated and downgrade resilience / forward secrecy are slightly weaker until the handshake completes (full once complete). Proven in the multi-stage AKE model (Dowling–Fischlin–Günther–Stebila style), standard model, authentication from IND-CCA of the long-term KEM. Implemented in Rustls (Rustls initially rejected certificates >64 KB).
- **Results (NIST round 2/3 level-1 schemes, netem 31 ms/1 Gbps and 196 ms/10 Mbps):** size-optimised KEMTLS needs 1,853 B of public-key objects vs 3,035 B for the best signed TLS 1.3 (−39%) incl. intermediate CA (vs 1,376 B for RSA+X25519 today); Kyber-Dilithium: 8,344 vs 10,036 B (round 3: 9,288 vs 11,452 B; excl. int. CA 5,556 vs 7,720). **Server CPU for asymmetric crypto −75% (KDDD→KKDD) to −90% (NFFF→NNFF)**; client −16%. Handshake time similar or slightly faster for lattice schemes; extra RTTs when Rainbow/GeMSS public keys are sent (initcwnd 10 MSS). Smaller trusted code base: no online signing on servers (signatures only at CAs) → fewer side-channel targets.
- **Caveats (later facts):** SIKE and Rainbow, used in several of its instantiations, were broken classically in 2022; KEMTLS is not standardised for the Web PKI; X25519MLKEM768 + classical certificates is what got deployed.
- **Future work (stated):** cases where clients know server keys in advance (KEMTLS-PDK); more primitives/levels.
- **Relevance:** alternative path for the PQ authentication step (G9/O4); particularly attractive for **mobile apps with hard-coded backends** (B01 recommends KEMTLS-PDK; pinning already embeds server keys in apps) — a design idea N1 can recommend to finance apps, and a reason pinning data (G9) matters.

### D04 NIST 2024, FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) (13 Aug 2024)
- **What it standardises:** ML-KEM (from CRYSTALS-Kyber round 3), security from Module-LWE; built as K-PKE (not to be used alone) + Fujisaki–Okamoto transform → IND-CCA2 KEM; NTT for fast polynomial multiplication; n = 256, q = 3,329.
- **Parameter sets (Table 2/3):** ML-KEM-512 (k=2, η1=3, η2=2, du=10, dv=4; category 1; RBG ≥128 bit): ek 800 B, dk 1,632 B, ct 768 B; **ML-KEM-768 (k=3, η1=2, η2=2, du=10, dv=4; category 3; RBG ≥192 bit): ek 1,184 B, dk 2,400 B, ct 1,088 B**; ML-KEM-1024 (k=4, η1=2, η2=2, du=11, dv=5; category 5; RBG ≥256): ek 1,568 B, dk 3,168 B, ct 1,568 B; shared secret always 32 B. Decapsulation failure rates 2^−138.8 / 2^−164.8 / 2^−174.8. **NIST recommends ML-KEM-768 as default.** Security categories defined relative to breaking AES-128/192/256 by key search.
- **Implementation rules:** approved RBG; input checking for Encaps/Decaps; destroy intermediates; no floating point; internal derandomised functions only for testing; "a combined KEM that includes ML-KEM as a component might not meet IND-CCA2" → see SP 800-227 for combiners (cf. D01/D02).
- **Differences from Kyber:** fixed 256-bit shared secret; FO variant no longer hashes ciphertext into the key; no pre-hash of encapsulation randomness; explicit input checks; domain separation by k added after the draft.
- **Relevance:** the exact primitive behind X25519MLKEM768 (0x11EC) that N1 counts; sizes (ek 1,184 + 32 = 1,216 B client share; ct 1,088 + 32 = 1,120 B server share) explain A01's +1,176/+1,088 byte medians and C03's 1,216-B key_share; parameters (n, q, k, η, du, dv) are what a **baby ML-KEM** for Toy-TLS (M3) scales down (e.g., small n, q) — the toy must keep the FO structure to demonstrate the defence faithfully.

### D05 Gupta & Rana 2026, Transcript-Bound Combiners for Downgrade-Resilient Hybrid PQ Key Establishment: Definition, Proof, and Embedded-Device Cost (arXiv 2609.21273; Maharishi Markandeshwar Univ., India)
- **Problem:** a hybrid KEM secures the key once a suite is agreed, but not the **negotiation**: if a hybrid KEM (e.g., X-Wing, designed as a drop-in with no negotiation) is used in a bespoke handshake without transcript authentication, an active MitM can delete the PQ option from the advertised lists → both peers silently complete classical X25519 (Logjam-style). TLS 1.3 (Finished MAC over transcript), IKEv2 and EDHOC already prevent this; the risk is custom/minimal protocols.
- **Construction:** K = KDF(label ‖ K_pq ‖ K_ec ‖ H(τ)), confirmation tag = MAC(K, τ) (SHAKE-256 KDF, SHA3-256 hash, HMAC-SHA3-256); τ = advertised lists, selected suite, keys and ciphertexts as each party saw them.
- **Results:** plain combiner downgraded with probability 1 (2,000/2,000 trials); bound combiner aborts every attempt; downgrade advantage ≤ q_H/2^256 + MAC forgery; strongest-link IND-CCA bound ≤ min(Adv_pq, Adv_ec) + q_H/2^γ (empirical slope ratio 0.97, R² = 0.98). Cost model from published Cortex-M4 numbers (pqm4, Lenngren X25519): X25519-only 114 B / 2.50 Mcycles; ML-KEM-768-only 2,322 B / 1.46 Mcycles; hybrid 2,386 B / 3.96 Mcycles; bound +0.47 Mcycles (+11.8% compute) but **+1.5% of radio-inclusive energy** (radio 86% of 13.28 mJ); ~80 hybrid handshakes/day on a 5-year coin cell vs 675 for X25519 only. Two latency regimes: wide-area network-bound (~208 ms), edge compute-bound (~36 ms).
- **Limitations (stated):** device numbers are a composed model, not a measured board; classical ROM proof (QROM sketched); assumes entity authentication elsewhere; DoS (forced aborts) not prevented.
- **Relevance:** reminds N1 that "PQ-capable on both sides" ≠ "PQ negotiated": negotiation and **fallback paths** matter. In TLS 1.3 a stripped key share is detected, but a **client that retries without PQ after a failure** (middlebox breakage, large ClientHello) or a server preferring X25519 still yields classical sessions — N1's HRR/fallback columns (G10) capture exactly this. Also shows radio bytes dominate PQ energy on constrained links (relevant to phones on weak cellular links, G11).

### E01 Blanco-Romero, Almenares Mendoza, García Rubio, Campo, Díaz Sánchez 2026, On the Practical Feasibility of Harvest-Now, Decrypt-Later Attacks (arXiv 2603.01091; UC3M Madrid)
- **Approach:** HN-DL as an economic problem: storage cost (overhead ratio α) × quantum work (E keys to break per session × T_q time per key). **Open-source loopback testbed** (patched OpenSSL 3.6.0, OpenSSH 9.9p2, tshark, Python): source patches log the ephemeral private keys a CRQC would recover; derivation modules rebuild all secrets from the PCAP + "quantum output" and decrypt with tshark; verified against SSLKEYLOGFILE. Attacks validated end-to-end for TLS 1.2 RSA, TLS 1.3 1-RTT, TLS 1.3 0-RTT resumption chain, QUIC (Initial keys from DCID), SSH curve25519.
- **Taxonomy (Table 1):** TLS 1.2 RSA — no FS, one key opens **all sessions per certificate key**; TLS 1.2 (EC)DHE, TLS 1.3 1-RTT, PSK-DHE, QUIC, SSH — per-session quantum break; **TLS 1.3 KeyUpdate — deterministic HKDF chain, breaking the first ECDHE exposes all epochs (E = 1)**; **TLS 1.3 0-RTT / pure-PSK resumption — one ECDHE break cascades through the whole PSK chain** (demonstrated). QUIC's packet protection adds nothing.
- **Storage model:** S(P) = H + C + P + nω + n_data·ℓ; handshake H ≈ 1,620 B (TLS 1.2 RSA), 2,160 (TLS 1.3), 2,400 (QUIC), ≥5,100 (SSH); ω = 22 B/record TLS 1.3; α∞ < 1.003 (TCP), 1.02 (QUIC); small sessions (<1 KB) α 3.5–8.5× → **small credential/API sessions are the costliest per byte yet highest value**; record lengths are cleartext → triage by size. ITU 8.8 ZB/yr traffic (~10^13 sessions/day). **Annual storage at $12.16/TB-yr (AWS fully loaded): 1% harvest 88 EB/yr ≈ $1.1 B; 10% $11 B; 100% $107 B**; LTO-9 tape media $5.25/TB; Monte Carlo (10,000 draws; payload log-N median 2 MB): 1% harvest O(10^9) USD/yr, 10-year cumulative O(10^10–10^11). Data shelf lives: health 25–50 yr, finance audits >7 yr. Q-Day expert window 2030–2040 (~50% within 15 yr). Cited: mobile traffic **52% TLS 1.3, 45% QUIC** (from B09 PARROT).
- **Defences (server-side):** ECH degrades SNI triage (needs CDN coalescence); disable TLS 1.2 RSA and 0-RTT; short ticket lifetimes (300 s vs 86,400 s), **enforce psk_dhe_ke**, rotate STEKs; **rekeying multiplies Shor runs**: E_eff(L,R) = ⌈min(L,P)/R⌉ (useless for small prefix targets like 4-KB credentials); SSH RekeyLimit 64 KB → E = 37 at 5 MB with 2.1% storage penalty; TLS 1.3/QUIC lack fresh-DH rekeying (Extended Key Update drafts pending) → PSK-DHE reconnection is the only way; larger groups (P-384) raise T_q; padding penalises defenders (self-harming).
- **Cited quantum cost:** 256-bit ECDLP ~10^11 Toffoli, ~2,330 logical qubits (Roetteler 2017) → T_q hours–days; with T_q = 1 h, E = 37 turns 1 h into ~2 days.
- **Stated limitations / open problems:** loopback only (no MTU/loss); interception cost excluded; **"the economics of partial PQC deployment also deserve study: because TLS and SSH negotiate key exchange parameters in cleartext, an adversary can discard quantum-resistant sessions and concentrate harvesting on the shrinking classical remainder."** No real servers measured; key-share reuse across connections not modelled.
- **Relevance (central to M1/M2):** gives N1 the E × T_q cost language; N1's "sessions per Shor run" is the **inverse of E**: ephemeral-key reuse, RSA key transport, psk_ke resumption and 0-RTT make one run open many sessions (amortisation factor > 1). Their explicit open problem (cleartext group → triage of classical remainder) is exactly what N1 measures in the wild (which app connections remain classical, i.e., harvest-worthy). Also: Bangladesh's MFS/bank API calls are small sessions — high α, high value.

### E02 Springall, Durumeric, Halderman 2016, Measuring the Security Harm of TLS Crypto Shortcuts (IMC 2016; U. Michigan / ICSI)
- **Q:** How much do performance shortcuts (DHE/ECDHE ephemeral reuse, session-ID caches, session tickets/STEKs) shrink real forward secrecy? Introduces the **"vulnerability window"** (span during which stealing server state decrypts an observed FS connection) and **"service groups"** (domains sharing a secret).
- **Method/data:** 9-week ZMap-based scans (2 Mar–4 May 2016) of Alexa Top 1M from U. Michigan, modified ZMap for ID/ticket resumption; browser-trusted (NSS) only; also Censys DHE-only scans. Churn: 1,527,644 unique domains seen; only 539,546 stayed whole 9 weeks; 291,643 always-listed with trusted cert = base. 10 quick connections per domain (Table 1): DHE support 252,340 → ≥2× same value 18,113 (7.2%), all-same 12,461; ECDHE support 390,120 → ≥2× same 60,370 (15.5%), all-same 41,683; tickets 354,697 issued → ≥2× same STEK ID 353,124, all-same 334,404.
- **Session IDs:** 97% set ID, 83% resumed after 1 s; 82% honour ≤1 h, 61% <5 min; 0.8% (2,845) ≥24 h (86% Google); defaults Apache 5 min, Nginx off/5 min, IIS 10 h.
- **Tickets:** 79% issue, 76% resume after 1 s; 67% accept <5 min, 76% ≤1 h; 54,522 Cloudflare domains 18 h; Google 8,535 domains 28 h hint; two domains 90-day hints; Apache/Nginx default 3 min (ticket lifetime ≠ STEK lifetime).
- **STEK lifetime (key result):** STEK identifier (16-byte per RFC 5077; mbedTLS 4-byte; SChannel DPAPI GUID) tracked first/last seen. Of 291,643: 23% never issue tickets; 41% new STEK daily; **22% same STEK ≥7 days; 10% ≥30 days**; yahoo, taobao, pinterest, yandex.ru, imgur, tmall 63 days (whole study), qq 56, netflix 54; 12 Top-100 sites ≥30 days. Cause: Apache ≥2.4.0/Nginx ≥1.5.7 read 48-byte key file from disk (changed only by admin + restart) or generate once per process. Fastly used one STEK all 9 weeks (gov.uk, foursquare, aclu); **Jack Henry & Associates: 79 bank/credit-union domains on one STEK for 59 days, then another shared one** (finance relevance).
- **Ephemeral reuse:** DHE (57% support DHE-only): 4.4% reuse in 10 scans; 1.3% ≥1 day, 1.2% ≥7 days, 0.52% ≥30 days (commsec.com.au brokerage 36 days). ECDHE (80% complete): **14.4% reuse in 10 scans; 3.4% ≥1 day, 3.0% ≥7 days, 1.4% ≥30 days**; whatsapp.com 62 d, netflix 59, **paytm.com 27 d**, betterment.com 62, mint.com 62.
- **Sharing:** session-cache groups 212,491 (86% singletons), largest Cloudflare 30,163 domains; STEK groups 170,634 (83% singletons), Cloudflare 62,176, Google 8,973, Automattic 4,182, TMall, Shopify, GoDaddy, Amazon; DH groups 421,492 (99% singletons), largest SquareSpace 1,627; one ECDHE value seen 1,790× across 179 domains (Jimdo on EC2); one DHE value across 137 domains (Hostway). 49% of domains share a cache with another popular domain.
- **Combined exposure:** 90.2% of trusted Top-1M use FS with modern browsers, yet **38% (110,788) have max window >24 h, 22% >7 days, 10% >30 days**. "Forward secrecy is a gradient, not binary." Google STEK rotated every 14 h, accepted 28 h → 2 keys per 28 h decrypt all Google ticket connections, including SMTP/IMAPS/POP3S (9.1% of Top-1M MX → Google). Yandex one STEK since ≥10 Jan 2016.
- **Recommendations:** disable resumption/reuse for max security; else HTTP/2 (one connection), rotate STEKs frequently, region-specific STEKs, short cache lifetimes, keep secrets in memory only. Critique of TLS 1.3 draft 15: **7-day PSK maximum set "without discussion"**.
- **Limitations:** lower bounds only (cannot see secure erasure); classical attacker who steals server state (not quantum); browsers only, web servers only; 2016 pre-TLS 1.3.
- **Relevance:** the methodological ancestor of N1 M1(b/c): **ephemeral key-share reuse detection by repeated connections** (N1 already reuses this probe) and STEK/ticket longevity. Quantum reframing: under a CRQC, a reused ECDHE value = one Shor run opens every session in the reuse window (amortisation); STEK (AES-128 typically, RFC 5077 suggests AES-CBC-128) becomes a Grover target only if quantum attacker; ticket lifetime/PSK mode determine whether one ECDHE break cascades (E01). Paytm (South Asian fintech) appears in the reuse list — the only South-Asian payment firm in the measurement literature. Not repeated for TLS 1.3/X25519 era or for app API hosts → N1 gap.

### E03 Hebrok, Nachtigall, Maehren, Erinola, Merget, Somorovsky, Schwenk 2023, We Really Need to Talk About Session Tickets (USENIX Security 2023; Paderborn / RUB / TII / achelos)
- **RQs:** RQ1 which crypto vulnerabilities can faulty ticket implementations introduce; RQ2 how 12 open-source stacks implement tickets; RQ3 are real servers vulnerable.
- **Background facts:** Cloudflare: resumption takes half the time of a full handshake at ~4% CPU. 78% of Alexa-1M TLS sites supported tickets (Sy et al. 2018). RFC 5077 format: key_name 16 B, IV 16 B, encrypted_state, MAC 32 B; **AES-128-CBC + HMAC-SHA256** recommended; RFC recommends rotating STEK every 24 h. TLS 1.2: STEK compromise decrypts the issuing session AND all resumed sessions (ticket sent in clear before encryption) → no FS regardless of key exchange. TLS 1.3: ticket carries resumption secret/PSK (derived, so issuing session protected), NewSessionTicket is encrypted (attacker only sees ticket when client redeems it); **psk_ke resumption and 0-RTT early data are decryptable with the STEK; only psk_dhe_ke gives FS for the resumed session**. Active STEK holder can impersonate server in all versions.
- **Pitfall taxonomy (Sec 3):** unencrypted tickets; weak/default keys (GnuTLS 2020 all-zero STEK bug, Klute CVE); reused keystream (CTR/GCM/ChaCha20); cryptographic wear-out (AES-GCM random 12-byte nonce → limit 2^32 tickets per STEK per NIST; CBC+HMAC 2^48); broken authentication → CBC padding oracle; weak algorithms (DES); decryption side channels.
- **Library table (Table 1):** BoringSSL AES-128-CBC/HMAC-SHA256 (RFC-like); Botan AES-256-GCM, 4-byte name + 8-byte magic + 16-byte seed; GnuTLS AES-256-CBC/HMAC-SHA1; Go AES-128-CTR/HMAC-SHA256; MatrixSSL 1.2 AES-256-CBC, 1.3 AES-256-GCM; mbedTLS 4-byte name, AES-GCM/CCM; OpenSSL 3.0.3 AES-256-CBC/HMAC-SHA256; Rustls ChaCha20-Poly1305 no key_name; s2n AES-256-GCM; Apache AES-128-CBC, Nginx AES-128/256-CBC, OpenLiteSpeed (BoringSSL) AES-128-CBC. All use EtM or AEAD; none fully follows RFC 5077. Wear-out risk: MatrixSSL-1.3, s2n, Rustls (2^32 tickets).
- **Scans:** pre-T1M (Apr 2021) 66,992 TLS / 53,059 issue → 1,923 weak STEKs; T1M (May 2021, Tranco 1M) 760,293 TLS / 594,238 issue / 547,159 resume → 3 weak; T100k (Apr 2022) 71,200 / 58,069 / 55,003 → 1 weak; IP100k (Apr 2022) 80,972 / 57,493 / 55,969 → 0; IPF (full IPv4, Aug 2022, ZGrab2, ≤TLS 1.2 only, 3 connections/host) 39,390,365 TLS / 29,621,531 issue → 189 weak, 1 reused keystream. 0 unencrypted, 0 missing auth, 0 padding oracles. Ticket issuance: T100k 82%, IP100k 71%; ~95–97% of issuers resume. Per version (Table A.4, T100k): TLS 1.3 supported by 54.26%, 87.06% of those issue tickets.
- **Key findings:** **AWS Application Load Balancers: 1,903 Tranco-100k hosts (≥1.9%) intermittently used an all-zero AES-256-CBC STEK** (key-rotation bug, mostly redirector hosts — but cookies still exposed) → passive decryption; Stackpath 20 hosts (171 domains on one IP; 90 hostnames affected; ~1.4% of tickets) zero AES-128 + zero HMAC; IPF 111 all-zero keys, 75 servers with 16×0x31 + 16×0x00 (partially initialised), 3 nginx hosts with 0x1011…1F; cause hypothesis: Nginx changed internal key struct in Dec 2016 (48-byte → 82-byte with size field) and external key-writers still assume the old layout. One "GateManager" server reused mbedTLS nonces. Some "tickets" were the 14-byte ASCII string "TICKET FAILURE" (18 servers); tickets >9,000 bytes seen; most 160–240 B.
- **Disclosure:** AWS fixed promptly; Stackpath fixed silently; hosting provider forwarded; infrastructure company no reply; rest to national CERT.
- **Countermeasures:** libraries should validate STEKs when set (not all-zero, entropy/Hamming checks); keep AES-CBC+HMAC or misuse-resistant AEAD (AES-GCM-SIV etc.); counter-based auto rotation; TLS 1.3 preferred.
- **Stated limitations/future work:** black-box limited; no timing side channels or wear-out testing; closed-source stacks unexamined → white-box analysis of more implementations; **root cause = "unauditability of session tickets"** (client cannot see STEK strength/algorithm).
- **Relevance:** (1) STEK is a symmetric key (AES-128-CBC in BoringSSL/Apache/RFC; AES-256 in OpenSSL default) → under a quantum adversary the STEK is a **Grover target** whose break decrypts all psk_ke/0-RTT/TLS 1.2 ticket sessions — N1's "Grover-on-STEK" price (G-group costs) is unaddressed anywhere; (2) clients cannot audit STEK algorithm → N1 can only observe ticket length/lifetime hints and psk modes; (3) TLS 1.3 ticket only visible when redeemed → passive capture of app resumption reveals psk mode; (4) CDNs/cloud LBs (AWS) concentrate risk — same infra-concentration theme as A01/A03/E02.

### E04 Adrian, Bhargavan, Durumeric, Gaudry, Green, Halderman, Heninger, Springall, Thomé, Valenta, VanderSloot, Wustrow, Zanella-Béguelin, Zimmermann 2015, Imperfect Forward Secrecy: How Diffie-Hellman Fails in Practice (CCS 2015; "Logjam")
- **Core idea:** NFS discrete log = **precomputation depending only on the prime p** (polynomial selection, sieving, linear algebra) + cheap per-target **descent** → one investment amortised over every server using the same group. "Well known among cryptographers… lost among practitioners."
- **Logjam (active):** TLS protocol flaw — DHE_EXPORT ServerKeyExchange signature does not cover the chosen ciphersuite → MitM rewrites ClientHello to DHE_EXPORT and ServerHello back; 512-bit discrete log computed in near real time. March 2015 scans: Top-1M HTTPS (539k sites): **68.3% DHE, 8.4% DHE_EXPORT**; IPv4 trusted (14.3M): 23.9% DHE, 4.9% DHE_EXPORT. **Two 512-bit primes = 92.3% of DHE_EXPORT** (Apache hard-coded prime 2.1.5–2.4.7: ~564k servers, 82%; mod_ssl default ~89k, 10%; 463 distinct primes).
- **512-bit computation (CADO-NFS):** precomputation ~7 days per prime (poly select 7,600 core-h; sieving 21,400 core-h on 2,000–3,000 cores; linear algebra 60,000 core-h on 36-node cluster, 2.16M-row matrix; DB 2.5 GB); **descent median 70 s (34–206 s)** over 3,500 logs; compare 512-bit RSA factoring ~8 days on same box / 3 h on 1,800 EC2 cores. Compromises ~7–7.8% of Top-1M. Delay workarounds: non-browser clients (curl/git) no timeouts; TLS warning alerts keep Firefox alive; **ephemeral key caching** (OpenSSL reuses g^b without SSL_OP_SINGLE_DH_USE; F5 BIG-IP unless "Single DH"; **Microsoft SChannel caches g^b for 2 h hard-coded**) — **17% of sampled IPv4 DHE hosts reused g^b at least once in 20 handshakes, 15% used only one value**; False Start leaks first request (passwords/cookies).
- **Other weak groups:** 2,631 trusted servers (118 Top-1M) used ≤512-bit non-export DHE (www.fbi.gov passive decryption demo); 4,800 of ~70,000 primes not safe (9 composite p); small-subgroup + short exponent (van Oorschot–Wiener) recovered full exponents for 159 hosts (53 trusted) — VPN web UIs 48, conferencing 27, comms 21, FTP 6; 5,741 Java hosts used DSA q as generator g (ASN.1 confusion).
- **State-level scaling (Table 2):** DH-768 ≈ 36,500 core-years precomputation (28,500 linear algebra), descent ~2 core-days → "academic"; **DH-1024 ≈ 45M core-years precomputation, descent ~30 core-days**; ASIC sieving ~$8M for one year (3M chips at ~$2); linear algebra ~hundreds of millions $ with ASICs (Titan 117 years; $11B in supercomputers otherwise); NSA CCP budget $10.5B (FY2012). 2048-bit ~10^9× harder.
- **Impact table (Table 3, passive unless noted):** one 1024-bit group → Top-1M HTTPS 17.9% (205k with downgrade 37.1%), IKEv1 66.1%, IKEv2 63.9%, SSH 25.7% (3.6M); ten groups → HTTPS Top-1M 24.0% (56.1% with downgrade). IKE: 86.1%/91.0% support Oakley Group 2; SSH 98.9% support Group 2, 21.8% prefer it. Mail: SMTP 50.7% STARTTLS, 14.8% DHE_EXPORT, 15.5% top-ten 1024-bit groups. NSA TURMOIL/VAO/CORALREEF documents (target 100,000 ESP keys/hour; needs two-sided IKE transcript + PSK) "consistent with" a 1024-bit DH break.
- **Recommendations:** move to ECDH (Curve25519); disable DHE_EXPORT; ≥2048-bit primes; clients reject <1024 (browsers moved 512→1024; Safari had accepted 16-bit groups); avoid fixed 1024-bit primes, verifiable generation (trapdoor risk); "don't deliberately weaken crypto". Akamai dropped export suites; negotiated FFDHE groups extension (RFC 7919) followed.
- **Limitations:** 1024-bit numbers are extrapolations from asymptotic complexity ("further work needed for greater confidence"); NSA evidence circumstantial; ECDH not analysed.
- **Relevance (concept anchor for M2 "sessions per break"):** Logjam is the **classical precedent for amortised cryptanalysis**: precomputation per shared parameter, cheap per-instance step, downgrade via unsigned negotiation (→ D05 transcript binding / hybrid fallback paths), and ephemeral-value caching (SChannel 2 h) that turns one discrete log into many sessions. Quantum analogue: Shor on ECDLP has no group-wide precomputation for a fixed curve beyond circuit compilation, so amortisation in the PQ era comes from **key reuse / resumption / RSA key transport**, not shared groups — a contrast N1 should state explicitly. Also the "promotion of PFS may have reduced security" irony parallels hybrid-only deployment with legacy fallbacks (A01 legacy features).

### E05 Valenta, Sullivan, Sanso, Heninger 2018, In Search of CurveSwap: Measuring Elliptic Curve Implementations in the Wild (IEEE EuroS&P 2018; UPenn / Cloudflare / Adobe)
- **Q:** Is Sullivan's 2015 CurveSwap (curve-parameter downgrade in TLS ≤1.2: client's supported-curves list is only authenticated in Finished via the DH secret) feasible? Measures EC support, point validation, twist security, key reuse for TLS (16 ports), SSH, IKEv1/v2; passive client data; source review incl. JWE.
- **Data:** 10% IPv4 ZMap/ZGrab scans Nov 2016–Aug 2017 (extrapolated to 100%), Censys baselines; **4,187,201 ClientHellos sampled from Cloudflare over ~5 min on 17 Oct 2016** (99.4% carry supported-curves).
- **Server support (Table 1, port 443):** Nov 2016 38.6M TLS, 24.8M ECDHE: secp256r1 97.0%, secp384r1 22.9%, secp521r1 10.2%, secp224r1 2.6%, brainpool256r1 3.9%, x25519 0 (not yet scanned/standardised); **Aug 2017 41.0M/28.8M: secp256r1 86.9%, x25519 740.7K (2.6%)**. 64% HTTPS and 54% SSH hosts support ECDH (vs 7.2%/13.8% in 2013, Bos et al.). SSH: x25519 77.2%, nistp256 97.8%. IKEv1: secp224r1 66.8%. No hosts negotiated ec2n-155/185 or custom explicit curves.
- **Client support (Table 2):** top orderings: 23,24,25 (NIST ascending; Firefox, IE11, Safari, Tinder app) 35.9%; 29,23,24 (x25519 first; Chrome 50–54) 21.7%; 23,24 15.8%; long SEC2 list (okhttp/3.2.0, Picsart, uservoice-android, Python-urllib) 14.8%. **>16% of clients offer 80-bit curves (sect163k1 etc.), mostly API clients/apps, not browsers.** Note: mobile/API libraries (okhttp) advertised long weak curve lists — **app clients lag browsers** (precedent for N1's app-vs-browser group gap).
- **Repeated key-exchange values (Table 3, secp256r1, two rapid scans):** **TLS 443: 22.9% (5.5M) same value both scans; 2.7% share a value with another host**; SSH 0%; IKEv1 0.3%; IKEv2 1.9%. Other ports: 563 (NNTPS) 82.7%, 636 (LDAPS) 65.0%, 8443 21.7%. Weak curves: 2.6–3.7% of supporting hosts repeat; ephemeral-static lifetimes short (secp160k1: 5 hosts same after 5 h, 2 after 25 h).
- **Servers ignoring client curves:** 25% (8.5M of 34.6M) replied with a curve the client never offered (always P-256/384/521) — RFC 4492 violation; not exploitable.
- **Invalid-curve acceptance:** order-5 point on invalid secp256r1 → 0.31% of HTTPS completed handshake → **est. 0.77% HTTPS, 0.04% SSH (Cerberus/VShell/SshServer), 4.04% IKEv2 fail validation**; no twist acceptance in TLS; **no host both failed validation AND reused keys → no feasible CurveSwap found**.
- **Protocol analysis:** TLS 1.3 (server signs transcript hash in CertificateVerify) and SSH (host key signs whole exchange) resist parameter downgrade; RFC 7627 extended master secret partially mitigates TLS 1.2; IKE requires breaking authentication too.
- **Source code:** JWE (RFC 7516) standard omits point validation → **node-jose (Cisco), jose2go, Nimbus JOSE+JWT, jose4j vulnerable to invalid-curve key recovery** (patched; Nimbus/jose4j partially protected by Java provider checks); NSS and Java 5-bit-window NAF scalar multiplication missing if/else (wrong results, not exploitable; patched NSS 3.31, Java Jul 2017).
- **Discussion:** long tail of curve support is a liability if any class weakens; newer constructions (Curve25519) are misuse-resistant; downgrade protection by transcript signing.
- **Limitations:** IPv4 only, 10% samples, firewalled hosts invisible; Cloudflare sample 5 minutes, skewed to Cloudflare customers and active timezones, includes bots/apps.
- **Relevance:** (1) second methodological ancestor for **ephemeral-key-reuse probing (two rapid handshakes)** — 22.9% of HTTPS hosts reused P-256 shares in 2016 → under CRQC each reused share = one Shor run unlocks many sessions; N1 should re-measure for X25519/X25519MLKEM768 shares on Bangladesh finance/API hosts; (2) **downgrade theory**: TLS 1.3 transcript signing prevents curve downgrade — so a hybrid→classical "downgrade" in TLS 1.3 is only possible if the client/server *legitimately* negotiate classical (fallback, HRR, middlebox) → N1 measures fallback, not cryptographic downgrade; (3) API/app clients offered weaker curves than browsers (okhttp) — an early sign that **app stacks lag**; (4) JWE/app-layer crypto bugs (A04's OIDC point; B06 app-layer encryption).

### E06 Mosca & Piani 2026 (March), Quantum Threat Timeline Report 2025 (evolutionQ / Global Risk Institute; 7th annual report since 2019)
- **Method:** online expert survey, **26 respondents** (e.g., Aharonov, Blais, Cirac, Coish, DiVincenzo, Ekerå, Ekert, Gottesman, Morello, Simmons, **Shor**, Wilhelm-Mauch, Boixo (Google), Eisert, Fitzsimons, Gambetta (IBM), Gao, Hensinger, Knight, Yi-Kai Liu (NIST), Maniscalco, Menicucci, Mølmer, Severini, Vandersypen, Weihs); mostly university-based; core of 2019 respondents retained. Key question unchanged since 2019: **likelihood that a QC able to factor RSA-2048 in <24 h is built within 5/10/15/20/30 years**, 7 uneven bins (<1%, <5%, <30%, ~50% [30–70%], >70%, >95%, >99%); optional point estimates (n = 15).
- **Raw counts (Appendix A.4, bins <1/<5/<30/~50/>70/>95/>99):** 5 yr 13/5/6/1/1/0/0; 10 yr 3/4/6/7/4/1/1; 15 yr 0/3/5/3/9/4/2; 20 yr 0/0/2/6/6/4/8; 30 yr 0/0/1/3/5/5/12 [reconstructed from the garbled table and checked against Table 1 text; each row sums to 26].
- **Headline results:** 5 yr: 13/26 ≥1%, 8/26 ≥5%. **10 yr: 19/26 (73%) >5%; 13/26 ~50% or more** (highest 10-yr optimism in the series); 15 yr: 18/26 ≥~50%, 15/26 "likely"+; 20 yr: 24/26 ≥~50%, 12/26 ≥95%; 30 yr: 22/26 "likely"+, one "unlikely". **Average cumulative probability: ~28% (pessimistic) to ~49% (optimistic) within 10 years (≈2035); ~15% within 5 years (optimistic); pessimistic ~51% by 15 yr, ~69% by 20 yr.** Upward shift vs 2022–2024 surveys; 2019–2021 were even higher for the mid-2030s (COVID/VC tightening as "watershed").
- **Other findings:** 100 logical qubits within 5 years — most sceptical; superconducting still most promising, cold atoms (Rydberg) nearly on par; surface code leading for superconducting, qLDPC and bosonic codes promising; Gidney 2025 (<1M qubits, <1 week for RSA-2048; 20× fewer qubits than Gidney–Ekerå 2021) and Chevignard et al. 2025 named as key theory advances; Google Willow distance-7 surface-code memory (logical qubit lives >2× best physical). Near-term milestone wanted by mid-2026: programmable logical processor with 5–10 logical qubits incl. fault-tolerant non-Clifford gates; "horizontal scale" across chips/cryostats. **Covert research:** majority of 22 think it could shift timeline by ≥2 years → "safer to assume threat is closer". Funding: most expect increases; largest "decrease" share yet; McKinsey ~50% start-up investment increase in 2024. Race: North America leads; China main challenger in 5 yr; Europe falling behind. Hype → "quantum winter" risk. DARPA QBI to verify utility-scale by 2033. BSI 2025: CRQC "likely within 15 years", maybe ~10 if qLDPC demos work.
- **Policy deadlines cited:** **Canada** — every federal department PQC migration plan by April 2026, high-priority systems by end-2031; **EU** coordinated roadmap — member states begin PQC deployment by 2026, critical infrastructure complete by end-2030.
- **Framework:** **Mosca inequality T_shelf-life + T_migration > T_threat** ⇒ exposure; maximum migration time (T_migration)_max = T_threat − T_shelf-life; HNDL; risk is also integrity/availability once CRQC arrives before migration completes; rushed migration creates classical bugs; recommends crypto-agility and the Quantum Risk Assessment (Mosca & Mulholland 2025).
- **Limitations (self-stated):** small n, coarse uneven bins, changing respondent pool, averages may mislead, experts admit forecasting difficulty; conflict of interest (evolutionQ sells quantum-safe products); question targets RSA-2048 only (not ECC-256, which needs fewer qubits — see F06/F09).
- **Relevance:** supplies N1's **T_threat** distribution for the Mosca/HNDL argument (Bangladesh financial data shelf-life ≥7–10 yrs; migration time unknown → N1 measures where migration stands). Note the report's metric is RSA-2048 factoring in 24 h; for TLS key exchange (X25519/P-256), ECDLP estimates (F06 Babbush 2026, F09 Luo) are the right benchmark and are generally *cheaper* than RSA-2048 — N1 should state that the survey is a conservative proxy for the ECDH threat.

### E07 Grover N., Haile, Pedersen, Uner, Erickson 2026, A Scenario-Based Evaluation of CRQC+AI Vulnerability Spectrum for TLS 1.3 Cryptographic Dependencies (arXiv 2608.23785v2, 7 Sep 2026; EnQuanta / MOYA / Lab33)
- **Type:** scenario/modelling paper; **no empirical data** ("No new empirical data were created"). Conflict of interest: all authors affiliated with EnQuanta (sells crypto-agile/hybrid products). Figures rendered with an AI model (Claude Fable 5) from author parameters; an earlier 2024 preprint version was withdrawn (authorship dispute).
- **Evidence tiers (Table 1A/1B):** mechanism-backed = RSA, ECC (Shor) → "migration mandatory"; contingency-backed = ML-KEM, ML-DSA (only if an undiscovered **effective-dimension collapse ρ** of lattice block size exists); hypothesis-only = SLH-DSA, AES-256 (no structural attack; Grover already priced). States explicitly: **no known break of ML-KEM, ML-DSA, SLH-DSA or AES-256.**
- **Scope:** five primitives as used in TLS 1.3 (RSA-2048, ML-KEM-768/1024, ML-DSA-44, SLH-DSA, AES-256); models "primitive erosion" only; TLS 1.3 = best case (ephemeral keys, negotiation, short-lived certs); SSH/IPsec/DNSSEC/code signing worse. Notes TLS 1.3 removed RSA key transport; RSA remains in certificates (RSASSA-PSS), legacy interop, downgrade exposure.
- **Background analyses (negative findings):** HHL runtime Õ(s·κ·polylog(N/ε)) — LWE matrices dense (s≈N), ill-conditioned, bounded-distance decoding not exact Ax=b, and output is a quantum state → **HHL gives at most polynomial help to an inner step, not a break**; 2024 claimed quantum LWE algorithm (Chen) withdrawn within days; quantum annealing (gap closes exponentially for hard instances; D-Wave factoring only small semiprimes; "documents the wall") and VQE (barren plateaus; no reduction from factoring/DLP/lattices) → no standalone break; geometric-algebra embedding = explicit falsifiable hypothesis only.
- **Lattice cost model (Sec 3.1.3, 4.5):** core-SVP cost 2^(c·β), c = 0.292 classical / 0.265 quantum sieving (QRAM-optimistic; best known 0.2563, Bonnetain et al. 2023); Kyber-1024 β ≈ 877 → ~2^256 classical / ~2^232 quantum; Kyber-768 hybrid β ≈ 625; ML-DSA-44 β ≈ 420. Break condition (0.265 − Δ)·β·(1 − ρ) ≤ B(t), with sieving floor 0.2075 (Kirshanova–Laarhoven list-size bound) and aggressive budget B(t) = 52 + 4(t − 2026) bits (B(2033) = 80, B(2036) ≈ 92). **Even at the floor ML-KEM-1024 costs 2^182 → erosion alone cannot break it by 2033; requires ρ ≥ 0.66 (ML-KEM-1024), ρ ≥ 0.52 (X25519+ML-KEM-768 hybrid, plus breaking X25519), ρ ≥ 0.17 (ML-DSA-44); 0.56/0.69/0.25 at c = 0.292.** Retrodiction: sieving exponent fell ~1.2×10⁻³/yr (0.2653 in 2015 → 0.2563 in 2023); reaching floor by 2033 would need ~7× historical rate (floor otherwise ~2064–2074). Memory (sieve list 2^182 / 2^129.7 vectors) further pushes dates later. Not priced: dual attacks, multi-target/amortised cost, decapsulation failures, side channels ("implementation compromise of a deployed PQC stack before 2035 is more probable than a structural lattice break").
- **Hardware channel model (Sec 3.3):** four channels — logical-qubit count (binding; ~10³ factor, 1.1 e-folds/yr, ≈2032), gate fidelity (≈2029), code efficiency/qLDPC (≈2029), decoder latency 60 µs→1 µs (≈2030); AI acceleration factors A1–A4 (1.0/1.3–1.5/1.8–2.5) → RSA-2048 crossover ≈2032 (no AI), ≈2031 (central), ≈2029 (high). Anchors: Gidney–Ekerå 2019/2021 20M qubits 8 h → Gidney 2025 <1M qubits <1 week; Willow Λ ≈ 2.14, 0.143%/cycle at d = 7; IBM Starling ~200 logical qubits by 2029; QuEra 20 physical per logical. Cited 2026 estimates: Iceberg "Pinnacle" <100,000 physical qubits for RSA-2048; Caltech/IQIM ~10,000 reconfigurable atoms (F07); Inria/CNRS 1,193 logical qubits for ECC-256 (~42% fewer than RSA); Hansung/Nanyang ECDLP circuit 40% better qubit×depth; Google March 2026 further reduction and internal PQC deadline moved 2030 → 2029; July 2026 "zero-knowledge proof approach" claim.
- **Capability model results (Appendix A, four AGI tracks with AGI onset 2028):** 50% crossovers — **RSA-2048 2032.5 / 2031.4 / 2030.5 / 2029.9 (Tracks 0–3)**; Kyber-1024 2045.9 (T1, marginal) / 2035.0 (T2) / 2032.3 (T3); ML-DSA-44 2035.9 / 2032.9; SLH-DSA, AES-256 none by 2046. Joint Monte Carlo (N = 40,000/cell): RSA-2048 T0 median 2033.0, **P(≤2035) = 0.95**; Kyber-1024 T0 median 2048.8, P(≤2035) = 0.00; T3 median 2033.0, P(≤2035) = 0.98. AGI onset is the dominant uncertainty for all software-driven dates (2-yr slip → ~1.8-yr later). Couplings α/β are "chosen rather than measured".
- **Policy/economics cited:** US EO (June 2026) — HVAs/high-impact systems PQC key establishment by **31 Dec 2030**, signatures by 31 Dec 2031; NIST IR 8547: RSA-2048/P-256 deprecated 2030, disallowed 2035; CNSA 2.0 requires ML-KEM-1024/AES-256; Citi/Hudson: single-day quantum attack on a top-5 US bank's Fedwire access = $730B–$1.95T direct, $2.0–3.3T GDP-at-risk; PQC market $1.9B (2025) → $12.4B (2035); Moody's ~2.5% of IT budgets; public awareness of PQC ~25–30%; Mosca/GRI "one in seven by 2026, ~50% by 2031" (older figure) and "34% by 2030".
- **Governance section (Sec 6):** crypto-agility = governance capability (inventory, owner, rotation authority, change control, evidence); **sector secrecy horizons: payments/card data X ≈ 5–10 yr with migration Y months–2 yr (cloud) → "lower" urgency**; health 25–50+; legal decades; national security 25–75+; sovereignty divergence (CNSA 2.0 standalone ML-KEM-1024 vs hybrid default); trust anchors lag key exchange; **Sec 6.5: "middleboxes, session-resumption caches and libraries that do not recognize the new groups can cause negotiation failure or a silent downgrade to a classical exchange… out of scope"**; entropy/key provenance.
- **AES claim to flag:** states AES-256 is "the only one of the three levels" meeting a 128-bit quantum bar under naive k/2 Grover, while also conceding Grover parallelises poorly and under NIST depth limits AES retains near-classical strength — internally hedged; contrasts with NIST categories where AES-128 key search defines Category 1 (G02 Jaques et al.).
- **Relevance:** gives N1 (a) an **ECC/RSA timeline anchored to resource estimates** (RSA crossover ~2030–2033; ECC cheaper), (b) explicit statement that **negotiation/fallback/resumption-cache downgrade is unmeasured ("out of scope")** — exactly N1's M-item on app fallback, (c) confirmation that hybrid X25519MLKEM768 falls only if both fall → HNDL protection rests on ML-KEM, so N1's question is coverage (who negotiates hybrid), not ML-KEM strength. Quality flag: speculative AGI driver, vendor COI, AI-rendered figures; use only the mechanism-backed tier and policy facts.

### E08 Wilson-Shah 2026, Quantifying Quantum Risk: A Measure of Crypto Agility (arXiv 2606.17116 preprint; single author)
- **Q:** "How agile is agile enough?" Introduces **rotation time t_rot** (time to patch/replace/swap a cryptographic control) as the measure of crypto-agility and links it to an annual risk tolerance R for a **hybrid system** (two independent controls C1, C2; attacker must breach both).
- **Model:** vulnerabilities in each control are Poisson (rates λU, λV per year); compromise if a disclosure in one control is followed by one in the other within t_rot; E(S) = λU·λV·(2Tt − t²); P(compromise) = 1 − exp(−λUλV(2Tt − t²)); **t_rot = T − √(T² + ln(1 − R)/(λUλV))**. Assumes constant motivated attacker, equal knowledge on disclosure, independence; treats CRQC arrival "no different from any other emergent exploitable vulnerability".
- **Data:** NVD CVEs (retrieved 22 Oct 2025) for 12 libraries (Botan, Bouncy Castle, BSAFE, Cryptlib, Crypto++, GnuTLS, Libgcrypt, LibreSSL, Mbed TLS, Nettle, OpenSSL, wolfSSL); newest CVSS version, NIST score preferred. **λ max = 10.20/yr (OpenSSL), min 0.35 (cryptlib), mean 3.36.**
- **Results (Table B1):** with λ = 10.20: R = 1% → t_rot 0.42 h; 5% → 2.16 h; 10% → 4.44 h; 25% → 12.13 h. With λ = 3.36: 1% → 3.90 h; 10% → 41.0 h; 25% → 112.4 h. → **required rotation "hours to days"**; real practice lags (2020 report: >50% of organisations cannot patch critical vulns within 72 h; ~15% unpatched after 30 days; common "patch within 7 days" policies). Mentions national payments infrastructure as a demanding-tolerance example.
- **Future work (stated):** weight by exploit likelihood (EPSS) instead of "constant attack"; rigorous treatment of 3+ controls (early analysis: little difference).
- **Limitations/critique (mine):** CVE counts ≠ algorithmic breaks; model addresses live compromise — **does not cover HNDL**, where rotation after a CRQC appears cannot protect already-harvested traffic (only pre-emptive hybrid deployment does); independence of hybrid components assumed; single-author, not peer reviewed.
- **Relevance:** gives N1 a quantitative vocabulary for **crypto-agility of app clients** — an app whose TLS stack is bundled (B04) or pinned (B02/B05) has rotation time = app-update cycle (days–months, user-dependent), versus server/CDN-side rotation (A01: infra-managed, hours). Supports the argument that platform/CDN-managed stacks are more agile than app-bundled ones; hybrid KEM (D01/D02) is the HNDL defence, agility is the live-attack defence.

### F01 Roetteler, Naehrig, Svore, Lauter 2017, Quantum Resource Estimates for Computing Elliptic Curve Discrete Logarithms (ASIACRYPT 2017; Microsoft Research; arXiv 1706.06752)
- **Method:** full reversible Toffoli-network implementation of controlled EC point addition (affine Weierstrass coordinates, prime fields) in LIQUi|> (F#); classical simulation of the point-addition circuit for NIST P-192, P-224, P-256, P-384, P-521 (up to 521 bits) to verify correctness; counts logical qubits, Toffoli gates and Toffoli depth (Clifford gates free). Modular arithmetic: Takahashi adders, Häner et al. constant adders, Montgomery multiplication (fewer Toffolis, more qubits), Kaliski binary-GCD Montgomery inverse with counter for constant 2n rounds (inversion dominates qubits and cost). Semiclassical Fourier transform (one control qubit recycled).
- **Formulas:** qubits ≤ **9n + 2⌈log2 n⌉ + 10**; Toffoli ≤ **448 n³ log2 n + 4090 n³** (point addition 224n² log2 n + 2045n², iterated 2n times). Per-circuit counts (Table 1): inversion 7n + 2log2 n + 9 qubits, 32n² log2 n Toffolis; Montgomery mul 5n + 4 qubits, 16n² log2 n − 26.3n².
- **Key numbers (Table 2):** **P-256: 2,330 logical qubits, 1.26×10¹¹ Toffoli gates, Toffoli depth 1.16×10¹¹**; P-224: 2,042 q / 8.43×10¹⁰; P-384: 3,484 q / 4.52×10¹¹; P-521: 4,719 q / 1.14×10¹². RSA (interpolated from Häner et al. 2017): RSA-2048 4,098 q / 5.20×10¹² Toffoli; **RSA-3072 (same classical security as P-256) 6,146 q / 1.86×10¹³** → **ECC is an easier quantum target than RSA at equal classical security** (supports Proos–Zalka 2003). Toffoli depth ≈ gate count (little parallelism).
- **Remarks:** Ekerå–Håstad short-DLP trick doesn't apply to ECC (only cuts RSA counts by 4); complete addition formulas / Edwards curves left open; fidelity loss from exceptional cases ≈ n/2^(n−1).
- **Limitations / future work (stated):** logical-level only (no error-correction overhead, no physical qubit counts, no runtime); register sharing (Proos–Zalka 2n + 8√n) not implemented; reduce qubits for reversible inversion; investigate other curve models.
- **Relevance:** the **canonical per-key price of breaking one ECDH share** (P-256 ~1.26×10¹¹ Toffoli on ~2,330 logical qubits) — used by E01 and by N1's "cost per Shor run" / sessions-per-run amortisation. Curve25519 (n = 255) ≈ same cost as P-256 (Montgomery curve, not directly simulated). Each *distinct* ephemeral share requires one full run → no amortisation unless keys are reused (E02/E05) or keys are long-lived (RSA key transport, static ECDH).

### F02 Häner, Jaques, Naehrig, Roetteler, Soeken 2020, Improved Quantum Circuits for Elliptic Curve Discrete Logarithms (PQCrypto 2020; Microsoft Quantum / Oxford; arXiv 2001.09580)
- **Method:** improves RNSL (F01) at the logical layer in Q# (unit-tested, automatic resource estimation); Clifford+T cost model (T gates dominant; AND gate 4 T vs Toffoli 7 T); adders: CDKMG (lowest T), DKRS carry-lookahead (lowest depth), TTK (lowest width); **windowed arithmetic with quantum table look-ups (QROM)**, pebbling ("multiply-then-add"), swap-based reformulation of Kaliski's binary GCD inversion, parallel pseudo-inverse correction, qubit reuse in modular division; affine Weierstrass point addition = 2 divisions, 2 multiplications, 1 squaring, 9 additions; exceptional cases ignored (negligible distortion).
- **Results (Table 1, full Shor ECDLP):** **P-256 — Low-W: 2,124 qubits (vs RNSL 2,338), T-count 1.72·2³² (~7.4×10⁹), T-depth 1.98·2³⁰; Low-T: 2,619 qubits, T 1.08·2³¹; Low-D: 2,871 qubits, T 1.34·2³², T-depth 1.12·2²⁴ (~1.9×10⁷)** — improvement over RNSL: T-count ×119, T-depth ×54 (Low-W); T-depth ×~6,000 for +22% qubits (Low-D). P-384 Low-W 3,151 qubits; P-521 Low-W 4,258 qubits (T-depth ×13,792 better in Low-D, +22% qubits). Abstract summary: "233 T gates with T-depth 225 and 2,871 qubits" for depth-optimised 256-bit.
- **Asymptotics:** Low-W ≈ 8n + 10.2 lg n − 1 qubits, 436n³ T gates, T-depth 120n³; Low-T 10n + 7.4 lg n + 1.3 qubits, 1115n³/lg n T; Low-D 11n + 3.9 lg n + 16.5 qubits, T-depth 285n².
- **Comparison:** RSA-3072 (Gidney–Ekerå 2019 extrapolation) ~2³⁴ T gates and 9,287 logical qubits → **ECC less quantum-secure than RSA at similar classical security**. Mentions 2,330 logical qubits ≈ 6.77×10⁷ physical qubits under plausible error rates (Fowler-style estimate).
- **Limitations / future work:** logical layer only (no surface-code layout); window >18 extrapolated; automatic T-depth optimisation explodes qubits; recursive GCD, projective/Edwards coordinates, Rines–Chuang multipliers left open.
- **Relevance:** updates N1's per-key cost: one P-256/X25519 ECDH break ≈ 10⁹–10¹⁰ T gates on ~2,100–2,900 logical qubits; **depth-optimised variants make per-session runtime short (T-depth ~10⁷) → once a CRQC exists, per-session time is small, so amortisation via key reuse matters less for runtime than for total machine-time budget** — nuance for M2. Shows the trend: same problem, ~100× cheaper in 3 years (algorithmic progress, cf. E06/E07 trend arguments).

### F03 Litinski 2023, How to Compute a 256-bit Elliptic Curve Private Key with Only 50 Million Toffoli Gates (arXiv 2306.08585; PsiQuantum)
- **Type:** theoretical resource estimate for Shor-ECDLP on 256-bit curves, comparing a 2D-local surface-code "baseline" architecture with PsiQuantum's "active-volume" architecture (non-local module connections); hardware cases: superconducting (1 µs cycle), trapped ions (1 ms), photonic fusion-based.
- **Headline numbers:** ~44–109 million Toffoli gates per key (depending on configuration) vs ~10¹¹ in F01 — roughly three orders of magnitude lower than the 2017 estimate; baseline architecture ~6,000 logical qubits, ~9.4 million physical qubits; time per key ranges from minutes–hours (fast superconducting/active-volume assumptions) to months (trapped ions, baseline). Active-volume architecture reported 300–700× cheaper per key than 2D-local. Assumes physical error at 10% of threshold; closer to 50% doubles code distance (4× footprint, 2× time). Notes 256-bit ECC is 100–300× cheaper than RSA-2048 in the same model → **ECC-256 expected to be the first widely used cryptosystem to fall**.
- **Stated limitations / open problems:** architecture-specific (author's employer's design); reaction-time limits (10 µs) may bound runtime; low-footprint regime and depth optimisations unexplored.
- **Relevance:** documents the steep downward trend in the estimated cost of breaking 256-bit ECDH (F01 → F02 → F03 → F05/F06), reinforcing that X25519/P-256 key exchange — the part of TLS that HNDL targets — is the most urgent migration item. N1 uses it only as a cited cost range; the defensive implication is that hybrid PQ key exchange coverage (A01) matters more than the precise attacker cost.

### F04 Gidney & Ekerå 2021, How to Factor 2048-bit RSA Integers in 8 Hours Using 20 Million Noisy Qubits (Quantum 5, 433; arXiv 1905.09749; Google / KTH & Swedish NCSA)
- **Type:** end-to-end physical resource estimate (surface code, planar nearest-neighbour superconducting grid, 10⁻³ gate error, 1 µs cycle, 10 µs reaction time), including noise, retries and layout — factors usually ignored. Combines windowed arithmetic, Ekerå–Håstad short-DLP variant, coset representation, oblivious carry runways.
- **Headline:** **RSA-2048 ≈ 20 million physical qubits, ~8 hours (expected ~0.31 days incl. retries), 5.9 megaqubit-days** — ~100× smaller spacetime volume than prior comparable estimates (Fowler 2012: ~1 billion qubits; Table 2: Van Meter 2009 6.5B qubits/410 days → this work 20M/0.31 days). Abstract-circuit cost: 3n + 0.002n lg n logical qubits, 0.3n³ Toffolis (≈2.7 billion Toffoli+T/2 at n = 2048). Table 3: RSA-1024 5.9M? [per-run qubits 9.7M, 1.3 h]; RSA-3072 38M qubits, 12 h; RSA-4096 55M, 22 h. Table 1 also lists ECDLP (Roetteler 2017) at n = 256: 130 billion Toffoli+T/2, 83 megaqubit-days.
- **Caveats (stated):** "ballpark figures… not exacting predictions"; doubling gate error raises qubits >10%; low end of estimates sensitive to future QEC advances.
- **Relevance:** benchmark used by E06 survey ("RSA-2048 in <24 h") and by every later estimate (F05 reduces to <1M qubits). For N1: RSA matters in TLS 1.2 RSA key transport (A05: 28.9% of nginx configs allow it; E01: one key opens all recorded sessions to that server) and in certificates; the 2048-bit RSA benchmark is what policy timelines (NIST IR 8547 2030/2035) are calibrated against.

### F05 Gidney 2025, How to Factor 2048-bit RSA Integers with Less than a Million Noisy Qubits (arXiv 2505.15917; Google Quantum AI)
- **Type:** updated physical resource estimate under the *same* assumptions as F04 (square grid, nearest-neighbour, 0.1% gate error, 1 µs cycle, 10 µs reaction time).
- **Headline:** **RSA-2048 with <1 million physical qubits in <1 week** (vs 20M qubits / 8 h in F04) — a ~20× qubit reduction traded for longer runtime. Peak ~1,409 logical qubits (m = 1,280 input qubits in dense "cold storage" via yoked surface codes at ~430 physical/logical; hot patches d = 25 at 1,352 physical/logical); ~12 h per shot, ~93% no-error shot rate; Toffoli count >100× lower than Chevignard–Fouque–Schrottenloher 2024 (which used ~2 trillion Toffolis for ~0.5n logical qubits). Enablers: approximate residue arithmetic (CFS 2024), yoked surface codes (2023/2025), magic-state cultivation (2024).
- **Author's conclusion:** cannot see another 10× qubit reduction under these assumptions, but "attacks always get better"; **endorses NIST IR 8547 draft: deprecate vulnerable systems after 2030, disallow after 2035 — "not because I expect sufficiently large quantum computers to exist by 2030, but because I prefer security to not be contingent on progress being slow."**
- **Limitations:** RSA only (ECC extension left to Ekerå/future work — later done in F06); assumptions about cultivation/yoking performance are projections.
- **Relevance:** the "<1M qubits" figure cited by E06 (expert survey) and E07; for N1 it is the authoritative statement that policy deadlines (2030/2035) are justified by risk management rather than by a predicted CRQC date — useful framing for Bangladesh regulator recommendations (H-group).

### F06 Babbush, Zalcman, Gidney, Broughton, Khattar, Neven, Bergamaschi, Drake, Boneh 2026, Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv 2603.28846v2; Google Quantum AI / UC Berkeley / Ethereum Foundation / Stanford)
- **Type:** whitepaper (~57 pp + appendix); new resource estimates for 256-bit ECDLP (secp256k1) plus blockchain vulnerability survey and policy discussion. Read sections I–IV, VII, IX in full; blockchain-specific sections (III, V, VI, VIII) skimmed for structure.
- **Disclosure model (novel):** authors **withhold the circuits** ("responsible disclosure" — quantum ECDLP vulnerabilities are "hard-to-fix") and instead publish a **zero-knowledge proof** (SP1 zkVM, Groth16) that a secret reversible point-addition circuit of the stated size is correct on 9,000 Fiat–Shamir-derived random inputs. Debate noted (Aaronson oscillating between non-disclosure and full transparency).
- **Headline estimates (single instance):** **≤1,200 logical qubits & ≤90 M Toffoli, or ≤1,450 logical qubits & ≤70 M Toffoli** for 256-bit ECDLP (~4.5n space); ~an order of magnitude better spacetime volume than prior single-instance work (prior: Chevignard et al. ~1,100 qubits but >100 B Toffoli; Litinski ~200 M Toffoli single-instance); **<500,000 physical qubits** (planar degree-4, 10⁻³ error, yoked storage); **~18–23 minutes** reaction-limited runtime at 10 µs; more aggressive architectures (qLDPC "bicycle", "Pinnacle") could approach ~100,000 qubits but need undemonstrated connectivity.
- **Fast-clock vs slow-clock:** superconducting/photonic/spin CRQCs solve ECDLP in minutes; neutral-atom/ion-trap 2–3 orders slower (relevant to F07/F08). Two scenarios for planning (fast attacks arrive with slow ones vs later).
- **Progress-measurement claims:** QC is in an "era of ferment" — **threshold model, not qubit counting**; the small-curve "challenge ladder" (F13) "may fail to provide a reliable early warning"; **"a successful public demonstration of Shor's algorithm on a 32-bit elliptic curve should not be seen as a wake-up call… as much as a potential signal that PQC adoption has already failed."** Transparency will decrease as CRQCs approach; first CRQC may be detected rather than announced.
- **Section IV (TLS-relevant):** ECDH key exchange lets a passive CRQC eavesdropper recover shared secrets; costs on other 256-bit curves "same order of magnitude"; 381-bit curves need ~50% bigger registers; TLS's strongest curve (P-521) needs only a slightly larger CRQC; **larger curves give "at best partial and temporary, at worst nearly non-existent" protection** (1024-bit curve ≈ 5,000 logical qubits, ~64× runtime).
- **Section VII (migration):** PQC is newer/less scrutinised (SIKE broken classically); quantum-algorithm research (Regev-reduction/DQI, Kikuchi-method LPN speedups) could eventually threaten lattices — or raise confidence; PQC implementations newer (Falcon Gaussian-sampling side channels); PQ signatures 1–2 orders larger (Falcon ~1,280 B vs ECDSA 64–73 B); composite/hybrid signatures costlier still; user education, UI defaults and "quantum-safe default settings" needed; migration takes years.
- **Outlook:** time to CRQC "still exceeds" migration time "though the margin for error is increasingly narrow"; urges immediate PQC migration. COI statement included.
- **Relevance:** (1) latest authoritative ECDLP cost — directly the cost of breaking one X25519/P-256 TLS key share (N1 cites as the 2026 reference, superseding F01–F03); (2) **counter-evidence to E01's "larger groups (P-384) raise T_q" defence** → a debate item; (3) supports N1's argument that waiting for demonstrations is unsafe; (4) "quantum-safe default settings" ↔ N1's platform-default finding (B04/B05).

### F07 Cain, Xu, King, Picard, Levine, Endres, Preskill, Huang, Bluvstein 2026, Shor's Algorithm Is Possible with as Few as 10,000 Reconfigurable Atomic Qubits (arXiv 2603.28627; Oratomic / Caltech / UC Berkeley)
- **Type:** architecture + resource estimate for **neutral-atom** fault-tolerant QC using high-rate qLDPC-style codes (~30% encoding rate, ≳1,000 logical qubits per block) with reconfigurable non-local connectivity; 1 ms stabiliser cycle; reuses published circuits (Gidney 2025 for RSA; Babbush et al. 2026 [F06] for ECC-256).
- **Headline:** Shor at cryptographic scale with **~10,000 physical qubits**; ECC-256 (P-256): space-efficient 9,739 qubits ≈ 1,000 days; balanced 11,961 qubits ≈ 260 days; time-efficient ≈ 19,000 qubits ≈ 52 days and **≈ 26,000 qubits ≈ 10 days**; RSA-2048: 11,033–13,255 qubits ≈ 10⁴ days, parallelised ≈ 102,000 qubits ≈ 97 days (RSA 1–2 orders slower than ECC due to depth). Claims 10× fewer qubits than small-block qLDPC architectures and 100× fewer than planar surface code.
- **Experimental anchors cited:** below-threshold universal fault-tolerant processing on up to ~500 atoms; arrays of >6,000 (6,100) coherent atoms; 360,000-trap tweezer arrays (no atoms yet); continuous reloading demonstrated.
- **Stated caveats:** "substantial engineering challenges remain"; estimates "preliminary"; slow clock (ms) → long runtimes; parallel surgery assumptions only benchmarked on ~10 PPMs; hardware speed-ups (µs readout, constant-velocity transport) could cut runtime to hours/minutes but need new work.
- **Conclusion:** "a neutral atom system capable of implementing Shor's algorithm could be constructed… underscores the importance of ongoing efforts to transition… to post-quantum standards."
- **Relevance:** the **slow-clock** counterpart to F06: very few qubits but days-to-months per key — i.e., a machine better suited to breaking a few high-value long-term keys (e.g., RSA server keys used for key transport, CA keys) than many per-session ephemeral keys. For N1 this sharpens the HNDL priority argument: **static/long-lived keys (RSA key transport, reused ECDH shares, STEKs-encrypting-tickets chains) are the first realistic targets**, whereas fresh per-session X25519 shares require one run each (E01 E-factor). Cited by E07 as "Caltech/IQIM 10,000 atoms".

### F08 Häner, Tripier, Young, Naehrig, Maksymov, Alam, Maslov, Parrott, de Sereville, Sullivan, Webster, Delfosse, Gamble, Roetteler 2026, Computing 256-bit Elliptic Curve Discrete Logarithms in 26 Days on a Fault-Tolerant Trapped-Ion Quantum Computer with 20,000 Qubits (arXiv 2609.05625; IonQ)
- **Type:** application-specific trapped-ion architecture (extension of IonQ's "Walking Cat" qLDPC architecture) with a full compiler and measurement-schedule-level depth estimates; secp256k1 target. Very long paper (~280k chars) — read Parts I–II, overview/contributions, results summaries and conclusion; circuit/compiler appendices skimmed.
- **Headline:** logical circuit ≈ **1,450 logical qubits and ~39–40 million Toffoli gates** (optimising Schrottenloher 2026's ~58M), with a rigorous success-probability lower bound (confidence ≥ 1 − 2⁻¹²⁸); physical: **≈ 19,397 trapped-ion qubits, ≈ 25.7 days, ~63% estimated success probability**. Previous trapped-ion estimates needed 1.2M–9.4M qubits. Fast CCZ factory + depth-one CCZ injection = 31× faster Toffolis.
- **Literature summary given by authors:** RSA-2048 physical-qubit estimates fell ~10⁹ (2012) → 10⁶ (2D grid) → 10⁵ (long-range connectivity); ECDLP gate counts fell from 6×10⁹ (Proos–Zalka 2003) → ~200M (Litinski 2023, single instance) → 1,462 qubits/84M (Schrottenloher 2026); space-optimised variants ~1,200 qubits, even <850 with higher Toffoli; neutral-atom <20,000 qubits (F07); superconducting <500,000 (F06). secp256k1's pseudo-Mersenne prime allows extra savings vs other curves.
- **Strengths claimed:** accounts for routing, Clifford/measurement costs, transport, leakage, loss and reloading usually ignored; conservative runtime bound.
- **Limitations (stated):** simplicity over exhaustive optimisation; loss model simplified; future work to improve runtime/footprint.
- **Relevance:** third independent 2026 estimate (with F06, F07) converging on **~10⁴–10⁵ physical qubits for slow-clock or ~5×10⁵ for fast-clock, ~10⁷–10⁸ Toffolis, ~1,200–1,450 logical qubits** for 256-bit ECDLP. For N1's synthesis: convergence across vendors (Google, Oratomic/Caltech, IonQ) is itself evidence; but all are vendor-authored projections (quality flag: industry COI, unbuilt hardware). Per-key runtime of weeks on slow-clock devices again implies early CRQCs would prioritise long-lived/high-value keys.

### F09 Luo H., Yang, Luo J., Wang, Su, Sun, Li L., Li T. 2026, Quantum Algorithm for Elliptic Curve Discrete Logarithms with Space-Efficient Point Addition (arXiv 2607.13816v3, Sep 2026; Tsinghua / Peking / Sun Yat-sen / CAS)
- **Type:** theoretical circuit-construction paper (logical level, standard circuit model); supersedes arXiv 2604.02311. Read introduction, contributions, comparison tables and overview in full; the long proof appendices (EEA step bounds, location-controlled arithmetic) skimmed.
- **Contribution:** a space-efficient reversible modular inversion (the dominant space cost in affine point addition), refining Proos–Zalka register sharing with "length registers" and location-controlled arithmetic, plus a rigorous bound on extended-Euclid step count (≤4⌈cn⌉, c = 3/log₂(2+√3)) replacing Proos–Zalka's inaccurate 4.5n.
- **Results:** ECDLP with **3n + 6⌊log₂ n⌋ + O(1) logical qubits** and 1056n³/log₂ n Toffolis; modular inversion 2n + 6log₂ n qubits, 229n² Toffolis. **secp256k1: 835 logical qubits, ~2^30.88 (~1.97×10⁹) Toffolis** vs Chevignard et al. (EUROCRYPT 2026) 1,098 qubits / 2^38.1; Babbush et al. (F06) 1,175 / 2^26.27 (space-opt.) or 1,425 / 2^25.94 (gate-opt.); Schrottenloher 2026 1,192 / 2^26.11 or 1,446 / 2^25.78. Space history: RNSL 9n → Häner 8n → CFS 3.12n + O(√n) → this 3n.
- **Trade-off:** fewer qubits but ~30× more Toffolis than F06/Schrottenloher (illustrates the space–time trade-off).
- **Limitations:** logical-level only — no error-correction, physical-qubit or runtime estimates; affine Weierstrass prime-field curves.
- **Relevance:** shows the **minimum logical machine size for breaking 256-bit ECDH keeps falling (below 1,000 logical qubits)**, i.e., the threshold for a "first" CRQC capable of attacking TLS key exchange is lower than RSA-centred surveys (E06) imply. Also an example that ECC estimates now come from multiple countries/groups (US vendors, China academia), weakening any argument that estimates are vendor hype alone.

### F10 Putranto, Wardhani, Kim 2025, Enhancing Quantum Cryptanalysis of Binary Elliptic Curves Through Optimized Out-of-Place Point Addition and ECPM Integration (IEEE Access 13, 148304; Pusan National University) [faculty-provided]
- **Type:** comparative resource-estimation framework for Shor-ECDLP over **binary fields GF(2^m)**; benchmarks published designs layer by layer — Level 1 field arithmetic (GCD-based vs Fermat's-little-theorem (FLT)-based inversion, Karatsuba multiplication, in-place vs out-of-place), Level 2/3 point addition (PA) and doubling (PD), full Shor iteration with ECPM using either (2n+2) PA (Banegas, Putranto, Jang) or 2n PD + 2 PA (Wardhani). Metrics: Toffoli, CNOT, qubits, depth, number of multi-controlled gates. Simulations with Qiskit and ETRI QCrypton for small degrees; numeric extrapolation for m = 8…571.
- **Findings:** Jang et al. lowest Toffoli/CNOT but relies on many multi-controlled gates (costly to decompose at scale); Wardhani et al. minimal depth with more qubits than Banegas; **proposed hybrid "2n PD + 2 PA_outplace"** (Jang out-of-place PA + Wardhani PD) keeps low Toffoli counts while cutting multi-controlled gate overhead → balanced space/time. Emphasises that width and depth must be co-optimised.
- **Limitations:** binary curves only; logical level (preliminary error-overhead analysis only); no physical-qubit or runtime estimate; no explicit future-work section.
- **Relevance:** binary curves (sect163k1 etc.) are **removed from TLS 1.3** and essentially absent from servers (E05: no host negotiated ec2n; but >16% of 2016 clients — mostly API/app libraries — still offered sect163 curves). For N1 the paper is mainly methodological (hierarchical resource accounting; depth vs width trade-off) and shows the faculty-linked line of work on quantum cryptanalysis circuits; it would matter only if N1 finds legacy apps still offering binary curves in ClientHellos (a checkable item in B-group ClientHello fingerprints).

### F11 Taguchi & Takayasu 2023, Concrete Quantum Cryptanalysis of Binary Elliptic Curves via Addition Chain (CT-RSA 2023, LNCS 13871, pp. 57–83; U. Tokyo / AIST) [faculty-provided]
- **Type:** logical-level resource estimate for the inversion step of Shor-ECDLP over **binary fields** (NIST degrees n = 163, 233, 283, 409, 571), improving Fermat's-little-theorem (FLT) inversion of Banegas et al. (fewer qubits) and Putranto et al. (lower depth).
- **Idea:** previous quantum FLT inversions used the fixed Itoh–Tsujii addition chain for n − 1; any addition chain works, and properties irrelevant classically (chain length, structure "d") change quantum qubit/Toffoli/depth costs → search for better chains.
- **Results:** two algorithms that weakly dominate predecessors at every degree: "basic" (vs Putranto) at n = 571 uses **74% of qubits, 93% of Toffolis, 95% of depth**; "extended" (vs Banegas) uses 93% qubits, 93% Toffolis, **82% depth**; Toffoli reductions appear for n = 409, 571; windowing (QROM) also applied.
- **Future work (stated):** full depth optimisation needs analysis of parallel quantum computation; better qubit-clearing methods.
- **Relevance:** same as F10 — binary curves are obsolete in TLS 1.3, so direct relevance to N1 is low; included because it is faculty-provided and represents the incremental-optimisation literature (small constant-factor gains per paper, which compound — cf. the F01→F06 trend). Useful in the synthesis as evidence that resource-estimate progress comes from many small algorithmic improvements, not only hardware.

### F12 Tippeconnic 2025, Breaking a 5-Bit Elliptic Curve Key Using IBM's 133-Qubit Quantum Computer ibm_torino (arXiv 2507.10592 preprint, July 2025; ASU email)
- **Claim:** a "Shor-style" circuit on IBM ibm_torino (Qiskit Runtime 2.0, June 2025): 15 qubits (10 logical + 5 ancilla), order-32 subgroup, 16,384 shots, **circuit depth 67,428, 106,455 gates, 54 s runtime**; correct key k = 7 appears **in the top 100** (a, b) results (3 times: counts 54, 41, 32) — not the top result (k = 0 and 24 dominate).
- **Quality flags (mine, important):** (1) the "elliptic curve" is abstracted to **index arithmetic mod 32** — points mapped to integers, group law = modular addition, scalar multiples precomputed classically, oracle built from 32×32 permutation unitaries — so no elliptic-curve arithmetic is executed (the hard part of real Shor-ECDLP); (2) with only 32 candidate keys, "k in the top 100 of 1,024 (a,b) pairs" is weak evidence — a near-uniform noisy distribution would also contain k = 7; no statistical test against noise; (3) depth 67k on NISQ hardware far exceeds coherence, so output is likely dominated by noise; (4) not peer reviewed; claims of "dictionary-style attacks" and "Shor continues to scale" are unsupported.
- **Relevance:** cited only as an example of **demonstration claims that do not measure progress toward a CRQC** — consistent with F06's warning that small-curve demonstrations are poor early-warning indicators and with F13's careful "challenge ladder" design. N1 should not use such demonstrations in threat timelines.

### F13 Dallaire-Demers, Doyle, Foo 2025/2026, Brace for Impact: ECDLP Challenges for Quantum Cryptanalysis (arXiv 2508.14011v2, Mar 2026; Pauli Group)
- **Contribution:** a reproducible, difficulty-graded **"challenge ladder"** of secp256k1-shaped curves (y² = x³ + 7 mod p) from 6 to 256 bits, with prime group orders and nothing-up-my-sleeve points (no pre-chosen secret) — a public "ruler" for fault-tolerant progress; classical calibration vs Pollard-rho records (Θ(2^(b/2)) unchanged); quantum costing mapped to surface code, repetition-cat and LDPC-cat codes.
- **Rationale:** Certicom ECC challenges too sparse; "Bitcoin puzzles" restrict the secret to an interval (map to kangaroo, not Shor). "No group has yet run Shor's ECDLP end-to-end on a prime field."
- **Resource ranges for 256-bit:** conservative surface code → millions of qubits, multi-day; aggressive surface code → sub-million, hours; repetition cat code ~1.26×10⁵ cat qubits, ~9 h (Gouzien et al.); LDPC cat code <4×10⁴ cat qubits. 6-bit rung: <few hundred logical qubits, seconds — first end-to-end FTQC demonstration target.
- **Timeline claim:** overlaying costs with public roadmaps → **first plausible window for a 256-bit break ≈ 2027–2033** "with wide error bars"; dots are "order-of-magnitude waypoints, not promises".
- **Discussion/recommendations:** "the shift from dozens to thousands of logical qubits within a short horizon is the relevant threshold for ECC"; prudent to finish PQ upgrades before devices reach the 160–256-bit rungs; hybrid signatures and commit-then-upgrade migration for Bitcoin (BIP 360 P2QRH).
- **Debate note:** F06 (Babbush et al. 2026) explicitly argues such ladders "may fail to provide a reliable early warning" because progress is threshold-like and advanced capabilities may not be published; F13 itself concedes canaries are "imperfect, because disclosures depend on what teams publish and because FTQC progress can arrive abruptly". Its 2027–2033 window is earlier than E06's expert median.
- **Relevance:** gives N1 (i) a principled way to talk about "early warning" and why HNDL-motivated migration cannot wait for demonstrations; (ii) a contrast case with F12's weak demo; (iii) another independent ECC-256 timeline input for the Mosca analysis.

### G01 Grassl, Langenberg, Roetteler, Steinwandt 2016, Applying Grover's Algorithm to AES: Quantum Resource Estimates (PQCrypto 2016; arXiv 1512.04965)
- **Type:** first full logical-level reversible implementation of AES-128/192/256 for Grover key search (Clifford+T; Toffoli = 7 T); r = 3/4/5 plaintext–ciphertext pairs to make the key unique; only SubBytes (S-box, GF(2⁸) inversion) needs T gates; key expansion a large share of per-iteration cost; no connectivity constraints, no error-correction overhead.
- **AES circuits (Tables 2–4):** AES-128 1,060,864 T gates, T-depth 50,688, 984 qubits; AES-192 1,204,224 T, 1,112 qubits; AES-256 1,505,280 T, 1,336 qubits.
- **Full Grover (Table 5):** **AES-128: 1.19·2⁸⁶ T gates, T-depth 1.06·2⁸⁰, 2,953 logical qubits**; AES-192: 1.81·2¹¹⁸ T, 4,449 qubits; AES-256: 1.41·2¹⁵¹ T, T-depth 1.44·2¹⁴⁴, 6,681 qubits. Qubits modest (3,000–7,000) but **depth is the obstacle** — "challenging to implement… due to the large circuit depth… the serial nature of Grover's algorithm".
- **Conclusion:** "it seems prudent to move away from 128-bit keys when expecting the availability of at least a moderate size quantum computer." Future work: fixed-point Grover, quantum linear/differential cryptanalysis.
- **Relevance:** baseline for the AES-128 Grover cost relevant to (a) TLS record keys (AES-128-GCM is the dominant TLS 1.3 suite: A07 79.2%) and (b) STEKs (AES-128-CBC in BoringSSL/Apache per E03). Key point for N1: **one Grover search ≈ 2⁸⁶ T gates at depth ~2⁸⁰ — not comparable to the ~10⁸–10¹⁰ gates of an ECDH break**, so in HNDL the realistic quantum route is always the key exchange, not the symmetric layer. Note the conclusion's "move away from 128-bit keys" is the source of the naive framing later contested by G02 (MAXDEPTH costing).

### G02 Jaques, Naehrig, Roetteler, Virdia 2020, Implementing Grover Oracles for Quantum Key Search on AES and LowMC (EUROCRYPT 2020; arXiv 1910.01700; Oxford / Microsoft / Royal Holloway)
- **Type:** Q# implementations (unit-tested, automatic resource estimation) of full Grover oracles for AES-128/192/256 and LowMC (Picnic); optimises **depth** (and depth×width) rather than qubit count, because Grover parallelises badly.
- **Key concept — NIST MAXDEPTH:** NIST's PQC call bounds total attack circuit depth (2⁴⁰ … 2⁹⁶; 2⁹⁶ ≈ gates atomic-scale qubits at light-speed could do in a millennium). Exceeding depth forces parallelisation: splitting the search across S machines costs ~√S more total work, so total gates ≈ G·D/MAXDEPTH (NIST formula from GLRS16).
- **Results:** AES-128 key search without depth limit **G-cost 1.34·2⁸³ gates, DW-cost 1.75·2⁸⁶ qubit-cycles**; **with MAXDEPTH = 2⁴⁰ → 1.07·2¹¹⁷ gates (×~2³⁴); 2⁶⁴ → 1.07·2⁹³; 2⁹⁶ → no parallelisation needed**. Table 12 vs NIST: Cat 1 (AES-128) NIST 2¹³⁰/2¹⁰⁶/2⁷⁴ vs this work 2¹¹⁷/2⁹³/2⁸³ at MAXDEPTH 2⁴⁰/2⁶⁴/2⁹⁶; Cat 3 (AES-192) 2¹⁸¹/2¹⁵⁷/2¹²⁶; Cat 5 (AES-256) 2²⁴⁵/2²²¹/2¹⁹⁰ → **consistent 11–13-bit reduction vs NIST's estimates** (AES slightly less quantum-secure than NIST's table, but still astronomically expensive); fewer plaintext–ciphertext pairs needed under parallelisation. Most shallow AES circuit to date (S-box à la Boyar–Peralta/Langenberg et al.).
- **Implications:** NIST categories are defined by AES key-search cost; lowering them makes it easier for PQC submissions to claim categories (except Cat 1 at MAXDEPTH 2⁹⁶). LowMC instances slightly below original NIST Cat-1 gate bound.
- **Future work (stated):** other cost metrics/constraints; **quantum multi-target attacks (e.g., Banegas–Bernstein) under MAXDEPTH left open**; further compiler optimisation.
- **Relevance:** this is the paper that **refutes the naive "AES-128 = 64-bit security" framing** used by A02, A05, A09 (and implicitly G01's conclusion and E07's AES remarks): under any realistic depth limit, AES-128 key search costs ~2⁹³–2¹¹⁷ gates. For N1: (a) record keys (AES-128-GCM) and STEKs are not the HNDL weak point; (b) the multi-target question (one Grover run covering many keys, e.g., many sessions or tickets) is explicitly unresolved — N1 should note it as open rather than claim amortisation for Grover. Anchors the "Grover-on-STEK is not cheap" side of N1's M2 discussion.

### G03 Chen H.-N., Cai, Gao, Lin 2025, Quantum Circuit for Implementing AES S-box with Low Costs (arXiv 2503.06097v2; Fujian Normal U. / BUPT) [faculty-provided]
- **Method:** AES S-box via composite field F((2⁴)²) instead of F(2⁸): GF(2⁸) inversion decomposed into F(2⁴) operations; fewer CNOTs in linear maps, lower T-depth in inversion and multiplication, narrower circuits; linear key schedule; full AES-128/192/256 circuits.
- **Results:** **AES-128 circuit width × T-depth DW(T) = 102,800 (1,028 qubits × T-depth 100)** — lowest reported (vs 128,640 [1,608 q, T-depth 80], 147,560, 334,560, and Grassl-style 7,549,440 [256 q, T-depth 29,490]); 20.09% lower DW(T) than the best prior at equal T-depth. AES-192 best DW(T) ≈ 138,720; AES-256 ≈ 179,760 (e.g., 1,284 q, T-depth 140, ~72.6k T).
- **Limitations:** oracle/circuit-level only — no full Grover cost or MAXDEPTH analysis; no future-work section.
- **Relevance:** incremental optimisation of the AES oracle (the inner loop of Grover). Even with the cheapest known oracle, a full Grover key search still requires ~2⁶⁴ sequential iterations for AES-128 (and far more under MAXDEPTH, G02). For N1, it supports the conclusion that improved oracles shave constants but **do not change the practical safety of AES-128 record/ticket keys relative to the ECDH key exchange**.

### G04 Wang Z., Zheng M., Wu, Wen, Wei, Long 2025, Reducing Quantum Resources for Attacking S-AES on Quantum Devices (npj Quantum Information 11:157; BAQIS / Tsinghua) [faculty-provided]
- **Scope:** **Simplified AES (S-AES, 16-bit key/block)** as a toy model: Grover oracle optimised from 160 to **120 Toffolis (32 qubits)** by refining SubNibble; proposes a Variational Quantum Attack Algorithm (VQAA) that avoids implementing the cipher as a quantum circuit; runs components on IBM superconducting hardware (XOR, MixColumn, SubNibble inverse, 3 × 10,000 shots).
- **Findings:** demonstrates feasibility of running small cryptanalytic subcircuits on current hardware; **VQAA training is hard** — random initial parameters rarely reach the target; attributes difficulty to ansatz design unrelated to S-AES structure ("constructing an efficient ansatz based on the structure of S-AES" is the key issue). Notes full AES oracles need ~10⁵ logical gates × ~2⁶⁴ iterations — "significant challenges remain in achieving quantum attacks on AES."
- **Relevance:** NISQ demonstrations on toy ciphers do not scale to AES; consistent with E07's finding that variational methods (barren plateaus) provide no route to breaking standard ciphers. Supports N1's position that symmetric TLS components are not near-term quantum targets.

### G05 Mandal, Anand, Rahman, Sarkar, Isobe 2024, Implementing Grover's on AES-based AEAD Schemes (Scientific Reports 14:21105; IIT Madras / U. Hyogo) [faculty-provided]
- **Scope:** first Grover key-search cost estimates (Qiskit circuits, T-depth-optimised) for AES-round-based AEADs **Rocca-S (256-bit key; 6G candidate), AEGIS-128 and Tiaoxin-346** under NIST MAXDEPTH (2⁴⁰/2⁶⁴/2⁹⁶), gate-count and depth×width metrics, following G02's parallelisation method.
- **Results (Table 14):** MAXDEPTH 2⁴⁰ G-cost: **Rocca-S 1.09·2²⁵³, AEGIS-128 1.14·2¹²⁴, Tiaoxin-346 1.22·2¹²⁴**; 2⁶⁴: 2²²⁹ / 2¹⁰⁰ / 2¹⁰⁰; 2⁹⁶ (no parallelisation): 2¹⁹⁷ / 2⁸⁶ / 2⁸⁷; G-cost×D: 1.08·2²⁹⁴ / 1.14·2¹⁶⁴ / 1.22·2¹⁶⁴. Compared against **original NIST thresholds (2¹³⁰/2¹⁰⁶/2⁷⁴ for Cat 1) and NIST's updated thresholds ("NISTup": 2¹¹⁷/2⁹³/2⁸⁴, from G02)** → all three meet the updated NIST bounds → "secure against quantum adversaries when considering Grover's."
- **Relevance:** demonstrates the **MAXDEPTH-aware costing methodology** that N1 should adopt for any symmetric-key discussion (vs the naive k/2 rule of A02/A05/A09); also shows NIST already **lowered** its Category-1 gate thresholds following G02 — a concrete example of the literature correcting itself.

### G06 Ulgen, Cildiroglu, Yayla 2026, Quantum Circuit Realization and Grover Cryptanalysis of the Hybrid ARX-SPN Cipher GFSPX (Physica Scripta 101, 285103; METU / Ankara U. / Siirt U.) [faculty-provided]
- **Scope:** lightweight block cipher GFSPX (64-bit block, 128-bit key; 4-branch generalised Feistel mixing ARX and SPN); qubit-optimised quantum implementation exploiting Feistel reversibility and a compact ripple-carry adder for modular additions.
- **Results:** **209 qubits, quantum cost 32,498, depth 7,617**; parallelised Grover oracle with 3 plaintext–ciphertext pairs; total key-recovery cost **1.12·2¹⁵⁹ gates**, below NIST Level-1 threshold 2¹⁷⁰ (the 2¹⁷⁰/MAXDEPTH formula) → "does not satisfy NIST's post-quantum requirements for a 128-bit key", but more Grover-resistant than pure-SPN lightweight ciphers because modular addition is costly in quantum circuits.
- **Future work:** 192/256-bit key variants; depth- or T-count-reduced adders.
- **Relevance:** limited for TLS (lightweight IoT cipher, not in TLS); illustrates the NIST-threshold methodology and that a "below Level 1" verdict still means ~2¹⁵⁹ gates — i.e., verdicts about "quantum insecurity" of 128-bit symmetric keys are relative to a policy threshold, not practical feasibility. Useful nuance for the AES-128 debate in N1.

### G07 Bernstein 2009, Cost Analysis of Hash Collisions: Will Quantum Computers Make SHARCS Obsolete? (SHARCS 2009; UIC) [faculty-provided]
- **Argument:** cost must be measured as **price-performance (machine size × time) with realistic 2-D communication costs**, not query counts. Shor makes NFS factoring hardware obsolete; Grover beats classical brute-force preimage search for large b; but for **hash collisions, the Brassard–Høyer–Tapp (BHT) "2^(b/3)" claim rests on a "nonsensical notion of cost"**: its table lookups cost M^(1/2) per access in a realistic mesh, cancelling the speed-up. Best quantum collision time 2^(b/2)/M^(1/2) on a size-M machine is worse than classical parallel rho (van Oorschot–Wiener 1994) at 2^(b/2)/M; classical machines of size 2^(b/6) already reach 2^(b/3). "Anyone afraid of quantum hash-collision algorithms already has much more to fear from non-quantum hash-collision algorithms."
- **Relevance (methodological anchor for N1's M2 "price per session"):** the paper establishes the **cost-accounting discipline** (area × time, communication, parallelism) that later underlies NIST MAXDEPTH reasoning (G02) and that N1 applies to amortisation: an attack's real cost is machine-time per unit of value obtained, not asymptotic query count. It also explains why SHA-256 transcript hashes/HKDF in TLS are not quantum weak points.

### H01 Näther, Herzinger, Gazdag, Steghöfer, Daum, Loebenberger 2024, Migrating Software Systems Towards Post-Quantum Cryptography — A Systematic Literature Review (IEEE Access / arXiv 2404.12854v2; Xitaso / genua / Fraunhofer AISEC)
- **Method:** PRISMA 2020 + Kitchenham SLR; ACM, IEEE, Springer, Google Scholar, ePrint, ETSI, TNO, OQS + 25 CORE-ranked conferences (2012–2024); 51,605 hits → 2,987 → 2,529 → 42 → snowballing 63 → 50 → **21 papers** (academic + grey literature, English only); thematic coding; RQ1 migration steps/roles, RQ2 how PQC is applied, RQ3 challenges.
- **RQ1:** four phases — **Diagnosis** (asset identification, risk assessment, cryptographic identification, cryptographic assessment), **Planning** (cryptographic prioritisation, migration plan), **Execution**, **Maintenance**; four role archetypes; terminology and steps inconsistent across literature; Diagnosis most documented but **the cryptographic inventory is ill-defined** ("serious research gap"); ETSI uniquely plans for failure/disorderly transition and isolation of unmigratable assets.
- **RQ2:** only **10 of 21** papers describe an actual migration (Nginx, IBM Db2, PostgreSQL, IoT ecosystem, ROS, Hyperledger Fabric/PQFabric, Delta Chat, CA, Kafka, IBE); 6 claim hybrid solutions (hybrid certificates, signatures, key establishment), 3 recommend hybrids, 6 mention, ~1/3 never mention hybrids; "Hybrid AND" vs "Hybrid OR" (TNO handbook). Weller & van der Gaag failed to integrate Wildfly-OpenSSL/Bouncy Castle PQC into microservices.
- **RQ3 challenges:** organisational (education/expertise; time, effort & cost — most frequent, 9/21; sceptics); PQC itself (hardware requirements, performance/availability, **security concerns incl. downgrade attacks to classical algorithms** [Muller & van Heesch; von Nethen], incomplete libraries/APIs/documentation); code & documentation (huge legacy code bases — Db2 tens of millions of LoC; DES kept for old clients; hard-coded crypto parameters).
- **Discussion takeaways:** (1) lack of maturity in PQC implementations ("most… experimental"); (2) no established migration framework (trial-and-error practice; no real migration reported role allocation); (3) cryptographic inventory lacks concept and tooling (Cryptosense: manual review, static scan, runtime tracing; testssl.sh, ssh_scan, ike-scan; SBOM/CBOM); (4) sparse PQC adoption, expected to accelerate after NIST FIPS (2024). Crypto-agility deliberately excluded for lack of a uniform definition.
- **Threats to validity:** small final set (21); no quality assessment; English only.
- **Relevance:** **no mobile apps, no finance sector, no developing countries** in the migration literature (zero hits for "mobile/Android/bank/finance" in the text) — supports N1's population gap. N1's measurement (which app endpoints/clients negotiate hybrid) is effectively an **external "cryptographic identification/assessment" (Diagnosis-phase) instrument** that organisations and regulators lack; the downgrade concern maps to N1's fallback measurement.

### H02 Näther, Herzinger, Steghöfer, Gazdag, Hirsch, Loebenberger 2024/2026, Toward a Common Understanding of Cryptographic Agility — A Systematic Review (IEEE Access; arXiv 2411.08781v3, Aug 2026; Xitaso / genua / OTH Amberg-Weiden / Fraunhofer AISEC)
- **Method:** PRISMA 2020 systematic review; 84 screened, **48 included (24 peer-reviewed, 24 grey)**; authors from academia 29, industry 31, standards bodies 8; multiple reviewers, replication package.
- **RQ1:** definitions mapped to six categories — context, mode (property/approach/objective), desired capabilities, quality attributes, cryptographic entities, drivers → **no consensus**; authors pick ad-hoc definitions; agility conflated with versatility and interoperability.
- **RQ2 literature-based definition:** "a theoretical or practical approach, objective, or property which provides capabilities for setting up, identifying, and modifying encryption methods and keying material in a flexible and efficient way while preserving business continuity."
- **RQ3 context-independent definition:** **"Cryptographic Agility represents the changeability of cryptographic entities"** (a *property*, not an objective; PQC migration is the one-time *objective*).
- **RQ4 layer model:** primitive → algorithm → library → application → platform → OS → device → IT infrastructure → organisation, grouped into conceptual, software, hardware, organisational domains (17 contexts); outer layers are enabled *and constrained* by inner ones. Defines **cryptographic interoperability** = ability to communicate securely using several mechanisms at the same time (distinct from agility); versatility relevant to hardware.
- **Exemplars:** **OpenSSL** (3.0 provider architecture + EVP API + runtime config; PQC since 3.5.0; constraints: legacy low-level API use, **no centralised cross-application policy**, trust in loaded providers); **NGINX** (backend fixed at compile time, TLS settings hot-reloadable via nginx.conf); GitLab CI/CD (NGINX TLS termination + GitLab Shell SSH).
- **Discussion:** maximal interoperability enlarges attack surface and prolongs deprecated algorithms; **coexistence periods raise downgrade risk "if negotiation and fallback behavior are not carefully controlled"**; PQC migration often requires *intentionally reducing* interoperability; agility cannot be universally quantified (CAMM maturity model, Mehrez & Omri property sets are orientation only) — assess relative to context.
- **Future work (stated):** empirical validation beyond software (hardware, organisational), cross-domain case studies, context-specific assessment approaches.
- **Relevance:** gives N1 precise vocabulary: Android apps sit at the **application layer on top of platform/OS libraries (Conscrypt/BoringSSL)** — their PQ status is constrained by inner layers (B04: 84% use OS default TLS) unless they bundle their own library (A07's "only large companies' own stacks"). N1's measured outcome (hybrid offered or not) is an *interoperability* observation, while the platform-update vs app-bundled distinction is an *agility* observation (cf. E08 rotation time). The downgrade-during-coexistence concern again motivates N1's fallback measurement.

### H03 Li F., Durumeric, Czyz, Karami, Bailey, McCoy, Savage, Paxson 2016, You've Got Vulnerability: Exploring Effective Vulnerability Notifications (USENIX Security 2016; UC Berkeley / Michigan / UIUC / GMU / NYU / UCSD / ICSI)
- **Design:** randomised controlled notification experiments for three vulnerability classes: publicly accessible **industrial control systems** (45,770 hosts; 2,563 WHOIS abuse contacts), **misconfigured IPv6 firewalls** (180,611 hosts; 3,536 contacts; no true control — pre-notification scans used), **DDoS amplifiers** (83,846 hosts; 5,960 contacts; NTP/DNS/Chargen). Variables: who to contact (WHOIS abuse vs national CERTs vs US-CERT), verbosity (terse / terse+link / verbose), language (native translations for Germany, Netherlands, Poland, Russia); daily rescans for weeks; permutation tests with Bonferroni correction.
- **Results:** **best regimen = verbose message sent directly to WHOIS abuse contacts → +11% of contacts remediated vs control** (statistically significant for ICS and IPv6; p < 0.0001 mostly); verbose ~56% more effective than terse after 2 days (difference fades, not significant after correction); only 16.8% clicked the info link and ≤40% of visitors patched; **national CERTs modest or no effect; US-CERT indistinguishable from control** (apparently did not forward); 17% of IPv6, 8% of ICS, 19% of amplifier hosts were in countries **without a CERT** (many in Africa, Central America, small island states); **translated messages performed worse** than English (recipients suspected phishing); **no notification had a significant effect on DDoS amplifiers**; effects short-lived (action within first couple of days or never); **repeat notifications did not help**; remediation often partial.
- **Responses:** 685 emails — 77% automated, 9% bounces, 14% human (93); 96% of human replies positive or neutral; 85.9–92.8% of contacts never replied; 57 survey responses.
- **Discussion/future work:** reasons for non-remediation (wrong contact, lack of education about significance or remediation, logistical hurdles, cost–benefit) left for future work; need standard security point-of-contact (WHOIS abuse is meant for abuse); better centralised mechanisms than CERTs; usable remediation tools; ethics (re-notification burden, full-disclosure threats); future abuse of notification channels (fake notifications).
- **Relevance:** N1 plans to disclose findings (e.g., classical-only endpoints, legacy features) to Bangladeshi operators and regulators. Evidence base: direct, detailed notices beat CERT relays; expect low response (B08 Okara: 726 emails, 0 replies); time-limited effect; language localisation not necessarily helpful; for countries where national CERT effectiveness is unknown (Bangladesh's BGD e-GOV CIRT / bank sector CIRT), notification efficacy is itself an open research question. Supports N1's plan to combine private operator disclosure with regulator-level recommendations (H-group gap: no study of notification efficacy in South Asia or for PQ-readiness issues, which are "not a vulnerability yet").
