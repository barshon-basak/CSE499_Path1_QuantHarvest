"""Run python tests.py. Assertions cover specification and full-key vector engine."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'.deps'))
import unittest, random
import numpy as np
import mini_aes, saes
from common import mul,mix,shift,sub
from clustering import Engine,metrics,PAPER_ROWS,sample_plaintexts,keys_for,N

class CipherTests(unittest.TestCase):
    def test_published_vectors(self):
        self.assertEqual(mini_aes.expand_key(0xC3F0),(0xC3F0,0x30FF,0x6696))
        self.assertEqual(mini_aes.encrypt(0x9C63,0xC3F0),0x72C6)
        self.assertEqual(saes.encrypt(0x6F6B,0xA73B),0x0738)
        self.assertEqual(saes.expand_key(0x4AF5),(0x4AF5,0xDD28,0x87AF))

    def test_phan_intermediate_states(self):
        self.assertEqual(sub(0x5F93,mini_aes.SBOX),0xF7A1)
        self.assertEqual(shift(0xF7A1),0xF1A7)
        self.assertEqual(mix(0xF1A7,3,2),0x0E3E)
        self.assertEqual(sub(0x3EC1,mini_aes.SBOX),0x1054)

    def test_field_independent_polynomial_reduction(self):
        for a in range(16):
            for b in range(16):
                product=0
                for j in range(4):
                    if b>>j&1: product^=a<<j
                for j in range(6,3,-1):
                    if product>>j&1: product^=0x13<<(j-4)
                self.assertEqual(mul(a,b),product)

    def test_linear_layers_all_states(self):
        for x in range(N):
            self.assertEqual(shift(shift(x)),x)
            self.assertEqual(mix(mix(x,3,2),3,2),x)
            self.assertEqual(mix(mix(x,1,4),9,2),x)

    def test_roundtrip_random(self):
        rng=random.Random(721)
        for cipher in (mini_aes,saes):
            for _ in range(1000):
                p,k=rng.randrange(N),rng.randrange(N)
                self.assertEqual(cipher.decrypt(cipher.encrypt(p,k),k),p)

    def test_vector_engine_all_keys_against_scalar(self):
        # Independent nibble key expansion and vector encryption vs scalar byte/nibble code.
        for cipher in (mini_aes,saes):
            engine=Engine(cipher);c=engine.encrypt(0xE0F7)
            for k in range(N):
                self.assertEqual(tuple(int(r[k]) for r in engine.round_keys),cipher.expand_key(k))
                self.assertEqual(int(c[k]),cipher.encrypt(0xE0F7,k))
            rng=random.Random(89)
            for _ in range(128):
                p,k=rng.randrange(N),rng.randrange(N)
                self.assertEqual(int(engine.encrypt(p)[k]),cipher.encrypt(p,k))

    def test_permutation_for_fixed_keys(self):
        pp=np.arange(N,dtype=np.uint16)
        for cipher in (mini_aes,saes):
            e=Engine(cipher)
            for key in (0,0xFFFF,0xC0E4,0x4C8C,0xF5E2):
                out=e.encrypt(pp,round_keys=cipher.expand_key(key))
                self.assertEqual(np.unique(out).size,N)

    def test_sampling(self):
        pp=sample_plaintexts()
        self.assertEqual(len(pp),109);self.assertEqual(len(set(pp)),109)
        self.assertEqual(pp,sample_plaintexts())

    def test_metrics_edge_cases_and_overflow(self):
        m,h=metrics(np.ones(N,dtype=np.int64))
        self.assertEqual(m['colliding_key_pairs'],0)
        self.assertEqual(m['keys_in_clusters_ge2'],0)
        counts=np.zeros(N,dtype=np.int64);counts[0]=N
        m,h=metrics(counts)
        self.assertEqual(m['colliding_key_pairs'],N*(N-1)//2)
        self.assertEqual(m['mean_cluster_known_key'],N)
        self.assertEqual(h[0],N-1)
        with self.assertRaises(ValueError): metrics(np.zeros(N))

    def test_input_validation(self):
        for cipher in (mini_aes,saes):
            for bad in (-1,65536,1.2,'1234',True):
                with self.assertRaises(ValueError): cipher.encrypt(bad,0)
                with self.assertRaises(ValueError): cipher.encrypt(0,bad)

    def test_supplied_collision(self):
        for k in (0xC0E4,0xE534,0xA233):
            self.assertEqual(mini_aes.encrypt(0xE0F7,k),0x8816)

    def test_paper_claims_recorded_not_assumed(self):
        # Do not turn potentially incorrect paper entries into assumed expected outputs.
        self.assertEqual(len(PAPER_ROWS),9)
        self.assertEqual(mini_aes.encrypt(0xBAD0,0xF5E2),0x2568)
        self.assertNotEqual(mini_aes.encrypt(0xBAD0,0xF5E2),0xE7AA)
        e=Engine(mini_aes)
        for _,p,c,keys in PAPER_ROWS:
            actual=np.flatnonzero(e.encrypt(p)==c)
            for k in keys:
                self.assertIn(k,actual)
                self.assertEqual(k in actual,mini_aes.encrypt(p,k)==c)
            if (p,c)==(0xFF48,0x7492):
                self.assertEqual(set(actual),{0x7E7C,0xF5E2})
            else:
                self.assertEqual(set(actual),set(keys))

    def test_saved_artifacts_if_present(self):
        root=Path(__file__).parent/'results'/'groups'
        files=list(root.glob('*.npz'))
        if not files: self.skipTest('run clustering.py to generate mapping files')
        self.assertEqual(len(files),218)
        for path in files:
            ciphername,hexp=path.stem.rsplit('_',1)
            cipher=mini_aes if ciphername=='mini_aes' else saes
            with np.load(path,allow_pickle=False) as z:
                offsets,keys=z['offsets'],z['keys']
                counts=np.diff(offsets).astype(np.int64)
                self.assertEqual(offsets.shape,(N+1,));self.assertEqual(int(offsets[-1]),N)
                self.assertTrue(np.array_equal(np.sort(keys),np.arange(N)))
                expected=Engine(cipher).encrypt(int(hexp,16))
                self.assertTrue(np.array_equal(expected[keys],np.repeat(np.arange(N),counts)))
                m,h=metrics(counts)
                self.assertEqual(int(h.sum()),N)
                self.assertEqual(int(np.dot(np.arange(len(h)),h)),N)

if __name__=='__main__': unittest.main(verbosity=2)
