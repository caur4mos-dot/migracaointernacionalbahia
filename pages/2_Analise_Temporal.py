import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ======================
# CONFIGURAÇÃO
# ======================

st.title("Análise Temporal")

st.write(
    """
    Evolução anual dos registros migratórios
    internacionais regularizados na Bahia.
    """
)

# ======================
# DADOS
# ======================

crescimento = pd.read_csv(
    "dados/crescimento_anual.csv"
)

# ======================
# GRÁFICO
# ======================

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=crescimento["ano"],
        y=crescimento["migrantes"],
        mode="lines+markers+text",
        text=crescimento["migrantes"],
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
    height=600,
    xaxis_title="Ano",
    yaxis_title="Número de migrantes",
    template="simple_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================
# TABELA
# ======================

st.subheader("Dados utilizados")

st.dataframe(
    crescimento,
    use_container_width=True
)
