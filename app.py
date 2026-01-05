from dotenv import load_dotenv
load_dotenv()

import streamlit as st

st.set_page_config(page_title="Atitude Social", layout="wide")

from utils.auth import require_pin

require_pin(
    app_name="Atitude Stock - Igreja",
    logo_path="assets/logo.png",
    version="v1.0.0",
    whatsapp="21994391902",
    developer="Diogo Silva",
    header_top_padding=40,
    actions_top_padding=16
)

# ✅ CSS GLOBAL — aplica em TODAS AS PÁGINAS
st.markdown("""
<style>

/* ✅ Max largura real no desktop */
@media (min-width: 900px) {
    .main .block-container {
        max-width: 1750px !important;   /* ✅ mais largo que antes */
        padding-left: 4rem !important;
        padding-right: 4rem !important;
        padding-top: 2.0rem !important;
        padding-bottom: 2.0rem !important;
    }
}

/* ✅ Mobile permanece confortável */
@media (max-width: 899px) {
    .main .block-container {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1.3rem !important;
        padding-bottom: 1.3rem !important;
    }
}

/* ✅ Tabelas e dataframes sempre 100% */
div[data-testid="stDataFrame"] {
    width: 100% !important;
}
div[data-testid="stTable"] {
    width: 100% !important;
}

/* ✅ Melhor uso de colunas */
div[data-testid="stHorizontalBlock"] {
    gap: 1.2rem !important;
}

/* ✅ Expande selects e inputs que ficam estreitos */
div[data-baseweb="select"] {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)


st.title("✅ Controle de Cestas Básicas")
st.write("Use o menu lateral para navegar.")
st.success("¹¹ E, respondendo ele, disse-lhes: Quem tiver duas túnicas, reparta com o que não tem, e quem tiver alimentos, faça da mesma maneira. Lucas 3:11")
