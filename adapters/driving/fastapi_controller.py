from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from application.clasificar_caso import ClasificarCaso

class ProblemaRequest(BaseModel):
    texto: str

class CasoResponse(BaseModel):
    id: int
    tipo: str
    tecnico: str

def crear_app(use_case: ClasificarCaso) -> FastAPI:
    app = FastAPI(title="Auto-Casos API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/casos", response_model=CasoResponse)
    def crear_caso(body: ProblemaRequest):
        try:
            id_caso = use_case.ejecutar(body.texto)
     
            caso = use_case.caso_repo.buscar_por_id(id_caso)  # ver nota abajo
            return CasoResponse(
                id=id_caso,
                tipo=caso.tipo.nombre,
                tecnico=f"{caso.tecnico.nombre} ({caso.tecnico.area})"
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app