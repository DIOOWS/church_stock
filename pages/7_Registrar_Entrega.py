import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.db import fetch_table

st.title("📊 Relatórios — Entregas e Exportação")

deliveries = fetch_table("deliveries", order="delivered_at")
families = fetch_table("families")
leaders = fetch_table("cell_leaders")
baskets = fetch_table("basket_types")
cells = fetch_table("cells")
supers = fetch_table("supervisors")

if not deliveries:
    st.info("Nenhuma entrega registrada ainda.")
    st.stop()

fam_map = {f["id"]: f for f in families}
leader_map = {l["id"]: l for l in leaders}
basket_map = {b["id"]: b for b in baskets}
cell_map = {c["id"]: c for c in cells}
super_map = {s["id"]: s for s in supers}

rows = []
for d in deliveries:
    fam = fam_map.get(d["family_id"])
    leader = leader_map.get(d["leader_id"])
    basket = basket_map.get(d["basket_type_id"])

    cell = cell_map.get(fam.get("cell_id")) if fam else None
    cell_name = cell["cell_name"] if cell else "-"
    cell_network = cell["network_name"] if cell else "-"

    supervisor = None
    if cell and cell.get("supervisor_id"):
        supervisor = super_map.get(cell["supervisor_id"])

    supervisor_name = supervisor["name"] if supervisor else "-"
    supervisor_phone = supervisor["phone"] if supervisor else "-"

    rows.append({
        "Data": d["delivered_at"],
        "Representante": fam["representative_name"] if fam else "-",
        "Telefone Representante": fam["representative_phone"] if fam else "-",
        "Célula": cell_name,
        "Rede da Célula": cell_network,
        "Supervisor": supervisor_name,
        "Telefone Supervisor": supervisor_phone,
        "Líder": leader["name"] if leader else "-",
        "Telefone Líder": leader["phone"] if leader else "-",
        "Rede do Líder": leader["network_name"] if leader else "-",
        "Cesta": basket["name"] if basket else "-",
        "Quantidade": d["quantity"]
    })

df = pd.DataFrame(rows)
df["Data"] = pd.to_datetime(df["Data"])

st.subheader("🔎 Filtros")

col1, col2, col3 = st.columns(3)
with col1:
    start = st.date_input("Data inicial", value=datetime.now().date() - timedelta(days=30))
with col2:
    end = st.date_input("Data final", value=datetime.now().date())
with col3:
    network_cell = st.selectbox("Rede da Célula", ["(todas)"] + sorted(df["Rede da Célula"].unique().tolist()))

leader_filter = st.selectbox("Líder", ["(todos)"] + sorted(df["Líder"].unique().tolist()))
basket_filter = st.selectbox("Tipo de cesta", ["(todas)"] + sorted(df["Cesta"].unique().tolist()))
cell_filter = st.selectbox("Célula", ["(todas)"] + sorted(df["Célula"].unique().tolist()))
supervisor_filter = st.selectbox("Supervisor", ["(todos)"] + sorted(df["Supervisor"].unique().tolist()))

f = df[(df["Data"].dt.date >= start) & (df["Data"].dt.date <= end)]
if network_cell != "(todas)":
    f = f[f["Rede da Célula"] == network_cell]
if leader_filter != "(todos)":
    f = f[f["Líder"] == leader_filter]
if basket_filter != "(todas)":
    f = f[f["Cesta"] == basket_filter]
if cell_filter != "(todas)":
    f = f[f["Célula"] == cell_filter]
if supervisor_filter != "(todos)":
    f = f[f["Supervisor"] == supervisor_filter]

st.subheader("📋 Resultados")
st.dataframe(f.sort_values("Data", ascending=False), use_container_width=True)

st.subheader("📥 Exportação")
csv = f.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Baixar CSV (Excel)",
    csv,
    file_name="relatorio_entregas.csv",
    mime="text/csv"
)

st.divider()
st.subheader("📌 Resumo")
colA, colB, colC = st.columns(3)
colA.metric("Entregas", len(f))
colB.metric("Total de cestas entregues", int(f["Quantidade"].sum()))
colC.metric("Famílias atendidas", f["Telefone Representante"].nunique())
