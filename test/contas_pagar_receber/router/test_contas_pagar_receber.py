from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_deve_listar_contas_pagar_receber():
    response = client.get('/contas-pagar-receber')
    assert response.status_code == 200 
    assert response.json() == [{'id': 1, 'descricao': 'aluguel', 'valor': '1200', 'tipo': 'Pagar'}]

def test_deve_criar_conta_pagar_receber():
    nova_conta = {
        'descricao': 'Curso Python',
        'valor': '80',
        'tipo': 'P'
    }

    response = client.post('/contas-pagar-receber', json=nova_conta)
    nova_conta["id"] = 5
    assert response.status_code == 201
    assert response.json() == nova_conta