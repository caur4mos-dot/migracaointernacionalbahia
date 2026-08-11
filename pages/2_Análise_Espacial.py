import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm

from streamlit_folium import st_folium


# =========================================================
# TÍTULO
# =========================================================

st.title("Distribuição Espacial")


# =========================================================
# CORES
# =========================================================

CORES = [
    "#deebf7",
    "#9ecae1",
    "#3182bd",
    "#6a00a8",
    "#3f007d"
]


# =========================================================
# LIMITAÇÃO DOS DADOS
# =========================================================

st.subheader("Limitação dos dados")

st.write(
    """
    Antes da visualização espacial, é importante destacar a elevada
    quantidade de registros sem especificação do município de residência.
    Essa limitação resulta em perda parcial de informações espaciais,
    uma vez que parte dos registros não pode ser adequadamente
    territorializada.
    """
)


@st.cache_data
def carregar_nao_especificado():

    dados = pd.read_csv(
        "dados/nao_especificado_municipio.csv"
    )

    dados = dados.rename(
        columns={
            "ano": "Ano",
            "total_registros": "Total de registros",
            "nao_especificado": "Não especificado",
            "percentual": "Percentual (%)"
        }
    )

    dados["Percentual (%)"] = (
        dados["Percentual (%)"].astype(str) + "%"
    )

    return dados


nao_esp = carregar_nao_especificado()

st.dataframe(
    nao_esp,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CARREGAMENTO DOS MAPAS
# =========================================================

@st.cache_data
def carregar_mapas():

    mapas = {}

    for ano in [2021, 2022, 2023, 2024, 2025]:

        caminho = f"dados/mapa_{ano}.geojson"

        mapa = gpd.read_file(caminho)

        # Garante latitude/longitude
        mapa = mapa.to_crs(epsg=4326)

        mapas[ano] = mapa

    return mapas


mapas = carregar_mapas()


# =========================================================
# TODOS OS MAPAS JUNTOS
# =========================================================

@st.cache_data
def preparar_dados_globais(mapas):

    todos = pd.concat(
        [
            mapas[2021],
            mapas[2022],
            mapas[2023],
            mapas[2024],
            mapas[2025]
        ],
        ignore_index=True
    )

    taxa_min = todos["taxa_100k"].min()
    taxa_max = todos["taxa_100k"].max()

    return todos, taxa_min, taxa_max


todos, taxa_min, taxa_max = preparar_dados_globais(mapas)


# =========================================================
# MAPA INTERATIVO POR ANO
# =========================================================

st.divider()

st.subheader(
    "Mapa interativo das microrregiões"
)


ano_escolhido = st.radio(
    "Selecione o ano",
    [2021, 2022, 2023, 2024, 2025],
    horizontal=True
)


# =========================================================
# MAPA SELECIONADO
# =========================================================

mapa = mapas[ano_escolhido]


# =========================================================
# PALETA
# =========================================================

colormap = cm.LinearColormap(
    colors=CORES,
    vmin=taxa_min,
    vmax=taxa_max
)

colormap.caption = (
    "Taxa por 10 mil habitantes"
)


# =========================================================
# CENTRO DO MAPA
# =========================================================

centro = [
    mapa.geometry.centroid.y.mean(),
    mapa.geometry.centroid.x.mean()
]


# =========================================================
# MAPA FOLIUM
# =========================================================

m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles="CartoDB positron"
)


# =========================================================
# CAMADA
# =========================================================

folium.GeoJson(

    mapa,

    style_function=lambda feature: {

        "fillColor": (
            "white"
            if (
                feature["properties"].get("taxa_100k") is None
                or feature["properties"].get("taxa_100k") == 0
            )
            else colormap(
                feature["properties"]["taxa_100k"]
            )
        ),

        "color": "black",
        "weight": 1,
        "fillOpacity": 0.9
    },

    tooltip=folium.GeoJsonTooltip(

        fields=[
            "name_micro",
            "total_migrantes",
            "populacao",
            "taxa_100k"
        ],

        aliases=[
            "Microrregião:",
            "Migrantes:",
            "População:",
            "Taxa por 10 mil:"
        ],

        localize=True,
        sticky=False
    )

).add_to(m)


# =========================================================
# LEGENDA
# =========================================================

colormap.add_to(m)


# =========================================================
# EXIBIR MAPA
# =========================================================

st_folium(
    m,
    width=None,
    height=700
)


# =========================================================
# TAXA MÉDIA 2021–2025
# =========================================================

st.divider()

st.subheader(
    "Taxa média de migração internacional por microrregião (2021–2025)"
)


# =========================================================
# CALCULAR MÉDIA
# =========================================================

@st.cache_data
def calcular_media(todos):

    media = (
        todos
        .groupby("name_micro")
        .agg(
            media_migrantes=(
                "total_migrantes",
                "mean"
            ),

            media_pop=(
                "populacao",
                "mean"
            ),

            media_taxa=(
                "taxa_100k",
                "mean"
            )
        )
        .reset_index()
    )

    return media


media = calcular_media(todos)


# =========================================================
# GEOMETRIA
# =========================================================

@st.cache_data
def construir_mapa_media(mapas, media):

    geometria = mapas[2025][
        [
            "name_micro",
            "geometry"
        ]
    ].copy()

    mapa_media = geometria.merge(
        media,
        on="name_micro",
        how="left"
    )

    mapa_media["media_taxa_plot"] = (
        mapa_media["media_taxa"]
    )

    mapa_media.loc[
        mapa_media["media_taxa_plot"] == 0,
        "media_taxa_plot"
    ] = None

    return mapa_media


mapa_media = construir_mapa_media(
    mapas,
    media
)


# =========================================================
# LIMITES DA MÉDIA
# =========================================================

taxa_min_media = (
    mapa_media["media_taxa_plot"]
    .dropna()
    .min()
)

taxa_max_media = (
    mapa_media["media_taxa_plot"]
    .dropna()
    .max()
)


# =========================================================
# PALETA DA MÉDIA
# =========================================================

colormap_media = cm.LinearColormap(
    colors=CORES,
    vmin=taxa_min_media,
    vmax=taxa_max_media
)

colormap_media.caption = (
    "Taxa média por 10 mil habitantes"
)


# =========================================================
# CENTRO
# =========================================================

centro_media = [
    mapa_media.geometry.centroid.y.mean(),
    mapa_media.geometry.centroid.x.mean()
]


# =========================================================
# MAPA DA MÉDIA
# =========================================================

m_media = folium.Map(
    location=centro_media,
    zoom_start=6,
    tiles="CartoDB positron"
)


# =========================================================
# ESTILO
# =========================================================

def estilo_media(feature):

    valor = feature["properties"]["media_taxa_plot"]

    if valor is None:
        cor = "white"
    else:
        cor = colormap_media(valor)

    return {
        "fillColor": cor,
        "color": "black",
        "weight": 1,
        "fillOpacity": 1
    }


# =========================================================
# TOOLTIP
# =========================================================

tooltip_media = folium.GeoJsonTooltip(

    fields=[
        "name_micro",
        "media_migrantes",
        "media_pop",
        "media_taxa"
    ],

    aliases=[
        "Microrregião:",
        "Média de migrantes:",
        "Média populacional:",
        "Taxa média por 10 mil:"
    ],

    localize=True,
    sticky=False
)


# =========================================================
# GEOJSON
# =========================================================

folium.GeoJson(

    mapa_media,

    style_function=estilo_media,

    tooltip=tooltip_media,

    zoom_on_click=False

).add_to(m_media)


# =========================================================
# LEGENDA
# =========================================================

colormap_media.add_to(m_media)


# =========================================================
# EXIBIR
# =========================================================

st_folium(
    m_media,
    use_container_width=True,
    height=700
)
