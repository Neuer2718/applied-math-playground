import random

def is_probable_prime(n: int, k: int = 10) -> bool:
    """Miller-Rabin primality test.
    n: number to test
    k: number of rounds (more rounds -> lower error prob)
    """
    if n in (2, 3):
        return True
    if n <= 1 or n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

if __name__ == "__main__":
    nums = [17, 561, 1105, 6700417, 2**61-1]
    for n in nums:
        print(f"{n} is prime? {is_probable_prime(n)}")