import streamlit as st
import pandas as pd
from utils.db import fetch_table
from utils.calculations import basket_summary
from utils.operations import quick_basket_checkout, register_delivery, register_delivery_custom_items
from utils.auth import require_pin
require_pin()
from utils.ui import apply_global_layout
apply_global_layout()



st.title("📦 Dashboard — Cestas disponíveis (montáveis)")

baskets = fetch_table("basket_types", {"is_active": True}, order="name")

if not baskets:
    st.warning("Nenhum tipo de cesta ativo cadastrado.")
    st.stop()

leaders = fetch_table("cell_leaders", order="name")
families = fetch_table("families", order="representative_name")
products = fetch_table("products", order="name")
prod_map = {p["id"]: p["name"] for p in products}
prod_name_to_id = {p["name"]: p["id"] for p in products}

# ==========================
# RESUMO POR CESTA
# ==========================
rows = []
for b in baskets:
    completas, limitante, falta = basket_summary(b["id"])
    rows.append({
        "id": b["id"],
        "Tipo de Cesta": b["name"],
        "Disponíveis": completas,
        "Falta p/ +1": f"Falta {falta} de {limitante}" if falta > 0 else "-"
    })

df = pd.DataFrame(rows)

st.subheader("📌 Disponibilidade atual")
st.dataframe(df[["Tipo de Cesta", "Disponíveis", "Falta p/ +1"]], use_container_width=True, height=280)

st.divider()

# ==========================
# BAIXA DIRETA
# ==========================
st.subheader("📤 Dar baixa direto do dashboard")

basket_name = st.selectbox("Tipo de cesta", df["Tipo de Cesta"].tolist())
basket_id = df[df["Tipo de Cesta"] == basket_name]["id"].values[0]
available = int(df[df["Tipo de Cesta"] == basket_name]["Disponíveis"].values[0])

st.metric("Disponíveis agora", available)

qty = st.number_input("Quantidade para baixar", min_value=1, step=1, value=1)

tab1, tab2 = st.tabs(["⚡ Baixa rápida", "📝 Registrar entrega"])

# ==========================
# TAB 1: Baixa rápida
# ==========================
with tab1:
    st.info("⚡ Baixa rápida: baixa o estoque baseado na receita (sem família/líder).")
    ref = st.text_input("Referência (opcional)", value="Baixa rápida - Dashboard")

    if qty > available:
        st.error(f"❌ Você pediu {qty}, mas só tem {available} disponíveis.")
    else:
        if st.button("⚡ Baixar agora"):
            try:
                quick_basket_checkout(basket_id, qty, reference=ref)
                st.success("✅ Baixa rápida realizada! Estoque atualizado.")
                st.experimental_rerun()
            except Exception as e:
                st.error("Erro ao realizar baixa rápida.")
                st.exception(e)

# ==========================
# TAB 2: Registrar entrega
# ==========================
with tab2:
    if not leaders or not families:
        st.warning("Cadastre líderes e famílias para registrar entrega.")
        st.stop()

    if qty > available:
        st.error(f"❌ Você pediu {qty}, mas só tem {available} disponíveis.")
        st.stop()

    leader_map = {f"{l['name']} ({l['phone']}) — {l['network_name']}": l for l in leaders}
    family_map = {f"{f['representative_name']} ({f['representative_phone']})": f for f in families}

    leader_sel = st.selectbox("Líder solicitante", list(leader_map.keys()))
    family_sel = st.selectbox("Família beneficiada", list(family_map.keys()))
    notes = st.text_area("Observação (opcional)")

    # ==========================
    # MODO PERSONALIZADO
    # ==========================
    partial_mode = st.checkbox("📦 Entrega personalizada (pode ajustar quantidades livremente)", value=False)

    items_dict = {}
    partial_notes = None

    if partial_mode:
        st.warning("⚠️ Ajuste os itens entregues. Isso baixa exatamente o que você definir.")

        recipe = fetch_table("basket_type_items", {"basket_type_id": basket_id})

        # Editor da receita base
        st.markdown("### ✅ Itens da cesta (base)")
        for it in recipe:
            pid = it["product_id"]
            req = float(it["quantity_required"]) * int(qty)

            colA, colB = st.columns([4, 2])
            with colA:
                st.write(prod_map.get(pid, "???"))
            with colB:
                qval = st.number_input(
                    "Qtd entregue",
                    value=float(req),
                    min_value=0.0,
                    step=1.0,
                    key=f"qty_{pid}"
                )
            items_dict[pid] = float(qval)

        # Permite adicionar itens extras fora da receita
        st.markdown("### ➕ Itens extras (opcional)")
        extra_add = st.checkbox("Adicionar item extra", value=False)

        if extra_add:
            extra_prod_name = st.selectbox("Produto extra", list(prod_name_to_id.keys()))
            extra_qty = st.number_input("Qtd extra entregue", min_value=0.0, step=1.0, value=0.0)

            if extra_qty > 0:
                items_dict[prod_name_to_id[extra_prod_name]] = float(extra_qty)

        partial_notes = st.text_input("Motivo / observação da entrega personalizada", placeholder="Ex: faltou açúcar, mandamos mais arroz")

    # ==========================
    # BOTÃO FINAL
    # ==========================
    if st.button("✅ Confirmar entrega e baixar estoque"):
        try:
            if partial_mode:
                delivery = register_delivery_custom_items(
                    family_id=family_map[family_sel]["id"],
                    leader_id=leader_map[leader_sel]["id"],
                    basket_type_id=basket_id,
                    quantity=int(qty),
                    recipient_name=family_map[family_sel]["representative_name"],
                    items_dict=items_dict,
                    notes=notes,
                    is_partial=True,
                    partial_notes=partial_notes
                )
                st.success(f"✅ Entrega personalizada registrada! ID: {delivery['id']}")
            else:
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
