import streamlit as st
import os

def require_pin(app_name="Atitude Stock - Igreja", logo_path="assets/logo.png"):
    pin = os.getenv("APP_PIN")

    # 🔓 Sem PIN = livre
    if not pin:
        st.sidebar.success("🔓 Acesso livre (sem PIN)")
        return True

    if "pin_ok" not in st.session_state:
        st.session_state.pin_ok = False

    # ✅ Já autenticado
    if st.session_state.pin_ok:
        st.sidebar.success("✅ Acesso liberado")
        st.sidebar.caption(app_name)

        if st.sidebar.button("🚪 Sair", use_container_width=True):
            st.session_state.pin_ok = False
            st.experimental_rerun()

        return True

    # ✅ Tela de login
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

    if logo_path and os.path.exists(logo_path):
        st.image(logo_path, width=200)

    st.markdown(f"<h1>🔐 Acesso Restrito</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#666;'>{app_name}<br>Somente equipe autorizada.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.info("Digite o PIN para acessar o sistema.")

    typed = st.text_input("PIN", type="password", placeholder="Digite o PIN de acesso")

    if st.button("✅ Entrar", use_container_width=True):
        if typed == pin:
            st.session_state.pin_ok = True
            st.experimental_rerun()
        else:
            st.error("❌ PIN incorreto.")

    st.caption("🔒 Segurança ativa: acesso protegido por PIN.")
    st.stop()
