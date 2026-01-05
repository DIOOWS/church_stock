from dotenv import load_dotenv
load_dotenv()

import streamlit as st
st.set_page_config(page_title="Atitude Stock - Igreja", layout="wide")

from utils.auth import require_pin
require_pin(
    app_name="Atitude Stock - Igreja",
    logo_path="assets/logo.png",
    version="v1.0.0",
    whatsapp="21994391902",
    developer="Diogo Silva"
)

st.title("✅ Controle de Cestas Básicas")
st.write("Use o menu lateral para navegar.")

st.success("¹¹ E, respondendo ele, disse-lhes: Quem tiver duas túnicas, reparta com o que não tem, e quem tiver alimentos, faça da mesma maneira. Lucas 3:11")
