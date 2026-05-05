# 🚀 Guía: Ejecutar la App con Streamlit

## 📋 Requisitos Previos

- Python 3.8+ instalado
- Git (opcional, solo si quieres usar GitHub)
- pip (gestor de paquetes de Python)

---

## 🏃 Ejecución Local (Desarrollo)

### Paso 1: Instalar Streamlit y dependencias

```bash
pip install -r requirements.txt
```

**O manualmente:**
```bash
pip install streamlit plotly
```

### Paso 2: Ejecutar la app

```bash
streamlit run app.py
```

**Salida esperada:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Paso 3: Abrir en el navegador

Automáticamente se abrirá http://localhost:8501 en tu navegador.

---

## 🌐 Desplegar en Streamlit Cloud (En Línea)

### Opción A: Desde GitHub (Recomendado)

#### Paso 1: Subir a GitHub

```bash
# Si aún no tienes git init
git init

# Crear .gitignore
echo "__pycache__/" > .gitignore
echo ".streamlit/" >> .gitignore
echo "*.pyc" >> .gitignore

# Agregar archivos
git add .
git commit -m "Deploy criptoanálisis app"

# Crear repositorio en GitHub
# (Ve a https://github.com/new y crea un repo)

# Empujar a GitHub (reemplaza con tu URL)
git remote add origin https://github.com/tuusername/mi-repo-cripto.git
git branch -M main
git push -u origin main
```

#### Paso 2: Conectar a Streamlit Cloud

1. Ve a **https://share.streamlit.io/**
2. Haz login con GitHub (o crea cuenta)
3. Click en "New app"
4. Selecciona:
   - **GitHub account:** tu usuario
   - **Repository:** mi-repo-cripto
   - **Branch:** main
   - **File path:** app.py
5. Click en "Deploy"

⏳ Espera 2-3 minutos mientras se instala y se despliega.

**URL resultante:**
```
https://tu-usuario-mi-repo-cripto.streamlit.app
```

---

### Opción B: Desde Replit (Súper fácil, sin GitHub)

1. Ve a **https://replit.com/**
2. Click en "Create Repl"
3. Selecciona "Python"
4. Sube los archivos:
   - `app.py`
   - `requirements.txt`
   - Todos los módulos (`*_lib.py`)
5. En el archivo `replit.nix` o en la terminal, ejecuta:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py --logger.level=error
   ```

6. Click en "Run" (botón verde)

**URL resultante:**
```
https://replit.com/@tu-usuario/mi-app-cripto
```

---

## 📁 Estructura de Archivos

```
mi-repo-cripto/
│
├── app.py                    ← App principal
├── requirements.txt          ← Dependencias
│
├── gcd_lib.py                ← Módulos criptográficos
├── vigenere_lib.py
├── kasiski_lib.py
├── alfabeto_lib.py
├── criptoanalisis_lib.py
├── comparador_lib.py
│
├── README_VIGENERE.md        ← Documentación
├── README_KASISKI.md
├── README_GCD.md
├── README_ALFABETO.md
├── README_CRIPTOANALISIS.md
├── README_COMPARADOR.md
│
└── .gitignore                ← Archivos a ignorar en Git
```

---

## 🔧 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'streamlit'`

**Solución:**
```bash
pip install streamlit
```

---

### Error: `ModuleNotFoundError: No module named 'gcd_lib'`

**Causa:** Los módulos no están en el mismo directorio.

**Solución:**
```
Asegúrate de que `app.py` está en la MISMA carpeta que los módulos (*_lib.py)
```

---

### La app se ve rara en Streamlit Cloud

**Solución:**
- Actualiza Streamlit:
  ```bash
  pip install --upgrade streamlit
  ```

- Borra caché:
  ```bash
  streamlit cache clear
  ```

---

### Error al subir a Streamlit Cloud: `requirements.txt not found`

**Solución:**
Asegúrate de que `requirements.txt` está en la RAÍZ del repositorio GitHub.

---

## 📊 Personalización

### Cambiar el tema

Edita `app.py` y modifica:
```python
st.set_page_config(
    page_title="Tu título",
    page_icon="🔐",
    layout="wide",  # "centered" o "wide"
    theme="auto"     # "light", "dark", "auto"
)
```

---

### Cambiar el nombre de la app en Streamlit Cloud

En tu repositorio GitHub, crea `.streamlit/config.toml`:

```toml
[app]
title = "🔐 Motor Criptográfico"

[client]
showErrorDetails = true
```

---

## 🚀 Tips para Producción

1. **Agregar favicon personalizado**
   ```python
   st.set_page_config(page_icon="🔐")
   ```

2. **Ocultar el menú de Streamlit**
   - Crea `.streamlit/config.toml`:
   ```toml
   [client]
   showMenuItems = false
   ```

3. **Agregar logo personalizado**
   ```python
   st.image("logo.png", width=100)
   ```

4. **Agregar contraseña (opcional)**
   ```python
   if st.secrets["password"] != input_password:
       st.error("Contraseña incorrecta")
       st.stop()
   ```

---

## 📱 Compartir la app

Una vez desplegada, puedes compartir:
- **Enlace directo:** https://tu-usuario-mi-app.streamlit.app
- **Incrustar en un iframe:**
  ```html
  <iframe src="https://tu-usuario-mi-app.streamlit.app" width="100%" height="600"></iframe>
  ```
- **Código QR:** Usa un generador QR con tu URL

---

## 🔐 Seguridad (Información Sensible)

Para guardar claves API u otra información sensible sin mostrarla en GitHub:

### Opción 1: Variables de entorno locales (`.env`)

```bash
# .env (NO subir a GitHub)
OPENAI_API_KEY=sk-xxx...
```

### Opción 2: Secrets en Streamlit Cloud

1. Ve a tu app en Streamlit Cloud
2. Click en menú (⋮) → "Settings"
3. "Secrets"
4. Agrega:
   ```
   OPENAI_API_KEY = "sk-xxx..."
   ```

5. En tu código:
   ```python
   api_key = st.secrets["OPENAI_API_KEY"]
   ```

---

## 📈 Monitoreo

### Ver logs en Streamlit Cloud

1. Ve a tu app en https://share.streamlit.io/
2. Click en tu app
3. "Settings" → "View logs"

---

## 🎓 Recursos Útiles

- **Documentación Streamlit:** https://docs.streamlit.io/
- **Cheat Sheet:** https://docs.streamlit.io/library/cheatsheet
- **Comunidad:** https://discuss.streamlit.io/
- **GitHub:** https://github.com/streamlit/streamlit

---

## 📧 Soporte

Si tienes problemas:
1. Revisa los [Streamlit Issues](https://github.com/streamlit/streamlit/issues)
2. Pregunta en [Streamlit Discussion](https://discuss.streamlit.io/)
3. Abre un issue en tu repositorio

---

¡Listo! Tu app está lista para ser desplegada 🚀

