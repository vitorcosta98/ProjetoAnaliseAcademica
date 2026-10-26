import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")
st.set_page_config(page_title="Análise Acadêmica", layout="wide")


@st.cache_data(ttl=300)
def get(path, **params):
    params = {k: v for k, v in params.items() if v}
    r = requests.get(f"{API}{path}", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


opcoes = get("/alunos/opcoes")
st.sidebar.header("Filtros")
filtro_ano = st.sidebar.selectbox("Ano de Ingresso", ["Todos"] + opcoes['ano_ingresso'])


st.title("Análise Acadêmica")