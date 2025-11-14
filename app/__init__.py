# app/__init__.py
from flask import Flask

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

    # NOTA: no existe el paquete app.Gestion_Vehiculos en el proyecto.
    # El blueprint de gestión de vehículos está definido en app/routes.py
    # (variable bp), por eso no intentamos importar
    # app.Gestion_Vehiculos.routes — eso provocaba ModuleNotFoundError.

    return app
