# vigenere.py

def obtener_posicion(letra, alfabeto):
    return alfabeto.index(letra)


def generar_clave_extendida(mensaje, clave, alfabeto):
    """
    Genera la clave repetida del tamaño del mensaje.
    """
    clave_ext = []
    i = 0

    for letra in mensaje:
        if letra in alfabeto:
            clave_ext.append(clave[i % len(clave)])
            i += 1
        else:
            clave_ext.append(letra)

    return "".join(clave_ext)


def cifrar_vigenere(mensaje, clave, alfabeto):
    """
    Cifra usando Vigenère:
        C = (P + K) mod n
    """

    n = len(alfabeto)
    resultado = []

    clave_ext = generar_clave_extendida(mensaje, clave, alfabeto)

    for i, letra in enumerate(mensaje):
        if letra in alfabeto:
            P = obtener_posicion(letra, alfabeto)
            K = obtener_posicion(clave_ext[i], alfabeto)

            C = (P + K) % n
            resultado.append(alfabeto[C])
        else:
            resultado.append(letra)

    return "".join(resultado), clave_ext


def analizar_polialfabetico(mensaje, cifrado):
    """
    Demuestra si una misma letra/carácter puede cifrarse de formas distintas.
    """
    mapa = {}

    for m, c in zip(mensaje, cifrado):
        if m not in mapa:
            mapa[m] = set()
        mapa[m].add(c)

    return mapa

def mostrar_proceso(mensaje, clave_ext, cifrado):
    """
    Muestra tabla paso a paso.
    """
    print("\nPos | M | K | C")
    print("----------------")

    for i in range(len(mensaje)):
        print(f"{i:>3} | {mensaje[i]} | {clave_ext[i]} | {cifrado[i]}")


def ejecutar_vigenere(alfabeto):

    print("\n--- CIFRADO VIGENÈRE ---")

    mensaje = input("Ingrese el mensaje: ")

    # ✅ VALIDACIÓN DEL MENSAJE ANTES DE PEDIR LA CLAVE
    if not mensaje.strip():
        print("❌ Error: el mensaje no puede estar vacío")
        return

    if not all(c in alfabeto for c in mensaje):
        print("❌ Error: el mensaje contiene caracteres fuera del alfabeto seleccionado")
        return

    clave = input("Ingrese la clave: ")

    # ✅ VALIDACIÓN DE LA CLAVE
    if not clave.strip():
        print("❌ Error: la clave no puede estar vacía")
        return

    if not all(c in alfabeto for c in clave):
        print("❌ Error: la clave contiene caracteres fuera del alfabeto seleccionado")
        return

    cifrado, clave_ext = cifrar_vigenere(mensaje, clave, alfabeto)

    print("\n📌 RESULTADOS:")
    print("Mensaje:", mensaje)
    print("Clave:", clave)
    print("Clave extendida:", clave_ext)
    print("Cifrado:", cifrado)

    print("\n📊 PROCESO:")
    mostrar_proceso(mensaje, clave_ext, cifrado)

    print("\n🔍 ANÁLISIS POLIALFABÉTICO:")
    mapa = analizar_polialfabetico(mensaje, cifrado)

    hay_variacion = False

    for letra in mapa:
        cambios = ", ".join(sorted(mapa[letra]))

        if len(mapa[letra]) > 1:
            hay_variacion = True
            print(f"{letra} → {cambios}  ✔ misma letra cifrada de formas distintas")
        else:
            print(f"{letra} → {cambios}")

    if not hay_variacion:
        print("\nℹ️ En este mensaje no se repite ningún carácter con claves distintas.")
        print("Para ver mejor el efecto polialfabético, prueba con un mensaje como: AAAAAA")