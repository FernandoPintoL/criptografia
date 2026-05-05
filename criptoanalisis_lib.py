import gcd_lib

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
        t += n

    return t

def resolver_afine(C1, M1, C2, M2, n=26):
    if M1 == M2:
        return "❌ M1 y M2 no pueden ser iguales"

    delta_C = (C1 - C2) % n
    delta_M = (M1 - M2) % n

    d = gcd_lib.gcd(delta_M, n)

    if d != 1:
        return (
            f"⚠️ mcd({delta_M},{n}) = {d}\n"
            "No hay solución única"
        )

    inv = inverso_modular(delta_M, n)

    if inv is None:
        return "❌ No existe inverso modular"

    a = (delta_C * inv) % n
    b = (C1 - a * M1) % n

    return (
        f"✔ a = {a}, b = {b}\n"
        f"C = ({a}M + {b}) mod {n}"
    )