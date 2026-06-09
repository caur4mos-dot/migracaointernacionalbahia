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
