from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import alunos as service

router = APIRouter(prefix="/alunos", tags=["alunos"])

@router.get("/resumo")
def get_resumo(db: Session = Depends(get_db)):
    return service.resumo(db)