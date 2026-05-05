# 🔐 GCD Lib - Validador de Constante de Decimación

## Descripción General

`gcd_lib.py` implementa herramientas matemáticas fundamentales para **validar parámetros criptográficos** del **Cifrado Afín**. Su función principal es verificar si una constante `a` es válida para cifrar mediante la relación:

```
C = (a × M + b) mod n
```

### Concepto Clave
Para que el cifrado afín funcione correctamente y se pueda descifrar, **la constante `a` debe ser coprima con el módulo `n`**, es decir: **mcd(a, n) = 1**.

---

## ¿Por qué es importante?

En criptografía:
- **Si mcd(a, n) = 1** → Existe un **inverso multiplicativo de a**
- **Si mcd(a, n) ≠ 1** → **NO existe inverso** → **No se puede descifrar**

Esto determina si se obtiene un **CCR (Conjunto Completo de Residuos)**, que es esencial para que el cifrado sea inyectivo (cada letra original mapea a una única letra cifrada).

---

## Funciones

### 1. `gcd(a, b)` — Máximo Común Divisor

**Propósito:** Calcular el MCD de dos números usando el algoritmo de Euclides.

```python
gcd(48, 18)   # Retorna: 6
gcd(15, 25)   # Retorna: 5
gcd(7, 26)    # Retorna: 1
```

**Fórmula matemática:**
```
gcd(a, 0) = a
gcd(a, b) = gcd(b, a mod b)
```

**Proceso paso a paso para gcd(48, 18):**
```
Paso 1: gcd(48, 18) → 48 mod 18 = 12 → gcd(18, 12)
Paso 2: gcd(18, 12) → 18 mod 12 = 6  → gcd(12, 6)
Paso 3: gcd(12, 6)  → 12 mod 6 = 0   → gcd(6, 0)
Paso 4: gcd(6, 0) = 6 ✓
```

**Características:**
- Maneja valores negativos (usa valores absolutos)
- Rápido y eficiente
- Complejidad: O(log(min(a, b)))

**Casos especiales:**
```python
gcd(0, 5)     # Retorna: 5
gcd(-12, 8)   # Retorna: 4 (usa abs)
gcd(1, 26)    # Retorna: 1 (coprimos)
```

---

### 2. `factores_comunes(a, b)` — Encuentra Divisores Compartidos

**Propósito:** Identificar qué números dividen a ambos valores.

```python
factores_comunes(12, 18)   # Retorna: [2, 3, 6]
factores_comunes(7, 26)    # Retorna: []
factores_comunes(4, 26)    # Retorna: [2]
```

**Algoritmo:**
```python
Para cada número i desde 2 hasta min(|a|, |b|):
    Si i divide a a Y i divide a b:
        Agregar i a la lista
Retornar lista de divisores comunes
```

**¿Qué significa?**
- `factores_comunes(12, 18) = [2, 3, 6]`
  - 12 = 2² × 3
  - 18 = 2 × 3²
  - Comparten: 2, 3, 2×3=6

**Utilidad en criptografía:**
- Si hay factores comunes → no es coprimo → no es válido para cifrado afín

**Complejidad:** O(min(a, b)) — puede ser lento con números grandes

---

### 3. `validar_constante(a, n)` — ✅ Validador Principal

**Propósito:** Verificar si `a` es válida para usar en Cifrado Afín modulo `n`.

```python
validar_constante(7, 26)    # Válida
validar_constante(4, 26)    # Inválida
validar_constante(0, 26)    # Inválida
```

**Retorna:** Una cadena de texto con el análisis detallado.

---

## Casos de Validación

### ✔ Caso 1: `a = 0`
```python
validar_constante(0, 26)
```

**Salida:**
```
❌ INVÁLIDO
a = 0, n = 26
0 no tiene inverso multiplicativo en ningún módulo
❌ No se puede usar en CCR
```

**Explicación:** El cero nunca tiene inverso multiplicativo.

---

### ✔ Caso 2: mcd(a, n) = 1 (Válido - Coprimos)
```python
validar_constante(7, 26)
```

**Salida:**
```
✔ VÁLIDO
a = 7, n = 26
mcd(7,26) = 1 → son coprimos
✔ Existe inverso modular
✔ Se puede usar en CCR
```

**Explicación:**
- 7 y 26 no comparten factores
- Existe inverso: 7⁻¹ ≡ 15 (mod 26) porque 7×15 ≡ 1 (mod 26)
- Se puede cifrar y descifrar correctamente

---

### ✔ Caso 3: mcd(a, n) ≠ 1 (Inválido - Comparten factores)
```python
validar_constante(4, 26)
```

**Salida:**
```
❌ INVÁLIDO
a = 4, n = 26
mcd(4,26) = 2 → comparten factores
Factores comunes: [2]
💡 Al compartir factores, no existe inverso multiplicativo
❌ No se puede usar en CCR
```

**Explicación:**
- 4 = 2²
- 26 = 2 × 13
- Comparten el factor 2
- No existe inverso de 4 módulo 26
- **No se puede descifrar correctamente**

---

### ✔ Caso 4: Otra combinación inválida
```python
validar_constante(6, 9)
```

**Salida:**
```
❌ INVÁLIDO
a = 6, n = 9
mcd(6,9) = 3 → comparten factores
Factores comunes: [3]
💡 Al compartir factores, no existe inverso multiplicativo
❌ No se puede usar en CCR
```

---

## Ejemplos de Uso Completo

### Ejemplo 1: Validar parámetro para Cifrado Afín
```python
import gcd_lib

# Validar si podemos usar a = 5 en módulo 26
resultado = gcd_lib.validar_constante(5, 26)
print(resultado)
```

**Salida:**
```
✔ VÁLIDO
a = 5, n = 26
mcd(5,26) = 1 → son coprimos
✔ Existe inverso modular
✔ Se puede usar en CCR
```

---

### Ejemplo 2: Calcular inverso multiplicativo
```python
import gcd_lib

# Verificar que 7 es válido
validez = gcd_lib.validar_constante(7, 26)
print(validez)

# Luego buscar su inverso (7 × x ≡ 1 mod 26)
for x in range(1, 26):
    if (7 * x) % 26 == 1:
        print(f"Inverso de 7 mod 26 es: {x}")
```

**Salida:**
```
✔ VÁLIDO
a = 7, n = 26
...
Inverso de 7 mod 26 es: 15
```

**Verificación:** 7 × 15 = 105 ≡ 1 (mod 26) ✓

---

### Ejemplo 3: Encontrar todos los valores válidos para n=26
```python
import gcd_lib

print("Valores válidos para a (módulo 26):")
validos = []

for a in range(1, 26):
    if gcd_lib.gcd(a, 26) == 1:
        validos.append(a)

print(validos)
```

**Salida:**
```
Valores válidos para a (módulo 26):
[1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
```

**Observación:** Son exactamente los números coprimos con 26.

---

## Tabla de Referencia para n = 26

| a | mcd(a,26) | ¿Válido? | Inverso |
|---|-----------|----------|---------|
| 1 | 1 | ✔ | 1 |
| 3 | 1 | ✔ | 9 |
| 5 | 1 | ✔ | 21 |
| 7 | 1 | ✔ | 15 |
| 9 | 1 | ✔ | 3 |
| 2 | 2 | ❌ | — |
| 4 | 2 | ❌ | — |
| 6 | 2 | ❌ | — |
| 8 | 2 | ❌ | — |
| 10 | 2 | ❌ | — |
| 12 | 2 | ❌ | — |
| 13 | 13 | ❌ | — |
| 14 | 2 | ❌ | — |

---

## Conceptos Matemáticos Clave

### Coprimos
Dos números son **coprimos** (o relativamente primos) si su MCD es 1.

```
mcd(a, n) = 1 ⟹ a y n son coprimos
```

### Inverso Multiplicativo
Un número `a` tiene inverso multiplicativo módulo `n` si existe `a⁻¹` tal que:

```
a × a⁻¹ ≡ 1 (mod n)
```

**Teorema:** Existe inverso multiplicativo de `a` módulo `n` **si y solo si mcd(a, n) = 1**

### Conjunto Completo de Residuos (CCR)
Un CCR módulo `n` es un conjunto de `n` números donde cada uno representa una clase residual diferente.

En Cifrado Afín, para que sea una **permutación válida**, necesitamos un CCR, lo que requiere que mcd(a, n) = 1.

---

## Función de Euler

El número de valores válidos de `a` para un módulo `n` es **φ(n)** (función de Euler):

```
φ(n) = número de enteros k en [1, n] tales que mcd(k, n) = 1
```

**Ejemplos:**
- φ(26) = 12 (números válidos: 1,3,5,7,9,11,15,17,19,21,23,25)
- φ(29) = 28 (26 es primo, todos menos el cero son válidos)
- φ(10) = 4 (números válidos: 1,3,7,9)

---

## Limitaciones

❌ **`factores_comunes()` es lenta:**
- Itera desde 2 hasta min(a, b)
- Complejidad O(n) para números grandes
- Mejor usar descomposición en primos

❌ **No encuentra inverso multiplicativo:**
- Solo valida si existe
- Para encontrarlo, usar algoritmo extendido de Euclides

---

## Mejoras Sugeridas

### Versión mejorada de `factores_comunes()`:
```python
def factores_comunes_rapido(a, b):
    """Usa descomposición en primos"""
    d = gcd(a, b)
    factores = []
    divisor = 2
    temp = d
    
    while divisor * divisor <= temp:
        if temp % divisor == 0:
            factores.append(divisor)
            while temp % divisor == 0:
                temp //= divisor
        divisor += 1
    
    if temp > 1:
        factores.append(temp)
    
    return factores
```

### Función para encontrar inverso:
```python
def inverso_multiplicativo(a, n):
    """Encuentra a⁻¹ mod n usando algoritmo extendido de Euclides"""
    if gcd(a, n) != 1:
        return None  # No existe inverso
    
    # Implementar algoritmo extendido de Euclides
    ...
```

---

## Relación con Otros Módulos

- **Cifrado Afín** — Usa `validar_constante()` para verificar parámetros
- **main.py** — Opción 3 llama a `validar_constante()`
- **comparador_lib.py** — Probablemente usa `gcd()` internamente

---

## Aplicaciones en Criptografía

1. **Validación de Cifrado Afín** ← Principal
2. **Criptoanálisis** — Detectar parámetros inválidos
3. **Generación de Alfabetos Mixtos** — Usar coprimos
4. **RSA** — Seleccionar números coprimos con φ(n)

---

## Requisitos

- Python 3.x
- Sin dependencias externas

---

## Resumen

| Función | Entrada | Salida | Uso |
|---------|---------|--------|-----|
| `gcd(a, b)` | Dos números | MCD | Verificar coprimalidad |
| `factores_comunes(a, b)` | Dos números | Lista de divisores | Análisis detallado |
| `validar_constante(a, n)` | Parámetros afín | Mensaje de validación | Cifrado afín seguro |

