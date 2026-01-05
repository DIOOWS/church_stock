import streamlit as st
import pandas as pd
from utils.db import fetch_table, insert_row, update_row, delete_row
from utils.auth import require_pin
require_pin()


st.title("👥 Supervisores e Líderes")

# ==========================
# SUPERVISORES
# ==========================
st.header("✅ Supervisores")

supers = fetch_table("supervisors", order="name")

st.subheader("➕ Cadastrar supervisor")
with st.form("add_supervisor", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        sup_name = st.text_input("Nome do Supervisor *")
    with col2:
        sup_phone = st.text_input("Telefone do Supervisor *", placeholder="Ex: 11999998888")

    submitted = st.form_submit_button("Cadastrar Supervisor")

    if submitted:
        if not sup_name.strip() or not sup_phone.strip():
            st.error("⚠️ Nome e telefone são obrigatórios.")
        else:
            try:
                insert_row("supervisors", {"name": sup_name.strip(), "phone": sup_phone.strip()})
                st.success("✅ Supervisor cadastrado!")
                st.experimental_rerun()
            except Exception as e:
                st.error("❌ Erro ao cadastrar. O telefone pode já existir.")
                st.exception(e)

st.divider()

st.subheader("📋 Supervisores cadastrados")
if not supers:
    st.info("Nenhum supervisor cadastrado ainda.")
else:
    sup_search = st.text_input("🔎 Buscar supervisor por nome ou telefone", placeholder="Ex: João / 119999")

    filtered_sup = []
    if sup_search.strip():
        s = sup_search.strip().lower()
        for sp in supers:
            if s in sp["name"].lower() or s in sp["phone"].lower():
                filtered_sup.append(sp)
    else:
        filtered_sup = supers

    df_sup = pd.DataFrame(filtered_sup)[["name", "phone", "created_at"]]
    df_sup.columns = ["Nome", "Telefone", "Criado em"]
    st.dataframe(df_sup, use_container_width=True, height=250)

st.divider()

st.subheader("✏️ Editar / 🗑️ Excluir supervisor")

if supers:
    sup_map = {f"{s['name']} ({s['phone']})": s for s in supers}
    sel_sup = st.selectbox("Selecione um supervisor", list(sup_map.keys()))
    sp = sup_map[sel_sup]

    with st.form("edit_supervisor"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Nome", value=sp["name"])
        with col2:
            new_phone = st.text_input("Telefone", value=sp["phone"])

        submitted = st.form_submit_button("Salvar alterações")

        if submitted:
            if not new_name.strip() or not new_phone.strip():
                st.error("⚠️ Nome e telefone são obrigatórios.")
            else:
                try:
                    update_row("supervisors", {"id": sp["id"]}, {
                        "name": new_name.strip(),
                        "phone": new_phone.strip()
                    })
                    st.success("✅ Supervisor atualizado!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error("❌ Erro ao atualizar. Telefone pode estar em uso.")
                    st.exception(e)

    st.warning("⚠️ Excluir supervisor pode afetar líderes e células ligados a ele.")
    confirm_sup = st.checkbox("Confirmo exclusão do supervisor selecionado.")
    if st.button("Excluir supervisor"):
        if not confirm_sup:
            st.error("Marque a confirmação.")
        else:
            try:
                delete_row("supervisors", {"id": sp["id"]})
                st.success("✅ Supervisor excluído!")
                st.experimental_rerun()
            except Exception as e:
                st.error("❌ Não foi possível excluir. Pode haver vínculos com líderes/células.")
                st.exception(e)

st.divider()

# ==========================
# LÍDERES
# ==========================
st.header("✅ Líderes de Célula")

leaders = fetch_table("cell_leaders", order="name")
sup_id_to_label = {s["id"]: f"{s['name']} ({s['phone']})" for s in supers} if supers else {}

st.subheader("➕ Cadastrar líder")

super_map = {f"{s['name']} ({s['phone']})": s for s in supers} if supers else {}

with st.form("add_leader", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        leader_name = st.text_input("Nome do Líder *")
        leader_phone = st.text_input("Telefone do Líder *", placeholder="Ex: 11999998888")

    with col2:
        network_name = st.text_input("Rede do Líder *", placeholder="Ex: Rede Azul")
        sup_opt = st.selectbox("Supervisor (opcional)", ["(sem supervisor)"] + list(super_map.keys()))

    submitted = st.form_submit_button("Cadastrar Líder")

    if submitted:
        if not leader_name.strip() or not leader_phone.strip() or not network_name.strip():
            st.error("⚠️ Nome, telefone e rede são obrigatórios.")
        else:
            supervisor_id = None
            if sup_opt != "(sem supervisor)":
                supervisor_id = super_map[sup_opt]["id"]

            try:
                insert_row("cell_leaders", {
                    "name": leader_name.strip(),
                    "phone": leader_phone.strip(),
                    "network_name": network_name.strip(),
                    "supervisor_id": supervisor_id
                })
                st.success("✅ Líder cadastrado!")
                st.experimental_rerun()
            except Exception as e:
                st.error("❌ Erro ao cadastrar. O telefone pode já existir.")
                st.exception(e)

st.divider()

st.subheader("📋 Líderes cadastrados")

if not leaders:
    st.info("Nenhum líder cadastrado ainda.")
else:
    leader_search = st.text_input("🔎 Buscar líder por nome, telefone ou rede", placeholder="Ex: Maria / 119999 / Rede Azul")

    filtered_leaders = []
    if leader_search.strip():
        s = leader_search.strip().lower()
        for l in leaders:
            if s in l["name"].lower() or s in l["phone"].lower() or s in l["network_name"].lower():
                filtered_leaders.append(l)
    else:
        filtered_leaders = leaders

    rows = []
    for l in filtered_leaders:
        rows.append({
            "Nome": l["name"],
            "Telefone": l["phone"],
            "Rede": l["network_name"],
            "Supervisor": sup_id_to_label.get(l.get("supervisor_id"), "-")
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, height=300)

st.divider()

st.subheader("✏️ Editar / 🗑️ Excluir líder")

if leaders:
    leader_map = {f"{l['name']} ({l['phone']}) — {l['network_name']}": l for l in leaders}
    sel_leader = st.selectbox("Selecione um líder", list(leader_map.keys()))
    l = leader_map[sel_leader]

    current_sup_label = sup_id_to_label.get(l.get("supervisor_id"), "(sem supervisor)")
    sup_options = ["(sem supervisor)"] + list(super_map.keys())
    sup_index = sup_options.index(current_sup_label) if current_sup_label in sup_options else 0

    with st.form("edit_leader"):
        col1, col2 = st.columns(2)

        with col1:
            new_name = st.text_input("Nome *", value=l["name"])
            new_phone = st.text_input("Telefone *", value=l["phone"])

        with col2:
            new_network = st.text_input("Rede *", value=l["network_name"])
            new_sup_opt = st.selectbox("Supervisor (opcional)", sup_options, index=sup_index)

        submitted = st.form_submit_button("Salvar alterações")

        if submitted:
            if not new_name.strip() or not new_phone.strip() or not new_network.strip():
                st.error("⚠️ Nome, telefone e rede são obrigatórios.")
            else:
                supervisor_id = None
                if new_sup_opt != "(sem supervisor)":
                    supervisor_id = super_map[new_sup_opt]["id"]

                try:
                    update_row("cell_leaders", {"id": l["id"]}, {
                        "name": new_name.strip(),
                        "phone": new_phone.strip(),
                        "network_name": new_network.strip(),
                        "supervisor_id": supervisor_id
                    })
                    st.success("✅ Líder atualizado!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error("❌ Erro ao atualizar. Telefone pode já existir em outro líder.")
                    st.exception(e)

    st.warning("⚠️ Excluir líder pode afetar histórico de entregas e células.")
    confirm_leader = st.checkbox("Confirmo exclusão do líder selecionado.")

    if st.button("Excluir líder"):
        if not confirm_leader:
            st.error("Marque a confirmação.")
        else:
            try:
                delete_row("cell_leaders", {"id": l["id"]})
                st.success("✅ Líder excluído!")
                st.experimental_rerun()
            except Exception as e:
                st.error("❌ Não foi possível excluir. Pode haver entregas registradas ou células vinculadas.")
                st.exception(e)
