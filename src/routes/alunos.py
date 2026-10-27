from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import alunos as service

router = APIRouter(prefix="/alunos", tags=["alunos"])

@router.get("/resumo")
def get_resumo(db: Session = Depends(get_db)):
    return service.resumo(db)

@router.get("/opcoes")
def get_opcoes(db: Session = Depends(get_db)):
    return service.opcoes(db)

@router.get("/top-cursos")
def top_cursos(limite: int = Query(10, ge=1, le=50), ano: str | None = None,
               tipo: str | None = None, db: Session = Depends(get_db)):
    return service.top_cursos(db, limite, ano=ano, tipo=tipo)

@router.get("/ano_ingresso")
def get_cursos(db: Session = Depends(get_db)):
    return service.por_ano_ingresso(db)

@router.get("/cancelamento")
def get_cancelamento(db: Session = Depends(get_db)):
    return service.cancelamento_por_campus(db)

@router.get('/por-campus')
def get_campus(tipo: str | None = None, curso: str | None = None,
               ano: str | None = None,db: Session = Depends(get_db)):
    return service.por_campus(db, tipo=tipo, curso=curso, ano=ano)