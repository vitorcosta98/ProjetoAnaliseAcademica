from sqlalchemy import select, func
from ..database import alunos

def resumo(db):
    q = select(func.count().label("total_registros"),
               func.count(func.distinct(alunos.c.nome)).label("total_alunos"),
               ).select_from(alunos)
    
    total = db.execute(q).one()

    return {"Response": "Requisição concluída com sucesso!",
            "Total de Alunos": total.total_alunos,}

