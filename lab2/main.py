from typing import Callable


def xor(a: int, b: int, _len: int) -> int:
    return (a ^ b) & ((1 << _len) - 1)


def square_plus(a: int, b: int, _len: int) -> int:
    return (a + b) & ((1 << _len) - 1)


def sp_round(x: int, key: int,
             round_bits: list[int],
             plus: Callable[[int, int, int], int] = None,
             s1: dict[int, int] = None, s2: dict[int, int] = None,
             p_: Callable = None, p_args: tuple = ()
             ) -> int:
    round_key = 0
    for i in round_bits:
        round_key <<= 1
        round_key |= bool(key & (1 << i - 1))

    t = plus(x, round_key, 8)
    t1 = t >> 4 & 0xf
    t2 = t & 0xf

    # todo: test from this moment
    n1 = s1[t1]
    n2 = s2[t2]

    n = (n1 << 4) | n2

    return p_(n, *p_args)


def main():
    N = 2  # position in group list
    surname = 'Индюков'
    name = 'Станислав'

    r = len(surname)
    q = len(name)

    X = 9 * N
    a = 'f'
    # print(list(map(lambda x: int(x, 16),'F	6	5	8	E	B	A	4	C	0	3	7	2	9	1	D'.split('\t'))))
    k = 0b11001010
    sp_round(123, k, [i for i in range(1, 9)], plus=square_plus)


if __name__ == "__main__":
    main()
