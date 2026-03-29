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
    --bg: #f6f7fb;
    --card: #ffffff;
    --text: #18212f;
    --muted: #64748b;
    --line: #e5e7eb;
    --primary: #2563eb;
    --primary-soft: #eff6ff;
    --ok-bg: #ecfdf3;
    --ok-border: #b7ebc6;
    --warn-bg: #fff7ed;
    --warn-border: #fed7aa;
    --radius: 18px;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, header, footer {visibility: hidden;}

.block-container {
    max-width: 860px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

.hero {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 1.6rem;
    margin-bottom: 1rem;
}

.hero h1 {
    margin: 0 0 .5rem 0;
    font-size: 2rem;
    color: var(--text) !important;
}

.hero p {
    margin: 0;
    color: var(--muted) !important;
    line-height: 1.6;
    font-size: 1rem;
}

.pill {
    display: inline-block;
    padding: .35rem .7rem;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary);
    font-size: .78rem;
    font-weight: 600;
    margin-bottom: .8rem;
}

.box {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.box h3 {
    margin: 0 0 .35rem 0;
    font-size: 1.05rem;
}

.box p {
    margin: 0;
    color: var(--muted);
    line-height: 1.55;
}

.result-good, .result-neutral {
    border-radius: 18px;
    padding: 1.2rem;
    border: 1px solid;
    margin-top: 1rem;
}

.result-good {
    background: var(--ok-bg);
    border-color: var(--ok-border);
}

.result-neutral {
    background: var(--warn-bg);
    border-color: var(--warn-border);
}

.result-label {
    font-size: .78rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: var(--muted);
    font-weight: 700;
    margin-bottom: .35rem;
}

.result-main {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
}

.stTabs [data-baseweb="tab-list"] {
    gap: .4rem;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border: 1px solid var(--line);
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
    border-radius: 12px !important;
    border: none !important;
    padding: .85rem 1rem !important;
    font-weight: 700 !important;
}

div[data-testid="stExpander"] {
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    background: #fbfcfe !important;
}

.small-note {
    color: var(--muted);
    font-size: .92rem;
    margin-bottom: .75rem;
}
</style>
""", unsafe_allow_html=True)

# ── Encabezado ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="pill">Predicción orientativa</div>
    <h1>¿La música podría ayudarte a sentirte mejor?</h1>
    <p>Responde unas preguntas sencillas sobre tus hábitos, cómo te has sentido últimamente
    y qué tipo de música escuchas. Al final te mostraremos un resultado fácil de entender.</p>
</div>
""", unsafe_allow_html=True)

st.progress(100 / 3)
st.caption("Completa los 3 pasos y luego haz clic en **Ver resultado**.")

with st.form("form_bienestar_musical"):
    tab1, tab2, tab3 = st.tabs(["1. Sobre ti", "2. Cómo te sientes", "3. Tu música"])

    with tab1:
        st.markdown('<div class="box"><h3>Cuéntanos un poco sobre ti</h3><p>Esta información nos ayuda a entender tu contexto general de escucha.</p></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            Age = st.slider("¿Qué edad tienes?", 10, 89, 22)
            Hours_per_day = st.slider("¿Cuántas horas al día escuchas música?", 0, 24, 3)
            st.caption("Incluye música mientras estudias, trabajas, haces ejercicio o descansas.")
        with col2:
            Primary_streaming = st.selectbox(
                "¿Dónde escuchas música con más frecuencia?",
                [
                    "Spotify",
                    "YouTube Music",
                    "Apple Music",
                    "Pandora",
                    "I do not use a streaming service.",
                    "Other streaming service"
                ]
            )
            While_working = st.selectbox(
                "¿Sueles escuchar música mientras trabajas o estudias?",
                ["Yes", "No"]
            )

        col3, col4, col5 = st.columns(3)
        with col3:
            Instrumentalist = st.selectbox("¿Tocas algún instrumento?", ["Yes", "No"])
        with col4:
            Composer = st.selectbox("¿Compones música?", ["Yes", "No"])
        with col5:
            Exploratory = st.selectbox("¿Te gusta descubrir música nueva?", ["Yes", "No"])

    with tab2:
        st.markdown('<div class="box"><h3>Ahora piensa en cómo te has sentido</h3><p>Usa una escala de 0 a 10. No hace falta que sea exacto; basta con una aproximación honesta.</p></div>', unsafe_allow_html=True)

        col6, col7, col8 = st.columns(3)
        with col6:
            Anxiety = st.slider("Ansiedad", 0, 10, 5)
            st.caption("0 = nada, 10 = muy alta")
        with col7:
            Depression = st.slider("Desánimo o depresión", 0, 10, 3)
            st.caption("0 = nada, 10 = muy alta")
        with col8:
            OCD = st.slider("Pensamientos o rutinas repetitivas (TOC)", 0, 10, 2)
            st.caption("0 = nada, 10 = muy alta")

        st.info("No es un diagnóstico clínico. Solo es una referencia para alimentar el modelo.")

    with tab3:
        st.markdown('<div class="box"><h3>Por último, cuéntanos qué música escuchas</h3><p>Empieza por lo más importante: tu género favorito y los géneros que más escuchas.</p></div>', unsafe_allow_html=True)

        Fav_genre = st.selectbox(
            "¿Cuál es tu género favorito?",
            ["Classical", "Country", "EDM", "Folk", "Gospel", "Hip hop",
             "Jazz", "K pop", "Latin", "Lofi", "Metal", "Pop",
             "R&B", "Rap", "Rock", "Video game music"]
        )

        st.markdown("<div class='small-note'>Marca con qué frecuencia escuchas estos géneros principales.</div>", unsafe_allow_html=True)

        freq_opts = ["Never", "Rarely", "Sometimes", "Very frequently"]

        col9, col10 = st.columns(2)
        with col9:
            f_pop = st.selectbox("Pop", freq_opts, index=2)
            f_rock = st.selectbox("Rock", freq_opts, index=2)
            f_latin = st.selectbox("Latin", freq_opts, index=2)
            f_lofi = st.selectbox("Lofi", freq_opts, index=3)
        with col10:
            f_rap = st.selectbox("Rap", freq_opts, index=2)
            f_hiphop = st.selectbox("Hip hop", freq_opts, index=2)
            f_jazz = st.selectbox("Jazz", freq_opts, index=1)
            f_classical = st.selectbox("Classical", freq_opts, index=1)

        with st.expander("Completar géneros opcionales"):
            st.caption("Solo completa esta parte si quieres afinar más la predicción.")
            col11, col12, col13 = st.columns(3)
            with col11:
                f_country = st.selectbox("Country", freq_opts, index=0)
                f_edm = st.selectbox("EDM", freq_opts, index=2)
                f_folk = st.selectbox("Folk", freq_opts, index=1)
            with col12:
                f_gospel = st.selectbox("Gospel", freq_opts, index=0)
                f_kpop = st.selectbox("K-pop", freq_opts, index=0)
                f_metal = st.selectbox("Metal", freq_opts, index=1)
            with col13:
                f_rnb = st.selectbox("R&B", freq_opts, index=1)
                f_videogame = st.selectbox("Video game music", freq_opts, index=1)

    submitted = st.form_submit_button("Ver resultado")

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

    st.markdown("## Tu resultado")

    if resultado == "Improve":
        st.markdown("""
        <div class="result-good">
            <div class="result-label">Interpretación</div>
            <div class="result-main">Con este perfil, la música podría tener un efecto positivo en tu bienestar.</div>
        </div>
        """, unsafe_allow_html=True)
        st.success("Esto sugiere que tus hábitos musicales se parecen a perfiles donde la música sí aporta una mejora percibida.")
    else:
        st.markdown("""
        <div class="result-neutral">
            <div class="result-label">Interpretación</div>
            <div class="result-main">Con este perfil, no aparece una mejora clara asociada al uso de música.</div>
        </div>
        """, unsafe_allow_html=True)
        st.warning("Esto no significa que la música no ayude nunca; solo que el modelo no detecta una señal positiva fuerte con estas respuestas.")

    st.info("Este resultado es solo orientativo y no reemplaza apoyo profesional en salud mental.")

    with st.expander("Ver datos preparados para el modelo"):
        st.dataframe(data_prep, use_container_width=True, hide_index=True)
