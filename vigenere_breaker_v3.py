from vigenere_lib import descifrar_vigenere, limpiar_texto
from collections import Counter
import math

# Frecuencias esperadas de letras en inglés (%)
FRECUENCIAS_INGLES = {
    'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127, 'F': 0.022,
    'G': 0.020, 'H': 0.061, 'I': 0.070, 'J': 0.002, 'K': 0.008, 'L': 0.040,
    'M': 0.024, 'N': 0.067, 'O': 0.075, 'P': 0.019, 'Q': 0.001, 'R': 0.060,
    'S': 0.063, 'T': 0.091, 'U': 0.028, 'V': 0.010, 'W': 0.024, 'X': 0.002,
    'Y': 0.020, 'Z': 0.001
}

def dividir_en_columnas(criptograma, longitud_clave):
    """Divide el criptograma en columnas según la longitud de clave"""
    columnas = [""] * longitud_clave
    for i, letra in enumerate(criptograma):
        columnas[i % longitud_clave] += letra
    return columnas


def chi_squared(texto):
    """
    Calcula chi-squared entre frecuencias observadas y esperadas.
    Menor valor = más parecido a inglés.
    """
    contador = Counter(texto)
    n = len(texto)

    chi2 = 0
    for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        observado = contador.get(letra, 0)
        esperado = FRECUENCIAS_INGLES[letra] * n

        if esperado > 0:
            chi2 += ((observado - esperado) ** 2) / esperado

    return chi2


def encontrar_desplazamiento_chi_squared(columna):
    """
    Encuentra el desplazamiento más probable usando chi-squared test.
    Prueba todos los 26 desplazamientos y elige el mejor.
    """
    mejor_desplazamiento = 0
    mejor_chi2 = float('inf')

    for desplazamiento in range(26):
        # Descifrar columna con este desplazamiento
        descifrada = ""
        for letra in columna:
            valor = ord(letra) - 65
            nuevo_valor = (valor - desplazamiento) % 26
            descifrada += chr(nuevo_valor + 65)

        # Calcular chi-squared
        chi2 = chi_squared(descifrada)

        if chi2 < mejor_chi2:
            mejor_chi2 = chi2
            mejor_desplazamiento = desplazamiento

    return mejor_desplazamiento, mejor_chi2


def romper_vigenere_chi_squared(criptograma, longitud_clave):
    """
    Rompe Vigenère usando chi-squared test en cada columna.
    Mucho más rápido y preciso que fuerza bruta.
    """
    print(f"\n🔓 ANALIZANDO CON CHI-SQUARED TEST")
    print(f"Longitud de clave: {longitud_clave}")
    print("=" * 80)

    criptograma = limpiar_texto(criptograma)
    columnas = dividir_en_columnas(criptograma, longitud_clave)

    clave_encontrada = ""
    chi2_total = 0

    print("\n📊 Análisis por columna:")
    print("-" * 80)

    for i, columna in enumerate(columnas):
        desplazamiento, chi2 = encontrar_desplazamiento_chi_squared(columna)
        letra_clave = chr(desplazamiento % 26 + 65)
        clave_encontrada += letra_clave
        chi2_total += chi2

        print(f"Columna {i}: Chi²={chi2:8.2f} → Desplazamiento={desplazamiento:2d} → Letra='{letra_clave}'")

    print(f"\nChi² Total: {chi2_total:.2f}")
    print(f"🔑 Clave encontrada: {clave_encontrada}")

    # Descifrar
    descifrado = descifrar_vigenere(criptograma, clave_encontrada)

    return {
        "clave": clave_encontrada,
        "descifrado": descifrado,
        "metodo": "Chi-Squared Test (Análisis Estadístico)",
        "chi2_score": chi2_total
    }


def romper_vigenere_v3(criptograma, longitud_clave):
    """
    Versión 3: Usa chi-squared test para romper Vigenère.
    Es rápido incluso con claves largas (hasta 10+ caracteres).
    """
    print("\n" + "🔓" * 40)
    print("DESCIFRANDO VIGENÈRE - CHI-SQUARED TEST".center(80))
    print("🔓" * 40)

    criptograma = limpiar_texto(criptograma)

    print(f"\n✅ Longitud de clave: {longitud_clave}")
    print(f"✅ Longitud del criptograma: {len(criptograma)}")

    print(f"\n⏳ Analizando cada columna...")

    resultado = romper_vigenere_chi_squared(criptograma, longitud_clave)

    return resultado


def mostrar_resultado_v3(resultado):
    """Muestra el resultado final"""
    print("\n" + "=" * 80)
    print("✅ DESCIFRADO COMPLETADO")
    print("=" * 80)
    print(f"\n🔑 Método: {resultado['metodo']}")
    print(f"🔑 Clave encontrada: {resultado['clave']}")
    print(f"📊 Score (Chi²): {resultado['chi2_score']:.2f} (menor = mejor)")
    print(f"\n📝 Primeros 200 caracteres del texto descifrado:")
    print(f"{resultado['descifrado'][:200]}...")
    print("\n" + "=" * 80)

    # Preguntar si ver completo
    ver = input("\n¿Ver texto completo? (s/n): ").strip().lower()
    if ver == 's':
        print("\n" + "=" * 80)
        print("📝 TEXTO DESCIFRADO COMPLETO")
        print("=" * 80)
        print(resultado['descifrado'])
        print("=" * 80)

    return resultado
