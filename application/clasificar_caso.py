from typing import Protocol
from domain.entities import Caso, TipoCaso, Tecnico
from domain.repositories import TipoCasoRepo, TecnicoRepo, CasoRepo

class ClasificadorPort(Protocol):
    def clasificar(self, texto: str, opciones: list[str]) -> str:...

class TecnicoSelectorPort(Protocol):
    def seleccionar(self, texto: str, tecnicos: list[Tecnico]) -> Tecnico:...
    
class ClasificarCaso:
    def __init__(self,
        tipo_repo: TipoCasoRepo,
        tecnico_repo: TecnicoRepo,
        caso_repo: CasoRepo,
        clasificador: ClasificadorPort,
        tecnico_selector: TecnicoSelectorPort
        ):
        self.tipo_repo        = tipo_repo
        self.tecnico_repo     = tecnico_repo
        self.caso_repo        = caso_repo
        self.clasificador     = clasificador
        self.tecnico_selector = tecnico_selector

    def ejecutar(self, texto_caso: str) -> int:
        
        tipos       = self.tipo_repo.listar_nombres()
        tipo_nombre = self.clasificador.clasificar(texto_caso, tipos)
        tipo        = self.tipo_repo.buscar_por_nombre(tipo_nombre)
       
        if not tipo:
            raise ValueError(f'Tipo {tipo_nombre} no existe')
        
        #ELEGIR TECNICO
        tecnicos = self.tecnico_repo.listar_tecnicos()
        tecnico  = self.tecnico_selector.seleccionar(texto_caso, tecnicos)
        
        caso = Caso(descripcion=texto_caso, tipo=tipo, tecnico=tecnico)
        return self.caso_repo.guardar(caso)
    

        
    