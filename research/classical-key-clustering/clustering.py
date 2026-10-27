"""Reproducible exhaustive key occupancy experiment. Run: python clustering.py."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent / '.deps'))
import argparse, csv, hashlib, json, math, platform, random, time
import numpy as np
from scipy.stats import binom
import mini_aes, saes
from common import mul

N = 65536
SEED = 20261023
PAPER = [0xE0F7,0xFF48,0x0B5D,0xA0D5,0x60B3]
STRUCTURED = [0,0xFFFF,0xAAAA,0x5555]
ROOT = Path(__file__).resolve().parent
# Exact table transcription, checked on PDF page 7. Prose discrepancies are separate.
PAPER_ROWS = [
 (9,0xE0F7,0x8816,[0xC0E4,0xE534,0xA233]),
 (9,0xFF48,0x9334,[0xC0E4]),
 (9,0x0B5D,0xA75A,[0xC0E4,0xC2B2,0xC2BD]),
 (10,0xA0D5,0x9BC5,[0x4C8C]),
 (10,0x60B3,0x7204,[0x4C8C]),
 (10,0xE0F7,0x5F69,[0x4C8C,0xD7C8]),
 (11,0xA0D5,0xA72D,[0xF5E2]),
 (11,0x0B5D,0x55E7,[0xF5E2,0xEABF]),
 (11,0xFF48,0x7492,[0xF5E2])]

def sample_plaintexts():
    # Exclusion ensures exactly 109 different plaintexts; saved list is authoritative.
    pool = [p for p in range(N) if p not in PAPER+STRUCTURED]
    return PAPER+STRUCTURED+random.Random(SEED).sample(pool,100)

class Engine:
    """Independent vectorized nibble implementation, checked against scalar modules.

    No calls to scalar key expansion or scalar encryption. Only GF multiplication
    is shared; tests additionally check it against polynomial long division.
    """
    def __init__(self, cipher):
        self.cipher = cipher
        self.name = cipher.__name__
        self.box = np.array(cipher.SBOX,dtype=np.uint16)
        self.mul_d = np.array([mul(cipher.DIAGONAL,i) for i in range(16)],dtype=np.uint16)
        self.mul_o = np.array([mul(cipher.OFF,i) for i in range(16)],dtype=np.uint16)
        self.keys = np.arange(N,dtype=np.uint16)
        self.round_keys = self.expand(self.keys)

    def expand(self,k):
        out = [k]
        for rc in ((1,2) if self.name=='mini_aes' else (8,3)):
            a,b,c,d = [(k>>s)&15 for s in (12,8,4,0)]
            if self.name=='mini_aes':
                aa = a ^ self.box[d] ^ rc
                bb = b ^ aa
                cc = c ^ bb
                dd = d ^ cc
            else:
                aa = a ^ self.box[d] ^ rc
                bb = b ^ self.box[c]
                cc = c ^ aa
                dd = d ^ bb
            k = (aa<<12)|(bb<<8)|(cc<<4)|dd
            out.append(k)
        return out

    def ns_sr(self,x):
        a,b,c,d = [self.box[(x>>s)&15] for s in (12,8,4,0)]
        return (a<<12)|(d<<8)|(c<<4)|b

    def mc(self,x):
        a,b,c,d = [(x>>s)&15 for s in (12,8,4,0)]
        md,mo = self.mul_d,self.mul_o
        return ((md[a]^mo[b])<<12)|((mo[a]^md[b])<<8)|((md[c]^mo[d])<<4)|(mo[c]^md[d])

    def encrypt(self,p,round_keys=None):
        k0,k1,k2 = self.round_keys if round_keys is None else round_keys
        return self.ns_sr(self.mc(self.ns_sr(p ^ k0)) ^ k1) ^ k2

def metrics(counts):
    counts = np.asarray(counts,dtype=np.int64)
    if counts.shape != (N,) or np.any(counts<0) or counts.sum()!=N:
        raise ValueError('expected 65536 nonnegative occupancies totaling 65536')
    hist = np.bincount(counts,minlength=N+1)
    occupied = int(N-hist[0])
    pairs = int(np.sum(counts*(counts-1)//2))
    kcoll = int(N-hist[1])
    p = counts[counts>0]/N
    return dict(occupied_ciphertexts=occupied,empty_ciphertexts=int(hist[0]),
                occupancy_fraction=occupied/N,max_cluster_size=int(counts.max()),
                singleton_ciphertexts=int(hist[1]),keys_in_clusters_ge2=kcoll,
                fraction_keys_in_clusters_ge2=kcoll/N,colliding_key_pairs=pairs,
                pair_ratio_to_ideal=pairs/32767.5,
                mean_cluster_random_ciphertext=float(counts.mean()),
                mean_cluster_occupied_ciphertext=N/occupied,
                mean_cluster_known_key=1+2*pairs/N,
                ciphertext_entropy_bits=float(-np.sum(p*np.log2(p))),
                expected_log2_cluster_known_key=float(np.sum(p*np.log2(counts[counts>0])))), hist

def write_csv(path,rows):
    rows = list(rows)
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w = csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

def keys_for(path,ciphertext):
    """Read one group; empty groups are represented by equal adjacent offsets."""
    if not 0<=ciphertext<N:
        raise ValueError('invalid ciphertext')
    with np.load(path,allow_pickle=False) as z:
        o=z['offsets']; return z['keys'][o[ciphertext]:o[ciphertext+1]].copy()

def baseline(replicates):
    rng=np.random.Generator(np.random.PCG64(SEED+1))
    rows=[]
    for i in range(replicates):
        counts=np.bincount(rng.integers(0,N,N,dtype=np.uint32),minlength=N)
        m,_=metrics(counts); rows.append(dict(replicate=i,**m))
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline-replicates',type=int,default=2000)
    args=ap.parse_args()
    if args.baseline_replicates<100:
        ap.error('use at least 100 baseline replicates')
    started=time.perf_counter()
    results=ROOT/'results'; groups=results/'groups'
    groups.mkdir(parents=True,exist_ok=True)
    plain=sample_plaintexts()
    write_csv(results/'plaintexts.csv',
              [dict(index=i,plaintext=f'{p:04X}',category='paper' if i<5 else 'structured' if i<9 else 'random') for i,p in enumerate(plain)])
    rows=[]; dists=[]; paper=[]; all_hist={}
    for cipher in (mini_aes,saes):
        engine=Engine(cipher)
        for i,p in enumerate(plain):
            ciphertexts=engine.encrypt(p)
            counts=np.bincount(ciphertexts,minlength=N)
            m,hist=metrics(counts)
            category='paper' if i<5 else 'structured' if i<9 else 'random'
            rows.append(dict(cipher=cipher.__name__,plaintext=f'{p:04X}',category=category,**m))
            all_hist[cipher.__name__,p]=hist
            # Complete range 0..observed maximum, including zero-key ciphertexts.
            dists.extend(dict(cipher=cipher.__name__,plaintext=f'{p:04X}',cluster_size=j,
                              ciphertext_count=int(h),ciphertext_fraction=int(h)/N,
                              key_count=j*int(h),key_fraction=j*int(h)/N)
                         for j,h in enumerate(hist[:int(counts.max())+1]))
            order=np.argsort(ciphertexts,kind='stable').astype('<u2')
            offsets=np.concatenate(([0],np.cumsum(counts))).astype('<u4')
            np.savez_compressed(groups/f'{cipher.__name__}_{p:04X}.npz',keys=order,offsets=offsets)
            # Validate every saved mapping by lossless reconstruction.
            with np.load(groups/f'{cipher.__name__}_{p:04X}.npz',allow_pickle=False) as z:
                assert np.array_equal(np.sort(z['keys']),np.arange(N,dtype=np.uint16))
                reconstructed=np.empty(N,dtype=np.uint16)
                reconstructed[z['keys']]=np.repeat(np.arange(N,dtype=np.uint16),np.diff(z['offsets']).astype(int))
                assert np.array_equal(reconstructed,ciphertexts)
            if cipher is mini_aes:
                for table,pp,c,expected in PAPER_ROWS:
                    if p==pp:
                        actual=np.flatnonzero(ciphertexts==c).tolist()
                        paper.append(dict(table=table,plaintext=f'{p:04X}',ciphertext=f'{c:04X}',
                                          reported_keys=' '.join(f'{k:04X}' for k in expected),
                                          computed_keys=' '.join(f'{k:04X}' for k in actual),
                                          all_reported_valid=all(k in actual for k in expected),
                                          exact_group_match=set(expected)==set(actual),
                                          actual_cluster_size=len(actual)))
            if i%25==0: print(cipher.__name__,i+1,'/',len(plain),flush=True)
    write_csv(results/'per_plaintext.csv',rows)
    # Sizes beyond the saved maximum have zero frequency by definition.
    import gzip
    with gzip.open(results/'cluster_distributions.csv.gz','wt',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(dists[0]));w.writeheader();w.writerows(dists)
    del dists
    write_csv(results/'paper_reproduction.csv',sorted(paper,key=lambda r:(r['table'],next(i for i,x in enumerate(PAPER_ROWS) if x[0]==r['table'] and f'{x[1]:04X}'==r['plaintext']))))
    aggregate=[];adist=[]
    for cipher in ('mini_aes','saes'):
        for cat in ('all','paper','structured','random'):
            subset=[r for r in rows if r['cipher']==cipher and (cat=='all' or r['category']==cat)]
            for metric in [k for k in subset[0] if k not in ('cipher','plaintext','category')]:
                vals=np.array([r[metric] for r in subset],dtype=float)
                aggregate.append(dict(cipher=cipher,category=cat,metric=metric,n=len(vals),
                    mean=float(vals.mean()),sd=float(vals.std(ddof=1)),minimum=float(vals.min()),
                    median=float(np.median(vals)),maximum=float(vals.max())))
            hh=sum((all_hist[cipher,int(r['plaintext'],16)] for r in subset),np.zeros(N+1,dtype=np.int64))
            last=int(np.flatnonzero(hh)[-1])
            for j,h in enumerate(hh[:last+1]):
                adist.append(dict(cipher=cipher,category=cat,cluster_size=j,ciphertext_count=int(h),
                                  mean_ciphertexts_per_plaintext=int(h)/len(subset),
                                  ciphertext_fraction=int(h)/(N*len(subset)),key_fraction=j*int(h)/(N*len(subset))))
    write_csv(results/'aggregate_metrics.csv',aggregate)
    with gzip.open(results/'aggregate_distributions.csv.gz','wt',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(adist[0])); w.writeheader(); w.writerows(adist)
    # Exact finite binomial, not a random permutation of ciphertexts across keys.
    b=baseline(args.baseline_replicates)
    write_csv(results/'ideal_simulations.csv',b)
    write_csv(results/'ideal_distribution.csv',[
        dict(cluster_size=j,binomial_probability=float(binom.pmf(j,N,1/N)),
             expected_ciphertexts=N*float(binom.pmf(j,N,1/N)),
             poisson_probability=math.exp(-1)/math.factorial(j),
             known_key_probability=float(binom.pmf(j-1,N-1,1/N)) if j else 0)
        for j in range(32)])
    intervals=[]
    for metric in ('occupied_ciphertexts','fraction_keys_in_clusters_ge2','colliding_key_pairs','max_cluster_size'):
        vals=np.array([r[metric] for r in b])
        intervals.append(dict(metric=metric,replicates=len(b),mean=float(vals.mean()),
                              sd=float(vals.std(ddof=1)),q025=float(np.quantile(vals,.025)),q975=float(np.quantile(vals,.975))))
    write_csv(results/'ideal_intervals.csv',intervals)
    # Within-plaintext paired differences. Descriptive; shared keys induce dependence.
    differences=[]
    for p in plain:
        a=next(r for r in rows if r['cipher']=='mini_aes' and r['plaintext']==f'{p:04X}')
        s=next(r for r in rows if r['cipher']=='saes' and r['plaintext']==f'{p:04X}')
        differences.append(dict(plaintext=f'{p:04X}',category=a['category'],**{k:a[k]-s[k] for k in
            ('occupied_ciphertexts','fraction_keys_in_clusters_ge2','colliding_key_pairs','max_cluster_size')}))
    write_csv(results/'paired_differences.csv',differences)
    manifest=dict(seed=SEED,random_sampler='random.Random(seed).sample(sorted allowed plaintexts,100)',
                  baseline_seed=SEED+1,baseline_rng='NumPy PCG64',baseline_replicates=len(b),
                  plaintext_count=len(plain),keys_per_plaintext=N,total_encryptions=2*len(plain)*N,
                  python=sys.version,numpy=np.__version__,platform=platform.platform(),
                  elapsed_seconds=time.perf_counter()-started,
                  paper_source='E:/10th sem/499A/Cryptanalysis.pdf',
                  paper_sha256=hashlib.sha256(Path('E:/10th sem/499A/Cryptanalysis.pdf').read_bytes()).hexdigest() if Path('E:/10th sem/499A/Cryptanalysis.pdf').exists() else None)
    (results/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    from plotting import make_plots
    make_plots(rows,all_hist,plain,b)
    print(json.dumps(manifest,indent=2),flush=True)

if __name__=='__main__': main()
