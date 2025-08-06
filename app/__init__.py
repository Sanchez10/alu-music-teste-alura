import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate


db = SQLAlchemy()

def create_app(testing=False):
    load_dotenv()

    app = Flask(__name__)

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
        app.config['TESTING'] = False

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev")

    db.init_app(app)
    migrate = Migrate(app, db)

    # Blueprints
    from app.routes.comentarios import comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix="/api/comentarios")

    from app.routes.relatorio import relatorio_bp
    app.register_blueprint(relatorio_bp)

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.resumo import resumo_bp
    app.register_blueprint(resumo_bp)

    # Scheduler apenas em produção
    if not testing:
        from apscheduler.schedulers.background import BackgroundScheduler
        from app.services.resumo import gerar_e_enviar_resumo

        scheduler = BackgroundScheduler()
        scheduler.add_job(gerar_e_enviar_resumo, "interval", weeks=1)
        scheduler.start()

    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "dashboard.login"

    from app.models.user_fake import UserFake
    @login_manager.user_loader
    def load_user(user_id):
        return UserFake(user_id)

    return app
