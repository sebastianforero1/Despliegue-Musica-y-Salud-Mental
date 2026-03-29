# -*- coding: utf-8 -*-
"""
Despliegue – Predicción de Efectos de la Música en la Salud Mental
Modelo: Random Forest Classifier
"""

import pickle
import numpy as np
import pandas as pd
import streamlit as st

# ── Cargar el modelo ──────────────────────────────────────────────────────────
# Cargamos el modelo
import pickle
filename = 'modelo-cla.pkl'
modelo, min_max_scaler, variables = pickle.load(open(filename, 'rb'))

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Música & Salud Mental",
    page_icon="🎵",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --ink:      #1a1523;
    --muted:    #6e6780;
    --bg:       #faf8f5;
    --surface:  #ffffff;
    --accent:   #7c4dff;
    --accent2:  #e91e8c;
    --ok:       #00897b;
    --warn:     #f57c00;
    --border:   rgba(26,21,35,.10);
    --radius:   14px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: var(--bg) !important;
    color: var(--ink) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 680px !important; padding: 2rem 1.75rem 3.5rem !important; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #1a1523 0%, #2d1b69 55%, #1a1523 100%);
    border-radius: var(--radius);
    padding: 2.25rem 2rem 2rem;
    margin-bottom: 1.75rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 70% 30%, rgba(124,77,255,.35) 0%, transparent 65%),
                radial-gradient(ellipse at 20% 80%, rgba(233,30,140,.20) 0%, transparent 60%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(124,77,255,.25);
    border: 1px solid rgba(124,77,255,.5);
    color: #c4b5fd;
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: .25rem .75rem;
    border-radius: 99px;
    margin-bottom: .75rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.85rem;
    line-height: 1.15;
    color: #fff !important;
    margin: 0 0 .5rem;
}
.hero p {
    font-size: .875rem;
    color: rgba(255,255,255,.6) !important;
    margin: 0;
    line-height: 1.55;
}
.hero-notes {
    position: absolute;
    right: 1.5rem; top: 1.25rem;
    font-size: 2.4rem;
    opacity: .15;
    pointer-events: none;
    letter-spacing: .1em;
}

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem 1.25rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 2px 16px rgba(26,21,35,.04);
}
.card-title {
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 1.1rem;
    display: flex; align-items: center; gap: .4rem;
}

/* ── Labels & inputs ── */
label, .stLabel, div[data-testid="stWidgetLabel"] p {
    font-size: .82rem !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
}
.stSelectbox > div > div,
.stSlider { margin-bottom: 0 !important; }

/* ── Slider accent ── */
div[data-testid="stSlider"] > div > div > div {
    background: rgba(124,77,255,.2) !important;
}
div[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #7c4dff, #e91e8c) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: .7rem 2rem !important;
    font-size: .92rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    cursor: pointer !important;
    letter-spacing: .01em;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: .88 !important; }

/* ── Result ── */
.result-positive {
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border: 1.5px solid #a5d6a7;
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem;
    margin-top: 1.25rem;
    display: flex; align-items: center; gap: 1.1rem;
}
.result-negative {
    background: linear-gradient(135deg, #fce4ec, #fff3e0);
    border: 1.5px solid #f48fb1;
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem;
    margin-top: 1.25rem;
    display: flex; align-items: center; gap: 1.1rem;
}
.result-icon { font-size: 2.2rem; }
.result-label {
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .09em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .2rem;
}
.result-value {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.35rem;
    color: var(--ink);
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid var(--border); margin: 1.4rem 0; }

/* ── Warning box ── */
.stAlert { border-radius: 10px !important; font-size: .84rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-notes">♩ ♪ ♫ ♬</div>
    <div class="hero-badge">🔬 Random Forest Classifier</div>
    <h1>Música & Salud Mental</h1>
    <p>Predice si escuchar música tiene un efecto positivo en tu bienestar mental,<br>
    basado en tus hábitos y géneros favoritos.</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 – Perfil personal
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title"><span>👤</span> Perfil personal</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    Age = st.slider("Edad", min_value=10, max_value=89, value=22, step=1)
    Hours_per_day = st.slider("Horas de música al día", min_value=0, max_value=24, value=3, step=1)
with col2:
    Primary_streaming = st.selectbox(
        "Servicio de streaming principal",
        ["Spotify", "YouTube Music", "Apple Music", "Pandora", "I do not use a streaming service", "Other streaming service"],
    )
    While_working = st.selectbox("¿Escucha mientras trabaja/estudia?", ["Yes", "No"])

col3, col4 = st.columns(2)
with col3:
    Instrumentalist = st.selectbox("¿Toca algún instrumento?", ["Yes", "No"])
    Composer = st.selectbox("¿Compone música?", ["Yes", "No"])
with col4:
    Exploratory = st.selectbox("¿Explora nuevos géneros/artistas?", ["Yes", "No"])

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 – Salud mental
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title"><span>🧠</span> Indicadores de salud mental (0 = nada · 10 = severo)</div>', unsafe_allow_html=True)

col5, col6, col7 = st.columns(3)
with col5:
    Anxiety = st.slider("Ansiedad", 0, 10, 5)
with col6:
    Depression = st.slider("Depresión", 0, 10, 3)
with col7:
    OCD = st.slider("TOC (OCD)", 0, 10, 2)

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 – Frecuencia de géneros
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title"><span>🎵</span> Frecuencia de escucha por género</div>', unsafe_allow_html=True)

freq_opts = ["Never", "Rarely", "Sometimes", "Very frequently"]

col_a, col_b, col_c = st.columns(3)
with col_a:
    f_classical   = st.selectbox("Classical",    freq_opts, index=1)
    f_country     = st.selectbox("Country",      freq_opts, index=0)
    f_edm         = st.selectbox("EDM",          freq_opts, index=2)
    f_folk        = st.selectbox("Folk",         freq_opts, index=1)
    f_gospel      = st.selectbox("Gospel",       freq_opts, index=0)
    f_hiphop      = st.selectbox("Hip hop",      freq_opts, index=2)
with col_b:
    f_jazz        = st.selectbox("Jazz",         freq_opts, index=1)
    f_kpop        = st.selectbox("K-pop",        freq_opts, index=0)
    f_latin       = st.selectbox("Latin",        freq_opts, index=2)
    f_lofi        = st.selectbox("Lofi",         freq_opts, index=3)
    f_metal       = st.selectbox("Metal",        freq_opts, index=1)
    f_pop         = st.selectbox("Pop",          freq_opts, index=2)
with col_c:
    f_rnb         = st.selectbox("R&B",          freq_opts, index=1)
    f_rap         = st.selectbox("Rap",          freq_opts, index=2)
    f_rock        = st.selectbox("Rock",         freq_opts, index=2)
    f_videogame   = st.selectbox("Video game music", freq_opts, index=1)
    Fav_genre     = st.selectbox(
        "Género favorito",
        ["Classical", "Country", "EDM", "Folk", "Gospel", "Hip hop",
         "Jazz", "K pop", "Latin", "Lofi", "Metal", "Pop",
         "R&B", "Rap", "Rock", "Video game music"],
    )

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PREDICCIÓN
# ══════════════════════════════════════════════════════════════════════════════
predict = st.button("🎶  Predecir efecto de la música")

if predict:
    # ── Construir fila de datos ──
    datos = {
        "Age":               Age,
        "Hours per day":     Hours_per_day,
        "Anxiety":           Anxiety,
        "Depression":        Depression,
        "OCD":               OCD,
        "Primary streaming service": Primary_streaming,
        "While working":     While_working,
        "Instrumentalist":   Instrumentalist,
        "Composer":          Composer,
        "Exploratory":       Exploratory,
        "Fav genre":         Fav_genre,
        "Frequency [Classical]":        f_classical,
        "Frequency [Country]":          f_country,
        "Frequency [EDM]":              f_edm,
        "Frequency [Folk]":             f_folk,
        "Frequency [Gospel]":           f_gospel,
        "Frequency [Hip hop]":          f_hiphop,
        "Frequency [Jazz]":             f_jazz,
        "Frequency [K pop]":            f_kpop,
        "Frequency [Latin]":            f_latin,
        "Frequency [Lofi]":             f_lofi,
        "Frequency [Metal]":            f_metal,
        "Frequency [Pop]":              f_pop,
        "Frequency [R&B]":              f_rnb,
        "Frequency [Rap]":              f_rap,
        "Frequency [Rock]":             f_rock,
        "Frequency [Video game music]": f_videogame,
    }

    data_raw = pd.DataFrame([datos])

    # ── Convertir object a category (igual que en entrenamiento) ──
    for col in data_raw.columns:
        if data_raw[col].dtype == "object":
            data_raw[col] = data_raw[col].astype("category")

    # ── Identificar columnas categóricas ──
    target_col = "Music effects"
    cat_cols_all = data_raw.select_dtypes(include=["category", "object"]).columns.tolist()
    binarias      = [c for c in cat_cols_all if data_raw[c].nunique() <= 2]
    multi_nivel   = [c for c in cat_cols_all if data_raw[c].nunique() > 2]

    data_prep = data_raw.copy()

    # get_dummies – binarias drop_first=True, multi-nivel drop_first=False
    if binarias:
        data_prep = pd.get_dummies(data_prep, columns=binarias, drop_first=True, dtype=int)
    if multi_nivel:
        data_prep = pd.get_dummies(data_prep, columns=multi_nivel, drop_first=False, dtype=int)

    # ── Alinear columnas con las del entrenamiento ──
    data_prep = data_prep.reindex(columns=variables, fill_value=0)

    # ── Normalizar numéricas ──
    predictoras_numericas = ["Age", "Hours per day", "Anxiety", "Depression", "OCD"]
    data_prep[predictoras_numericas] = min_max_scaler.transform(data_prep[predictoras_numericas])

    # ── Predicción ──
    Y_pred_enc = model_rf.predict(data_prep)
    Y_pred     = labelencoder.inverse_transform(Y_pred_enc)
    resultado  = Y_pred[0]

    st.markdown("<hr>", unsafe_allow_html=True)

    if resultado == "Improve":
        st.markdown(f"""
        <div class="result-positive">
            <div class="result-icon">🎉</div>
            <div>
                <div class="result-label">Efecto predicho</div>
                <div class="result-value">✅ La música mejora tu bienestar mental</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-negative">
            <div class="result-icon">💭</div>
            <div>
                <div class="result-label">Efecto predicho</div>
                <div class="result-value">➖ Sin efecto positivo detectado</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.warning("⚠️ Este modelo es orientativo. El error estimado en validación cruzada (MAE) puede variar. Consulta a un profesional de salud mental.")

    with st.expander("🔍 Ver datos preparados para el modelo"):
        st.dataframe(data_prep, use_container_width=True, hide_index=True)
