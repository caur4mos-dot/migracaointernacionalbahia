import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import pyreadr

from branca.colormap import LinearColormap
from streamlit_folium import st_folium


# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.title("Predição dos Fluxos Migratórios para 2026")

st.write(
    """
    Esta seção apresenta a predição da taxa de migrantes
    internacionais regularizados por 10 mil habitantes
    nas microrregiões da Bahia para o ano de 2026.
    """
)


# =====================================================
# LEITURA DO MAPA
# =====================================================

@st.cache_data
def carregar_mapa_2026():

    mapa = gpd.read_file(
        "dados/mapa_predicao_2026.geojson"
    )

    return mapa.to_crs(epsg=4326)


mapa_2026 = carregar_mapa_2026()


# =====================================================
# LEITURA DAS MÉTRICAS
# =====================================================

@st.cache_data
def carregar_metricas():

    resultado_rds = pyreadr.read_r(
        "dados/metricas_validacao_2023_2025.rds"
    )

    metricas = list(resultado_rds.values())[0]

    # Padronização dos nomes das colunas

    metricas.columns = [
        str(col).strip().lower()
        for col in metricas.columns
    ]

    # Padronização dos nomes utilizados na página

    metricas = metricas.rename(
        columns={
            "ano_teste": "ano",
            "correlacao_spearman": "spearman",
            "mae": "mae",
            "mape": "mape"
        }
    )

    return metricas


metricas = carregar_metricas()


# =====================================================
# MAPA INTERATIVO
# =====================================================

st.subheader(
    "Mapa Interativo da Predição para 2026"
)


taxa_min = 0
taxa_max = 4


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
    "Taxa prevista por 10 mil habitantes"
)


# =====================================================
# CENTRO DO MAPA
# =====================================================

centro = [
    mapa_2026.geometry.centroid.y.mean(),
    mapa_2026.geometry.centroid.x.mean()
]


# =====================================================
# CONSTRUÇÃO DO MAPA
# =====================================================

m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles="CartoDB positron"
)


folium.GeoJson(
    mapa_2026,

    style_function=lambda feature: {

        "fillColor":
            "white"
            if (
                feature["properties"].get(
                    "taxa_prevista_2026"
                ) is None
                or feature["properties"].get(
                    "taxa_prevista_2026"
                ) == 0
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
            "Taxa prevista por 10 mil habitantes:"
        ],

        localize=True,

        sticky=False
    )

).add_to(m)


colormap.add_to(m)


# =====================================================
# EXIBIÇÃO DO MAPA
# =====================================================

st_folium(
    m,
    use_container_width=True,
    height=700
)


# =====================================================
# VALIDAÇÃO DO MODELO
# =====================================================

st.divider()

st.header(
    "Validação do Modelo"
)


st.write(
    """
    Antes da realização da predição para 2026,
    o modelo foi submetido a uma validação temporal
    do tipo walk-forward, utilizando os anos de 2023,
    2024 e 2025 como períodos de teste.

    Em cada etapa, o modelo foi treinado utilizando
    exclusivamente informações disponíveis nos anos
    anteriores ao período de teste. As taxas previstas
    foram então comparadas com os valores efetivamente
    observados.
    """
)


# =====================================================
# MÉTRICAS DE VALIDAÇÃO
# =====================================================

st.subheader(
    "Métricas de validação"
)


if "ano" not in metricas.columns:

    st.error(
        "A coluna de ano não foi encontrada no arquivo de métricas."
    )

else:

    for _, linha in metricas.iterrows():

        ano = int(linha["ano"])

        st.markdown(
            f"### Ano de teste: {ano}"
        )

        col1, col2, col3 = st.columns(3)


        # ---------------------------------------------
        # MAE
        # ---------------------------------------------

        with col1:

            if "mae" in metricas.columns:

                st.metric(
                    "Erro Absoluto Médio (MAE)",
                    f"{float(linha['mae']):.2f}"
                )


        # ---------------------------------------------
        # MAPE
        # ---------------------------------------------

        with col2:

            if "mape" in metricas.columns:

                st.metric(
                    "Erro Percentual Absoluto Médio (MAPE)",
                    f"{float(linha['mape']):.1f}%"
                )


        # ---------------------------------------------
        # SPEARMAN
        # ---------------------------------------------

        with col3:

            if "spearman" in metricas.columns:

                st.metric(
                    "Correlação de Spearman",
                    f"{float(linha['spearman']):.2f}"
                )


        st.divider()
