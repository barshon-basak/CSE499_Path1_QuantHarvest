"""Musa-Schaefer-Wedig two-round S-AES, MSB-first column-major state."""
from common import check16, pack, encrypt_with_keys, decrypt_with_keys
SBOX = (9,4,10,11,13,1,8,5,6,2,0,3,12,14,15,7)
DIAGONAL, OFF = 1, 4

def expand_key(key):
    check16(key)
    w = [key >> 8, key & 255]
    for rc in (0x80,0x30):
        prev = w[-1]
        g = (SBOX[prev & 15] << 4) | SBOX[prev >> 4]
        a = w[-2] ^ g ^ rc
        w.extend([a,prev ^ a])
    return tuple((w[i]<<8)|w[i+1] for i in (0,2,4))

def encrypt(plaintext, key):
    check16(plaintext)
    return encrypt_with_keys(plaintext,expand_key(key),SBOX,DIAGONAL,OFF)

def decrypt(ciphertext, key):
    check16(ciphertext)
    return decrypt_with_keys(ciphertext,expand_key(key),SBOX,9,2)
