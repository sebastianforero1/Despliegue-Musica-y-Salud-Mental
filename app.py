# -*- coding: utf-8 -*-
import pickle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Música y bienestar",
    page_icon="🎧",
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #f5f7fb;
    --card: #ffffff;
    --text: #111827;
    --muted: #6b7280;
    --border: #dbe2ea;
    --primary: #1d4ed8;
    --primary-soft: #eff6ff;
    --danger-bg: #fef2f2;
    --danger-border: #fecaca;
    --danger-text: #991b1b;
    --success-bg: #ecfdf5;
    --success-border: #bbf7d0;
    --success-text: #166534;
    --warn-bg: #fff7ed;
    --warn-border: #fed7aa;
    --warn-text: #9a3412;
    --radius: 18px;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, header, footer { visibility: hidden; }

.block-container {
    max-width: 860px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

.hero {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.6rem;
    margin-bottom: 1rem;
}

.hero h1 {
    margin: 0 0 .4rem 0;
    font-size: 2rem;
    color: var(--text) !important;
}

.hero p {
    margin: 0;
    color: var(--muted) !important;
    line-height: 1.6;
    font-size: 1rem;
}

.badge {
    display: inline-block;
    padding: .35rem .7rem;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary);
    font-size: .78rem;
    font-weight: 600;
    margin-bottom: .8rem;
}

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem;
    margin-bottom: 1rem;
}

.card h3 {
    margin: 0 0 .35rem 0;
    font-size: 1.05rem;
}

.card p {
    margin: 0;
    color: var(--muted);
    line-height: 1.55;
}

.section-note {
    color: var(--muted);
    font-size: .92rem;
    margin-top: .25rem;
}

.result-good, .result-neutral {
    border-radius: 18px;
    padding: 1.2rem;
    margin-top: 1rem;
    border: 1px solid;
}
.result-good {
    background: var(--success-bg);
    border-color: var(--success-border);
}
.result-neutral {
    background: var(--warn-bg);
    border-color: var(--warn-border);
}
.result-label {
    font-size: .78rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    font-weight: 700;
    color: var(--muted);
    margin-bottom: .35rem;
}
.result-text {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
}

.stTabs [data-baseweb="tab-list"] {
    gap: .45rem;
}
.stTabs [data-baseweb="tab"] {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: .6rem .9rem;
}
.stTabs [aria-selected="true"] {
    background: var(--primary-soft) !important;
    color: var(--primary) !important;
    border-color: #bfdbfe !important;
}

.stFormSubmitButton > button {
    width: 100% !important;
    background: var(--primary) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .9rem 1rem !important;
    font-weight: 700 !important;
}

div[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    background: #fafcff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Opciones base ─────────────────────────────────────────────────────────────
placeholder = "Selecciona una opción"
yes_no = [placeholder, "Yes", "No"]
streaming_options = [
    placeholder,
    "Spotify",
    "YouTube Music",
    "Apple Music",
    "Pandora",
    "I do not use a streaming service.",
    "Other streaming service"
]
genre_options = [
    placeholder,
    "Classical", "Country", "EDM", "Folk", "Gospel", "Hip hop",
    "Jazz", "K pop", "Latin", "Lofi", "Metal", "Pop",
    "R&B", "Rap", "Rock", "Video game music"
]

# ── Encabezado ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">Predicción orientativa</div>
    <h1>Música y bienestar emocional</h1>
    <p>Responde las 3 secciones completas. Cuando termines, podrás obtener una predicción
    sobre si la música podría tener un efecto positivo en tu bienestar.</p>
</div>
""", unsafe_allow_html=True)

st.progress(33, text="Completa las 3 secciones antes de continuar")

with st.form("form_musica_bienestar"):
    tab1, tab2, tab3 = st.tabs(["1. Sobre ti", "2. Cómo te sientes", "3. Tu música"])

    with tab1:
        st.markdown("""
        <div class="card">
            <h3>Información personal</h3>
            <p>Completa estos datos básicos para describir tus hábitos generales.</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            Age = st.slider("Edad", 10, 89, 22)
            Hours_per_day = st.slider("Horas al día escuchando música", 0, 24, 3)
        with col2:
            Primary_streaming = st.selectbox("Servicio principal de música", streaming_options, index=0)
            While_working = st.selectbox("¿Escuchas música mientras trabajas o estudias?", yes_no, index=0)

        col3, col4, col5 = st.columns(3)
        with col3:
            Instrumentalist = st.selectbox("¿Tocas un instrumento?", yes_no, index=0)
        with col4:
            Composer = st.selectbox("¿Compones música?", yes_no, index=0)
        with col5:
            Exploratory = st.selectbox("¿Te gusta descubrir música nueva?", yes_no, index=0)

    with tab2:
        st.markdown("""
        <div class="card">
            <h3>Cómo te has sentido últimamente</h3>
            <p>Usa una escala de 0 a 10. No hace falta ser exacto; basta con una aproximación.</p>
        </div>
        """, unsafe_allow_html=True)

        col6, col7, col8 = st.columns(3)
        with col6:
            Anxiety = st.slider("Ansiedad", 0, 10, 0)
        with col7:
            Depression = st.slider("Desánimo o depresión", 0, 10, 0)
        with col8:
            OCD = st.slider("Pensamientos repetitivos (TOC)", 0, 10, 0)

        mental_check = st.checkbox("Confirmo que revisé y completé esta sección")

    with tab3:
        st.markdown("""
        <div class="card">
            <h3>Tu relación con la música</h3>
            <p>Selecciona tu género favorito y la frecuencia con que escuchas algunos géneros principales.</p>
        </div>
        """, unsafe_allow_html=True)

        Fav_genre = st.selectbox("Género favorito", genre_options, index=0)

        freq_opts = [placeholder, "Never", "Rarely", "Sometimes", "Very frequently"]

        col9, col10 = st.columns(2)
        with col9:
            f_pop = st.selectbox("Pop", freq_opts, index=0)
            f_rock = st.selectbox("Rock", freq_opts, index=0)
            f_latin = st.selectbox("Latin", freq_opts, index=0)
            f_lofi = st.selectbox("Lofi", freq_opts, index=0)
        with col10:
            f_rap = st.selectbox("Rap", freq_opts, index=0)
            f_hiphop = st.selectbox("Hip hop", freq_opts, index=0)
            f_jazz = st.selectbox("Jazz", freq_opts, index=0)
            f_classical = st.selectbox("Classical", freq_opts, index=0)

        with st.expander("Géneros opcionales"):
            col11, col12, col13 = st.columns(3)
            with col11:
                f_country = st.selectbox("Country", freq_opts, index=0)
                f_edm = st.selectbox("EDM", freq_opts, index=0)
                f_folk = st.selectbox("Folk", freq_opts, index=0)
            with col12:
                f_gospel = st.selectbox("Gospel", freq_opts, index=0)
                f_kpop = st.selectbox("K-pop", freq_opts, index=0)
                f_metal = st.selectbox("Metal", freq_opts, index=0)
            with col13:
                f_rnb = st.selectbox("R&B", freq_opts, index=0)
                f_videogame = st.selectbox("Video game music", freq_opts, index=0)

        music_check = st.checkbox("Confirmo que revisé y completé esta sección")

    submitted = st.form_submit_button("Predecir resultado")

if submitted:
    errores = []

    # Validaciones sección 1
    if Primary_streaming == placeholder:
        errores.append("Selecciona tu servicio principal de música.")
    if While_working == placeholder:
        errores.append("Indica si escuchas música mientras trabajas o estudias.")
    if Instrumentalist == placeholder:
        errores.append("Indica si tocas un instrumento.")
    if Composer == placeholder:
        errores.append("Indica si compones música.")
    if Exploratory == placeholder:
        errores.append("Indica si te gusta descubrir música nueva.")

    # Validaciones sección 2
    if not mental_check:
        errores.append("Confirma la sección 'Cómo te sientes'.")

    # Validaciones sección 3
    if Fav_genre == placeholder:
        errores.append("Selecciona tu género favorito.")
    if f_pop == placeholder:
        errores.append("Completa la frecuencia de escucha de Pop.")
    if f_rock == placeholder:
        errores.append("Completa la frecuencia de escucha de Rock.")
    if f_latin == placeholder:
        errores.append("Completa la frecuencia de escucha de Latin.")
    if f_lofi == placeholder:
        errores.append("Completa la frecuencia de escucha de Lofi.")
    if f_rap == placeholder:
        errores.append("Completa la frecuencia de escucha de Rap.")
    if f_hiphop == placeholder:
        errores.append("Completa la frecuencia de escucha de Hip hop.")
    if f_jazz == placeholder:
        errores.append("Completa la frecuencia de escucha de Jazz.")
    if f_classical == placeholder:
        errores.append("Completa la frecuencia de escucha de Classical.")
    if not music_check:
        errores.append("Confirma la sección 'Tu música'.")

    if errores:
        st.error("No puedes predecir todavía. Revisa los siguientes campos obligatorios:")
        for e in errores:
            st.markdown(f"- {e}")
        st.stop()

    # Completar opcionales vacíos con 'Never'
    def fill_optional(value):
        return "Never" if value == placeholder else value

    f_country = fill_optional(f_country)
    f_edm = fill_optional(f_edm)
    f_folk = fill_optional(f_folk)
    f_gospel = fill_optional(f_gospel)
    f_kpop = fill_optional(f_kpop)
    f_metal = fill_optional(f_metal)
    f_rnb = fill_optional(f_rnb)
    f_videogame = fill_optional(f_videogame)

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

    st.markdown("## Resultado")

    if resultado == "Improve":
        st.markdown("""
        <div class="result-good">
            <div class="result-label">Predicción</div>
            <div class="result-text">La música podría tener un efecto positivo en tu bienestar.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-neutral">
            <div class="result-label">Predicción</div>
            <div class="result-text">No se observa un efecto positivo claro con este perfil.</div>
        </div>
        """, unsafe_allow_html=True)

    st.info("Este resultado es orientativo y no reemplaza la evaluación de un profesional de salud mental.")

    with st.expander("Ver datos preparados para el modelo"):
        st.dataframe(data_prep, use_container_width=True, hide_index=True)
