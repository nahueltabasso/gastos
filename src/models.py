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
        
    def to_dict(self) -> dict:
        return {
            'DESCRIPCION': getattr(self, 'descripcion', '') or '',
            'FECHA': getattr(self, 'fecha', '') or '',
            'PESOS': '$ ' + str(getattr(self, 'total_pesos', '0.0')) or '0.0',
            'U$D OFICIAL': '$ ' +  str(getattr(self, 'total_dolar_oficial', '0.0')) or '0.0',
            'U$D MEP': '$ ' + str(getattr(self, 'total_dolar_mep', '0.0')) or '0.0',
            'TITULAR': getattr(self, 'titular', '') or ''
        }
    
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
    
    def to_dict(self) -> dict:
        return {
            'TOTAL $': '$ ' + str(getattr(self, 'total_pesos_acum', '0.0')) or '0.0',
            'TOTAL U$D OF': '$ ' + str(getattr(self, 'total_dolar_oficial_acum', 0.0)) or '0.0',
            'TOTAL U$D MEP': '$ ' +  str(getattr(self, 'total_dolar_mep_acum', 0.0)) or '0.0',
        }
    

class PagoCasa(Base):
    __tablename__ = 'pagos_casa'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column(String(150))
    fecha: Mapped[str] = mapped_column(String(15))
    total_usd: Mapped[float]
    tipo: Mapped[str] = mapped_column(String(20))
    
    @staticmethod
    def fecha_to_key(fecha: str) -> tuple:
        meses = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
            "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
            "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }
        try:
            mes, anio = fecha.split('-')
            return (int(anio), meses.get(mes, 0))
        except Exception:
            return (0, 0) 
    
    def set_valores(self, data: dict) -> None:
        self.descripcion = data['descripcion']
        self.fecha = data['fecha']
        self.total_usd = data['total_usd']
        self.tipo = data['tipo']
        
    def to_dict(self) -> dict:
        return {
            'DESCRIPCION': getattr(self, 'descripcion', '') or '',
            'FECHA': getattr(self, 'fecha', '') or '',
            'TOTAL U$D': '$ ' + str(getattr(self, 'total_usd', '0.0')) or '0.0',
            'TIPO': '+' if self.tipo == 'sumar' else '-'
        }
        
    def __repr__(self) -> str:
        return f"""PagoCasa(id={self.id!r}, 
                descripcion={self.descripcion!r}, 
                fecha={self.fecha!r}, 
                total_usd={self.total_usd!r}, 
                tipo={self.tipo!r})"""
    
                
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
        
        
@dataclass
class Totales():
    total: float = 0.0
    resta: float = 0.0
    
    def calcular_totales(self, pagos: list[PagoCasa]) -> None:
        for pago in pagos:
            if pago.tipo == 'sumar':
                self.total += pago.total_usd
            else:
                self.resta += pago.total_usd
        self.resta = self.total - self.resta
        
    def to_dict(self) -> dict:
        return {
            'TOTAL U$D': '$ ' + str(self.total) if self.total else '0.0',
            'RESTA U$D': '$ ' + str(self.resta) if self.resta else '0.0'
        }   