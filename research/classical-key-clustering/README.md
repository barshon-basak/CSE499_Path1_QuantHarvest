# Classical key clustering: Mini-AES versus S-AES

An executed, reproducible study of the **16-bit, two-round Mini-AES used by Kiran et al. (2026)** and authoritative **16-bit, two-round S-AES**. Start with [FINDINGS.md](FINDINGS.md) for results and [SPECIFICATION.md](SPECIFICATION.md) for the paper audit and exact conventions. No Grover simulation is performed.

## Run from a fresh environment

Python 3.12 was used. In a terminal, change to this folder, then:

```text
python -m venv .venv
```

Activate the environment (`.venv\Scripts\activate` on Windows; `source .venv/bin/activate` on macOS/Linux), then:

```text
python -m pip install -r requirements.txt
python tests.py
python clustering.py --baseline-replicates 2000
python tests.py
python analyze.py
```

Run these commands sequentially. The post-run test checks all 218 saved mappings; running tests while enumeration is writing partial output will correctly fail its completeness check. Output files use stable names and are replaced on reruns. Use a clean copy of the project when changing the design, so stale mapping files do not mix with another experiment. Scalar `mini_aes.py`, `saes.py` and `common.py` use only Python's standard library; enumeration and plots need the pinned packages. Bundled results allow reading findings without installing anything.

The original PDF is not required to rerun encryption or analysis. If its original path is available, the run records its hash; otherwise the new manifest's paper hash is null. The archived original run's manifest records the actual inspected file. `analyze.py` reads only generated data and code constants.

## Experimental design

For each cipher, enumerate every integer key 0..65535 at each plaintext. Fixed paper values: E0F7, FF48, 0B5D, A0D5, 60B3. Structured values: 0000, FFFF, AAAA, 5555. Select 100 additional distinct values without replacement from the ascending remaining domain using Python `random.Random(20261023).sample`. Exact order and category are saved in `results/plaintexts.csv`. Total: 109 distinct plaintexts per cipher, 14,286,848 evaluations.

Ideal baseline: at one fixed plaintext, independently keyed random permutations give independent uniform outputs across keys. Simulate 2000 arrays of 65536 independent uniform outputs with PCG64 seed 20261024. The exact single-bin law is Binomial(65536,1/65536), approximately Poisson(1), and mean unordered pair collisions is 32767.5. Full derivation, two sampling perspectives, design-based random-plaintext intervals and limits are in FINDINGS.md.

## Files and outputs

| Path | Contents |
|---|---|
| `mini_aes.py`, `saes.py` | Scalar encrypt/decrypt and key expansion |
| `common.py` | Field arithmetic and scalar layers |
| `clustering.py` | Independent vector implementation, enumeration, summaries, ideal baseline |
| `tests.py` | 13 test methods including published vectors, all-key agreement, permutation checks and full mapping audit |
| `plotting.py` | Four figures, each PNG and SVG |
| `analyze.py` | Findings, exact ideal metrics, random-plaintext confidence intervals and extra prose checks |
| `results/per_plaintext.csv` | All 218 cipher/plaintext records and metrics |
| `results/cluster_distributions.csv.gz` | Complete empirical distributions, sizes 0 through each observed maximum |
| `results/aggregate_metrics.csv` | Mean, sample SD, median, min and max, for all/paper/structured/random categories separately |
| `results/aggregate_distributions.csv.gz` | Pooled histogram counts, mean per-plaintext counts, key and ciphertext fractions by category |
| `results/paired_differences.csv` | Mini-AES minus S-AES for each matched plaintext |
| `results/random_plaintext_confidence.csv` | Approximate 95% finite-population Student-t intervals using only 100 random plaintexts |
| `results/paper_reproduction.csv` | Nine exact Table 9–11 key group comparisons, with validity and completeness flags |
| `results/prose_checks.csv` | Additional BAD0 and Phan example groups |
| `results/ideal_distribution.csv` | Exact binomial and Poisson probabilities for sizes 0..31; theoretical tail beyond 31 is not stored here |
| `results/ideal_exact_metrics.json` | Exact finite-N theoretical expectations and pair SD |
| `results/ideal_simulations.csv`, `ideal_intervals.csv` | Individual baseline replicates and pointwise 95% simulation reference intervals |
| `results/groups/*.npz` | Lossless ciphertext-to-all-keys mapping, including empty groups |
| `results/manifest.json`, `tests-final.txt`, `execution.log` | Run identity, environment, input hash, verification log and execution output |
| `SHA256SUMS.txt` | Packaged-file integrity hashes (excludes itself) |

All hex plaintext/key/ciphertext fields are exactly four hex digits, without a 0x prefix in generated CSV. Interpret them as hex strings, not decimal numbers. Empirical cluster sizes above the last saved size have zero frequency; size zero explicitly counts ciphertexts with no preimage key. The histograms use the ciphertext perspective; `key_count`/`key_fraction` weight a bin of size j by j.

## Query a preserved key group

```python
from clustering import keys_for
keys = keys_for('results/groups/mini_aes_E0F7.npz', 0x8816)
print([f'{int(k):04X}' for k in keys])
# ['A233', 'C0E4', 'E534']
```

Each `.npz` stores `keys` (65536 uint16 entries, sorted by ciphertext then key) and `offsets` (65537 uint32 entries). Ciphertext c's keys are `keys[offsets[c]:offsets[c+1]]`. Equal adjacent offsets represent an empty group. Keys occur exactly once. The last offset equals 65536 and cannot fit in uint16, so uint32 is intentional. Load with `allow_pickle=False`; there are no executable objects. This is a compact compressed sparse-row representation of the complete group mapping.

For later relation studies, query a group and test its keys on further COMMON plaintext/ciphertext pairs. Keys that agree on a single pair are candidate keys, not automatically equivalent encryption functions.

## Validation performed

Published vectors: Phan P=9C63, K=C3F0, C=72C6, and designer-attributed S-AES P=6F6B, K=A73B, C=0738. Key schedules, intermediate states, independent polynomial arithmetic and random round trips also pass. All 65536 keys at E0F7 agree between scalar and vector implementations for both ciphers. Five fixed-key full plaintext permutations are checked for each cipher. Every mapping is reconstructed and compared with its generated ciphertext array, with histogram conservation identities. The final suite passes all 13 tests.

The original pre-run log recorded a completeness failure because tests overlapped with output generation (44 of 218 mapping files existed then); all encryption tests passed. The final sequential validation passes, and this scheduling issue did not change cipher code or data. The intermediate log is omitted from the deliverable archive.

## Evidence limits

The paper's Mini-AES examples reproduce, but Table 11 omits key 7E7C for FF48→7492. Its S-AES S-box Table 1 has a B→4 typo; the authoritative B→3 is used. See SPECIFICATION.md for all observed discrepancies and primary links. The Sage report is context, not an implementation oracle. Clustering alone is normal for an ideal cipher with this block/key size; differences from an ideal marginal do not establish an attack or conclusions about full AES.

The source PDF remains unchanged at the user-provided path. The archive includes our specification audit and source hash/links, not the PDF, extracted text or rendered source pages. Existing synced project sources were not modified.
