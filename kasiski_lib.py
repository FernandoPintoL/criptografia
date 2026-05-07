import gcd_lib

def limpiar_texto(texto):
    return "".join(c for c in texto.upper() if c.isalpha())

def buscar_repeticiones(texto, n=3):
    posiciones = {}

    for i in range(len(texto) - n + 1):
        patron = texto[i:i + n]

        if patron in posiciones:
            posiciones[patron].append(i)
        else:
            posiciones[patron] = [i]

    repetidos = {}

    for patron, pos in posiciones.items():
        if len(pos) > 1:
            repetidos[patron] = pos

    return repetidos

def calcular_distancias(repeticiones):
    distancias = []

    for pos in repeticiones.values():
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                distancias.append(pos[j] - pos[i])

    return distancias

def calcular_mcd_lista(lista):
    if not lista:
        return None

    resultado = lista[0]
    for x in lista[1:]:
        resultado = gcd_lib.gcd(resultado, x)

    return resultado

def kasiski(texto, n=3):

    texto_original = texto
    texto = limpiar_texto(texto)

    if len(texto) < n:
        return {
            "mensaje": "❌ Texto demasiado corto para análisis",
            "texto_original": texto_original,
            "texto_limpio": texto,
            "repeticiones": {},
            "distancias": [],
            "mcd": None,
            "posibles_claves": []
        }

    repeticiones = buscar_repeticiones(texto, n)
    distancias = calcular_distancias(repeticiones)

    if not distancias:
        return {
            "mensaje": "❌ No se encontraron repeticiones útiles",
            "texto_original": texto_original,
            "texto_limpio": texto,
            "repeticiones": repeticiones,
            "distancias": [],
            "mcd": None,
            "posibles_claves": []
        }

    mcd = calcular_mcd_lista(distancias)

    posibles = []

    if mcd:
        for i in range(2, mcd + 1):
            if mcd % i == 0:
                posibles.append(i)

    return {
        "mensaje": "✔ Análisis Kasiski completado",
        "texto_original": texto_original,
        "texto_limpio": texto,
        "repeticiones": repeticiones,
        "distancias": distancias,
        "mcd": mcd,
        "posibles_claves": posibles
    }

def resumen_kasiski(texto, n=3):
    """
    Salida amigable para consola
    """
    data = kasiski(texto, n)

    resultado = []
    resultado.append("🔍 MÉTODO DE KASISKI")
    resultado.append("--------------------")

    resultado.append(f"Mensaje: {data['mensaje']}")
    resultado.append(f"MCD estimado: {data['mcd']}")
    resultado.append(f"Posibles longitudes de clave: {data['posibles_claves']}")

    resultado.append("\n📌 Repeticiones:")
    for k, v in data["repeticiones"].items():
        resultado.append(f"{k} → {v}")

    resultado.append("\n📏 Distancias:")
    resultado.append(str(data["distancias"]))

    return "\n".join(resultado)