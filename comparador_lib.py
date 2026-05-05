import gcd_lib

def limpiar_texto(texto):
    """Solo letras A-Z en mayúsculas"""
    return "".join(c for c in texto.upper() if c.isalpha())

def cifrar_cesar(texto, k, n=26):
    texto = limpiar_texto(texto)
    if not texto:
        return ""

    resultado = []
    for letra in texto:
        x = ord(letra) - 65
        c = (x + k) % n
        resultado.append(chr(c + 65))

    return "".join(resultado)

def cifrar_afin(texto, a, b, n=26):
    if gcd_lib.gcd(a, n) != 1:
        return None

    texto = limpiar_texto(texto)
    if not texto:
        return ""

    resultado = []
    for letra in texto:
        x = ord(letra) - 65
        c = (a * x + b) % n
        resultado.append(chr(c + 65))

    return "".join(resultado)


def frecuencia(texto):
    total = len(texto)
    if total == 0:
        return {chr(i + 65): 0.0 for i in range(26)}

    freq = {chr(i + 65): 0 for i in range(26)}

    for letra in texto:
        freq[letra] += 1

    for letra in freq:
        freq[letra] = round((freq[letra] / total) * 100, 2)

    return freq

def indice_coincidencia(texto):
    N = len(texto)
    if N <= 1:
        return 0.0

    conteo = {}
    for c in texto:
        conteo[c] = conteo.get(c, 0) + 1

    suma = sum(f * (f - 1) for f in conteo.values())
    return round(suma / (N * (N - 1)), 4)


def generar_mapeo(k=None, a=None, b=None, n=26):
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    mapa_cesar = {}
    mapa_afin = {}

    for i, letra in enumerate(alfabeto):
        if k is not None:
            mapa_cesar[letra] = chr(((i + k) % n) + 65)
        if a is not None:
            mapa_afin[letra] = chr(((a * i + b) % n) + 65)

    return mapa_cesar, mapa_afin


def interpretar():
    return (
        "⚠️ Ambos cifrados son sustituciones monoalfabéticas.\n"
        "👉 No cambian la frecuencia de letras, solo las reordenan.\n"
        "🔐 El cifrado Afín es estructuralmente más complejo que César,\n"
        "pero ambos son vulnerables a análisis de frecuencia."
    )


def comparar_cifras(texto, k, a, b, n=26):
    texto_limpio = limpiar_texto(texto)

    if not texto_limpio:
        return "❌ El texto no contiene letras válidas"

    cesar = cifrar_cesar(texto_limpio, k, n)
    afin = cifrar_afin(texto_limpio, a, b, n)

    if afin is None:
        return "❌ 'a' no es válido para cifrado afín"

    freq_original = frecuencia(texto_limpio)
    freq_cesar = frecuencia(cesar)
    freq_afin = frecuencia(afin)

    ic_original = indice_coincidencia(texto_limpio)
    ic_cesar = indice_coincidencia(cesar)
    ic_afin = indice_coincidencia(afin)

    mapa_cesar, mapa_afin = generar_mapeo(k, a, b, n)

    analisis = interpretar()

    return {
        "original": texto_limpio,
        "cesar": cesar,
        "afin": afin,

        "freq_original": freq_original,
        "freq_cesar": freq_cesar,
        "freq_afin": freq_afin,

        "IC_original": ic_original,
        "IC_cesar": ic_cesar,
        "IC_afin": ic_afin,

        "mapa_cesar": mapa_cesar,
        "mapa_afin": mapa_afin,

        "analisis": analisis
    }