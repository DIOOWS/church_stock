import streamlit as st
import pandas as pd
from utils.db import fetch_table, insert_row, update_row, delete_row
from utils.auth import require_pin
require_pin()


st.title("🏠 Famílias / Beneficiários")

# ==========================
# CARREGAMENTO DE DADOS
# ==========================
cells = fetch_table("cells", order="cell_name")
families = fetch_table("families", order="representative_name")

cell_map = {c["cell_name"]: c for c in cells} if cells else {}
cell_id_to_name = {c["id"]: c["cell_name"] for c in cells} if cells else {}

# ==========================
# CADASTRO
# ==========================
st.subheader("➕ Cadastrar família")

with st.form("add_family", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        representative_name = st.text_input("Nome do representante da família *")
        representative_phone = st.text_input("Telefone do representante *", placeholder="Ex: 11999998888")
        is_church_member = st.checkbox("É membro da igreja?")
        is_cell_member = st.checkbox("É membro de célula?")

    with col2:
        total_people = st.number_input("Total de pessoas na família", min_value=1, step=1, value=1)
        adults = st.number_input("Adultos", min_value=0, step=1, value=0)
        children = st.number_input("Crianças", min_value=0, step=1, value=0)
        adolescents = st.number_input("Adolescentes", min_value=0, step=1, value=0)
        elderly = st.number_input("Idosos", min_value=0, step=1, value=0)

    cell_opt = st.selectbox("Célula (opcional)", ["(sem célula)"] + list(cell_map.keys()))

    submitted = st.form_submit_button("Cadastrar família")

    if submitted:
        if not representative_name.strip() or not representative_phone.strip():
            st.error("⚠️ Nome e telefone do representante são obrigatórios.")
        else:
            cell_id = None
            if cell_opt != "(sem célula)":
                cell_id = cell_map[cell_opt]["id"]

            try:
                insert_row("families", {
                    "representative_name": representative_name.strip(),
                    "representative_phone": representative_phone.strip(),
                    "is_church_member": is_church_member,
                    "is_cell_member": is_cell_member,
                    "total_people": int(total_people),
                    "adults": int(adults),
                    "children": int(children),
                    "adolescents": int(adolescents),
                    "elderly": int(elderly),
                    "cell_id": cell_id
                })
                st.success("✅ Família cadastrada com sucesso!")
                st.experimental_rerun()

            except Exception as e:
                st.error("❌ Erro ao cadastrar. O telefone pode já existir no sistema.")
                st.exception(e)

st.divider()

# ==========================
# LISTAGEM + BUSCA
# ==========================
st.subheader("📋 Famílias cadastradas")

if not families:
    st.info("Nenhuma família cadastrada ainda.")
    st.stop()

search = st.text_input("🔎 Buscar por nome ou telefone", placeholder="Ex: Diogo / 1199999")

filtered = []
if search.strip():
    s = search.strip().lower()
    for f in families:
        if s in f["representative_name"].lower() or s in f["representative_phone"].lower():
            filtered.append(f)
else:
    filtered = families

df = pd.DataFrame(filtered)

# Adiciona célula como coluna
df["cell_name"] = df["cell_id"].map(cell_id_to_name).fillna("-")

# Ordena melhor e seleciona colunas principais
df_display = df[[
    "representative_name",
    "representative_phone",
    "cell_name",
    "total_people",
    "adults",
    "children",
    "adolescents",
    "elderly",
    "is_church_member",
    "is_cell_member"
]].copy()

df_display.columns = [
    "Representante",
    "Telefone",
    "Célula",
    "Total",
    "Adultos",
    "Crianças",
    "Adolescentes",
    "Idosos",
    "Membro Igreja",
    "Membro Célula"
]

st.dataframe(df_display, use_container_width=True, height=350)

st.divider()

# ==========================
# EDITAR / EXCLUIR
# ==========================
st.subheader("✏️ Editar / 🗑️ Excluir família")

# Cria opções: Nome + Telefone (para evitar confusão)
fam_map = {f"{f['representative_name']} ({f['representative_phone']})": f for f in filtered}
if not fam_map:
    st.warning("Nenhuma família encontrada para editar/excluir com esse filtro.")
    st.stop()

sel = st.selectbox("Selecione uma família", list(fam_map.keys()))
f = fam_map[sel]

st.info(
    f"✅ Selecionada: **{f['representative_name']}**\n\n"
    f"Telefone: **{f['representative_phone']}**"
)

with st.form("edit_family"):
    col1, col2 = st.columns(2)

    with col1:
        rep_name = st.text_input("Representante *", value=f["representative_name"])
        rep_phone = st.text_input("Telefone *", value=f["representative_phone"])
        is_church = st.checkbox("Membro da igreja?", value=f["is_church_member"])
        is_cell = st.checkbox("Membro de célula?", value=f["is_cell_member"])

    with col2:
        total = st.number_input("Total pessoas", min_value=1, step=1, value=int(f["total_people"]))
        adults = st.number_input("Adultos", min_value=0, step=1, value=int(f["adults"]))
        children = st.number_input("Crianças", min_value=0, step=1, value=int(f["children"]))
        adolescents = st.number_input("Adolescentes", min_value=0, step=1, value=int(f["adolescents"]))
        elderly = st.number_input("Idosos", min_value=0, step=1, value=int(f["elderly"]))

    current_cell_name = cell_id_to_name.get(f.get("cell_id"), "(sem célula)")
    cell_opt = st.selectbox(
        "Célula (opcional)",
        ["(sem célula)"] + list(cell_map.keys()),
        index=(["(sem célula)"] + list(cell_map.keys())).index(current_cell_name)
        if current_cell_name in (["(sem célula)"] + list(cell_map.keys())) else 0
    )

    submit = st.form_submit_button("Salvar alterações")

    if submit:
        if not rep_name.strip() or not rep_phone.strip():
            st.error("⚠️ Nome e telefone são obrigatórios.")
        else:
            cell_id = None
            if cell_opt != "(sem célula)":
                cell_id = cell_map[cell_opt]["id"]

            try:
                update_row("families", {"id": f["id"]}, {
                    "representative_name": rep_name.strip(),
                    "representative_phone": rep_phone.strip(),
                    "is_church_member": is_church,
                    "is_cell_member": is_cell,
                    "total_people": int(total),
                    "adults": int(adults),
                    "children": int(children),
                    "adolescents": int(adolescents),
                    "elderly": int(elderly),
                    "cell_id": cell_id
                })
                st.success("✅ Família atualizada!")
                st.experimental_rerun()

            except Exception as e:
                st.error("❌ Erro ao atualizar. O telefone pode já existir em outra família.")
                st.exception(e)

st.divider()

st.warning("⚠️ Excluir família pode quebrar histórico de entregas.")
confirm = st.checkbox("Confirmo exclusão da família selecionada.")

if st.button("Excluir família"):
    if not confirm:
        st.error("Marque a confirmação para excluir.")
    else:
        try:
            delete_row("families", {"id": f["id"]})
            st.success("✅ Família excluída!")
            st.experimental_rerun()
        except Exception as e:
            st.error("❌ Não foi possível excluir. Pode haver entregas registradas para essa família.")
            st.exception(e)
