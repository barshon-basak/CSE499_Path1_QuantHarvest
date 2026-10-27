"""Shared field operations; no Sage dependency. Integer bits are MSB first."""
def check16(value):
    if type(value) is not int or not 0 <= value < 65536:
        raise ValueError('expected a Python integer in 0..65535')

def unpack(x):
    return [(x >> s) & 15 for s in (12, 8, 4, 0)]

def pack(a):
    return (int(a[0]) << 12) | (int(a[1]) << 8) | (int(a[2]) << 4) | int(a[3])

def mul(a, b):
    """GF(16), modulus x^4+x+1 = 0x13."""
    out = 0
    for _ in range(4):
        if b & 1:
            out ^= a
        a <<= 1
        if a & 16:
            a ^= 0x13
        b >>= 1
    return out

def sub(x, box):
    return pack([box[n] for n in unpack(x)])

def shift(x):
    a,b,c,d = unpack(x)
    return pack([a,d,c,b])

def mix(x, diagonal, off):
    a,b,c,d = unpack(x)
    return pack([mul(diagonal,a)^mul(off,b), mul(off,a)^mul(diagonal,b),
                 mul(diagonal,c)^mul(off,d), mul(off,c)^mul(diagonal,d)])

def encrypt_with_keys(p, keys, box, diagonal, off):
    x = p ^ keys[0]
    x = mix(shift(sub(x,box)),diagonal,off) ^ keys[1]
    return shift(sub(x,box)) ^ keys[2]

def decrypt_with_keys(c, keys, box, inv_diagonal, inv_off):
    inv = [box.index(i) for i in range(16)]
    x = sub(shift(c ^ keys[2]),inv) ^ keys[1]
    x = sub(shift(mix(x,inv_diagonal,inv_off)),inv)
    return x ^ keys[0]
