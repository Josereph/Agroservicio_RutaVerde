from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #Registrar las rutas
    from app import routes
    app.register_blueprint(routes.bp)
    return app
