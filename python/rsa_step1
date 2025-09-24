from sympy import randprime, gcd, mod_inverse

p = randprime(10**5, 10**6)
q = randprime(10**5, 10**6)
n = p * q
phi = (p-1)*(q-1)
e = 65537
d = mod_inverse(e, phi)

print("Public key:", (n, e))
print("Private key:", (n, d))

msg = 42
c = pow(msg, e, n)
print("Encrypted:", c)

m = pow(c, d, n,)
print("Decrypted:", m)