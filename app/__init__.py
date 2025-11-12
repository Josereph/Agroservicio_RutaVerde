from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Blueprint principal
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # NOTA: no existe el paquete `app.Gestion_Vehiculos` en el proyecto.
    # El blueprint de gestión de vehículos está definido en `app/routes.py`
    # (variable `bp`), por eso no intentamos importar
    # `app.Gestion_Vehiculos.routes` — eso provocaba ModuleNotFoundError.

    return app
