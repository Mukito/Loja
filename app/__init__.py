from flask import Flask
from app.config import Config
from app.database import init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as tabelas do SQLite dentro do contexto do app
    with app.app_context():
        init_db()

    # Registro de módulos/rotas
    from app.routes.auth_routes import auth_bp
    from app.routes.store_routes import store_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(store_bp)

    return app
