import streamlit as st
import os
import base64

def _get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def require_pin(app_name="Atitude Stock - Igreja", logo_path="assets/logo.jfif"):
    pin = os.getenv("APP_PIN")

    # ==========================
    # ✅ CSS GLOBAL (logo circular + botão logout vermelho)
    # ==========================
    st.markdown(
        """
        <style>
        /* logo circular */
        .sidebar-logo {
            display: flex;
            justify-content: center;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .sidebar-logo img {
            width: 110px;
            height: 110px;
            border-radius: 999px;
            object-fit: cover;
            border: 3px solid rgba(255,255,255,0.25);
            box-shadow: 0px 4px 12px rgba(0,0,0,0.35);
        }

        /* botão logout vermelho */
        div.stButton > button {
            background-color: #dc2626 !important;
            color: white !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            border: none !important;
            padding: 0.65em 1em !important;
        }
        div.stButton > button:hover {
            background-color: #b91c1c !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ==========================
    # 🔓 Sem PIN = modo aberto
    # ==========================
    if not pin:
        with st.sidebar:
            if logo_path and os.path.exists(logo_path):
                img64 = _get_base64_image(logo_path)
                st.markdown(
                    f"""
                    <div class="sidebar-logo">
                        <img src="data:image/png;base64,{img64}">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown(f"### {app_name}")
            st.success("🔓 Acesso livre (sem PIN)")
        return True

    # ==========================
    # Estado inicial
    # ==========================
    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # ==========================
    # ✅ SIDEBAR FIXO SEMPRE
    # ==========================
    with st.sidebar:
        # Logo circular (se existir)
        if logo_path and os.path.exists(logo_path):
            img64 = _get_base64_image(logo_path)
            st.markdown(
                f"""
                <div class="sidebar-logo">
                    <img src="data:image/png;base64,{img64}">
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(f"### {app_name}")
        st.markdown("---")

        if st.session_state.pin_ok:
            st.success("✅ Acesso liberado")

            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.clear()
                st.experimental_rerun()

            st.markdown("---")
        else:
            # esconder navegação enquanto não autenticado
            st.markdown(
                """
                <style>
                [data-testid="stSidebarNav"] {display: none;}
                </style>
                """,
                unsafe_allow_html=True
            )

    # ==========================
    # ✅ Se já autenticado, libera
    # ==========================
    if st.session_state.pin_ok:
        return True

    # ==========================
    # ✅ Tela de PIN
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
