import streamlit as st
import pandas as pd
from utils.db import fetch_table, insert_row, update_row, delete_row

st.title("🛒 Produtos — Cadastro / Edição / Exclusão")

products = fetch_table("products", order="name")

st.subheader("➕ Cadastrar novo produto")
with st.form("add_product"):
    name = st.text_input("Nome do produto")
    unit = st.selectbox("Unidade", ["unidade", "kg", "litro", "pacote", "caixa", "saco"])
    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if not name.strip():
            st.error("Nome obrigatório.")
        else:
            try:
                new = insert_row("products", {"name": name.strip(), "unit": unit})[0]
                insert_row("inventory", {"product_id": new["id"], "quantity": 0})
                st.success("Produto cadastrado com sucesso!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao cadastrar: {e}")

st.divider()
st.subheader("📋 Produtos cadastrados")

if not products:
    st.info("Nenhum produto cadastrado.")
    st.stop()

df = pd.DataFrame(products)[["id", "name", "unit", "created_at"]]
st.dataframe(df.rename(columns={"name": "Produto", "unit": "Unidade"}), use_container_width=True)

st.divider()
st.subheader("✏️ Editar / 🗑️ Excluir produto")

prod_map = {f"{p['name']} ({p['unit']})": p for p in products}
selected = st.selectbox("Selecione um produto", list(prod_map.keys()))
p = prod_map[selected]

col1, col2 = st.columns(2)

with col1:
    new_name = st.text_input("Novo nome", value=p["name"])
    new_unit = st.selectbox("Nova unidade", ["unidade", "kg", "litro", "pacote", "caixa", "saco"], index=["unidade", "kg", "litro", "pacote", "caixa", "saco"].index(p["unit"]))

    if st.button("Salvar alterações"):
        try:
            update_row("products", {"id": p["id"]}, {"name": new_name.strip(), "unit": new_unit})
            st.success("Produto atualizado!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")

with col2:
    st.warning("⚠️ Excluir produto pode afetar cestas já cadastradas.")
    confirm = st.checkbox("Confirmo que quero excluir este produto.")
    if st.button("Excluir produto"):
        if not confirm:
            st.error("Marque a confirmação para excluir.")
        else:
            try:
                delete_row("products", {"id": p["id"]})
                st.success("Produto excluído!")
                st.experimental_rerun()
            except Exception as e:
                st.error("Não foi possível excluir. Talvez ele esteja em alguma cesta. Remova da cesta primeiro.")
                st.exception(e)
