# N1 Master Plan: "The Post-Quantum App Gap" (your one-file guide, v2)

> **Umbrella research question:** *Who and what decides whether a mobile-first population's app traffic is protected against "harvest-now, decrypt-later" quantum attacks, how large is the resulting gap in Bangladesh, and what would close it?*
>
> **What this file is:** the single guide for the whole journey, from day 1 to thesis and papers. It merges `N1_Gap_Portfolio.md` (still useful as a 1-page summary) with a **full reading of the key papers**, a precise gap statement, 15 research gaps, phase-by-phase instructions, decision gates, data formats, analysis, writing and publishing.
>
> **Everything factual below was checked on 30 Sept 2026.** **(verify)** marks things your experiments must confirm. Re-check "first/novel" claims in the week you write them.
>
> **Tools in this folder (all tested on this laptop):**
> - `n1_tools.py`: `pcap`, `apk`, `timing`, `analyze`, `selftest`
> - `f2_starter.py`: server probe
>
> Background concepts are in `Beginners_Guide.md` (Parts B, C and E).

---

## 0. How to use this file

| When | Read |
|---|---|
| **Now (day 1)** | Part A (understand) → Part B1–B2 (what you're answering) → Part C Phase 0 |
| **Every Monday** | Part H2 (timeline): what's due this week. Part D (gates) if a gate is this week. |
| **Before each phase** | That phase in Part C: goal → steps → outputs → "done when" |
| **When something surprises you** | Part D2–D4 (scenarios, negative results, contingencies) |
| **From week 8** | Part G (writing), and Part I (reading guide) as you write related work |

**Weekly loop:** plan (Mon, 30 min) → do (Tue–Fri) → log results in the shared CSVs, commit code → update the "claim ledger" (G3) → show the faculty something every 2 weeks.

---

# PART A: UNDERSTAND

## A1. The problem in one page

Every bKash login, bank balance check or e-KYC selfie upload travels over **TLS**. Today TLS protects the session key with **X25519**, an elliptic-curve key exchange. **Shor's algorithm breaks elliptic curves**, so anyone who **records** that traffic today can **decrypt it later** once a large quantum computer exists. That is "harvest-now, decrypt-later" (HNDL).

The fix already exists: **hybrid X25519MLKEM768** (RFC 10024), which adds the post-quantum ML-KEM so the attacker must break both.

**Where it gets interesting (verified in §A3):**
- **Browsers** (Chrome since v131, Nov 2024) and **iPhone apps** (iOS 26, Sept 2025, by default in Apple's networking APIs) now send the hybrid automatically.
- **Android's built-in TLS library does not.** It isn't in Android 17 either: Google's own announcement lists post-quantum for keystore, boot, attestation and app signing, but **not** app networking. Conscrypt's maintainers state the post-quantum API "only works on Java and not on Android".
- **Flutter's TLS reportedly doesn't enable it either (verify)**, on Android *or* iOS.
- **Bangladesh is 91.2% Android.** Money moves through **apps**, not browsers.

So **your phone's platform and your app's framework, not you, decide whether your financial data is protected.** Nobody has measured this for apps, and certainly not in a mobile-first developing country. The best recent study (IMC 2026) says in writing that it *excluded mobile apps and API endpoints*.

## A2. How N1 connects to your faculty's guidance and papers

| Faculty's guidance / papers | How N1 uses it |
|---|---|
| *"The threat is always real for RSA & ECC (Shor-based)"* | N1 measures whether the **defense against Shor** (hybrid ML-KEM replacing pure X25519/ECDH) actually reaches users' apps. X25519 is an elliptic-curve (Curve25519, prime-field) key exchange, and Shor solves the elliptic-curve discrete log on any curve. |
| Papers on **Shor against elliptic curves** (Putranto et al., IEEE Access 2025; Taguchi & Takayasu, CT-RSA 2023) | They estimate the quantum cost for binary curves. Prime-field estimates are dropping fast too (Roetteler et al. 2017; Google 2026 estimates under 500k physical qubits for 256-bit ECC). **This is your motivation paragraph:** the attack gets cheaper every year, so un-migrated app traffic matters. |
| *"AES-256 is a safer choice (Grover)"*; Grover papers (S-AES, AEAD, GFSPX) | **Gap G15:** N1 also records the **symmetric cipher** each session uses (AES-128 vs AES-256 vs ChaCha20). Early result: Cloudflare, Google and Apple picked **AES-256-GCM**; Bangladesh Bank's site picked **AES-128-GCM**. |
| *"Focus on defense mechanisms (prevent/block quantum attacks)"* | N1 is a **defense-deployment** study: where the defense is missing, why, what fixing costs, and whether telling providers helps (G11–G14). |
| Bernstein 2009 (*count real costs honestly*) | Your cost section (G11) measures **real bytes and milliseconds on real Bangladeshi networks**, not assumptions. |
| *"Structural changes to toy systems"* (Track A) | Not N1's track. If the faculty insists on Track A, run **N2** (`Research_Questions_v3.md`) in parallel with one team member. |

**One-paragraph pitch for your faculty:**
> "Quantum computers running Shor's algorithm will break the elliptic-curve key exchange that protects today's app traffic, and recorded traffic can be decrypted later. The standard defense (hybrid ML-KEM) is now on by default in browsers and in iPhone apps since iOS 26, but not in Android's built-in TLS, and Bangladesh is 91% Android with money moving through apps. We will measure, for the first time, whether Bangladeshi financial and government apps are protected. We'll find which layer (OS, app framework, server) blocks protection, what fixing it costs on local networks, and whether notifying providers helps. The work needs only our own phones and free tools, and produces 2–3 papers even if some parts fail."

## A3. The evidence (verified facts)

| # | Fact | Source (primary where possible) |
|---|---|---|
| E1 | **iOS 26 / iPadOS 26 / macOS Tahoe 26 / visionOS 26** "automatically advertise support for hybrid, quantum-secure key exchange in TLS 1.3". **URLSession and Network.framework** do it by default. Apple warns that legacy servers "that fail to read large ClientHello messages" may break. Test servers with `nscurl --tls-diagnostics`; success shows group X25519MLKEM768 and cipher suite 0x1302 (AES-256-GCM). | [Apple Support 122756](https://support.apple.com/en-us/122756), [WWDC25-314](https://developer.apple.com/videos/play/wwdc2025/314/) |
| E2 | **Android 17's post-quantum work** covers Keystore ML-DSA-65/87, Verified Boot ML-DSA, Remote Attestation (KeyMint chains), and **hybrid Play App Signing**. **No mention of TLS, Conscrypt, WebView or Cronet.** | [Google blog (Mar 2026)](https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/) |
| E3 | **Conscrypt PR #1452** (merged 5 Jan 2026) adds post-quantum named-group support via Java's `SSLParameters`, but "it only works on Java and not on Android, because these methods are not yet available on Android". Press as of 25 Mar 2026: no documented Android 17 change for app networking; WebView-based apps benefit via Chrome. | [conscrypt#1452](https://github.com/google/conscrypt/issues/1452), [Gadget Hacks](https://android.gadgethacks.com/news/android-17-quantum-safe-security-whats-protected-and-whats-not/) |
| E4 | **Flutter/Dart:** Dart 3.13's BoringSSL "does not offer … X25519MLKEM768 in its default groups" and `SecurityContext` exposes no setting. **This is based on source review, not measurement**, so your lab would be the first empirical check. | [quantum-bank PR #8](https://github.com/joaobsjunior/quantum-bank/pull/8) |
| E5 | **Bangladesh (Aug 2026): Android 91.21%, iOS 8.72%.** Android versions: 13 (17.4%), 15 (15.1%), 11 (14.0%), 12 (14.0%), 16 (13.4%), 14 (11.6%). | [StatCounter OS](https://gs.statcounter.com/os-market-share/mobile/bangladesh), [StatCounter Android](https://gs.statcounter.com/android-version-market-share/mobile/bangladesh) |
| E6 | **Cloudflare 2025:** over 50% of human traffic post-quantum by late Oct 2025. **Chrome delayed post-quantum on Android until Nov 2024 because of slower mobile connections.** 39% of the top 100k domains support post-quantum, but **only 3.7% of origins behind Cloudflare** do, so the CDN edge is post-quantum and the origin often isn't. About 0.05% of connections break with origins (ossification). | [Cloudflare PQ 2025](https://blog.cloudflare.com/pq-2025/) |
| E7 | **IMC 2026 ("Mind the Gap"):** 11 *cloud* vantage points (including Mumbai); 49.22% of domains default to post-quantum (Mar 2026); **finance ~59%, government ~38%**; 94% of deployments are provider-managed (Cloudflare + Fastly ≈ 70%). Median latency delta is **0 ms on cloud paths**. **It explicitly excludes mobile apps and custom API endpoints** and notes cloud paths don't represent constrained networks. | [arXiv 2607.29005](https://arxiv.org/html/2607.29005v1) |
| E8 | **Harvest-now-decrypt-later economics:** storage costs $5–12/TB-year; harvesting 1% of global traffic costs about $1.1B/year. **Resumption with PSK-only or 0-RTT inherits the original handshake's weakness.** Small credential/API sessions are the most "worth harvesting". Mobile traffic is about 52% TLS 1.3 and 45% QUIC. | [arXiv 2603.01091](https://arxiv.org/abs/2603.01091) |
| E9 | **Certificate pinning** is most common in **finance** apps. Of the pinned certificates they could match between the app's files and its live connections, 80 of 110 were CA certificates and 30 were leaf certificates (24 of those pinned by public-key hash). **The same company pins differently on Android and iOS** (fewer than half consistent). | [Pradeep et al., IMC 2022](https://dl.acm.org/doi/10.1145/3517745.3561439) |
| E10 | **Android app TLS baseline (2023, before post-quantum rollout):** 90 top apps; median **94 handshakes** in 5 minutes; little resumption; post-quantum handshakes would multiply handshake data about 8×. A banking app made only 4 handshakes because the testers had no account. | [Mankowski, Wiggers & Moonsamy, EuroS&PW 2023](https://thomwiggers.nl/publication/tls-on-android/tls-on-android.pdf) |
| E11 | **App crypto-API scan (2025 poster):** 4,018 apps; RSA used in 781; no post-quantum adoption. **It doesn't analyze TLS/transport at all.** | [Strauss et al., arXiv 2506.00790](https://arxiv.org/pdf/2506.00790) |
| E12 | **Our own measurements (30 Sept 2026, this laptop in Bangladesh):** www.bb.org.bd **accepts only X25519** (not post-quantum) with AES-128-GCM, and is hosted on **its own network (AS139616, Central Bank of Bangladesh)**. Cloudflare, Google and Apple negotiate X25519MLKEM768 + AES-256-GCM. A post-quantum handshake to Cloudflare took **121.8 ms vs 109.9 ms** median (n = 15). | `n1_tools.py`, `f2_starter.py` |
| E13 | **Bangladesh Bank ICT Security Guideline v4.0 (Apr 2023)** requires cryptographic protection of data in transit and defined cryptoperiods. **Check in week 1 whether it mentions post-quantum** (we couldn't download the PDF automatically). | [Bangladesh Bank guideline list](https://www.bb.org.bd/en/index.php/about/guidelist) |

## A4. What the closest studies did, and exactly what they left open

| Study | What it did | What it did **not** do (your opening) |
|---|---|---|
| Mankowski, Wiggers, Moonsamy (EuroS&PW 2023) | Captured TLS of 90 German top apps on one Android 11 phone; counted handshakes and resumptions; *estimated* post-quantum overhead | Before deployment: no post-quantum negotiation measured; no framework attribution; no iOS; banking barely exercised; no developing country |
| Pradeep et al. (IMC 2022) | Pinning prevalence, methods and cross-platform consistency | Didn't consider pinning as a **post-quantum migration blocker** |
| Strauss et al. (arXiv 2025 poster) | Static scan of crypto API use in 4,018 apps | **No transport/TLS analysis**; not sector-specific; no joint transport + app-layer view |
| "Mind the Gap" (IMC 2026) | Longitudinal server-side post-quantum TLS from 11 cloud vantage points | **Excluded mobile apps and custom API endpoints**; cloud paths only |
| Dubey & Varshney (arXiv 2026); Loizou & Ghadafi (UK sectors, arXiv 2026) | Server scans of domains and organizations | Websites/SMTP only; no apps; no client side |
| Cloudflare Radar | Aggregate client post-quantum share per country/ASN | Can't attribute to **apps, frameworks or OS layers** |
| Apple / Google announcements | Platform features | Announcements, not measurements of what apps actually do |

> **The gap:** The post-quantum transition of TLS has been measured for browsers and public web servers, but not for **mobile applications**, which is where most sensitive traffic flows in mobile-first countries. With iOS 26 enabling hybrid ML-KEM by default and Android's platform TLS still lacking it, *which layer decides app-level protection* (OS, networking framework, app configuration, or server) is unknown. The consequences for an Android-dominated country's financial sector, and the cost and levers for closing the gap, are also unmeasured.

**Why now:** iOS 26 (Sept 2025) created the platform split; Android 17 (2026) confirmed networking isn't covered yet; Google's own migration target is 2029. Measure the "before" now and you can also measure the change later (opportunistic gaps O1–O4).

## A5. The concepts you need (quick reference)

| Term | What to look at |
|---|---|
| **ClientHello → `key_share`** | Which groups the app *sends keys for*. X25519MLKEM768 = **0x11EC** (older draft Kyber = 0x6399). |
| **`supported_groups`** | Groups the app *could* use. If post-quantum is here but not in key_share, the server may request it with a **HelloRetryRequest**. |
| **ServerHello → `key_share`** | The group the **server chose**, i.e. what protected this session. |
| **HelloRetryRequest (HRR)** | Server asks the client to resend with another group (costs an extra round trip). |
| **Cipher suite** | TLS 1.3: `AES_128_GCM` (0x1301), `AES_256_GCM` (0x1302), `CHACHA20_POLY1305` (0x1303). The Grover view (G15). |
| **Resumption (`pre_shared_key`) and `psk_key_exchange_modes`** | `psk_dhe_ke` does a fresh key exchange. `psk_ke` doesn't, so it **inherits** the old session's protection (E8). |
| **SNI** | Hostname in the ClientHello. It tells you *which service* (first-party API vs analytics SDK). |
| **QUIC** | HTTP/3 over UDP; its handshake is TLS 1.3 too. Read it in Wireshark (filter `quic && tls.handshake.type == 1`). |

**Where TLS lives in each Android/iOS networking stack** (your G1 lab fills in the "?"):

| Stack | TLS engine | Android default post-quantum | iOS default post-quantum |
|---|---|---|---|
| HttpURLConnection / OkHttp (native Kotlin/Java, React Native on Android) | Platform **Conscrypt** (BoringSSL inside) | **No** (E3) **(verify per version)** | n/a |
| URLSession / Network.framework (native Swift, React Native on iOS) | Apple TLS | n/a | **Yes** (iOS 26+, E1) |
| **Flutter** (`dart:io`) | Dart's own BoringSSL (both platforms) | **Reportedly no** (E4) **(verify)** | **Reportedly no (verify)**, which would erase iOS's advantage |
| **WebView** / Chrome Custom Tabs | Chromium (updated through the Play Store) | **Yes if recent** (Chrome ≥131) **(verify versions)** | WKWebView = Apple TLS → yes (iOS 26) **(verify)** |
| **Cronet** (Play Services or bundled) | Chromium network stack | **? (verify)** | n/a |
| .NET MAUI / Xamarin, Unity, Ktor, bundled Conscrypt | Varies | **? (verify)** | **? (verify)** |

---

# PART B: RESEARCH DESIGN

## B1. The umbrella question, 4 pillars and 15 gaps

| ID | Gap (short) | Research question | Method | Phase | Effort (person-weeks) | If yes / if no |
|---|---|---|---|---|---|---|
| **P1: Client side** | | | | | | |
| **G1** ⭐ | Framework default matrix | Which stacks offer X25519MLKEM768 by default, on which OS versions? | Test apps + `cdn-cgi/trace` | 2 | 4–5 | Yes: developer guidance. No: "Google's recommended stacks leave apps unprotected". |
| **G2** | Update lag and device ecosystem | What share of devices run post-quantum-capable versions of WebView/Chrome/Play services? | Trace-page survey (no infrastructure) + StatCounter | 7 | 3 | Mostly updated: framework choice matters. Not: "a hidden update divide". |
| **G3** ⭐⭐ | **Platform divide** (same app on iOS vs Android) | How often does protection differ between the iOS and Android versions of the same app, and does the OS or the framework explain it? | Hotspot capture of app pairs | 2 + 3 | 3–4 | A divide exists: policy headline. No divide: "frameworks equalize". |
| **P2: Ecosystem** | | | | | | |
| **G4** (core) | The Bangladesh app 2×2 + layer attribution | What fraction of Bangladeshi app connections negotiate post-quantum, and which layer decides? | Captures + lab + server probes | 3–5 | backbone | Any result is the baseline finding |
| **G5** | Third-party SDK layer | Do SDK connections (analytics, ads, crash, maps) lead or lag the app's own traffic? | Label SNIs in captures | 8 | 1–2 | Lead: "your bank's API is the weak link". Lag: "data leaks via side doors". |
| **G6** | App-layer crypto on top of TLS | How often is quantum-vulnerable RSA/ECC used inside apps, and does it change effective protection? | `n1_tools.py apk` signals + jadx | 4 | 3 | RSA: two layers to migrate. Symmetric: a safety net. |
| **G7** | Exposure weighted by data lifetime | Are long-lived flows (e-KYC, identity, statements) better or worse protected than telemetry? | Flow-step labeling + resumption modes | 3 + 8 | 2–3 | Either way it gives the policy weight |
| **P3: Infrastructure** | | | | | | |
| **G8** | The API gap (app backends vs websites) + hosting | Do app API hosts lag the same organization's website? Does hosting (CDN, cloud, own network) explain it? | `f2_starter` pairs + Team Cymru ASN lookup | 5 | 2 | APIs lag: "web studies overestimate readiness". APIs lead: modern clouds. |
| **G9** | Pinning as a migration blocker | Which finance apps pin what (CA or leaf, RSA or ECDSA), and would post-quantum or Merkle Tree certificates break them? | NSC via apktool + SPKI regex + crt.sh | 4 | 2–3 | Few pin: reassuring. Many leaf pins: a hazard list. |
| **G10** | Network path | Do Bangladeshi operators' paths break or slow post-quantum app handshakes? | Captures and timing per network | 6 | 2 | Any failures are actionable; none is good news with evidence |
| **P4: Closing the gap** | | | | | | |
| **G11** | Cost on Bangladeshi networks and low-end phones | What latency, data and battery does post-quantum add here? | `n1_tools.py timing`, test apps | 6 | 2–3 | Real numbers either way (supporting section) |
| **G12** | Static → dynamic prediction at scale | Do APK features predict measured behavior? What does a large static scan show? | Classifier on your data → AndroZoo | 10 (stretch) | 5–6 | Predictable: scalable method. Not: runtime dominates. |
| **G13** | Notification experiment | Does responsible notification with a fix guide speed up adoption in 3–6 months? | Notify → re-measure | 9 | 2 + waiting | Both outcomes are publishable (a known study genre) |
| **G14** | Human layer | What do Bangladeshi fintech developers and bank teams know, and what blocks them? | Survey (30–60) + interviews (8–12), IRB | 9 (optional) | 5–6 | Any blocker pattern explains the "why" |
| **G15** | Grover view + resumption | Do app sessions use AES-256 (NSA's CNSA 2.0 level) or AES-128? Do resumptions use `psk_ke` (inherits exposure)? | Extra columns already in `n1_tools.py pcap` | 8 | 1 | Links N1 to the faculty's AES-256 point |

**Opportunistic gaps.** Record a baseline now so these become possible:
- **O1:** Google ships post-quantum in Conscrypt → a before/after natural experiment.
- **O2:** Flutter/Dart enables it → measure how fast apps pick it up.
- **O3:** Chrome ships post-quantum for WebRTC (listed for about Chrome 157) → calls in WebView apps.
- **O4:** post-quantum or Merkle Tree certificates go live (2026–27) → test G9's predictions.
- **O5:** a global app study appears → keep the Bangladesh / G3 / G7 / G13 / G14 angles.

## B2. Hypotheses (write them down before measuring; this protects you from "we found nothing")

| ID | Hypothesis | Falsified if | If falsified, you report |
|---|---|---|---|
| H1 | Native Android stacks (HttpURLConnection, OkHttp) **don't** offer post-quantum on any Android version 10–17 | Any version offers it | Which version/update brought it (then O1 starts) |
| H2 | WebView/Chrome Custom Tabs offer it when WebView ≥ 131 | Recent WebView doesn't | "Even Chromium-in-apps lacks it": a surprising, strong finding |
| H3 | Flutter apps offer it on **neither** platform | They do | E4 was wrong; you corrected it empirically |
| H4 | For native-built apps, iOS versions offer post-quantum and Android versions don't (the platform divide) | No difference | "Platforms equalized", with an explanation |
| H5 | Fewer than 30% of Bangladeshi financial apps' first-party connections negotiate post-quantum | ≥ 30% | Which layers enabled it (usually CDN + WebView/Cronet) |
| H6 | App API hosts lag their organizations' websites | APIs equal or lead | "Web measurements are representative of apps" |
| H7 | Finance apps that pin mostly pin CA keys (as in IMC 2022), so post-quantum CA changes will force app updates | Pins are rare or dynamic | "Pinning won't block the post-quantum certificate migration" |
| H8 | Post-quantum adds under 30 ms at the median on Bangladeshi 4G, with a heavier tail | Much larger | Network-specific bottlenecks (G10) |

## B3. The measurement model and definitions

- **Unit:** one TLS connection (a row from `n1_tools.py pcap`). Only **first-party** connections count for headline numbers. G5 uses third-party ones.
- **Client offers post-quantum** = `client_offers_pq_keyshare = True`. Note: `client_supports_pq_group` without a key share means post-quantum is only possible via a retry.
- **Server accepts post-quantum** = captured `pq_negotiated = True`, **or** the `f2_starter.py` probe shows `pq_hybrid_handshake = ok` for that hostname. The probe tells you about servers the app never *offered* post-quantum to.
- **App outcome (per app × device)** from its first-party connections (built into `n1_tools.py analyze`):
  - ✅ **protected**: offers and accepts
  - 🟠 **server bottleneck**: offers, doesn't accept
  - 🟠 **app-side bottleneck**: doesn't offer, accepts
  - 🔴 **both missing**
- **Layer attribution for app-side bottlenecks:**
  1. The lab (G1) says this framework on this Android version doesn't offer post-quantum → **framework/OS layer**.
  2. The lab says it does, but the app doesn't → **app configuration layer** (old bundled library, custom TLS settings).
  3. A framework not in the lab → **unknown**. Add it to the lab or report it as unknown.
- **Data-lifetime weighting (G7).** Each connection gets `flow_step` ∈ {onboarding/e-KYC, login, statement/history, transaction, telemetry, content}. Assign lifetime classes (≥10 years, 1–10 years, under 1 year). Weighted exposure = share of *long-lived* flows that are not post-quantum. A `psk_ke` resumption counts as unprotected if its parent session was classical (E8).
- **Grover view (G15).** Share of first-party sessions using AES-256-GCM vs AES-128-GCM vs ChaCha20, per platform and app. (Context: NIST considers AES-128 adequate even post-quantum; the NSA's CNSA 2.0 requires AES-256.)

## B4. Sampling and the experiment matrix

- **Apps (about 50):**
  - mobile money (e.g. bKash, Nagad, Rocket, Upay)
  - banks (e.g. CellFin, Astha, City Touch, EBL Skybanking; aim for 12–15 banks)
  - telecom self-care (MyGP, My Robi, MyBL)
  - e-commerce and ride-sharing (Daraz, Chaldal, Pathao, Foodpanda)
  - government and health (search Google Play)
  - **Verify every name and package yourself.** Inclusion: ≥100k downloads, Bangladesh-focused, handles personal or financial data. Record the package, version and date.
- **Optional comparison set:** 20 global top apps (for context).
- **Android devices:** real phones for **Android 11 or 12** (old) and **Android 15 or 16** (new). These cover Bangladesh's biggest versions (E5). Emulators for **10, 11, 12, 13, 14, 15, 16, 17**, using *Google Play* images.
- **iOS (G3):** 1 iPhone on iOS 26 (borrow if needed), capturing about **20 apps** that exist on both platforms. Also 1 iPhone on iOS 18 or older if available (before/after the OS change).
- **Networks:** Grameenphone, Robi, Banglalink and Teletalk mobile data; home broadband; NSU Wi-Fi. The full campaign runs on 1 network; G10/G11 repeat a subset on all.
- **Session protocol (adapted from Mankowski et al.):** **5 minutes** per app per device. They found traffic stable after 5 minutes. Steps are in Phase 3.
- **Background noise:** capture the phone for 30 minutes with a system app open and no target app (as they did with the calculator). This gives you the OS's own background connections to exclude.

## B5. Ethics, legal, and responsible disclosure

- ✅ **Your own devices and your own accounts only.** No transactions for research.
- ✅ Read only **handshake metadata** (ClientHello/ServerHello), which is sent unencrypted by design.
- ❌ No decryption, no man-in-the-middle, no pinning bypass. Don't use PCAPdroid's TLS-decryption feature. Keep server probes to a few handshakes per host.
- ❌ Don't redistribute APKs; don't publish device IP addresses.
- ✅ The **G2 survey** and **G14 interviews** need **university ethics/IRB approval** and a consent page, and must collect **no IP addresses** (tell participants to delete the `ip=` line).
- ✅ **Disclosure:** notify affected providers (and BGD e-GOV CIRT for government apps) at least **60–90 days** before publishing (Phase 9 has the template).
- ✅ Show Parts B and C to the faculty **before Phase 3**.

---

# PART C: THE JOURNEY (phases)

> Week numbers assume two semesters (CSE499A = weeks 0–12, CSE499B = weeks 13–24). Phases overlap on purpose.

### Phase 0 (week 0–1): setup, baseline, approval
**Serves:** everything; the baseline enables O1–O4.
1. Clone a private GitHub repo with folders `captures/`, `apks/` (git-ignored), `data/`, `lab/`, `analysis/`, `paper/`.
2. Laptop: Python ≥ 3.13 with `ssl` on OpenSSL ≥ 3.5 (`python -c "import ssl; print(ssl.OPENSSL_VERSION)"`). Install Wireshark, Android Studio (includes adb and emulators), jadx and apktool.
3. Run `python n1_tools.py selftest` and `python n1_tools.py timing cloudflare.com 20`.
4. **Baseline record** (`data/baseline.md`):
   - for each test phone: Android version, security patch, **Google Play system update** date, **Android System WebView** version, Chrome version
   - for the iPhone: iOS version
   - today's date
5. Read the 5 must-read sources (Part I, items 1–5).
6. Meet the faculty: show the pitch (A2), agree on the track, and ask about **IRB** for G2/G14.

**Done when:** selftest passes, the baseline file exists, and the faculty has approved.

### Phase 1 (weeks 1–2): pilot → Gate 1
**Serves:** G4 feasibility.
1. Install **PCAPdroid** (free; captures one app via Android's VPN mechanism; no root). Settings: *Target app* = the app; *Dump mode* = **PCAP file** (PCAPNG is a paid feature and isn't needed).
2. Capture **Chrome** (control), **bKash**, **one bank app**, **Pathao/Daraz**, and **one WebView-style app**, 5 minutes each.
3. `python n1_tools.py pcap captures\pilot_*.pcap > data\pilot.csv`
4. `python f2_starter.py <5 first-party hostnames> > data\pilot_servers.csv`
5. **If a banking app refuses to run with the VPN active:** Windows *Mobile hotspot* → Wireshark on the hotspot adapter → save as **pcap**.

**Gate 1:** at least 4 of 5 apps parsed, and Chrome shows `client_offers_pq_keyshare = True`. If not, see Part D3.

### Phase 2 (weeks 2–6): the framework lab (G1 + G3-lab) → arXiv note
**Serves:** G1, G3, G2 baseline. **The fastest publishable result.**

**Method:** each test app fetches `https://www.cloudflare.com/cdn-cgi/trace` and prints the **`kex=`** line, which shows the negotiated group for that connection (verified: this laptop gets `kex=X25519MLKEM768`). No capture is needed.

Build these **sketches** (test them yourself):

```kotlin
// Android: HttpURLConnection (platform Conscrypt). Manifest: <uses-permission android:name="android.permission.INTERNET"/>
thread { Log.i("PQTEST", "HttpURLConnection " + URL(TRACE).readText().lines().first { it.startsWith("kex=") }) }
// Android: OkHttp
thread { Log.i("PQTEST", "OkHttp " + OkHttpClient().newCall(Request.Builder().url(TRACE).build()).execute()
                                       .body!!.string().lines().first { it.startsWith("kex=") }) }
// Android: WebView (read the kex line on screen)
webView.loadUrl(TRACE)
```
```dart
// Flutter (dart:io), run on BOTH Android and iOS
final r = await (await HttpClient().getUrl(Uri.parse(TRACE))).close();
print('Flutter ${(await r.transform(utf8.decoder).join()).split('\n').firstWhere((l) => l.startsWith('kex='))}');
```
```javascript
// React Native (Android: OkHttp underneath; iOS: URLSession underneath), run on both
fetch(TRACE).then(r => r.text()).then(t => console.log('RN ' + t.split('\n').find(l => l.startsWith('kex='))));
```
```swift
// iOS native (URLSession), if you have a Mac with Xcode
URLSession.shared.dataTask(with: URL(string: TRACE)!) { d, _, _ in
    print(String(decoding: d!, as: UTF8.self).split(separator: "\n").first { $0.hasPrefix("kex=") }!) }.resume()
```
(`TRACE = "https://www.cloudflare.com/cdn-cgi/trace"`.) Also test **Cronet** (Play Services provider, following Android's Cronet guide), **Chrome Custom Tabs**, and **.NET MAUI / Unity** if time allows. **No Mac?** Test iOS with prebuilt apps: open the trace URL in Safari (Apple TLS) and in an in-app browser (WKWebView).

**Matrix:** stacks × Android **10–17** emulators (*Google Play* images) × 2 real phones × iPhone.
**Output:** `lab/lab_results.csv` with columns `stack, platform, os_version, device, webview_version, play_system_update, kex, date`.

**Engage the community:** if a major stack lacks post-quantum (e.g. Dart), open a polite GitHub issue with your evidence. That builds a public record of your finding and its date.

**Output:** an **arXiv note by week 6**, *"Which mobile networking stacks negotiate post-quantum TLS by default? A 2026 measurement"*. This stakes your claim (see G1/G2 in Part G).

**Gate 2 (week 6):** at least 6 stacks × 3 Android versions + iOS data. If not, see D3.

### Phase 3 (weeks 4–10): app sample and capture campaign (G4, G5, G7, G15; a G3 subset)
**3a (weeks 3–4). Build `data/apps.csv`:** columns `app, package, category, downloads, version, date, has_ios_version`.

**3b. Session protocol (each app × each device), 5 minutes:**
1. Force-stop the app (fresh connections). Start the capture.
2. Minutes 0–1: open the app and stay on the first screen. **Log timestamps.**
3. Minutes 1–3: log in (your own account) → view balance/history → open the statement screen.
4. Minutes 3–4: open profile/KYC screens (*view only*). If you're still in the onboarding stage (no account), capture up to the e-KYC step without submitting.
5. Minutes 4–5: leave the app idle in the foreground.
6. Stop and export `<app>_<device>_<osver>_<net>_<YYYYMMDD>.pcap`.
7. Write each step's start time in `data/sessions.csv` (`capture_file, step, start_time`). This is how you label `flow_step` (G7) without decrypting.

**3c. Parse:** `python n1_tools.py pcap captures\*.pcap > data\connections_raw.csv`. Then add columns by hand or script (Part E3): `app, device, platform, os_version, network, first_party, flow_step, transport`.

**3d. Label SNIs:** first-party (the company's domains) vs third-party (e.g. `*.googleapis.com`, `graph.facebook.com`, `*.appsflyer.com`, `*.crashlytics.com`).

**3e. QUIC:** open the capture in Wireshark with filter `quic && tls.handshake.type == 1` and add those rows by hand with `transport=QUIC`.

**3f. iOS subset (G3):** about 20 apps on the iPhone via laptop hotspot + Wireshark, using the same protocol.

**Gate 3 (week 10):** at least 40 apps × 2 Android phones captured, plus at least 15 iOS pairs.

### Phase 4 (weeks 6–10): static analysis (G1 link, G6, G9)
1. `adb shell "pm list packages | grep -i <name>"` → `adb shell pm path <package>` → `adb pull` **all** APK splits into `apks/` (git-ignored).
2. `python n1_tools.py apk apks\<app>_*.apk` prints:
   - frameworks (Flutter, OkHttp, Cronet, React Native, WebView-hybrid…)
   - **signals:** `spki_pins`, `rsa_cipher_strings`, `pem_public_keys`, `pem_certificates`, `cert_files`, `network_security_config`

   These are **lower bounds**: obfuscated or native code is missed.
3. **Pinning (G9), following IMC 2022:**
   - `apktool d <app>.apk` → read `res/xml/network_security_config.xml` `<pin-set>` digests.
   - Convert each base64 pin to hex: `python -c "import base64,sys; print(base64.b64decode(sys.argv[1]).hex())" <pin>`.
   - Look it up at `https://crt.sh/?spkisha256=<hex>` to see **which certificate** is pinned (CA or leaf) and its **key type** (RSA or ECDSA).
4. **App-layer crypto (G6):** open the flagged apps in **jadx**. Search `Cipher.getInstance`, `KeyFactory`, `KeyAgreement` and note **what** is encrypted (PIN? payload? token?).
5. **Output:** `data/static.csv` with columns `app, frameworks, spki_pins, pinned_cert_type, pinned_key_alg, rsa_cipher_strings, app_layer_crypto_notes`.

### Phase 5 (weeks 8–10): server side and hosting (G8)
1. For each organization, list **pairs**: website host + the API hosts seen in captures.
2. `python f2_starter.py <all hosts> > data\servers.csv`. Columns: `domain, classic_handshake, pq_hybrid_handshake, clienthello_bytes, split_hello_ok`.
3. **Hosting owner** for each host (Windows-friendly, free; tested):
   ```
   python -c "import socket; print(socket.gethostbyname('www.bb.org.bd'))"      -> 103.142.142.53
   nslookup -type=TXT 53.142.142.103.origin.asn.cymru.com                      -> "139616 | 103.142.142.0/24 | BD ..."
   nslookup -type=TXT AS139616.asn.cymru.com                                   -> "... The Central Bank of Bangladesh, BD"
   ```
   Classify each as CDN (Cloudflare/Akamai/Fastly/CloudFront), cloud (AWS/Azure/GCP), or **own/local network**.
4. **Nuance (E6):** a CDN edge can be post-quantum while the CDN → bank-server link is classical. Report "post-quantum at the edge" separately; you can't see the origin link.
5. **Output:** `data/hosting.csv` with columns `org, host, role (web/api), ip, asn, as_name, hosting_class`.

### Phase 6 (weeks 10–12): network path and cost (G10, G11)
1. Tether the laptop to each network, then run `python n1_tools.py timing cloudflare.com 100` and the same against 2 Bangladeshi post-quantum-capable hosts.
2. Repeat morning, evening and night. Save to `data/timing.csv` with columns `network, time, group, median_ms, p90_ms, n`.
3. Re-capture 10 apps on all 4 mobile operators, looking for resets, retries or missing ServerHellos (G10).
4. **Optional:** compare a test app using OkHttp (classic) vs Cronet (post-quantum, if G1 confirms) for real request times and battery (Android Settings → Battery usage) on a low-end phone.

### Phase 7 (weeks 8–12, parallel): update-lag survey (G2) (needs IRB)
**No infrastructure needed:** participants open `https://www.cloudflare.com/cdn-cgi/trace` (a) in their phone's browser and (b) inside an app's in-app browser (a link opened from Messenger/Facebook, which uses WebView). They paste **only** the `uag=` and `kex=` lines into a Google Form, along with phone model and Android version. Target 100+ phones.
**You learn:** what share of real Bangladeshi phones' browsers and WebViews negotiate post-quantum, by Android version. Combine with StatCounter (E5).

### Phase 8 (weeks 12–15): analysis
See Part F. Produce every table and figure listed there. Freeze `data/` (tag a git release).

### Phase 9 (weeks 14–26): disclosure, notification experiment (G13), interviews (G14, optional)
1. **Disclosure email** (all affected providers, week 14):
   > Subject: Post-quantum TLS readiness of [App]. Research notice from [University].
   > We are students at [University] studying post-quantum readiness of mobile apps in Bangladesh. By passively observing our own device's TLS handshakes (no decryption), we found that [App vX] [does not offer / its API server does not accept] hybrid post-quantum key exchange (X25519MLKEM768, RFC 10024). This is not an active vulnerability. It concerns long-term "harvest-now, decrypt-later" risk. A one-page fix guide is attached. We plan to publish aggregate results after [date + 90 days] and would be glad to re-test after changes. Contact: [names], supervisor [name].
2. **Fix guide (1 page):**
   - **Server side:** enable X25519MLKEM768 (OpenSSL ≥ 3.5, or a post-quantum-capable CDN/load balancer).
   - **App side:** WebView/Custom Tabs for web flows; Cronet for native networking if G1 confirms; watch the Flutter/Conscrypt updates.
   - **Pinning:** pin CA keys with backup pins, not leaf keys.
3. **G13:** if there are more than 20 organizations, notify a random half at week 14 and the rest at week 20. Re-measure everyone at weeks 20 and 26. Report the difference. Follow published best practices for notification studies (arXiv 2106.08029).
4. **G14 (optional, IRB):** a survey of 30–60 developers and security staff (awareness, blockers, vendors, the regulator) plus 8–12 interviews of 30 minutes.

### Phase 10 (weeks 14–20): writing and submission
See Part G. Submit **Paper A** by about week 18–20; the thesis draft is due by week 22.

### Phase 11 (months 6–9+): longitudinal and opportunistic (O1–O5)
Re-run the Phase 2 lab and a 15-app capture every month. If O1–O4 happen, you already have the "before" data.

---

# PART D: DECISION GATES AND CONTINGENCIES

## D1. Gates

| Gate | Week | Pass condition | If it fails |
|---|---|---|---|
| G-1 | 2 | ≥ 4/5 pilot apps parsed; the Chrome control offers post-quantum | Switch to the hotspot method; if both fail, go **lab + static only** (D3) |
| G-2 | 6 | Lab matrix ≥ 6 stacks × 3 Android versions + iOS | Cut Unity/.NET; keep Conscrypt/OkHttp/WebView/Flutter/Cronet/RN |
| G-3 | 10 | ≥ 40 apps × 2 phones; ≥ 15 iOS pairs | Reduce to 30 apps; keep G3 even at 10 pairs |
| G-4 | 15 | Results frozen; the story chosen via D2 | Write the minimum viable thesis (D5) |

## D2. Which story does your data tell? (decide at week 6 and again at week 12)

```
A. Most apps UNPROTECTED because of the framework/OS   → Lead: G1 + G3 platform divide; add G11, G13.
B. Most apps PROTECTED (WebView/Cronet/CDNs)            → Lead: "partial protection": G5, G6, G7, G2.
C. SERVER is the bottleneck (apps offer, APIs decline) → Lead: G8 API gap + hosting, G9, G13 to banks.
D. Capture blocked                                      → Lead: G1/G3 lab + static G6/G9/G12.
E. Scooped by a global app study                        → Lead: Bangladesh + G3 same-app pairs, G7, G13, G14.
```

## D3. Contingencies

| Problem | Fix |
|---|---|
| Apps detect the VPN (PCAPdroid) | Laptop hotspot + Wireshark (Phase 1 step 5) |
| Capture file is `.pcapng` | Wireshark → File → Save As → *Wireshark/tcpdump - pcap* |
| Much of the traffic is QUIC | Parse in the Wireshark GUI (Phase 3e) |
| TLS 1.2 connections | Classic by definition. Record `tls_version`. |
| No iPhone available | Borrow for 2 days; or do G3 with Safari/in-app browsers only; or drop G3 to "future work" |
| No Mac for Swift | Use React Native/Flutter on iOS via Expo/Codemagic, or the prebuilt-app method (Phase 2) |
| IRB is slow | Start G2/G14 paperwork in week 1; they're optional for the minimum thesis |
| An app update changes results mid-study | Record the version; re-capture 10 apps at the end and report the drift |
| Google ships post-quantum in Conscrypt mid-project (O1) | 🎉 Re-run the lab on all versions and write the before/after paper |

## D4. Negative results are findings (how to phrase them)

| You find… | You write… |
|---|---|
| Cronet via Play Services lacks post-quantum | "Google's recommended app network stack lacks the protection Google's browser has" |
| No Bangladeshi app offers post-quantum | "A mobile-first financial sector with zero app-level post-quantum protection: which layer blocks it" |
| Pinning is rare | "Pinning won't block the post-quantum certificate migration in this sector" |
| Static features don't predict behavior | "Runtime configuration dominates; dynamic measurement is essential" |
| Notifications changed nothing | "Awareness isn't the bottleneck; platform or regulator action is" |
| No iOS/Android difference | "Frameworks neutralize OS defaults" |

## D5. Minimum viable thesis (if a lot goes wrong)
**G1 (lab) + G4 (≥ 25 apps) + one of {G3, G8, G9}.** This needs only emulators, 1–2 phones, `n1_tools.py` and `f2_starter.py`.

---

# PART E: TOOLS, DATA AND FILES

## E1. Tools

| Tool | Use | Notes |
|---|---|---|
| `n1_tools.py pcap` | Per-connection CSV (each file parsed separately; wildcards like `captures\*.pcap` work in any shell). Columns: `capture_file, sni, server_port, client_offers_pq_keyshare, client_supports_pq_group, client_keyshares, server_selected, hello_retry, pq_negotiated, tls_version, cipher_suite, resumption_offered, psk_modes, resumption_accepted` | TCP only; classic pcap |
| `n1_tools.py apk` | Frameworks + pinning/crypto signals | Pass **all** APK splits |
| `n1_tools.py timing host n` | Median/p90 handshake ms, post-quantum vs X25519 | Excludes TCP connect |
| `n1_tools.py analyze conn.csv servers.csv` | Headline % with Wilson 95% CI; per-app 2×2; McNemar old vs new phone | Needs columns `app, device, first_party, sni, client_offers_pq_keyshare, pq_negotiated` |
| `n1_tools.py selftest` | Checks everything offline | Run after any edit |
| `f2_starter.py hosts…` | Does the server accept post-quantum? Does it survive a split ClientHello? | Polite: a few handshakes |
| PCAPdroid, Wireshark, adb, apktool, jadx, crt.sh, Team Cymru DNS | Capture, inspect, pull APKs, decode configs, look up pins, find hosting | All free |
| `nscurl --tls-diagnostics` (macOS only) | Apple's server check | Optional |

## E2. Data files (the team must use exactly these)

| File | Columns |
|---|---|
| `data/apps.csv` | app, package, category, downloads, version, date, has_ios_version |
| `data/sessions.csv` | capture_file, app, device, platform, os_version, network, step, start_time |
| `data/connections.csv` | *(from pcap)* + app, device, platform, os_version, network, first_party, flow_step, transport |
| `data/servers.csv` | *(from f2_starter)* domain, classic_handshake, pq_hybrid_handshake, clienthello_bytes, split_hello_ok |
| `data/hosting.csv` | org, host, role, ip, asn, as_name, hosting_class |
| `data/static.csv` | app, frameworks, spki_pins, pinned_cert_type, pinned_key_alg, rsa_cipher_strings, app_layer_crypto_notes |
| `lab/lab_results.csv` | stack, platform, os_version, device, webview_version, play_system_update, kex, date |
| `data/timing.csv` | network, time, host, group, median_ms, p90_ms, n |
| `data/baseline.md` | device versions and dates (Phase 0) |

## E3. Joining captures to your session log (to fill in `flow_step` etc.)
Label each connection by its capture file and approximate time. If you need exact timestamps, extend `n1_tools.py` to output the first packet time per stream. That's a small change once you're comfortable with the code. Until then, label by SNI + session step, which is usually enough, since each screen calls characteristic hosts.

---

# PART F: ANALYSIS COOKBOOK

**Headline numbers (with 95% Wilson CIs, from `n1_tools.py analyze`):**
1. % of first-party connections post-quantum-negotiated: overall, per category, per platform.
2. Number of apps in each 2×2 cell (per device).
3. Layer attribution counts (framework/OS vs app configuration vs server vs unknown).
4. Old vs new Android: McNemar exact p-value (built in).
5. iOS vs Android on the same apps (G3): a paired table plus McNemar.
6. G8: website-vs-API post-quantum rates per organization; a table by hosting class.
7. G9: % of apps pinning; CA vs leaf; RSA vs ECDSA.
8. G15: cipher-suite shares; % of resumptions using `psk_ke`.
9. G7: long-lived-flow exposure vs all-flow exposure.
10. G11: median and p90 latency deltas per network, with bootstrap CIs (resample the per-run times 1,000 times).

**Figures:**
- (1) 2×2 stacked bars per category
- (2) framework × OS-version heatmap (G1)
- (3) iOS-vs-Android paired dot plot (G3)
- (4) "which layer decides" bar
- (5) website-vs-API scatter (G8)
- (6) latency CDFs per network (G11)
- (7) exposure by data lifetime (G7)

---

# PART G: WRITING AND PUBLISHING

## G1. Outputs and venues

| Output | Contents | Target venue (examples) | When |
|---|---|---|---|
| **arXiv note** | G1 (+ early G3) | arXiv → a workshop | Week 6 |
| **Paper A: "The Post-Quantum Platform Divide"** | G1 + G2 + G3 (+ G15) | ACM **WiSec**, **PETS**, *Computers & Security* (Q1) | Weeks 18–20 |
| **Paper B: "The App Gap in a Mobile-First Financial Sector"** | G4–G9 (+ G11) | *Computers & Security*, *JISA* (Q1), *IEEE Access* | Weeks 22–26 |
| **Paper C (optional)** | G13 + G14 | USEC/SOUPS workshops, *Computers & Security* | Month 9+ |
| **Thesis** | Umbrella question; chapters = pillars P1–P4 | CSE499 report | Week 22–24 |

## G2. Paper A outline
1. **Introduction:** HNDL + Shor's threat to elliptic curves (cite the faculty's ECC papers and 2025–26 estimates); iOS 26 vs Android; Bangladesh is 91% Android.
2. **Background:** the TLS 1.3 key share; X25519MLKEM768; where TLS lives per stack (A5 table).
3. **Method:** the trace-based lab, versions, devices, the survey.
4. **Results:** the framework matrix; the platform divide; update lag.
5. **Discussion:** who is left behind; recommendations to Google, Flutter and app developers.
6. **Limitations and ethics.**
7. **Related work** (Part I).
8. **Conclusion.**

## G3. Claim ledger (claim only what you measure; re-search before submitting)
- "To our knowledge, the first measurement of post-quantum key exchange **in mobile apps** of a mobile-first developing country." (G4)
- "The first same-app **iOS-vs-Android** comparison after iOS 26." (G3)
- "The first empirical **framework default matrix** for post-quantum TLS on Android and iOS." (G1)
- "Evidence on whether **app API backends lag websites**." (G8)
- "A **data-lifetime-weighted** HNDL exposure metric for app traffic." (G7)

## G4. A draft related-work gap paragraph (adapt it; don't copy it blindly)
> Prior measurements of post-quantum TLS focus on servers and browsers: longitudinal scans of top domains from cloud vantage points [Mind the Gap, IMC 2026], domain-level readiness studies [Dubey & Varshney 2026; Loizou & Ghadafi 2026], and aggregate client statistics [Cloudflare Radar]. The IMC 2026 study explicitly excludes mobile applications and custom API endpoints. For apps, Mankowski et al. [EuroS&PW 2023] characterized TLS usage before post-quantum deployment and estimated its overhead; Pradeep et al. [IMC 2022] measured certificate pinning; and Strauss et al. [2025] statically scanned cryptographic API use without examining transport security. None measure whether apps actually negotiate hybrid post-quantum key exchange, which platform or framework layer determines it, or how this plays out in mobile-first, Android-dominated economies. We fill this gap.

## G5. Threats to validity (write this section early)
Sample size and selection; single capture location (CDN edges vary by location); point-in-time measurement (apps update); emulator vs real device (system updates); unexercised code paths (as in IMC 2022, results are a lower bound); origin links hidden behind CDNs; QUIC parsed manually; the survey's self-selection bias.

---

# PART H: TEAM, TIMELINE AND RISKS

## H1. Roles (3 people)

| Member | Owns | Also helps with |
|---|---|---|
| **A: capture lead** | Phases 1, 3 (sessions, log, QUIC rows, iOS subset) | G7 flow labels |
| **B: lab and static lead** | Phases 2, 4 (test apps, emulators, APK signals, pinning, jadx) | arXiv note |
| **C: servers, cost and analysis lead** | Phases 5, 6, 8 (hosting, timing, statistics, figures) | Writing lead; disclosure |

## H2. Timeline (24 weeks)

| Week | 0 | 1–2 | 3–4 | 5–6 | 7–8 | 9–10 | 11–12 | 13–15 | 16–18 | 19–20 | 21–24 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Setup and baseline (P0) | ■ | | | | | | | | | | |
| Pilot (P1) → Gate 1 | | ■ | | | | | | | | | |
| Framework lab (P2) → arXiv (wk 6) | | ■ | ■ | ■ | | | | | | | |
| App list + captures (P3) | | | ■ | ■ | ■ | ■ | | | | | |
| Static analysis (P4) | | | | ■ | ■ | ■ | | | | | |
| Servers and hosting (P5) | | | | | ■ | ■ | | | | | |
| Cost and network (P6) | | | | | | | ■ | | | | |
| Survey (P7, IRB) | | | | | ■ | ■ | ■ | | | | |
| Analysis (P8) → Gate 4 | | | | | | | ■ | ■ | | | |
| Disclosure / G13 (P9) | | | | | | | | ■ | ■ | ■ | ■ |
| Writing (P10): Paper A, thesis | | | | | ■ | | | ■ | ■ | ■ | ■ |

(■ = active. CSE499A covers weeks 0–12; CSE499B covers weeks 13–24.)

## H3. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| A global app study appears | Medium | Medium | arXiv note at week 6; the unique angles in D2-E |
| Google/Flutter ship post-quantum mid-project | Medium | **Positive** | Baseline recorded → before/after paper (O1/O2) |
| Apps block capture | Medium | Medium | Hotspot method; the lab/static path (D5) |
| Scarce iPhone access | Medium | Medium | Borrow; in-app-browser method; G3 as future work |
| IRB delay | Medium | Low | G2/G14 are optional |
| Team member drops out | Low–Medium | High | Shared CSVs + git; each phase documented here |

---

# PART I: READING GUIDE (what to extract from each)

| # | Read | Extract |
|---|---|---|
| 1 | [Apple Support 122756](https://support.apple.com/en-us/122756) + [WWDC25-314](https://developer.apple.com/videos/play/wwdc2025/314/) | Which APIs are post-quantum by default; `nscurl`; the warning about large ClientHellos |
| 2 | [Google: PQC in Android](https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/) + [conscrypt#1452](https://github.com/google/conscrypt/issues/1452) | What Android 17 covers and what it doesn't |
| 3 | [Mankowski, Wiggers & Moonsamy 2023](https://thomwiggers.nl/publication/tls-on-android/tls-on-android.pdf) | Their pipeline (hotspot + tshark, 5-minute sessions, background calibration) and numbers to compare against |
| 4 | [Mind the Gap, IMC 2026](https://arxiv.org/html/2607.29005v1) | Sector and country numbers; excluded apps/APIs; latency deltas on cloud paths |
| 5 | [Pradeep et al., IMC 2022](https://dl.acm.org/doi/10.1145/3517745.3561439) | Pin-detection method (NSC, SPKI regex, crt.sh); finance prevalence; CA vs leaf |
| 6 | [Strauss et al. 2025](https://arxiv.org/pdf/2506.00790) | Static crypto rules (for G6); what they didn't cover |
| 7 | [Blanco-Romero et al. 2026](https://arxiv.org/abs/2603.01091) | HNDL cost numbers; resumption modes (G7, G15) |
| 8 | [Cloudflare PQ 2025](https://blog.cloudflare.com/pq-2025/) + [Radar](https://radar.cloudflare.com/post-quantum) | The Chrome Android delay; the origin-side gap; per-country/ASN data |
| 9 | [RFC 10024](https://www.rfc-editor.org/info/rfc10024/) | Exact codepoints and message sizes |
| 10 | [Dubey & Varshney 2026](https://arxiv.org/abs/2606.16473), [Loizou & Ghadafi 2026](https://arxiv.org/abs/2608.02147) | Server-side baselines to contrast with |
| 11 | [Li et al., USENIX Security 2016](https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/li) + [notification best practices (arXiv 2106.08029)](https://arxiv.org/pdf/2106.08029) | How to design G13 |
| 12 | [quantum-bank PR #8](https://github.com/joaobsjunior/quantum-bank/pull/8), [tldr.fail](https://tldr.fail/), [JEP 527](https://openjdk.org/jeps/527) | Flutter status (to verify), middlebox bugs, Java-server post-quantum |
| 13 | The Bangladesh Bank ICT Security Guideline v4.0 ([guideline list](https://www.bb.org.bd/en/index.php/about/guidelist)) | What it requires for crypto in transit; whether post-quantum is mentioned (for recommendations) |

---

### The very next 3 actions
1. `python n1_tools.py selftest`, then write `data/baseline.md` for your phones.
2. Pilot capture of Chrome + bKash (Phase 1), then run `n1_tools.py pcap`.
3. Send the faculty the pitch (A2) with this plan, and ask about IRB for G2/G14.
