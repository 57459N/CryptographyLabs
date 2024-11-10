import random


def pow(x: int, y: int, mod: int = None) -> int:
    # https://en.wikipedia.org/wiki/Exponentiation_by_squaring
    if mod is not None:
        result = 1
        base = x % mod

        while y > 0:
            if y % 2 == 1:
                result = (result * base) % mod
            y //= 2
            base = (base * base) % mod

        return result

    bits = []
    while y:
        bits.append(y & 1)
        y >>= 1

    res = 1
    bits = list(reversed(bits))
    for bit in bits[:-1]:
        res *= x ** bit
        res *= res
    res *= x ** bits[-1]
    return res


def gcd(a: int, b: int):
    return extended_gcd(a, b)[0]


def extended_gcd(a: int, b: int):
    # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    if a == 0:
        return b, 0, 1
    gcd, s1, t1 = extended_gcd(b % a, a)
    s = t1 - (b // a) * s1
    t = s1
    return gcd, s, t


def mod_inverse(a: int, m: int):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m


def right_rotate(number: int, shift: int = 1, bit_length: int = 32):
    mask = (1 << bit_length) - 1
    number &= mask

    shift %= bit_length
    rotated = (number >> shift) | ((number << (bit_length - shift)) & mask)

    return rotated


def get_random_relatively_prime(n: int):
    while True:
        x = random.randint(2, n - 1)
        if gcd(x, n) == 1:
            return x


def is_prime(n, rounds=5):
    # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test

    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False

    s, t = 0, n - 1
    while t % 2 == 0:
        s += 1
        t //= 2

    for _ in range(rounds):
        a = random.randint(2, n - 2)
        x = pow(a, t, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def generate_big_prime(n_bits: int):
    while True:
        p = random.randint(2 ** (n_bits - 1), 2 ** n_bits - 1)
        if p % 2 == 1 and is_prime(p):
            return p
