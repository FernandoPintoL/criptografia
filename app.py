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
                        st.markdown("## 🔐 Cómo Funciona el Cifrado de Vigenère")

                        st.markdown("### Concepto Principal")
                        st.info("""
                        A diferencia de César (monoalfabético), Vigenère es **polialfabético**:
                        - Cada posición usa un desplazamiento DIFERENTE
                        - El desplazamiento es determinado por la clave
                        - La misma letra se cifra de múltiples formas según su posición
                        """)

                        st.markdown("### Fórmula Matemática del Cifrado")
                        st.latex(r"C_i = (M_i + K_i) \bmod 26")
                        st.write("Donde:")
                        st.write("- **C_i**: Letra cifrada en posición i")
                        st.write("- **M_i**: Letra original en posición i")
                        st.write("- **K_i**: Letra de la clave en posición i (repetida si es necesario)")
                        st.write("- **mod 26**: Módulo 26 (número de letras en alfabeto)")

                        st.markdown("### Fórmula Matemática del Descifrado")
                        st.latex(r"M_i = (C_i - K_i) \bmod 26")
                        st.write("Donde:")
                        st.write("- **M_i**: Letra original (recuperada)")
                        st.write("- **C_i**: Letra cifrada")
                        st.write("- **K_i**: Letra de la clave")

                        st.markdown("### Secuencia de Pasos Detallada")

                        col_seq1, col_seq2 = st.columns([1, 2])

                        with col_seq1:
                            st.markdown("""
                            **Paso 1:** Preparación

                            **Paso 2:** Extensión

                            **Paso 3:** Conversión

                            **Paso 4:** Cifrado

                            **Paso 5:** Verificación
                            """)

                        with col_seq2:
                            st.markdown("""
                            Convertir todo a mayúsculas, sin espacios

                            Repetir la clave para igualar longitud del texto

                            Convertir letras a números (A=0, B=1, ..., Z=25)

                            Aplicar: C = (M + K) mod 26 a cada letra

                            Convertir números cifrados de vuelta a letras
                            """)

                        st.markdown("### Ejemplo Visual Paso a Paso")

                        st.write("**Datos de entrada:**")
                        col_ej1, col_ej2, col_ej3 = st.columns(3)
                        with col_ej1:
                            st.write("Texto: HELLO")
                        with col_ej2:
                            st.write("Clave: SECRET")
                        with col_ej3:
                            st.write("Resultado: ?????")

                        st.write("**Proceso letra por letra:**")

                        ejemplos = [
                            ("H", "S", "H(7) + S(18) = 25 mod 26 = 25 → Z"),
                            ("E", "E", "E(4) + E(4) = 8 mod 26 = 8 → I"),
                            ("L", "C", "L(11) + C(2) = 13 mod 26 = 13 → N"),
                            ("L", "R", "L(11) + R(17) = 28 mod 26 = 2 → C"),
                            ("O", "E", "O(14) + E(4) = 18 mod 26 = 18 → S"),
                        ]

                        for original, clave_letra, calculo in ejemplos:
                            col_orig, col_clave, col_calc, col_cifrada = st.columns([1.5, 1.5, 4, 1])
                            with col_orig:
                                st.code(original)
                            with col_clave:
                                st.code(clave_letra)
                            with col_calc:
                                st.caption(calculo)
                            with col_cifrada:
                                st.code(calculo[-1])

                        st.success("**Resultado Final: ZINCSI**")

                        st.markdown("### Propiedades Criptográficas")
                        st.markdown("""
                        - **Polialfabético:** La misma letra se cifra de múltiples formas
                        - **Período:** Se repite cada N letras (N = longitud de clave)
                        - **Seguridad:** Más fuerte que César, pero vulnerable a Kasiski + Chi-Squared
                        - **Frecuencias:** Oculta el análisis de frecuencias de una sola letra
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
                        st.markdown("## 🔎 Método de Kasiski - Análisis Profundo")

                        st.markdown("### El Problema a Resolver")
                        st.info("""
                        Dado un criptograma de Vigenère:
                        - **Objetivo:** Encontrar la LONGITUD de la clave
                        - **Sin saber:** Cuál es la clave exacta
                        - **Herramienta:** Análisis estadístico de repeticiones
                        """)

                        st.markdown("### Principio Matemático Fundamental")

                        st.write("**Teorema de Kasiski:**")
                        st.latex(r"\text{Si } d(\text{repetición}_1, \text{repetición}_2) = k, \text{ entonces } k \equiv 0 \pmod{n}")
                        st.write("Donde:")
                        st.write("- **d:** distancia entre dos repeticiones del mismo patrón")
                        st.write("- **k:** la distancia calculada")
                        st.write("- **n:** longitud de la clave (lo que buscamos)")

                        st.write("**Explicación:**")
                        st.write("""
                        Si el mismo texto plano se cifra con las MISMAS letras de clave,
                        aparecerá el mismo criptograma. La distancia entre estas repeticiones
                        SIEMPRE será múltiplo de la longitud de clave.
                        """)

                        st.markdown("### Fórmula para Hallar la Longitud")
                        st.latex(r"n = \gcd(d_1, d_2, d_3, ..., d_m)")
                        st.write("Donde:")
                        st.write("- **n:** Longitud probable de la clave")
                        st.write("- **gcd:** Máximo Común Divisor")
                        st.write("- **d_i:** Distancias entre repeticiones encontradas")

                        st.markdown("### Secuencia de Pasos Detallada")

                        st.markdown("#### Paso 1: Limpieza del Texto")
                        st.write("Eliminar espacios, puntuación, convertir a mayúsculas")
                        st.write("**Ejemplo:**")
                        st.write("- Entrada: `The quick brown fox`")
                        st.write("- Salida: `THEQUICKBROWNFOX`")

                        st.markdown("#### Paso 2: Buscar Patrones Repetidos")
                        st.write("Buscar secuencias de n caracteres que aparezcan más de una vez")
                        st.latex(r"\text{Patrones encontrados: } \{(p_1, [pos_1, pos_2, ...]), (p_2, [...]), ...\}")
                        st.write("**Ejemplo (buscando patrones de 3 caracteres):**")
                        st.write("- Patrón `THE` aparece en posiciones [0, 15, 42]")
                        st.write("- Patrón `QUI` aparece en posiciones [3, 18]")
                        st.write("- Patrón `FOX` aparece en posiciones [10, 28]")

                        st.markdown("#### Paso 3: Calcular Distancias")
                        st.write("Para cada par de posiciones del mismo patrón, calcular la distancia")
                        st.latex(r"d_{i,j} = pos_j - pos_i")
                        st.write("**Ejemplo:**")
                        st.write("- `THE` en [0, 15, 42] → distancias: 15-0=15, 42-0=42, 42-15=27")
                        st.write("- `QUI` en [3, 18] → distancia: 18-3=15")
                        st.write("- `FOX` en [10, 28] → distancia: 28-10=18")
                        st.write("- **Todas las distancias:** [15, 42, 27, 15, 18]")

                        st.markdown("#### Paso 4: Hallar el MCD")
                        st.write("Calcular el Máximo Común Divisor de todas las distancias")
                        st.latex(r"\gcd(15, 42, 27, 15, 18) = ?")
                        st.write("**Factorización:**")
                        st.write("- 15 = 3 × 5")
                        st.write("- 42 = 2 × 3 × 7")
                        st.write("- 27 = 3³")
                        st.write("- 15 = 3 × 5")
                        st.write("- 18 = 2 × 3²")
                        st.write("- **MCD = 3** (el único factor común)")

                        st.markdown("#### Paso 5: Encontrar Divisores (Posibles Longitudes)")
                        st.write("Los divisores del MCD son posibles longitudes de clave")
                        st.write("**Si MCD = 3:**")
                        st.write("- Divisores: 1, 3")
                        st.write("- Descartamos 1 (sería Caesar)")
                        st.write("- **Conclusión: La clave probablemente tiene longitud 3**")

                        st.markdown("### Diagrama del Flujo Completo")
                        st.write("""
                        ```
                        CRIPTOGRAMA
                           ↓
                        [Paso 1] Limpiar
                           ↓
                        [Paso 2] Buscar repeticiones
                           ↓
                        [Paso 3] Calcular distancias
                           ↓
                        [Paso 4] Calcular MCD de distancias
                           ↓
                        [Paso 5] Encontrar divisores del MCD
                           ↓
                        LONGITUD PROBABLE DE CLAVE
                        ```
                        """)

                        st.markdown("### Ejemplo Matemático Completo")
                        st.write("**Entrada:** `LXFOPVEFRNHRABJKL` (pequeño criptograma)")
                        st.write("**Patrón buscado:** 3 caracteres")
                        st.write("**Patrón encontrado:** `FRN` en posiciones [8, 14]")
                        st.write("**Distancia:** 14 - 8 = 6")
                        st.write("**MCD de todas distancias:** 6")
                        st.write("**Divisores:** 1, 2, 3, 6")
                        st.write("**Conclusión:** Longitud probable: 2, 3 ó 6")

                        st.markdown("### Por Qué Funciona Este Método")
                        st.success("""
                        **Principio Fundamental:**

                        En Vigenère, si el texto plano tiene una repetición y esa repetición
                        se cifra con las MISMAS letras de clave, el criptograma también
                        tendrá una repetición. La distancia entre estas repeticiones siempre
                        será un MÚLTIPLO de la longitud de clave.

                        **Ejemplo:**
                        - Clave: KEYKEY... (longitud 3)
                        - Si "THE" aparece en posición 0 y 21 del texto original
                        - La repetición en el criptograma estará a distancia 21
                        - 21 es múltiplo de 3 (21 = 3 × 7)
                        """)

                        st.markdown("### Limitaciones y Consideraciones")
                        st.warning("""
                        - **Requiere texto largo:** Más texto = más repeticiones = más exactitud
                        - **Falsos positivos:** Coincidencias casuales pueden dar distancias incorrectas
                        - **Múltiples divisores:** Pueden haber varias posibles longitudes
                        - **Preferencia:** Probar primero números PRIMOS (menos divisores)
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
        modo_aleatorio = st.checkbox("🎲 Modo aleatorio", value=False)

    with col2:
        if st.button("🔤 Generar", key="btn_alfabeto"):
            try:
                resultado = alfabeto_lib.generar_alfabeto_mixto(clave, aleatorio=modo_aleatorio)

                tab1, tab2, tab3 = st.tabs(["Resultado", "Detalles", "Información"])

                with tab1:
                    st.success("✔ Alfabeto generado")

                    # Modo indicator
                    if resultado["modo"] == "aleatorio":
                        st.info("🎲 Modo ALEATORIO - El resto del alfabeto está mezclado al azar")
                    else:
                        st.info("📝 Modo NORMAL - El resto del alfabeto está en orden A-Z")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Clave Original:**")
                        st.code(resultado["clave_original"] if resultado["clave_original"] else "(vacía)", language=None)

                        st.write("**Clave Limpia:**")
                        st.code(resultado["clave_limpia"], language=None)

                    with col_b:
                        st.write("**Modo:**")
                        st.metric("Tipo de Generación", resultado["modo"].upper())

                        st.write("**Longitud:**")
                        st.metric("Caracteres", resultado["longitud"])

                    st.divider()
                    st.write("**Alfabeto Mixto Generado:**")
                    st.code(resultado["alfabeto_mixto"], language=None)

                    # Mapeo visual
                    st.write("**Mapeo de Sustitución (primeros 5 caracteres):**")
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
                    st.write("**Alfabeto Base:**")
                    st.code(resultado["alfabeto_base"], language=None)

                    st.write("**Estructura del Alfabeto Generado:**")
                    if resultado["clave_limpia"]:
                        st.write(f"1. **Clave limpia:** {resultado['clave_limpia']} ({len(resultado['clave_limpia'])} caracteres)")
                        st.write(f"2. **Resto del alfabeto:** {len(resultado['alfabeto_base']) - len(resultado['clave_limpia'])} caracteres")
                        if resultado["modo"] == "aleatorio":
                            st.write("   - Ordenamiento: ALEATORIO (cada ejecución es diferente)")
                        else:
                            st.write("   - Ordenamiento: NORMAL (en orden alfabético)")
                    else:
                        st.write("- Sin clave, el alfabeto completo se genera")
                        if resultado["modo"] == "aleatorio":
                            st.write("  en orden ALEATORIO (sustitución pura aleatoria)")
                        else:
                            st.write("  en orden NORMAL (A-Z)")

                    st.write("**Alfabeto Mixto Completo:**")
                    st.code(resultado["alfabeto_mixto"], language=None)

                with tab3:
                    st.markdown("""
                    **¿Cómo funciona?**

                    **Modo NORMAL (predecible):**
                    1. Se limpia la clave (mayúsculas, sin duplicados)
                    2. Se coloca la clave al inicio del alfabeto
                    3. Se agregan las letras restantes EN ORDEN A-Z

                    Ejemplo con clave "SECRETO":
                    - Original: ABCDEFGHIJKLMNOPQRSTUVWXYZ
                    - Mixto:    SECRTOABDFGHIJKLMNOPQUVWXYZ
                    - Uso: Educativo, fácil de entender

                    **Modo ALEATORIO (más seguro):**
                    1. Se limpia la clave (mayúsculas, sin duplicados)
                    2. Se coloca la clave al inicio del alfabeto
                    3. Se agregan las letras restantes MEZCLADAS ALEATORIAMENTE

                    Ejemplo con clave "SECRETO":
                    - Original: ABCDEFGHIJKLMNOPQRSTUVWXYZ
                    - Mixto:    SECRTOFGPWZBMJUQINLXVKHDYA  (aleatorio)
                    - Cada ejecución es diferente!
                    - Uso: Criptografía real, máxima seguridad

                    **Sin clave + Aleatorio (Sustitución Pura):**
                    - Genera un alfabeto completamente aleatorio
                    - Máxima seguridad
                    - No usa clave, es pura aleatoriedad

                    **Utilidad:**
                    - Educación: modo normal
                    - Cifrados de sustitución simple: modo normal
                    - Inicialización de matriz Playfair: modo aleatorio para seguridad
                    - Análisis criptográfico: ambos modos
                    - Investigación de fortaleza: modo aleatorio
                    """)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ======================== 5️⃣ CRIPTOANÁLISIS ========================
elif opcion == "5️⃣ Criptoanálisis (resolver a y b) 🔍":
    st.header("🔍 Criptoanálisis del Cifrado Afín por Ecuaciones")
    st.markdown("""
    Ataque matemático al Cifrado Afín utilizando dos correspondencias conocidas de plaintext-ciphertext.
    Si se conocen dos pares (M₁,C₁) y (M₂,C₂), es posible resolver el sistema de ecuaciones para
    encontrar los parámetros secretos **a** (multiplicador) y **b** (desplazamiento).
    """)

    st.info("💡 Seleccione un alfabeto e ingrese dos pares conocidos. El sistema resolverá automáticamente para hallar **a** y **b**")

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
                            st.markdown("## 📐 Explicación Conceptual")

                            st.markdown("""
                            ### El Problema a Resolver
                            Dado un criptograma de cifrado afín, se tiene:
                            - **Dos pares conocidos:** (M₁, C₁) y (M₂, C₂)
                            - **Dos incógnitas:** a (multiplicador) y b (desplazamiento)
                            - **Objetivo:** Encontrar los valores secretos de a y b
                            """)
                            st.info("💡 Esto es un ataque de **texto plano conocido** (Known Plaintext Attack)")

                            st.markdown("### Fórmula del Cifrado Afín (LaTeX)")
                            st.latex(r"C_i = (a \cdot M_i + b) \bmod n")
                            st.markdown("""
                            Donde:
                            - C_i: Letra cifrada en posición i
                            - M_i: Letra original en posición i
                            - a: Multiplicador (debe cumplir gcd(a,n) = 1)
                            - b: Desplazamiento aditivo
                            - n: Tamaño del alfabeto (módulo)
                            """)

                            st.markdown("### Secuencia de 4 Pasos - Resolver el Sistema")

                            col_paso1, col_paso2 = st.columns(2)

                            with col_paso1:
                                st.markdown("**Paso 1: Calcular Diferencias**")
                                st.markdown("""
                                ΔC = C₁ - C₂ (mod n)
                                ΔM = M₁ - M₂ (mod n)

                                Estas diferencias crean una nueva ecuación
                                sin la variable b.
                                """)

                            with col_paso2:
                                st.markdown("**Paso 2: Encontrar Inverso Modular**")
                                st.markdown("""
                                Calcular (ΔM)⁻¹ mod n

                                Este es el número que cumple:
                                (ΔM) × (ΔM)⁻¹ ≡ 1 (mod n)
                                """)

                            col_paso3, col_paso4 = st.columns(2)

                            with col_paso3:
                                st.markdown("**Paso 3: Resolver para 'a'**")
                                st.latex(r"a \equiv \Delta C \times (\Delta M)^{-1} \pmod{n}")
                                st.markdown("""
                                El multiplicador se obtiene
                                de la proporción entre diferencias.
                                """)

                            with col_paso4:
                                st.markdown("**Paso 4: Resolver para 'b'**")
                                st.latex(r"b \equiv C_1 - a \times M_1 \pmod{n}")
                                st.markdown("""
                                Una vez conocido 'a', se calcula 'b'
                                usando cualquiera de los pares.
                                """)

                            st.divider()

                            st.markdown("### Solución Encontrada - Detalles")

                            col_sol1, col_sol2 = st.columns(2)

                            with col_sol1:
                                st.markdown("**Parámetros Criptográficos:**")
                                st.markdown(f"""
                                - **a = {a}** (multiplicador)
                                - **b = {b}** (desplazamiento)
                                - **n = {n}** (módulo)
                                - **gcd(a, n) = 1** ✓ (válido)
                                """)

                            with col_sol2:
                                st.markdown("**Ecuación General:**")
                                st.latex(f"C = ({a} \\cdot M + {b}) \\bmod {n}")

                            st.markdown("### Cálculos Realizados (Paso a Paso)")

                            delta_c = (C1 - C2) % n
                            delta_m = (M1 - M2) % n

                            st.markdown(f"""
                            **Paso 1 - Diferencias:**
                            - ΔC = C₁ - C₂ = {C1} - {C2} = **{delta_c}** (mod {n})
                            - ΔM = M₁ - M₂ = {M1} - {M2} = **{delta_m}** (mod {n})

                            **Paso 2 - Inverso Modular:**
                            - Se busca (ΔM)⁻¹ tal que: {delta_m} × (ΔM)⁻¹ ≡ 1 (mod {n})
                            """)

                            st.markdown(f"""
                            **Paso 3 - Cálculo de 'a':**
                            - a ≡ ΔC × (ΔM)⁻¹ (mod {n})
                            - a ≡ {delta_c} × inverso (mod {n})
                            - **a = {a}** ✓

                            **Paso 4 - Cálculo de 'b':**
                            - b ≡ C₁ - a × M₁ (mod {n})
                            - b ≡ {C1} - {a} × {M1} (mod {n})
                            - b ≡ {C1} - {(a * M1) % n} (mod {n})
                            - **b = {b}** ✓
                            """)

                            st.markdown("### Por Qué Funciona Este Ataque")

                            st.success("""
                            **Principio Matemático:**

                            El cifrado afín es un sistema de ecuaciones lineales:
                            - C₁ = aM₁ + b (mod n)
                            - C₂ = aM₂ + b (mod n)

                            Con 2 ecuaciones y 2 incógnitas, el sistema es SIEMPRE RESOLUBLE
                            si gcd(M₁ - M₂, n) = 1.

                            Por eso es vulnerable a ataques de texto plano conocido:
                            si se conocen 2 pares plaintext-ciphertext, se rompe completamente.
                            """)

                            st.markdown("### Limitaciones y Consideraciones")

                            st.warning("""
                            ⚠️ **Debilidades del Cifrado Afín:**

                            1. **Vulnerable a KPA (Known Plaintext Attack):**
                               - Solo se necesitan 2 pares plaintext-ciphertext
                               - En idioma natural, esto es frecuente

                            2. **Espacio de claves pequeño:**
                               - Para alfabeto de 26 letras: solo φ(26) × 26 = 312 claves válidas
                               - Se puede romper por fuerza bruta fácilmente

                            3. **Vulnerable a análisis de frecuencias:**
                               - Es monoalfabético, preserva patrones
                               - Las letras más frecuentes siguen siendo frecuentes

                            4. **No proporciona confidencialidad moderna:**
                               - NO usar en aplicaciones reales de seguridad
                               - Solo para fines educativos
                            """)
                    else:
                        st.error(f"❌ {resultado.get('mensaje', 'Error desconocido')}")
                        st.warning("⚠️ No se pudo resolver el sistema. Verifique que las correspondencias sean válidas.")
                except Exception as e:
                    st.error(f"❌ Error al resolver: {str(e)}")
                    st.warning("⚠️ Ocurrió un error inesperado. Verifique los datos ingresados.")

# ======================== 6️⃣ COMPARADOR ========================
elif opcion == "6️⃣ Comparar César vs Afín 📊":
    st.header("📊 Comparador de Cifras Clásicas (César vs Afín)")
    st.markdown("""
    Compara dos métodos de cifrado clásico monoalfabético: César (simple) y Afín (más complejo).
    Observa cómo cambian las características criptográficas y la resistencia ante ataques.
    """)

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
                        st.markdown("## 📊 Análisis Detallado de Ambos Métodos")

                        st.markdown("### 1. Fórmula Matemática - Cifrado de César")
                        st.latex(r"C_i = (M_i + k) \bmod n")
                        st.markdown("""
                        Donde:
                        - C_i: Letra cifrada
                        - M_i: Letra original
                        - k: Desplazamiento (clave)
                        - n: Tamaño del alfabeto
                        """)

                        st.markdown("### 2. Fórmula Matemática - Cifrado Afín")
                        st.latex(r"C_i = (a \cdot M_i + b) \bmod n")
                        st.markdown("""
                        Donde:
                        - C_i: Letra cifrada
                        - M_i: Letra original
                        - a: Multiplicador (debe cumplir gcd(a,n) = 1)
                        - b: Desplazamiento
                        - n: Tamaño del alfabeto
                        """)

                        st.divider()

                        st.markdown("### 3. Características de Ambos Métodos")

                        col_carac1, col_carac2 = st.columns(2)

                        with col_carac1:
                            st.markdown("**Cifrado de César (k={}):**".format(k))
                            st.markdown(f"""
                            - **Tipo:** Monoalfabético simple
                            - **Claves posibles:** {len(alfabeto)} (muy débil)
                            - **Parámetros:** Solo 1 (k)
                            - **Proceso:** Desplazamiento puro
                            - **Vulnerabilidad:** Análisis de frecuencias
                            - **Fuerza bruta:** {len(alfabeto)} intentos
                            """)

                        with col_carac2:
                            st.markdown("**Cifrado Afín (a={}, b={}):**".format(a, b))
                            st.markdown(f"""
                            - **Tipo:** Monoalfabético general
                            - **Claves posibles:** ~312 (26 letras)
                            - **Parámetros:** Dos (a, b)
                            - **Proceso:** Transformación lineal
                            - **Vulnerabilidad:** Análisis de frecuencias
                            - **Fuerza bruta:** 312 intentos
                            """)

                        st.divider()

                        st.markdown("### 4. Comparativa de Propiedades Criptográficas")

                        comparativa_data = {
                            "Característica": [
                                "Tipo de cifrado",
                                "Número de claves",
                                "Análisis frecuencias",
                                "IC (Índice Coincidencia)",
                                "Patrón preservado",
                                "Seguridad actual",
                                "Vulnerabilidad principal",
                                "Ataque más rápido"
                            ],
                            "César": [
                                "Substitución simple",
                                f"{len(alfabeto)} (muy pocas)",
                                "Sí, se mantiene igual",
                                "Igual al original",
                                "Todos los patrones",
                                "Muy débil (histórico)",
                                "Fuerza bruta: 26 pasos",
                                "Fuerza bruta"
                            ],
                            "Afín": [
                                "Substitución lineal",
                                "~312 (aún pocas)",
                                "Sí, se mantiene igual",
                                "Igual al original",
                                "Todos los patrones",
                                "Muy débil (histórico)",
                                "Fuerza bruta: 312 pasos",
                                "Fuerza bruta o KPA"
                            ]
                        }

                        df_comparativa = st.dataframe(comparativa_data)

                        st.divider()

                        st.markdown("### 5. Secuencia de Cifrado - Paso a Paso")

                        col_seq1, col_seq2 = st.columns(2)

                        with col_seq1:
                            st.markdown("**César:**")
                            st.markdown(f"""
                            1. Tomar letra original: M
                            2. Obtener valor: pos = índice(M)
                            3. Sumar desplazamiento: pos + {k}
                            4. Aplicar módulo: (pos + {k}) mod {len(alfabeto)}
                            5. Convertir a letra: C = alfabeto[resultado]

                            **Ejemplo:** H → (7 + {k}) mod 26 = {(7 + k) % len(alfabeto)} → alfabeto[{(7 + k) % len(alfabeto)}]
                            """)

                        with col_seq2:
                            st.markdown("**Afín:**")
                            st.markdown(f"""
                            1. Tomar letra original: M
                            2. Obtener valor: pos = índice(M)
                            3. Multiplicar: {a} × pos
                            4. Sumar desplazamiento: ({a} × pos) + {b}
                            5. Aplicar módulo: ({a} × pos + {b}) mod {len(alfabeto)}
                            6. Convertir a letra: C = alfabeto[resultado]

                            **Ejemplo:** H → ({a} × 7 + {b}) mod 26 = {(a * 7 + b) % len(alfabeto)} → alfabeto[{(a * 7 + b) % len(alfabeto)}]
                            """)

                        st.divider()

                        st.markdown("### 6. Por Qué Se Preserva el IC (Índice de Coincidencia)")

                        st.info("""
                        **Propiedad de Biyección:**

                        Tanto César como Afín son transformaciones BIYECTIVAS (1:1).
                        Esto significa:
                        - Cada letra original → exactamente una letra cifrada
                        - Cada letra cifrada ← exactamente una letra original

                        Por lo tanto:
                        - La frecuencia relativa de cada letra se preserva
                        - Si E aparecía 12 veces en el original
                        - Su cifrada (por ejemplo X) aparecerá 12 veces en el criptograma

                        El IC (Índice de Coincidencia) depende SOLO de las frecuencias,
                        no de la transformación. Por eso es IGUAL en ambos casos.
                        """)

                        st.divider()

                        st.markdown("### 7. Vulnerabilidades - Análisis de Frecuencias")

                        col_vuln1, col_vuln2 = st.columns(2)

                        with col_vuln1:
                            st.markdown("**Cómo se rompe César:**")
                            st.markdown("""
                            1. Calcular frecuencias del criptograma
                            2. Asumir que la más frecuente es E
                            3. Calcular desplazamiento: k = pos(cif_E) - pos(E)
                            4. Probar con fuerza bruta los 26 valores
                            5. Seleccionar el que genera texto sensato

                            **Tiempo:** Milisegundos
                            """)

                        with col_vuln2:
                            st.markdown("**Cómo se rompe Afín:**")
                            st.markdown("""
                            1. Opción A - Fuerza bruta: Probar 312 pares (a,b)
                            2. Opción B - Análisis avanzado:
                               - Identificar las 2 letras más frecuentes
                               - Asumir qué letras del original son
                               - Resolver sistema de ecuaciones
                               - Obtener a y b directamente
                            3. Verificar resultado

                            **Tiempo:** Segundos a milisegundos
                            """)

                        st.divider()

                        st.success("""
                        ### ✅ Conclusión

                        **Similitudes:**
                        - Ambos son monoalfabéticos
                        - Ambos preservan IC y frecuencias
                        - Ambos vulnerables a análisis de frecuencias
                        - Ambos débiles ante ataques modernos

                        **Diferencias:**
                        - Afín tiene 12× más claves posibles (~312 vs 26)
                        - Afín requiere verificar gcd(a,n) = 1
                        - Afín es más complejo pero NO más seguro en práctica

                        **Lección de Seguridad:**
                        Aumentar la complejidad matemática no garantiza seguridad.
                        El verdadero problema es que ambos son monoalfabéticos.
                        La solución es usar cifrados POLIALFABÉTICOS (como Vigenère)
                        o métodos modernos (como AES).
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
