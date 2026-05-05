def gcd(a, b):
    a, b = abs(a), abs(b)
    
    while b != 0:
        a, b = b, a % b
    
    return a

def factores_comunes(a, b):
    comunes = []
    menor = min(abs(a), abs(b))
    
    for i in range(2, menor + 1):
        if a % i == 0 and b % i == 0:
            comunes.append(i)
    
    return comunes

def validar_constante(a, n):
    d = gcd(a, n)

    if a == 0:
        return (
            f"❌ INVÁLIDO\n"
            f"a = {a}, n = {n}\n"
            f"0 no tiene inverso multiplicativo en ningún módulo\n"
            f"❌ No se puede usar en CCR"
        )

    if d == 1:
        return (
            f"✔ VÁLIDO\n"
            f"a = {a}, n = {n}\n"
            f"mcd({a},{n}) = 1 → son coprimos\n"
            f"✔ Existe inverso modular\n"
            f"✔ Se puede usar en CCR"
        )
    else:
        comunes = factores_comunes(a, n)

        return (
            f"❌ INVÁLIDO\n"
            f"a = {a}, n = {n}\n"
            f"mcd({a},{n}) = {d} → comparten factores\n"
            f"Factores comunes: {comunes}\n"
            f"💡 Al compartir factores, no existe inverso multiplicativo\n"
            f"❌ No se puede usar en CCR"
        )