import streamlit as st
import os

def require_pin():
    pin = os.getenv("APP_PIN")

    if not pin:
        return True

    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # ✅ Se ainda não autenticou
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

    # ✅ Já autenticado: mostrar botão Sair no sidebar
    if st.sidebar.button("🚪 Sair"):
        st.session_state.pin_ok = False
        st.experimental_rerun()

    return True
