import streamlit as st
import pandas as pd
from utils.db import fetch_table
from utils.operations import add_stock

st.title("📥 Estoque — Entrada / Ajuste")

products = fetch_table("products", order="name")
if not products:
    st.warning("Cadastre produtos primeiro.")
    st.stop()

prod_map = {f"{p['name']} ({p['unit']})": p for p in products}

st.subheader("➕ Entrada / Ajuste")
with st.form("stock_form"):
    selected = st.selectbox("Produto", list(prod_map.keys()))
    movement_type = st.selectbox("Tipo", ["entrada", "ajuste", "correcao"])
    qty = st.number_input("Quantidade", step=0.1, value=0.0)
    reference = st.text_input("Referência (opcional)", placeholder="Ex: doação do mercado X")
    submitted = st.form_submit_button("Salvar")

    if submitted:
        if qty == 0:
            st.error("Quantidade deve ser diferente de zero.")
        else:
            product = prod_map[selected]
            add_stock(product["id"], qty, movement_type=movement_type, reference=reference)
            st.success("Movimento registrado!")
            st.experimental_rerun()

st.divider()
st.subheader("📌 Estoque atual")

inv = fetch_table("inventory")
inv_map = {i["product_id"]: float(i["quantity"]) for i in inv}

rows = []
for p in products:
    rows.append({
        "Produto": p["name"],
        "Unidade": p["unit"],
        "Quantidade": inv_map.get(p["id"], 0.0)
    })

st.dataframe(pd.DataFrame(rows), use_container_width=True)

st.divider()
st.subheader("🧾 Histórico de Movimentos (últimos 50)")

moves = fetch_table("stock_movements", order="created_at")
moves = sorted(moves, key=lambda x: x["created_at"], reverse=True)[:50]

if not moves:
    st.info("Nenhum movimento registrado ainda.")
else:
    prod_id_to_name = {p["id"]: p["name"] for p in products}
    dfm = pd.DataFrame(moves)
    dfm["Produto"] = dfm["product_id"].map(prod_id_to_name)
    dfm = dfm[["created_at", "Produto", "qty_change", "movement_type", "reference"]]
    dfm.columns = ["Data", "Produto", "Qtd", "Tipo", "Referência"]
    st.dataframe(dfm, use_container_width=True)
