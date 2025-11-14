# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config  # importa desde app/config.py

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)

    # 1) Cargar configuración (BD, SECRET_KEY, etc.)
    app.config.from_object(config_class)

    # 2) Inicializar SQLAlchemy con esta app
    db.init_app(app)

    # 3) Registrar blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
