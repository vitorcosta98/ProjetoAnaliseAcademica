from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import alunos as service
from ..schema import Resumo, ItemCampus, ItemAno, Cancelamento

router = APIRouter(prefix="/alunos", tags=["alunos"])

@router.get("/resumo", response_model=Resumo, summary="Totais Gerais da Base.")
def get_resumo(db: Session = Depends(get_db)):
    return service.resumo(db)

@router.get("/opcoes", summary="Valores Disponíveis para os Filtros.")
def get_opcoes(db: Session = Depends(get_db)):
    return service.opcoes(db)

@router.get("/top-cursos", summary="Cursos com Mais Registros.")
def top_cursos(limite: int = Query(10, ge=1, le=50), ano: str | None = None,
               tipo: str | None = None, db: Session = Depends(get_db)):
    return service.top_cursos(db, limite, ano=ano, tipo=tipo)

@router.get("/ano_ingresso", response_model=list[ItemAno], summary="Registros por Ano de Ingresso.")
def get_anos(db: Session = Depends(get_db)):
    return service.por_ano_ingresso(db)

@router.get("/cancelamento", response_model=list[Cancelamento], summary="Taxa de Cancelamento entre ingressantes, por Campus.")
def get_cancelamento(db: Session = Depends(get_db)):
    return service.cancelamento_por_campus(db)

@router.get('/por-campus', response_model=list[ItemCampus], summary="Registros por Campus.")
def get_campus(tipo: str | None = None, curso: str | None = None,
               ano: str | None = None,db: Session = Depends(get_db)):
    return service.por_campus(db, tipo=tipo, curso=curso, ano=ano)