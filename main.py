import gcd_lib
import alfabeto_lib
import vigenere_lib
import kasiski_lib
from cripto_analisis_comparador.criptoanalisis import criptoanalisis
from cripto_analisis_comparador.comparador import ejecutar_comparador
from cripto_analisis_comparador.alfabetos import obtener_alfabeto, mostrar_menu_alfabetos

def pedir_entero(mensaje):
    """Pide un número entero de forma segura"""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("❌ Debes ingresar un número entero válido")


def mostrar_menu():
    print("\n===== MENÚ GCD / CRIPTO =====")
    print("1. Calcular MCD")
    print("2. Verificar si son coprimos")
    print("3. Validar constante (cripto)")
    print("4. Generar alfabeto mixto 🔤")
    print("5. Criptoanálisis (resolver a y b) 🔍")
    print("6. Comparar César vs Afín 📊")  
    print("7. Vigenère (polialfabético) 🔐")
    print("8. Método de Kasiski 🔎")
    print("9. Salir")


def menu():
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            a = pedir_entero("Ingrese a: ")
            b = pedir_entero("Ingrese b: ")
            print(f"\n👉 MCD({a}, {b}) = {gcd_lib.gcd(a, b)}")

        elif opcion == "2":
            a = pedir_entero("Ingrese a: ")
            b = pedir_entero("Ingrese b: ")
            if gcd_lib.gcd(a, b) == 1:
                print(f"\n✔ {a} y {b} son coprimos")
            else:
                print(f"\n❌ {a} y {b} NO son coprimos")

        elif opcion == "3":
            print("\n🔐 VALIDADOR DE CONSTANTE")
            a = pedir_entero("Ingrese a: ")
            n = pedir_entero("Ingrese n (módulo): ")

            if n <= 1:
                print("\n❌ El módulo n debe ser mayor que 1")
                continue

            resultado = gcd_lib.validar_constante(a, n)

            if "❌" in resultado:
                print("\n🚨 ALERTA CRIPTOGRÁFICA 🚨")
            else:
                print("\n✅ CONFIGURACIÓN VÁLIDA")

            print(resultado)

        elif opcion == "4":
            print("\n🔤 GENERADOR DE ALFABETO MIXTO")
            clave = input("Ingrese palabra clave (opcional): ")

            try:
                data = alfabeto_lib.generar_alfabeto_mixto(clave)

                print("\n📌 RESULTADO:")
                print(f"Clave original: {data['clave_original']}")
                print(f"Clave limpia:   {data['clave_limpia']}")
                print(f"Alfabeto base:  {data['alfabeto_base']}")
                print(f"Alfabeto mixto: {data['alfabeto_mixto']}")
                print(f"Longitud:       {data['longitud']}")

            except Exception as e:
                print(f"\n❌ Error: {e}")

        elif opcion == "5":
            print("\n🔍 CRIPTOANÁLISIS (C = aM + b mod n)")

            mostrar_menu_alfabetos()
            opcion_alfabeto = input("Seleccione el tipo de alfabeto: ")
            alfabeto = obtener_alfabeto(opcion_alfabeto)

            if not alfabeto:
                print("❌ Error: opción de alfabeto inválida")
                continue

            criptoanalisis(alfabeto)

        elif opcion == "6":
            print("\n📊 COMPARADOR DE CIFRAS (César vs Afín)")

            mostrar_menu_alfabetos()
            opcion_alfabeto = input("Seleccione el tipo de alfabeto: ")
            alfabeto = obtener_alfabeto(opcion_alfabeto)

            if not alfabeto:
                print("❌ Error: opción de alfabeto inválida")
                continue

            ejecutar_comparador(alfabeto)

        elif opcion == "7":
            print("\n🔐 VIGENÈRE (POLIALFABÉTICO)")

            texto = input("Ingrese texto: ")
            clave = input("Ingrese clave: ")

            try:
                cifrado = vigenere_lib.cifrar_vigenere(texto, clave)
                descifrado = vigenere_lib.descifrar_vigenere(cifrado, clave)

                print("\n📌 RESULTADOS:")
                print("Original:", vigenere_lib.limpiar_texto(texto))
                print("Clave:", vigenere_lib.limpiar_texto(clave))
                print("Cifrado:", cifrado)
                print("Descifrado:", descifrado)

                print("\n📊 PROCESO:")
                print(vigenere_lib.mostrar_proceso(texto, clave))

                print("\n🔍 ANÁLISIS:")
                print(vigenere_lib.analisis_polialfabetico(texto, clave))

            except Exception as e:
                print("\n❌ Error:", e)

        elif opcion == "8":
            print("\n🔎 MÉTODO DE KASISKI")

            texto = input("Ingrese texto cifrado: ")
            n = pedir_entero("Longitud de patrón (3 recomendado): ")

            resultado = kasiski_lib.resumen_kasiski(texto, n)

            print("\n📌 RESULTADO:")
            print(resultado)

        elif opcion == "9":
            print("\n👋 Saliendo...")
            break

        else:
            print("\n❌ Opción inválida")


if __name__ == "__main__":
    menu()