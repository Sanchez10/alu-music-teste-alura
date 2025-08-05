from flask import Blueprint, request, jsonify
from app.models.comentario import Comentario
from app import db
from app.utils.auth import token_required
from app.services.classifier import classificar_comentario, classificar_comentarios_em_lote

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
        tags_funcionalidades=resultado["tags_funcionalidades"],
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
            "tags_funcionalidades": comentario.tags_funcionalidades,
            "confianca": comentario.confianca
        })

    return jsonify(resultado)


@comentarios_bp.route("/lote", methods=["POST"])
@token_required
def cadastrar_comentarios_em_lote():
    dados = request.get_json()
    lista_textos = dados.get("comentarios", [])

    if not isinstance(lista_textos, list) or not all(isinstance(t, str) for t in lista_textos):
        return jsonify({"erro": "Envie um JSON com uma lista de strings em 'comentarios'"}), 400

    resultados = classificar_comentarios_em_lote(lista_textos)

    comentarios_salvos = []
    for texto, resultado in zip(lista_textos, resultados):
        comentario = Comentario(
            texto=texto,
            categoria=resultado["categoria"],
            tags_funcionalidades=resultado["tags_funcionalidades"],
            confianca=resultado["confianca"]
        )
        db.session.add(comentario)
        comentarios_salvos.append({
            "texto": texto,
            "categoria": resultado["categoria"],
            "tags_funcionalidades": resultado["tags_funcionalidades"],
            "confianca": resultado["confianca"]
        })

    db.session.commit()
    return jsonify(comentarios_salvos), 201
