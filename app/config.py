# app/config.py
import os

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-clave-secreta-aqui-cambiar-en-produccion'

    # Conexión a MySQL (ajusta usuario/pass/host según tu entorno)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:U22qrv88*@localhost/RutaVerdeBD'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Otras configuraciones
    DEBUG = True
