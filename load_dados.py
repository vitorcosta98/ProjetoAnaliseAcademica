import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("dados_editados.csv")

engine = create_engine('sqlite:///bancodados.db')

df.to_sql(
    name='DadosAlunos',
    con=engine,
    if_exists='replace',
    index=False
)

print('Dados carregados com sucesso!')