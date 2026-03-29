import pickle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Música & Salud Mental",
    page_icon="🎵",
    layout="centered",
)

filename = "modelo-cla.pkl"

try:
    with open(filename, "rb") as f:
        modelo, min_max_scaler, variables = pickle.load(open(filename, 'rb'))
except Exception as e:
    st.error(f"Error cargando el modelo: {e}")
    st.stop()

# ... tu interfaz ...

if predict:
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

    Y_pred = modelo.predict(data_prep)
    resultado = Y_pred[0]
