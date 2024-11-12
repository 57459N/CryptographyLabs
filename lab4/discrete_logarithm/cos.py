from ..algorithms import gcd


def integrate_solutions(base_solutions, mod, constraints):
    return [(base + constraint) % mod for base, constraint in zip(base_solutions, constraints)]


def gauss_mod(matrix, results, mod):
    n = len(matrix)
    m = len(matrix[0])
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    results[i], results[j] = results[j], results[i]
                    break
        inv = pow(matrix[i][i], -1, mod)
        for k in range(i, m):
            matrix[i][k] = (matrix[i][k] * inv) % mod
        results[i] = (results[i] * inv) % mod
        for j in range(i + 1, n):
            factor = matrix[j][i]
            for k in range(i, m):
                matrix[j][k] = (matrix[j][k] - factor * matrix[i][k]) % mod
            results[j] = (results[j] - factor * results[i]) % mod

    # Обратный проход
    solution = [0] * m
    for i in range(n - 1, -1, -1):
        solution[i] = results[i]
        for j in range(i + 1, m):
            solution[i] = (solution[i] - matrix[i][j] * solution[j]) % mod

    return solution


def modular_exponentiation(base, exp, mod):
    """Быстрое возведение в степень по модулю."""
    result = 1
    while exp > 0:
        if exp % 2 == 1:  # Если степень нечетная
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result


def solve_discrete_log(p, a, b):
    """
    Решение уравнения a^x ≡ b (mod p) методом фактор-базы.
    :param p: Простое число.
    :param a: Основание.
    :param b: Значение.
    :return: x (если найден) или None.
    """
    factor_base = [i for i in range(2, p) if gcd(i, p - 1) == 1]

    relations = []
    exponents = []
    for base in factor_base:
        relation = []
        value = b
        for factor in factor_base:
            exp = 0
            while value % factor == 0:
                exp += 1
                value //= factor
            relation.append(exp)
        if value == 1:
            relations.append(relation)
            exponents.append(base)

    if len(relations) < len(factor_base):
        raise ValueError("Недостаточно данных для решения.")

    base_solutions = gauss_mod(relations, exponents, p)
    if base_solutions is None:
        raise ValueError("Система уравнений не имеет решений.")

    constraints = [0] * len(base_solutions)  # Например, без дополнительных ограничений
    restored_solutions = integrate_solutions(base_solutions, p, constraints)

    return restored_solutions


p = 45951073884270286226032052763881415515719372656837623979876510536196955265855797727317529662963847850835787091128581966738335275550658833691142951202730541
g = 2625467471760376718918222286204657241898958153650814079310165332185997495820966518407823475477541521513824900261146103918895634849893126850917576190256648
e = 23789114049968287433465136151371367637584601305958190883272454513529448223661319215654255831456768953819437288396473699890455354287085700231512700500367001

x = solve_discrete_log(p, g, e)
if x is not None:
    print(f"Решение: x = {x}")
else:
    print("Решение не найдено или алгоритм не завершен.")
