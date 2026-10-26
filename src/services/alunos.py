from sqlalchemy import select, func, case
from ..database import alunos as a


def resumo(db):
    q = select(
        func.count().label('total_registros'),
        func.sum(case((a.c.tipo == "Concluinte", 1), else_=0)).label('concluintes'),
        func.sum(case((a.c.tipo == "Ingressante", 1), else_=0)).label('ingressantes'),
        func.count(func.distinct(a.c.campus)).label('campi'),
        func.count(func.distinct(a.c.curso)).label('cursos'),
    ).select_from(a)

    return dict(db.execute(q).one()._mapping)


def _filtros(q, periodo=None, curso=None, campus=None, tipo=None):
    if periodo: q = q.where(a.c.periodo == periodo)
    if curso: q = q.where(a.c.curso == curso)
    if campus: q = q.where(a.c.campus == campus)
    if tipo: q = q.where(a.c.tipo == tipo)

    return q


def opcoes(db):
    def distintos(col):
        return [r[0] for r in db.execute(select(col).distinct().order_by(col))]

    return {"campi": distintos(a.c.campus), "niveis":distintos(a.c.nivel), "tipos":distintos(a.c.tipo)}


def top_cursos(db, limite, **f):
    q = select(a.c.curso, func.count().label('total')).select_from(a)
    q = _filtros(q,**f).group_by(a.c.curso).order_by(func.count().desc()).limit(limite)
    return [{"curso": c, "total": t} for c, t in db.execute(q).all()]


def por_ano_ingresso(db, **f):
    q = select(a.c.ano, func.count().label('total')).select_from(a)
    q = _filtros(q, **f).group_by(a.c.ano).order_by(a.c.ano)
    return [{"ano": y, "total": t} for y, t in db.execute(q).all()]


def cancelamento_por_campus(db):
    cancelados = func.sum(case((a.c.situacao == "CANCELADO",1), else_=0))
    q = (select(a.c.campus, func.count().label('ingressantes'), cancelados.label('cancelados'))
         .select_from(a).where(a.c.tipo == 'Ingressante').group_by(a.c.campus))

    out = [{"campus":c, "ingressantes":i, "cancelados": cl,
            "taxa_cancelamento":round(cl/i * 100, 1)} for c, i, cl in db.execute(q).all()]

    return sorted(out, key=lambda x: x["taxa_cancelamento"], reverse=True)

