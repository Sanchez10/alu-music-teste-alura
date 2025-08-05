from app import db
import uuid

from sqlalchemy.dialects.postgresql import JSONB

class Comentario(db.Model):
    __tablename__ = "comentarios"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    texto = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(20))
    tags_funcionalidades = db.Column(JSONB)
    confianca = db.Column(db.Float)
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
