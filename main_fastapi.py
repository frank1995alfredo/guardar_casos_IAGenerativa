from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from adapters.driven.repositorio_postgres import (
    PostgresCasoRepo, PostgresTecnicoRepo, PostgresTipoCasoRepo
)

from adapters.driven.clasificador_ollama import OllamaClasificador, OllamaTecnicoSelector
from adapters.driving.fastapi_controller import crear_app
from application.clasificar_caso import ClasificarCaso
import uvicorn

ENGINE_URL = "postgresql+psycopg2://postgres:4!oroDEV24@10.252.1.14:5432/ORODELTI_PR"

engine = create_engine(ENGINE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_use_case():
    with SessionLocal() as session:
        tipo_repo    = PostgresTipoCasoRepo(session)
        tecnico_repo = PostgresTecnicoRepo(session)
        caso_repo    = PostgresCasoRepo(session)
        clasificador = OllamaClasificador()
        selector     = OllamaTecnicoSelector()
        yield ClasificarCaso(tipo_repo, tecnico_repo, caso_repo,
                             clasificador, selector)
app = crear_app(next(get_use_case()))

if __name__ == "__main__":
    uvicorn.run("main_fastapi:app", host="0.0.0.0", port=8000, reload=True)