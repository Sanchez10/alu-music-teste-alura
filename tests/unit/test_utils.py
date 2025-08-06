# tests/unit/test_utils.py

import pytest
from flask import Flask, jsonify
from app.utils.auth import token_required

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True  # Ignora a verificação do token no modo de teste

    @app.route("/rota_protegida")
    @token_required
    def rota_protegida():
        return jsonify({"mensagem": "Acesso concedido"})

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_token_required_ignorado_em_modo_test(client):
    response = client.get("/rota_protegida")
    assert response.status_code == 200
    assert response.json["mensagem"] == "Acesso concedido"

def test_token_required_bloqueia_fora_do_modo_test():
    app = Flask(__name__)
    app.config['TESTING'] = False

    @app.route("/rota_real")
    @token_required
    def rota_real():
        return jsonify({"mensagem": "Acesso liberado"})

    client = app.test_client()

    # Sem token
    response = client.get("/rota_real")
    assert response.status_code == 401
    assert "erro" in response.json

    # Com token malformado
    response = client.get("/rota_real", headers={"Authorization": "InvalidToken"})
    assert response.status_code == 401

    # Com token correto
    response = client.get("/rota_real", headers={"Authorization": "Bearer qualquer_coisa"})
    assert response.status_code == 200
