# comparador.py

from .math_utils import es_coprimo
from .afin import cifrar_afin
from .cesar import cifrar_cesar


def frecuencia(texto, alfabeto):
    """
    Calcula la frecuencia relativa de cada símbolo.
    """
    total = len(texto)

    if total == 0:
        return {l: 0 for l in alfabeto}

    conteo = {l: 0 for l in alfabeto}

    for letra in texto:
        if letra in conteo:
            conteo[letra] += 1

    return {
        l: round((conteo[l] / total) * 100, 2)
        for l in conteo
    }


def indice_coincidencia(texto):
    """
    Calcula el índice de coincidencia.
    """
    N = len(texto)

    if N <= 1:
        return 0

    conteo = {}

    for c in texto:
        conteo[c] = conteo.get(c, 0) + 1

    suma = sum(f * (f - 1) for f in conteo.values())

    return round(suma / (N * (N - 1)), 4)


def comparar_cifrados(mensaje, desplazamiento, a, b, alfabeto):
    """
    Compara cifrado César vs Afín con análisis criptográfico.
    """

    n = len(alfabeto)

    if not es_coprimo(a, n):
        raise ValueError(f"'a' no es coprimo con {n}")

    # 🔐 Cifrado
    cesar = cifrar_cesar(mensaje, desplazamiento, alfabeto)
    afin = cifrar_afin(mensaje, a, b, alfabeto)

    # 📊 Frecuencia
    freq_original = frecuencia(mensaje, alfabeto)
    freq_cesar = frecuencia(cesar, alfabeto)
    freq_afin = frecuencia(afin, alfabeto)

    # 📏 Índice de coincidencia
    ic_original = indice_coincidencia(mensaje)
    ic_cesar = indice_coincidencia(cesar)
    ic_afin = indice_coincidencia(afin)

    return {
        "original": mensaje,
        "cesar": cesar,
        "afin": afin,

        "frecuencias": {
            "original": freq_original,
            "cesar": freq_cesar,
            "afin": freq_afin
        },

        "indice_coincidencia": {
            "original": ic_original,
            "cesar": ic_cesar,
            "afin": ic_afin
        }
    }

def pedir_entero(mensaje):
    try:
        return int(input(mensaje))
    except ValueError:
        print("❌ Error: debe ingresar un número entero válido")
        return None

def ejecutar_comparador(alfabeto):

    print("\n--- COMPARADOR DE CIFRADOS ---")

    mensaje = input("Ingrese el mensaje: ")

    if not mensaje.strip():
        print("❌ Error: mensaje vacío")
        return

    if not all(c in alfabeto for c in mensaje):
        print("❌ Error: el mensaje contiene caracteres fuera del alfabeto seleccionado")
        return

    k = pedir_entero("Desplazamiento César: ")
    if k is None:
        return

    a = pedir_entero("Valor a (Afín): ")
    if a is None:
        return

    b = pedir_entero("Valor b (Afín): ")
    if b is None:
        return

    try:
        resultado = comparar_cifrados(mensaje, k, a, b, alfabeto)

        print("\n📌 RESULTADOS:")
        print("Original:", resultado["original"])
        print("César:", resultado["cesar"])
        print("Afín:", resultado["afin"])

        print("\n📊 ÍNDICE DE COINCIDENCIA:")
        print("Original:", resultado["indice_coincidencia"]["original"])
        print("César:", resultado["indice_coincidencia"]["cesar"])
        print("Afín:", resultado["indice_coincidencia"]["afin"])

        print("\n🧠 ANÁLISIS:")
        print(
            "Ambos cifrados son monoalfabéticos.\n"
            "No cambian la distribución de frecuencias,\n"
            "solo reordenan los símbolos.\n"
            "El Afín es más complejo que César,\n"
            "pero ambos son vulnerables a análisis de frecuencia."
        )

    except ValueError as e:
        print("❌ Error:", e)