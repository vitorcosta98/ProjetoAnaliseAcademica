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
filtro_curso = st.sidebar.selectbox("Curso", [None] + opcoes['cursos'], format_func=lambda x: x or 'Todos')
filtro_tipo = st.sidebar.selectbox("Tipo", [None] + opcoes['tipos'], format_func=lambda x: x or 'Todos')


st.title("Análise Acadêmica")
k = get("/alunos/resumo")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros", f"{k['total_registros']:,}".replace(",", "."))
c2.metric("Concluintes", f"{k['concluintes']:,}".replace(",", '.'))
c3.metric("Ingressantes", f"{k['ingressantes']:,}".replace(",", '.'))
c4.metric("Cursos", k['cursos'])

col1, col2 = st.columns(2)
df_campus = pd.DataFrame(get("/alunos/por-campus",tipo=filtro_tipo))
col1.plotly_chart(px.bar(df_campus, x="total", y='campus', orientation='h',
                         title='Registros por Campus'), use_container_width=True)

df_cursos = pd.DataFrame(get("/alunos/top-cursos", limite=10, tipo=filtro_tipo))
col2.plotly_chart(px.bar(df_cursos, x='total', y='curso', orientation='h',
                        title='Top 10 Cursos'), use_container_width=True)

df_ano = pd.DataFrame(get("/alunos/ano_ingresso", tipo=filtro_tipo))
st.plotly_chart(px.line(df_ano, x='ano', y='total', title='Registros por Ano de Ingresso'),
                use_container_width=True)

df_canc = pd.DataFrame(get("/alunos/cancelamento"))
st.plotly_chart(px.bar(df_canc, x='campus', y="taxa_cancelamento",
                       title='Taxa de Cancelamento entre Ingressantes (%)'),
                       use_container_width=True)