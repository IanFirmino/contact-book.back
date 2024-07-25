from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from shared.exceptions import NotFound 
from ..models.contas_pagar_receber_model import ContaPagarReceber

router = APIRouter(prefix="/contas-pagar-receber")

class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'P'
    RECEBER = 'R'

class ContaPagarReceberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    descricao: str
    valor: Decimal
    tipo: str

class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length =3, max_length=255)
    valor: Decimal = Field(gt= 0)
    tipo: ContaPagarReceberTipoEnum

@router.get("/{id}", response_model=ContaPagarReceberResponse)
def buscar_conta_por_id(id: int, db: Session = Depends(get_db)):
    conta = db.query(ContaPagarReceber).get(id)
    if not conta:
        raise NotFound("Conta não encontrada")
    return conta

@router.get("", response_model=List[ContaPagarReceberResponse])
def listar_contas(db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()

@router.post("", response_model=ContaPagarReceberResponse,  status_code=201)
def criar_conta(conta: ContaPagarReceberRequest, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    contas_pagar_receber = ContaPagarReceber(**conta.dict())
    db.add(contas_pagar_receber)
    db.commit()
    return contas_pagar_receber

@router.put("/{id}", response_model= ContaPagarReceberResponse, status_code=201)
def alterar_conta(id: int, nova_conta: ContaPagarReceberRequest = Body(...), db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    conta = db.query(ContaPagarReceber).get(id)
    if not conta:
        raise NotFound("Conta não encontrada")

    conta.descricao = nova_conta.descricao
    conta.tipo = nova_conta.tipo
    conta.valor = nova_conta.valor

    db.commit()
    db.refresh(conta)
    return conta

@router.delete("/{id}", status_code=204)
def deletar_conta(id: int, db: Session = Depends(get_db)):
    conta = db.query(ContaPagarReceber).get(id)
    if not conta:
        raise NotFound("Conta não encontrada")

    db.delete(conta)
    db.commit()