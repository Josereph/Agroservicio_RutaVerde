# app/config.py
import os

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-aqui-cambiar-en-produccion'
    
    # Configuración de base de datos (ejemplo con SQLite)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:U22qrv88*@localhost/RutaVerdeBD'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECO = True #Para visualizar consultas con consola
    
    # Otras configuraciones
    class DevelopmentConfig(Config):
        DEBUG = True
        
    class ProductionConfig(Config):
        DEBUG = False
