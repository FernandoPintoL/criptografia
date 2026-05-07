# ================================================================================
# ALGORITMO EUCLIDIANO PARA CÁLCULO DE MCD
# ================================================================================

def gcd(a, b):
    """
    Calcula el Máximo Común Divisor (MCD) usando el Algoritmo de Euclides.

    Fórmula: gcd(a, b) = gcd(b, a mod b) hasta que b = 0

    Ejemplo:
        gcd(48, 18) = gcd(18, 12) = gcd(12, 6) = gcd(6, 0) = 6
    """
    a, b = abs(a), abs(b)

    while b != 0:
        a, b = b, a % b

    return a

def factores_comunes(a, b):
    """
    Encuentra todos los factores comunes entre dos números (excepto 1).

    Ejemplo:
        factores_comunes(12, 18) = [2, 3, 6]
    """
    comunes = []
    menor = min(abs(a), abs(b))

    for i in range(2, menor + 1):
        if a % i == 0 and b % i == 0:
            comunes.append(i)

    return comunes

def inverso_modular(a, n):
    """
    Calcula el INVERSO MULTIPLICATIVO de 'a' módulo 'n'.

    Si (a * x) % n == 1, entonces x es el inverso de a módulo n.
    Esto es crucial para DESCIFRAR en criptografía afín.

    Ejemplo:
        inverso_modular(3, 11) = 4
        Porque: (3 * 4) mod 11 = 12 mod 11 = 1

    Uso en Criptografía:
        Si cifras con: c = (a * m + b) mod 26
        Descifras con: m = (a⁻¹ * (c - b)) mod 26
        donde a⁻¹ es el inverso de a
    """
    a = a % n  # Normalizar a al rango [0, n)

    for x in range(1, n):
        if (a * x) % n == 1:  # Buscar x tal que a*x ≡ 1 (mod n)
            return x

    return None  # Si no hay inverso

def validar_constante(a, n):
    """
    Valida si una constante 'a' es válida para usar en Criptografía Afín.

    REGLA: Para que 'a' sea válido, mcd(a, n) DEBE ser 1 (coprimos)

    Si son coprimos:
        - Existe inverso multiplicativo
        - Puede usarse en Criptografía de Cifrado por Resto (CCR)
        - Se muestra el inverso encontrado

    Si NO son coprimos:
        - NO existe inverso
        - NO puede usarse en CCR
        - Se muestran los factores comunes
    """
    d = gcd(a, n)

    if a == 0:
        return (
            f"❌ INVÁLIDO\n"
            f"a = {a}, n = {n}\n"
            f"0 no tiene inverso multiplicativo en ningún módulo\n"
            f"❌ No se puede usar en CCR"
        )

    if d == 1:
        # Son coprimos → EXISTE inverso
        inv = inverso_modular(a, n)

        return (
            f"✔ VÁLIDO\n"
            f"a = {a}, n = {n}\n"
            f"mcd({a},{n}) = 1 → son coprimos\n"
            f"✔ Existe inverso modular\n"
            f"Inverso de {a} módulo {n}: {inv}\n"
            f"Comprobación: ({a} × {inv}) mod {n} = {(a * inv) % n}\n"
            f"✔ Se puede usar en CCR"
        )
    else:
        # NO son coprimos → NO existe inverso
        comunes = factores_comunes(a, n)

        return (
            f"❌ INVÁLIDO\n"
            f"a = {a}, n = {n}\n"
            f"mcd({a},{n}) = {d} → comparten factores\n"
            f"Factores comunes: {comunes}\n"
            f"💡 Al compartir factores, no existe inverso multiplicativo\n"
            f"❌ No se puede usar en CCR"
        )