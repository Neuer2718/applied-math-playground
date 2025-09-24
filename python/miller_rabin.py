import random

def is_probable_prime(n: int, k: int = 10) -> bool:
    """Miller-Rabin primality test.
    n: number to test
    k: number of rounds (more rounds -> lower error prob)
    """
    # Handle small numbers and simple cases
    if n in (2, 3):  # 2 and 3 are prime
        return True
    if n <= 1 or n % 2 == 0:  # negatives, 0, 1, and evens > 2 are not prime
        return False
    
    # Write n - 1 as 2^r * d with d odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform k rounds of testing
    for _ in range(k):
        # Choose a random base a in [2, n-2]
        a = random.randrange(2, n - 1)
        # Compute a^d % n
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue  # This round passes
        
        # Square repeatedly to see if we can get n - 1
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            # If we never hit n - 1, n is composite
            return False
    return True  # Probably prime if all rounds passed

if __name__ == "__main__":
    # Test the function with some known primes and composites
    nums = [17, 561, 1105, 6700417, 2**61-1]
    for n in nums:
        print(f"{n} is prime? {is_probable_prime(n)}")