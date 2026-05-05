# 🔤 Alfabeto Lib - Generador de Alfabetos Mixtos

## Descripción General

`alfabeto_lib.py` implementa un **generador de alfabetos personalizados** basado en una palabra clave opcional. Permite crear **alfabetos de cifra desordenados** para dificultar el análisis criptoanalítico, especialmente en ciencias tradicionales como **sustitución simple** o **Playfair**.

### Concepto Clave
En lugar de usar el alfabeto estándar (A-Z) para cifrar, se puede usar un **alfabeto reordenado** donde las letras más frecuentes se distribuyen irregularmente, complicando el análisis de frecuencias.

---

## Funciones

### 1. `limpiar_clave(clave, alfabeto)`

**Propósito:** Procesar la clave eliminando duplicados y caracteres inválidos.

```python
limpiar_clave("SECRETO", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# Retorna: "SECRETO"

limpiar_clave("SEEECRETO", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# Retorna: "SECRETO"  (sin duplicados)

limpiar_clave("SE1@CRE#TO", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# Retorna: "SECRETO"  (sin caracteres especiales)
```

**Qué hace:**
- Convierte a mayúsculas
- Mantiene solo las letras presentes en el alfabeto
- Elimina la primera ocurrencia de duplicados (mantiene el orden)
- Retorna cadena limpia sin repeticiones

**Algoritmo:**
```
Para cada letra en clave:
    Si la letra está en el alfabeto Y no la hemos visto:
        Agregar a resultado
        Marcar como vista
```

**Características:**
- Preserva el orden original de la clave
- Case-insensitive (convierte a mayúsculas)
- Filtra caracteres fuera del alfabeto

---

### 2. `generar_alfabeto_mixto(clave="", alfabeto_base=None)`

**Propósito:** Generar un alfabeto personalizado basado en una clave.

```python
# Sin clave
generar_alfabeto_mixto()

# Con clave
generar_alfabeto_mixto("SECRETO")

# Con clave y alfabeto personalizado
generar_alfabeto_mixto("CLAVE", "ABCDEFGHIJ")
```

**Algoritmo:**
```
1. Limpiar la clave
2. Obtener las letras del alfabeto base que NO están en la clave
3. Concatenar: clave_limpia + resto
4. Validar (longitud y duplicados)
5. Retornar diccionario con información
```

**Ejemplo paso a paso (clave = "SECRETO"):**
```
Alfabeto base:    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Clave limpia:     S E C R T O (sin duplicados ni caracteres inválidos)
Resto:            A B D F G H I J K L M N P Q U V W X Y Z (sin S,E,C,R,T,O)
Alfabeto mixto:   S E C R T O A B D F G H I J K L M N P Q U V W X Y Z
```

**Validaciones:**
- ✓ Verifica que la longitud sea correcta (26 letras)
- ✓ Verifica que no haya duplicados
- ✓ Lanza excepciones si hay problemas

**Retorna un diccionario:**
```python
{
    "clave_original": "SECRETO",           # Clave tal cual se pasó
    "clave_limpia": "SECRETO",             # Clave procesada
    "alfabeto_base": "ABCDEFGHIJ...",      # Alfabeto original
    "alfabeto_mixto": "SECRETO...",        # Alfabeto generado
    "longitud": 26                          # Longitud del alfabeto
}
```

---

## Ejemplos de Uso

### Ejemplo 1: Generador básico sin clave
```python
import alfabeto_lib

resultado = alfabeto_lib.generar_alfabeto_mixto()

print("Clave original:", resultado["clave_original"])
print("Alfabeto mixto:", resultado["alfabeto_mixto"])
print("Longitud:", resultado["longitud"])
```

**Salida:**
```
Clave original: 
Alfabeto mixto: ABCDEFGHIJKLMNOPQRSTUVWXYZ
Longitud: 26
```

---

### Ejemplo 2: Con clave "SECRETO"
```python
import alfabeto_lib

resultado = alfabeto_lib.generar_alfabeto_mixto("SECRETO")

print("Clave original:", resultado["clave_original"])
print("Clave limpia:", resultado["clave_limpia"])
print("Alfabeto mixto:", resultado["alfabeto_mixto"])
```

**Salida:**
```
Clave original: SECRETO
Clave limpia: SECRETO
Alfabeto mixto: SECRETOABDFGHIJKLMNOPQUVWXYZ
```

---

### Ejemplo 3: Con clave que tiene duplicados
```python
import alfabeto_lib

resultado = alfabeto_lib.generar_alfabeto_mixto("SEEECRETO")

print("Clave original:", resultado["clave_original"])
print("Clave limpia:", resultado["clave_limpia"])
print("Alfabeto mixto:", resultado["alfabeto_mixto"])
```

**Salida:**
```
Clave original: SEEECRETO
Clave limpia: SECRETO       ← Duplicados eliminados
Alfabeto mixto: SECRETOABDFGHIJKLMNOPQUVWXYZ
```

---

### Ejemplo 4: Con caracteres especiales en la clave
```python
import alfabeto_lib

resultado = alfabeto_lib.generar_alfabeto_mixto("SE@#CR1ET0!")

print("Clave limpia:", resultado["clave_limpia"])
print("Alfabeto mixto:", resultado["alfabeto_mixto"])
```

**Salida:**
```
Clave limpia: SECRETO     ← Solo letras
Alfabeto mixto: SECRETOABDFGHIJKLMNOPQUVWXYZ
```

---

### Ejemplo 5: Usar en un cifrado de sustitución
```python
import alfabeto_lib

# Generar alfabeto mixto
resultado = alfabeto_lib.generar_alfabeto_mixto("CLAVE")
alfabeto_mixto = resultado["alfabeto_mixto"]
alfabeto_base = resultado["alfabeto_base"]

# Crear un mapa de cifrado A→alfabeto_mixto
mapa_cifrado = {}
for i, letra in enumerate(alfabeto_base):
    mapa_cifrado[letra] = alfabeto_mixto[i]

print("Mapa de cifrado:")
print(mapa_cifrado)

# Cifrar un mensaje
mensaje = "HOLA MUNDO"
cifrado = ""
for letra in mensaje.upper():
    if letra in mapa_cifrado:
        cifrado += mapa_cifrado[letra]
    else:
        cifrado += letra  # Mantener espacios, números, etc.

print(f"Original: {mensaje}")
print(f"Cifrado: {cifrado}")
```

**Salida:**
```
Mapa de cifrado:
{'A': 'C', 'B': 'L', 'C': 'A', 'D': 'V', 'E': 'E', ...}

Original: HOLA MUNDO
Cifrado: QEVN QRYOD
```

---

## Casos de Error

### Error 1: Alfabeto incompleto
```python
# Si por error se genera un alfabeto incompleto
# Se lanza: ValueError("El alfabeto generado es inválido (longitud incorrecta)")
```

### Error 2: Alfabeto con duplicados
```python
# Si por error se generan duplicados
# Se lanza: ValueError("El alfabeto generado tiene duplicados")
```

---

## Tabla de Comparación

| Escenario | Alfabeto | Uso |
|-----------|----------|-----|
| Sin clave | ABCDEFGHIJKLMNOPQRSTUVWXYZ | Análisis fácil (estándar) |
| Clave "ABC" | ABCDEFGHIJKLMNOPQRSTUVWXYZ | Clave muy corta, poco útil |
| Clave "SECRETO" | SECRETOABDFGHIJKLMNOPQUVWXYZ | Clave efectiva |
| Clave larga | CLAVEMUYLARGOABCDFHIJKNPQSTUXVWXYZ | Máxima seguridad |

---

## Ventajas y Limitaciones

### ✅ Ventajas
- Fácil de usar
- Genera alfabetos válidos y sin duplicados
- Valida automáticamente
- Retorna información completa
- Clave opcional

### ❌ Limitaciones
- No es criptográficamente seguro (solo obfuscación)
- Vulnerable al análisis de frecuencias
- Si se conoce la clave, se rompe fácilmente
- La clave debe ser suficientemente larga (mínimo 6-8 caracteres)

---

## Casos de Uso en Criptografía

1. **Cifrado de Sustitución Simple** — Base para un cifrado
2. **Matriz Playfair** — Inicializar la matriz 5×5
3. **Escítala** — Reordenar alfabeto
4. **Análisis educativo** — Mostrar cómo se obfusca el alfabeto

---

## Matemáticas

### Número de alfabetos posibles
```
Sin clave: 1 alfabeto (A-Z)
Con clave: 26! / repeticiones posibles
```

**Ejemplo:**
- Clave "SECRETO" (7 letras únicas) → Los 7 primeros posiciones fijas
- Resto (19 letras) → 19! formas de ordenarlas
- Total de variaciones: 19! ≈ 121,645,100,408,832

---

## Mejoras Sugeridas

### Soporte para alfabetos personalizados
```python
# Alfabeto solo con consonantes
generar_alfabeto_mixto("CLAVE", "BCDFGHJKLMNPQRSTVWXYZ")

# Alfabeto numérico
generar_alfabeto_mixto("1234", "0123456789")
```

### Función para encontrar inversa
```python
def generar_alfabeto_inverso(alfabeto_mixto):
    """Crea el mapa inverso para descifrar"""
    alfabeto_base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    inverso = {}
    for i, letra in enumerate(alfabeto_base):
        inverso[alfabeto_mixto[i]] = letra
    return inverso
```

---

## Relación con Otros Módulos

- **main.py** — Opción 4 usa `generar_alfabeto_mixto()`
- **Cifrado Afín** — Podría usar el alfabeto mixto
- **Análisis de Frecuencias** — Estudiar cómo afecta el alfabeto

---

## Requisitos

- Python 3.x
- Módulo `string` (estándar)
- Sin otras dependencias

---

## Resumen

| Función | Entrada | Salida | Uso |
|---------|---------|--------|-----|
| `limpiar_clave()` | Clave + alfabeto | Clave limpia | Procesar clave |
| `generar_alfabeto_mixto()` | Clave (opcional) | Diccionario | Generar alfabeto |

