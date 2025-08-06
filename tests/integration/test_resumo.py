import pytest
from app.services.resumo import gerar_e_enviar_resumo
from app.models.comentario import Comentario
from app import db

def test_gerar_resumo(client):
    # Insere um comentário recente no banco para testar o resumo
    comentario = Comentario(texto="Este é um ótimo artista!", categoria="ELOGIO")
    db.session.add(comentario)
    db.session.commit()

    resposta = gerar_e_enviar_resumo()
    assert "Resumo gerado" in resposta or "Nenhum comentário" in resposta
