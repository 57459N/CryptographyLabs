import math


def gelfond_shanks(g, e, p):
    m = math.isqrt(p) + 1

    table = {}
    value = g
    for j in range(m):
        table[value] = j
        value = value * g % p

    c = pow(g, -m, p)
    for i in range(m):
        y = (e * pow(c, i, p)) % p
        if y in table:
            return i * m + table[y]
    return None


if __name__ == '__main__':
    p = 45951073884270286226032052763881415515719372656837623979876510536196955265855797727317529662963847850835787091128581966738335275550658833691142951202730541
    g = 2625467471760376718918222286204657241898958153650814079310165332185997495820966518407823475477541521513824900261146103918895634849893126850917576190256648
    e = 23789114049968287433465136151371367637584601305958190883272454513529448223661319215654255831456768953819437288396473699890455354287085700231512700500367001

    d = gelfond_shanks(g, e, p)
    if d is not None:
        print(f"Частный ключ (d) найден: {d}")
    else:
        print("Не удалось найти частный ключ.")