# -*- coding: utf-8 -*-
import pickle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Música & Salud Mental",
    page_icon="🎵",
    layout="centered",
)

# ── Cargar modelo ─────────────────────────────────────────────────────────────
filename = "modelo-cla.pkl"

try:
    with open(filename, "rb") as f:
        modelo, labelencoder, variables, min_max_scaler = pickle.load(f)
except FileNotFoundError:
    st.error("No se encontró el archivo 'modelo-cla.pkl'.")
    st.stop()
except ModuleNotFoundError as e:
    st.error(f"Falta una dependencia para cargar el modelo: {e}")
    st.stop()
except Exception as e:
    st.error(f"Error cargando el modelo: {e}")
    st.stop()

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap');

:root{
    --bg:#f7f4ef;
    --card:#ffffff;
    --ink:#1f1728;
    --muted:#6f667c;
    --line:#e8e1d8;
    --accent:#6c4cf1;
    --accent-soft:#efeaff;
    --success-bg:#eaf7ee;
    --success-bd:#b8e0c2;
    --danger-bg:#fff1f3;
    --danger-bd:#f5b7c2;
    --radius:16px;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--ink) !important;
}

#MainMenu, header, footer {visibility:hidden;}
.block-container{
    max-width: 820px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

.hero {
    background: #171221;
    color: white;
    border-radius: 24px;
    padding: 1.8rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,.06);
}
.hero h1{
    font-family: 'DM Serif Display', serif !important;
    font-size: 2rem;
    margin: 0 0 .4rem 0;
    color: white !important;
}
.hero p{
    color: rgba(255,255,255,.72) !important;
    margin: 0;
    line-height: 1.55;
}
.badge {
    display:inline-block;
    padding:.35rem .7rem;
    border-radius:999px;
    background: rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.12);
    font-size:.75rem;
    margin-bottom:.8rem;
}

.section-card{
    background: var(--card);
    border:1px solid var(--line);
    border-radius: var(--radius);
    padding: 1.25rem 1.25rem 1rem 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(26,21,35,.04);
}

.section-title{
    font-size:.82rem;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:.08em;
    color: var(--muted);
    margin-bottom: .9rem;
}

.helper {
    color: var(--muted);
    font-size: .93rem;
    margin: .25rem 0 0 0;
}

.result-ok, .result-no {
    border-radius: 18px;
    padding: 1.2rem 1.2rem;
    margin: 1rem 0 1rem 0;
    border: 1px solid;
}
.result-ok{
    background: var(--success-bg);
    border-color: var(--success-bd);
}
.result-no{
    background: var(--danger-bg);
    border-color: var(--danger-bd);
}
.result-title{
    font-size:.78rem;
    text-transform:uppercase;
    letter-spacing:.08em;
    color: var(--muted);
    font-weight:700;
    margin-bottom:.35rem;
}
.result-text{
    font-size:1.2rem;
    font-weight:700;
    color: var(--ink);
}

.stButton > button, .stFormSubmitButton > button {
    width: 100% !important;
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .85rem 1rem !important;
    font-weight: 700 !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    opacity: .92;
}

div[data-testid="stExpander"]{
    border:1px solid var(--line) !important;
    border-radius: 14px !important;
    background: #fcfbf9 !important;
}

label, .stLabel, div[data-testid="stWidgetLabel"] p{
    font-weight:600 !important;
    color: var(--ink) !important;
}

hr{
    border:none;
    border-top:1px solid var(--line);
    margin:1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">Predicción con Random Forest</div>
    <h1>Música y salud mental</h1>
    <p>Completa tu perfil, tus indicadores de bienestar y tus preferencias musicales.
    Al final recibirás una predicción orientativa sobre el efecto de la música en tu bienestar mental.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<p class='helper'>Consejo: deja los valores sugeridos si solo quieres probar la app rápidamente.</p>", unsafe_allow_html=True)

with st.form("music_mental_health_form"):
    st.markdown('<div class="section-card"><div class="section-title">Perfil personal</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        Age = st.slider("Edad", 10, 89, 22)
        Hours_per_day = st.slider("Horas de música al día", 0, 24, 3)
    with col2:
        Primary_streaming = st.selectbox(
            "Servicio de streaming principal",
            ["Spotify", "YouTube Music", "Apple Music", "Pandora",
             "I do not use a streaming service.", "Other streaming service"]
        )
        While_working = st.selectbox("¿Escucha música mientras trabaja o estudia?", ["Yes", "No"])

    col3, col4 = st.columns(2)
    with col3:
        Instrumentalist = st.selectbox("¿Toca algún instrumento?", ["Yes", "No"])
    with col4:
        Composer = st.selectbox("¿Compone música?", ["Yes", "No"])

    Exploratory = st.selectbox("¿Explora nuevos géneros o artistas?", ["Yes", "No"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">Bienestar emocional</div>', unsafe_allow_html=True)
    st.markdown("<p class='helper'>Usa una escala de 0 a 10, donde 0 es nada y 10 es muy alto.</p>", unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    with col5:
        Anxiety = st.slider("Ansiedad", 0, 10, 5)
    with col6:
        Depression = st.slider("Depresión", 0, 10, 3)
    with col7:
        OCD = st.slider("TOC", 0, 10, 2)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">Preferencias musicales</div>', unsafe_allow_html=True)
    Fav_genre = st.selectbox(
        "Género favorito",
        ["Classical", "Country", "EDM", "Folk", "Gospel", "Hip hop",
         "Jazz", "K pop", "Latin", "Lofi", "Metal", "Pop",
         "R&B", "Rap", "Rock", "Video game music"]
    )

    st.markdown("<p class='helper'>Primero completa los géneros principales. Si quieres más detalle, abre la sección avanzada.</p>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    freq_opts = ["Never", "Rarely", "Sometimes", "Very frequently"]

    with col_a:
        f_pop   = st.selectbox("Pop", freq_opts, index=2)
        f_rock  = st.selectbox("Rock", freq_opts, index=2)
        f_latin = st.selectbox("Latin", freq_opts, index=2)
        f_rap   = st.selectbox("Rap", freq_opts, index=2)

    with col_b:
        f_lofi  = st.selectbox("Lofi", freq_opts, index=3)
        f_hiphop = st.selectbox("Hip hop", freq_opts, index=2)
        f_jazz  = st.selectbox("Jazz", freq_opts, index=1)
        f_classical = st.selectbox("Classical", freq_opts, index=1)

    with st.expander("Opciones avanzadas de géneros"):
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            f_country = st.selectbox("Country", freq_opts, index=0)
            f_edm = st.selectbox("EDM", freq_opts, index=2)
            f_folk = st.selectbox("Folk", freq_opts, index=1)
        with col_c2:
            f_gospel = st.selectbox("Gospel", freq_opts, index=0)
            f_kpop = st.selectbox("K-pop", freq_opts, index=0)
            f_metal = st.selectbox("Metal", freq_opts, index=1)
        with col_c3:
            f_rnb = st.selectbox("R&B", freq_opts, index=1)
            f_videogame = st.selectbox("Video game music", freq_opts, index=1)

    st.markdown("</div>", unsafe_allow_html=True)

    submitted = st.form_submit_button("Predecir efecto de la música")

if submitted:
    datos = {
        "Age": Age,
        "Hours per day": Hours_per_day,
        "Anxiety": Anxiety,
        "Depression": Depression,
        "OCD": OCD,
        "Primary streaming service": Primary_streaming,
        "While working": While_working,
        "Instrumentalist": Instrumentalist,
        "Composer": Composer,
        "Exploratory": Exploratory,
        "Fav genre": Fav_genre,
        "Frequency [Classical]": f_classical,
        "Frequency [Country]": f_country,
        "Frequency [EDM]": f_edm,
        "Frequency [Folk]": f_folk,
        "Frequency [Gospel]": f_gospel,
        "Frequency [Hip hop]": f_hiphop,
        "Frequency [Jazz]": f_jazz,
        "Frequency [K pop]": f_kpop,
        "Frequency [Latin]": f_latin,
        "Frequency [Lofi]": f_lofi,
        "Frequency [Metal]": f_metal,
        "Frequency [Pop]": f_pop,
        "Frequency [R&B]": f_rnb,
        "Frequency [Rap]": f_rap,
        "Frequency [Rock]": f_rock,
        "Frequency [Video game music]": f_videogame,
    }

    data_raw = pd.DataFrame([datos])

    for col in data_raw.columns:
        if data_raw[col].dtype == "object":
            data_raw[col] = data_raw[col].astype("category")

    cat_cols_all = data_raw.select_dtypes(include=["category", "object"]).columns.tolist()
    binarias = [c for c in cat_cols_all if data_raw[c].nunique() <= 2]
    multi_nivel = [c for c in cat_cols_all if data_raw[c].nunique() > 2]

    data_prep = data_raw.copy()

    if binarias:
        data_prep = pd.get_dummies(data_prep, columns=binarias, drop_first=True, dtype=int)
    if multi_nivel:
        data_prep = pd.get_dummies(data_prep, columns=multi_nivel, drop_first=False, dtype=int)

    data_prep = data_prep.reindex(columns=variables, fill_value=0)

    predictoras_numericas = ["Age", "Hours per day", "Anxiety", "Depression", "OCD"]
    data_prep[predictoras_numericas] = min_max_scaler.transform(data_prep[predictoras_numericas])

    Y_pred_enc = modelo.predict(data_prep)
    Y_pred = labelencoder.inverse_transform(Y_pred_enc)
    resultado = Y_pred[0]

    if resultado == "Improve":
        st.markdown("""
        <div class="result-ok">
            <div class="result-title">Resultado</div>
            <div class="result-text">La música probablemente tenga un efecto positivo en tu bienestar mental</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-no">
            <div class="result-title">Resultado</div>
            <div class="result-text">No se detecta un efecto positivo claro con este perfil</div>
        </div>
        """, unsafe_allow_html=True)

    st.info("Este resultado es orientativo y no sustituye la evaluación de un profesional de salud mental.")

    with st.expander("Ver datos preparados para el modelo"):
        st.dataframe(data_prep, use_container_width=True, hide_index=True)
