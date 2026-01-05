import streamlit as st
import os
import base64


def _get_base64_image(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


def require_pin(
    app_name="Atitude Stock - Igreja",
    logo_path="assets/logo.png",
    version="v1.0.0",
    whatsapp="21994391902",
    developer="Diogo Silva",
    header_top_padding=28,
    actions_top_padding=10
):
    pin = os.getenv("APP_PIN")

    w = str(whatsapp).strip()
    whatsapp_link = f"https://wa.me/{w}"

    display = w
    if len(w) >= 11:
        display = f"({w[:2]}) {w[2:7]}-{w[7:]}"

    # ==========================
    # ✅ CSS GLOBAL
    # ==========================
    st.markdown(
        f"""
        <style>
        section[data-testid="stSidebar"] > div {{
            padding-top: 10px;
        }}

        .sidebar-header {{
            text-align: center;
            margin-top: {header_top_padding}px;
            margin-bottom: 8px;
        }}

        .sidebar-logo {{
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }}
        .sidebar-logo img {{
            width: 92px;
            height: 92px;
            border-radius: 999px;
            object-fit: cover;
            border: 3px solid rgba(255,255,255,0.18);
            box-shadow: 0px 6px 18px rgba(0,0,0,0.35);
        }}

        .sidebar-title {{
            font-size: 17px;
            font-weight: 900;
            margin: 0;
            padding: 0;
        }}

        .sidebar-actions {{
            text-align: center;
            margin-top: {actions_top_padding}px;
            margin-bottom: 12px;
        }}

        .sidebar-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.18);
            border: 1px solid rgba(34, 197, 94, 0.35);
            color: #a7f3d0;
            font-size: 13px;
            font-weight: 800;
            margin-bottom: 10px;
        }}

        div.stButton > button {{
            background-color: #dc2626 !important;
            color: white !important;
            border-radius: 12px !important;
            font-weight: 900 !important;
            border: none !important;
            padding: 0.70em 1em !important;
            margin-top: 0px !important;
        }}
        div.stButton > button:hover {{
            background-color: #b91c1c !important;
            color: white !important;
        }}

        /* ✅ rodapé */
        .sidebar-footer {{
            position: fixed;
            bottom: 10px;
            left: 0;
            width: 100%;
            padding: 0 18px;
            text-align: center;
            font-size: 12px;
            color: rgba(255,255,255,0.55);
            line-height: 1.35;
            z-index: 9999;
        }}

        .sidebar-footer .footer-version {{
            font-weight: 900;
            color: rgba(255,255,255,0.78);
            margin-bottom: 3px;
        }}

        .sidebar-footer .footer-contact {{
            font-weight: 700;
            color: rgba(255,255,255,0.70);
            margin-bottom: 3px;
        }}

        .sidebar-footer .footer-dev {{
            font-weight: 600;
            color: rgba(255,255,255,0.60);
        }}

        .sidebar-footer a {{
            color: rgba(255,255,255,0.78);
            text-decoration: none;
        }}
        .sidebar-footer a:hover {{
            text-decoration: underline;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # ==========================
    # ✅ SIDEBAR HEADER SEMPRE VISÍVEL
    # ==========================
    with st.sidebar:
        img_html = ""
        img64 = _get_base64_image(logo_path)
        if img64:
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

        # ✅ rodapé fixo sempre
        st.markdown(
            f"""
            <div class="sidebar-footer">
                <div class="footer-version">📦 {version}</div>
                <div class="footer-contact">📞 <a href="{whatsapp_link}" target="_blank">WhatsApp: {display}</a></div>
                <div class="footer-dev">👨‍💻 Desenvolvedor: {developer}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 🔓 sem PIN = livre
    if not pin:
        with st.sidebar:
            st.success("🔓 Acesso livre (sem PIN)")
        return True

    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # ✅ logado
    if st.session_state.pin_ok:
        with st.sidebar:
            st.markdown(
                """
                <div class="sidebar-actions">
                    <span class="sidebar-badge">✅ Acesso liberado</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        return True

    # ✅ não logado: esconder menu
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

    # ✅ Tela PIN
    st.title("🔐 Acesso Restrito")
    st.caption("Somente equipe autorizada.")
    st.info("Digite o PIN para acessar o sistema.")

    typed = st.text_input("PIN", type="password")

    col1, col2 = st.columns([2, 1])
    with col1:
        login_btn = st.button("✅ Entrar", use_container_width=True)
    with col2:
        if st.button("🔄 Limpar", use_container_width=True):
            st.rerun()

    if login_btn:
        if typed == pin:
            st.session_state.pin_ok = True
            st.rerun()
        else:
            st.error("❌ PIN incorreto")

    st.caption("🔒 Segurança ativa: acesso protegido por PIN.")
    st.stop()
