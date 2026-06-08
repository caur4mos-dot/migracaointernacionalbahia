import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuração da página para aproveitar melhor o espaço horizontal
st.set_page_config(layout="wide")

# ==================================
# TÍTULO GERAL
# ==================================

st.title("📊 Painel do Perfil Sociodemográfico")

st.markdown(
    """
    O objetivo desta aba é trazer uma visualização do Perfil Sociodemográfico junto a visualização temporal dos resultados 
    dos migrantes regularizados no estado da Bahia.
    """
)

# ==================================
# LEITURA DOS DADOS
# ==================================

crescimento = pd.read_csv("dados/crescimento_anual.csv")
sexo = pd.read_csv("dados/sexo_ano.csv")
classificacao = pd.read_csv("dados/classificacao_ano.csv")
heat_continente = pd.read_csv("dados/heat_continente.csv")
heat_amparo = pd.read_csv("dados/heat_amparo.csv")
heat_profissao = pd.read_csv("dados/heat_profissao.csv")

# ==================================
# FILTROS GERAIS (OPÇÃO 1: SLIDER DE INTERVALO)
# ==================================
with st.container(border=True):
    st.markdown("##### 📅 Selecione o Período de Análise")
    
    # Identifica o ano mínimo e máximo diretamente dos seus dados
    ano_minimo = int(crescimento["ano"].min())
    ano_maximo = int(crescimento["ano"].max())
    
    # Cria o controle deslizante com duas pontas para intervalo de anos
    ano_inicio, ano_fim = st.slider(
        label="Arraste para definir o intervalo de anos:",
        label_visibility="collapsed", # Oculta o label interno para ficar mais limpo
        min_value=ano_minimo,
        max_value=ano_maximo,
        value=(ano_minimo, ano_maximo), # Padrão: período completo
        step=1
    )
    
    # Converte o intervalo selecionado em uma lista de anos para os filtros funcionarem
    anos_selecionados = list(range(ano_inicio, ano_fim + 1))

st.markdown("<br>", unsafe_allow_html=True)

# ==================================
# ABAS DOS GRÁFICOS DE LINHA
# ==================================

aba1, aba2, aba3 = st.tabs(
    [
        "📈 Evolução Total",
        "👨👩 Perfil por Sexo",
        "📋 Classificação Migratória"
    ]
)

# ==================================
# EVOLUÇÃO
# ==================================

with aba1:

    st.subheader(
        "Evolução anual da frequência absoluta dos migrantes com registros migratórios na Bahia"
    )

    crescimento_filtrado = crescimento[crescimento["ano"].isin(anos_selecionados)]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=crescimento_filtrado["ano"],
            y=crescimento_filtrado["migrantes"],
            mode="lines+markers+text",
            text=[
                f"{x:,}".replace(",", ".")
                for x in crescimento_filtrado["migrantes"]
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
        height=550,
        template="simple_white",
        showlegend=False,
        xaxis_title="Ano",
        yaxis_title="Número de migrantes"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=anos_selecionados
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# SEXO
# ==================================

with aba2:

    st.subheader(
        "Evolução anual do sexo dos migrantes regularizados na Bahia"
    )

    sexo_filtrado = sexo[sexo["ano"].isin(anos_selecionados)]

    cores = {
        "Masculino": "#333795",
        "Feminino": "#B31D2D",
        "Não especificado": "#F2B134"
    }

    fig = go.Figure()

    for sexo_cat in sexo_filtrado["SEXO"].unique():

        dados = sexo_filtrado[
            sexo_filtrado["SEXO"] == sexo_cat
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
        height=550,
        template="simple_white",
        xaxis_title="Ano",
        yaxis_title="Número de migrantes",
        legend_title="Sexo"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=anos_selecionados
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# CLASSIFICAÇÃO
# ==================================

with aba3:

    st.subheader(
        "Evolução anual das classificações de situação migratória na Bahia"
    )

    classificacao_filtrada = classificacao[classificacao["ano"].isin(anos_selecionados)]

    cores_class = {
        "Temporário": "#333795",
        "Residente": "#B31D2D",
        "Provisório": "#F2B134"
    }

    fig = go.Figure()

    for categoria in classificacao_filtrada["CLASSIFICACAO_REGISTRO"].unique():

        dados = classificacao_filtrada[
            classificacao_filtrada["CLASSIFICACAO_REGISTRO"] == categoria
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
        height=550,
        template="simple_white",
        xaxis_title="Ano",
        yaxis_title="Número de migrantes",
        legend_title="Classificação"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=anos_selecionados
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# SEPARADOR DE SEÇÃO
# ==================================

st.markdown("<hr>", unsafe_allow_html=True)
st.header("📋 Distribuições Percentuais Anuais")

# ==================================
# ABAS DOS HEATMAPS
# ==================================

aba_h1, aba_h2, aba_h3 = st.tabs(
    [
        "🌎 Continente",
        "📄 Tipologia de Amparo",
        "💼 Grupo Profissional"
    ]
)

# ==================================
# PALETA HEATMAP
# ==================================

cores_heatmap = [
    [0.00, "#deebf7"],
    [0.25, "#9ecae1"],
    [0.50, "#3182bd"],
    [0.75, "#6a00a8"],
    [1.00, "#3f007d"]
]

# ==================================
# CONTINENTE
# ==================================

with aba_h1:

    st.subheader(
        "Distribuição percentual por continente de origem"
    )

    heat_continente_filtrado = heat_continente[heat_continente["ano"].isin(anos_selecionados)]

    tabela = heat_continente_filtrado.pivot(
        index="CONTINENTE",
        columns="ano",
        values="percentual"
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=tabela.values,
            x=tabela.columns,
            y=tabela.index,
            colorscale=cores_heatmap,
            text=np.round(tabela.values, 1),
            texttemplate="%{text}%",
            colorbar_title="%"
        )
    )

    fig.update_layout(
        height=500,
        template="simple_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# AMPARO
# ==================================

with aba_h2:

    st.subheader(
        "Distribuição percentual por tipologia de amparo"
    )

    heat_amparo_filtrado = heat_amparo[heat_amparo["ano"].isin(anos_selecionados)]

    tabela = heat_amparo_filtrado.pivot(
        index="TIPOLOGIA_AMPAROS",
        columns="ano",
        values="percentual"
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=tabela.values,
            x=tabela.columns,
            y=tabela.index,
            colorscale=cores_heatmap,
            text=np.round(tabela.values, 1),
            texttemplate="%{text}%",
            colorbar_title="%"
        )
    )

    fig.update_layout(
        height=650,
        template="simple_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================
# PROFISSÃO
# ==================================

with aba_h3:

    st.subheader(
        "Distribuição percentual por grupo profissional"
    )

    heat_profissao_filtrado = heat_profissao[heat_profissao["ano"].isin(anos_selecionados)]

    tabela = heat_profissao_filtrado.pivot(
        index="grupo_profissao",
        columns="ano",
        values="percentual"
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=tabela.values,
            x=tabela.columns,
            y=tabela.index,
            colorscale=cores_heatmap,
            text=np.round(tabela.values, 1),
            texttemplate="%{text}%",
            colorbar_title="%"
        )
    )

    fig.update_layout(
        height=650,
        template="simple_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
