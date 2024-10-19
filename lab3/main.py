import time
import random


def fast_pow(x: int, y: int, mod: int = None) -> int:
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


def is_prime(n, rounds=10):
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
        x = fast_pow(a, t, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = fast_pow(x, 2, n)
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


def get_private_key(p: int, q: int, e: int) -> int | None:
    phi = (p - 1) * (q - 1)
    gcd, _, _ = extended_gcd(e, phi)
    while gcd != 1:
        return None
    return mod_inverse(e, phi)


def encrypt(x: int, e: int, n: int) -> int:
    return fast_pow(x, e, n)


def decrypt(y: int, d: int, n: int) -> int:
    return fast_pow(y, d, n)


def _help():
    print(r'''
    gen {p} {q} {e}           - gets private key   - p (prime), q (prime), e (public key)           
    encr {x} {e} {n | p q}    - encrypts message   - x (int), e (public key), n (module) | p q (primes)            
    decr {x} {d} {n | p q}    - encrypts message   - x (int), d (private key), n (module) | p q (primes)            

    help - list of commands
    exit - exit
    ''')


def main():
    while True:
        s = input("> ")
        args = s.split(" ")
        command = args[0]

        if command == "help":
            _help()
            continue

        match command:
            case "gen":
                try:
                    p1, p2, p3 = int(args[1]), int(args[2]), int(args[3])
                except ValueError:
                    print("Arguments must be integers.")
                if pk := get_private_key(p1, p2, p3):
                    print(pk)
                else:
                    print('Such public key does not fit.')

            case "encr":
                try:
                    if len(args) == 4:
                        p1, p2, p3 = int(args[1]), int(args[2]), int(args[3])
                    elif len(args) == 5:
                        p1, p2, p3 = int(args[1]), int(args[2]), int(args[3]) * int(args[4])
                except ValueError:
                    print("Arguments must be integers.")
                print(encrypt(p1, p2, p3))

            case "decr":
                try:
                    if len(args) == 4:
                        p1, p2, p3 = int(args[1]), int(args[2]), int(args[3])
                    elif len(args) == 5:
                        p1, p2, p3 = int(args[1]), int(args[2]), int(args[3]) * int(args[4])
                except ValueError:
                    print("Arguments must be integers.")
                print(decrypt(p1, p2, p3))

            case "exit":
                print("Bye, bye!")
                break

            case _:
                print("Unknown command.")
                _help()


if __name__ == "__main__":
    main()
