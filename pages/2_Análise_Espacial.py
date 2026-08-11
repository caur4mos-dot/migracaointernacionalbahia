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


# =========================================================
# REGISTROS SEM MUNICÍPIO ESPECIFICADO
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
#
# ATENÇÃO: apontando para as versões SIMPLIFICADAS
# (geradas com rmapshaper no R). Mova os arquivos
# "_simplificado.geojson" da pasta Transferências para
# dentro de "dados/" antes de rodar o app, ou ajuste os
# caminhos abaixo para onde eles estiverem.
# =========================================================

ARQUIVOS_MAPAS = {
    2021: "dados/mapa_2021_simplificado.geojson",
    2022: "dados/mapa_2022_simplificado.geojson",
    2023: "dados/mapa_2023_simplificado.geojson",
    2024: "dados/mapa_2024_simplificado.geojson",
    2025: "dados/mapa_2025_simplificado.geojson"
}


# =========================================================
# CARREGAR OS MAPAS + CALCULAR MÉDIA
#
# TUDO NUMA ÚNICA FUNÇÃO CACHEADA.
#
# Antes, calcular_media() rodava de novo a cada rerun
# do Streamlit (ex: toda vez que o usuário trocava o ano
# no radio), mesmo sem depender do ano escolhido. Juntando
# tudo aqui, o groupby/concat só roda uma vez, e fica em
# cache junto com o carregamento dos geojsons.
# =========================================================

@st.cache_data
def carregar_mapas_e_media():

    mapa_2021 = gpd.read_file(ARQUIVOS_MAPAS[2021]).to_crs(4326)
    mapa_2022 = gpd.read_file(ARQUIVOS_MAPAS[2022]).to_crs(4326)
    mapa_2023 = gpd.read_file(ARQUIVOS_MAPAS[2023]).to_crs(4326)
    mapa_2024 = gpd.read_file(ARQUIVOS_MAPAS[2024]).to_crs(4326)
    mapa_2025 = gpd.read_file(ARQUIVOS_MAPAS[2025]).to_crs(4326)

    mapas = {
        2021: mapa_2021,
        2022: mapa_2022,
        2023: mapa_2023,
        2024: mapa_2024,
        2025: mapa_2025
    }

    # ---- escala global ----

    todos_taxa = pd.concat(
        [m[["taxa_100k"]] for m in mapas.values()],
        ignore_index=True
    )

    taxa_min = todos_taxa["taxa_100k"].min()
    taxa_max = todos_taxa["taxa_100k"].max()

    # ---- média 2021-2025 ----

    todos = pd.concat(
        list(mapas.values()),
        ignore_index=True
    )

    media = (
        todos
        .groupby("name_micro")
        .agg(
            media_migrantes=("total_migrantes", "mean"),
            media_pop=("populacao", "mean"),
            media_taxa=("taxa_100k", "mean")
        )
        .reset_index()
    )

    geometria = mapa_2025[["name_micro", "geometry"]]

    mapa_media = geometria.merge(media, on="name_micro", how="left")

    mapa_media["media_taxa_plot"] = mapa_media["media_taxa"]
    mapa_media.loc[
        mapa_media["media_taxa_plot"] == 0,
        "media_taxa_plot"
    ] = None

    return mapas, taxa_min, taxa_max, mapa_media


mapas, taxa_min, taxa_max, mapa_media = carregar_mapas_e_media()


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
# GERAR HTML DO MAPA (CACHEADO POR ANO)
#
# Isso evita reconstruir o folium.Map inteiro sempre que o
# Streamlit re-executa o script (ex: qualquer interação na
# página). Trocar de ano e voltar não recalcula nada.
# =========================================================

@st.cache_data
def gerar_html_mapa(ano):

    mapa_ano = mapas[ano]

    centro = [
        mapa_ano.geometry.centroid.y.mean(),
        mapa_ano.geometry.centroid.x.mean()
    ]

    m = folium.Map(
        location=centro,
        zoom_start=6,
        tiles="CartoDB positron"
    )

    folium.GeoJson(

        mapa_ano,

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

    colormap.add_to(m)

    return m.get_root().render()


st.components.v1.html(
    gerar_html_mapa(ano_escolhido),
    height=700,
    scrolling=False
)


# =========================================================
# TAXA MÉDIA 2021–2025
# =========================================================

st.divider()

st.subheader(
    "Taxa média de migração internacional por microrregião (2021–2025)"
)


taxa_min_media = mapa_media["media_taxa_plot"].dropna().min()
taxa_max_media = mapa_media["media_taxa_plot"].dropna().max()


colormap_media = cm.LinearColormap(
    colors=CORES,
    vmin=taxa_min_media,
    vmax=taxa_max_media
)

colormap_media.caption = (
    "Taxa média por 10 mil habitantes"
)


# =========================================================
# GERAR HTML DO MAPA DA MÉDIA (CACHEADO)
# =========================================================

@st.cache_data
def gerar_html_mapa_media():

    centro_media = [
        mapa_media.geometry.centroid.y.mean(),
        mapa_media.geometry.centroid.x.mean()
    ]

    m_media = folium.Map(
        location=centro_media,
        zoom_start=6,
        tiles="CartoDB positron"
    )

    def estilo_media(feature):

        valor = feature["properties"].get("media_taxa_plot")

        cor = "white" if valor is None else colormap_media(valor)

        return {
            "fillColor": cor,
            "color": "black",
            "weight": 1,
            "fillOpacity": 1
        }

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

    folium.GeoJson(
        mapa_media,
        style_function=estilo_media,
        tooltip=tooltip_media,
        zoom_on_click=False
    ).add_to(m_media)

    colormap_media.add_to(m_media)

    return m_media.get_root().render()


st.components.v1.html(
    gerar_html_mapa_media(),
    height=700,
    scrolling=False
)
