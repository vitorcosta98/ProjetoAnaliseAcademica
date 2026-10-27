import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE/"dados_editados.csv")

df = df.rename(columns={
    "Ingressante/Concluinte": "tipo",
    "Nome": "nome",
    "Nível de Ensino": "nivel",
    "Curso": "curso",
    "Campus": "campus",
    "Situação de Matrícula": "situacao",
    "Período de Ingresso": "periodo",
})

df["ano"] = df['periodo'].str[:4].astype(str)


engine = create_engine(f'sqlite:///{BASE / 'bancodados.db'}')

df.to_sql(
    name='DadosAlunos',
    con=engine,
    if_exists='replace',
    index=False
)

print('Dados carregados com sucesso!')