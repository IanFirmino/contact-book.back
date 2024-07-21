from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session
from ...shared.database import get_db
from ..models.contas_pagar_receber_model import ContaPagarReceber

router = APIRouter(prefix="/contas-pagar-receber")

class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str

    class Config:
        orm_mode = True

class ContaPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str

@router.get("", response_model=List[ContaPagarReceberResponse])
def listar_contas(db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()

@router.post("", response_model=ContaPagarReceberResponse,  status_code=201)
def criar_conta(conta: ContaPagarReceberRequest, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    contas_pagar_receber = ContaPagarReceber(**conta.dict())
    db.add(contas_pagar_receber)
    db.commit()
    return contas_pagar_receber
