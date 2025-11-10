from flask import Blueprint, render_template # type: ignore

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')

@bp.route('/gestion_evidencia') 
def gestion_evidencia():
    """Módulo de Gestión de Evidencias y Documentación"""
    servicios = [
        {'Id_Servicio': 1, 'cliente_nombre': 'Agropecuaria Los Pinos'},
        {'Id_Servicio': 2, 'cliente_nombre': 'Distribuidora San José'},
        {'Id_Servicio': 3, 'cliente_nombre': 'Cooperativa El Progreso'}
    ]
    return render_template('modules/Gestion_Evidencia/Vista.html', title='Gestión de Evidencia',servicios=servicios)





