from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Vehiculos, CatTipoVehiculo, CatEstadoVehiculo

bp = Blueprint('main', __name__)

# ============================================================
# RUTA PRINCIPAL
# ============================================================
@bp.route('/')
@bp.route('/index')
def index():
    return render_template('layouts/index.html', title='Inicio')

@bp.route('/alertas')
def alertas():
    """
    Sistema de Alertas
    Muestra el dashboard de alertas sin registros activos
    """
    return render_template('layouts/Alertas.html', title='Sistema de Alertas')


# ============================================================
# GESTIÓN DE EVIDENCIA
# ============================================================
@bp.route('/gestion_evidencia')
def gestion_evidencia():
    servicios = [
        {'Id_Servicio': 1, 'cliente_nombre': 'Agropecuaria Los Pinos'},
        {'Id_Servicio': 2, 'cliente_nombre': 'Distribuidora San José'},
        {'Id_Servicio': 3, 'cliente_nombre': 'Cooperativa El Progreso'}
    ]
    return render_template(
        'modules/Gestion_Evidencia/Vista.html',
        title='Gestión de Evidencia',
        servicios=servicios
    )


# ============================================================
# UBICACIONES
# ============================================================
@bp.route('/ubicaciones')
def ubicaciones():
    return render_template('Modules/Gestion_Ubicaciones/Vista4.html', title='Ubicaciones')


@bp.route('/detalles')
def detalles():
    return render_template('Modules/Gestion_Ubicaciones/detalles.html', title='Detalles')


# ============================================================
# SERVICIOS
# ============================================================
@bp.route('/servicios')
def servicios():
    return render_template('Modules/Gestion_Servicio/Vista2.html', title='Servicios')




# ============================================================
# CONDUCTORES
# ============================================================
@bp.route('/conductores')
def conductores():
    return render_template("Modules/Gestion_Conductores/chepe.html", title='Conductores')


# ============================================================
# MINI MENÚ DE RECURSOS OPERATIVOS
# ============================================================
@bp.route('/recursos')
def recursos():
    return render_template('layouts/MiniMenuRecursos.html', title='Recursos Operativos')


# ============================================================
# GESTIÓN DE VEHÍCULOS (GET + POST)
# ============================================================
@bp.route('/vehiculos', methods=['GET', 'POST'])
def vehiculos():
    """Vista del módulo de gestión de vehículos"""
    return render_template('Modules/Gestion_Vehiculos/VistaGestionVehiculos.html', title='Gestión de Vehículos')
