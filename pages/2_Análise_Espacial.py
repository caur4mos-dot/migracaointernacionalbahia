import streamlit as st
import pandas as pd

st.title("Distribuição Espacial")

st.subheader(
    "Limitação dos dados"
)

st.write(
    """
    Antes da visualização espacial, é importante destacar a elevada quantidade de registros sem especificação do município de residência. Essa limitação resulta em perda parcial de informações espaciais, uma vez que parte dos registros não pode ser adequadamente territorializada.
    """
)

nao_esp = pd.read_csv(
    "dados/nao_especificado_municipio.csv"
)

# Renomear colunas
nao_esp = nao_esp.rename(
    columns={
        "ano": "Ano",
        "total_registros": "Total de registros",
        "nao_especificado": "Não especificado",
        "percentual": "Percentual (%)"
    }
)

# Formatar percentual
nao_esp["Percentual (%)"] = (
    nao_esp["Percentual (%)"]
    .astype(str)
    + "%"
)

st.dataframe(
    nao_esp,
    use_container_width=True,
    hide_index=True
)

import streamlit as st
import geopandas as gpd
import folium

from branca.colormap import LinearColormap
from streamlit_folium import st_folium


# =========================
# SELEÇÃO DO ANO
# =========================

st.subheader(
    "Mapa interativo das microrregiões"
)

ano_escolhido = st.radio(
    "Selecione o ano",
    [2021, 2022, 2023, 2024, 2025],
    horizontal=True
)


# =========================
# ARQUIVOS
# =========================

arquivos = {
    2021: "dados/mapa_2021.geojson",
    2022: "dados/mapa_2022.geojson",
    2023: "dados/mapa_2023.geojson",
    2024: "dados/mapa_2024.geojson",
    2025: "dados/mapa_2025.geojson"
}


# =========================
# CARREGAR TODOS
# (para escala fixa)
# =========================

g2021 = gpd.read_file("dados/mapa_2021.geojson")
g2022 = gpd.read_file("dados/mapa_2022.geojson")
g2023 = gpd.read_file("dados/mapa_2023.geojson")
g2024 = gpd.read_file("dados/mapa_2024.geojson")
g2025 = gpd.read_file("dados/mapa_2025.geojson")

todos = pd.concat(
    [g2021, g2022, g2023, g2024, g2025],
    ignore_index=True
)

taxa_min = todos["taxa_100k"].min()
taxa_max = todos["taxa_100k"].max()


# =========================
# CARREGAR ANO SELECIONADO
# =========================

mapa = gpd.read_file(
    arquivos[ano_escolhido]
)

mapa = mapa.to_crs(4326)


# =========================
# PALETA
# =========================

cores = [
    "#deebf7",
    "#9ecae1",
    "#3182bd",
    "#6a00a8",
    "#3f007d"
]

colormap = LinearColormap(
    colors=cores,
    vmin=taxa_min,
    vmax=taxa_max
)

colormap.caption = (
    "Taxa por 100 mil habitantes"
)


# =========================
# CENTRO DO MAPA
# =========================

centro = [
    mapa.geometry.centroid.y.mean(),
    mapa.geometry.centroid.x.mean()
]


# =========================
# MAPA FOLIUM
# =========================

m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles="CartoDB positron"
)


# =========================
# CAMADA
# =========================

folium.GeoJson(
    mapa,

    style_function=lambda feature: {
        "fillColor": (
            "white"
            if (
                feature["properties"]["taxa_100k"] is None
                or feature["properties"]["taxa_100k"] == 0
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
            "Taxa por 100 mil:"
        ],

        localize=True,
        sticky=False
    )

).add_to(m)


colormap.add_to(m)


# =========================
# EXIBIR
# =========================

st_folium(
    m,
    width=None,
    height=700
)

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm
from streamlit_folium import st_folium

# =========================
# TÍTULO
# =========================

st.divider()

st.subheader(
    "Taxa média de migração internacional por microrregião (2021–2025)"
)


# =========================
# LER MAPAS
# =========================

mapa_2021 = gpd.read_file(
    "dados/mapa_2021.geojson"
)

mapa_2022 = gpd.read_file(
    "dados/mapa_2022.geojson"
)

mapa_2023 = gpd.read_file(
    "dados/mapa_2023.geojson"
)

mapa_2024 = gpd.read_file(
    "dados/mapa_2024.geojson"
)

mapa_2025 = gpd.read_file(
    "dados/mapa_2025.geojson"
)

# =========================
# JUNTAR TODOS
# =========================

todos = pd.concat(
    [
        mapa_2021,
        mapa_2022,
        mapa_2023,
        mapa_2024,
        mapa_2025
    ],
    ignore_index=True
)

# =========================
# MÉDIA POR MICRORREGIÃO
# =========================

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

# =========================
# GEOMETRIA
# =========================

geometria = mapa_2025[
    [
        "name_micro",
        "geometry"
    ]
]

# =========================
# UNIR
# =========================

mapa_media = geometria.merge(
    media,
    on="name_micro",
    how="left"
)

# =========================
# ZEROS BRANCOS
# =========================

mapa_media["media_taxa_plot"] = (
    mapa_media["media_taxa"]
)

mapa_media.loc[
    mapa_media["media_taxa_plot"] == 0,
    "media_taxa_plot"
] = None

# =========================
# MESMAS CORES DO R
# =========================

cores = [
    "#deebf7",
    "#9ecae1",
    "#3182bd",
    "#6a00a8",
    "#3f007d"
]

# =========================
# LIMITES
# =========================

taxa_min = (
    mapa_media["media_taxa_plot"]
    .dropna()
    .min()
)

taxa_max = (
    mapa_media["media_taxa_plot"]
    .dropna()
    .max()
)

# =========================
# ESCALA CONTÍNUA
# =========================

colormap = cm.LinearColormap(
    colors=cores,
    vmin=taxa_min,
    vmax=taxa_max
)

# =========================
# MAPA
# =========================

centro = [
    mapa_media.geometry.centroid.y.mean(),
    mapa_media.geometry.centroid.x.mean()
]

m = folium.Map(
    location=centro,
    zoom_start=6,
    tiles="CartoDB positron"
)

# =========================
# ESTILO
# =========================

def estilo(feature):

    valor = feature["properties"]["media_taxa_plot"]

    if valor is None:
        cor = "white"
    else:
        cor = colormap(valor)

    return {
        "fillColor": cor,
        "color": "black",
        "weight": 1,
        "fillOpacity": 1
    }

# =========================
# TOOLTIP
# =========================

tooltip = folium.GeoJsonTooltip(
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
        "Taxa média por 100 mil:"
    ],
    localize=True,
    sticky=False
)

# =========================
# GEOJSON
# =========================

folium.GeoJson(
    mapa_media,
    style_function=estilo,
    tooltip=tooltip,
    zoom_on_click=False
).add_to(m)

# =========================
# LEGENDA
# =========================

colormap.caption = (
    "Taxa média por 100 mil habitantes"
)

colormap.add_to(m)

# =========================
# EXIBIR
# =========================

st_folium(
    m,
    use_container_width=True,
    height=700
)
