from flask import Blueprint, render_template # type: ignore

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')

@bp.route('/ubicaciones')
def ubicacion():
    """Ruta de servicios de ubicaciones"""
    return render_template('Modules/Gestion_Ubicaciones/Vista4.html', title='Servicios')

