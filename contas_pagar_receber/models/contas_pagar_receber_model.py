from ..shared.database import Base
from sqlalchemy import Column, Integer, String, Numeric

class ContaPagarReceber(Base):
    __tablename__ = 'contas_pagar_receber'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255)) 
    valor = Column(Numeric)
    tipo = Column(String(30))