# 🎵 Música & Bienestar — Predictor de Impacto Musical en la Salud Mental

> Aplicación web interactiva que predice si los hábitos musicales de una persona pueden tener un efecto positivo en su bienestar emocional, utilizando un modelo de clasificación entrenado con datos reales.
> Desplegada en: https://despliegue-musica-y-salud-mental-moqsnonbrqyp93pij7g7xq.streamlit.app
---

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Motivación](#motivación)
- [Demo](#demo)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Dataset](#dataset)
- [Modelo de Machine Learning](#modelo-de-machine-learning)
- [Aplicación Web](#aplicación-web)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Uso de la Aplicación](#uso-de-la-aplicación)
- [Variables del Modelo](#variables-del-modelo)
- [Estructura de Archivos](#estructura-de-archivos)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Consideraciones Éticas](#consideraciones-éticas)
- [Autores](#autores)

---

## Descripción General

**Música & Bienestar** es una aplicación de predicción orientativa que, a partir de un perfil musical y emocional del usuario, estima si sus hábitos de escucha musical tienen el potencial de mejorar su bienestar percibido.

El sistema combina un modelo de clasificación supervisado —entrenado sobre una encuesta real de música y salud mental— con una interfaz web limpia y accesible construida en Streamlit. El usuario responde preguntas sobre su edad, plataforma de streaming, frecuencia de escucha por géneros y niveles de ansiedad, depresión y TOC, y recibe un resultado inmediato e interpretado.

---

## Motivación

Numerosos estudios en musicoterapia y psicología sugieren que la música puede tener efectos significativos sobre el estado emocional de las personas. Sin embargo, estos efectos no son universales: dependen del perfil del oyente, el género musical, el contexto de escucha y factores de salud mental preexistentes.

Este proyecto nació con el propósito de explorar esa relación de manera empírica: ¿Es posible predecir, a partir del perfil de escucha de alguien, si la música le ayuda o no? La respuesta que buscamos no es clínica, sino orientativa y educativa.

---

## Demo

La aplicación se divide en tres pasos guiados:

1. **Sobre ti** — edad, plataforma de streaming, hábitos de escucha.
2. **Cómo te sientes** — niveles de ansiedad, depresión y TOC en escala 0–10.
3. **Tu música** — género favorito y frecuencia de escucha por 16 géneros.

Al enviar, el modelo clasifica al usuario en una de dos categorías:

| Resultado | Significado |
|-----------|-------------|
| ✅ **Improve** | El perfil se parece a usuarios que reportaron mejora en su bienestar gracias a la música. |
| 🔍 **Sin señal clara** | El modelo no detecta una señal positiva fuerte con este perfil de hábitos. |

---

## Arquitectura del Proyecto

```
┌─────────────────────────────────────────────────────┐
│                   Usuario (Navegador)                │
└─────────────────────┬───────────────────────────────┘
                      │  Formulario web
                      ▼
┌─────────────────────────────────────────────────────┐
│              Streamlit (app.py)                      │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────┐  │
│  │ Tab: Perfil  │  │ Tab: Emociones│  │Tab: Música│  │
│  └──────┬───────┘  └──────┬────────┘  └─────┬────┘  │
│         └─────────────────┴────────────────-┘        │
│                     Validación de campos              │
│                           │                          │
│              Preprocesamiento de datos                │
│         (one-hot encoding + min-max scaling)          │
│                           │                          │
│              modelo-cla.pkl (pickle)                  │
│     ┌─────────────────────────────────────────┐      │
│     │  Clasificador + LabelEncoder + Scaler   │      │
│     └─────────────────────────────────────────┘      │
│                           │                          │
│              Predicción e interpretación              │
└───────────────────────────┬─────────────────────────-┘
                            │
                   Resultado al usuario
```

---

## Dataset

El modelo fue entrenado con el dataset público **MxMH (Music & Mental Health Survey)**, recopilado mediante encuestas voluntarias a más de 700 participantes de diferentes edades y países.

### Variables originales del dataset

| Categoría | Variables |
|-----------|-----------|
| **Demográficas** | Edad, plataforma de streaming, horas de escucha al día |
| **Hábitos** | Escucha mientras trabaja, carácter explorador, instrumentista, compositor |
| **Géneros** | Frecuencia de escucha (Never / Rarely / Sometimes / Very frequently) para 16 géneros |
| **Salud mental** | Ansiedad, Depresión, TOC, Insomnio (escala 0–10) |
| **Variable objetivo** | `Music effects` → Improve / No effect / Worsen |

### Preprocesamiento aplicado

- Las variables `Worsen` y `No effect` se unificaron en una sola clase (`No improve`) para simplificar el problema y aumentar la robustez del modelo ante el desbalance de clases.
- Variables categóricas binarias codificadas con **One-Hot Encoding + drop_first**.
- Variables categóricas multi-nivel codificadas con **One-Hot Encoding sin drop** (ej. género favorito, plataforma).
- Variables numéricas (`Age`, `Hours per day`, `Anxiety`, `Depression`, `OCD`) normalizadas con **MinMaxScaler** en rango [0, 1].

---

## Modelo de Machine Learning

### Archivo del modelo

El modelo se carga desde `modelo-cla.pkl`, un archivo pickle que contiene una tupla con cuatro objetos:

```python
(modelo, labelencoder, variables, min_max_scaler)
```

| Objeto | Tipo | Descripción |
|--------|------|-------------|
| `modelo` | Clasificador sklearn | Modelo entrenado (ej. Random Forest, SVM, etc.) |
| `labelencoder` | `LabelEncoder` | Codifica/decodifica la variable objetivo |
| `variables` | `list[str]` | Lista ordenada de columnas que espera el modelo |
| `min_max_scaler` | `MinMaxScaler` | Escalador ajustado sobre el conjunto de entrenamiento |

### Pipeline de predicción

1. El usuario completa el formulario → se construye un `dict` con las respuestas.
2. Se convierte en un `pd.DataFrame` de una fila.
3. Variables categóricas → `pd.get_dummies()`.
4. Se realinean las columnas con `reindex(columns=variables, fill_value=0)` para garantizar que el modelo reciba exactamente el mismo espacio de características con el que fue entrenado.
5. Variables numéricas → `min_max_scaler.transform()`.
6. `modelo.predict()` → clase codificada → `labelencoder.inverse_transform()` → etiqueta legible.

---

## Aplicación Web

### Características de la interfaz

- **Tema oscuro** con tipografía `DM Serif Display` (títulos) y `DM Sans` (cuerpo).
- **Flujo guiado en 3 pestañas** con indicadores de campo obligatorio (`*`).
- **Validación en el cliente** antes de lanzar la predicción: si falta algún campo requerido, se muestra un banner de error con la lista de campos pendientes y en qué pestaña se encuentran.
- **Géneros opcionales** (Country, EDM, Folk, Gospel, K-pop, Metal, R&B, Video Game Music) se asignan automáticamente a `"Never"` si el usuario no los completa, sin bloquear el flujo.
- **Resultado interpretado** con cards visuales diferenciadas por color (verde para mejora, naranja para sin señal clara) y lenguaje accesible.
- **Aviso de responsabilidad** siempre visible junto al resultado.
- **Panel técnico colapsable** para inspeccionar los datos preparados enviados al modelo.

---

## Instalación y Ejecución

### Requisitos

- Python 3.8 o superior
- pip

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/musica-bienestar.git
cd musica-bienestar
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Asegurarte de tener el modelo

El archivo `modelo-cla.pkl` debe estar en la raíz del proyecto (mismo directorio que `app.py`). Si no lo tienes, consulta la sección [Entrenamiento del modelo](#entrenamiento-del-modelo).

### 5. Ejecutar la aplicación

```bash
streamlit run app.py
```

La app estará disponible en `http://localhost:8501`.

---

### `requirements.txt` mínimo

```
streamlit>=1.30.0
pandas>=1.5.0
scikit-learn>=1.2.0
```

---

## Uso de la Aplicación

### Paso 1 — Sobre ti

| Campo | Tipo | Obligatorio |
|-------|------|-------------|
| Edad | Slider (10–89) | ✅ |
| Horas al día de escucha | Slider (0–24) | ✅ |
| Plataforma de streaming | Selectbox | ✅ |
| ¿Escucha mientras trabaja? | Selectbox | ✅ |
| ¿Toca algún instrumento? | Selectbox | ✅ |
| ¿Compone música? | Selectbox | ✅ |
| ¿Le gusta descubrir música nueva? | Selectbox | ✅ |

### Paso 2 — Cómo te sientes

| Campo | Tipo | Obligatorio |
|-------|------|-------------|
| Ansiedad | Slider (0–10) | ✅ |
| Desánimo / Depresión | Slider (0–10) | ✅ |
| Pensamientos repetitivos (TOC) | Slider (0–10) | ✅ |

### Paso 3 — Tu música

| Campo | Tipo | Obligatorio |
|-------|------|-------------|
| Género favorito | Selectbox (16 opciones) | ✅ |
| Frecuencia: Pop, Rock, Latin, Lofi, Rap, Hip hop, Jazz, Classical | Selectbox × 8 | ✅ |
| Frecuencia: Country, EDM, Folk, Gospel, K-pop, Metal, R&B, Video game | Selectbox × 8 | ❌ (opcional) |

---

## Variables del Modelo

El modelo trabaja con el siguiente conjunto de características tras el preprocesamiento:

### Numéricas (normalizadas con MinMaxScaler)

- `Age`
- `Hours per day`
- `Anxiety`
- `Depression`
- `OCD`

### Categóricas binarias (One-Hot, drop_first)

- `While working` → Yes / No
- `Instrumentalist` → Yes / No
- `Composer` → Yes / No
- `Exploratory` → Yes / No

### Frecuencias de géneros (One-Hot, sin drop)

Para cada uno de los 16 géneros (`Classical`, `Country`, `EDM`, `Folk`, `Gospel`, `Hip hop`, `Jazz`, `K pop`, `Latin`, `Lofi`, `Metal`, `Pop`, `R&B`, `Rap`, `Rock`, `Video game music`):
- `Frequency [Género]_Rarely`
- `Frequency [Género]_Sometimes`
- `Frequency [Género]_Very frequently`
- *(Never es la categoría de referencia)*

### Otras categóricas multi-nivel (One-Hot, sin drop)

- `Primary streaming service` (Spotify, YouTube Music, Apple Music, Pandora, Other, None)
- `Fav genre` (16 géneros posibles)

---

## Estructura de Archivos

```
musica-bienestar/
│
├── app.py                  # Aplicación principal de Streamlit
├── modelo-cla.pkl          # Modelo serializado (no incluido en el repo público)
├── requirements.txt        # Dependencias de Python
├── README.md               # Este archivo
│
└── notebooks/              # (Opcional) Notebooks de exploración y entrenamiento
    ├── 01_eda.ipynb
    ├── 02_preprocessing.ipynb
    └── 03_model_training.ipynb
```

> ⚠️ El archivo `modelo-cla.pkl` puede no estar incluido en el repositorio si contiene datos sensibles o supera el límite de tamaño de GitHub. En ese caso, entrénalo con los notebooks incluidos o solicítalo a los autores.

---

## Tecnologías Utilizadas

| Tecnología | Versión recomendada | Uso |
|------------|---------------------|-----|
| Python | ≥ 3.8 | Lenguaje base |
| Streamlit | ≥ 1.30 | Interfaz web interactiva |
| pandas | ≥ 1.5 | Manipulación de datos |
| scikit-learn | ≥ 1.2 | Modelo de ML, preprocesamiento |
| pickle | stdlib | Serialización del modelo |
| Google Fonts | — | Tipografía (DM Serif Display, DM Sans) |

---

## Consideraciones Éticas

- **No es un diagnóstico clínico.** Los resultados son orientativos y no reemplazan la evaluación de un profesional de salud mental.
- **Los datos de salud mental son sensibles.** La aplicación no almacena, registra ni transmite ninguna respuesta del usuario.
- **Sesgos del dataset.** El modelo fue entrenado sobre una encuesta voluntaria con una muestra que puede no ser representativa de todas las poblaciones. Los resultados deben interpretarse con cautela.
- **Variable objetivo simplificada.** Las clases `Worsen` y `No effect` fueron unificadas en `No improve`. Esto puede subestimar casos donde la música tiene un efecto neutro pero no negativo.
- **Uso responsable.** Esta herramienta es educativa. Si el usuario atraviesa una situación de salud mental difícil, se le recomienda buscar apoyo profesional.

---

## Autores

Desarrollado como proyecto académico de ciencia de datos aplicada.

| Nombre | Rol |
|--------|-----|
| **Sebastián Forero Duque** | Desarrollo, modelado y diseño de la aplicación |
| **Santiago Gallego Henao** | Desarrollo, modelado y diseño de la aplicación |

---

*Este proyecto es de carácter académico y orientativo. No tiene fines diagnósticos ni clínicos.*
