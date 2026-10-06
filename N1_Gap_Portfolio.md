# N1 Gap Portfolio: "The Post-Quantum App Gap" (summary)

> **This is the short overview.** The **master file** with full steps, commands, data formats, gates and writing guidance is **`N1_Implementation_Plan.md`**. If the two ever disagree, the plan wins.
> **Why a portfolio?** Projects die when (a) someone already did it, (b) the gap is narrower than expected, or (c) the expected result doesn't appear. A rich topic with **many related gaps** means every outcome, including negative ones, becomes a finding.
> **Contents:** 1 umbrella question · 4 pillars · **15 gaps** · 5 opportunistic gaps · a decision tree · a paper plan. Facts were checked on 30 Sept 2026; **(verify)** marks things your experiments must confirm.

---

## 1. Why this topic is "prosperous" (the evidence)

| # | Fact | Source |
|---|---|---|
| 1 | **iOS 26 (Sept 2025) advertises hybrid X25519MLKEM768 by default** in URLSession / Network.framework, so iPhone apps got protection for free. Apple warns that legacy servers that can't read large ClientHellos may break. | [Apple 122756](https://support.apple.com/en-us/122756), [WWDC25-314](https://developer.apple.com/videos/play/wwdc2025/314/) |
| 2 | **Android 17's post-quantum work covers Keystore, Verified Boot, Attestation and Play App Signing, with no mention of TLS or app networking.** | [Google blog, Mar 2026](https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/) |
| 3 | Conscrypt's post-quantum named-group support "**only works on Java and not on Android**" (PR #1452, merged Jan 2026). WebView-based apps benefit via Chrome. | [conscrypt#1452](https://github.com/google/conscrypt/issues/1452), [Gadget Hacks](https://android.gadgethacks.com/news/android-17-quantum-safe-security-whats-protected-and-whats-not/) |
| 4 | **Flutter/Dart (3.13) reportedly doesn't offer X25519MLKEM768 by default**, on Android *and* iOS. This is based on source review, not measurement **(verify)**, so your lab would be the first empirical check. | [quantum-bank PR #8](https://github.com/joaobsjunior/quantum-bank/pull/8) |
| 5 | **Bangladesh: 91.2% Android, 8.7% iOS** (Aug 2026). The top Android versions are 13, 15, 11, 12, 16 and 14. | [StatCounter](https://gs.statcounter.com/os-market-share/mobile/bangladesh) |
| 6 | **The best 2026 post-quantum TLS measurement (IMC 2026) explicitly excluded mobile apps and custom API endpoints**, and used only cloud vantage points. Finance ~59%, government ~38% of domains support post-quantum. | [Mind the Gap](https://arxiv.org/html/2607.29005v1) |
| 7 | **Harvest-now-decrypt-later is cheap:** harvesting 1% of global traffic costs about $1.1B/year. PSK-only or 0-RTT resumption inherits the original handshake's weakness. | [Blanco-Romero et al. 2026](https://arxiv.org/abs/2603.01091) |
| 8 | **Our measurement:** www.bb.org.bd (its own network, **AS139616**) accepts only **X25519 + AES-128-GCM**; Cloudflare, Google and Apple negotiate **X25519MLKEM768 + AES-256-GCM**. | `n1_tools.py`, `f2_starter.py` |

**Put together:** *whether a person's financial traffic is protected against future quantum decryption is decided by their phone's platform and their app's framework, not by them.* In a 91%-Android country that has consequences (a **"post-quantum platform divide"**), and nobody has measured it for apps.

**Supporting context:**
- Chrome delayed post-quantum on Android until Nov 2024 because of slow mobile connections.
- Only 3.7% of origins behind Cloudflare are post-quantum ([Cloudflare 2025](https://blog.cloudflare.com/pq-2025/)).
- Pinning is most common in finance apps, mostly of CA keys ([IMC 2022](https://dl.acm.org/doi/10.1145/3517745.3561439)).

**Link to your faculty's guidance:** N1 measures whether the **defense against Shor** (hybrid ML-KEM replacing elliptic-curve X25519) reaches app users (the faculty's "RSA/ECC threat is real"). G15 adds the **Grover view** (AES-128 vs AES-256).

---

## 2. The umbrella question and its four pillars

> **Umbrella RQ:** *Who and what decides whether a mobile-first population's app traffic is protected against harvest-now-decrypt-later, how large is the resulting gap in Bangladesh, and what would close it?*

```
                              UMBRELLA QUESTION
   ┌──────────────┬────────────────────┬─────────────────────┬──────────────────────┐
   P1 CLIENT       P2 ECOSYSTEM          P3 INFRASTRUCTURE      P4 CLOSING THE GAP
   "Who decides    "How exposed is       "What blocks on the    "What does fixing cost,
    on the phone?"  BD traffic really?"   server/network side?"  what makes providers fix?"
   G1 G2 G3        G4 G5 G6 G7 G15       G8 G9 G10              G11 G12 G13 G14
```

**An app's communication stack, and where each gap sits:**
```
User
 └─ App code ── app-layer crypto (RSA-encrypted PIN? JWE?) ............ G6
     └─ Networking framework (OkHttp / Flutter / RN / Cronet / WebView) . G1, G3
         └─ OS TLS (Android Conscrypt / iOS Network.framework) ......... G1, G3
             └─ Device ecosystem (OS version, WebView & Play updates) .. G2
 └─ Third-party SDKs (analytics, ads, crash, maps), their own stacks ... G5
Session details (cipher: AES-128 vs AES-256; resumption psk_ke) ........ G15
Network path (mobile operator / ISP / enterprise middleboxes) ........... G10
Server edge (CDN / cloud / API gateway / own network) ................... G8, G9
Data value (short-lived ping vs. NID + selfie from e-KYC) ............... G7
```

---

## 3. The 15 gaps (each one alone is publishable; they share data)

"Phase" refers to `N1_Implementation_Plan.md`, Part C. **If yes / if no** = what each outcome means, so neither is a dead end.

| ID | Gap | Research question (short) | Method | Phase | Effort (person-weeks) | If yes / if no |
|---|---|---|---|---|---|---|
| **G1** ⭐ | Framework default matrix | Which Android/iOS stacks offer X25519MLKEM768 by default, on which OS versions? | Test apps read `kex=` from `cloudflare.com/cdn-cgi/trace` | 2 | 4–5 | Many: developer guidance. Few: "Google's recommended stacks leave apps unprotected". |
| **G2** | Update lag and device ecosystem | What share of real phones run post-quantum-capable browsers/WebViews? | Trace-page survey (paste `uag=` + `kex=`; IRB) + StatCounter | 7 | 3 | Mostly updated: framework choice matters. Not: a hidden update divide. |
| **G3** ⭐⭐ | **Platform divide** | For the same apps, does protection differ between iOS and Android, and do OS defaults or frameworks explain it? | Hotspot capture of about 20 app pairs | 2 + 3 | 3–4 | A divide: policy headline. None: "frameworks equalize". |
| **G4** (core) | Bangladesh app 2×2 + layer attribution | What fraction of first-party app connections negotiate post-quantum, and which layer decides? | Captures + lab + server probes; `n1_tools.py analyze` | 3–5 | backbone | Any result is the baseline finding |
| **G5** | Third-party SDK layer | Do SDK connections lead or lag the app's own traffic? | Label SNIs in captures | 8 | 1–2 | Lead: "the bank's API is the weak link". Lag: "side doors". |
| **G6** | App-layer crypto on top of TLS | How often is RSA/ECC used *inside* finance apps, and does it change effective protection? | `n1_tools.py apk` signals + jadx | 4 | 3 | RSA: two layers to migrate. Symmetric: a safety net. |
| **G7** | Exposure weighted by data lifetime | Are long-lived flows (e-KYC, identity, statements) better or worse protected? | Session-step log → `flow_step` labels; resumption modes | 3 + 8 | 2–3 | Either way it gives the policy weight |
| **G8** | API gap + hosting | Do app API hosts lag the same organization's website? Does hosting explain it? | `f2_starter.py` pairs + Team Cymru ASN lookup | 5 | 2 | Lag: "web studies overestimate readiness". Lead: modern clouds. |
| **G9** | Pinning as a migration blocker | Which finance apps pin what (CA or leaf, RSA or ECDSA), and would post-quantum or Merkle Tree certificates break them? | apktool → NSC `<pin-set>`, SPKI regex, crt.sh | 4 | 2–3 | Few pin: reassuring. Many leaf pins: a hazard list. |
| **G10** | Network path | Do Bangladeshi operators' paths break or slow post-quantum app handshakes? | Re-capture 10 apps on 4 operators; timing | 6 | 2 | Failures are actionable; none is evidence of readiness |
| **G11** | Cost on Bangladeshi networks | Latency, data and battery cost of post-quantum here? (today: +12 ms median, n = 15) | `n1_tools.py timing`; OkHttp vs Cronet app | 6 | 2–3 | Real numbers either way (supporting) |
| **G12** | Static → dynamic prediction at scale | Do APK features predict measured behavior? | Classifier → AndroZoo scan | stretch | 5–6 | Yes: a scalable method. No: runtime dominates. |
| **G13** | Notification experiment | Does notification plus a fix guide speed up adoption in 3–6 months? | Notify (random halves) → re-measure | 9 | 2 + waiting | Both outcomes are publishable |
| **G14** | Human layer | What do Bangladeshi fintech developers and bank teams know, and what blocks them? | Survey (30–60) + interviews (8–12); IRB | 9 (optional) | 5–6 | Any blocker pattern explains the "why" |
| **G15** | Grover view + resumption | Do app sessions use AES-256 (CNSA 2.0 level) or AES-128? Do resumptions use `psk_ke` (inherits exposure)? | `cipher_suite`, `psk_modes` columns (already in the tool) | 8 | 1 | Links N1 to the faculty's AES-256 point |

---

## 4. Opportunistic gaps (record a baseline now; see Plan Phase 0)

| ID | If this happens… | …then you get |
|---|---|---|
| **O1** | Google ships post-quantum in Conscrypt (Android 17/18 or Mainline) | A before/after **natural experiment** on how fast it reaches old devices |
| **O2** | Flutter/Dart enables X25519MLKEM768 | **Diffusion time** into Bangladeshi Flutter apps |
| **O3** | Chrome ships post-quantum for WebRTC (listed for about Chrome 157) | Calls in WebView apps, before vs after |
| **O4** | Post-quantum or Merkle Tree certificates go live (2026–27) | G9's pinning-breakage predictions become testable |
| **O5** | A global app study appears | Keep Bangladesh + G3 same-app pairs + G7 + G13 + G14 |

---

## 5. Decision tree (decide at week 6 and again at week 12; Plan Part D)

```
A. Most apps UNPROTECTED because of the framework/OS   → Lead: G1 + G3 platform divide; add G11, G13.
B. Most apps PROTECTED (WebView/Cronet/CDNs)            → Lead: "partial protection": G5, G6, G7, G2, G15.
C. SERVER is the bottleneck (apps offer, APIs decline) → Lead: G8 API gap + hosting, G9, G13 to banks.
D. Capture blocked                                      → Lead: G1/G3 lab + static G6/G9/G12.
E. Scooped by a global app study                        → Lead: Bangladesh + G3 pairs, G7, G13, G14.
```

**Negative results are findings:**

| If you find… | You write… |
|---|---|
| Cronet via Play Services lacks post-quantum | "Google's recommended app network stack lacks the protection Google's browser has" |
| No Bangladeshi app offers post-quantum | "A mobile-first financial sector with zero app-level post-quantum protection: which layer blocks it" |
| Pinning is rare | "Pinning won't block the post-quantum certificate migration in this sector" |
| Static features don't predict behavior | "Runtime configuration dominates; dynamic measurement is essential" |
| Notifications changed nothing | "Awareness isn't the bottleneck; platform or regulator action is" |
| No iOS/Android difference | "Frameworks neutralize OS defaults" |

**Minimum viable thesis:** G1 + G4 (≥ 25 apps) + one of {G3, G8, G9}.

---

## 6. Papers and thesis (Plan Part G)

| Output | Gaps | Target (examples) | When |
|---|---|---|---|
| **arXiv note** (claim stake) | G1 (+ early G3) | arXiv → workshop | Week 6 |
| **Paper A: "The Post-Quantum Platform Divide"** | G1 + G2 + G3 (+ G15) | ACM WiSec, PETS, *Computers & Security* | Weeks 18–20 |
| **Paper B: "The App Gap in a Mobile-First Financial Sector"** | G4–G9 (+ G11) | *Computers & Security*, *JISA*, *IEEE Access* | Weeks 22–26 |
| **Paper C (optional)** | G13 + G14 | USEC/SOUPS, *Computers & Security* | Month 9+ |
| **Thesis** | Umbrella question; chapters = P1–P4 | CSE499 report | Weeks 22–24 |

**What you can claim** (re-search before submitting):
- The first measurement of post-quantum key exchange **in mobile apps** of a mobile-first developing country (G4).
- The first same-app **iOS-vs-Android** comparison after iOS 26 (G3).
- The first empirical **framework default matrix** (G1).
- Evidence on whether **app API backends lag websites** (G8).
- A **data-lifetime-weighted** HNDL exposure metric (G7).

---

## 7. First 4 weeks (matches Plan Parts C and H)

| Week | Do (Plan phase) | Produces |
|---|---|---|
| 0–1 | **Phase 0:** setup, `n1_tools.py selftest`, `data/baseline.md`, faculty meeting (pitch in Plan A2), ask about IRB | Baseline + approval |
| 1–2 | **Phase 1:** pilot: Chrome control + bKash + 3 apps → **Gate 1** | The pipeline works |
| 2–4 | **Phase 2:** lab v0 → v1: HttpURLConnection, OkHttp, WebView, Flutter, React Native, Cronet on Android 10–17 emulators + real phones; iPhone if possible. **Phase 3a:** build `apps.csv`. | G1 matrix draft, first G3 pair |
| 4 | Choose the storyline (§5); outline the arXiv note; show the faculty | A direction chosen with evidence |

---

## 8. Key sources (full reading guide: Plan Part I)
- [Apple 122756](https://support.apple.com/en-us/122756) · [WWDC25-314](https://developer.apple.com/videos/play/wwdc2025/314/) · [Google: PQC in Android](https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/) · [conscrypt#1452](https://github.com/google/conscrypt/issues/1452)
- [Mankowski, Wiggers & Moonsamy, EuroS&PW 2023](https://thomwiggers.nl/publication/tls-on-android/tls-on-android.pdf) · [Pradeep et al., IMC 2022](https://dl.acm.org/doi/10.1145/3517745.3561439) · [Strauss et al. 2025](https://arxiv.org/pdf/2506.00790)
- [Mind the Gap, IMC 2026](https://arxiv.org/html/2607.29005v1) · [Dubey & Varshney 2026](https://arxiv.org/abs/2606.16473) · [Loizou & Ghadafi 2026](https://arxiv.org/abs/2608.02147)
- [Blanco-Romero et al. 2026](https://arxiv.org/abs/2603.01091) · [Cloudflare PQ 2025](https://blog.cloudflare.com/pq-2025/) · [RFC 10024](https://www.rfc-editor.org/info/rfc10024/)
- [StatCounter OS](https://gs.statcounter.com/os-market-share/mobile/bangladesh) · [StatCounter Android versions](https://gs.statcounter.com/android-version-market-share/mobile/bangladesh) · [Flutter/Dart note](https://github.com/joaobsjunior/quantum-bank/pull/8)
- [Li et al., USENIX Security 2016](https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/li) · [Notification best practices](https://arxiv.org/pdf/2106.08029) · [Chromium PQ DTLS](https://www.chromium.org/Home/chromium-security/quarterly-updates/) · [DigiCert 2026](https://postquantum.com/security-pqc/digicert-quantum-readiness-outlook-2026/)
