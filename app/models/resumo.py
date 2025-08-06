from app import db
import uuid

class ResumoSemanal(db.Model):
    __tablename__ = "resumos_semanal"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    resumo = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
