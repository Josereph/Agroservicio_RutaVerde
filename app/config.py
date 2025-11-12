# app/config.py
import os


class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-aqui-cambiar-en-produccion'
    
    # Configuración de base de datos (ejemplo con SQLite)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:RAHP2907/RutaVerdeBD'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True #para ver las consultas SQL en la consola
    
    # Otras configuraciones
    class DevelopmentConfig(Config):
        DEBUG = True
    
    class ProductionConfig(Config):
        DEBUG = False
    
