import streamlit as st
import os
import base64


def _get_base64_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def require_pin(app_name="Atitude Stock - Igreja", logo_path="assets/logo.png"):
    pin = os.getenv("APP_PIN")

    # ==========================
    # ✅ CSS GLOBAL (sidebar header fixo + logo circular + badge + logout vermelho)
    # ==========================
    st.markdown(
        """
        <style>
        /* Sidebar padding */
        section[data-testid="stSidebar"] > div {
            padding-top: 10px;
        }

        /* Header do sidebar sempre central */
        .sidebar-header {
            text-align: center;
            margin-top: 4px;
            margin-bottom: 6px;
        }

        /* Logo circular */
        .sidebar-logo {
            display: flex;
            justify-content: center;
            margin-bottom: 8px;
        }
        .sidebar-logo img {
            width: 95px;
            height: 95px;
            border-radius: 999px;
            object-fit: cover;
            border: 3px solid rgba(255,255,255,0.18);
            box-shadow: 0px 6px 18px rgba(0,0,0,0.35);
        }

        /* Título */
        .sidebar-title {
            font-size: 17px;
            font-weight: 900;
            margin: 0;
            padding: 0;
        }

        /* Badge de status */
        .sidebar-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.18);
            border: 1px solid rgba(34, 197, 94, 0.35);
            color: #a7f3d0;
            font-size: 13px;
            font-weight: 800;
            margin-top: 10px;
            margin-bottom: 8px;
        }

        /* Botão logout vermelho */
        div.stButton > button {
            background-color: #dc2626 !important;
            color: white !important;
            border-radius: 12px !important;
            font-weight: 900 !important;
            border: none !important;
            padding: 0.70em 1em !important;
            margin-top: 6px !important;
        }
        div.stButton > button:hover {
            background-color: #b91c1c !important;
            color: white !important;
        }

        /* Separador menor */
        hr {
            margin: 10px 0px !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ==========================
    # ✅ SIDEBAR HEADER SEMPRE VISÍVEL
    # ==========================
    with st.sidebar:
        img_html = ""
        if logo_path and os.path.exists(logo_path):
            img64 = _get_base64_image(logo_path)
            img_html = f"""
            <div class="sidebar-logo">
                <img src="data:image/png;base64,{img64}">
            </div>
            """

        st.markdown(
            f"""
            <div class="sidebar-header">
                {img_html}
                <div class="sidebar-title">{app_name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==========================
    # 🔓 Se não existe PIN, deixa livre
    # ==========================
    if not pin:
        with st.sidebar:
            st.success("🔓 Acesso livre (sem PIN)")
        return True

    # ==========================
    # Estado inicial
    # ==========================
    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # ==========================
    # ✅ Se autenticado, sidebar mostra badge + logout
    # ==========================
    if st.session_state.pin_ok:
        with st.sidebar:
            st.markdown(
                '<div class="sidebar-header"><span class="sidebar-badge">✅ Acesso liberado</span></div>',
                unsafe_allow_html=True
            )

            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.clear()
                st.experimental_rerun()

            st.markdown("---")
        return True

    # ==========================
    # ✅ Se NÃO autenticado: esconder navegação do menu
    # ==========================
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # ==========================
    # ✅ Tela PIN
    # ==========================
    st.title("🔐 Acesso Restrito")
    st.caption("Somente equipe autorizada.")
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
