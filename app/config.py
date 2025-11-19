# app/config.py
import os

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-aqui-cambiar-en-produccion'

    # Conexión a MySQL (ajusta usuario/pass/host según tu entorno)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:RAHP2907@localhost/RutaVerdeBD'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mostrar consultas SQL en la consola
    SQLALCHEMY_ECHO = True   # estaba mal escrito como SQLALCHEMY_ECO


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
