import streamlit as st
import os

def require_pin(app_name="Controle de Cestas - Igreja", logo_path="assets/logo.png"):
    """
    Proteção simples por PIN para apps Streamlit sem login.
    - Usa APP_PIN do .env / Secrets
    - Guarda status em st.session_state["pin_ok"]
    - Exibe botão de logout no sidebar
    - Exibe logo na tela de PIN se existir
    """

    pin = os.getenv("APP_PIN")

    # Se não existe PIN, não bloqueia (modo aberto)
    if not pin:
        st.sidebar.success("🔓 Acesso livre (sem PIN)")
        return True

    # Inicializa estado
    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # Se já logado, mostra logout e status
    if st.session_state.pin_ok:
        st.sidebar.success("✅ Acesso liberado")
        st.sidebar.caption(app_name)

        if st.sidebar.button("🚪 Sair"):
            st.session_state.pin_ok = False
            st.experimental_rerun()

        return True

    # =======================
    # TELA DE LOGIN
    # =======================
    st.set_page_config(page_title=app_name, layout="centered")

    # ✅ Logo centralizado (se existir)
    if logo_path and os.path.exists(logo_path):
        st.image(logo_path, width=200)

    st.markdown(
        f"""
        <div style="text-align:center;">
            <h1>🔐 Acesso Restrito</h1>
            <p style="color: #666;">
                {app_name}<br>
                Somente equipe autorizada.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Digite o PIN para acessar o sistema.")

    show_pin = st.checkbox("Mostrar PIN digitado", value=False)
    typed = st.text_input(
        "PIN",
        type="default" if show_pin else "password",
        placeholder="Digite o PIN de acesso"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        login_btn = st.button("✅ Entrar", use_container_width=True)

    with col2:
        if st.button("🔄 Limpar", use_container_width=True):
            st.experimental_rerun()

    if login_btn:
        if typed == pin:
            st.session_state.pin_ok = True
            st.success("✅ Acesso liberado!")
            st.experimental_rerun()
        else:
            st.error("❌ PIN incorreto. Tente novamente.")

    st.markdown("---")
    st.caption("🔒 Segurança: O sistema usa PIN para proteger informações e evitar acesso indevido.")

    st.stop()
