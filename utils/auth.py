import streamlit as st
import os

def require_pin(app_name="Atitude Stock - Igreja", logo_path="assets/logo.jfif"):
    pin = os.getenv("APP_PIN")

    if not pin:
        with st.sidebar:
            if os.path.exists(logo_path):
                st.image(logo_path, width=120)
            st.success("🔓 Acesso livre (sem PIN)")
        return True

    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # ==========================
    # ✅ SIDEBAR FIXO (SEMPRE)
    # ==========================
    with st.sidebar:
        # ✅ LOGO
        if logo_path and os.path.exists(logo_path):
            st.image(logo_path, width=110)

        st.markdown(f"### {app_name}")
        st.markdown("---")

        if st.session_state.pin_ok:
            st.success("✅ Acesso liberado")

            # ✅ Botão de logout com cor e ícone (HTML + CSS)
            st.markdown(
                """
                <style>
                div.stButton > button {
                    background-color: #dc2626 !important;
                    color: white !important;
                    border-radius: 10px !important;
                    font-weight: 600 !important;
                    border: none !important;
                    padding: 0.6em 1em !important;
                }
                div.stButton > button:hover {
                    background-color: #b91c1c !important;
                    color: white !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.clear()
                st.experimental_rerun()

            st.markdown("---")

        else:
            # ✅ Se não autenticado, esconder o menu de navegação
            st.markdown(
                """
                <style>
                [data-testid="stSidebarNav"] {display: none;}
                </style>
                """,
                unsafe_allow_html=True
            )

    # ==========================
    # ✅ BLOQUEIO TOTAL
    # ==========================
    if st.session_state.pin_ok:
        return True

    # ==========================
    # ✅ TELA DE PIN
    # ==========================
    st.title("🔐 Acesso Restrito")
    st.caption(app_name)

    st.info("Digite o PIN para acessar o sistema.")

    typed = st.text_input("PIN", type="password")

    col1, col2 = st.columns([2, 1])
    with col1:
        login_btn = st.button("✅ Entrar", use_container_width=True)
    with col2:
        if st.button("🔄 Limpar", use_container_width=True):
            st.experimental_rerun()

    if login_btn:
        if typed == pin:
            st.session_state.pin_ok = True
            st.experimental_rerun()
        else:
            st.error("❌ PIN incorreto")

    st.caption("🔒 Segurança ativa: acesso protegido por PIN.")
    st.stop()
