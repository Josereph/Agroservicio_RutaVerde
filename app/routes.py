from flask import Blueprint, render_template # type: ignore

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')

@bp.route('/alertas')
def alertas():
    """
    Sistema de Alertas
    Muestra el dashboard de alertas sin registros activos
    """
    return render_template('layouts/Alertas.html', title='Sistema de Alertas')



@bp.route('/gestion_evidencia') 
def gestion_evidencia():
    """Módulo de Gestión de Evidencias y Documentación"""
    servicios = [
        {'Id_Servicio': 1, 'cliente_nombre': 'Agropecuaria Los Pinos'},
        {'Id_Servicio': 2, 'cliente_nombre': 'Distribuidora San José'},
        {'Id_Servicio': 3, 'cliente_nombre': 'Cooperativa El Progreso'}
    ]
    return render_template('modules/Gestion_Evidencia/Vista.html', title='Gestión de Evidencia',servicios=servicios)


@bp.route('/ubicaciones')
def ubicaciones():
    """Ruta de servicios de ubicaciones"""
    return render_template('Modules/Gestion_Ubicaciones/Vista4.html', title='Ubicaciones')

@bp.route('/detalles')
def detalles():
    """Ruta de servicios de detalles"""
    return render_template('Modules/Gestion_Ubicaciones/detalles.html', title='detalles')

# Alias en minúsculas para evitar confusiones con /Servicios
@bp.route('/servicios')
def servicios():
    """Ruta de servicios"""
    return render_template('Modules/Gestion_Servicio/Vista2.html', title='Servicios')


@bp.route('/conductores')
def conductores():
    """Ruta de conductores"""
    return render_template("Modules/Gestion_Conductores/chepe.html", title='Conductores')


# 🔹 NUEVA RUTA → Mini menú de Recursos Operativos
@bp.route('/recursos')
def recursos():
    """Mini menú de recursos operativos"""
    return render_template('layouts/MiniMenuRecursos.html', title='Recursos Operativos')



@bp.route('/vehiculos')
def vehiculos():
    """Vista del módulo de gestión de vehículos"""
    return render_template('Modules/Gestion_Vehiculos/VistaGestionVehiculos.html', title='Gestión de Vehículos')