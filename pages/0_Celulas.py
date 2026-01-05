import streamlit as st
import pandas as pd
from utils.db import fetch_table, insert_row, update_row, delete_row
from utils.auth import require_pin
require_pin()


st.title("🏠 Células — Cadastro / Edição / Exclusão")

cells = fetch_table("cells", order="cell_name")
leaders = fetch_table("cell_leaders", order="name")
supers = fetch_table("supervisors", order="name")

leader_map = {f"{l['name']} ({l['phone']})": l for l in leaders} if leaders else {}
super_map = {f"{s['name']} ({s['phone']})": s for s in supers} if supers else {}

# ==========================
# CADASTRO DE CÉLULA
# ==========================
st.subheader("➕ Cadastrar nova célula")

with st.form("add_cell"):
    cell_name = st.text_input("Nome da Célula (obrigatório)", placeholder="Ex: Célula Esperança")
    network_name = st.text_input("Rede (obrigatório)", placeholder="Ex: Rede Azul")

    leader_opt = st.selectbox("Líder (opcional)", ["(sem líder)"] + list(leader_map.keys()))
    super_opt = st.selectbox("Supervisor (opcional)", ["(sem supervisor)"] + list(super_map.keys()))

    submitted = st.form_submit_button("Cadastrar célula")

    if submitted:
        if not cell_name.strip() or not network_name.strip():
            st.error("Nome da célula e rede são obrigatórios.")
        else:
            leader_id = None
            supervisor_id = None

            if leader_opt != "(sem líder)":
                leader_id = leader_map[leader_opt]["id"]
            if super_opt != "(sem supervisor)":
                supervisor_id = super_map[super_opt]["id"]

            try:
                insert_row("cells", {
                    "cell_name": cell_name.strip(),
                    "network_name": network_name.strip(),
                    "leader_id": leader_id,
                    "supervisor_id": supervisor_id
                })
                st.success("Célula cadastrada com sucesso!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao cadastrar célula: {e}")

st.divider()

# ==========================
# LISTAGEM
# ==========================
st.subheader("📋 Células cadastradas")

if not cells:
    st.info("Nenhuma célula cadastrada ainda.")
    st.stop()

leader_id_to_label = {l["id"]: f"{l['name']} ({l['phone']})" for l in leaders} if leaders else {}
super_id_to_label = {s["id"]: f"{s['name']} ({s['phone']})" for s in supers} if supers else {}

rows = []
for c in cells:
    rows.append({
        "Célula": c["cell_name"],
        "Rede": c["network_name"],
        "Líder": leader_id_to_label.get(c["leader_id"], "-"),
        "Supervisor": super_id_to_label.get(c["supervisor_id"], "-"),
        "Criado em": c["created_at"]
    })

st.dataframe(pd.DataFrame(rows), use_container_width=True)

st.divider()

# ==========================
# EDITAR / EXCLUIR
# ==========================
st.subheader("✏️ Editar / 🗑️ Excluir célula")

cell_map = {c["cell_name"]: c for c in cells}
selected_cell = st.selectbox("Selecione uma célula", list(cell_map.keys()))
c = cell_map[selected_cell]

with st.form("edit_cell"):
    new_cell_name = st.text_input("Nome da célula", value=c["cell_name"])
    new_network_name = st.text_input("Rede", value=c["network_name"])

    # Seleção atual de líder/supervisor
    leader_current_label = leader_id_to_label.get(c["leader_id"], "(sem líder)")
    super_current_label = super_id_to_label.get(c["supervisor_id"], "(sem supervisor)")

    leader_opt = st.selectbox("Líder (opcional)", ["(sem líder)"] + list(leader_map.keys()),
                              index=(["(sem líder)"] + list(leader_map.keys())).index(leader_current_label) if leader_current_label in (["(sem líder)"] + list(leader_map.keys())) else 0)

    super_opt = st.selectbox("Supervisor (opcional)", ["(sem supervisor)"] + list(super_map.keys()),
                             index=(["(sem supervisor)"] + list(super_map.keys())).index(super_current_label) if super_current_label in (["(sem supervisor)"] + list(super_map.keys())) else 0)

    submitted = st.form_submit_button("Salvar alterações")

    if submitted:
        leader_id = None
        supervisor_id = None

        if leader_opt != "(sem líder)":
            leader_id = leader_map[leader_opt]["id"]
        if super_opt != "(sem supervisor)":
            supervisor_id = super_map[super_opt]["id"]

        try:
            update_row("cells", {"id": c["id"]}, {
                "cell_name": new_cell_name.strip(),
                "network_name": new_network_name.strip(),
                "leader_id": leader_id,
                "supervisor_id": supervisor_id
            })
            st.success("Célula atualizada!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Erro ao atualizar: {e}")

st.warning("⚠️ Excluir célula pode afetar famílias vinculadas.")
confirm = st.checkbox("Confirmo exclusão da célula.")
if st.button("Excluir célula"):
    if not confirm:
        st.error("Marque confirmação.")
    else:
        try:
            delete_row("cells", {"id": c["id"]})
            st.success("Célula excluída!")
            st.experimental_rerun()
        except Exception as e:
            st.error("Não foi possível excluir. Talvez existam famílias vinculadas a essa célula.")
            st.exception(e)
