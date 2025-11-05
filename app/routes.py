from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')

@bp.route('/Servicios')
def servicios():
    """Ruta de servicios"""
    return render_template('Servicios.html', title='Servicios')

@bp.route('/conductores')
def conductores():
    """Ruta de conductores"""
    return render_template("Modules/Gestion_Conductores/chepe.html", title='Conductores')