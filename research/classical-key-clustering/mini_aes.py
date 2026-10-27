"""Phan (2002) two-round Mini-AES, verified against Kiran et al. (2026).

Hex ABCD is column-major state [[A,C],[B,D]]. See SPECIFICATION.md.
"""
from common import check16, unpack, pack, encrypt_with_keys, decrypt_with_keys
SBOX = (14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7)
DIAGONAL, OFF = 3, 2

def expand_key(key):
    check16(key)
    w = unpack(key)
    for rc in (1,2):
        a = w[-4] ^ SBOX[w[-1]] ^ rc
        b = w[-3] ^ a
        c = w[-2] ^ b
        d = w[-1] ^ c
        w.extend([a,b,c,d])
    return tuple(pack(w[i:i+4]) for i in (0,4,8))

def encrypt(plaintext, key):
    check16(plaintext)
    return encrypt_with_keys(plaintext,expand_key(key),SBOX,DIAGONAL,OFF)

def decrypt(ciphertext, key):
    check16(ciphertext)
    return decrypt_with_keys(ciphertext,expand_key(key),SBOX,3,2)
