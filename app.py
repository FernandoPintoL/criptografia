import streamlit as st
import gcd_lib
import alfabeto_lib
import criptoanalisis_lib
import comparador_lib
import vigenere_lib
import kasiski_lib
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="🔐 Criptoanálisis Polialfabético",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🔐 Motor Criptográfico Polialfabético")
st.markdown("Herramienta educativa para análisis de cifrados clásicos")

# Menú en sidebar
opcion = st.sidebar.radio(
    "📋 Selecciona una opción",
    [
        "🏠 Inicio",
        "🔐 Vigenère (Polialfabético)",
        "🔎 Método de Kasiski",
        "🔤 Alfabeto Mixto",
        "🔍 Criptoanálisis",
        "📊 Comparador César vs Afín",
        "✔ Validador de Constante"
    ]
)

# ======================== 🏠 INICIO ========================
if opcion == "🏠 Inicio":
    st.header("Bienvenido al Motor Criptográfico")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Módulos Disponibles")
        st.markdown("""
        1. **🔐 Vigenère** - Cifrador polialfabético con análisis detallado
        2. **🔎 Kasiski** - Detecta la longitud probable de clave
        3. **🔤 Alfabeto Mixto** - Generador de alfabetos personalizados
        4. **🔍 Criptoanálisis** - Ataque por ecuaciones simultáneas
        5. **📊 Comparador** - Análisis César vs Afín
        6. **✔ Validador** - Verifica parámetros criptográficos
        """)

    with col2:
        st.subheader("🎯 Características")
        st.markdown("""
        ✅ Análisis paso a paso
        ✅ Visualización de procesos
        ✅ Gráficos estadísticos
        ✅ Validaciones automáticas
        ✅ Explicaciones detalladas
        ✅ Soporte para múltiples parámetros
        """)

    st.divider()
    st.subheader("💡 ¿Por dónde empezar?")
    st.info("""
    **Para principiantes:**
    1. Comienza con el **Comparador** para entender César vs Afín
    2. Explora **Vigenère** para ver cifrados polialfabéticos
    3. Usa **Kasiski** para romper Vigenère

    **Para avanzados:**
    1. Intenta **Criptoanálisis** con ecuaciones
    2. Experimenta con **Alfabetos Mixtos**
    3. Valida constantes con el **Validador**
    """)

# ======================== 🔐 VIGENÈRE ========================
elif opcion == "🔐 Vigenère (Polialfabético)":
    st.header("🔐 Cifrado de Vigenère")
    st.markdown("Cifrador polialfabético que demuestra cómo una misma letra se cifra diferente según su posición.")

    col1, col2 = st.columns(2)

    with col1:
        texto = st.text_area("Texto a cifrar:", placeholder="Ingrese el texto aquí", height=100)
        clave = st.text_input("Clave (palabra clave):", placeholder="Ej: SECRETO")

    with col2:
        if st.button("🔐 Cifrar", key="btn_vigenere_cifrar"):
            if not texto or not clave:
                st.error("❌ Por favor ingrese texto y clave")
            else:
                try:
                    resultado = vigenere_lib.resumen_vigenere(texto, clave)

                    st.success("✔ Cifrado exitoso")

                    tab1, tab2, tab3, tab4 = st.tabs(["Resultados", "Proceso", "Análisis", "Información"])

                    with tab1:
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write("**Texto Original:**")
                            st.code(resultado["original"], language=None)
                        with col_b:
                            st.write("**Texto Cifrado:**")
                            st.code(resultado["cifrado"], language=None)

                        st.write("**Clave Extendida:**")
                        st.code(resultado["clave_extendida"], language=None)

                        st.write("**Verificación (Descifrado):**")
                        st.code(resultado["descifrado"], language=None)

                    with tab2:
                        st.write("**Proceso Paso a Paso:**")
                        st.code(resultado["proceso"], language=None)

                    with tab3:
                        st.write("**Análisis Polialfabético:**")
                        st.code(resultado["analisis"], language=None)
                        st.info("🔍 Observe cómo cada letra se cifra de múltiples formas según su posición.")

                    with tab4:
                        st.markdown("""
                        **¿Cómo funciona Vigenère?**
                        - Cada letra de la clave actúa como desplazamiento
                        - A diferencia de César, el desplazamiento cambia en cada posición
                        - Esto rompe la correspondencia única de los sistemas monoalfabéticos

                        **Fórmula:** C = (M + K) mod 26
                        - C: letra cifrada
                        - M: letra original
                        - K: letra de la clave
                        """)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ======================== 🔎 KASISKI ========================
elif opcion == "🔎 Método de Kasiski":
    st.header("🔎 Método de Kasiski")
    st.markdown("Detecta la longitud probable de clave en cifrados de Vigenère buscando repeticiones.")

    col1, col2 = st.columns(2)

    with col1:
        criptograma = st.text_area("Criptograma (texto cifrado):", placeholder="Ingrese el texto cifrado", height=100)
        n = st.number_input("Longitud de patrón:", min_value=2, max_value=10, value=3)

    with col2:
        if st.button("🔎 Analizar", key="btn_kasiski"):
            if not criptograma:
                st.error("❌ Por favor ingrese un criptograma")
            else:
                try:
                    resultado = kasiski_lib.kasiski(criptograma, n)

                    st.success("✔ Análisis completado")

                    tab1, tab2, tab3 = st.tabs(["Resultados", "Detalles", "Información"])

                    with tab1:
                        st.write(kasiski_lib.resumen_kasiski(criptograma, n))

                    with tab2:
                        col_a, col_b = st.columns(2)

                        with col_a:
                            st.write("**MCD Estimado:**")
                            st.metric("MCD", resultado["mcd"] if resultado["mcd"] else "N/A")

                            st.write("**Posibles Longitudes de Clave:**")
                            st.code(str(resultado["posibles_claves"]), language=None)

                        with col_b:
                            st.write("**Distancias Encontradas:**")
                            st.code(str(resultado["distancias"]), language=None)

                        st.write("**Repeticiones Detectadas:**")
                        for patron, posiciones in list(resultado["repeticiones"].items())[:10]:
                            st.write(f"- `{patron}` en posiciones: {posiciones}")

                    with tab3:
                        st.markdown("""
                        **¿Cómo funciona Kasiski?**
                        1. Busca patrones repetidos de n caracteres
                        2. Calcula distancias entre repeticiones
                        3. Halla el MCD de todas las distancias
                        4. El MCD (o sus divisores) es la longitud probable de clave

                        **¿Por qué funciona?**
                        Si el mismo texto se cifra con la misma parte de la clave,
                        aparecerá el mismo criptograma, y la distancia será múltiplo de la longitud.
                        """)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ======================== 🔤 ALFABETO MIXTO ========================
elif opcion == "🔤 Alfabeto Mixto":
    st.header("🔤 Generador de Alfabetos Mixtos")
    st.markdown("Crea alfabetos personalizados basados en palabras clave para dificultar el análisis.")

    col1, col2 = st.columns(2)

    with col1:
        clave = st.text_input("Palabra clave (opcional):", placeholder="Ej: SECRETO")
        if st.button("🔤 Generar", key="btn_alfabeto"):
            try:
                resultado = alfabeto_lib.generar_alfabeto_mixto(clave)

                tab1, tab2 = st.tabs(["Resultado", "Información"])

                with tab1:
                    st.success("✔ Alfabeto generado")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Clave Original:**")
                        st.code(resultado["clave_original"] if resultado["clave_original"] else "(vacía)", language=None)

                        st.write("**Clave Limpia:**")
                        st.code(resultado["clave_limpia"], language=None)

                    with col_b:
                        st.write("**Alfabeto Base:**")
                        st.code(resultado["alfabeto_base"], language=None)

                        st.write("**Longitud:**")
                        st.metric("Caracteres", resultado["longitud"])

                    st.divider()
                    st.write("**Alfabeto Mixto Generado:**")
                    st.code(resultado["alfabeto_mixto"], language=None)

                    # Mapeo visual
                    st.write("**Mapeo de Sustitución:**")
                    alfabeto_base = resultado["alfabeto_base"]
                    alfabeto_mixto = resultado["alfabeto_mixto"]

                    mapeo_visual = " → ".join([f"{b}" for b in alfabeto_base[:5]]) + " → ..."
                    mapeo_a = " → ".join([f"{m}" for m in alfabeto_mixto[:5]]) + " → ..."

                    col_map1, col_map2 = st.columns(2)
                    with col_map1:
                        st.write("**Original:**")
                        st.code(mapeo_visual)
                    with col_map2:
                        st.write("**Mixto:**")
                        st.code(mapeo_a)

                with tab2:
                    st.markdown("""
                    **¿Cómo funciona?**
                    1. Se limpia la clave (mayúsculas, sin duplicados)
                    2. Se coloca la clave al inicio del alfabeto
                    3. Se agregan las letras restantes en orden

                    **Ejemplo con clave "SECRETO":**
                    - Original: ABCDEFGHIJKLMNOPQRSTUVWXYZ
                    - Mixto: SECRETOABDFGHIJKLMNOPQUVWXYZ

                    **Utilidad:**
                    - Base para cifrados de sustitución simple
                    - Inicialización de matriz Playfair
                    - Análisis educativo
                    """)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ======================== 🔍 CRIPTOANÁLISIS ========================
elif opcion == "🔍 Criptoanálisis":
    st.header("🔍 Criptoanálisis por Ecuaciones")
    st.markdown("Ataque al Cifrado Afín mediante dos correspondencias conocidas: C₁=aM₁+b y C₂=aM₂+b")

    st.info("💡 Ingrese dos pares (Criptograma, Plaintext) y el sistema resolverá para hallar `a` y `b`")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Primer par:**")
        C1 = st.number_input("C₁ (criptograma 1):", min_value=0, max_value=25, value=5)
        M1 = st.number_input("M₁ (plaintext 1):", min_value=0, max_value=25, value=0)

    with col2:
        st.write("**Segundo par:**")
        C2 = st.number_input("C₂ (criptograma 2):", min_value=0, max_value=25, value=8)
        M2 = st.number_input("M₂ (plaintext 2):", min_value=0, max_value=25, value=1)

    with col3:
        st.write("**Parámetros:**")
        n = st.number_input("Módulo n:", min_value=1, max_value=1000, value=26)
        if st.button("🔍 Resolver", key="btn_crypto"):
            resultado = criptoanalisis_lib.resolver_afine(C1, M1, C2, M2, n)

            if "✔" in resultado:
                st.success(resultado)

                # Extraer a y b
                lineas = resultado.split('\n')
                datos = lineas[0].split(',')
                a = int(datos[0].split('=')[1].strip())
                b = int(datos[1].split('=')[1].strip())

                st.divider()

                tab1, tab2 = st.tabs(["Verificación", "Información"])

                with tab1:
                    st.write("**Verificación de la solución:**")
                    col_v1, col_v2 = st.columns(2)

                    with col_v1:
                        C1_calc = (a * M1 + b) % n
                        C2_calc = (a * M2 + b) % n
                        st.write(f"C₁ = ({a} × {M1} + {b}) mod {n} = {C1_calc} ✓" if C1_calc == C1 else f"Error: {C1_calc} ≠ {C1}")
                        st.write(f"C₂ = ({a} × {M2} + {b}) mod {n} = {C2_calc} ✓" if C2_calc == C2 else f"Error: {C2_calc} ≠ {C2}")

                with tab2:
                    st.markdown(f"""
                    **Parámetros encontrados:**
                    - a = {a} (multiplicador)
                    - b = {b} (desplazamiento)
                    - n = {n} (módulo)

                    **Fórmula:** C = ({a}M + {b}) mod {n}

                    **Sistema resuelto:**
                    1. ΔC = {(C1-C2)%n}, ΔM = {(M1-M2)%n}
                    2. a ≡ ΔC × (ΔM)⁻¹ (mod {n})
                    3. b ≡ C₁ - a×M₁ (mod {n})
                    """)
            else:
                st.error(resultado)
                st.warning("⚠️ No se pudo resolver el sistema. Verifique que las correspondencias sean válidas.")

# ======================== 📊 COMPARADOR ========================
elif opcion == "📊 Comparador César vs Afín":
    st.header("📊 Comparador de Cifras Clásicas")
    st.markdown("Cifra el mismo mensaje con César y Afín para observar cómo cambia la distribución.")

    col1, col2 = st.columns(2)

    with col1:
        texto = st.text_area("Texto a cifrar:", placeholder="Ingrese el texto", height=80)
        k = st.number_input("k (desplazamiento César):", min_value=1, max_value=25, value=3)

    with col2:
        a = st.number_input("a (multiplicador Afín):", min_value=1, max_value=25, value=5)
        b = st.number_input("b (desplazamiento Afín):", min_value=0, max_value=25, value=8)

        if st.button("📊 Comparar", key="btn_comparar"):
            resultado = comparador_lib.comparar_cifras(texto, k, a, b)

            if isinstance(resultado, str):
                st.error(resultado)
            else:
                st.success("✔ Análisis completado")

                tab1, tab2, tab3, tab4 = st.tabs(["Resultados", "Frecuencias", "Mapeos", "Análisis"])

                with tab1:
                    col_res1, col_res2, col_res3 = st.columns(3)

                    with col_res1:
                        st.write("**Original:**")
                        st.code(resultado["original"], language=None)

                    with col_res2:
                        st.write("**César (k={}):**".format(k))
                        st.code(resultado["cesar"], language=None)

                    with col_res3:
                        st.write("**Afín (a={}, b={}):**".format(a, b))
                        st.code(resultado["afin"], language=None)

                with tab2:
                    col_freq1, col_freq2 = st.columns(2)

                    with col_freq1:
                        st.write("**IC (Índice de Coincidencia):**")
                        col_ic1, col_ic2, col_ic3 = st.columns(3)
                        col_ic1.metric("Original", f"{resultado['IC_original']:.4f}")
                        col_ic2.metric("César", f"{resultado['IC_cesar']:.4f}")
                        col_ic3.metric("Afín", f"{resultado['IC_afin']:.4f}")
                        st.info("El IC mide la probabilidad de coincidencia. En monoalfabéticos es igual en todos.")

                    with col_freq2:
                        st.write("**Distribución de Frecuencias:**")
                        freq_orig = {k: v for k, v in sorted(resultado["freq_original"].items(), key=lambda x: x[1], reverse=True)[:5]}
                        freq_cesar = {k: v for k, v in sorted(resultado["freq_cesar"].items(), key=lambda x: x[1], reverse=True)[:5]}
                        freq_afin = {k: v for k, v in sorted(resultado["freq_afin"].items(), key=lambda x: x[1], reverse=True)[:5]}

                        st.write("**Top 5 (Original):**")
                        st.bar_chart(freq_orig)
                        st.write("**Top 5 (César):**")
                        st.bar_chart(freq_cesar)
                        st.write("**Top 5 (Afín):**")
                        st.bar_chart(freq_afin)

                with tab3:
                    col_map1, col_map2 = st.columns(2)

                    with col_map1:
                        st.write("**Mapeo César:**")
                        mapa_texto = ""
                        for letra, cifrada in list(resultado["mapa_cesar"].items())[:13]:
                            mapa_texto += f"{letra}→{cifrada} "
                        st.code(mapa_texto + "\n...")

                    with col_map2:
                        st.write("**Mapeo Afín:**")
                        mapa_texto = ""
                        for letra, cifrada in list(resultado["mapa_afin"].items())[:13]:
                            mapa_texto += f"{letra}→{cifrada} "
                        st.code(mapa_texto + "\n...")

                with tab4:
                    st.write(resultado["analisis"])
                    st.warning("""
                    ⚠️ **Conclusión:**
                    Ambos son monoalfabéticos: preservan frecuencias.
                    Afín es más seguro que César, pero aún débil.
                    Vulnerables a análisis de frecuencias.
                    """)

# ======================== ✔ VALIDADOR ========================
elif opcion == "✔ Validador de Constante":
    st.header("✔ Validador de Constante de Decimación")
    st.markdown("Verifica si una constante `a` es válida para el Cifrado Afín.")

    col1, col2 = st.columns(2)

    with col1:
        a = st.number_input("Constante a:", min_value=0, max_value=100, value=7)
        n = st.number_input("Módulo n:", min_value=1, max_value=1000, value=26)

    with col2:
        if st.button("✔ Validar", key="btn_validar"):
            resultado = gcd_lib.validar_constante(a, n)

            tab1, tab2 = st.tabs(["Resultado", "Información"])

            with tab1:
                if "✔" in resultado:
                    st.success(resultado)
                else:
                    st.error(resultado)

            with tab2:
                st.markdown(f"""
                **Análisis de mcd({a}, {n}):**

                mcd = {gcd_lib.gcd(a, n)}

                **Explicación:**
                - Para que `a` sea válido en Cifrado Afín, debe cumplir: mcd(a, n) = 1
                - Si mcd(a, n) ≠ 1, no existe inverso multiplicativo
                - Sin inverso, no se puede descifrar correctamente
                - CCR = Conjunto Completo de Residuos
                """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    🔐 Motor Criptográfico Polialfabético | Herramienta Educativa |
    <a href='https://github.com'>GitHub</a>
</div>
""", unsafe_allow_html=True)
