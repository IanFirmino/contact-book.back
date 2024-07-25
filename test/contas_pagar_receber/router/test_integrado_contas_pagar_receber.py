from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.dependencies import get_db
from shared.database import Base
from sqlalchemy.pool import StaticPool
from decimal import Decimal

client = TestClient(app) #python -m pytest
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_deve_listar_contas_pagar_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    conta_um = {
        'descricao': 'Curso Python',
        'valor': '80',
        'tipo': 'P'
    } 
    conta_dois = {
        'descricao': 'Curso C#',
        'valor': '80',
        'tipo': 'P'
    }

    response = client.post('/contas-pagar-receber', json=conta_um)
    response = client.post('/contas-pagar-receber', json=conta_dois)

    response = client.get('/contas-pagar-receber')
    assert response.status_code == 200 

def test_deve_criar_conta_pagar_receber(): 
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        'descricao': 'Curso Python',
        'valor': '80',
        'tipo': 'P'
    }

    response = client.post('/contas-pagar-receber', json=nova_conta)
    nova_conta["id"] = 1
    assert response.status_code == 201, response.text

def test_deve_erro_enum_tipo_pagar_diferente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        'descricao': 'Curso Python',
        'valor': '80',
        'tipo': 'G'
    }

    response = client.post('/contas-pagar-receber', json=nova_conta)
    nova_conta["id"] = 1
    assert response.status_code == 422, response.text

def test_deve_erro_valor_menor_que_zero():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        'descricao': 'Curso Python',
        'valor': '-80',
        'tipo': 'P'
    }

    response = client.post('/contas-pagar-receber', json=nova_conta)
    nova_conta["id"] = 1
    assert response.status_code == 422, response.text

def test_deve_alterar_valor_conta():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        'descricao': 'Curso Python',
        'valor': '80',
        'tipo': 'P'
    }

    response = client.post('/contas-pagar-receber', json=nova_conta)
    id_conta = response.json()['id']

    response = client.put(f'/contas-pagar-receber/{id_conta}', json={
        'descricao': 'Curso Python',
        'valor': '100000',
        'tipo': 'P'
    })

    assert response.status_code == 201
    assert Decimal(response.json()['valor']) == Decimal('100000.0'), response.text

def test_deve_deletar_conta():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {
        'descricao': 'Curso Python',
        'valor': '80',
        'tipo': 'P'
    }

    response = client.post('/contas-pagar-receber', json=nova_conta)
    id_conta = response.json()['id']

    response = client.delete(f'/contas-pagar-receber/{id_conta}')

    assert response.status_code == 204