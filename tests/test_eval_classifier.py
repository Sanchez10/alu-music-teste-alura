import pytest
from sklearn.metrics import classification_report, f1_score
from unittest.mock import patch
from app.services.classifier import classificar_comentario

dados_teste = [
    ("Esse show foi incrível!", "ELOGIO"),
    ("Poderia ter mais informações sobre o evento", "SUGESTÃO"),
    ("Que horário vai começar o show?", "DÚVIDA"),
    ("Comprei e não recebi nada ainda!", "CRÍTICA"),
    ("Ganhe ingressos grátis aqui!", "SPAM")
]

@patch("app.services.classifier.classificar_comentario")
def test_avaliacao_llm(mock_classificar):
    # Simula respostas fixas
    mock_classificar.side_effect = lambda texto: {
        "categoria": {
            "Esse show foi incrível!": "ELOGIO",
            "Poderia ter mais informações sobre o evento": "SUGESTÃO",
            "Que horário vai começar o show?": "DÚVIDA",
            "Comprei e não recebi nada ainda!": "CRÍTICA",
            "Ganhe ingressos grátis aqui!": "SPAM",
        }.get(texto, "ELOGIO"),
        "tags_funcionalidades": [],
        "confianca": 0.95
    }

    verdadeiros = []
    previstos = []

    for texto, esperado in dados_teste:
        resultado = classificar_comentario(texto)
        verdadeiros.append(esperado)
        previstos.append(resultado["categoria"])

    print("\nRelatório de Avaliação:\n")
    print(classification_report(verdadeiros, previstos, zero_division=0))

    f1 = f1_score(verdadeiros, previstos, average="macro")
    assert f1 >= 0.7, f"F1 Score muito baixo: {f1:.2f}"
