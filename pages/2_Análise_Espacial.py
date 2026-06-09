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

# ==================================
# MAPA INTERATIVO DA MÉDIA 2021-2025
# ==================================

import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium

st.divider()

st.subheader(
    "Taxa média de migração internacional por microrregião (2021–2025)"
)

st.write(
    """
    O mapa apresenta a taxa média anual de migrantes
    internacionais regularizados por 100 mil habitantes
    nas microrregiões da Bahia entre 2021 e 2025.

    A média reduz oscilações específicas de cada ano
    e permite identificar os territórios que mantiveram
    maior intensidade migratória ao longo do período.
    """
)

# ==================================
# LEITURA DOS GEOJSON
# ==================================

g2021 = gpd.read_file("dados/mapa_2021.geojson")
g2022 = gpd.read_file("dados/mapa_2022.geojson")
g2023 = gpd.read_file("dados/mapa_2023.geojson")
g2024 = gpd.read_file("dados/mapa_2024.geojson")
g2025 = gpd.read_file("dados/mapa_2025.geojson")

# ==================================
# JUNTAR TODOS OS ANOS
# ==================================

todos = pd.concat(
    [g2021, g2022, g2023, g2024, g2025],
    ignore_index=True
)

# ==================================
# CALCULAR MÉDIAS
# ==================================

medias = (
    todos
    .groupby("name_micro")
    .agg(
        media_migrantes=("total_migrantes", "mean"),
        media_populacao=("populacao", "mean"),
        media_taxa=("taxa_100k", "mean")
    )
    .reset_index()
)

# ==================================
# GEOMETRIA ÚNICA
# ==================================

geometria = g2025[
    ["name_micro", "geometry"]
].copy()

mapa_media = geometria.merge(
    medias,
    on="name_micro",
    how="left"
)

# ==================================
# MAPA
# ==================================

m = folium.Map(
    location=[-12.8, -41.5],
    zoom_start=6,
    tiles="CartoDB positron"
)

folium.Choropleth(
    geo_data=mapa_media,
    data=mapa_media,
    columns=["name_micro", "media_taxa"],
    key_on="feature.properties.name_micro",
    fill_color="PuBuGn",
    fill_opacity=0.9,
    line_opacity=0.8,
    legend_name="Taxa média por 100 mil habitantes"
).add_to(m)

# ==================================
# TOOLTIP
# ==================================

tooltip = folium.GeoJsonTooltip(
    fields=[
        "name_micro",
        "media_migrantes",
        "media_populacao",
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

folium.GeoJson(
    mapa_media,
    tooltip=tooltip,
    style_function=lambda x: {
        "color": "black",
        "weight": 1
    }
).add_to(m)

# ==================================
# EXIBIR
# ==================================

st_folium(
    m,
    use_container_width=True,
    height=700
)
