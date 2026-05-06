# alfabetos.py

def mostrar_menu_alfabetos():
    print("\nSeleccione tipo de alfabeto:")
    print("1. Letras mayúsculas con Ñ (mod 27)")
    print("2. Letras mayúsculas + números (mod 37)")
    print("3. Letras mayúsculas, minúsculas y tildes (mod 64)")
    print("4. Letras + números (mod 74)")
    print("5. ASCII extendido (mod 224)")


def validar_alfabeto(alfabeto):
    """
    Verifica que el alfabeto no tenga duplicados.
    """
    if len(set(alfabeto)) != len(alfabeto):
        raise ValueError("El alfabeto contiene caracteres duplicados")


def obtener_alfabeto(opcion):
    """
    Devuelve un alfabeto según la opción elegida.
    """

    alfabetos = {

        "1": "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ",

        "2": "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789",

        "3": (
            "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
            "abcdefghijklmnñopqrstuvwxyz"
            "ÁÉÍÓÚáéíóú"
        ),

        "4": (
            "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
            "abcdefghijklmnñopqrstuvwxyz"
            "ÁÉÍÓÚáéíóú"
            "0123456789"
        ),

        "5": ''.join(chr(i) for i in range(32, 256))
    }

    alfabeto = alfabetos.get(opcion)

    if not alfabeto:
        return None

    # 🔒 Validación importante
    validar_alfabeto(alfabeto)

    return alfabeto