import streamlit as st

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="Migração Internacional na Bahia",
    page_icon="🌎",
    layout="wide"
)

# =========================
# TÍTULO
# =========================

st.markdown(
    """
    <div style="max-width:1200px; margin:auto;">

        <h1 style="
            text-align:center;
            font-size:40px;
            margin-bottom:40px;
        ">
            Análise temporal, espacial e sociodemográfica da migração internacional regularizada na Bahia entre 2021 e 2025 utilizando Inteligência Artificial para predição de 2026
        </h1>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# INTRODUÇÃO
# =========================

st.markdown(
    """
    <div style="
        max-width:1200px;
        margin:auto;
        text-align:justify;
        font-size:18px;
        line-height:1.8;
    ">

    <p>
    Este site apresenta análises dos fluxos migratórios internacionais
    regularizados na Bahia utilizando dados do SISMIGRA com o objetivo
    de compreender os padrões migratórios e apoiar a gestão pública no
    fortalecimento de políticas de acolhimento, regularização documental,
    inclusão social, emprego, educação e planejamento territorial.
    </p>

    <p>
    O estudo está alinhado à Lei de Migração nº 13.445/2017 e aos
    Objetivos de Desenvolvimento Sustentável (ODS) 10.7 e 16, que
    preveem a facilitação de uma migração segura, ordenada e regular,
    bem como o fortalecimento de instituições eficazes e do acesso à
    justiça.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# OBJETIVOS
# =========================

st.markdown(
    """
    <div style="
        max-width:1200px;
        margin:auto;
        text-align:center;
        font-size:18px;
        line-height:1.8;
        padding-top:20px;
        padding-bottom:20px;
    ">

    <h3>Objetivos do Estudo</h3>

    • Analisar a evolução temporal da migração internacional regularizada na Bahia entre 2021 e 2025.<br>

    • Identificar padrões espaciais entre municípios e microrregiões do estado.<br>

    • Caracterizar o perfil sociodemográfico dos migrantes internacionais regularizados.<br>

    • Aplicar modelos de Inteligência Artificial para estimar a taxa migratória de 2026.

    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# NAVEGAÇÃO
# =========================

st.markdown(
    """
    <div style="
        max-width:1200px;
        margin:auto;
        text-align:center;
        font-size:18px;
        line-height:1.8;
    ">

    <h3>Seções Disponíveis</h3>

    📊 Análise Temporal<br>
    🌎 Análise Espacial<br>
    👥 Perfil Sociodemográfico<br>
    🤖 Predição dos Fluxos Migratórios

    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# =========================
# LOGOS
# =========================

st.markdown(
    """
    <h3 style="text-align:center;">
    Objetivos de Desenvolvimento Sustentável
    </h3>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.image(
        "SDG-icon-PT-RGB-10-1.jpg",
        use_container_width=True
    )

with col2:
    st.image(
        "Design sem nome(6).png",
        use_container_width=True
    )

with col3:
    st.image(
        "Objetivo_Desenvolvimento_Sustentável_16_PT.jpg",
        use_container_width=True
    )

st.divider()

# =========================
# DESENVOLVEDORES
# =========================

st.markdown(
    """
    <h2 style="text-align:center;">
    Desenvolvedores
    </h2>

    <div style="
        text-align:center;
        font-size:20px;
        line-height:1.8;
    ">
        Cauã Ramos Santos Oliveira<br>
        Denise Nunes Viola
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# =========================
# FOTOS
# =========================

col1, col2 = st.columns(2)

with col1:
    st.image(
        "WhatsApp Image 2026-06-05 at 15.10.02.jpeg",
        use_container_width=True
    )

with col2:
    st.image(
        "117146658_326983188474224_7519955368301025113_n.jpg",
        use_container_width=True
    )

st.divider()

# =========================
# RODAPÉ
# =========================

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:15px;
        color:gray;
        padding-bottom:20px;
    ">

    Universidade do Estado da Bahia (UNEB)<br>
    Projeto de análise dos fluxos migratórios internacionais regularizados na Bahia

    </div>
    """,
    unsafe_allow_html=True
)
