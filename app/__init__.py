import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app(testing=False):
    load_dotenv()

    app = Flask(__name__)

    if testing:
        # Configuração para testes
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        app.config['TESTING'] = True
    else:
        # Configuração padrão (produção/desenvolvimento)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
        app.config['TESTING'] = False

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev")

    db.init_app(app)

    from app.routes.comentarios import comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix="/api/comentarios")

    return app
