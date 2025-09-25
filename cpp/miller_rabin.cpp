// Miller–Rabin primality test in C++
// Deterministic for 64-bit integers
// Demonstrates number theory & fast modular arithmetic

#include <bits/stdc++.h>
using namespace std;

// convenience typedefs
using u128 = unsigned __int128;  // 128-bit type for safe modular multiplication
using u64 = uint64_t;            // 64-bit unsigned int

// (a * b) % mod using 128-bit to avoid overflow
static inline u64 mul_mod(u64 a, u64 b, u64 mod) {
    return (u128)a * b % mod;
}

// fast modular exponentiation: base^exp mod mod
static inline u64 pow_mod(u64 a, u64 e, u64 mod) {
    u64 r = 1;
    while (e) {
        if (e & 1) r = mul_mod(r, a, mod);
        a = mul_mod(a, a, mod);
        e >>= 1;
    }
    return r;
}

// Miller–Rabin test for n
bool is_probable_prime(u64 n) {
    if (n < 2) return false;

    // small prime check
    for (u64 p : {2ull,3ull,5ull,7ull,11ull,13ull,17ull,19ull,23ull,29ull,31ull,37ull}) {
        if (n % p == 0) return n == p;
    }

    // write n-1 = d * 2^r with d odd
    u64 d = n - 1, r = 0;
    while ((d & 1) == 0) { d >>= 1; ++r; }

    // deterministic bases for 64-bit integers
    const u64 bases[] = {2ull, 3ull, 5ull, 7ull, 11ull, 13ull, 17ull};

    // one MR check for base a
    auto check = [&](u64 a) {
        if (a % n == 0) return true;
        u64 x = pow_mod(a, d, n);
        if (x == 1 || x == n - 1) return true;
        for (u64 i = 1; i < r; ++i) {
            x = mul_mod(x, x, n);
            if (x == n - 1) return true;
        }
        return false;
    };

    // run the test for each base
    for (u64 a : bases) {
        if (a >= n) continue;
        if (!check(a)) return false;
    }
    return true;
}

int main() {
    // test values: small primes, Carmichael numbers, and large primes
    vector<u64> nums = {
        17ull, 561ull, 1105ull, 6700417ull,  // 561 and 1105 are pseudoprimes
        (1ULL << 61) - 1,                    // 2^61 - 1, a Mersenne prime
        18446744073709551557ull              // big prime near 2^64
    };

    for (auto n : nums) {
        cout << n << " is prime? "
             << (is_probable_prime(n) ? "true" : "false") << "\n";
    }
    return 0;
}
