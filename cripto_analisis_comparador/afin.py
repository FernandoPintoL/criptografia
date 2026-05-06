# afin.py
from .math_utils import es_coprimo


def cifrar_afin(mensaje, a, b, alfabeto):
    """
    Cifra un mensaje usando el cifrado Afín.

    Fórmula:
        C = (a * P + b) mod n

    Donde:
        - P: posición de la letra en el alfabeto
        - C: posición cifrada
        - a, b: claves
        - n: tamaño del alfabeto

    Requisito:
        a debe ser coprimo con n (para que exista inverso modular)
    """

    n = len(alfabeto)

    # 🔴 Validación matemática
    if not es_coprimo(a, n):
        raise ValueError(f"'a' = {a} no es coprimo con n = {n}")

    # 🔥 Diccionario para acceso rápido O(1)
    mapa = {letra: i for i, letra in enumerate(alfabeto)}

    resultado = []

    for letra in mensaje:

        # Solo cifrar si pertenece al alfabeto
        if letra in mapa:
            P = mapa[letra]

            # Fórmula del cifrado afín
            C = (a * P + b) % n

            resultado.append(alfabeto[C])
        else:
            # Mantener caracteres externos (espacios, símbolos)
            resultado.append(letra)

    return "".join(resultado)

    