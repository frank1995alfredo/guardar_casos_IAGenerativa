#puertos driven

from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import TipoCaso, Tecnico, Caso

class TipoCasoRepo(ABC):
    @abstractmethod
    def listar_nombres(self) -> List[str]:...
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[TipoCaso]:...
    
class TecnicoRepo(ABC):
    @abstractmethod
    def listar_tecnicos(self) -> List[Tecnico]:...
    
class CasoRepo(ABC):
    @abstractmethod
    def guardar(self, caso: Caso) -> int:...
    
    