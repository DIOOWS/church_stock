from dotenv import load_dotenv
load_dotenv()

import streamlit as st

# ✅ sempre primeiro
st.set_page_config(page_title="Atitude Stock - Igreja", layout="wide")

# ✅ importa depois do set_page_config
from utils.auth import require_pin
require_pin(app_name="Atitude Stock - Igreja")

st.title("✅ Controle de Cestas Básicas")
st.write("Use o menu lateral para navegar.")
st.success("Sistema pronto: Dashboard, Produtos, Estoque, Cestas, Líderes, Famílias, Entregas e Relatórios.")
