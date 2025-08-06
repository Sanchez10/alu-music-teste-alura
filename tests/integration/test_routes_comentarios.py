import pytest
from unittest.mock import patch
from app import create_app, db

@pytest.fixture
def client():
    app = create_app(testing=True)

    # Usa banco em memória
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test'

    with app.app_context():
        db.create_all()  # Cria as tabelas para os testes

        with app.test_client() as client:
            yield client


@patch('app.services.classifier.classificar_comentario')
def test_cadastrar_comentario(mock_classificar, client):
    # Mock do classificador
    mock_classificar.return_value = {
        "categoria": "ELOGIO",
        "tags_funcionalidades": [{"codigo": "melodia", "explicacao": "Boa melodia"}],
        "confianca": 0.92
    }

    # Cabeçalho simulado de autenticação (ajuste conforme seu token_required)
    auth_header = {"Authorization": "Bearer token-de-teste"}

    response = client.post("/api/comentarios/", json={"texto": "Excelente show!"}, headers=auth_header)

    assert response.status_code == 201
    assert "id" in response.get_json()


@patch('app.services.classifier.classificar_comentario')
def test_listar_comentarios(mock_classificar, client):
    mock_classificar.return_value = {
        "categoria": "ELOGIO",
        "tags_funcionalidades": [{"codigo": "melodia", "explicacao": "Boa melodia"}],
        "confianca": 0.92
    }

    auth_header = {"Authorization": "Bearer token-de-teste"}

    # Primeiro insere um comentário
    client.post("/api/comentarios/", json={"texto": "Excelente show!"}, headers=auth_header)

    # Depois consulta os comentários
    response = client.get("/api/comentarios/", headers=auth_header)

    assert response.status_code == 200
    resultado = response.get_json()
    assert isinstance(resultado, list)
    assert len(resultado) >= 1
    assert resultado[0]["categoria"] == "ELOGIO"
