import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==================================
# TÍTULO
# ==================================

st.title("📊 Perfil Sociodemográfico")

st.write(
    """
    Evolução do perfil dos registros migratórios
    internacionais regularizados na Bahia
    entre 2021 e 2025.
    """
)

# ==================================
# LEITURA DOS DADOS
# ==================================

crescimento = pd.read_csv(
    "dados/crescimento_anual.csv"
)

sexo = pd.read_csv(
    "dados/sexo_ano.csv"
)

classificacao = pd.read_csv(
    "dados/classificacao_ano.csv"
)

# ==================================
# ABAS
# ==================================

aba1, aba2, aba3 = st.tabs(
    [
        "📈 Evolução",
        "👨👩 Sexo",
        "📋 Classificação"
    ]
)

# ==================================
# ABA 1 - EVOLUÇÃO
# ==================================

with aba1:

    st.subheader(
        "Evolução anual dos registros migratórios"
    )

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
            line=dict(
                color="#333795",
                width=5
            ),
            marker=dict(
                color="#B31D2D",
                size=12
            )
        )
    )

    fig.update_layout(
        height=600,
        template="simple_white",
        showlegend=False,
        xaxis_title="Ano",
        yaxis_title="Número de migrantes"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[2021, 2022, 2023, 2024, 2025]
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# ABA 2 - SEXO
# ==================================

with aba2:

    st.subheader(
        "Evolução anual segundo sexo"
    )

    cores = {
        "Masculino": "#333795",
        "Feminino": "#B31D2D",
        "Não especificado": "#F2B134"
    }

    fig = go.Figure()

    for sexo_cat in sexo["SEXO"].unique():

        dados = sexo[
            sexo["SEXO"] == sexo_cat
        ]

        fig.add_trace(
            go.Scatter(
                x=dados["ano"],
                y=dados["n"],
                mode="lines+markers+text",
                text=dados["n"],
                textposition="top center",
                name=sexo_cat,
                line=dict(
                    width=4,
                    color=cores.get(
                        sexo_cat,
                        "#444444"
                    )
                ),
                marker=dict(
                    size=10
                )
            )
        )

    fig.update_layout(
        height=600,
        template="simple_white",
        xaxis_title="Ano",
        yaxis_title="Número de migrantes",
        legend_title="Sexo"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[2021, 2022, 2023, 2024, 2025]
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# ABA 3 - CLASSIFICAÇÃO
# ==================================

with aba3:

    st.subheader(
        "Evolução anual segundo classificação do registro"
    )

    cores_class = {
        "Temporário": "#333795",
        "Residente": "#B31D2D",
        "Provisório": "#F2B134"
    }

    fig = go.Figure()

    for categoria in classificacao[
        "CLASSIFICACAO_REGISTRO"
    ].unique():

        dados = classificacao[
            classificacao[
                "CLASSIFICACAO_REGISTRO"
            ] == categoria
        ]

        fig.add_trace(
            go.Scatter(
                x=dados["ano"],
                y=dados["n"],
                mode="lines+markers+text",
                text=dados["n"],
                textposition="top center",
                name=categoria,
                line=dict(
                    width=4,
                    color=cores_class.get(
                        categoria,
                        "#444444"
                    )
                ),
                marker=dict(
                    size=10
                )
            )
        )

    fig.update_layout(
        height=600,
        template="simple_white",
        xaxis_title="Ano",
        yaxis_title="Número de migrantes",
        legend_title="Classificação"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[2021, 2022, 2023, 2024, 2025]
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
