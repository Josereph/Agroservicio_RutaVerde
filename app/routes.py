from flask import Blueprint, render_template # type: ignore

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')

<<<<<<< HEAD
@bp.route('/servicios')
def servicios():
    """Ruta de servicios"""
    return render_template('Modules/Gestion_Servicio/Vista2.html', title='Servicios')
=======
@bp.route('/ubicaciones')
def ubicacion():
    """Ruta de servicios de ubicaciones"""
    return render_template('Modules/Gestion_Ubicaciones/Vista4.html', title='Servicios')
>>>>>>> f6c97e6 (cambios en routes y base.html)


<<<<<<< HEAD
=======
@bp.route('/recursos')
def recursos():
    """Mini menú de recursos operativos"""
    return render_template('layouts/MiniMenuRecursos.html', title='Recursos Operativos')


@bp.route('/vehiculos')
def vehiculos():
    """Vista del módulo de gestión de vehículos"""
    return render_template('Modules/Gestion_Vehiculos/VistaGestionVehiculos.html', title='Gestión de Vehículos')

>>>>>>> 5a697a1 (Cambios sobre diseño en mi rama)
