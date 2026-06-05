import streamlit as st

# Configuração da página (Só pode aparecer uma vez no código e deve ser a primeira coisa)
st.set_page_config(
    page_title="Migração Internacional na Bahia",
    page_icon="🌎",
    layout="wide"
)

# Título Principal
st.title("Análise temporal, espacial e sociodemográfica da migração internacional regularizada na Bahia entre 2021 e 2025 utilizando Inteligência Artificial para predição de 2026")

# Texto introdutório
st.markdown("""
Este site apresenta análises dos fluxos migratórios internacionais regularizados
na Bahia utilizando dados do SISMIGRA com o objetivo de compreender os padrões migratórios e apoiar a gestão da Bahia no fortalecimento de políticas públicas de acolhimento,
regularização documental, inclusão social, emprego, educação e planejamento territorial. Se alinhando a lei de Migração n° 13.445/2017 e ao Objetivo de Desenvolvimento Sustentável
(ODS) 10.7, que prevê a facilitação de uma migração segura e regular, e o ODS 16, que enfatiza instituições eficazes e acesso à justiça.

### Seções

- Perfil Sociodemográfico
- Visualização Espacial
- Predição dos Fluxos Migratórios
""")

# Linha divisória para os logos
st.markdown("---")

# Criando 3 colunas para os logos
col1, col2, col3 = st.columns(3)

with col1:
    # SE O NOME NO GITHUB ESTIVER DIFERENTE, AJUSTE AQUI:
    st.image("Objetivo_Desenvolvimento_Sustentável_16_PT.jpg", width=250)

with col2:
    # SE O NOME NO GITHUB ESTIVER DIFERENTE, AJUSTE AQUI:
    st.image("Design sem nome(6).png", width=400)


with col3:
    # SE O NOME NO GITHUB ESTIVER DIFERENTE, AJUSTE AQUI:
    st.image("SDG-icon-PT-RGB-10-1.jpg", width=250)
