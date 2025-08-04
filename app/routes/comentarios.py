from flask import Blueprint, request, jsonify
from app.models.comentario import Comentario
from app import db
from app.utils.auth import token_required
from app.services.classifier import classificar_comentario

comentarios_bp = Blueprint("comentarios", __name__)

@comentarios_bp.route("/", methods=["POST"])
@token_required
def cadastrar_comentario():
    dados = request.get_json()
    texto = dados.get("texto")
    if not texto:
        return jsonify({"erro": "Texto é obrigatório"}), 400

    resultado = classificar_comentario(texto)
    comentario = Comentario(
        texto=texto,
        categoria=resultado["categoria"],
        tags=",".join(resultado["tags"]),
        confianca=resultado["confianca"]
    )
    db.session.add(comentario)
    db.session.commit()
    return jsonify({"id": comentario.id}), 201


@comentarios_bp.route("/", methods=["GET"])
@token_required
def listar_comentarios():
    comentarios = Comentario.query.all()

    resultado = []
    for comentario in comentarios:
        resultado.append({
            "id": comentario.id,
            "texto": comentario.texto,
            "categoria": comentario.categoria,
            "tags": comentario.tags,
            "confianca": comentario.confianca
        })

    return jsonify(resultado)
