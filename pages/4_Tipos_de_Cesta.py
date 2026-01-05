import streamlit as st
import pandas as pd
from utils.db import fetch_table, insert_row, update_row, delete_row
from utils.calculations import analyze_basket

st.title("🧺 Tipos de Cesta — Cadastro e Receita (com validação de estoque)")

baskets = fetch_table("basket_types", order="name")
products = fetch_table("products", order="name")
prod_id_to_name = {p["id"]: p["name"] for p in products}

if not products:
    st.warning("Cadastre produtos antes de criar cestas.")
    st.stop()

# ==========================
# CRIAR NOVA CESTA
# ==========================
st.subheader("➕ Criar tipo de cesta")

with st.form("add_basket", clear_on_submit=True):
    name = st.text_input("Nome da cesta *", placeholder="Ex: Cesta Adulto")
    desc = st.text_area("Descrição (opcional)")
    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if not name.strip():
            st.error("Nome obrigatório.")
        else:
            try:
                insert_row("basket_types", {"name": name.strip(), "description": desc})
                st.success("✅ Cesta cadastrada!")
                st.experimental_rerun()
            except Exception as e:
                st.error("❌ Erro ao cadastrar. O nome pode já existir.")
                st.exception(e)

st.divider()

if not baskets:
    st.info("Nenhuma cesta cadastrada ainda.")
    st.stop()

# ==========================
# LISTAGEM DE CESTAS
# ==========================
st.subheader("📋 Cestas cadastradas")
df = pd.DataFrame(baskets)[["name", "description", "created_at"]]
df.columns = ["Cesta", "Descrição", "Criado em"]
st.dataframe(df, use_container_width=True, height=250)

st.divider()

# ==========================
# SELECIONAR CESTA
# ==========================
st.subheader("🔍 Selecionar e gerenciar cesta")

basket_map = {b["name"]: b for b in baskets}
selected_basket_name = st.selectbox("Selecione um tipo de cesta", list(basket_map.keys()))
b = basket_map[selected_basket_name]

st.markdown(f"### 🧺 {b['name']}")

# ==========================
# ANÁLISE DE ESTOQUE DA CESTA
# ==========================
completas, faltas, checklist = analyze_basket(b["id"])

colA, colB = st.columns(2)
with colA:
    st.metric("✅ Cestas completas montáveis", completas)
with colB:
    if not checklist:
        st.warning("⚠️ Sem itens cadastrados ainda.")
    else:
        if faltas:
            pid, falta = sorted(faltas.items(), key=lambda x: x[1], reverse=True)[0]
            pname = prod_id_to_name.get(pid, "???")
            st.error(f"❌ Próxima cesta incompleta — falta {falta:.2f} de {pname}")
        else:
            st.success("✅ Próxima cesta também completa")

if checklist:
    st.subheader("📌 Checklist por item (estoque x receita)")
    rows = []
    for it in checklist:
        rows.append({
            "Produto": prod_id_to_name.get(it["product_id"], "???"),
            "Estoque": it["stock"],
            "Necessário (por cesta)": it["required"],
            "Sobra após completas": it["remaining"],
            "Ok para +1?": "✅" if it["ok_for_next"] else "❌",
            "Falta para +1": it["missing_for_next"]
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    if faltas:
        st.error("❌ Para montar mais 1 cesta, falta:")
        for pid, falta in faltas.items():
            st.write(f"- **{prod_id_to_name.get(pid, '???')}**: falta **{falta:.2f}**")
    else:
        st.success("✅ Com o estoque atual, você consegue montar mais 1 cesta completa.")

st.divider()

# ==========================
# EDITAR / EXCLUIR CESTA
# ==========================
st.subheader("✏️ Editar / 🗑️ Excluir cesta")

with st.form("edit_basket"):
    new_name = st.text_input("Nome", value=b["name"])
    new_desc = st.text_area("Descrição", value=b.get("description") or "")
    submitted = st.form_submit_button("Salvar alterações")

    if submitted:
        if not new_name.strip():
            st.error("Nome obrigatório.")
        else:
            try:
                update_row("basket_types", {"id": b["id"]}, {"name": new_name.strip(), "description": new_desc})
                st.success("✅ Cesta atualizada!")
                st.experimental_rerun()
            except Exception as e:
                st.error("❌ Erro ao atualizar. Talvez nome já exista.")
                st.exception(e)

st.warning("⚠️ Excluir cesta pode afetar histórico de entregas.")
confirm_del = st.checkbox("Confirmo exclusão desta cesta.")
if st.button("Excluir cesta"):
    if not confirm_del:
        st.error("Marque confirmação.")
    else:
        try:
            delete_row("basket_types", {"id": b["id"]})
            st.success("✅ Cesta excluída!")
            st.experimental_rerun()
        except Exception as e:
            st.error("❌ Não foi possível excluir (pode ter entregas registradas).")
            st.exception(e)

st.divider()

# ==========================
# ITENS DA CESTA (RECEITA)
# ==========================
st.subheader("📦 Itens da cesta (receita)")

items = fetch_table("basket_type_items", {"basket_type_id": b["id"]})
item_map_by_label = {}

if items:
    table = []
    for it in items:
        label = f"{prod_id_to_name.get(it['product_id'], '???')} (req: {float(it['quantity_required']):.2f})"
        item_map_by_label[label] = it

        table.append({
            "Produto": prod_id_to_name.get(it["product_id"], "???"),
            "Quantidade necessária": float(it["quantity_required"])
        })
    st.dataframe(pd.DataFrame(table), use_container_width=True)
else:
    st.info("Esta cesta ainda não possui itens.")

st.divider()

# ==========================
# ADICIONAR ITEM (COM BUSCA)
# ==========================
st.subheader("➕ Adicionar item na cesta")

prod_search = st.text_input("Buscar produto", placeholder="Ex: arroz / açúcar")
filtered_products = []

if prod_search.strip():
    s = prod_search.strip().lower()
    for p in products:
        if s in p["name"].lower():
            filtered_products.append(p)
else:
    filtered_products = products[:30]  # não pesa

if not filtered_products:
    st.warning("Nenhum produto encontrado com essa busca.")
else:
    filtered_map = {p["name"]: p for p in filtered_products}

    with st.form("add_item"):
        prod_name = st.selectbox("Produto", list(filtered_map.keys()))
        qty_req = st.number_input("Quantidade necessária", min_value=0.1, step=0.1, value=1.0)
        submitted = st.form_submit_button("Adicionar")

        if submitted:
            try:
                insert_row("basket_type_items", {
                    "basket_type_id": b["id"],
                    "product_id": filtered_map[prod_name]["id"],
                    "quantity_required": float(qty_req)
                })
                st.success("✅ Item adicionado!")
                st.experimental_rerun()
            except Exception as e:
                st.error("❌ Erro ao adicionar. Talvez o produto já esteja nesta cesta.")
                st.exception(e)

st.divider()

# ==========================
# REMOVER ITEM
# ==========================
st.subheader("🗑️ Remover item da cesta")

if not items:
    st.info("Nenhum item para remover.")
else:
    item_label = st.selectbox("Selecione item para remover", list(item_map_by_label.keys()))
    it = item_map_by_label[item_label]

    if st.button("Remover item"):
        try:
            delete_row("basket_type_items", {"id": it["id"]})
            st.success("✅ Item removido!")
            st.experimental_rerun()
        except Exception as e:
            st.error("❌ Erro ao remover item.")
            st.exception(e)
