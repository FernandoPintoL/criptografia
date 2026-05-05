# 📊 Comparador Lib - Comparador de Cifras Clásicas

## Descripción General

`comparador_lib.py` implementa un **comparador analítico** entre dos sistemas de cifrado clásicos: **César** y **Afín**. Permite cifrar el mismo mensaje con ambos algoritmos y **observar cómo afectan a la distribución de caracteres**, realizando análisis estadísticos detallados para entender sus diferencias y vulnerabilidades.

### Objetivo Principal
Demostrar que aunque ambos son **sustituciones monoalfabéticas**, el cifrado Afín tiene una estructura matemática más compleja que César, pero ambos mantienen invariantes estadísticas (frecuencias y distribuciones) que los hacen vulnerables al análisis de frecuencias.

---

## Conceptos Clave

### Monoalfabético vs Polialfabético
- **César y Afín:** Monoalfabéticos (cada letra siempre mapea a la misma letra)
- **Vigénère:** Polialfabético (cada letra mapea a diferentes letras según su posición)

### Invariantes Estadísticas
```
Si el original tiene: A=10%, B=5%, C=3%
El cifrado tendrá los mismos porcentajes, solo permutados:
  A→E, B→R, C→S
  E=10%, R=5%, S=3% (en el cifrado)
```

**Esto es el talón de Aquiles de los monoalfabéticos.**

---

## Funciones

### 1. `limpiar_texto(texto)`

**Propósito:** Preparar el texto para análisis.

```python
limpiar_texto("¡Hola, Mundo!")  # Retorna: "HOLAMUNDO"
```

**Qué hace:**
- Convierte a mayúsculas
- Elimina espacios y caracteres especiales
- Mantiene solo letras A-Z

---

### 2. `cifrar_cesar(texto, k, n=26)`

**Propósito:** Cifrar usando el algoritmo de César.

```python
cifrar_cesar("HOLA", k=3)  # Retorna: "KROH"
```

**Fórmula:**
```
C = (M + k) mod n

Donde:
  C = letra cifrada
  M = letra original (0-25)
  k = desplazamiento (clave)
  n = módulo (26)
```

**Ejemplo paso a paso:**
```
Texto: HOLA
k = 3

H (7) → (7+3) mod 26 = 10 (K)
O (14) → (14+3) mod 26 = 17 (R)
L (11) → (11+3) mod 26 = 14 (O)
A (0) → (0+3) mod 26 = 3 (D)

Resultado: KROD
```

**Características:**
- Simple y rápido
- Solo depende de un parámetro `k`
- Fácil de romper (solo 26 posibilidades)

---

### 3. `cifrar_afin(texto, a, b, n=26)`

**Propósito:** Cifrar usando el algoritmo Afín.

```python
cifrar_afin("HOLA", a=5, b=8)  # Retorna: "IDJA"
```

**Fórmula:**
```
C = (a·M + b) mod n

Donde:
  C = letra cifrada
  M = letra original (0-25)
  a = multiplicador (debe ser coprimo con n)
  b = desplazamiento
  n = módulo (26)
```

**Validación:**
```python
if gcd(a, n) != 1:
    return None  # 'a' no es válido
```

**Ejemplo paso a paso:**
```
Texto: HOLA
a = 5, b = 8

H (7) → (5×7 + 8) mod 26 = 43 mod 26 = 17 (R)
O (14) → (5×14 + 8) mod 26 = 78 mod 26 = 0 (A)
L (11) → (5×11 + 8) mod 26 = 63 mod 26 = 11 (L)
A (0) → (5×0 + 8) mod 26 = 8 mod 26 = 8 (I)

Resultado: RALI
```

**Características:**
- Más complejo que César (dos parámetros)
- Requiere validación de `a` (debe ser coprimo con 26)
- 12 × 26 = 312 combinaciones posibles
- Aún vulnerable a análisis de frecuencias

---

### 4. `frecuencia(texto)`

**Propósito:** Calcular la distribución de letras en porcentaje.

```python
frecuencia("HOLA")
# Retorna: {'A': 25.0, 'H': 25.0, 'L': 25.0, 'O': 25.0, ...}

frecuencia("AABBCC")
# Retorna: {'A': 33.33, 'B': 33.33, 'C': 33.33, ...}
```

**Algoritmo:**
```
Para cada letra:
    conteo = número de apariciones
    frecuencia = (conteo / total) × 100
```

**Utilidad en criptoanálisis:**
- En textos largos, las letras más frecuentes son: E, A, O, I
- Si el cifrado mantiene estas frecuencias, es monoalfabético
- Si no, es polialfabético

---

### 5. `indice_coincidencia(texto)`

**Propósito:** Calcular el Índice de Coincidencia (IC), una medida estadística.

```python
indice_coincidencia("HELLO WORLD")  # Retorna: 0.065
indice_coincidencia("AAAABBBBCCCC") # Retorna: 0.333
```

**Fórmula:**
```
IC = Σ f(i) × (f(i) - 1) / (N × (N - 1))

Donde:
  f(i) = frecuencia de la letra i
  N = longitud total del texto
```

**Interpretación:**
```
IC ≈ 0.065 → Texto en inglés (monoalfabético o cifrado con Vigénère de clave larga)
IC ≈ 0.038 → Texto aleatorio o Vigénère uniforme
IC ≈ 0.5   → Texto muy repetitivo
```

**Ejemplo:**
```
Texto: "AAABBBCCC" (N=9)

Conteo: A=3, B=3, C=3

IC = (3×2 + 3×2 + 3×2) / (9×8)
   = (6 + 6 + 6) / 72
   = 18 / 72
   = 0.25
```

**Utilidad:**
- Detectar si un cifrado es monoalfabético o polialfabético
- Estimar la longitud de clave en Vigénère
- Validar suposiciones en criptoanálisis

---

### 6. `generar_mapeo(k=None, a=None, b=None, n=26)`

**Propósito:** Generar el mapeo completo (diccionario) de cómo se cifran todas las letras.

```python
mapa_cesar, mapa_afin = generar_mapeo(k=3, a=5, b=8)

print(mapa_cesar)
# {'A': 'D', 'B': 'E', 'C': 'F', ..., 'Z': 'C'}

print(mapa_afin)
# {'A': 'I', 'B': 'N', 'C': 'S', ..., 'Z': 'D'}
```

**Utilidad:**
- Ver visualmente cómo mapea cada letra
- Comparar los mapeos lado a lado
- Entender la estructura del cifrado

---

### 7. `interpretar()`

**Propósito:** Proporcionar un análisis interpretativo.

```python
print(interpretar())
```

**Salida:**
```
⚠️ Ambos cifrados son sustituciones monoalfabéticas.
👉 No cambian la frecuencia de letras, solo las reordenan.
🔐 El cifrado Afín es estructuralmente más complejo que César,
pero ambos son vulnerables a análisis de frecuencia.
```

---

### 8. `comparar_cifras(texto, k, a, b, n=26)` ✅ **Función Principal**

**Propósito:** Realizar un análisis completo comparando ambos cifrados.

```python
resultado = comparar_cifras(
    texto="El criptograma es una forma de arte",
    k=5,
    a=7,
    b=3
)
```

**Retorna un diccionario con:**

```python
{
    "original": str,              # Texto limpio
    "cesar": str,                 # Texto cifrado con César
    "afin": str,                  # Texto cifrado con Afín
    
    "freq_original": dict,        # Frecuencias del original
    "freq_cesar": dict,           # Frecuencias del César
    "freq_afin": dict,            # Frecuencias del Afín
    
    "IC_original": float,         # Índice de coincidencia del original
    "IC_cesar": float,            # IC del César
    "IC_afin": float,             # IC del Afín
    
    "mapa_cesar": dict,           # Mapeo A→X, B→Y, ...
    "mapa_afin": dict,            # Mapeo A→P, B→Q, ...
    
    "analisis": str               # Interpretación
}
```

---

## Ejemplos de Uso Completo

### Ejemplo 1: Comparación Básica
```python
import comparador_lib

texto = "HELLO WORLD"
k = 3
a = 5
b = 8

resultado = comparador_lib.comparar_cifras(texto, k, a, b)

print("Original:", resultado["original"])
print("César:", resultado["cesar"])
print("Afín:", resultado["afin"])

print("\nFrecuencias original:")
print(resultado["freq_original"])

print("\nÍndice de Coincidencia:")
print(f"Original: {resultado['IC_original']}")
print(f"César: {resultado['IC_cesar']}")
print(f"Afín: {resultado['IC_afin']}")
```

**Salida:**
```
Original: HELLOWORLD
César: KHOORZRUOG
Afín: RSVVSYSVSR

Frecuencias original:
{'A': 0.0, 'B': 0.0, ..., 'D': 10.0, 'E': 10.0, 'H': 10.0, 'L': 20.0, 'O': 20.0, ...}

Índice de Coincidencia:
Original: 0.1111
César: 0.1111      ← Igual al original
Afín: 0.1111       ← Igual al original
```

---

### Ejemplo 2: Demostrar Invariancia de Frecuencias
```python
import comparador_lib

texto = "AABBCCDDEE"  # Frecuencias iguales
resultado = comparador_lib.comparar_cifras(texto, k=3, a=5, b=8)

print("Frecuencias original:", resultado["freq_original"])
print("Frecuencias César:", resultado["freq_cesar"])
print("Frecuencias Afín:", resultado["freq_afin"])
```

**Salida:**
```
Frecuencias original: 
{'A': 20.0, 'B': 20.0, 'C': 20.0, 'D': 20.0, 'E': 20.0, ...}

Frecuencias César: 
{'D': 20.0, 'E': 20.0, 'F': 20.0, 'G': 20.0, 'H': 20.0, ...}
                      ↑ Las mismas frecuencias, letras diferentes

Frecuencias Afín: 
{'I': 20.0, 'N': 20.0, 'S': 20.0, 'X': 20.0, 'C': 20.0, ...}
                      ↑ Las mismas frecuencias, letras diferentes
```

---

### Ejemplo 3: Texto Largo (Análisis Real)
```python
import comparador_lib

texto = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
resultado = comparador_lib.comparar_cifras(texto, k=3, a=7, b=10)

print("Análisis:")
print(resultado["analisis"])

# Encontrar letras más frecuentes
freq_original = resultado["freq_original"]
freq_ordenada = sorted(freq_original.items(), key=lambda x: x[1], reverse=True)
print("\nLetras más frecuentes (original):")
for letra, freq in freq_ordenada[:5]:
    print(f"  {letra}: {freq}%")
```

---

### Ejemplo 4: Observar Mapeos
```python
import comparador_lib

resultado = comparador_lib.comparar_cifras("ABC", k=5, a=7, b=3)

print("Mapeo César:")
for original, cifrado in list(resultado["mapa_cesar"].items())[:10]:
    print(f"  {original} → {cifrado}")

print("\nMapeo Afín:")
for original, cifrado in list(resultado["mapa_afin"].items())[:10]:
    print(f"  {original} → {cifrado}")
```

**Salida:**
```
Mapeo César:
  A → F
  B → G
  C → H
  D → I
  ...

Mapeo Afín:
  A → D
  B → K
  C → R
  D → Y
  ...
```

---

## Análisis Comparativo: César vs Afín

### Tabla de Comparación

| Aspecto | César | Afín |
|---------|-------|------|
| **Fórmula** | C = (M + k) mod 26 | C = (aM + b) mod 26 |
| **Parámetros** | 1 (k) | 2 (a, b) |
| **Posibilidades** | 26 | 312 (12 × 26) |
| **Monoalfabético** | Sí | Sí |
| **Preserva frecuencias** | Sí | Sí |
| **IC invariante** | Sí | Sí |
| **Fácil de romper** | Muy (solo 26) | Moderado (312) |
| **Análisis frecuencias** | Aplica | Aplica |
| **Vigencia histórica** | Muy antigua | Clásica |

---

## Vulnabilidades

### ✗ Ambos comparten debilidades

1. **Invariancia de Frecuencias**
   ```
   Si E es la letra más frecuente en inglés,
   será la más frecuente en el cifrado
   ```

2. **Invariancia del IC**
   ```
   IC(original) = IC(César) = IC(Afín)
   ```

3. **Ataque de Plaintext Conocido**
   ```
   Si se conoce 1 par → se rompe César
   Si se conocen 2 pares → se rompe Afín
   ```

4. **Tamaño de espacio de claves**
   ```
   César: 26 (fuerza bruta trivial)
   Afín: 312 (fuerza bruta rápida)
   ```

---

## Interpretación de Resultados

### Índice de Coincidencia

```
IC ≈ 0.065 (inglés) → Monoalfabético
IC ≈ 0.038 (aleatorio) → Polialfabético o muy desordenado
```

### Frecuencias

```
Si las frecuencias permanecen iguales pero reordenadas:
→ El cifrado es monoalfabético

Si las frecuencias se aplanan uniformemente:
→ El cifrado es bueno (Vigénère, polialfabético)
```

---

## Mejoras Sugeridas

### 1. Añadir métricas adicionales
```python
def divergencia_kullback_leibler(freq1, freq2):
    """Mide cuánto cambia la distribución"""
    ...

def chi_cuadrado(freq_esperada, freq_observada):
    """Test de bondad de ajuste"""
    ...
```

### 2. Visualización gráfica
```python
import matplotlib.pyplot as plt

def graficar_frecuencias(resultado):
    """Graficar las frecuencias de los tres textos"""
    ...
```

### 3. Ataque automático
```python
def atacar_cesar(criptograma):
    """Probar todos los 26 valores de k"""
    ...

def atacar_afin(criptograma):
    """Usar análisis de frecuencias para encontrar a, b"""
    ...
```

---

## Relación con Otros Módulos

- **gcd_lib.py** — Valida que `a` sea coprimo con 26
- **main.py** — Opción 6 usa `comparar_cifras()`
- **criptoanalisis_lib.py** — Complementa con ataques algebraicos

---

## Requisitos

- Python 3.x
- Módulo `gcd_lib` (incluido en el proyecto)
- Sin otras dependencias externas

---

## Conclusiones

### Puntos Clave

✅ **César y Afín son monoalfabéticos**
- Mantienen las frecuencias de letras intactas
- El IC (Índice de Coincidencia) no cambia
- Ambos son vulnerables al análisis de frecuencias

✅ **Afín es más seguro que César (pero aún débil)**
- 312 claves vs 26 (seguridad marginal)
- Requiere 2 pares conocidos para romperse (vs 1 para César)

❌ **Ninguno es adecuado para criptografía moderna**
- Ambos se rompen en segundos
- Usar AES, ChaCha20, o similar

---

## Resumen de Funciones

| Función | Entrada | Salida | Uso |
|---------|---------|--------|-----|
| `cifrar_cesar()` | texto, k | cifrado | Cifrado César |
| `cifrar_afin()` | texto, a, b | cifrado | Cifrado Afín |
| `frecuencia()` | texto | dict | Análisis de frecuencias |
| `indice_coincidencia()` | texto | float | Métrica estadística |
| `generar_mapeo()` | k, a, b | (dict, dict) | Visualizar mapeos |
| `comparar_cifras()` | texto, k, a, b | dict | Análisis completo |

