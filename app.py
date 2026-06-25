import streamlit as st

st.set_page_config(
    page_title="Migração Internacional na Bahia",
    page_icon="🌎",
    layout="wide"
)

# Título principal
st.markdown(
    """
    <h1 style="text-align: center;">
    Análise temporal, espacial e sociodemográfica da migração internacional regularizada na Bahia entre 2021 e 2025 utilizando Inteligência Artificial para predição de 2026
    </h1>
    """,
    unsafe_allow_html=True
)

# Texto introdutório e seções
st.markdown(
    """
    <div style="
        max-width: 1400px;
        margin-left: 20px;
        margin-right: 20px;
        font-size: 18px;
    ">

    <p style="text-align: justify;">
    Este site apresenta análises dos fluxos migratórios internacionais regularizados
    na Bahia utilizando dados do SISMIGRA com o objetivo de compreender os padrões
    migratórios e apoiar a gestão da Bahia no fortalecimento de políticas públicas
    de acolhimento, regularização documental, inclusão social, emprego, educação
    e planejamento territorial.
    </p>

    <p style="text-align: justify;">
    O estudo está alinhado à Lei de Migração nº 13.445/2017 e aos Objetivos de
    Desenvolvimento Sustentável (ODS) 10.7 e 16, que preveem a facilitação de uma
    migração segura e regular, bem como o fortalecimento de instituições eficazes
    e do acesso à justiça.
    </p>

    <h3>Seções</h3>

    <ul>
        <li>Perfil Sociodemográfico</li>
        <li>Visualização Espacial</li>
        <li>Predição dos Fluxos Migratórios</li>
    </ul>

    </div>
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


st.markdown("---")
