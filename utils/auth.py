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
    app_name="Atitude Social",
    logo_path="assets/logo.png",
    version="v1.0.0",
    whatsapp="21994391902",
    developer="Diogo Silva",
    header_top_padding=30,
    actions_top_padding=16
):
    pin = os.getenv("APP_PIN")

    w = str(whatsapp).strip()
    whatsapp_link = f"https://wa.me/{w}"

    display = w
    if len(w) >= 11:
        display = f"({w[:2]}) {w[2:7]}-{w[7:]}"

    # ✅ CSS Sidebar
    st.markdown(
        f"""
        <style>
        section[data-testid="stSidebar"] {{
            position: relative;
        }}

        section[data-testid="stSidebar"] > div {{
            padding-top: 10px;
            padding-bottom: 190px; /* ✅ reserva espaço footer + logout */
        }}

        .sidebar-header {{
            text-align: center;
            margin-top: {header_top_padding}px;
            margin-bottom: 6px;
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

        section[data-testid="stSidebar"] h3 {{
            text-align: center;
            font-size: 17px !important;
            font-weight: 900 !important;
            margin-top: 0px !important;
            margin-bottom: 14px !important;
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

        /* ✅ separador elegante no footer */
        .footer-divider {{
            height: 1px;
            width: 100%;
            background: linear-gradient(
                to right,
                rgba(255,255,255,0.02),
                rgba(255,255,255,0.15),
                rgba(255,255,255,0.02)
            );
            margin: 10px 0 12px 0;
        }}

        /* ✅ FOOTER FIXO */
        .sidebar-footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 14px 14px 16px 14px;
            background: rgba(15, 23, 42, 0.96);
            z-index: 9999;
        }}

        /* ✅ card bonito */
        .footer-card {{
            padding: 12px 12px 10px 12px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.10);
            background: rgba(255,255,255,0.04);
            box-shadow: 0px 12px 30px rgba(0,0,0,0.32);
            text-align: center;
            font-size: 12px;
            color: rgba(255,255,255,0.75);
            line-height: 1.45;
        }}

        .footer-version {{
            font-weight: 900;
            margin-bottom: 4px;
            font-size: 12px;
            color: rgba(255,255,255,0.92);
        }}

        .footer-row {{
            margin: 4px 0;
            font-weight: 650;
            color: rgba(255,255,255,0.75);
        }}

        .footer-row strong {{
            color: rgba(255,255,255,0.92);
        }}

        .footer-row a {{
            color: rgba(255,255,255,0.88);
            font-weight: 800;
            text-decoration: none;
        }}
        .footer-row a:hover {{
            text-decoration: underline;
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
        </style>
        """,
        unsafe_allow_html=True
    )

    # ✅ Função do footer card
    def render_footer():
        st.markdown(
            f"""
            <div class="sidebar-footer">
                <div class="footer-divider"></div>
                <div class="footer-card">
                    <div class="footer-version">📦 {version}</div>
                    <div class="footer-row">📞 <a href="{whatsapp_link}" target="_blank">WhatsApp: {display}</a></div>
                    <div class="footer-row">👨‍💻 <strong>{developer}</strong></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ✅ Sidebar Header sempre aparece
    with st.sidebar:
        img64 = _get_base64_image(logo_path)
        if img64:
            st.markdown(
                f"""
                <div class="sidebar-header">
                    <div class="sidebar-logo">
                        <img src="data:image/png;base64,{img64}">
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(f"### {app_name}")

    # 🔓 Sem PIN = livre
    if not pin:
        with st.sidebar:
            st.success("🔓 Acesso livre (sem PIN)")
            render_footer()
        return True

    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # ✅ LOGADO
    if st.session_state.pin_ok:
        with st.sidebar:
            st.markdown(
                f"""
                <div class="sidebar-actions">
                    <span class="sidebar-badge">✅ Acesso liberado</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.clear()
                st.rerun()

            render_footer()
        return True

    # ✅ DESLOGADO (esconde menu)
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        render_footer()

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
