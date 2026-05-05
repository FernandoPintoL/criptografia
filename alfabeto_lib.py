import string

def limpiar_clave(clave, alfabeto):
    resultado = ""

    for letra in clave.upper():
        if letra in alfabeto and letra not in resultado:
            resultado += letra

    return resultado

def generar_alfabeto_mixto(clave="", alfabeto_base=None):

    if alfabeto_base is None:
        alfabeto_base = string.ascii_uppercase

    clave_limpia = limpiar_clave(clave, alfabeto_base)
    resto = "".join(letra for letra in alfabeto_base if letra not in clave_limpia)
    alfabeto_mixto = clave_limpia + resto

    if len(alfabeto_mixto) != len(alfabeto_base):
        raise ValueError("El alfabeto generado es inválido (longitud incorrecta)")

    if len(set(alfabeto_mixto)) != len(alfabeto_mixto):
        raise ValueError("El alfabeto generado tiene duplicados")

    return {
        "clave_original": clave,
        "clave_limpia": clave_limpia,
        "alfabeto_base": alfabeto_base,
        "alfabeto_mixto": alfabeto_mixto,
        "longitud": len(alfabeto_mixto)
    }