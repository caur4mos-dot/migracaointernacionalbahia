import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ==================================
# CONFIGURAÇÃO
# ==================================

st.title("📈 Análise Temporal")

st.write(
    """
    Evolução dos registros migratórios
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
# ABA 1
# ==================================

with aba1:

    total_migrantes = crescimento["migrantes"].sum()

    valor_2021 = crescimento.loc[
        crescimento["ano"] == 2021,
        "migrantes"
    ].values[0]

    valor_2025 = crescimento.loc[
        crescimento["ano"] == 2025,
        "migrantes"
    ].values[0]

    crescimento_pct = (
        (valor_2025 - valor_2021)
        / valor_2021
    ) * 100

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Migrantes em 2025",
        f"{valor_2025:,}".replace(",", ".")
    )

    col2.metric(
        "Crescimento",
        f"{crescimento_pct:.1f}%"
    )

    col3.metric(
        "Total",
        f"{total_migrantes:,}".replace(",", ".")
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

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# ABA 2
# ==================================

with aba2:

    fig = go.Figure()

    cores = {
        "Masculino": "#333795",
        "Feminino": "#B31D2D",
        "Não especificado": "#f2b134"
    }

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
        yaxis_title="Número de migrantes"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# ABA 3
# ==================================

with aba3:

    cores_class = {
        "Temporário": "#333795",
        "Residente": "#B31D2D",
        "Provisório": "#f2b134"
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
        yaxis_title="Número de migrantes"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
