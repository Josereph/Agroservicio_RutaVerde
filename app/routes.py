from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')

@bp.route('/gestion_evidencia')
def servicios():
    return render_template('modules/Gestion_Evidencia/Vista.html', title='Gestión de Evidencia')





