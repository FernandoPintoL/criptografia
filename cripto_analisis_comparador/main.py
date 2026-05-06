# main.py

from analisis_afin import analizar_constante
from alfabeto_mixto import generar_alfabeto_mixto
from criptoanalisis import criptoanalisis
from vigenere import ejecutar_vigenere
from kasiski import ejecutar_kasiski
from comparador import ejecutar_comparador

from alfabetos import obtener_alfabeto, mostrar_menu_alfabetos


def pedir_entero(mensaje):
    """
    Pide un número entero de forma segura.
    """
    try:
        return int(input(mensaje))
    except ValueError:
        print("❌ Error: debe ingresar un número entero válido")
        return None


def seleccionar_alfabeto():
    mostrar_menu_alfabetos()
    opcion = input("Seleccione el tipo de alfabeto: ")

    alfabeto = obtener_alfabeto(opcion)

    if not alfabeto:
        print("Error: opción de alfabeto inválida")
        return None

    return alfabeto


def ejecutar_analisis_afin_ui(alfabeto):
    print("\n--- VALIDADOR DE CONSTANTE 'a' ---")

    n = len(alfabeto)
    print(f"Tamaño del alfabeto (n): {n}")

    a = pedir_entero("Ingrese el valor de a: ")
    if a is None:
        return

    resultado = analizar_constante(a, n)

    print("\n📌 RESULTADO:")

    if resultado["valido"]:
        print("✔ VÁLIDO")
        print(f"mcd({a}, {n}) = 1 → son coprimos")
        print("✔ Existe inverso modular")
        print("✔ Se puede usar en el cifrado Afín")
    else:
        print("❌ INVÁLIDO")
        print(f"mcd({a}, {n}) = {resultado['mcd']}")

        if resultado["factores"]:
            print("Factores comunes:", resultado["factores"])

        print("💡 Al compartir factores, no existe inverso modular")
        print("❌ No se puede usar en el cifrado Afín")


def ejecutar_alfabeto_mixto_ui(alfabeto):
    print("\n--- GENERADOR DE ALFABETO MIXTO ---")

    clave = input("Ingrese la palabra clave (puede estar vacía): ")

    try:
        resultado = generar_alfabeto_mixto(clave, alfabeto)

        print("\n📌 RESULTADO:")
        print(f"Alfabeto base (n = {len(alfabeto)}):")

        # 🔥 MOSTRAR DE FORMA SEGURA
        print(repr(alfabeto))

        print("\nAlfabeto mixto:")
        print(repr(resultado))

    except Exception as e:
        print("❌ Error:", e)


def menu():
    while True:

        print("\n----SISTEMA DE CIFRADOS CLÁSICOS----")
        print("1. Validador de Constante de Decimación")
        print("2. Generador de Alfabetos Mixtos")
        print("3. Módulo de Criptoanálisis por Ecuaciones")
        print("4. Comparador de Cifras Clásicas")
        print("5. Motor del Cifrador Polialfabético de Vigenère")
        print("6. Detector del Periodo mediante el Método de Kasiski")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        # EJERCICIO 1
        if opcion == "1":
            alfabeto = seleccionar_alfabeto()
            if not alfabeto:
                continue

            ejecutar_analisis_afin_ui(alfabeto)

        # EJERCICIO 2
        elif opcion == "2":
            alfabeto = seleccionar_alfabeto()
            if not alfabeto:
                continue

            ejecutar_alfabeto_mixto_ui(alfabeto)

        # EJERCICIO 3
        elif opcion == "3":
            alfabeto = seleccionar_alfabeto()
            if not alfabeto:
                continue

            criptoanalisis(alfabeto)

        # EJERCICIO 4
        elif opcion == "4":
            alfabeto = seleccionar_alfabeto()
            if not alfabeto:
                continue

            ejecutar_comparador(alfabeto)

        # EJERCICIO 5
        elif opcion == "5":
            alfabeto = seleccionar_alfabeto()
            if not alfabeto:
                continue

            ejecutar_vigenere(alfabeto)

        # EJERCICIO 6
        elif opcion == "6":
            alfabeto = seleccionar_alfabeto()
            if not alfabeto:
                continue

            ejecutar_kasiski(alfabeto)

        elif opcion == "0":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()