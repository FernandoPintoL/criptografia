# analisis_afin.py

from math_utils import mcd


def factores_comunes(a, n):
    """
    Devuelve los factores comunes entre a y n (excepto 1)
    """
    comunes = []

    for i in range(2, min(abs(a), abs(n)) + 1):
        if a % i == 0 and n % i == 0:
            comunes.append(i)

    return comunes


def analizar_constante(a, n):
    """
    Analiza si la constante 'a' es válida en el cifrado Afín.

    Condición:
        mcd(a, n) = 1  → existe inverso modular
    """

    if n <= 1:
        raise ValueError("El módulo n debe ser mayor que 1")

    if a == 0:
        return {
            "valido": False,
            "mensaje": "0 no tiene inverso multiplicativo",
            "mcd": n,
            "factores": []
        }

    d = mcd(a, n)

    if d == 1:
        return {
            "valido": True,
            "mensaje": "Existe inverso modular",
            "mcd": d,
            "factores": []
        }
    else:
        return {
            "valido": False,
            "mensaje": "No existe inverso modular",
            "mcd": d,
            "factores": factores_comunes(a, n)
        }