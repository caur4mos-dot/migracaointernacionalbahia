import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm

from streamlit_folium import st_folium


# =========================================================
# CONFIGURAÇÃO
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


# =========================================================
# TABELA DE REGISTROS SEM MUNICÍPIO
# =========================================================

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
# ARQUIVOS DOS MAPAS
# =========================================================

ARQUIVOS_MAPAS = {
    2021: "dados/mapa_2021.geojson",
    2022: "dados/mapa_2022.geojson",
    2023: "dados/mapa_2023.geojson",
    2024: "dados/mapa_2024.geojson",
    2025: "dados/mapa_2025.geojson"
}


# =========================================================
# CARREGAR MAPAS
# =========================================================

@st.cache_data
def carregar_mapas():

    mapa_2021 = gpd.read_file(
        ARQUIVOS_MAPAS[2021]
    ).to_crs(4326)

    mapa_2022 = gpd.read_file(
        ARQUIVOS_MAPAS[2022]
    ).to_crs(4326)

    mapa_2023 = gpd.read_file(
        ARQUIVOS_MAPAS[2023]
    ).to_crs(4326)

    mapa_2024 = gpd.read_file(
        ARQUIVOS_MAPAS[2024]
    ).to_crs(4326)

    mapa_2025 = gpd.read_file(
        ARQUIVOS_MAPAS[2025]
    ).to_crs(4326)

    return (
        mapa_2021,
        mapa_2022,
        mapa_2023,
        mapa_2024,
        mapa_2025
    )


(
    mapa_2021,
    mapa_2022,
    mapa_2023,
    mapa_2024,
    mapa_2025
) = carregar_mapas()


# =========================================================
# ESCALA GLOBAL
# =========================================================

@st.cache_data
def calcular_limites(
    mapa_2021,
    mapa_2022,
    mapa_2023,
    mapa_2024,
    mapa_2025
):

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

    taxa_min = todos["taxa_100k"].min()
    taxa_max = todos["taxa_100k"].max()

    return taxa_min, taxa_max


taxa_min, taxa_max = calcular_limites(
    mapa_2021,
    mapa_2022,
    mapa_2023,
    mapa_2024,
    mapa_2025
)


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
# SELECIONAR MAPA
# =========================================================

mapas = {
    2021: mapa_2021,
    2022: mapa_2022,
    2023: mapa_2023,
    2024: mapa_2024,
    2025: mapa_2025
}

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
# CENTRO
# =========================================================

centro = [
    mapa.geometry.centroid.y.mean(),
    mapa.geometry.centroid.x.mean()
]


# =========================================================
# MAPA
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
            "Taxa por 10 mil:"
        ],

        localize=True,
        sticky=False
    )

).add_to(m)


colormap.add_to(m)


# =========================================================
# EXIBIR
# =========================================================

st_folium(
    m,
    use_container_width=True,
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
def calcular_media(
    mapa_2021,
    mapa_2022,
    mapa_2023,
    mapa_2024,
    mapa_2025
):

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

    geometria = mapa_2025[
        [
            "name_micro",
            "geometry"
        ]
    ]

    mapa_media = geometria.merge(
        media,
        on="name_micro",
        how="left"
    )

    return mapa_media


mapa_media = calcular_media(
    mapa_2021,
    mapa_2022,
    mapa_2023,
    mapa_2024,
    mapa_2025
)


# =========================================================
# ZEROS COMO BRANCO
# =========================================================

mapa_media["media_taxa_plot"] = (
    mapa_media["media_taxa"]
)

mapa_media.loc[
    mapa_media["media_taxa_plot"] == 0,
    "media_taxa_plot"
] = None


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
# MAPA
# =========================================================

folium.GeoJson(
    mapa_media,
    style_function=estilo_media,
    tooltip=tooltip_media,
    zoom_on_click=False
).add_to(m_media)


colormap_media.add_to(m_media)


# =========================================================
# EXIBIR
# =========================================================

st_folium(
    m_media,
    use_container_width=True,
    height=700
)
