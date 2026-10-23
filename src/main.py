from fastapi import FastAPI
from .routes import alunos

app = FastAPI(title="API Analise Acadêmica")
app.include_router(alunos.router)