# -*- coding: utf-8 -*-
import pickle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Música & Bienestar",
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
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:          #0d0e12;
    --surface:     #15161c;
    --surface2:    #1d1e27;
    --border:      #2a2b38;
    --border-hi:   #3d3e52;
    --text:        #f0f1f6;
    --muted:       #787a96;
    --accent:      #c8a96e;
    --accent2:     #7c6fcd;
    --green:       #4ade80;
    --green-bg:    #0f2318;
    --warn:        #fb923c;
    --warn-bg:     #1f1108;
    --error:       #f87171;
    --error-bg:    #1f0d0d;
    --radius:      16px;
    --radius-sm:   10px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, header, footer { visibility: hidden; }

.block-container {
    max-width: 820px !important;
    padding-top: 2.5rem !important;
    padding-bottom: 5rem !important;
}

/* ── Hero ── */
.hero {
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    border: 1px solid var(--border-hi);
    padding: 2.8rem 2.4rem 2.2rem;
    margin-bottom: 2rem;
    background: var(--surface);
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 55% at 80% 20%, rgba(124,111,205,.18) 0%, transparent 65%),
        radial-gradient(ellipse 50% 40% at 10% 90%, rgba(200,169,110,.12) 0%, transparent 60%);
    pointer-events: none;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    font-family: 'DM Sans', sans-serif;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(200,169,110,.1);
    border: 1px solid rgba(200,169,110,.25);
    border-radius: 999px;
    padding: .3rem .8rem;
    margin-bottom: 1.1rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.4rem !important;
    line-height: 1.15 !important;
    color: var(--text) !important;
    margin: 0 0 .9rem !important;
}
.hero h1 em {
    font-style: italic;
    color: var(--accent);
}
.hero p {
    font-size: .97rem;
    color: var(--muted);
    line-height: 1.7;
    max-width: 56ch;
    margin: 0;
}

/* ── Progress stepper ── */
.stepper {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 2rem;
}
.step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    position: relative;
}
.step-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: .8rem;
    font-weight: 700;
    border: 2px solid var(--border);
    background: var(--surface);
    color: var(--muted);
    z-index: 1;
    transition: all .3s;
}
.step-circle.active {
    border-color: var(--accent);
    background: rgba(200,169,110,.15);
    color: var(--accent);
}
.step-circle.done {
    border-color: var(--green);
    background: rgba(74,222,128,.12);
    color: var(--green);
}
.step-label {
    margin-top: .35rem;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .05em;
    text-transform: uppercase;
    color: var(--muted);
}
.step-label.active { color: var(--accent); }
.step-label.done   { color: var(--green); }
.step-line {
    flex: 1;
    height: 2px;
    background: var(--border);
    margin-top: -18px;
}
.step-line.done { background: var(--green); }

/* ── Section card ── */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.6rem;
    margin-bottom: 1.5rem;
}
.section-card h3 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    color: var(--text);
    margin: 0 0 .4rem;
}
.section-card p {
    font-size: .88rem;
    color: var(--muted);
    margin: 0;
    line-height: 1.6;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.2rem 0;
}

/* ── Validation banner ── */
.val-banner {
    background: var(--error-bg);
    border: 1px solid var(--error);
    border-radius: var(--radius-sm);
    padding: .9rem 1.1rem;
    margin-bottom: 1.2rem;
    font-size: .9rem;
    color: var(--error);
    display: flex;
    gap: .6rem;
    align-items: flex-start;
}
.val-banner ul {
    margin: .3rem 0 0 .5rem;
    padding: 0;
    list-style: none;
    color: #fca5a5;
    font-size: .85rem;
}
.val-banner ul li::before { content: "→ "; }

/* ── Result cards ── */
.result-wrap {
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}
.result-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    opacity: .6;
    pointer-events: none;
}
.result-good {
    background: var(--green-bg);
    border-color: rgba(74,222,128,.3);
}
.result-good::before {
    background: radial-gradient(ellipse 60% 50% at 90% 10%, rgba(74,222,128,.2) 0%, transparent 70%);
}
.result-neutral {
    background: var(--warn-bg);
    border-color: rgba(251,146,60,.3);
}
.result-neutral::before {
    background: radial-gradient(ellipse 60% 50% at 90% 10%, rgba(251,146,60,.2) 0%, transparent 70%);
}
.result-badge {
    display: inline-block;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    border-radius: 999px;
    padding: .25rem .75rem;
    margin-bottom: .9rem;
}
.result-good .result-badge   { background: rgba(74,222,128,.15); color: var(--green); }
.result-neutral .result-badge { background: rgba(251,146,60,.15); color: var(--warn); }
.result-icon {
    font-size: 2.4rem;
    margin-bottom: .6rem;
    display: block;
}
.result-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--text);
    margin: 0 0 .6rem;
    line-height: 1.25;
}
.result-body {
    font-size: .92rem;
    color: var(--muted);
    line-height: 1.65;
    max-width: 52ch;
}
.disclaimer {
    margin-top: 1.2rem;
    padding: .9rem 1.1rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: .82rem;
    color: var(--muted);
    line-height: 1.55;
}

/* ── Streamlit component overrides ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: .4rem;
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px 10px 0 0 !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
    padding: .6rem 1rem !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: var(--surface2) !important;
    border-color: var(--border) var(--border) var(--surface2) !important;
    color: var(--accent) !important;
}

.stSlider [data-baseweb="slider"] { padding: .3rem 0; }

.stSelectbox label, .stSlider label {
    font-size: .85rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    margin-bottom: .15rem !important;
}

.stFormSubmitButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #c8a96e, #b8894e) !important;
    color: #0d0e12 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: .9rem 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: .02em !important;
    cursor: pointer !important;
    transition: opacity .2s !important;
}
.stFormSubmitButton > button:hover { opacity: .9 !important; }

div[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    background: var(--surface2) !important;
}

.stInfo, .stSuccess, .stWarning {
    border-radius: 10px !important;
    font-size: .88rem !important;
}

/* Caption overrides */
.stCaption { color: var(--muted) !important; font-size: .78rem !important; }

/* Number badge for required hint */
.req-note {
    font-size: .78rem;
    color: var(--muted);
    margin-bottom: 1rem;
}
.req-note span {
    color: var(--error);
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ── Encabezado ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">🎵 Predicción orientativa</div>
    <h1>¿La música puede<br><em>mejorar tu bienestar?</em></h1>
    <p>Responde unas preguntas sobre tus hábitos, cómo te has sentido últimamente
    y qué tipo de música escuchas. Al final verás un resultado fácil de interpretar.</p>
</div>
""", unsafe_allow_html=True)

# ── Inicializar estado ────────────────────────────────────────────────────────
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "validation_errors" not in st.session_state:
    st.session_state.validation_errors = []

# ── Formulario ────────────────────────────────────────────────────────────────
with st.form("form_bienestar_musical"):

    tab1, tab2, tab3 = st.tabs(["👤 Sobre ti", "💭 Cómo te sientes", "🎶 Tu música"])

    # ── TAB 1 ─────────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("""
        <div class="section-card">
            <h3>Cuéntanos sobre ti</h3>
            <p>Esta información nos ayuda a entender tu contexto general de escucha musical.</p>
        </div>
        <p class="req-note">Los campos marcados con <span>*</span> son obligatorios.</p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            Age = st.slider("Edad *", 10, 89, 22)
            Hours_per_day = st.slider("Horas al día que escuchas música *", 0, 24, 3)
            st.caption("Incluye música mientras estudias, trabajas, haces ejercicio o descansas.")
        with col2:
            Primary_streaming = st.selectbox(
                "Plataforma principal *",
                ["— Selecciona una opción —", "Spotify", "YouTube Music", "Apple Music",
                 "Pandora", "I do not use a streaming service.", "Other streaming service"]
            )
            While_working = st.selectbox(
                "¿Escuchas música mientras trabajas o estudias? *",
                ["— Selecciona una opción —", "Yes", "No"]
            )

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        col3, col4, col5 = st.columns(3)
        with col3:
            Instrumentalist = st.selectbox(
                "¿Tocas algún instrumento? *",
                ["— Selecciona una opción —", "Yes", "No"]
            )
        with col4:
            Composer = st.selectbox(
                "¿Compones música? *",
                ["— Selecciona una opción —", "Yes", "No"]
            )
        with col5:
            Exploratory = st.selectbox(
                "¿Te gusta descubrir música nueva? *",
                ["— Selecciona una opción —", "Yes", "No"]
            )

    # ── TAB 2 ─────────────────────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div class="section-card">
            <h3>¿Cómo te has sentido últimamente?</h3>
            <p>Usa una escala de 0 a 10. No hace falta que sea exacto; una aproximación honesta es suficiente.</p>
        </div>
        """, unsafe_allow_html=True)

        col6, col7, col8 = st.columns(3)
        with col6:
            Anxiety = st.slider("Ansiedad *", 0, 10, 5)
            st.caption("0 = nada · 10 = muy alta")
        with col7:
            Depression = st.slider("Desánimo / Depresión *", 0, 10, 3)
            st.caption("0 = nada · 10 = muy alta")
        with col8:
            OCD = st.slider("Pensamientos repetitivos (TOC) *", 0, 10, 2)
            st.caption("0 = nada · 10 = muy alta")

        st.info("ℹ️ Esto no es un diagnóstico clínico. Solo es una referencia para el modelo predictivo.")

    # ── TAB 3 ─────────────────────────────────────────────────────────────────
    with tab3:
        st.markdown("""
        <div class="section-card">
            <h3>¿Qué música escuchas?</h3>
            <p>Elige tu género favorito y con qué frecuencia escuchas los géneros principales.</p>
        </div>
        """, unsafe_allow_html=True)

        Fav_genre = st.selectbox(
            "¿Cuál es tu género favorito? *",
            ["— Selecciona un género —", "Classical", "Country", "EDM", "Folk", "Gospel",
             "Hip hop", "Jazz", "K pop", "Latin", "Lofi", "Metal", "Pop", "R&B",
             "Rap", "Rock", "Video game music"]
        )

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("**Frecuencia de escucha por género** — Géneros principales *")

        freq_opts = ["— Selecciona —", "Never", "Rarely", "Sometimes", "Very frequently"]

        col9, col10 = st.columns(2)
        with col9:
            f_pop      = st.selectbox("Pop *", freq_opts)
            f_rock     = st.selectbox("Rock *", freq_opts)
            f_latin    = st.selectbox("Latin *", freq_opts)
            f_lofi     = st.selectbox("Lofi *", freq_opts)
        with col10:
            f_rap      = st.selectbox("Rap *", freq_opts)
            f_hiphop   = st.selectbox("Hip hop *", freq_opts)
            f_jazz     = st.selectbox("Jazz *", freq_opts)
            f_classical = st.selectbox("Classical *", freq_opts)

        with st.expander("🎸 Géneros opcionales (mejoran la precisión)"):
            st.caption("Puedes dejarlos en blanco; se asignará 'Never' automáticamente.")
            col11, col12, col13 = st.columns(3)
            with col11:
                f_country = st.selectbox("Country", freq_opts, index=1)
                f_edm     = st.selectbox("EDM",     freq_opts, index=3)
                f_folk    = st.selectbox("Folk",    freq_opts, index=2)
            with col12:
                f_gospel  = st.selectbox("Gospel",  freq_opts, index=1)
                f_kpop    = st.selectbox("K-pop",   freq_opts, index=1)
                f_metal   = st.selectbox("Metal",   freq_opts, index=2)
            with col13:
                f_rnb     = st.selectbox("R&B",     freq_opts, index=2)
                f_videogame = st.selectbox("Video game music", freq_opts, index=2)

    # ── Botón ─────────────────────────────────────────────────────────────────
    submitted = st.form_submit_button("🎵 Ver mi resultado")

# ── Validación y predicción ───────────────────────────────────────────────────
PLACEHOLDER = "— Selecciona"

if submitted:
    errors = []

    # Tab 1
    if Primary_streaming.startswith(PLACEHOLDER):
        errors.append("Plataforma de streaming (pestaña «Sobre ti»)")
    if While_working.startswith(PLACEHOLDER):
        errors.append("Escucha mientras trabajas (pestaña «Sobre ti»)")
    if Instrumentalist.startswith(PLACEHOLDER):
        errors.append("¿Tocas algún instrumento? (pestaña «Sobre ti»)")
    if Composer.startswith(PLACEHOLDER):
        errors.append("¿Compones música? (pestaña «Sobre ti»)")
    if Exploratory.startswith(PLACEHOLDER):
        errors.append("¿Te gusta descubrir música nueva? (pestaña «Sobre ti»)")

    # Tab 3
    if Fav_genre.startswith(PLACEHOLDER):
        errors.append("Género favorito (pestaña «Tu música»)")
    freq_required = {
        "Pop": f_pop, "Rock": f_rock, "Latin": f_latin, "Lofi": f_lofi,
        "Rap": f_rap, "Hip hop": f_hiphop, "Jazz": f_jazz, "Classical": f_classical,
    }
    missing_freq = [k for k, v in freq_required.items() if v.startswith(PLACEHOLDER)]
    if missing_freq:
        errors.append(f"Frecuencia de escucha para: {', '.join(missing_freq)} (pestaña «Tu música»)")

    if errors:
        items = "".join(f"<li>{e}</li>" for e in errors)
        st.markdown(f"""
        <div class="val-banner">
            <div>
                <strong>⚠️ Faltan {len(errors)} campo(s) obligatorio(s)</strong>
                <ul>{items}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Normalizar opcionales que quedaron en placeholder → "Never"
        def clean_freq(val):
            return val if not val.startswith(PLACEHOLDER) else "Never"

        f_country   = clean_freq(f_country)
        f_edm       = clean_freq(f_edm)
        f_folk      = clean_freq(f_folk)
        f_gospel    = clean_freq(f_gospel)
        f_kpop      = clean_freq(f_kpop)
        f_metal     = clean_freq(f_metal)
        f_rnb       = clean_freq(f_rnb)
        f_videogame = clean_freq(f_videogame)

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
        binarias     = [c for c in cat_cols_all if data_raw[c].nunique() <= 2]
        multi_nivel  = [c for c in cat_cols_all if data_raw[c].nunique() > 2]

        data_prep = data_raw.copy()
        if binarias:
            data_prep = pd.get_dummies(data_prep, columns=binarias, drop_first=True, dtype=int)
        if multi_nivel:
            data_prep = pd.get_dummies(data_prep, columns=multi_nivel, drop_first=False, dtype=int)

        data_prep = data_prep.reindex(columns=variables, fill_value=0)

        predictoras_numericas = ["Age", "Hours per day", "Anxiety", "Depression", "OCD"]
        data_prep[predictoras_numericas] = min_max_scaler.transform(data_prep[predictoras_numericas])

        Y_pred_enc = modelo.predict(data_prep)
        Y_pred     = labelencoder.inverse_transform(Y_pred_enc)
        resultado  = Y_pred[0]

        st.markdown("## Tu resultado")

        if resultado == "Improve":
            st.markdown("""
            <div class="result-wrap result-good">
                <span class="result-icon">🎧</span>
                <div class="result-badge">Señal positiva detectada</div>
                <p class="result-title">La música podría tener un efecto positivo en tu bienestar.</p>
                <p class="result-body">
                    Tus hábitos musicales se parecen a los de perfiles donde la música
                    sí aporta una mejora percibida en el bienestar emocional.
                    Seguir escuchando música con intención puede ser beneficioso para ti.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-wrap result-neutral">
                <span class="result-icon">🔍</span>
                <div class="result-badge">Sin señal clara</div>
                <p class="result-title">No se detecta una mejora clara asociada a tu perfil musical.</p>
                <p class="result-body">
                    Esto no significa que la música no ayude; solo que el modelo no encuentra
                    una señal positiva fuerte con estas respuestas. Explorar nuevos géneros,
                    contextos de escucha o hábitos podría cambiar este resultado.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer">
            ⚕️ <strong>Aviso importante:</strong> Este resultado es solo orientativo y no reemplaza
            el apoyo de un profesional en salud mental. Si estás pasando por un momento difícil,
            considera consultar con un especialista.
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔬 Ver datos preparados para el modelo"):
            st.dataframe(data_prep, use_container_width=True, hide_index=True)
