import streamlit as st

st.set_page_config(
    page_title="Migração Internacional na Bahia",
    page_icon="🌎",
    layout="wide"
)

# Título principal
st.markdown(
    """
    <div style="max-width: 1200px; margin: auto;">
        <h1 style="text-align: center;">
            Análise temporal, espacial e sociodemográfica da migração internacional regularizada na Bahia entre 2021 e 2025 utilizando Inteligência Artificial para predição de 2026
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Texto introdutório e seções
st.markdown(
    """
    <div style="max-width: 1200px; margin: auto; text-align: justify; font-size: 18px;">

    Este site apresenta análises dos fluxos migratórios internacionais regularizados
    na Bahia utilizando dados do SISMIGRA com o objetivo de compreender os padrões
    migratórios e apoiar a gestão da Bahia no fortalecimento de políticas públicas
    de acolhimento, regularização documental, inclusão social, emprego, educação
    e planejamento territorial.

    O estudo está alinhado à Lei de Migração nº 13.445/2017 e aos Objetivos de
    Desenvolvimento Sustentável (ODS) 10.7 e 16, que preveem a facilitação de uma
    migração segura e regular, bem como o fortalecimento de instituições eficazes
    e do acesso à justiça.

    </div>

    ### Seções

    - Perfil Sociodemográfico
    - Visualização Espacial
    - Predição dos Fluxos Migratórios
    """,
    unsafe_allow_html=True
)

# Linha divisória
st.markdown("---")

# Logos
col1, col2, col3 = st.columns(3)

with col1:
    st.image("SDG-icon-PT-RGB-10-1.jpg", width=250)

with col2:
    st.image("Design sem nome(6).png", width=350)

with col3:
    st.image("Objetivo_Desenvolvimento_Sustentável_16_PT.jpg", width=250)

# Desenvolvedores
st.markdown(
    """
    ### Desenvolvedores

    - Cauã Ramos Santos Oliveira
    - Denise Nunes Viola
    """
)

# Fotos
col1, col2 = st.columns(2)

with col1:
    st.image(
        "WhatsApp Image 2026-06-05 at 15.10.02.jpeg",
        width=400
    )

with col2:
    st.image(
        "117146658_326983188474224_7519955368301025113_n.jpg",
        width=400
    )

st.markdown("---")
