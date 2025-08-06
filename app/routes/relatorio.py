from flask import Blueprint, send_file
from app.models.comentario import Comentario
from sqlalchemy import extract, func
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from cachetools import TTLCache

relatorio_bp = Blueprint("relatorio", __name__)
cache = TTLCache(maxsize=10, ttl=60)

@relatorio_bp.route("/relatorio/semana")
def relatorio_semana():
    if 'grafico' in cache:
        return send_file(cache['grafico'], mimetype='image/png')

    sete_dias_atras = datetime.utcnow() - timedelta(days=7)

    dados = (
        Comentario.query
        .filter(Comentario.criado_em >= sete_dias_atras)
        .with_entities(Comentario.categoria, func.count().label("quantidade"))
        .group_by(Comentario.categoria)
        .all()
    )

    categorias = [d[0] for d in dados]
    quantidades = [d[1] for d in dados]

    fig, ax = plt.subplots()
    ax.bar(categorias, quantidades)
    ax.set_title("Comentários por Categoria - Últimos 7 dias")

    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    cache['grafico'] = img
    return send_file(img, mimetype='image/png')
