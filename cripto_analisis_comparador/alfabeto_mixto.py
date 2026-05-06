# alfabeto_mixto.py

def limpiar_clave(clave, alfabeto):
    """
    Elimina duplicados y caracteres inválidos de la clave.
    """
    resultado = ""

    for letra in clave:
        if letra in alfabeto and letra not in resultado:
            resultado += letra

    return resultado


def generar_alfabeto_mixto(clave, alfabeto_base):
    """
    Genera un alfabeto mixto respetando estrictamente el alfabeto seleccionado.
    No convierte mayúsculas/minúsculas automáticamente.
    """

    if clave is None:
        raise ValueError("La clave no puede ser None")

    clave = clave.strip()

    if not clave:
        return alfabeto_base
    
    # 🔥 VALIDACIÓN ESTRICTA (FORMA PRO)
    if not all(letra in alfabeto_base for letra in clave):
        raise ValueError(
            "La clave contiene caracteres no válidos para el alfabeto seleccionado"
        )

    # 🔤 Eliminar duplicados
    clave_limpia = ""
    for letra in clave:
        if letra not in clave_limpia:
            clave_limpia += letra

    # 🔄 Completar alfabeto
    resto = "".join(l for l in alfabeto_base if l not in clave_limpia)

    return clave_limpia + resto