# 🔎 Kasiski Lib - Detector del Período de Vigénère

## Descripción General

`kasiski_lib.py` implementa el **Método de Kasiski**, un algoritmo criptoanalítico que permite **descubrir la longitud probable de la clave** utilizada en un cifrado de Vigénère, **sin necesidad de descifrar el mensaje**.

### Principio Fundamental
Si el mismo texto aparece en múltiples lugares de un criptograma cifrado con Vigénère, la **distancia entre sus repeticiones es un múltiplo de la longitud de la clave**. Calculando el MCD de todas estas distancias, obtenemos la longitud.

---

## ¿Cómo Funciona?

### Ejemplo Conceptual

Imagina que cifras "THEOLDMAN" con clave "KEY" (longitud 3):

```
Texto:     T H E O L D M A N
Clave:     K E Y K E Y K E Y (repetida)
Cifrado:   D L C I P C W E X
```

Si la palabra "THE" aparece nuevamente 6 caracteres después:
```
Distancia = 6
MCD(6) = 6 o sus divisores: [2, 3, 6]
La longitud real es 3 ✓
```

---

## Funciones

### 1. `limpiar_texto(texto)`
**Propósito:** Preparar el texto para análisis.

```python
limpiar_texto("CRIPTOGRAMA123!")  # Retorna: "CRIPTOGRAMA"
```

**Qué hace:**
- Convierte a mayúsculas
- Elimina números y caracteres especiales
- Mantiene solo letras

---

### 2. `buscar_repeticiones(texto, n=3)`
**Propósito:** Encontrar cadenas de caracteres que se repiten.

```python
buscar_repeticiones("THEQUICKBROWNFOXTHEQUICKBROWN", 3)
```

**Retorna:**
```python
{
    'THE': [0, 16],
    'QUI': [3, 19],
    'BRO': [10, 26],
    ...
}
```

**Parámetros:**
- `texto` — Texto a analizar
- `n` — Longitud de patrón (default: 3)

**Qué hace:**
- Busca todos los patrones de `n` caracteres
- Registra sus posiciones
- Solo retorna patrones que aparecen **más de una vez**

---

### 3. `calcular_distancias(repeticiones)`
**Propósito:** Calcular las distancias entre repeticiones.

```python
repeticiones = {'THE': [0, 16], 'QUI': [3, 19]}
calcular_distancias(repeticiones)
```

**Retorna:**
```python
[16, 16]  # THE está a 16 caracteres de distancia
```

**Fórmula:**
```
Distancia = posición_2 - posición_1
```

**Matemáticamente:** Cada distancia es un **múltiplo de la longitud de clave**.

---

### 4. `calcular_mcd_lista(lista)`
**Propósito:** Calcular el MCD de todas las distancias.

```python
calcular_mcd_lista([16, 24, 32, 40])
```

**Retorna:**
```python
8  # MCD(16, 24, 32, 40) = 8
```

**Proceso:**
```
MCD(16, 24) = 8
MCD(8, 32) = 8
MCD(8, 40) = 8
→ MCD final = 8
```

**Significado:** La longitud probable de la clave es **8** (o un divisor de 8).

---

### 5. `kasiski(texto, n=3)`
**Propósito:** Función principal que realiza el análisis completo.

```python
resultado = kasiski("CRIPTOGRAMAENCIFRADO", 3)
```

**Retorna un diccionario:**
```python
{
    "mensaje": "✔ Análisis Kasiski completado",
    "texto_limpio": "CRIPTOGRAMAENCIFRADO",
    "repeticiones": {'CRI': [0, 9], 'AMA': [6, 15], ...},
    "distancias": [9, 9, 6, 12, 18],
    "mcd": 3,
    "posibles_claves": [3]
}
```

**Validaciones:**
- Si el texto es muy corto: devuelve error
- Si no hay repeticiones: devuelve error
- Si hay repeticiones: retorna análisis completo

---

### 6. `resumen_kasiski(texto, n=3)`
**Propósito:** Formato legible para mostrar en consola.

```python
print(resumen_kasiski("CRIPTOGRAMACLAVE", 3))
```

**Salida:**
```
🔍 MÉTODO DE KASISKI
--------------------
Mensaje: ✔ Análisis Kasiski completado
MCD estimado: 4
Posibles longitudes de clave: [2, 4]

📌 Repeticiones:
CRI → [0, 8]
OGR → [3, 11]

📏 Distancias:
[8, 8]
```

---

## Ejemplo de Uso Completo

```python
import kasiski_lib
import vigenere_lib

# Crear un criptograma con Vigénère
texto = "ELLARGO CRIPTOGRAMA MUESTRA PATRONES REPETIDOS"
clave = "SECRETO"  # Longitud = 7

cifrado = vigenere_lib.cifrar_vigenere(texto, clave)
print(f"Cifrado: {cifrado}")

# Aplicar Método de Kasiski
resultado = kasiski_lib.kasiski(cifrado, 3)

print(f"MCD estimado: {resultado['mcd']}")
print(f"Posibles longitudes: {resultado['posibles_claves']}")

# Mostrar análisis detallado
print(kasiski_lib.resumen_kasiski(cifrado, 3))
```

**Salida esperada:**
```
MCD estimado: 7
Posibles longitudes: [7]  ← ¡Descubrió la longitud!
```

---

## Casos de Uso

### Caso 1: Clave Corta (Fácil)
```
Clave: "KEY" (longitud 3)
Distancias encontradas: [3, 6, 9, 12]
MCD = 3 ✅ Se descubre fácilmente
```

### Caso 2: Clave Larga (Difícil)
```
Clave: "LONGSECRETPASSWORD" (longitud 18)
Distancias encontradas: [18, 36, 54]
MCD = 18 ✅ Se descubre si hay suficientes repeticiones
```

### Caso 3: Texto Corto (Falla)
```
Clave: "KEY"
Texto cifrado: "ABCDEF"  (muy corto)
Resultado: ❌ No hay suficientes repeticiones
```

---

## Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `texto` | str | Criptograma a analizar |
| `n` | int | Longitud de patrones buscados (default: 3) |

---

## Estructura del Resultado

```python
{
    "mensaje": str,              # Estado del análisis
    "texto_limpio": str,         # Texto sin espacios/caracteres
    "repeticiones": dict,        # Patrones → [posiciones]
    "distancias": list,          # Todas las distancias
    "mcd": int,                  # Máximo Común Divisor
    "posibles_claves": list      # Divisores del MCD (posibles longitudes)
}
```

---

## Excepciones y Errores

| Error | Causa | Solución |
|-------|-------|----------|
| Texto demasiado corto | Menos de `n` caracteres | Usar texto más largo |
| No se encontraron repeticiones | Patrones únicos | Reducir `n` (buscar patrones más cortos) |

---

## Limitaciones y Consideraciones

### Cuándo funciona bien:
✅ Criptograma **largo** (100+ caracteres)  
✅ Clave **corta o mediana** (3-20 caracteres)  
✅ Muchas **repeticiones naturales** en el texto original  

### Cuándo funciona mal:
❌ Criptograma **muy corto** (<50 caracteres)  
❌ Clave **muy larga** (casi igual que el texto)  
❌ Texto original sin repeticiones naturales  
❌ Patrón `n` muy grande (difícil de repetir)  

---

## Mejoras Sugeridas

Después de obtener la longitud de clave con Kasiski, puedes:

1. **Análisis de Frecuencia por Columna**
   - Dividir el criptograma en columnas según la longitud
   - Cada columna fue cifrada con la misma letra de clave
   - Aplicar análisis de frecuencia a cada columna

2. **Búsqueda por Fuerza Bruta**
   - Probar todas las claves de la longitud descubierta
   - Validar según frecuencias esperadas del idioma

3. **Índice de Coincidencia**
   - Verificar la longitud descubierta
   - Calcular IC para validar hipótesis

---

## Historia del Método

**Friedrich Wilhelm Kasiski (1805-1881)**, criptógrafo prusiano, publicó este método en 1863, mucho antes de la era digital. Fue el **primer ataque práctico contra Vigénère** y demostró que el cifrado no era impenetrable.

---

## Notas Matemáticas

**Relación fundamental:**
```
Si P = patrón repetido
Si distancia entre repeticiones = d₁, d₂, ..., dₙ

Entonces: d₁ ≡ 0 (mod L)
         d₂ ≡ 0 (mod L)
         ...
         dₙ ≡ 0 (mod L)

Donde L = longitud de clave

Por lo tanto: L divide a MCD(d₁, d₂, ..., dₙ)
```

---

## Requisitos

- Python 3.x
- Módulo `gcd_lib` (incluido en el proyecto)
- Sin otras dependencias

---

## Relación con Otros Módulos

- **vigenere_lib.py** — Genera los criptogramas para analizar
- **gcd_lib.py** — Calcula el MCD de distancias
- **main.py** — Interfaz que integra ambos módulos

