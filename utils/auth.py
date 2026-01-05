import streamlit as st
import os

def require_pin(app_name="Atitude Stock - Igreja", logo_path=None):
    pin = os.getenv("APP_PIN")

    if not pin:
        st.sidebar.success("🔓 Sem PIN configurado")
        return True

    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # ✅ Se já autenticado: mostra logout
    if st.session_state.pin_ok:
        st.sidebar.success("✅ Acesso liberado")
        st.sidebar.caption(app_name)

        # ✅ Logout REAL
        if st.sidebar.button("🚪 Sair", use_container_width=True):
            st.session_state.clear()
            st.experimental_rerun()

        return True

    # ✅ Se NÃO autenticado: esconder navegação e bloquear tudo
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🔐 Acesso Restrito")
    st.caption(app_name)
    st.info("Digite o PIN para acessar o sistema.")

    typed = st.text_input("PIN", type="password")

    if st.button("✅ Entrar", use_container_width=True):
        if typed == pin:
            st.session_state.pin_ok = True
            st.experimental_rerun()
        else:
            st.error("❌ PIN incorreto")

    st.stop()
