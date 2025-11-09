from flask import Blueprint, render_template # type: ignore

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')


@bp.route('/ubicaciones')
def ubicaciones():
    """Ruta de servicios de ubicaciones"""
    return render_template('Modules/Gestion_Ubicaciones/Vista4.html', title='Ubicaciones')

# Alias en minúsculas para evitar confusiones con /Servicios
@bp.route('/servicios')
@bp.route('/Servicios')
def servicios():
    """Ruta de servicios"""
    return render_template('Servicios.html', title='Servicios')


# 🔹 NUEVA RUTA → Mini menú de Recursos Operativos
@bp.route('/recursos')
def recursos():
    """Mini menú de recursos operativos"""
    return render_template('layouts/MiniMenuRecursos.html', title='Recursos Operativos')
