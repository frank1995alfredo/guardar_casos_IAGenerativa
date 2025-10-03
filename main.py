from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.repositories import TipoCasoRepo, TecnicoRepo, CasoRepo
from application.clasificar_caso import ClasificarCaso
from adapters.driven.repositorio_postgres import (
    PostgresTipoCasoRepo, PostgresTecnicoRepo, PostgresCasoRepo
)
from adapters.driven.clasificador_ollama import OllamaClasificador, OllamaTecnicoSelector
from adapters.driving.controller import CLIController

ENGINE_URL = "postgresql+psycopg2://postgres:4!oroDEV24@localhost:5432/ORODELTI_PR"

engine = create_engine(ENGINE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def main():
    with SessionLocal() as session:
        
        tipo_repo    = PostgresTipoCasoRepo(session)
        tecnico_repo = PostgresTecnicoRepo(session)
        caso_repo    = PostgresCasoRepo(session)
        clasificador = OllamaClasificador()
        selector     = OllamaTecnicoSelector() 
        
        caso_uso = ClasificarCaso(tipo_repo, tecnico_repo, caso_repo, clasificador, selector)

        CLIController(caso_uso).run()

if __name__ == "__main__":
    main()
                