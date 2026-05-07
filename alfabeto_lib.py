import string
import random

# ================================================================================
# ALFABETO BASE ESTÁNDAR - Constante global
# ================================================================================
# Alfabeto base utilizado en todas las funciones por defecto
# Facilita mantener consistencia y cambiar si es necesario
ALFABETO_BASE = string.ascii_uppercase


# ================================================================================
# FUNCIÓN 1: VALIDAR CLAVE
# ================================================================================
def validar_clave(clave, alfabeto=ALFABETO_BASE):
    """
    Valida que la clave SOLO contenga caracteres válidos del alfabeto.

    PARÁMETROS:
        clave: Clave a validar (str)
        alfabeto: Alfabeto permitido (por defecto: A-Z mayúsculas)

    RETORNA:
        clave convertida a mayúsculas (str)

    LANZA EXCEPCIÓN:
        ValueError si la clave contiene caracteres inválidos

    EJEMPLOS:
        validar_clave("SECRETO") → "SECRETO" ✓
        validar_clave("secret") → "SECRET" ✓ (convertida a mayúsculas)
        validar_clave("SECRET0") → ERROR (contiene '0' que no está en alfabeto)
        validar_clave("ABC123") → ERROR (contiene números)

    USO EN CRIPTOGRAFÍA:
        Se ejecuta ANTES de limpiar_clave() para asegurar que
        los datos de entrada sean válidos desde el inicio.
    """
    clave = clave.upper()

    for c in clave:
        if c not in alfabeto:
            raise ValueError(
                f"Carácter inválido en clave: '{c}'. "
                f"Solo se permiten letras del alfabeto."
            )

    return clave


# ================================================================================
# FUNCIÓN 2: LIMPIAR CLAVE
# ================================================================================
def limpiar_clave(clave, alfabeto=ALFABETO_BASE):
    """
    Limpia la clave eliminando DUPLICADOS y caracteres inválidos.

    PROCESO:
        1. VALIDA la clave (lanza error si contiene caracteres inválidos)
        2. ELIMINA letras repetidas, manteniendo el orden original
        3. RETORNA la clave limpia

    PARÁMETROS:
        clave: Clave a limpiar (str)
        alfabeto: Alfabeto permitido (por defecto: A-Z mayúsculas)

    RETORNA:
        Clave limpia sin duplicados (str)

    EJEMPLOS:
        limpiar_clave("SECRETO") → "SECRETO" (7 únicos)
        limpiar_clave("SECRET") → "SECRET" (6 únicos)
        limpiar_clave("HELLOWORLD") → "HELOWRD" (7 únicos)
        limpiar_clave("AAABBBCCC") → "ABC" (3 únicos)
        limpiar_clave("ABC123") → ERROR (números no permitidos)

    DIFERENCIA CON VERSIÓN ANTERIOR:
        - Ahora VALIDA la clave primero
        - Antes: ignoraba silenciosamente caracteres inválidos
        - Ahora: lanza ERROR explícito para detectar problemas
    """
    clave = validar_clave(clave, alfabeto)

    resultado = ""

    for letra in clave:
        if letra not in resultado:
            resultado += letra

    return resultado


# ================================================================================
# FUNCIÓN 3: GENERAR ALFABETO MIXTO
# ================================================================================
def generar_alfabeto_mixto(clave="", aleatorio=False, alfabeto_base=ALFABETO_BASE):
    """
    Genera un ALFABETO MIXTO (sustitución) basado en una clave.

    PROCESO:
        1. LIMPIA la clave (elimina duplicados)
        2. GENERA el resto del alfabeto (letras no en clave)
        3. SI modo aleatorio: MEZCLA aleatoriamente el resto
        4. COMBINA: clave_limpia + resto (ordenado o aleatorio)

    PARÁMETROS:
        clave: Palabra clave para iniciar el alfabeto (str, default="")
        aleatorio: Si True, mezcla aleatoriamente el resto (bool, default=False)
        alfabeto_base: Alfabeto base a usar (default: A-Z mayúsculas)

    RETORNA:
        Diccionario con:
            - clave_original: clave tal como fue ingresada
            - clave_limpia: clave sin duplicados
            - alfabeto_base: alfabeto base usado
            - alfabeto_mixto: el alfabeto generado (sustitución)
            - modo: "normal" o "aleatorio"
            - longitud: 26 (para inglés)

    MODOS:

        MODO NORMAL (aleatorio=False):
            Genera alfabeto PREDECIBLE y ORDENADO
            generar_alfabeto_mixto("SECRET")
            → "SECRETABDFGHIJKLMNOPQTUVWXYZ"

            Estructura: [clave] + [A-Z restantes en orden]
            Uso: Educativo, para entender el sistema

        MODO ALEATORIO (aleatorio=True):
            Genera alfabeto ALEATORIO (más seguro)
            generar_alfabeto_mixto("SECRET", aleatorio=True)
            → "SECRETQWXZPDFGJKMLNHBUVYIO"  (puede variar)

            Estructura: [clave] + [A-Z restantes MEZCLADOS]
            Uso: Criptografía real, más seguridad

        SIN CLAVE + ALEATORIO:
            Genera sustitución totalmente aleatoria
            generar_alfabeto_mixto("", aleatorio=True)
            → "MXQPZWVFDLKBGNUOYSRTJCHIAE"  (completamente aleatorio)

            Uso: Máxima seguridad, sustitución pura

    EJEMPLOS:

        Ejemplo 1: Modo normal con clave
        >>> resultado = generar_alfabeto_mixto("SECRETO")
        >>> resultado["alfabeto_mixto"]
        'SECRETOABDFGHIJKLMNPQUVWXYZ'
        >>> resultado["modo"]
        'normal'

        Ejemplo 2: Modo aleatorio con clave
        >>> resultado = generar_alfabeto_mixto("SECRETO", aleatorio=True)
        >>> resultado["alfabeto_mixto"]
        'SECRETOWXZPDFGJKMLNHBQUVYIA'
        >>> resultado["modo"]
        'aleatorio'

        Ejemplo 3: Sustitución aleatoria pura
        >>> resultado = generar_alfabeto_mixto("", aleatorio=True)
        >>> resultado["alfabeto_mixto"]
        'QWXZPDFGJKMLNHBUVYIAERTOSCL'
        >>> resultado["clave_limpia"]
        ''

    SEGURIDAD:
        - NORMAL: NO es seguro (patrón predecible A-Z)
        - ALEATORIO: Más seguro (resta es aleatorio)
        - SIN CLAVE ALEATORIO: Máximamente seguro

    EDUCACIÓN:
        - Use NORMAL para mostrar el concepto
        - Use ALEATORIO para simulaciones reales
    """
    clave_limpia = limpiar_clave(clave, alfabeto_base)

    # Generar lista de letras restantes (no en clave)
    resto = [letra for letra in alfabeto_base if letra not in clave_limpia]

    # OPCIÓN 1: Si modo normal, mantener orden
    # OPCIÓN 2: Si modo aleatorio, mezclar
    if aleatorio:
        random.shuffle(resto)

    # Combinar: clave limpia + resto (ordenado o aleatorio)
    alfabeto_mixto = clave_limpia + "".join(resto)

    # Validaciones de seguridad
    if len(alfabeto_mixto) != len(alfabeto_base):
        raise ValueError("El alfabeto generado es inválido (longitud incorrecta)")

    if len(set(alfabeto_mixto)) != len(alfabeto_mixto):
        raise ValueError("El alfabeto generado tiene duplicados")

    return {
        "clave_original": clave,
        "clave_limpia": clave_limpia,
        "alfabeto_base": alfabeto_base,
        "alfabeto_mixto": alfabeto_mixto,
        "modo": "aleatorio" if aleatorio else "normal",
        "longitud": len(alfabeto_mixto)
    }