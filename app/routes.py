from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')

@bp.route('/servicios')
def servicios():
    """Ruta de servicios"""
    return render_template('Modules/Gestion_Servicio/Vista2.html', title='Servicios')


# 🔹 NUEVA RUTA → Mini menú de Recursos Operativos
@bp.route('/recursos')
def recursos():
    """Mini menú de recursos operativos"""
    return render_template('layouts/MiniMenuRecursos.html', title='Recursos Operativos')
