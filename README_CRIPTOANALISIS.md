# 🔍 Criptoanálisis Lib - Módulo de Criptoanálisis por Ecuaciones

## Descripción General

`criptoanalisis_lib.py` implementa un **ataque criptoanalítico al Cifrado Afín** mediante un sistema de ecuaciones lineales. Si el atacante puede deducir dos correspondencias probables entre texto claro y cifrado, puede resolver un sistema de dos ecuaciones para determinar las constantes secretas `a` y `b`.

### Concepto Fundamental
El Cifrado Afín es vulnerable si se conocen suficientes pares de (criptograma, plaintext). Con solo **dos pares**, es posible romperlo completamente.

---

## Teoría Matemática

### Cifrado Afín
```
C = (a·M + b) mod n

Donde:
  C = letra cifrada (0-25)
  M = letra original (0-25)
  a = multiplicador (debe ser coprimo con n)
  b = desplazamiento
  n = módulo (26 para alfabeto inglés)
```

### Sistema de Dos Ecuaciones

Si conocemos dos pares:
```
C₁ = a·M₁ + b (mod 26)  ... (1)
C₂ = a·M₂ + b (mod 26)  ... (2)
```

**Restando (2) de (1):**
```
C₁ - C₂ ≡ a(M₁ - M₂) (mod 26)
ΔC ≡ a·ΔM (mod 26)
```

**Despejando `a`:**
```
a ≡ ΔC · (ΔM)⁻¹ (mod 26)
```

**Despejando `b`:**
```
b ≡ C₁ - a·M₁ (mod 26)
```

### Condición de Solución Única
Para que exista una solución única:
```
mcd(ΔM, 26) = 1

Si mcd(ΔM, 26) ≠ 1 → hay múltiples soluciones o ninguna
```

---

## Funciones

### 1. `inverso_modular(a, n)`

**Propósito:** Calcular el inverso multiplicativo de `a` módulo `n`.

```python
inverso_modular(7, 26)   # Retorna: 15  (porque 7×15 ≡ 1 mod 26)
inverso_modular(5, 26)   # Retorna: 21  (porque 5×21 ≡ 1 mod 26)
inverso_modular(2, 26)   # Retorna: None (2 no tiene inverso mod 26)
```

**Algoritmo:** Usa el **Algoritmo Extendido de Euclides**

```
Entrada: a, n
Salida: a⁻¹ mod n (o None si no existe)

1. Inicializar t=0, nuevo_t=1, r=n, nuevo_r=a
2. Mientras nuevo_r ≠ 0:
   - cociente = r ÷ nuevo_r (división entera)
   - Actualizar t, r usando fórmulas
3. Si r > 1: no existe inverso → retornar None
4. Si t < 0: t = t + n
5. Retornar t
```

**¿Por qué funciona?**
El algoritmo extendido de Euclides encuentra `x` tal que:
```
a·x + n·y = mcd(a, n)

Si mcd(a, n) = 1:
a·x ≡ 1 (mod n)
→ x es el inverso multiplicativo
```

**Complejidad:** O(log(min(a, n)))

---

### 2. `resolver_afine(C1, M1, C2, M2, n=26)`

**Propósito:** Resolver el sistema de ecuaciones para hallar `a` y `b`.

```python
resolver_afine(5, 0, 8, 1, 26)
# Retorna: "✔ a = 3, b = 5\nC = (3M + 5) mod 26"
```

**Parámetros:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `C1` | int | Primer criptograma (0-25) |
| `M1` | int | Primer plaintext correspondiente (0-25) |
| `C2` | int | Segundo criptograma (0-25) |
| `M2` | int | Segundo plaintext correspondiente (0-25) |
| `n` | int | Módulo (default: 26) |

**Algoritmo:**

```
1. Validar que M1 ≠ M2
2. Calcular ΔC = (C1 - C2) mod n
3. Calcular ΔM = (M1 - M2) mod n
4. Verificar que mcd(ΔM, n) = 1
5. Encontrar inverso: inv = (ΔM)⁻¹ mod n
6. Calcular: a = (ΔC × inv) mod n
7. Calcular: b = (C1 - a×M1) mod n
8. Retornar: "a = X, b = Y"
```

**Validaciones:**
- ✓ M1 ≠ M2 (de lo contrario, no hay sistema)
- ✓ mcd(ΔM, 26) = 1 (solución única)
- ✓ Existencia del inverso modular

**Posibles salidas:**

1. **Éxito:**
   ```
   ✔ a = 3, b = 5
   C = (3M + 5) mod 26
   ```

2. **M1 = M2 (error):**
   ```
   ❌ M1 y M2 no pueden ser iguales
   ```

3. **Sin solución única:**
   ```
   ⚠️ mcd(ΔM, 26) = 2
   No hay solución única
   ```

4. **Sin inverso modular:**
   ```
   ❌ No existe inverso modular
   ```

---

## Ejemplos de Uso Completo

### Ejemplo 1: Ataque Simple
```python
import criptoanalisis_lib

# Suponemos que:
# "A" se cifra como "F"  → M=0, C=5
# "B" se cifra como "H"  → M=1, C=7

resultado = criptoanalisis_lib.resolver_afine(
    C1=5, M1=0,
    C2=7, M2=1,
    n=26
)

print(resultado)
```

**Salida:**
```
✔ a = 2, b = 5
C = (2M + 5) mod 26
```

**Verificación:**
- C = 2×0 + 5 = 5 ✓ (A→F)
- C = 2×1 + 5 = 7 ✓ (B→H)

---

### Ejemplo 2: Ataque con palabras conocidas
```python
import criptoanalisis_lib

# Criptograma: "IHHWVC IFMMP"
# Plaintext conocido: "HELLO WORLD"
# Correspondencias:
# H → I (M=7, C=8)
# E → H (M=4, C=7)

resultado = criptoanalisis_lib.resolver_afine(
    C1=8, M1=7,
    C2=7, M2=4,
    n=26
)

print(resultado)
```

**Salida:**
```
✔ a = 1, b = 1
C = (1M + 1) mod 26
```

(Esto es el cifrado de César con desplazamiento 1)

---

### Ejemplo 3: Caso sin solución única
```python
import criptoanalisis_lib

# M1=0, M2=13 tienen mcd(13, 26) = 13 ≠ 1

resultado = criptoanalisis_lib.resolver_afine(
    C1=5, M1=0,
    C2=8, M2=13,
    n=26
)

print(resultado)
```

**Salida:**
```
⚠️ mcd(13, 26) = 13
No hay solución única
```

---

### Ejemplo 4: Ataque completo
```python
import criptoanalisis_lib

# Tenemos un criptograma y creemos saber dos correspondencias
# Usamos el ataque para hallar a y b
# Luego ciframos/desciframos con esos parámetros

C1, M1 = 8, 7   # Suposición 1
C2, M2 = 7, 4   # Suposición 2

resultado = criptoanalisis_lib.resolver_afine(C1, M1, C2, M2)

if "✔" in resultado:
    # Extraer a y b
    linea = resultado.split('\n')[0]
    a = int(linea.split('=')[1].split(',')[0].strip())
    b = int(linea.split('=')[2].strip())
    
    print(f"Parámetros encontrados: a={a}, b={b}")
    
    # Descifrar el mensaje
    criptograma = "IHHWVCIFMMP"
    descifrado = ""
    
    for letra in criptograma:
        if letra.isalpha():
            c = ord(letra) - 65
            m = (c - b) * pow(a, -1, 26) % 26  # Inverso de a
            descifrado += chr(m + 65)
        else:
            descifrado += letra
    
    print(f"Descifrado: {descifrado}")
else:
    print("No se puede resolver:", resultado)
```

---

## Paso a Paso de un Ataque Real

### Escenario
- **Texto original (conocido):** "THE"
- **Texto cifrado (observado):** "WKH"
- **Correspondencias:** T→W (M=19, C=22), H→K (M=7, C=10)

### Resolución Manual

**Paso 1: Calcular diferencias**
```
ΔC = (22 - 10) mod 26 = 12
ΔM = (19 - 7) mod 26 = 12
```

**Paso 2: Verificar solución única**
```
mcd(12, 26) = 2 ≠ 1
⚠️ No hay solución única
```

**Conclusión:** Las correspondencias asumidas probablemente son incorrectas.

---

### Escenario Correcto
- **Correspondencias:** T→W (M=19, C=22), H→P (M=7, C=15)

**Paso 1: Calcular diferencias**
```
ΔC = (22 - 15) mod 26 = 7
ΔM = (19 - 7) mod 26 = 12
```

**Paso 2: Verificar solución única**
```
mcd(12, 26) = 2 ≠ 1
⚠️ Aún no hay solución única
```

**Paso 3: Elegir mejores correspondencias**
- **Correspondencias:** A→B (M=0, C=1), B→D (M=1, C=3)

```
ΔC = (1 - 3) mod 26 = -2 ≡ 24 (mod 26)
ΔM = (0 - 1) mod 26 = -1 ≡ 25 (mod 26)
mcd(25, 26) = 1 ✓
```

**Paso 4: Calcular inverso**
```
a ≡ 24 × 25⁻¹ (mod 26)
25⁻¹ ≡ 25 (mod 26)  [porque 25×25=625≡1 mod 26]
a ≡ 24 × 25 ≡ 600 ≡ 16 (mod 26)
```

**Paso 5: Calcular b**
```
b ≡ 1 - 16×0 ≡ 1 (mod 26)
```

**Resultado:** `C = (16M + 1) mod 26`

---

## Limitaciones y Consideraciones

### ✅ Cuándo funciona bien
- Se conocen **exactamente 2 pares** clave-valor
- Las correspondencias son **correctas**
- mcd(ΔM, 26) = 1

### ❌ Cuándo falla
- Las correspondencias asumidas son **incorrectas**
- mcd(ΔM, 26) ≠ 1 (escolio múltiples o ninguna solución)
- Los pares no son independientes (M1 - M2 = 0)

### ⚠️ Mejora sugerida
Probar múltiples pares de correspondencias y validar mediante análisis de frecuencias.

---

## Relación Matemática con Otras Funciones

**`gcd_lib.gcd()`** → Verifica si mcd(ΔM, 26) = 1  
**`inverso_modular()`** → Calcula (ΔM)⁻¹ mod 26  

---

## Aplicaciones Prácticas

1. **Ataque de Plaintext Conocido**
   - Si el atacante conoce parte del mensaje original

2. **Ataque de Plaintext Elegido**
   - Si el atacante puede hacer cifrar palabras específicas

3. **Análisis Criptográfico**
   - Validar la robustez del Cifrado Afín

---

## Mejoras Sugeridas

### 1. Probar múltiples pares automáticamente
```python
def ataque_fuerza_bruta(criptograma, plaintext_parcial):
    """Probar todas las combinaciones de pares conocidos"""
    for i in range(len(plaintext_parcial)-1):
        for j in range(i+1, len(plaintext_parcial)):
            # Intentar resolver con pares (i, j)
            ...
```

### 2. Validar con análisis de frecuencias
```python
def validar_parametros(a, b, criptograma):
    """Verificar si los parámetros son correctos"""
    # Descifrar y calcular IC (índice de coincidencia)
    ...
```

### 3. Interfaz mejorada
```python
def atacar_afine_interactivo():
    """Interfaz amigable para el ataque"""
    print("Ingrese dos correspondencias conocidas")
    ...
```

---

## Notas de Seguridad

🔴 **El Cifrado Afín es débil:**
- Con solo 2 pares clave-valor, se puede romper completamente
- No es seguro para datos sensibles
- Es principalmente educativo

✅ **Cómo protegerse:**
- Usar cifrados modernos (AES, ChaCha20, etc.)
- No reutilizar parámetros
- Usar claves criptográficas fuertes

---

## Requisitos

- Python 3.x
- Módulo `gcd_lib` (incluido en el proyecto)
- Sin otras dependencias externas

---

## Resumen

| Función | Entrada | Salida | Complejidad |
|---------|---------|--------|-------------|
| `inverso_modular()` | a, n | a⁻¹ mod n | O(log n) |
| `resolver_afine()` | C1, M1, C2, M2 | a, b | O(log n) |

**Caso de Uso Principal:** Romper Cifrado Afín si se conocen 2 pares clave-valor.

