from dataclasses import dataclass

@dataclass
class Tecnico:
    id: int
    nombre: str
    area: str

@dataclass
class TipoCaso:
    id: int
    nombre: str

@dataclass
class Caso:
    descripcion: str
    tipo: TipoCaso
    tecnico: Tecnico