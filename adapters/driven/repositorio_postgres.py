from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import List, Optional
from domain.entities import TipoCaso as TipoCasoEnt, Tecnico as TecnicoEnt, Caso as CasoEnt
from domain.repositories import TipoCasoRepo, TecnicoRepo, CasoRepo
Base = declarative_base()

class TipoCasoORM(Base):
    __tablename__ = "tipo_caso"
    __table_args__ = {"schema": "ejemplo"}
    id = Column(Integer, primary_key=True)
    nombre = Column(String)

class TecnicoORM(Base):
    __tablename__ = "desarrollador"
    __table_args__ = {"schema": "ejemplo"}
    id   = Column(Integer, primary_key=True)
    nombre = Column(String)
    area   = Column(String)

class CasoORM(Base):
    __tablename__ = "casos"
    __table_args__ = {"schema": "ejemplo"}
    id = Column(Integer, primary_key=True)
    descripcion = Column(Text)
    tipo_caso_id = Column(Integer, ForeignKey("ejemplo.tipo_caso.id"))
    desarrollador_id = Column(Integer, ForeignKey("ejemplo.desarrollador.id"))

class PostgresTipoCasoRepo(TipoCasoRepo):
    def __init__(self, session: Session):
        self.session = session
        
    def listar_nombres(self) -> List[str]:
        return [r[0] for r in self.session.query(TipoCasoORM.nombre).distinct()]
    
    def buscar_por_nombre(self, nombre: str) -> Optional[TipoCasoEnt]:
        row = self.session.query(TipoCasoORM).filter(TipoCasoORM.nombre.ilike(nombre)).first()
        return TipoCasoEnt(id=row.id, nombre=row.nombre) if row else None

class PostgresTecnicoRepo(TecnicoRepo):
    def __init__(self, session: Session):
        self.session = session
        
    def listar_tecnicos(self) -> List[TecnicoEnt]:
        return [TecnicoEnt(id=r.id, nombre=r.nombre, area=r.area)
                for r in self.session.query(TecnicoORM).all()]

class PostgresCasoRepo(CasoRepo):
    def __init__(self, session: Session):
        self.session = session
        
    def guardar(self, caso: CasoEnt) -> int:
        orm_caso = CasoORM(descripcion=caso.descripcion,
                           tipo_caso_id=caso.tipo.id,
                           desarrollador_id=caso.tecnico.id)
        self.session.add(orm_caso)
        self.session.flush()
        self.session.commit()
        return orm_caso.id