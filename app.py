import streamlit as st

st.set_page_config(
    page_title="Migração Internacional na Bahia",
    page_icon="🌎",
    layout="wide"
)

# =========================================================
# TÍTULO PRINCIPAL
# =========================================================

st.markdown(
    """
    <h1 style="text-align: center;">
    Análise temporal, espacial e sociodemográfica da migração internacional regularizada na Bahia entre 2021 e 2025 utilizando Inteligência Artificial para predição de 2026
    </h1>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TEXTO INTRODUTÓRIO
# =========================================================

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
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# BOTÕES DE NAVEGAÇÃO (SEÇÕES)
#
# Cada botão é um st.page_link dentro de um st.container
# com "key" próprio — isso gera uma classe CSS exclusiva
# (st-key-<nome>) que usamos abaixo para colorir cada
# botão individualmente.
#
# Caminhos conferidos direto no repositório (pasta pages/):
# 1_Perfil_Sociodemografico.py
# 2_Análise_Espacial.py
# 3_Predição_com_IA.py
# =========================================================

st.markdown("### Seções")

st.markdown(
    """
    <style>

    /* Estilo base de todos os botões de navegação */
    div[data-testid="stPageLink"] {
        border-radius: 10px;
        padding: 4px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.18);
    }

    div[data-testid="stPageLink"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.28);
    }

    div[data-testid="stPageLink"] p {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: white !important;
        text-align: center;
        width: 100%;
        white-space: pre-line !important;
        line-height: 1.3 !important;
    }

    div[data-testid="stPageLink"] a {
        justify-content: center !important;
        padding: 14px 10px !important;
        border-radius: 10px !important;
        text-decoration: none !important;
    }

    /* Botão 1 — azul */
    .st-key-btn_perfil div[data-testid="stPageLink"] a {
        background-color: #333795 !important;
    }

    /* Botão 2 — vermelho */
    .st-key-btn_espacial div[data-testid="stPageLink"] a {
        background-color: #B31D2D !important;
    }

    /* Botão 3 — amarelo/dourado */
    .st-key-btn_predicao div[data-testid="stPageLink"] a {
        background-color: #F2B134 !important;
    }

    .st-key-btn_predicao div[data-testid="stPageLink"] p {
        color: #333795 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

col_a, col_b, col_c = st.columns(3)

with col_a:
    with st.container(key="btn_perfil"):
        st.page_link(
            "pages/1_Perfil_Sociodemografico.py",
            label="Perfil\nSociodemográfico",
            use_container_width=True
        )

with col_b:
    with st.container(key="btn_espacial"):
        st.page_link(
            "pages/2_Análise_Espacial.py",
            label="Visualização\nEspacial",
            use_container_width=True
        )

with col_c:
    with st.container(key="btn_predicao"):
        st.page_link(
            "pages/3_Predição_com_IA.py",
            label="Predição dos\nFluxos Migratórios",
            use_container_width=True
        )


# =========================================================
# LINHA DIVISÓRIA
# =========================================================

st.markdown("---")


# =========================================================
# LOGOS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.image("SDG-icon-PT-RGB-10-1.jpg", width=250)

with col2:
    st.image("Design sem nome(6).png", width=350)

with col3:
    st.image("Objetivo_Desenvolvimento_Sustentável_16_PT.jpg", width=250)


# =========================================================
# DESENVOLVEDORES
# =========================================================

st.markdown(
    """
    ### Desenvolvedores
    - Cauã Ramos Santos Oliveira
    - Denise Nunes Viola
    """
)


# =========================================================
# FOTOS
# =========================================================

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
