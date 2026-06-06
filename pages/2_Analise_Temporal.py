import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==================================
# CONFIGURAÇÃO
# ==================================

st.title("📈 Análise Temporal")

st.write(
    """
    Evolução anual dos registros migratórios
    internacionais regularizados na Bahia.
    """
)

# ==================================
# CARREGAR DADOS
# ==================================

crescimento = pd.read_csv(
    "dados/crescimento_anual.csv"
)

# ==================================
# INDICADORES
# ==================================

total_migrantes = crescimento["migrantes"].sum()

valor_2021 = crescimento.loc[
    crescimento["ano"] == 2021,
    "migrantes"
].values[0]

valor_2025 = crescimento.loc[
    crescimento["ano"] == 2025,
    "migrantes"
].values[0]

crescimento_percentual = (
    (valor_2025 - valor_2021)
    / valor_2021
) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Migrantes em 2025",
        value=f"{valor_2025:,}".replace(",", ".")
    )

with col2:
    st.metric(
        label="Crescimento 2021–2025",
        value=f"{crescimento_percentual:.1f}%"
    )

with col3:
    st.metric(
        label="Total de Registros",
        value=f"{total_migrantes:,}".replace(",", ".")
    )

st.markdown("---")

# ==================================
# GRÁFICO
# ==================================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=crescimento["ano"],
        y=crescimento["migrantes"],
        mode="lines+markers+text",

        text=[
            f"{x:,}".replace(",", ".")
            for x in crescimento["migrantes"]
        ],

        textposition="top center",

        textfont=dict(
            size=16
        ),

        line=dict(
            color="#333795",
            width=5
        ),

        marker=dict(
            color="#B31D2D",
            size=14
        ),

        hovertemplate=
        "<b>Ano:</b> %{x}<br>" +
        "<b>Migrantes:</b> %{y:,}<extra></extra>"
    )
)

fig.update_layout(

    title=dict(
        text="Evolução dos Registros Migratórios",
        x=0.5,
        font=dict(size=24)
    ),

    height=650,

    paper_bgcolor="white",
    plot_bgcolor="white",

    font=dict(
        size=14
    ),

    showlegend=False,

    margin=dict(
        l=40,
        r=40,
        t=80,
        b=40
    )
)

fig.update_xaxes(
    title="Ano",
    showgrid=False,
    tickmode="linear"
)

fig.update_yaxes(
    title="Número de Migrantes",
    gridcolor="#E5E5E5"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)

# ==================================
# PRÓXIMA ETAPA
# ==================================

st.markdown("---")

st.subheader("Heatmaps Temporais")

st.info(
    """
    Nesta seção serão apresentados os heatmaps
    das características sociodemográficas dos
    migrantes entre 2021 e 2025.
    """
)
