# tests/unit/test_models.py

from app.models.comentario import Comentario
import uuid

def test_model_comentario_instanciacao():
    comentario = Comentario(
        texto="Ótimo atendimento!",
        categoria="ELOGIO",
        tags_funcionalidades=[{"codigo": "atendimento", "explicacao": "Rápido"}],
        confianca=0.95
    )

    # ID deve ser string UUID
    assert comentario.id is not None
    assert isinstance(uuid.UUID(comentario.id), uuid.UUID)

    assert comentario.texto == "Ótimo atendimento!"
    assert comentario.categoria == "ELOGIO"
    assert isinstance(comentario.tags_funcionalidades, list)
    assert comentario.tags_funcionalidades[0]["codigo"] == "atendimento"
    assert comentario.confianca == 0.95

    # criado_em é setado automaticamente pelo banco — será None até inserção no banco
    assert comentario.criado_em is None
