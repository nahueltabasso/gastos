from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from dataclasses import dataclass, field
from database import Base
from dolar_service import get_current_dolar_value, get_dolar_value_by_date

class Gasto(Base):
    __tablename__ = 'gastos'

    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column(String(150))
    fecha: Mapped[str] = mapped_column(String(15))
    total_pesos: Mapped[float]
    total_dolar_oficial: Mapped[float]
    total_dolar_mep: Mapped[float]
    titular: Mapped[str] = mapped_column(String(50))
    valor_dolar_oficial: Mapped[float]
    valor_dolar_mep: Mapped[float]
    
    def set_valores(self, data: dict) -> None:
        self.descripcion = data['descripcion']
        self.fecha = data['fecha']
        self.total_pesos = data['total_pesos']
        self.total_dolar_oficial = data['total_dolar_oficial'] if 'total_dolar_oficial' in data else 0.0
        self.total_dolar_mep = data['total_dolar_mep'] if 'total_dolar_mep' in data else 0.0
        self.titular = data['titular']
        self.valor_dolar_oficial = data['valor_dolar_oficial'] if 'valor_dolar_oficial' in data else 0.0
        self.valor_dolar_mep = data['valor_dolar_mep'] if 'valor_dolar_mep' in data else 0.0
        
    def set_costos(self, create: bool=False) -> None:
        if create:
            dolar: Dolar = get_current_dolar_value()
        else:
            dolar: Dolar = get_dolar_value_by_date(self.fecha)
        self.total_dolar_oficial = round(self.total_pesos / dolar.oficial.value_sell, 2)
        self.total_dolar_mep = round(self.total_pesos / dolar.blue.value_sell, 2)
        self.valor_dolar_oficial = dolar.oficial.value_sell
        self.valor_dolar_mep = dolar.blue.value_sell
    
    def __repr__(self) -> str:
        return f"""Bill(id={self.id!r}, 
                descricion={self.descripcion!r}, 
                fecha={self.fecha!r}, 
                total_pesos={self.total_pesos!r}, 
                total_dolar_oficial={self.total_dolar_oficial!r},
                total_dolar_mep={self.total_dolar_mep!r},
                titular={self.titular!r},
                valor_dolar_oficial={self.valor_dolar_oficial!r}, 
                valor_dolar_mep={self.valor_dolar_mep!r})"""
                
class TotalDinero(Base):
    __tablename__ = 'totales'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    total_pesos_acum: Mapped[float]
    total_dolar_oficial_acum: Mapped[float]
    total_dolar_mep_acum: Mapped[float]
    tipo: Mapped[str] = mapped_column(String(20))  # 'oficial' o 'mep'
    
                
@dataclass
class TipoDolar:
    value_avg: float = 0.0
    value_sell: float = 0.0
    value_buy: float = 0.0
    
@dataclass
class Dolar:
    oficial: TipoDolar = field(default_factory=TipoDolar)
    blue: TipoDolar = field(default_factory=TipoDolar)

    def setValores(self, data: dict):
        self.oficial.value_avg = data['oficial']['value_avg']
        self.oficial.value_sell = data['oficial']['value_sell']
        self.oficial.value_buy = data['oficial']['value_buy']
        
        self.blue.value_avg = data['blue']['value_avg']
        self.blue.value_sell = data['blue']['value_sell']
        self.blue.value_buy = data['blue']['value_buy']
        
        