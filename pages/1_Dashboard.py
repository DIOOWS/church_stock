import streamlit as st
import pandas as pd
from utils.db import fetch_table
from utils.calculations import basket_summary
from utils.operations import quick_basket_checkout, register_delivery

st.title("📦 Dashboard — Cestas disponíveis (montáveis)")

baskets = fetch_table("basket_types", {"is_active": True}, order="name")

if not baskets:
    st.warning("Nenhum tipo de cesta cadastrado ainda.")
    st.stop()

# Carrega líderes e famílias apenas para entrega completa
leaders = fetch_table("cell_leaders", order="name")
families = fetch_table("families", order="representative_name")

# ==========================
# RESUMO LIMPO POR CESTA
# ==========================
rows = []
for b in baskets:
    completas, limitante, falta = basket_summary(b["id"])

    if falta > 0:
        falta_texto = f"Falta {falta} de {limitante}"
    else:
        falta_texto = "-"

    rows.append({
        "id": b["id"],
        "Tipo de Cesta": b["name"],
        "Disponíveis": completas,
        "Falta p/ +1": falta_texto
    })

df = pd.DataFrame(rows)

st.subheader("📌 Disponibilidade atual")
st.dataframe(
    df[["Tipo de Cesta", "Disponíveis", "Falta p/ +1"]],
    use_container_width=True,
    height=300
)

st.divider()

# ==========================
# BAIXA DIRETA PELO DASHBOARD
# ==========================
st.subheader("📤 Dar baixa direto no Dashboard")

basket_name = st.selectbox("Tipo de cesta", df["Tipo de Cesta"].tolist())
basket_id = df[df["Tipo de Cesta"] == basket_name]["id"].values[0]
available = int(df[df["Tipo de Cesta"] == basket_name]["Disponíveis"].values[0])

st.metric("Disponíveis agora", available)

qty = st.number_input("Quantidade para baixar", min_value=1, step=1, value=1)

if qty > available:
    st.error(f"❌ Você pediu {qty}, mas só tem {available} disponíveis.")
    st.stop()

tab1, tab2 = st.tabs(["⚡ Baixa rápida", "📝 Entrega completa (com registro)"])

# ==========================
# TAB 1: Baixa rápida
# ==========================
with tab1:
    st.info("⚡ Baixa rápida: baixa do estoque sem registrar família/líder.")
    ref = st.text_input("Referência (opcional)", value="Baixa rápida - Dashboard")
    if st.button("⚡ Baixar agora (rápido)"):
        try:
            quick_basket_checkout(basket_id, qty, reference=ref)
            st.success("✅ Baixa rápida realizada! Estoque atualizado.")
            st.experimental_rerun()
        except Exception as e:
            st.error("Erro ao realizar baixa rápida.")
            st.exception(e)

# ==========================
# TAB 2: Entrega completa
# ==========================
with tab2:
    if not leaders or not families:
        st.warning("Cadastre líderes e famílias para registrar entrega completa.")
    else:
        leader_map = {f"{l['name']} ({l['phone']}) — {l['network_name']}": l for l in leaders}
        family_map = {f"{f['representative_name']} ({f['representative_phone']})": f for f in families}

        leader_sel = st.selectbox("Líder solicitante", list(leader_map.keys()))
        family_sel = st.selectbox("Família beneficiada", list(family_map.keys()))
        notes = st.text_area("Observação (opcional)")

        if st.button("✅ Registrar entrega e baixar"):
            try:
                delivery = register_delivery(
                    family_id=family_map[family_sel]["id"],
                    leader_id=leader_map[leader_sel]["id"],
                    basket_type_id=basket_id,
                    quantity=int(qty),
                    recipient_name=family_map[family_sel]["representative_name"],
                    notes=notes
                )
                st.success(f"✅ Entrega registrada! ID: {delivery['id']}")
                st.experimental_rerun()
            except Exception as e:
                st.error("Erro ao registrar entrega.")
                st.exception(e)
