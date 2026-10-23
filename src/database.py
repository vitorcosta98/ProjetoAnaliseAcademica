from pathlib import Path
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base

db_path = Path(__file__).resolve().parent.parent/"bancodados.db"

engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)

metadata = MetaData()
alunos = Table("DadosAlunos", metadata, autoload_with=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()