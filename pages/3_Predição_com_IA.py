import streamlit as st
import geopandas as gpd
import folium

from streamlit_folium import st_folium
from branca.colormap import LinearColormap

# =========================
# TÍTULO
# =========================

st.subheader(
    "Predição da taxa de migração internacional para 2026"
)

st.write(
    """
    O mapa apresenta a taxa prevista de migrantes
    internacionais regularizados por 100 mil habitantes
    nas microrregiões da Bahia para o ano de 2026.
    """
)

# =========================
# LEITURA DO GEOJSON
# =========================

mapa_2026 = gpd.read_file(
    "dados/mapa_predicao_2026.geojson"
)

# =========================
# LIMITES DA ESCALA
# =========================

taxa_min = mapa_2026[
    "taxa_prevista_2026"
].min()

taxa_max = mapa_2026[
    "taxa_prevista_2026"
].max()

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
    "Taxa prevista por 100 mil habitantes"
)

# =========================
# MAPA BASE
# =========================

m = folium.Map(
    location=[-12.8, -41.7],
    zoom_start=6,
    tiles="CartoDB positron"
)

# =========================
# FUNÇÃO DE COR
# =========================

def estilo(feature):

    valor = feature["properties"][
        "taxa_prevista_2026"
    ]

    if valor is None:
        cor = "white"
    else:
        cor = colormap(valor)

    return {
        "fillColor": cor,
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.9
    }

# =========================
# TOOLTIP
# =========================

tooltip = folium.GeoJsonTooltip(
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

# =========================
# CAMADA
# =========================

folium.GeoJson(
    mapa_2026,
    style_function=estilo,
    tooltip=tooltip
).add_to(m)

# =========================
# LEGENDA
# =========================

colormap.add_to(m)

# =========================
# EXIBIR
# =========================

st_folium(
    m,
    width="100%",
    height=700
)
