from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os


st.set_page_config(page_title="Controle de Cestas - Igreja", layout="wide")

pin = os.getenv("APP_PIN")

if pin:
    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    if not st.session_state.pin_ok:
        st.title("🔐 Acesso")
        typed = st.text_input("Digite o PIN de acesso", type="password")
        if st.button("Entrar"):
            if typed == pin:
                st.session_state.pin_ok = True
                st.experimental_rerun()
            else:
                st.error("PIN incorreto.")
        st.stop()

st.title("✅ Controle de Cestas Básicas")
st.write("Use o menu lateral para navegar.")
st.success("Sistema pronto: Dashboard, Produtos, Estoque, Cestas, Líderes, Famílias, Entregas e Relatórios.")
