import math

def generate_factor_base(p, const=1.0):
    B = math.exp(const * math.sqrt(math.log(p) * math.log(math.log(p))))
    B = int(B)
    factor_base = [q for q in range(2, B + 1) if is_prime(q)]
    return factor_base

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def modular_exponentiation(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def decompose_mod_factor_base(value, factor_base, p):
    exponents = []
    for q in factor_base:
        exp = 0
        while value % q == 0:
            exp += 1
            value //= q
        exponents.append(exp)
    if value == 1:
        return exponents
    return None

def collect_relations(a, p, factor_base):
    relations = []
    right_hand_sides = []
    r_values = []
    for r in range(1, p):
        value = modular_exponentiation(a, r, p)
        exponents = decompose_mod_factor_base(value, factor_base, p)
        if exponents is not None:
            relations.append(exponents)
            right_hand_sides.append(r)
            r_values.append(r)
            if len(relations) >= len(factor_base):
                break
    return relations, right_hand_sides, r_values

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

    solution = [0] * m
    for i in range(n - 1, -1, -1):
        solution[i] = results[i]
        for j in range(i + 1, m):
            solution[i] = (solution[i] - matrix[i][j] * solution[j]) % mod

    return solution

def solve_discrete_log(p, a, b):
    """
    Решение уравнения a^x ≡ b (mod p) методом фактор-базы.
    """
    factor_base = generate_factor_base(p)

    relations, right_hand_sides, r_values = collect_relations(a, p, factor_base)

    log_values = gauss_mod(relations, right_hand_sides, p - 1)

    for r in range(1, p):
        value = modular_exponentiation(a, r, p)
        exponents = decompose_mod_factor_base(value, factor_base, p)
        if exponents is not None:
            x = sum(log_values[q] * exponents[q] for q in range(len(factor_base))) % (p - 1)
            return x

    return None

if __name__ == "__main__":
    p = 45951073884270286226032052763881415515719372656837623979876510536196955265855797727317529662963847850835787091128581966738335275550658833691142951202730541
    g = 2625467471760376718918222286204657241898958153650814079310165332185997495820966518407823475477541521513824900261146103918895634849893126850917576190256648
    e = 23789114049968287433465136151371367637584601305958190883272454513529448223661319215654255831456768953819437288396473699890455354287085700231512700500367001
    x = solve_discrete_log(p, g, e)
    print(x)