# rsa_demo.py
# Minimal RSA (textbook). For learning only — no padding, not secure for real use.

from dataclasses import dataclass
from typing import Tuple
from sympy import randprime, gcd, mod_inverse

# ---------- Math utils ----------
def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0: 
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a: int, m: int) -> int:
    # You can use sympy.mod_inverse OR the egcd above
    return mod_inverse(a, m)  # replace with custom if you want: (egcd(a,m)[1] % m)

def modexp(base: int, exp: int, mod: int) -> int:
    return pow(base, exp, mod)

# ---------- Encoding helpers ----------
def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big")

def int_to_bytes(x: int, length: int | None = None) -> bytes:
    # auto-size if length not provided
    if length is None:
        length = (x.bit_length() + 7) // 8 or 1
    return x.to_bytes(length, byteorder="big")

# ---------- RSA core ----------
@dataclass
class RSAKeyPair:
    n: int
    e: int
    d: int

def generate_keypair(bits: int = 1024, e: int = 65537) -> RSAKeyPair:
    # pick primes so that gcd(e, phi)=1
    half = bits // 2
    # quick-and-clean prime selection
    while True:
        p = randprime(2**(half-1), 2**half)
        q = randprime(2**(half-1), 2**half)
        if p == q:
            continue
        n = p * q
        phi = (p - 1) * (q - 1)
        if gcd(e, phi) == 1:
            d = modinv(e, phi)
            return RSAKeyPair(n=n, e=e, d=d)

def encrypt_int(m: int, pub_n: int, pub_e: int) -> int:
    if m >= pub_n:
        raise ValueError("Message integer must be < modulus n. Use chunking/encoding.")
    return modexp(m, pub_e, pub_n)

def decrypt_int(c: int, priv_n: int, priv_d: int) -> int:
    return modexp(c, priv_d, priv_n)

# user-facing helpers (bytes <-> RSA int)
def encrypt_bytes(msg: bytes, kp: RSAKeyPair) -> int:
    m = bytes_to_int(msg)
    return encrypt_int(m, kp.n, kp.e)

def decrypt_bytes(cipher_int: int, kp: RSAKeyPair) -> bytes:
    m = decrypt_int(cipher_int, kp.n, kp.d)
    # pad to full byte length of modulus to preserve leading zeros if you want
    return int_to_bytes(m)

# ---------- Demo ----------
if __name__ == "__main__":
    # 1) keygen
    kp = generate_keypair(bits=1024)  # use 2048+ for anything non-demo
    print("n bits:", kp.n.bit_length())

    # 2) message
    msg = b"hello RSA"
    print("msg:", msg)

    # 3) encrypt/decrypt
    c = encrypt_bytes(msg, kp)
    out = decrypt_bytes(c, kp)

    print("cipher (int):", c)
    print("recovered   :", out)

    assert out == msg, "Decryption failed"
    print("OK ✅")