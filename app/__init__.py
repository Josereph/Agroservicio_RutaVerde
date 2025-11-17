# app/__init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import os

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)

    # Cargar configuración general (incluye BD)
    app.config.from_object(config_class)

    # Carpetas para evidencias
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads', 'evidencias')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

    # Inicializar BD
    db.init_app(app)

    # Registrar blueprint
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Manejo de errores
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('layouts/404.html'), 404

    return app
