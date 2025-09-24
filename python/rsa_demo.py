# rsa_demo.py
# Minimal RSA (textbook). For learning only — no padding, not secure for real use.

from dataclasses import dataclass
from typing import Tuple
from sympy import randprime, gcd, mod_inverse

# ---------- Math utils ----------
def egcd(a: int, b: int) -> Tuple[int, int, int]:
    # Extended Euclidean Algorithm
    if b == 0: 
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a: int, m: int) -> int:
    # Modular inverse of a mod m
    # Uses sympy's mod_inverse (safe/fast) instead of custom egcd
    return mod_inverse(a, m)

def modexp(base: int, exp: int, mod: int) -> int:
    # Fast modular exponentiation
    return pow(base, exp, mod)

# ---------- Encoding helpers ----------
def bytes_to_int(b: bytes) -> int:
    # Convert bytes -> integer for RSA math
    return int.from_bytes(b, byteorder="big")

def int_to_bytes(x: int, length: int | None = None) -> bytes:
    # Convert integer -> bytes
    # auto-size if length not provided
    if length is None:
        length = (x.bit_length() + 7) // 8 or 1
    return x.to_bytes(length, byteorder="big")

# ---------- RSA core ----------
@dataclass
class RSAKeyPair:
    n: int  # modulus
    e: int  # public exponent
    d: int  # private exponent

def generate_keypair(bits: int = 1024, e: int = 65537) -> RSAKeyPair:
    # Generate RSA keypair
    half = bits // 2
    while True:
        # Pick two random primes of ~half the size
        p = randprime(2**(half-1), 2**half)
        q = randprime(2**(half-1), 2**half)
        if p == q:  # ensure distinct primes
            continue
        n = p * q
        phi = (p - 1) * (q - 1)  # Euler's totient
        if gcd(e, phi) == 1:  # ensure e is coprime to phi
            d = modinv(e, phi)  # private exponent
            return RSAKeyPair(n=n, e=e, d=d)

def encrypt_int(m: int, pub_n: int, pub_e: int) -> int:
    # Encrypt integer message with public key
    if m >= pub_n:
        raise ValueError("Message integer must be < modulus n. Use chunking/encoding.")
    return modexp(m, pub_e, pub_n)

def decrypt_int(c: int, priv_n: int, priv_d: int) -> int:
    # Decrypt integer ciphertext with private key
    return modexp(c, priv_d, priv_n)

# user-facing helpers (bytes <-> RSA int)
def encrypt_bytes(msg: bytes, kp: RSAKeyPair) -> int:
    # Encrypt byte string
    m = bytes_to_int(msg)
    return encrypt_int(m, kp.n, kp.e)

def decrypt_bytes(cipher_int: int, kp: RSAKeyPair) -> bytes:
    # Decrypt back to bytes
    m = decrypt_int(cipher_int, kp.n, kp.d)
    return int_to_bytes(m)

# ---------- Demo ----------
if __name__ == "__main__":
    # 1) keygen
    kp = generate_keypair(bits=2048)  # use 2048+ for real applications
    print("n bits:", kp.n.bit_length())

    # 2) message
    msg = b"hello RSA"
    print("msg:", msg)

    # 3) encrypt/decrypt
    c = encrypt_bytes(msg, kp)
    out = decrypt_bytes(c, kp)

    print("cipher (int):", c)
    print("recovered   :", out)

    # sanity check
    assert out == msg, "Decryption failed"
    print("OK ✅")