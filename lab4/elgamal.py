import random
from algorithms import is_prime, get_random_relatively_prime
from sha256 import sha256


def _generate_prime(q):
    while True:
        R = random.randint(2, 4 * (q + 1) // 2) * 2
        p = q * R + 1
        if pow(2, q * R, p) != 1 or pow(2, R, p) == 1:
            continue

        if is_prime(p):
            return p, R


def _find_generator(p, R):
    while True:
        x = get_random_relatively_prime(p)
        g = pow(x, R, p)

        if g != 1:
            return g


def generate_keys(q):
    p, R = _generate_prime(q)
    g = _find_generator(p, R)

    d = get_random_relatively_prime(q)

    e = pow(g, d, p)

    return p, q, g, e, d


def sign(p, q, g, d, message):
    m = sha256(message)
    k = random.randint(1, q - 1)

    r = pow(g, k, p)
    try:
        k_inv = pow(k, -1, q)
    except ValueError:
        k_inv = pow(k, -1, q)

    s = (k_inv * (m - d * r)) % q

    return r, s


def verify(p, q, g, e, message, signature):
    r, s = signature
    if not (1 <= r < p) or not (0 <= s < q):
        return False

    m = sha256(message)
    left_side = pow(e, r, p) * pow(r, s, p) % p
    right_side = pow(g, m, p)

    return left_side == right_side
