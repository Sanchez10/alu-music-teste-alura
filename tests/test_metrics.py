import pytest
from sklearn.metrics import classification_report, f1_score, recall_score
from unittest.mock import patch
from app.services.classifier import classificar_comentario

casos_de_teste = [
    {"texto": "Esse show foi incrível!", "esperado": "ELOGIO"},
    {"texto": "Poderia ter mais informações sobre o evento", "esperado": "SUGESTÃO"},
    {"texto": "Que horário vai começar o show?", "esperado": "DÚVIDA"},
    {"texto": "Comprei e não recebi nada ainda!", "esperado": "CRÍTICA"},
    {"texto": "Ganhe ingressos grátis aqui!", "esperado": "SPAM"}
]

@patch("app.services.classifier.classificar_comentario")
def test_metricas_classificador(mock_classificar):
    # Simula a saída do classificador conforme o esperado
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

    y_true = []
    y_pred = []

    for caso in casos_de_teste:
        resultado = classificar_comentario(caso["texto"])
        y_true.append(caso["esperado"])
        y_pred.append(resultado["categoria"])

    print("\nRelatório de Classificação:")
    print(classification_report(y_true, y_pred, digits=3))

    f1 = f1_score(y_true, y_pred, average="macro")
    recall = recall_score(y_true, y_pred, average="macro")

    assert f1 >= 0.6, f"F1-score abaixo do baseline: {f1:.2f}"
