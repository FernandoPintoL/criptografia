# kasiski.py

from math_utils import mcd


def limpiar_texto(texto, alfabeto):
    return "".join(c for c in texto if c in alfabeto)


def encontrar_repeticiones(texto, longitud=3):
    """
    Busca subcadenas repetidas y guarda sus posiciones.
    """
    posiciones = {}

    for i in range(len(texto) - longitud + 1):
        sub = texto[i:i + longitud]

        if sub not in posiciones:
            posiciones[sub] = []

        posiciones[sub].append(i)

    return {k: v for k, v in posiciones.items() if len(v) > 1}


def calcular_distancias(posiciones):
    """
    Calcula todas las distancias entre repeticiones.
    """
    distancias = []

    for lista in posiciones.values():
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                distancias.append(lista[j] - lista[i])

    return distancias


def mcd_lista(numeros):
    if not numeros:
        return None

    resultado = numeros[0]

    for num in numeros[1:]:
        resultado = mcd(resultado, num)

    return resultado


def posibles_longitudes(mcd_valor):
    """
    Devuelve divisores del MCD.
    """
    if not mcd_valor or mcd_valor < 2:
        return []

    return [i for i in range(2, mcd_valor + 1) if mcd_valor % i == 0]


def kasiski(texto, alfabeto, longitud=3):
    """
    Aplica el método de Kasiski respetando estrictamente el alfabeto seleccionado.
    """

    texto = limpiar_texto(texto, alfabeto)

    if len(texto) < longitud:
        return {"error": "Texto demasiado corto"}

    repeticiones = encontrar_repeticiones(texto, longitud)

    if not repeticiones:
        return {
            "mensaje": "No se encontraron repeticiones",
            "repeticiones": {},
            "distancias": [],
            "mcd": None,
            "claves": []
        }

    distancias = calcular_distancias(repeticiones)
    valor_mcd = mcd_lista(distancias)
    claves = posibles_longitudes(valor_mcd)

    return {
        "texto": texto,
        "repeticiones": repeticiones,
        "distancias": distancias,
        "mcd": valor_mcd,
        "claves": claves
    }


def ejecutar_kasiski(alfabeto):

    print("\n--- MÉTODO DE KASISKI ---")

    texto = input("Ingrese el texto cifrado: ")

    if not texto.strip():
        print("❌ Error: el texto no puede estar vacío")
        return

    # ✅ Validación estricta
    if not all(c in alfabeto for c in texto):
        print("❌ Error: el texto contiene caracteres fuera del alfabeto seleccionado")
        return

    resultado = kasiski(texto, alfabeto)

    if "error" in resultado:
        print("❌ Error:", resultado["error"])
        return

    print("\n📌 REPETICIONES:")

    if resultado["repeticiones"]:
        for sub, pos in resultado["repeticiones"].items():
            print(f"{sub} → {pos}")
    else:
        print("No se encontraron repeticiones.")

    print("\n📏 DISTANCIAS:")
    print(resultado["distancias"])

    print("\n📊 MCD:")
    print(resultado["mcd"])

    print("\n🔑 POSIBLES LONGITUDES DE CLAVE:")
    print(resultado["claves"])

    print("\n🧠 INTERPRETACIÓN:")
    print(
        "Las distancias entre repeticiones suelen ser múltiplos de la longitud de la clave.\n"
        "El MCD aproxima esa longitud.\n"
        "Los divisores del MCD son posibles tamaños de clave."
    )