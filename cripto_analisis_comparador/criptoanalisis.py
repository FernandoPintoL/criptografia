# criptoanalisis.py

from .math_utils import inverso_modular, mcd


def letra_a_numero(letra, alfabeto):
    if letra in alfabeto:
        return alfabeto.index(letra)
    return None


def pedir_letra(mensaje, alfabeto):
    letra = input(mensaje)

    # ❌ Validación de tamaño
    if len(letra) != 1:
        print("❌ Error: solo se permite un carácter por entrada")
        return None

    # ❌ Validación de alfabeto
    if letra not in alfabeto:
        print("❌ Error: carácter fuera del alfabeto seleccionado")
        return None

    return letra


def resolver_afin(M1, C1, M2, C2, n):
    """
    Resuelve:
        C = aM + b (mod n)
    """

    if M1 == M2:
        raise ValueError("M1 y M2 no pueden ser iguales")

    delta_M = (M1 - M2) % n
    delta_C = (C1 - C2) % n

    d = mcd(delta_M, n)

    if d != 1:
        return {
            "exito": False,
            "mensaje": f"No hay solución única porque mcd({delta_M}, {n}) = {d}"
        }

    inv = inverso_modular(delta_M, n)

    if inv is None:
        return {
            "exito": False,
            "mensaje": "No existe inverso modular"
        }

    a = (delta_C * inv) % n
    b = (C1 - a * M1) % n

    return {
        "exito": True,
        "a": a,
        "b": b,
        "ecuacion": f"C = ({a}M + {b}) mod {n}"
    }


def criptoanalisis(alfabeto):

    n = len(alfabeto)

    print("\n--- CRIPTOANÁLISIS POR ECUACIONES ---")
    print(f"Módulo n = {n}")
    print("Usa correspondencias tipo: M → C")

    # 🔥 USO DE VALIDACIÓN PASO A PASO
    M1 = pedir_letra("Ingrese M1: ", alfabeto)
    if M1 is None:
        return

    C1 = pedir_letra("Ingrese C1: ", alfabeto)
    if C1 is None:
        return

    M2 = pedir_letra("Ingrese M2: ", alfabeto)
    if M2 is None:
        return

    C2 = pedir_letra("Ingrese C2: ", alfabeto)
    if C2 is None:
        return

    # 🔢 Convertir
    M1 = letra_a_numero(M1, alfabeto)
    C1 = letra_a_numero(C1, alfabeto)
    M2 = letra_a_numero(M2, alfabeto)
    C2 = letra_a_numero(C2, alfabeto)

    resultado = resolver_afin(M1, C1, M2, C2, n)

    print("\n📌 RESULTADO:")

    if not resultado["exito"]:
        print("❌", resultado["mensaje"])
        return

    print(f"a = {resultado['a']}")
    print(f"b = {resultado['b']}")
    print("Ecuación:", resultado["ecuacion"])

    print("\n🧠 INTERPRETACIÓN:")
    print("Se resuelve un sistema de ecuaciones modulares.")
    print("Permite romper el cifrado Afín con dos pares M → C.")