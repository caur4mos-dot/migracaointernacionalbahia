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
# FILTROS GERAIS (OPÇÃO 3: SELECTBOX ÚNICA)
# ==================================
with st.container(border=True):
    st.markdown("##### 📅 Filtrar por Ano Específico")
    
    # Lista única de anos disponíveis nos seus dados
    anos_disponiveis = sorted(crescimento["ano"].unique())
    
    # Caixa de seleção simples para escolher apenas um ano
    ano_selecionado = st.selectbox(
        label="Selecione o ano desejado:",
        options=anos_disponiveis,
        index=len(anos_disponiveis) - 1 # Define o último ano (2025) como padrão inicial
    )

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
        f"Frequência absoluta dos migrantes com registros migratórios na Bahia em {ano_selecionado}"
    )

    # Filtragem exata do ano selecionado
    crescimento_filtrado = crescimento[crescimento["ano"] == ano_selecionado]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=crescimento_filtrado["ano"],
            y=crescimento_filtrado["migrantes"],
            mode="markers+text", # Como é só um ponto, mudamos para marcadores e texto
            text=[
                f"{x:,}".replace(",", ".")
                for x in crescimento_filtrado["migrantes"]
            ],
            textposition="top center",
            marker=dict(
                color="#B31D2D",
                size=14
            )
        )
    )

    fig.update_layout(
        height=400,
        template="simple_white",
        showlegend=False,
        xaxis_title="Ano",
        yaxis_title="Número de migrantes"
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[ano_selecionado]
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
        f"Distribuição por sexo dos migrantes regularizados na Bahia em {ano_selecionado}"
    )

    # Filtragem exata do ano selecionado
    sexo_filtrado = sexo[sexo["ano"] == ano_selecionado]

    cores = {
        "Masculino": "#333795",
        "Feminino": "#B31D2D",
        "Não especificado": "#F2B134"
    }

    fig = go.Figure()

    # Como mudamos para ano único, um gráfico de Barras fica esteticamente melhor que linhas de ponto único
    fig.add_trace(
        go.Bar(
            x=sexo_filtrado["SEXO"],
            y=sexo_filtrado["n"],
            text=sexo_filtrado["n"],
            textposition="auto",
            marker_color=[cores.get(cat, "#444444") for cat in sexo_filtrado["SEXO"]]
        )
    )

    fig.update_layout(
        height=450,
        template="simple_white",
        xaxis_title="Sexo",
        yaxis_title="Número de migrantes",
        showlegend=False
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
        f"Classificações de situação migratória na Bahia em {ano_selecionado}"
    )

    # Filtragem exata do ano selecionado
    classificacao_filtrada = classificacao[classificacao["ano"] == ano_selecionado]

    cores_class = {
        "Temporário": "#333795",
        "Residente": "#B31D2D",
        "Provisório": "#F2B134"
    }

    fig = go.Figure()

    # Mudado para gráfico de Barras para melhor representação de ponto único no tempo
    fig.add_trace(
        go.Bar(
            x=classificacao_filtrada["CLASSIFICACAO_REGISTRO"],
            y=classificacao_filtrada["n"],
            text=classificacao_filtrada["n"],
            textposition="auto",
            marker_color=[cores_class.get(cat, "#444444") for cat in classificacao_filtrada["CLASSIFICACAO_REGISTRO"]]
        )
    )

    fig.update_layout(
        height=450,
        template="simple_white",
        xaxis_title="Classificação",
        yaxis_title="Número de migrantes",
        showlegend=False
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
st.header("📋 Distribuições Percentuais")

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
        f"Distribuição percentual por continente de origem ({ano_selecionado})"
    )

    heat_continente_filtrado = heat_continente[heat_continente["ano"] == ano_selecionado]

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
        f"Distribuição percentual por tipologia de amparo ({ano_selecionado})"
    )

    heat_amparo_filtrado = heat_amparo[heat_amparo["ano"] == ano_selecionado]

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
        f"Distribuição percentual por grupo profissional ({ano_selecionado})"
    )

    heat_profissao_filtrado = heat_profissao[heat_profissao["ano"] == ano_selecionado]

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
