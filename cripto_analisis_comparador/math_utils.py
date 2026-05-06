# math_utils.py

def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def es_coprimo(a, n):
    return mcd(a, n) == 1


def inverso_modular(a, n):
    t, nuevo_t = 0, 1
    r, nuevo_r = n, a

    while nuevo_r != 0:
        cociente = r // nuevo_r
        t, nuevo_t = nuevo_t, t - cociente * nuevo_t
        r, nuevo_r = nuevo_r, r - cociente * nuevo_r

    if r > 1:
        return None

    if t < 0:
        t = t + n

    return t