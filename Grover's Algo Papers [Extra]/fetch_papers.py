"""Build the Path_3 literature collection: Semantic Scholar metadata + PDFs + README index + BibTeX.

Run:  S2_API_KEY=... python fetch_papers.py      (re-runnable: cached metadata and existing PDFs are skipped)
Key is read from the environment so it never lands in git.
"""
import json, os, re, sys, time, unicodedata, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).parent
KEY = os.environ.get("S2_API_KEY") or sys.exit("set S2_API_KEY")
API = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,authors,year,venue,externalIds,openAccessPdf,citationCount,url,citationStyles"
UA = {"User-Agent": "Mozilla/5.0 (CSE499 literature review)"}

THEMES = {
    1: "01_Grover_Foundations",
    2: "02_Search_With_Priors_SuperQuadratic",
    3: "03_Guessing_Theory_Metrics",
    4: "04_Parallel_Depth_Limits_Cost_Models",
    5: "05_Grover_Resource_Estimates_Practical_Cost",
    6: "06_Password_Guessing_Models",
    7: "07_Password_Hashing_MHF_Quantum",
    8: "08_QRAM_State_Preparation_Loaders",
    9: "09_SideChannel_Key_Enumeration_Leakage",
}

# (theme, S2 id or None -> title search, title, explicit PDF url or None, why it matters for Path_3)
PAPERS = [
    (1, "ARXIV:quant-ph/9605043", "A fast quantum mechanical algorithm for database search", None, "The algorithm itself"),
    (1, "ARXIV:quant-ph/9701001", "Strengths and weaknesses of quantum computing", None, "BBBV lower bound: Omega(sqrt N) for unstructured search"),
    (1, "ARXIV:quant-ph/9605034", "Tight bounds on quantum searching", None, "BBHT: unknown number of solutions, exact success curve"),
    (1, "ARXIV:quant-ph/9711070", "Grover's quantum searching algorithm is optimal", None, "Zalka: exact optimality + parallel bound; upper half of the budget sandwich (Q*1, RQ1)"),
    (1, "ARXIV:quant-ph/0005055", "Quantum amplitude amplification and estimation", None, "Amplitude amplification from a non-uniform start state A (the loader framing, Q*2)"),
    (2, "ARXIV:0908.3066", "Quantum search with advice", None, "Montanaro: 'exponential' average-case speedups with a prior; origin of super-quadratic claims"),
    (2, "ARXIV:2009.08721", "Quantum search with prior knowledge", None, "He-Zhang-Sun: optimal success with exactly T queries for any prior (budgeted view)"),
    (2, "ARXIV:2509.06549", "Super-Quadratic Quantum Speed-ups and Guessing Many Likely Keys", None, "GMN: s > 2 for passwords/Kyber/LPN; main target of Q*1"),
    (2, "ARXIV:2609.28226", "Pinpointing Super-Quadratic Quantum Enumeration Speedups: Exact and Certified Evaluation of the Guessing-Moment Exponent under Product-Distribution Advice", None, "Schubert et al. 2026: exponents up to 3.97 on ML-KEM/ML-DSA leakage; week-1 kill test"),
    (2, None, "Quantum Key Search with Side Channel Advice", "https://eprint.iacr.org/2017/171.pdf", "Martin et al.: budgeted search with advice is quadratic; QRAM-based product-prior loader"),
    (2, None, "Towards Quantum Large-Scale Password Guessing on Real-World Distributions", "https://eprint.iacr.org/2021/1299.pdf", "Duermuth et al.: quantum password guessing, hash-call cost only (no depth)"),
    (2, "ARXIV:2001.03598", "Guesswork with Quantum Side Information", None, "Quantum guesswork theory; information-theoretic side of guessing"),
    (2, None, "A Hybrid Lattice Basis Reduction and Quantum Search Attack on LWE", "https://eprint.iacr.org/2017/221.pdf", "Quantum search over non-uniform LWE secrets (Kyber/LPN angle of GMN)"),
    (3, "DOI:10.1109/18.481781", "An inequality on guessing and its application to sequential decoding", None, "Arikan: guessing moments vs Renyi entropy (basis of s exponents)"),
    (3, None, "Guesswork and entropy", None, "Malone-Sullivan: guesswork of Markov sources (O6)"),
    (3, "DOI:10.1109/SP.2012.49", "The Science of Guessing: Analyzing an Anonymized Corpus of 70 Million Passwords", "https://www.jbonneau.com/doc/B12-IEEESP-analyzing_70M_anonymized_passwords.pdf", "Bonneau: why guessing entropy is the wrong metric; partial guessing (template for the critique)"),
    (3, None, "Zipf's Law in Passwords", None, "Wang et al.: Zipf prior used by GMN for LinkedIn"),
    (4, "ARXIV:1309.6116", "Optimal parallel quantum query algorithms", None, "Jeffery-Magniez-de Wolf: parallel query lower bounds (RQ2, O1)"),
    (4, "ARXIV:quant-ph/0407217", "Quantum search for multiple items using parallel queries", None, "Grover-Radhakrishnan: parallel-query search"),
    (4, None, "Quantum Lattice Enumeration in Limited Depth", "https://eprint.iacr.org/2023/1423.pdf", "Bindel et al. CRYPTO 2024: precedent for a limited-depth re-analysis of a quantum speedup"),
    (4, "ARXIV:2608.19158", "Quantum Speedups Require Structure or Depth", None, "Blanc et al. 2026: big unstructured speedups need depth (complexity support for Q*1)"),
    (4, "ARXIV:2011.04149", "Focus beyond quadratic speedups for error-corrected quantum advantage", None, "Babbush et al.: quadratic speedups die under fault-tolerance overheads"),
    (4, "ARXIV:2203.04975", "Quantifying Grover speed-ups beyond asymptotic analysis", None, "Cade et al.: concrete Grover crossover points"),
    (4, None, "Reassessing Grover's Algorithm", "https://eprint.iacr.org/2017/811.pdf", "Fluhrer: parallel Grover cost scaling"),
    (4, None, "Quantum cryptanalysis in the RAM model: Claw-finding attacks on SIKE", "https://eprint.iacr.org/2019/103.pdf", "Jaques-Schanck: G-cost / DW-cost models and QRAM costing"),
    (4, None, "Submission Requirements and Evaluation Criteria for the Post-Quantum Cryptography Standardization Process", "https://csrc.nist.gov/CSRC/media/Projects/Post-Quantum-Cryptography/documents/call-for-proposals-final-dec-2016.pdf", "NIST (2016) PQC call for proposals: source of MAXDEPTH 2^40-2^96"),
    (5, "ARXIV:1512.04965", "Applying Grover's algorithm to AES: quantum resource estimates", None, "Grassl et al.: first AES Grover oracle costing"),
    (5, "ARXIV:1910.01700", "Implementing Grover oracles for quantum key search on AES and LowMC", None, "Jaques et al. EUROCRYPT 2020: AES under MAXDEPTH; N*D^2*W/MAXDEPTH form"),
    (5, "ARXIV:1603.09383", "Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3", None, "Amy et al.: hash oracle depth (KDF oracle cost, A1)"),
    (5, "ARXIV:1902.02332", "Benchmarking the quantum cryptanalysis of symmetric, public-key and hash-based cryptographic schemes", None, "Gheorghiu-Mosca: physical cost data behind NAP Table 4.1 (PBKDF2)"),
    (5, None, "On the practical cost of Grover for AES key recovery", "https://csrc.nist.gov/csrc/media/Events/2024/fifth-pqc-standardization-conference/documents/papers/on-practical-cost-of-grover.pdf", "UK NCSC, NIST PQC conference 2024: MAXDEPTH 2^48 = 8.9 years at 1 us; Grover on AES impractical"),
    (5, "ARXIV:2005.05911", "An Economic Model for Quantum Key-Recovery Attacks against Ideal Ciphers", None, "Harsha-Blocki: economic attacker model (O3)"),
    (5, None, "Quantum Implementation of SHA-1", "https://eprint.iacr.org/2025/1415.pdf", "SHA-1 circuit depth ~9k: oracle depth for WPA2/PBKDF2-SHA1 rows of A1"),
    (5, None, "Quantum implementation of Keccak-f(25) for emulator and quantum hardware, and application to quantum password cracking", "https://eprint.iacr.org/2026/2085.pdf", "Chenu-Chizzini (EU JRC) 2026: nearest toy model (uniform prior, no depth cap) for instrument T"),
    (5, None, "Quantum Computing: Progress and Prospects", "https://nap.nationalacademies.org/catalog/25196", "National Academies 2019, Table 4.1: PBKDF2 Grover = 2.3e7 years (free PDF behind NAP login)"),
    (6, "DOI:10.1109/SP.2009.8", "Password Cracking Using Probabilistic Context-Free Grammars", None, "PCFG model: a prior Q*2 must load coherently"),
    (6, "DOI:10.1007/978-3-319-15618-7_10", "OMEN: Faster Password Guessing Using an Ordered Markov Enumerator", None, "Markov enumerator: classical counterpart of a coherent ranker (Q*2, O2)"),
    (6, "DOI:10.1145/2810103.2813631", "Monte Carlo Strength Evaluation: Fast and Reliable Password Checking", None, "Classical guess numbers at scale -> quantum guess numbers for free (A1 4.1)"),
    (6, None, "Fast, Lean, and Accurate: Modeling Password Guessability Using Neural Networks", "https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_melicher.pdf", "Neural password models: state-of-the-art priors"),
    (6, None, "On the Economics of Offline Password Cracking", None, "Blocki-Harsha-Zhou: rational attacker stopping rule (budgeted metric, O3)"),
    (7, None, "Stronger key derivation via sequential memory-hard functions", "https://www.tarsnap.com/scrypt/scrypt.pdf", "scrypt original"),
    (7, "DOI:10.1109/EuroSP.2016.31", "Argon2: New Generation of Memory-Hard Functions for Password Hashing and Other Applications", "https://raw.githubusercontent.com/P-H-C/phc-winner-argon2/master/argon2-specs.pdf", "Argon2 i/d/id (O5)"),
    (7, None, "A Future-Adaptable Password Scheme", "https://www.usenix.org/legacy/events/usenix99/provos/provos.pdf", "Provos-Mazieres, USENIX 1999 (bcrypt): no quantum circuit exists yet (A1 4.3)"),
    (7, None, "Scrypt is Maximally Memory-Hard", "https://eprint.iacr.org/2016/989.pdf", "Classical proof that O4 asks to lift to the QROM"),
    (7, None, "Efficiently Computing Data-Independent Memory-Hard Functions", "https://eprint.iacr.org/2016/115.pdf", "Alwen-Blocki: Argon2i weakness (classical side of O5)"),
    (7, "ARXIV:2110.04191", "The Parallel Reversible Pebbling Game: Analyzing the Post-Quantum Security of iMHFs", None, "Blocki-Holman-Lee: reversible pebbling model for quantum MHF cost"),
    (7, None, "Data-Dependent Memory-Hard Functions: Sustained Space and Cumulative Complexity Trade-offs in the Parallel Random Oracle Model", "https://eprint.iacr.org/2026/1724.pdf", "Blocki-Holman 2026: dMHFs in the PROM"),
    (7, None, "Optimized Quantum Circuit for Quantum Security Strength Analysis of Argon2", "https://eprint.iacr.org/2023/1150.pdf", "Argon2 Grover circuit (A1 oracle depth)"),
    (7, None, "Grover on Scrypt", None, "Scrypt Grover circuit (A1 oracle depth)"),
    (7, None, "On the Compressed-Oracle Technique, and Post-Quantum Security of Proofs of Sequential Work", "https://eprint.iacr.org/2020/1305.pdf", "Quantum sequentiality of hash chains: why stretching resists Grover (A1 4.2, O4)"),
    (7, "ARXIV:2301.05680", "Cumulative Memory Lower Bounds for Randomized and Quantum Computation", None, "Quantum cumulative-memory lower bounds (O4 toolkit)"),
    (8, "ARXIV:0708.1879", "Quantum random access memory", None, "Bucket-brigade QRAM"),
    (8, "ARXIV:2305.10310", "QRAM: A Survey and Critique", None, "Jaques-Rattew: active QRAM erases advantage (O5, loader cost)"),
    (8, "ARXIV:quant-ph/0208112", "Creating superpositions that correspond to efficiently integrable probability distributions", None, "Grover-Rudolph state preparation: tilted-chain loader building block (RQ4)"),
    (8, "ARXIV:1805.03662", "Encoding Electronic Spectra in Quantum Circuits with Linear T Complexity", None, "QROM + alias-sampling state preparation (top-L list loader)"),
    (8, "ARXIV:1812.00954", "Trading T-gates for dirty qubits in state preparation and unitary synthesis", None, "QROAM: cheapest table-lookup loaders"),
    (9, None, "An optimal Key Enumeration Algorithm and its Application to Side-Channel Attacks", "https://eprint.iacr.org/2011/610.pdf", "Classical key enumeration with side-channel posteriors (A2)"),
    (9, None, "Simpler and More Efficient Rank Estimation for Side-Channel Security Assessment", "https://eprint.iacr.org/2014/920.pdf", "Rank curves: the classical input the budget sandwich needs (A2)"),
    (9, None, "Study of Deep Learning Techniques for Side-Channel Analysis and Introduction to ASCAD Database", "https://eprint.iacr.org/2018/053.pdf", "ASCAD: public template posteriors for A2 experiments"),
    (9, None, "Lest We Remember: Cold Boot Attacks on Encryption Keys", "https://www.usenix.org/legacy/event/sec08/tech/full_papers/halderman/halderman.pdf", "Cold-boot priors on AES keys (dependent priors, A2)"),
]

_last = 0.0
def s2(path, body=None):
    """One Semantic Scholar call, spaced >1.1 s apart (key limit: 1 req/s), retried on 429/5xx."""
    global _last
    for attempt in range(5):
        time.sleep(max(0, 1.1 - (time.time() - _last)))
        _last = time.time()
        req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                                     headers={"x-api-key": KEY, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            if e.code not in (429, 500, 502, 503, 504): raise
            time.sleep(2 ** attempt)
        except OSError:  # timeouts, resets, URLError
            time.sleep(2 ** attempt)
    return None

def fetch_meta():
    """S2 record per paper, cached in papers.json keyed by S2 id or title, so editing PAPERS only fetches new entries."""
    path = HERE / "papers.json"
    cache = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    ids = [p[1] for p in PAPERS if p[1] and p[1] not in cache]
    if ids:
        for pid, m in zip(ids, s2(f"/paper/batch?fields={FIELDS}", {"ids": ids}) or []):
            if m: cache[pid] = m
    for _, pid, title, _, _ in PAPERS:
        key = pid or title
        if key not in cache:  # no id, or id unknown to S2 -> title match; {} records a permanent miss
            r = s2(f"/paper/search/match?query={urllib.parse.quote(title)}&fields={FIELDS}")
            cache[key] = ((r or {}).get("data") or [{}])[0]
            print(("ok  " if cache[key] else "MISS") + f" {title[:70]}")
    path.write_text(json.dumps(cache, indent=1), encoding="utf-8")
    return [{"theme": t, "title": title, "pdf": pdf, "why": why, "s2": cache[pid or title]}
            for t, pid, title, pdf, why in PAPERS]

def slug(s, n=6):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return "_".join(re.findall(r"[A-Za-z0-9]+", s)[:n])

def download(urls, dest):
    for u in urls:
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90) as r:
                data = r.read()
            if data[:4] == b"%PDF":
                dest.write_bytes(data)
                return u
        except Exception as e:
            print(f"     fail {u}: {e}")
        time.sleep(1)
    return None

def main():
    meta = fetch_meta()
    for i, e in enumerate(meta, 1):
        m = e["s2"] or {}
        first = m["authors"][0]["name"].split()[-1] if m.get("authors") else "NA"
        e["file"] = f"{THEMES[e['theme']]}/{i:02d}_{slug(first, 1)}{m.get('year') or ''}_{slug(e['title'])}.pdf"
        dest = HERE / e["file"]
        dest.parent.mkdir(exist_ok=True)
        if dest.exists():
            e["got"] = True; continue
        ext = m.get("externalIds") or {}
        urls = [e["pdf"], ext.get("ArXiv") and f"https://arxiv.org/pdf/{ext['ArXiv']}",
                (m.get("openAccessPdf") or {}).get("url")]
        src = download([u for u in dict.fromkeys(urls) if u], dest)
        e["got"] = bool(src)
        print(f"{'PDF ' if src else 'NONE'} {i:02d} {e['file']}")
    write_index(meta)

def write_index(meta):
    got = sum(e["got"] for e in meta)
    out = [f"# Path_3 literature collection ({len(meta)} papers, {got} PDFs downloaded)\n",
           "Built by `fetch_papers.py` from Semantic Scholar metadata. Themes map to `../Grover_Research_Gaps.md` "
           "(Q*1 super-quadratic under limits, Q*2 loaders, A1 passwords, A2 leakage, O1-O6 open problems).\n",
           "Titles are curated; author, year, venue and citation counts come from Semantic Scholar.\n"]
    missing = [(i, e) for i, e in enumerate(meta, 1) if not e["got"]]
    if missing:
        out += ["## Download manually\n",
                "Scripts can't fetch these: ePrint and MDPI show a browser check, and the rest are paywalled. "
                "Open each link in a browser, save the PDF at the path shown, then re-run `fetch_papers.py` to refresh this index.\n",
                *[f"- [ ] **{i}.** [{e['title']}]({e['pdf'] or ((e['s2'] or {}).get('openAccessPdf') or {}).get('url') or (e['s2'] or {}).get('url', '')}) → `{e['file']}`"
                  for i, e in missing]]
    bib = []
    for t, folder in THEMES.items():
        out.append(f"\n## {folder.replace('_', ' ')}\n\n| # | Paper | First author | Year | Venue | Cites | Why it matters | PDF |\n|---|---|---|---|---|---|---|---|")
        for i, e in enumerate(meta, 1):
            if e["theme"] != t: continue
            m = e["s2"] or {}
            authors = m.get("authors") or []
            who = (authors[0]["name"] + (" et al." if len(authors) > 1 else "")) if authors else ""
            link = m.get("url") or e["pdf"] or ""
            title = e["title"].replace("|", "/")
            pdf = f"[pdf](<{e['file']}>)" if e["got"] else "**manual**"
            out.append(f"| {i} | [{title}]({link}) | {who} | {m.get('year') or ''} | {(m.get('venue') or '').replace('|', '/')} | "
                       f"{m.get('citationCount', '')} | {e['why']} | {pdf} |")
            if (m.get("citationStyles") or {}).get("bibtex"):
                bib.append(m["citationStyles"]["bibtex"].replace(m.get("title") or e["title"], e["title"]))
    (HERE / "README.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    (HERE / "references.bib").write_text("\n\n".join(bib) + "\n", encoding="utf-8")
    print(f"\n{got}/{len(meta)} PDFs, {len(bib)} BibTeX entries")

if __name__ == "__main__":
    main()
