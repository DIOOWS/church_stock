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

/* ✅ largura maior no desktop */
@media (min-width: 900px) {
    .main .block-container {
        max-width: 1400px;
        padding-left: 3rem;
        padding-right: 3rem;
        padding-top: 2.0rem;
        padding-bottom: 2.0rem;
    }
}

/* ✅ mobile continua normal */
@media (max-width: 899px) {
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
}

/* ✅ cards padrão */
.wide-card {
    max-width: 1100px;
    margin: 0 auto;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

</style>
""", unsafe_allow_html=True)

st.title("✅ Controle de Cestas Básicas")
st.write("Use o menu lateral para navegar.")
st.success("¹¹ E, respondendo ele, disse-lhes: Quem tiver duas túnicas, reparta com o que não tem, e quem tiver alimentos, faça da mesma maneira. Lucas 3:11")
