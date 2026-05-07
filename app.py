import streamlit as st
import gcd_lib
import alfabeto_lib
import vigenere_lib
import kasiski_lib
import vigenere_breaker_v3
import plotly.graph_objects as go
from cripto_analisis_comparador.criptoanalisis import criptoanalisis, resolver_afin
from cripto_analisis_comparador.comparador import comparar_cifrados
from cripto_analisis_comparador.alfabetos import obtener_alfabeto, mostrar_menu_alfabetos

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
        "1️⃣ Calcular MCD",
        "2️⃣ Verificar si son coprimos",
        "3️⃣ Validar constante (cripto)",
        "4️⃣ Generar alfabeto mixto 🔤",
        "5️⃣ Criptoanálisis (resolver a y b) 🔍",
        "6️⃣ Comparar César vs Afín 📊",
        "7️⃣ Vigenère (polialfabético) 🔐",
        "8️⃣ Método de Kasiski 🔎",
        "9️⃣ Romper Vigenère",
        "0️⃣ Salir"
    ]
)

# ======================== 🏠 INICIO ========================
if opcion == "🏠 Inicio":
    st.header("Bienvenido al Motor Criptográfico")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Módulos Disponibles")
        st.markdown("""
1️⃣ **Calcular MCD** - Máximo Común Divisor (Algoritmo de Euclides)

2️⃣ **Verificar si son coprimos** - Validar números coprimos

3️⃣ **Validar constante (cripto)** - Verifica parámetros criptográficos

4️⃣ **Generar alfabeto mixto** 🔤 - Generador de alfabetos personalizados

5️⃣ **Criptoanálisis (resolver a y b)** 🔍 - Ataque por ecuaciones simultáneas

6️⃣ **Comparar César vs Afín** 📊 - Análisis comparativo de cifrados

7️⃣ **Vigenère (polialfabético)** 🔐 - Cifrador polialfabético con análisis detallado

8️⃣ **Método de Kasiski** 🔎 - Detecta la longitud probable de clave

9️⃣ **Romper Vigenère** - Descifra automáticamente con Chi-Squared
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
    1. Comienza con 6️⃣ **Comparador** para entender César vs Afín
    2. Explora 7️⃣ **Vigenère** para cifrar/descifrar
    3. Usa 8️⃣ **Kasiski** para encontrar la longitud de clave

    **Para ataques criptoanalíticos:**
    1. 8️⃣ **Kasiski** → Encuentra longitud de clave
    2. 9️⃣ **Romper Vigenère** → Encuentra la clave exacta
    3. Verifica que el descifrado tenga sentido

    **Para avanzados:**
    1. Intenta 5️⃣ **Criptoanálisis** con ecuaciones
    2. Experimenta con 4️⃣ **Alfabetos Mixtos**
    3. Valida constantes con 3️⃣ el **Validador**
    """)

# ======================== 1️⃣ CALCULAR MCD ========================
elif opcion == "1️⃣ Calcular MCD":
    st.header("1️⃣ Calcular MCD")
    st.markdown("Calcula el Máximo Común Divisor de dos números usando el algoritmo de Euclides.")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Número a:", min_value=0, value=48)
    with col2:
        b = st.number_input("Número b:", min_value=0, value=18)

    if st.button("🔢 Calcular MCD", key="btn_mcd"):
        resultado = gcd_lib.gcd(a, b)
        st.success(f"✔ MCD({a}, {b}) = **{resultado}**")

# ======================== 2️⃣ VERIFICAR COPRIMOS ========================
elif opcion == "2️⃣ Verificar si son coprimos":
    st.header("2️⃣ Verificar si son coprimos")
    st.markdown("Dos números son coprimos si su MCD es 1 (no comparten factores comunes).")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Número a:", min_value=1, value=7)
    with col2:
        b = st.number_input("Número b:", min_value=1, value=26)

    if st.button("✔ Verificar Coprimos", key="btn_coprimos"):
        mcd_valor = gcd_lib.gcd(a, b)
        if mcd_valor == 1:
            st.success(f"✔ **{a} y {b} son coprimos** (MCD = 1)")
            st.info("Esto significa que pueden usarse en el Cifrado Afín")
        else:
            st.error(f"❌ **{a} y {b} NO son coprimos** (MCD = {mcd_valor})")
            st.warning(f"Comparten factores comunes. No son válidos para Cifrado Afín")

# ======================== 7️⃣ VIGENÈRE ========================
elif opcion == "7️⃣ Vigenère (polialfabético) 🔐":
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

                    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Resultados", "Proceso Simple", "Proceso Detallado", "Análisis", "Información"])

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
                        st.write("**Proceso Paso a Paso (Forma Simple):**")
                        st.code(resultado["proceso"], language=None)

                    with tab3:
                        st.write("**Proceso Paso a Paso (Valores Numéricos):**")
                        proceso_detallado = vigenere_lib.mostrar_proceso_detallado(texto, clave)
                        st.code(proceso_detallado, language=None)

                    with tab4:
                        st.write("**Análisis Polialfabético:**")
                        st.code(resultado["analisis"], language=None)
                        st.info("🔍 Observe cómo cada letra se cifra de múltiples formas según su posición.")

                    with tab5:
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
elif opcion == "8️⃣ Método de Kasiski 🔎":
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

                    tab1, tab2, tab3, tab4 = st.tabs(["Resultados", "Pasos Detallados", "Detalles Técnicos", "Información"])

                    with tab1:
                        st.write(kasiski_lib.resumen_kasiski(criptograma, n))

                    with tab2:
                        st.subheader("📋 Proceso Paso a Paso")

                        st.markdown("### Paso 1️⃣: Limpieza del Texto")
                        col_clean1, col_clean2 = st.columns(2)
                        with col_clean1:
                            st.write("**Texto Original:**")
                            st.code(resultado["texto_original"][:200] + ("..." if len(resultado["texto_original"]) > 200 else ""), language=None)
                        with col_clean2:
                            st.write("**Texto Limpio:**")
                            st.code(resultado["texto_limpio"][:200] + ("..." if len(resultado["texto_limpio"]) > 200 else ""), language=None)
                        st.info(f"✔ Longitud original: {len(resultado['texto_original'])} caracteres → Longitud limpia: {len(resultado['texto_limpio'])} caracteres")

                        st.markdown("### Paso 2️⃣: Búsqueda de Repeticiones")
                        if resultado["repeticiones"]:
                            st.write(f"**Se encontraron {len(resultado['repeticiones'])} patrones diferentes repetidos:**")
                            for patron, posiciones in list(resultado["repeticiones"].items())[:15]:
                                st.write(f"- `{patron}` aparece en {len(posiciones)} ocasiones")
                                st.caption(f"  Posiciones: {posiciones}")
                            if len(resultado["repeticiones"]) > 15:
                                st.info(f"... y {len(resultado['repeticiones']) - 15} patrones más")
                        else:
                            st.warning("⚠️ No se encontraron repeticiones")

                        st.markdown("### Paso 3️⃣: Cálculo de Distancias")
                        if resultado["distancias"]:
                            st.write(f"**Total de distancias calculadas: {len(resultado['distancias'])}**")
                            st.write("Primeras 20 distancias:")
                            st.code(str(resultado["distancias"][:20]), language=None)
                            if len(resultado["distancias"]) > 20:
                                st.caption(f"... {len(resultado['distancias']) - 20} distancias más")
                        else:
                            st.warning("⚠️ No se calcularon distancias")

                        st.markdown("### Paso 4️⃣: Cálculo del MCD")
                        if resultado["mcd"]:
                            st.metric("MCD (Máximo Común Divisor)", resultado["mcd"])
                            st.info(f"El MCD estimado es **{resultado['mcd']}** - Este es el candidato más probable para la longitud de la clave")
                        else:
                            st.warning("⚠️ No se pudo calcular el MCD")

                        st.markdown("### Paso 5️⃣: Posibles Longitudes de Clave")
                        if resultado["posibles_claves"]:
                            st.success(f"**Longitudes de clave probables: {resultado['posibles_claves']}**")
                            st.write(f"Estos son los divisores del MCD {resultado['mcd']} (excepto 1)")
                        else:
                            st.warning("⚠️ No se encontraron posibles longitudes")

                    with tab3:
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

                    with tab4:
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

# ======================== 🔓 ROMPER VIGENÈRE ========================
elif opcion == "9️⃣ Romper Vigenère":
    st.header("🔓 Romper Cifrado Vigenère")
    st.markdown("Descifra Vigenère automáticamente conociendo la longitud de la clave. Utiliza análisis estadístico (Chi-Squared Test).")

    col1, col2 = st.columns(2)

    with col1:
        criptograma = st.text_area("Criptograma (texto cifrado):", placeholder="Pegue el texto cifrado aquí", height=120)

    with col2:
        longitud_clave = st.number_input("Longitud de clave (encontrada con Kasiski):", min_value=1, max_value=20, value=7)

        if st.button("🔓 Descifrar", key="btn_romper_vigenere"):
            if not criptograma:
                st.error("❌ Por favor ingrese un criptograma")
            else:
                try:
                    with st.spinner("⏳ Analizando con Chi-Squared Test..."):
                        resultado = vigenere_breaker_v3.romper_vigenere_v3(criptograma, longitud_clave)

                    st.success("✔ Descifrado completado")

                    tab1, tab2, tab3, tab4 = st.tabs(["Resultado", "Pasos Detallados", "Análisis Técnico", "Información"])

                    with tab1:
                        col_res1, col_res2 = st.columns(2)
                        with col_res1:
                            st.write("**Clave encontrada:**")
                            st.code(resultado["clave"], language=None)
                        with col_res2:
                            st.write("**Score (Chi²):**")
                            st.metric("Chi² Score", f"{resultado['chi2_score']:.2f}")

                        st.write("**Texto descifrado (primeros 300 caracteres):**")
                        st.code(resultado["descifrado"][:300] + ("..." if len(resultado["descifrado"]) > 300 else ""), language=None)

                        with st.expander("📖 Ver texto descifrado completo"):
                            st.code(resultado["descifrado"], language=None)

                    with tab2:
                        st.subheader("📋 Proceso Paso a Paso")

                        st.markdown("### Paso 1️⃣: Limpieza del Texto")
                        st.info(f"✔ Texto limpio (sin espacios ni caracteres especiales)")
                        st.caption(f"Longitud original: {len(criptograma)} → Longitud limpia: {len(resultado['criptograma_limpio'])} caracteres")
                        st.code(resultado['criptograma_limpio'][:150] + ("..." if len(resultado['criptograma_limpio']) > 150 else ""), language=None)

                        st.markdown("### Paso 2️⃣: División en Columnas")
                        st.info(f"✔ Criptograma dividido en {resultado['longitud_clave']} columnas")
                        st.caption(f"Cada columna fue cifrada con una letra diferente de la clave")

                        col_div1, col_div2 = st.columns(2)
                        with col_div1:
                            st.write(f"**Número de columnas:** {len(resultado['columnas'])}")
                            for i, col in enumerate(resultado['columnas'][:3]):
                                st.write(f"- Columna {i}: {len(col)} caracteres")
                        with col_div2:
                            st.write(f"**Primeros caracteres de cada columna:**")
                            for i, col in enumerate(resultado['columnas']):
                                st.code(col[:15] + ("..." if len(col) > 15 else ""), language=None)

                        st.markdown("### Paso 3️⃣: Análisis de Cada Columna (Chi-Squared Test)")
                        st.info(f"✔ Para cada columna se probaron 26 desplazamientos posibles")

                        for analisis in resultado['analisis_columnas']:
                            col_analisis1, col_analisis2, col_analisis3, col_analisis4 = st.columns(4)

                            with col_analisis1:
                                st.metric(f"Columna {analisis['numero']}", f"{analisis['longitud']} car.")
                            with col_analisis2:
                                st.metric("Desplazamiento", analisis['desplazamiento'])
                            with col_analisis3:
                                st.metric("Letra Clave", analisis['letra_clave'])
                            with col_analisis4:
                                st.metric("Chi² Score", f"{analisis['chi2']:.2f}")

                            st.caption(f"Muestra: {analisis['muestra']}")

                        st.markdown("### Paso 4️⃣: Reconstrucción de la Clave")
                        st.success(f"**Clave encontrada: {resultado['clave']}**")
                        st.write(f"Chi² Total (suma de todos): **{resultado['chi2_score']:.2f}**")
                        st.caption("Menor valor = mejor ajuste a frecuencias de inglés")

                        st.markdown("### Paso 5️⃣: Descifrado Final")
                        st.info(f"✔ Criptograma descifrado usando la clave encontrada")
                        st.code(resultado['descifrado'][:200] + ("..." if len(resultado['descifrado']) > 200 else ""), language=None)

                    with tab3:
                        st.write("**Método:** Chi-Squared Test")
                        st.write("**¿Cómo funciona?**")
                        st.markdown("""
                        1. Divide el criptograma en columnas según la longitud de clave
                        2. Para cada columna, prueba los 26 desplazamientos posibles
                        3. Calcula chi-squared entre frecuencias observadas y esperadas en inglés
                        4. Selecciona el desplazamiento con el chi-squared más bajo (mejor coincidencia)
                        5. Reconstruye la clave completa

                        **Ventajas:**
                        - Rápido incluso para claves largas (hasta 10+ caracteres)
                        - Basado en análisis estadístico matemático
                        - Preciso para textos en inglés
                        """)

                        st.info("💡 **Flujo recomendado:**\n1. Use Kasiski para encontrar la longitud\n2. Use esta herramienta para encontrar la clave\n3. Verifique que el descifrado tenga sentido")

                    with tab4:
                        st.markdown("""
                        **¿Cuándo usar esta herramienta?**
                        - Cuando ya conoces la longitud de la clave (por Kasiski)
                        - Cuando tienes un criptograma de Vigenère
                        - Para textos en inglés o español

                        **Limitaciones:**
                        - Funciona mejor con textos largos (>200 caracteres)
                        - Requiere que el texto sea realmente en inglés
                        - No funciona bien con textos muy cortos
                        """)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ======================== 4️⃣ ALFABETO MIXTO ========================
elif opcion == "4️⃣ Generar alfabeto mixto 🔤":
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

# ======================== 5️⃣ CRIPTOANÁLISIS ========================
elif opcion == "5️⃣ Criptoanálisis (resolver a y b) 🔍":
    st.header("🔍 Criptoanálisis por Ecuaciones")
    st.markdown("Ataque al Cifrado Afín mediante dos correspondencias conocidas: C₁=aM₁+b y C₂=aM₂+b")

    st.info("💡 Seleccione un alfabeto e ingrese dos pares (letra) y el sistema resolverá para hallar `a` y `b`")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Seleccionar Alfabeto:**")

        opciones_alfabeto = {
            "1": "Alfabeto estándar (A-Z)",
            "2": "Español",
            "3": "Español extendido",
            "4": "Números",
            "5": "Alfanumérico"
        }

        opcion_sel = st.selectbox("Tipo de alfabeto:", list(opciones_alfabeto.values()))
        clave_opcion = [k for k, v in opciones_alfabeto.items() if v == opcion_sel][0]
        alfabeto = obtener_alfabeto(clave_opcion)

        if alfabeto:
            n = len(alfabeto)
            st.success(f"✔ Alfabeto seleccionado (n={n})")
            st.write(f"Alfabeto: {alfabeto}")

    with col2:
        if alfabeto:
            st.write("**Ingrese dos pares de correspondencia:**")

            col_m1, col_c1 = st.columns(2)
            with col_m1:
                M1_letra = st.selectbox("M₁ (plaintext 1):", list(alfabeto), key="M1")
                M1 = alfabeto.index(M1_letra)
            with col_c1:
                C1_letra = st.selectbox("C₁ (criptograma 1):", list(alfabeto), key="C1")
                C1 = alfabeto.index(C1_letra)

            col_m2, col_c2 = st.columns(2)
            with col_m2:
                M2_letra = st.selectbox("M₂ (plaintext 2):", list(alfabeto), key="M2")
                M2 = alfabeto.index(M2_letra)
            with col_c2:
                C2_letra = st.selectbox("C₂ (criptograma 2):", list(alfabeto), key="C2")
                C2 = alfabeto.index(C2_letra)

            if st.button("🔍 Resolver", key="btn_crypto"):
                try:
                    resultado = resolver_afin(M1, C1, M2, C2, n)

                    if resultado.get("exito", False):
                        st.success("✔ Sistema resuelto")

                        a = resultado["a"]
                        b = resultado["b"]

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
                        st.error(f"❌ {resultado.get('mensaje', 'Error desconocido')}")
                        st.warning("⚠️ No se pudo resolver el sistema. Verifique que las correspondencias sean válidas.")
                except Exception as e:
                    st.error(f"❌ Error al resolver: {str(e)}")
                    st.warning("⚠️ Ocurrió un error inesperado. Verifique los datos ingresados.")

# ======================== 6️⃣ COMPARADOR ========================
elif opcion == "6️⃣ Comparar César vs Afín 📊":
    st.header("📊 Comparador de Cifras Clásicas")
    st.markdown("Cifra el mismo mensaje con César y Afín para observar cómo cambia la distribución.")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Seleccionar Alfabeto:**")

        opciones_alfabeto = {
            "1": "Alfabeto estándar (A-Z)",
            "2": "Español",
            "3": "Español extendido",
            "4": "Números",
            "5": "Alfanumérico"
        }

        opcion_sel = st.selectbox("Tipo de alfabeto:", list(opciones_alfabeto.values()), key="comp_alfabeto")
        clave_opcion = [k for k, v in opciones_alfabeto.items() if v == opcion_sel][0]
        alfabeto = obtener_alfabeto(clave_opcion)

        if alfabeto:
            st.success(f"✔ Alfabeto seleccionado (n={len(alfabeto)})")

        texto = st.text_area("Texto a cifrar:", placeholder="Ingrese el texto", height=80)

    with col2:
        if alfabeto:
            k = st.number_input("k (desplazamiento César):", min_value=1, max_value=len(alfabeto)-1, value=3)
            a = st.number_input("a (multiplicador Afín):", min_value=1, max_value=len(alfabeto)-1, value=5)
            b = st.number_input("b (desplazamiento Afín):", min_value=0, max_value=len(alfabeto)-1, value=8)

            if st.button("📊 Comparar", key="btn_comparar"):
                try:
                    resultado = comparar_cifrados(texto, k, a, b, alfabeto)

                    st.success("✔ Análisis completado")

                    tab1, tab2, tab3, tab4 = st.tabs(["Resultados", "Índice de Coincidencia", "Frecuencias", "Análisis"])

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
                        st.write("**IC (Índice de Coincidencia):**")
                        col_ic1, col_ic2, col_ic3 = st.columns(3)
                        col_ic1.metric("Original", f"{resultado['indice_coincidencia']['original']:.4f}")
                        col_ic2.metric("César", f"{resultado['indice_coincidencia']['cesar']:.4f}")
                        col_ic3.metric("Afín", f"{resultado['indice_coincidencia']['afin']:.4f}")
                        st.info("El IC mide la probabilidad de coincidencia. En monoalfabéticos es igual en todos.")

                    with tab3:
                        st.write("**Distribución de Frecuencias:**")
                        freq_orig = {k: v for k, v in sorted(resultado["frecuencias"]["original"].items(), key=lambda x: x[1], reverse=True)[:5]}
                        freq_cesar = {k: v for k, v in sorted(resultado["frecuencias"]["cesar"].items(), key=lambda x: x[1], reverse=True)[:5]}
                        freq_afin = {k: v for k, v in sorted(resultado["frecuencias"]["afin"].items(), key=lambda x: x[1], reverse=True)[:5]}

                        col_f1, col_f2, col_f3 = st.columns(3)
                        with col_f1:
                            st.write("**Top 5 (Original):**")
                            st.bar_chart(freq_orig)
                        with col_f2:
                            st.write("**Top 5 (César):**")
                            st.bar_chart(freq_cesar)
                        with col_f3:
                            st.write("**Top 5 (Afín):**")
                            st.bar_chart(freq_afin)

                    with tab4:
                        st.markdown("""
                        **Análisis:**
                        Ambos son monoalfabéticos: preservan frecuencias.

                        - Afín es más seguro que César, pero aún débil
                        - La distribución de frecuencias no cambia
                        - Vulnerables a análisis de frecuencias
                        - El Índice de Coincidencia debe ser similar en ambos
                        """)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ======================== 3️⃣ VALIDADOR ========================
elif opcion == "3️⃣ Validar constante (cripto)":
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

# ======================== 0️⃣ SALIR ========================
elif opcion == "0️⃣ Salir":
    st.info("👋 ¡Hasta luego!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    🔐 Motor Criptográfico Polialfabético | Herramienta Educativa |
    <a href='https://github.com'>GitHub</a>
</div>
""", unsafe_allow_html=True)
