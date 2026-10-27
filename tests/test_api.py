from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_resumo():
    r = client.get("/alunos/resumo")
    assert r.status_code == 200
    assert r.json()["total_registros"] == 31770


def test_tipo_invalido():
    assert client.get("/alunos/por-campus?tipo=Qualquer").status_code == 422


def test_limite_fora_do_intervalo():
    assert client.get("/alunos/top-cursos?limite=500").status_code == 422