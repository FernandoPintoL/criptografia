# 🔐 Vigenère Lib - Motor del Cifrador Polialfabético

## Descripción General

`vigenere_lib.py` implementa el **Cifrado de Vigénère**, un algoritmo criptográfico clásico que utiliza una palabra clave para cifrar texto de forma **polialfabética**. A diferencia del cifrado de César (que siempre mapea A→D), Vigénère mapea la misma letra a **diferentes resultados según su posición**.

### Característica Principal
Una misma letra del texto original se cifra de formas **distintas según su posición relativa respecto a la clave**, rompiendo la correspondencia única de los sistemas monoalfabéticos.

---

## Funciones

### 1. `limpiar_texto(texto)`
**Propósito:** Preparar el texto para cifrado.

```python
limpiar_texto("¡Hola Mundo!")  # Retorna: "HOLAMUNDO"
```

**Qué hace:**
- Convierte a mayúsculas
- Elimina espacios y caracteres especiales
- Mantiene solo letras alfabéticas

---

### 2. `generar_clave(texto, clave)`
**Propósito:** Extender la clave para que tenga la misma longitud que el texto.

```python
texto = "HOLA"
clave = "KEY"
generar_clave(texto, clave)  # Retorna: "KEYK"
```

**Proceso:**
- La clave se repite cíclicamente: K-E-Y-K-E-Y-K-E-Y...
- Se alinea con cada letra del texto

---

### 3. `cifrar_vigenere(texto, clave, n=26)`
**Propósito:** Cifrar el texto usando la clave Vigénère.

```python
cifrar_vigenere("HOLA", "KEY")  # Retorna: "RSVF"
```

**Fórmula matemática:**
```
C = (M + K) mod 26
Donde:
  C = letra cifrada
  M = letra del mensaje (0-25)
  K = letra de la clave (0-25)
```

**Ejemplo paso a paso (HOLA con clave KEY):**
```
Pos | Mensaje | Clave | Cifrado
----|---------|-------|--------
 0  |    H    |   K   |   R
 1  |    O    |   E   |   S
 2  |    L    |   Y   |   V
 3  |    A    |   K   |   F
```

---

### 4. `descifrar_vigenere(texto, clave, n=26)`
**Propósito:** Recuperar el texto original a partir del cifrado.

```python
descifrar_vigenere("RSVF", "KEY")  # Retorna: "HOLA"
```

**Fórmula matemática:**
```
M = (C - K) mod 26
Donde:
  M = letra original
  C = letra cifrada (0-25)
  K = letra de la clave (0-25)
```

---

### 5. `mostrar_proceso(texto, clave)`
**Propósito:** Mostrar visualmente cómo se cifra cada letra.

```python
mostrar_proceso("HOLA", "KEY")
```

**Salida:**
```
Pos | M | K | C
----------------
  0 | H | K | R
  1 | O | E | S
  2 | L | Y | V
  3 | A | K | F
```

---

### 6. `analisis_polialfabetico(texto, clave)`
**Propósito:** Demostrar el carácter polialfabético del cifrado.

```python
analisis_polialfabetico("AAAAAA", "BCD")
```

**Salida:**
```
🔍 ANÁLISIS POLIALFABÉTICO
-------------------------
A → B, D, F
```

**¿Qué significa?**
- La letra **A** se cifra como **B** (posición 0, clave B)
- La letra **A** se cifra como **D** (posición 1, clave C)
- La letra **A** se cifra como **F** (posición 2, clave D)

**Esto rompe la substitución monoalfabética**, donde una letra siempre se mapea a la misma letra cifrada.

---

### 7. `dividir_en_columnas(texto, clave)`
**Propósito:** Agrupar el texto en columnas según la longitud de la clave.

```python
dividir_en_columnas("HOLAMUNDODELCRIPTO", "KEY")
```

**Salida:**
```
['HMDDL', 'OMDEO', 'AOURL', 'UCTIP']
```

**Utilidad:** En criptoanálisis, cada columna fue cifrada con la misma letra clave, permitiendo análisis de frecuencia por columnas.

---

### 8. `resumen_vigenere(texto, clave)`
**Propósito:** Análisis completo en un solo llamado.

```python
resultado = resumen_vigenere("HOLA", "KEY")
```

**Retorna un diccionario con:**
- `original` — Texto limpio
- `clave` — Clave limpia
- `clave_extendida` — Clave repetida
- `cifrado` — Texto cifrado
- `descifrado` — Verificación (debe ser igual al original)
- `proceso` — Tabla de cifrado paso a paso
- `analisis` — Análisis polialfabético
- `columnas` — Texto dividido en columnas

---

## Ejemplo de Uso Completo

```python
import vigenere_lib

# Cifrar un mensaje
texto = "El criptograma de Vigenère"
clave = "SECRETO"

cifrado = vigenere_lib.cifrar_vigenere(texto, clave)
print(f"Cifrado: {cifrado}")

# Descifrar
descifrado = vigenere_lib.descifrar_vigenere(cifrado, clave)
print(f"Descifrado: {descifrado}")

# Ver el proceso paso a paso
print(vigenere_lib.mostrar_proceso(texto, clave))

# Verificar el carácter polialfabético
print(vigenere_lib.analisis_polialfabetico(texto, clave))

# Análisis completo
resultado = vigenere_lib.resumen_vigenere(texto, clave)
print(resultado)
```

---

## Conceptos Clave

### Polialfabético vs Monoalfabético

**Monoalfabético (ej: César):**
```
A → siempre → D
B → siempre → E
C → siempre → F
```

**Polialfabético (ej: Vigénère):**
```
A → puede ser → D, F, H, J, ...
B → puede ser → E, G, I, K, ...
C → puede ser → F, H, J, L, ...
```
Depende de la **posición y la clave**.

### Ventajas de Vigénère
✅ Resistente al análisis de frecuencia simple  
✅ Cada letra se cifra diferente según su posición  
✅ Fácil de implementar manualmente  

### Debilidades de Vigénère
❌ Vulnerable al **Método de Kasiski** (detecta longitud de clave)  
❌ Vulnerable al **Análisis de Índice de Coincidencia**  
❌ Si se conoce la longitud de clave, se rompe fácilmente  

---

## Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `texto` | str | Texto a cifrar/descifrar |
| `clave` | str | Palabra clave para el cifrado |
| `n` | int | Tamaño del alfabeto (default: 26) |

---

## Excepciones

- **`ValueError: ❌ La clave no puede estar vacía`** — Se lanza si la clave está vacía después de limpiar

---

## Notas Matemáticas

**Cifrado:**
```
C[i] = (M[i] + K[i mod len(K)]) mod 26
```

**Descifrado:**
```
M[i] = (C[i] - K[i mod len(K)]) mod 26
```

Donde:
- Letras se convierten a números: A=0, B=1, ..., Z=25
- Chr(65) = 'A' en ASCII

---

## Requisitos

- Python 3.x
- Sin dependencias externas

