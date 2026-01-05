import streamlit as st
import os

def require_pin(app_name="Atitude Stock - Igreja"):
    pin = os.getenv("APP_PIN")

    if not pin:
        st.sidebar.success("🔓 Sem PIN configurado")
        return True

    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # ✅ já autenticado
    if st.session_state.pin_ok:
        st.sidebar.success("✅ Acesso liberado")
        st.sidebar.caption(app_name)

        if st.sidebar.button("🚪 Sair"):
            st.session_state.pin_ok = False
            st.experimental_rerun()

        return True

    st.title("🔐 Acesso")
    typed = st.text_input("Digite o PIN", type="password")

    if st.button("Entrar"):
        if typed == pin:
            st.session_state.pin_ok = True
            st.experimental_rerun()
        else:
            st.error("PIN incorreto")

    st.stop()
