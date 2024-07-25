from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, ConfigDict, Field
from typing import List
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from shared.exceptions import NotFound 
from ..models.fornecedor_cliente_model import FornecedorCliente

router = APIRouter(prefix="/fornecedor-cliente")

class FornecedorClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str

class FornecedorClienteRequest(BaseModel):
    nome: str = Field(in_length=2, max_length=255)

@router.get("/{id}", response_model=FornecedorClienteResponse)
def buscar_fornecedor_cliente_por_id(id: int, db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor = db.query(FornecedorCliente).get(id)
    if not fornecedor:
        raise NotFound("Fornecedor cliente não encontrado")
    return fornecedor

@router.get("", response_model=List[FornecedorClienteResponse])
def listar_fornecedor_clientes(db: Session = Depends(get_db)) -> List[FornecedorClienteResponse]:
    return db.query(FornecedorCliente).all()

@router.post("", response_model=FornecedorClienteResponse)
def criar_fornecedor_cliente(novo_fornecedor: FornecedorClienteRequest = Body(...), db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor = FornecedorCliente(**novo_fornecedor.dict())
    db.add(fornecedor)
    db.commit()
    return fornecedor

@router.put("/{id}", response_model=FornecedorClienteResponse, status_code=201)
def alterar_fornecedor_cliente(id: int, novo_fornecedor: FornecedorClienteRequest = Body(...), db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor = db.query(FornecedorCliente).get(id)
    if not fornecedor:
        raise NotFound("Fornecedor cliente não encontrado")
    
    fornecedor.nome = novo_fornecedor.nome
    db.commit()
    db.refresh(fornecedor)
    return fornecedor

@router.delete("/{id}", status_code=204)
def deletar_fornecedor_cliente(id: int, db: Session = Depends(get_db)):
    fornecedor = db.query(FornecedorCliente).get(id)
    if not fornecedor:
        raise NotFound("Fornecedor cliente não encontrado")

    db.delete(fornecedor)
    db.commit()