from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Ruta principal de la aplicacion"""
    return render_template('layouts/index.html', title='Inicio')

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
# Alias en minúsculas para evitar confusiones con /Servicios
@bp.route('/servicios')
@bp.route('/Servicios')
=======
@bp.route('/gestion_evidencia')

# Alias en minúsculas para evitar confusiones con /Servicios
@bp.route('/servicios')
@bp.route('/Servicios')

>>>>>>> 405b73d (resolviendo conflictos)
def servicios():
    """Ruta de servicios"""
    return render_template('Modules/Gestion_Servicio/Vista2.html', title='Servicios')
=======
@bp.route('/gestion_evidencia') 
def gestion_evidencia():
    """Módulo de Gestión de Evidencias y Documentación"""
    servicios = [
        {'Id_Servicio': 1, 'cliente_nombre': 'Agropecuaria Los Pinos'},
        {'Id_Servicio': 2, 'cliente_nombre': 'Distribuidora San José'},
        {'Id_Servicio': 3, 'cliente_nombre': 'Cooperativa El Progreso'}
    ]
    return render_template('modules/Gestion_Evidencia/Vista.html', title='Gestión de Evidencia',servicios=servicios)


>>>>>>> 5dfc803 (Agregar diseño en el modulo Gestion_Evidencia)


@bp.route('/conductores')
def conductores():
    """Ruta de conductores"""
    return render_template("Modules/Gestion_Conductores/chepe.html", title='Conductores')

# 🔹 NUEVA RUTA → Mini menú de Recursos Operativos
@bp.route('/recursos')
def recursos():
    """Mini menú de recursos operativos"""
    return render_template('layouts/MiniMenuRecursos.html', title='Recursos Operativos')
=======
@bp.route('/gestion_evidencia')
def servicios():
    return render_template('modules/Gestion_Evidencia/Vista.html', title='Gestión de Evidencia')




>>>>>>> 8e34deb (Rutas agregadas)

