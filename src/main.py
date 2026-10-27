import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from .routes import alunos

logger = logging.getLogger(__name__)
app = FastAPI(title="API Analise Acadêmica")
app.include_router(alunos.router)

@app.exception_handler(SQLAlchemyError)
async def erro_banco(request: Request, exc: SQLAlchemyError):
    logger.exception("Erro ao acessar banco de dados.")
    return JSONResponse(status_code=503,
                        content={"detail":"Banco de dados indisponível."})