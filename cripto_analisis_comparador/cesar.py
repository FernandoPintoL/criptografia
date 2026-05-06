# cesar.py

def cifrar_cesar(mensaje, desplazamiento, alfabeto):
    """
    Cifra un mensaje usando el cifrado César.

    Fórmula:
        C = (P + k) mod n

    Donde:
        - P: posición de la letra
        - k: desplazamiento
        - n: tamaño del alfabeto
    """

    if not alfabeto:
        raise ValueError("El alfabeto no puede estar vacío")

    if len(set(alfabeto)) != len(alfabeto):
        raise ValueError("El alfabeto contiene caracteres duplicados")

    n = len(alfabeto)

    # 🔥 acceso rápido
    mapa = {letra: i for i, letra in enumerate(alfabeto)}

    resultado = []

    for letra in mensaje:
        if letra in mapa:
            P = mapa[letra]
            C = (P + desplazamiento) % n
            resultado.append(alfabeto[C])
        else:
            resultado.append(letra)

    return "".join(resultado)