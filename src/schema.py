from pydantic import BaseModel

class Periodo(BaseModel):
    periodo: str

class Curso(BaseModel):
    curso: str

class Campus(BaseModel):
    campus: str
