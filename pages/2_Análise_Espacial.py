import streamlit as st
import pandas as pd

st.title("Distribuição Espacial")

st.subheader(
    "Qualidade da informação de município de residência"
)

st.write(
    """
    Parte dos registros migratórios não possui município de residência
    informado. A tabela abaixo apresenta a quantidade e o percentual
    desses registros por ano.
    """
)

nao_esp = pd.read_csv(
    "dados/nao_especificado_municipio.csv"
)

st.dataframe(
    nao_esp,
    use_container_width=True,
    hide_index=True
)
