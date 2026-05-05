from vigenere_breaker_v3 import romper_vigenere_v3, mostrar_resultado_v3
from vigenere_lib import limpiar_texto

def main():
    print("\n" + "🔓" * 40)
    print("ROMPER VIGENÈRE - VERSIÓN 3 (CHI-SQUARED)".center(80))
    print("🔓" * 40)

    while True:
        print("\n" + "=" * 80)
        print("ROMPER CIFRADO VIGENÈRE CON ANÁLISIS ESTADÍSTICO")
        print("=" * 80)

        print("\n📝 Ingresa el criptograma:")
        criptograma = input("\n👉 Criptograma: ").strip()

        if not criptograma:
            print("❌ Error: El criptograma no puede estar vacío")
            continue

        # Limpiar
        criptograma_limpio = limpiar_texto(criptograma)

        if not criptograma_limpio:
            print("❌ Error: El criptograma debe contener letras")
            continue

        print(f"\n✅ Longitud del criptograma: {len(criptograma_limpio)} caracteres")

        while True:
            try:
                longitud_clave = int(input("\n🔑 Longitud de la clave (encontrada por Kasiski): "))
                if longitud_clave < 1 or longitud_clave > len(criptograma_limpio):
                    print(f"❌ Error: La longitud debe estar entre 1 y {len(criptograma_limpio)}")
                    continue
                break
            except ValueError:
                print("❌ Error: Debes ingresar un número")

        print(f"\n⏳ Analizando con Chi-Squared Test...")
        print("   Esto es rápido incluso para claves largas...\n")

        try:
            resultado = romper_vigenere_v3(criptograma_limpio, longitud_clave)
            mostrar_resultado_v3(resultado)

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            continue

        # Preguntar si continuar
        nueva_prueba = input("\n¿Intentar con otro criptograma? (s/n): ").strip().lower()
        if nueva_prueba != 's':
            print("\n👋 ¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
