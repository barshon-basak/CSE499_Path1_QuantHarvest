# Cipher specification and evidence audit

## Sources inspected

1. Kiran, Safdar, Khalid, Butt and Jalil (2026), *Quantum cryptanalysis of SPN ciphers with known plaintext*, npj Quantum Information 12:85, DOI https://doi.org/10.1038/s41534-026-01218-x. User-provided `E:/10th sem/499A/Cryptanalysis.pdf`, 15 pages. Read text and visually inspected pages 3, 4, 7 and 9. SHA-256 recorded in `results/manifest.json`. Source PDF is unchanged. Its classical definitions and Tables 9–11 are the target; quantum implementation and Grover are outside this experiment.
2. Phan (2002), *Mini Advanced Encryption Standard (Mini-AES): A Testbed for Cryptanalysis Students*, Cryptologia 26(4), 283–306. Author-hosted copy: https://www.geocities.ws/dearphael/MiniAES.pdf. Sections 3.1–3.7, Table 2 and Example 9 establish ordering, key schedule, and a worked encryption.
3. Musa, Schaefer and Wedig (2003), *A Simplified AES Algorithm and Its Linear and Differential Cryptanalyses*, Cryptologia 27(2), 148–177. https://doi.org/10.1080/0161-110391891838. Bibliographic page verified; full publisher text was not available. The 2010 online date in the 2026 bibliography is not the original volume publication year.
4. Simmons, *Algebraic Cryptanalysis of Simplified AES*, author research paper, description section: https://cscdb.nku.edu/~christensen/Alg%20cryptanalysis%20SAES.pdf. Gives S-box, finite field, byte schedule and explicit round composition.
5. Holden, *A Simplified AES Algorithm*, university teaching specification: https://www.rose-hulman.edu/class/ma/holden/Archived_Courses/Math479-0304/lectures/s-aes.pdf. Confirms mix matrix, round constants and designer-attributed worked vector. Matching published assignment: https://www.rose-hulman.edu/class/ma/holden/Archived_Courses/Math479-0304/homework/homework4-cs.html.
6. Sage issue https://github.com/sagemath/sage/issues/40069. Reports implicit finite-field/S-box indexing conversion in the key schedule. The report also involves row/column serialization, so do not equate displayed Sage binary strings with the external integer convention without conversion. This project uses explicit integer tables and polynomial arithmetic; it neither imports Sage nor claims to validate its current implementation or fix status.

## Exact conventions

For BOTH ciphers, hexadecimal `ABCD` means nibbles `(A,B,C,D)` from most to least significant. The state matrix is `[[A,C],[B,D]]` (column major), not `[[A,B],[C,D]]`. The same serialization applies to keys and ciphertexts. A nibble's bit weights are 8,4,2,1; in GF(16), these represent x^3,x^2,x,1. Reduction polynomial is x^4+x+1 (`0x13`). Addition is XOR.

ShiftRow: `(A,B,C,D) -> (A,D,C,B)`; it swaps the second and fourth serialized nibbles. MixColumns multiplies each adjacent pair `(A,B)` and `(C,D)` by the respective matrix, with field multiplication, not integer multiplication.

Both encrypt as initial XOR K0; SubNib; ShiftRow; MixColumns; XOR K1; SubNib; ShiftRow; XOR K2. The final round has NO MixColumns. There are two rounds plus initial key addition, not three full rounds.

| Property | Mini-AES | S-AES |
|---|---|---|
| S-box outputs for inputs 0..F | E 4 D 1 2 F B 8 3 A 6 C 5 9 0 7 | 9 4 A B D 1 8 5 6 2 0 3 C E F 7 |
| Mix matrix | [[3,2],[2,3]] | [[1,4],[4,1]] |
| Inverse mix matrix | same | [[9,2],[2,9]] |
| Key expansion unit | nibble | byte |
| Round constants | 1,2 (nibbles) | 80,30 (bytes) |

Mini-AES: w0..w3 are original key nibbles. For each round with constant rc, `new0=old0 XOR S(old3) XOR rc`; `new1=old1 XOR new0`; `new2=old2 XOR new1`; `new3=old3 XOR new2`. Concatenate in that order; K0 is the original key. This matches Phan Table 2 and the 2026 key-schedule discussion, pages 8–9.

S-AES: W0 and W1 are high and low bytes. For each round constant RC, `g(W)=SubNib(RotNib(W)) XOR RC`; `new0=old0 XOR g(old1)`; `new1=old1 XOR new0`. Concatenate the bytes to form each round key. RC high nibbles are x^3=8 and x^4 mod (x^4+x+1)=3. These constants and byte-based recurrence must not be replaced with Mini-AES's nibble recurrence.

## Validation and discrepancies

Independent published vectors: Mini-AES `P=9C63 K=C3F0 C=72C6`, with K1=30FF, K2=6696 (Phan Example 9); S-AES `P=6F6B K=A73B C=0738` (Holden, attributed to cipher designers). Tests check intermediate Phan states, full-key scalar/vector agreement, field arithmetic, invertibility and saved mapping conservation.

The 2026 paper's Table 1 on page 3 prints S-AES input `1011` -> `0100`. Authoritative S-AES uses `1011` -> `0011`. The printed table has a duplicated output and is not a permutation; it cannot define the intended block cipher. Use the authoritative S-AES box above. Mini-AES Table 3 agrees with Phan.

All nine Table 9–11 plaintext/ciphertext rows and every reported key are valid under this implementation. Eight rows list the complete exhaustive group. Table 11's `FF48 -> 7492` omits `7E7C`: actual group is `{7E7C,F5E2}`. Table 9's prose says the first and second pairs cluster; its table and enumeration instead show the first and third cluster. Table 11's prose includes `BAD0 -> E7AA` rather than its table's `0B5D -> 55E7`. The extra prose vector is separately verified in `results/prose_checks.csv`; it is not substituted into the requested 109-plaintext design. The prose correctly says FF48 clusters despite its table listing only F5E2.

The extra Table 11 prose claim `BAD0 -> E7AA` under `F5E2` does **not** reproduce: `encrypt(BAD0,F5E2)=2568`. Exhaustive enumeration finds `57A2` as the sole key for `BAD0 -> E7AA`. In contrast, the actual table's `0B5D -> 55E7` reproduces with both `F5E2` and `EABF`. This is recorded as a prose error, not silently repaired.

`results/paper_reproduction.csv` records exact expected and computed groups; sorting differences are not mismatches. No values were adjusted to fit examples.
