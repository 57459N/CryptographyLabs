from typing import Callable

table_114 = {
    1: [10, 9, 13, 6, 14, 11, 4, 5, 15, 1, 3, 12, 7, 0, 8, 2],
    2: [8, 0, 12, 4, 9, 6, 7, 11, 2, 3, 1, 15, 5, 14, 10, 13],
    3: [15, 6, 5, 8, 14, 11, 10, 4, 12, 0, 3, 7, 2, 9, 1, 13],
    4: [3, 8, 13, 9, 6, 11, 15, 0, 2, 5, 12, 10, 4, 14, 1, 7],
    5: [15, 8, 14, 9, 7, 2, 0, 13, 12, 6, 1, 5, 11, 4, 3, 10],
    6: [2, 8, 9, 7, 5, 15, 0, 11, 12, 1, 13, 14, 10, 3, 6, 4],
    7: [3, 8, 11, 5, 6, 4, 14, 10, 2, 12, 1, 7, 9, 15, 13, 0],
    8: [1, 2, 3, 14, 6, 13, 11, 8, 15, 10, 12, 5, 7, 9, 0, 4],
}


def xor(a: int, b: int, _len: int) -> int:
    return (a ^ b) & ((1 << _len) - 1)


def square_plus(a: int, b: int, _len: int) -> int:
    return (a + b) & ((1 << _len) - 1)


def sp_round(x: int, key: int,
             round_bits: list[int],
             plus: Callable[[int, int, int], int] = None,
             s1: list[int] = None, s2: list[int] = None,
             p_: Callable = None, p_args: tuple = ()
             ) -> int:
    round_key = 0
    for i in round_bits:
        round_key <<= 1
        round_key |= bool(key & (1 << i - 1))

    t = plus(x, round_key, 8)
    t1 = t >> 4 & 0xf
    t2 = t & 0xf

    n1 = s1[t1]
    n2 = s2[t2]

    n = (n1 << 4) | n2
    return p_(n, *p_args)


def sp_crypt(X: int, key: int, iters: int = 3, verbose: bool = True) -> int:
    round_bits_list = [
        [1, 2, 3, 4, 5, 6, 7, 8],
        [1, 2, 3, 4, 9, 10, 11, 12],
        [5, 6, 7, 8, 12, 11, 10, 9],
    ]
    s1_idx = 1
    s2_idx = 7

    value = X
    if verbose:
        print(f'k: {key :012b}')
        print(f'start X: {value :08b}')

    for i in range(iters):
        value = sp_round(
            value,
            key,
            round_bits_list[i],
            plus=square_plus,
            s1=table_114[s1_idx], s2=table_114[s2_idx],
            p_=lambda x: ((x << 6) | (x >> (8 - 6))) & 0xff
        )
        if verbose:
            print(f'after {i + 1}: {value :08b}')
    return value


def main():
    N = 2  # position in group list
    surname = 'Индюков'
    name = 'Станислав'

    r = len(surname)
    q = len(name)

    X = 9 * N
    key = abs(4096 - 13 * q * r)

    print(f'start: {X :08b}')
    print(f'crypt: {sp_crypt(X, key, verbose=False) :08b}')


if __name__ == "__main__":
    main()
