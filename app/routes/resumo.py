from flask import Blueprint, jsonify
from app.services.resumo import gerar_e_enviar_resumo
from app.models.resumo import ResumoSemanal

resumo_bp = Blueprint("resumo", __name__, url_prefix="/resumo")

@resumo_bp.route("/resumo/gerar", methods=["POST"])
def gerar_resumo():
    resultado = gerar_e_enviar_resumo()
    return jsonify({"mensagem": resultado})

@resumo_bp.route("/resumo/testar", methods=["POST"])
def testar_resumo():
    resultado = gerar_e_enviar_resumo()
    return jsonify({"mensagem": resultado})

@resumo_bp.route("/semanal", methods=["GET"])
def listar_resumos():
    resumos = ResumoSemanal.query.order_by(ResumoSemanal.data_fim.desc()).limit(5).all()
    return jsonify([
        {
            "inicio": r.data_inicio.isoformat(),
            "fim": r.data_fim.isoformat(),
            "resumo": r.resumo
        } for r in resumos
    ])
