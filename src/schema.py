from pydantic import BaseModel

class Resumo(BaseModel):
    total_registros: int
    concluintes: int
    ingressantes: int
    campi: int
    cursos: int

class ItemCampus(BaseModel):
    campus: str
    total: int

class ItemAno(BaseModel):
    ano: str
    total: int

class Cancelamento(BaseModel):
    campus: str
    ingressantes: int
    cancelados: int
    taxa_cancelamento: float