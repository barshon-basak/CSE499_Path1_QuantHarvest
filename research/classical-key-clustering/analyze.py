"""Generate evidence-based report and inference CSV from completed enumeration."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent/'.deps'))
import csv,json,math,hashlib
import numpy as np
from scipy.stats import t,binom
from clustering import ROOT,N,write_csv,Engine
import mini_aes

def main():
    res=ROOT/'results'
    rows=list(csv.DictReader((res/'per_plaintext.csv').open()))
    metrics=['occupied_ciphertexts','fraction_keys_in_clusters_ge2','colliding_key_pairs','max_cluster_size']
    def vals(cipher,metric,cat='all'):
        return np.array([float(r[metric]) for r in rows if r['cipher']==cipher and (cat=='all' or r['category']==cat)])
    ci=[]
    for metric in metrics:
        for c in ('mini_aes','saes','mini_minus_saes'):
            a=vals(c,metric,'random') if c!='mini_minus_saes' else vals('mini_aes',metric,'random')-vals('saes',metric,'random')
            # SRS without replacement from the 65527 non-prespecified plaintexts.
            se=a.std(ddof=1)/math.sqrt(100)*math.sqrt((65527-100)/65527)
            half=float(t.ppf(.975,99)*se)
            ci.append(dict(cipher=c,metric=metric,n=100,mean=float(a.mean()),sample_sd=float(a.std(ddof=1)),
                           standard_error=float(se),ci95_low=float(a.mean()-half),ci95_high=float(a.mean()+half)))
    write_csv(res/'random_plaintext_confidence.csv',ci)
    q0=math.exp(N*math.log1p(-1/N))
    expected=dict(occupied_ciphertexts=N*(1-q0),fraction_keys_in_clusters_ge2=1-math.exp((N-1)*math.log1p(-1/N)),
                  colliding_key_pairs=(N-1)/2,mean_cluster_known_key=2-1/N,
                  pair_sd=math.sqrt((N*(N-1)/2)*(1/N)*(1-1/N)),empty_ciphertexts=N*q0)
    (res/'ideal_exact_metrics.json').write_text(json.dumps(expected,indent=2))
    prose=[]
    engine=Engine(mini_aes)
    for p,c,k in [(0xBAD0,0xE7AA,0xF5E2),(0x9C63,0x72C6,0xC3F0)]:
        keys=np.flatnonzero(engine.encrypt(p)==c)
        prose.append(dict(plaintext=f'{p:04X}',ciphertext=f'{c:04X}',key=f'{k:04X}',
                          computed_ciphertext=f'{mini_aes.encrypt(p,k):04X}',
                          actual_keys=' '.join(f'{x:04X}' for x in keys)))
    write_csv(res/'prose_checks.csv',prose)
    lines=['# Executed classical key-clustering study','',
      'Executed on 23 October 2026. Both ciphers: 109 distinct plaintexts × 65,536 keys, totaling **14,286,848 encryptions**. No Grover computation. All saved groups were reconstructed and compared with the encryption arrays.','',
      '## Main findings','',
      '| Across all 109 plaintexts | Mini-AES | S-AES | Ideal fixed-plaintext expectation |',
      '|---|---:|---:|---:|']
    for metric,label,fmt in [('occupied_ciphertexts','Occupied ciphertexts (mean)',',.2f'),('fraction_keys_in_clusters_ge2','Keys in clusters ≥2 (mean fraction)','.6f'),('colliding_key_pairs','Colliding key pairs (mean)',',.2f')]:
        lines.append(f'| {label} | {vals("mini_aes",metric).mean():{fmt}} | {vals("saes",metric).mean():{fmt}} | {expected[metric]:{fmt}} |')
    lines+=['| Largest observed cluster | 9 | 9 | Maximum is random; simulated 95% interval 7–9 |','',
      'Both ciphers have occupancy distributions close to the ideal binomial/Poisson(1) shape. Collisions are expected even in an ideal cipher: roughly 63.2% of keys share their observed ciphertext with another key. They do not by themselves establish equivalent full encryption functions, reduced master-key entropy, a practical attack, or a weakness relative to AES.','',
      'The means show modest, systematic departures from the ideal expectation (slightly more occupied ciphertexts and fewer colliding pairs). Thus “similar to ideal” does not mean “exactly ideal.” These are deterministic two-round toy ciphers, and these measurements do not establish pseudorandomness.','',
      '## Variation across plaintexts','',
      '| Metric | Mini-AES mean ± SD [min,max] | S-AES mean ± SD [min,max] |','|---|---|---|']
    for metric in metrics:
        a,b=vals('mini_aes',metric),vals('saes',metric)
        lines.append(f'| {metric} | {a.mean():.6g} ± {a.std(ddof=1):.6g} [{a.min():.6g}, {a.max():.6g}] | {b.mean():.6g} ± {b.std(ddof=1):.6g} [{b.min():.6g}, {b.max():.6g}] |')
    lines+=['','## Random-plaintext inference','',
      'The five paper and four structured plaintexts are deliberate choices. Inference below uses only the other 100: a simple random sample without replacement from the 65,527 remaining plaintexts. Intervals are approximate 95% Student-t intervals with finite population correction. They quantify uncertainty about each fixed cipher’s mean across that plaintext population, not across possible cipher designs. Paired intervals compare the same plaintexts. They are exploratory and not adjusted for multiple metrics.','',
      '| Population/metric | Random sample mean | Approximate 95% interval |','|---|---:|---:|']
    for r in ci:
        if r['metric'] in ('colliding_key_pairs','occupied_ciphertexts'):
            lines.append(f'| {r["cipher"]}: {r["metric"]} | {r["mean"]:.2f} | [{r["ci95_low"]:.2f}, {r["ci95_high"]:.2f}] |')
    lines+=['',
      'The paired colliding-pair interval includes zero: this sample does not resolve a difference in mean pair collisions between the ciphers. Each cipher’s estimated mean pair count is below the ideal mean 32,767.5. Effect sizes, sampling design and interval assumptions matter more here than an unqualified significance label.','',
      'The 2,000 independent ideal occupancy simulations provide pointwise reference intervals for ONE plaintext. They are not simultaneous confidence bands across 109 plaintexts. Actual ciphers reuse keys and schedules across plaintexts; an ideal family also has within-key permutation constraints across distinct plaintexts. This project simulates the exact fixed-plaintext marginal, not a joint model of all plaintexts. No independent-plaintext ideal-model aggregate p-value is claimed.','',
      '## Paper reproduction','',
      'Source: Kiran et al. (2026), user PDF, Tables 9–11 on page 7. Every printed key is valid. Eight of nine printed groups are exhaustive. Table 11’s FF48→7492 group is actually {7E7C,F5E2}; the table lists only F5E2. All nine groups and exact flags appear in `results/paper_reproduction.csv`.','',
      'E0F7→8816 has exactly {A233,C0E4,E534}. The prose/table disagreements and the incorrect B→4 entry in the paper’s S-AES S-box are detailed in `SPECIFICATION.md`. The implementation uses authoritative S-AES B→3. The extra prose claim BAD0→E7AA under F5E2 does not reproduce: its ciphertext is 2568. The only key for BAD0→E7AA is 57A2. Phan’s original 9C63→72C6 example has exactly {98DD,C3F0,E873}, matching the 2026 paper’s separate example. These checks appear in `results/prose_checks.csv`.','',
      '## Correct ideal model and the two perspectives','',
      'Let N=65,536 ciphertext values and K=65,536 independently keyed random permutations. At one fixed plaintext, outputs across keys are independent uniform ciphertexts. This is balls into bins; it is NOT one permutation mapping keys onto ciphertexts. Let n_c be the number of keys yielding c and H_j the number of ciphertexts with n_c=j, including H_0.','',
      '- A random ciphertext sees n_c ~ Binomial(K,1/N), approximately Poisson(1). E[H_j]=N·Pr(n_c=j). Mean size is exactly 1, including empty groups. Expected occupied ciphertexts: N·[1−(1−1/N)^K].',
      '- A uniformly random known key sees the size-biased group containing its own ciphertext: 1+Binomial(K−1,1/N), approximately 1+Poisson(1). Its expected size is 2−1/N. Probability of ≥2 is 1−(1−1/N)^(K−1), approximately 0.63212. This differs from a random nonempty ciphertext, which instead sees the binomial conditioned on ≥1.',
      '- Colliding unordered key pairs: sum_c n_c(n_c−1)/2. Ideal expectation is choose(K,2)/N=32,767.5. Variance is choose(K,2)(1/N)(1−1/N); pair-match indicators are pairwise independent at a fixed plaintext, even when two pairs share a key.',
      '- The ciphertext-weighted fraction in clusters ≥2 is 1−Pr(n_c=0)−Pr(n_c=1), approximately 0.26424. It must not be confused with the key-weighted fraction ≈0.63212.',
      '- Empirically, keys in clusters ≥2 = K−H_1; known-key mean cluster size = sum_c n_c²/K = 1+2·pairs/K. Ciphertext entropy and expected log2 candidate count are also included in the metric CSV.','',
      'The binomial histogram bins are dependent because occupancies sum to K. Ordinary independent Poisson-bin chi-square assumptions are not used. Single-pair clusters are not proof of equivalent keys: equivalence requires agreement on every plaintext; testing surviving groups against further common plaintext/ciphertext pairs is a separate next phase.','',
      '## Reproducibility and limits','',
      'Seed 20261023; Python `random.Random(seed).sample` selects 100 distinct values from an ascending list excluding the nine fixed values. `results/plaintexts.csv` freezes the exact sample and order. Baseline uses NumPy PCG64 seed 20261024. Versions and input hash are recorded in the manifest.','',
      'Only two rounds and the specified conventions are studied. All-key enumeration is exhaustive for each selected plaintext, but all 65,536 plaintexts were not surveyed. Structured and paper cases are not a random population sample. Toy-cipher conclusions cannot be extrapolated to full AES or practical security. No relation analysis, equivalent-key classification, or quantum experiment is claimed.','',
      'Scalar and vector implementations are separate, but share the specification constants and field helper; the field helper has an independent polynomial-reduction test. Published vectors provide external validation. Five complete fixed-key plaintext permutations are checked for each cipher; that is not an exhaustive test of every key/plaintext combination.','',
      '![Two sampling perspectives](plots/occupancy_perspectives.png)','',
      '![Plaintext variation](plots/plaintext_variation.png)','']
    (ROOT/'FINDINGS.md').write_text('\n'.join(lines),encoding='utf-8')
    print('Report and confidence CSV generated.')

if __name__=='__main__':main()
