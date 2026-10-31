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


st.title("Análise Acadêmica")
st.caption("Fonte: Base PDA 2022-2024. Filtros: Campus usa Tipo, curso e ano; "
           "Top 10 usa tipo e ano.")


try:
    opcoes = get("/alunos/opcoes")
    k = get("/alunos/resumo")
except requests.RequestException:
    st.error('Não foi possível conectar à API. Verifique se ela está no ar (python run.py)')
    st.stop()


st.sidebar.header("Filtros")

filtro_ano = st.sidebar.selectbox("Ano de Ingresso", [None] + opcoes['ano_ingresso'], format_func=lambda x: x or "Todos")
filtro_curso = st.sidebar.selectbox("Curso", [None] + opcoes['cursos'], format_func=lambda x: x or 'Todos')
filtro_tipo = st.sidebar.selectbox("Tipo", [None] + opcoes['tipos'], format_func=lambda x: x or 'Todos')

c1, c2, c3, c4 = st.columns(4)
c1.metric("Registros", f"{k['total_registros']:,}".replace(",", "."))
c2.metric("Concluintes", f"{k['concluintes']:,}".replace(",", '.'))
c3.metric("Ingressantes", f"{k['ingressantes']:,}".replace(",", '.'))
c4.metric("Cursos", k['cursos'])

col1, col2 = st.columns(2)
try:
    df_campus = pd.DataFrame(get("/alunos/por-campus",tipo=filtro_tipo, curso=filtro_curso, ano=filtro_ano))
    df_campus = df_campus.sort_values(by='total', ascending=True)
    fig_campus = px.bar(df_campus, x='total', y='campus',
                        text=df_campus['total'], orientation='h',
                        title='Registros por Campus')
    fig_campus.update_traces(texttemplate='%{text:,}',textposition='outside')
    fig_campus.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig_campus.update_yaxes(title=None)
    col1.plotly_chart(fig_campus,width="stretch")
except:
    col1.text("Sem dados para os filtros selecionados.")


try:
    df_cursos = pd.DataFrame(get("/alunos/top-cursos", limite=10, tipo=filtro_tipo, ano=filtro_ano))
    df_cursos = df_cursos.sort_values(by='total', ascending=True)
    fig_cursos = px.bar(df_cursos, x='total', y='curso',
                        text=df_cursos['total'], orientation='h',
                        title='Top 10 Cursos')
    fig_cursos.update_traces(texttemplate="%{text:,}", textposition='outside')
    fig_cursos.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig_cursos.update_yaxes(title=None)
    col2.plotly_chart(fig_cursos,width="stretch")
except:
    col2.text("Sem dados para os filtros selecionados.")

df_ano = pd.DataFrame(get("/alunos/ano_ingresso"))
if df_ano.empty:
    st.info("Sem dados para exibir esse visual.")
else:
    st.plotly_chart(px.line(df_ano, x='ano', y='total', title='Registros por Ano de Ingresso'),
                width="stretch")

df_canc = pd.DataFrame(get("/alunos/cancelamento"))
if not df_canc.empty:
    fig_linha = px.bar(df_canc, x='campus', y="taxa_cancelamento",
                        text=df_canc['taxa_cancelamento'],title='Taxa de Cancelamento entre Ingressantes (%)')
    fig_linha.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_linha.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig_linha,width="stretch")