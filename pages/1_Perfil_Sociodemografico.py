import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =========================
# CARREGAR DADOS
# =========================

crescimento_anual = pd.read_csv(
    "dados/crescimento_anual.csv"
)

# =========================
# TÍTULO
# =========================

st.title("Perfil Sociodemográfico")

st.subheader("Evolução anual da frequência absoluta dos migrantes com registros migratórios na Bahia
")

# =========================
# GRÁFICO
# =========================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=crescimento_anual["ano"],
        y=crescimento_anual["migrantes"],
        mode="lines+markers+text",
        text=crescimento_anual["migrantes"],
        textposition="top center",
        line=dict(
            color="#333795",
            width=4
        ),
        marker=dict(
            color="#b31d2d",
            size=10
        ),
        name="Migrantes"
    )
)

fig.update_layout(
    template="simple_white",
    height=600,
    xaxis_title="Ano",
    yaxis_title="Número de migrantes",
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(crescimento_anual)
