from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')

# Alias en minúsculas para evitar confusiones con /Servicios
@bp.route('/servicios')
@bp.route('/Servicios')
def servicios():
    """Ruta de servicios"""
    return render_template('Servicios.html', title='Servicios')


@bp.route('/conductores')
def conductores():
    """Ruta de conductores"""
    return render_template("Modules/Gestion_Conductores/chepe.html", title='Conductores')

# 🔹 NUEVA RUTA → Mini menú de Recursos Operativos
@bp.route('/recursos')
def recursos():
    """Mini menú de recursos operativos"""
    return render_template('layouts/MiniMenuRecursos.html', title='Recursos Operativos')

