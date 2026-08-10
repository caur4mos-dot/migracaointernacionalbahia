import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import plotly.express as px

from branca.colormap import LinearColormap
from streamlit_folium import st_folium


# =====================================================
# TÍTULO
# =====================================================

st.title("Predição dos Fluxos Migratórios para 2026")

st.write(
    """
    Esta seção apresenta a predição da taxa de migrantes
    internacionais regularizados por 100 mil habitantes
    nas microrregiões da Bahia para o ano de 2026.
    """
)


# =====================================================
# LEITURA DOS DADOS
# =====================================================

mapa_2026 = gpd.read_file(
    "dados/mapa_predicao_2026.geojson"
)

metricas = pd.read_csv(
    "dados/metricas_validacao.csv"
)


# =====================================================
# MAPA INTERATIVO
# =====================================================

st.subheader(
    "Mapa Interativo da Predição para 2026"
)

taxa_min = 0
taxa_max = 40

colormap = LinearColormap(
    colors=[
        "#F2F2F2",
        "#FFFF00",
        "#F5E400",
        "#FFA500",
        "#FF0000"
    ],
    vmin=taxa_min,
    vmax=taxa_max
)

colormap.caption = (
    "Taxa prevista por 100 mil habitantes"
)


# =====================================================
# CENTRO DO MAPA
# =====================================================

centro = [
    mapa_2026.geometry.centroid.y.mean(),
    mapa_2026.geometry.centroid.x.mean()
]

m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles="CartoDB positron"
)


# =====================================================
# CAMADA DO MAPA
# =====================================================

folium.GeoJson(
    mapa_2026,

    style_function=lambda feature: {

        "fillColor":
            "white"
            if (
                feature["properties"].get(
                    "taxa_prevista_2026"
                ) == 0
                or feature["properties"].get(
                    "taxa_prevista_2026"
                ) is None
            )
            else colormap(
                feature["properties"][
                    "taxa_prevista_2026"
                ]
            ),

        "color": "black",

        "weight": 1,

        "fillOpacity": 1
    },

    tooltip=folium.GeoJsonTooltip(

        fields=[
            "name_micro",
            "taxa_prevista_2026"
        ],

        aliases=[
            "Microrregião:",
            "Taxa prevista 2026:"
        ],

        localize=True,

        sticky=False
    )

).add_to(m)


# =====================================================
# LEGENDA
# =====================================================

colormap.add_to(m)


# =====================================================
# EXIBIR MAPA
# =====================================================

st_folium(
    m,
    use_container_width=True,
    height=700
)


# =====================================================
# VALIDAÇÃO
# =====================================================

st.divider()

st.header(
    "Validação do Modelo"
)

st.write(
    """
    Antes da realização da predição para 2026,
    o modelo foi submetido a uma validação temporal.

    Em cada etapa, foram utilizados apenas os dados
    disponíveis nos anos anteriores para realizar a
    previsão do ano subsequente. O procedimento foi
    aplicado aos anos de 2023, 2024 e 2025, permitindo
    avaliar o desempenho do modelo em diferentes
    períodos do histórico analisado.
    """
)


# =====================================================
# MÉTRICAS POR ANO
# =====================================================

st.subheader(
    "Métricas de validação"
)


# arredondamento apenas para exibição
metricas_exibicao = metricas.copy()

metricas_exibicao["mae"] = (
    metricas_exibicao["mae"].round(2)
)

metricas_exibicao["mape"] = (
    metricas_exibicao["mape"].round(1)
)

metricas_exibicao["correlacao_spearman"] = (
    metricas_exibicao[
        "correlacao_spearman"
    ].round(2)
)


# =====================================================
# TABELA DE MÉTRICAS
# =====================================================

st.dataframe(
    metricas_exibicao.rename(
        columns={
            "ano_teste": "Ano",
            "n": "N",
            "mae": "MAE",
            "mape": "MAPE (%)",
            "correlacao_spearman":
                "Correlação de Spearman"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# =====================================================
# DESTAQUES DA VALIDAÇÃO
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

    mae_medio = metricas["mae"].mean()

    st.metric(
        "MAE médio",
        f"{mae_medio:.2f}"
    )


with col2:

    mape_medio = metricas["mape"].mean()

    st.metric(
        "MAPE médio",
        f"{mape_medio:.1f}%"
    )


with col3:

    spearman_medio = (
        metricas[
            "correlacao_spearman"
        ].mean()
    )

    st.metric(
        "Spearman médio",
        f"{spearman_medio:.2f}"
    )
