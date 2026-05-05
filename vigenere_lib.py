def limpiar_texto(texto):
    return "".join(c for c in texto.upper() if c.isalpha())

def generar_clave(texto, clave):
    texto = limpiar_texto(texto)
    clave = limpiar_texto(clave)

    if not clave:
        raise ValueError("❌ La clave no puede estar vacía")

    return "".join(clave[i % len(clave)] for i in range(len(texto)))

def cifrar_vigenere(texto, clave, n=26):
    texto = limpiar_texto(texto)
    if not texto:
        return ""

    clave_ext = generar_clave(texto, clave)

    resultado = []
    for i in range(len(texto)):
        m = ord(texto[i]) - 65
        k = ord(clave_ext[i]) - 65
        c = (m + k) % n
        resultado.append(chr(c + 65))

    return "".join(resultado)

def descifrar_vigenere(texto, clave, n=26):
    texto = limpiar_texto(texto)
    if not texto:
        return ""

    clave_ext = generar_clave(texto, clave)

    resultado = []
    for i in range(len(texto)):
        c = ord(texto[i]) - 65
        k = ord(clave_ext[i]) - 65
        m = (c - k) % n
        resultado.append(chr(m + 65))

    return "".join(resultado)

def mostrar_proceso(texto, clave):
    texto = limpiar_texto(texto)
    clave_ext = generar_clave(texto, clave)
    cifrado = cifrar_vigenere(texto, clave)

    lineas = []
    lineas.append("Pos | M | K | C")
    lineas.append("----------------")

    for i in range(len(texto)):
        lineas.append(f"{i:>3} | {texto[i]} | {clave_ext[i]} | {cifrado[i]}")

    return "\n".join(lineas)

def mostrar_proceso_detallado(texto, clave):
    """Muestra el proceso paso a paso con valores numéricos"""
    texto = limpiar_texto(texto)
    clave_ext = generar_clave(texto, clave)
    cifrado = cifrar_vigenere(texto, clave)

    lineas = []
    lineas.append("=" * 70)
    lineas.append("PROCESO DETALLADO DE CIFRADO VIGENÈRE")
    lineas.append("=" * 70)

    for i in range(len(texto)):
        m_letra = texto[i]
        k_letra = clave_ext[i]
        c_letra = cifrado[i]

        m_val = ord(m_letra) - 65
        k_val = ord(k_letra) - 65
        c_val = ord(c_letra) - 65

        lineas.append(f"\nPosición {i}:")
        lineas.append(f"  {m_letra} + {k_letra} →")
        lineas.append(f"  {m_val} + {k_val} = {m_val + k_val}")
        lineas.append(f"  ({m_val + k_val}) mod 26 = {c_val}")
        lineas.append(f"  {c_val} → {c_letra} ✓")

    lineas.append("\n" + "=" * 70)
    lineas.append(f"Resultado: {cifrado}")
    lineas.append("=" * 70)

    return "\n".join(lineas)

def analisis_polialfabetico(texto, clave):
    texto = limpiar_texto(texto)
    clave_ext = generar_clave(texto, clave)
    cifrado = cifrar_vigenere(texto, clave)

    mapa = {}

    for i in range(len(texto)):
        m = texto[i]
        c = cifrado[i]

        if m not in mapa:
            mapa[m] = set()

        mapa[m].add(c)

    resultado = []
    resultado.append("🔍 ANÁLISIS POLIALFABÉTICO")
    resultado.append("-------------------------")

    for letra in sorted(mapa):
        cambios = ", ".join(sorted(mapa[letra]))
        resultado.append(f"{letra} → {cambios}")

    return "\n".join(resultado)

def dividir_en_columnas(texto, clave):
    texto = limpiar_texto(texto)
    clave = limpiar_texto(clave)

    columnas = [""] * len(clave)

    for i, letra in enumerate(texto):
        columnas[i % len(clave)] += letra

    return columnas


def resumen_vigenere(texto, clave):
    texto_limpio = limpiar_texto(texto)

    if not texto_limpio:
        return "❌ Texto inválido"

    cifrado = cifrar_vigenere(texto_limpio, clave)
    descifrado = descifrar_vigenere(cifrado, clave)

    columnas = dividir_en_columnas(texto_limpio, clave)

    return {
        "original": texto_limpio,
        "clave": limpiar_texto(clave),
        "clave_extendida": generar_clave(texto_limpio, clave),

        "cifrado": cifrado,
        "descifrado": descifrado,

        "proceso": mostrar_proceso(texto_limpio, clave),
        "analisis": analisis_polialfabetico(texto_limpio, clave),

        "columnas": columnas
    }