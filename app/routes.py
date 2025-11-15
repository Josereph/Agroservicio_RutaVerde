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
    # ---------- POST → Registrar nuevo vehículo ----------
    if request.method == 'POST':
        print("⚠️ LLEGÓ POST /vehiculos")
        print("FORM DATA:", request.form)

        unidad_numero = request.form.get('unidad_numero')
        placa = request.form.get('placa')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        anio = request.form.get('anio', type=int)
        capacidad = request.form.get('capacidad', type=float)

        # Estos NOMBRES deben coincidir con name="..." del HTML
        tipo_id = request.form.get('tipo_id', type=int)
        estado_id = request.form.get('estado_id', type=int)

        vin = request.form.get('vin') or None
        km = request.form.get('km_actual', type=int)
        seguro_raw = request.form.get('seguro_vigente')
        aseguradora = request.form.get('aseguradora') or None
        poliza = request.form.get('poliza_numero') or None
        fecha_seguro = request.form.get('fecha_venc_seguro') or None
        obs = request.form.get('observaciones') or None

        # Normalizar km y seguro_vigente
        if km is None:
            km = 0
        seguro_vigente = True if seguro_raw == "1" else False

        # Validación mínima (solo campos obligatorios de verdad)
        if not all([unidad_numero, placa, tipo_id, capacidad, estado_id]):
            flash("Debes completar los campos obligatorios: unidad, placa, tipo, capacidad y estado.", "danger")
            return redirect(url_for('main.vehiculos'))

        # Crear objeto vehículo con TODOS los campos que quieres guardar
        nuevo = Vehiculos(
            unidad_numero=unidad_numero,
            placa=placa,
            vin=vin,
            marca=marca,
            modelo=modelo,
            anio=anio,
            capacidad_kg=capacidad,
            tipo_id=tipo_id,
            estado_id=estado_id,
            km_actual=km,
            seguro_vigente=seguro_vigente,
            aseguradora=aseguradora,
            poliza_numero=poliza,
            fecha_venc_seguro=fecha_seguro,
            observaciones=obs
        )

        try:
            db.session.add(nuevo)
            db.session.commit()
            print("✅ Vehículo insertado con ID:", nuevo.id_vehiculo)
            flash("Vehículo registrado correctamente.", "success")
        except Exception as e:
            db.session.rollback()
            print("❌ ERROR al guardar vehículo:", e)
            flash(f"Error al guardar el vehículo: {e}", "danger")

        return redirect(url_for('main.vehiculos'))

    # ---------- GET → Mostrar formulario y tabla ----------
    tipos = CatTipoVehiculo.query.order_by(CatTipoVehiculo.nombre).all()
    estados = CatEstadoVehiculo.query.order_by(CatEstadoVehiculo.nombre).all()
    lista_vehiculos = Vehiculos.query.all()

    return render_template(
        'Modules/Gestion_Vehiculos/VistaGestionVehiculos.html',
        title='Gestión de Vehículos',
        vehiculos=lista_vehiculos,
        tipos=tipos,
        estados=estados
    )
    
    # ============================================================
# EDITAR VEHÍCULO
# ============================================================
@bp.route('/vehiculos/editar/<int:id_vehiculo>', methods=['GET', 'POST'])
def editar_vehiculo(id_vehiculo):
    vehiculo = Vehiculos.query.get_or_404(id_vehiculo)

    if request.method == 'POST':
        # Mismos campos que en crear
        unidad_numero = request.form.get('unidad_numero')
        placa = request.form.get('placa')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        anio = request.form.get('anio', type=int)
        capacidad = request.form.get('capacidad', type=float)

        tipo_id = request.form.get('tipo_id', type=int)
        estado_id = request.form.get('estado_id', type=int)

        vin = request.form.get('vin') or None
        km = request.form.get('km_actual', type=int)
        seguro_raw = request.form.get('seguro_vigente')
        aseguradora = request.form.get('aseguradora') or None
        poliza = request.form.get('poliza_numero') or None
        fecha_seguro = request.form.get('fecha_venc_seguro') or None
        obs = request.form.get('observaciones') or None

        if km is None:
            km = 0
        seguro_vigente = True if seguro_raw == "1" else False

        if not all([unidad_numero, placa, tipo_id, capacidad, estado_id]):
            flash("Debes completar los campos obligatorios: unidad, placa, tipo, capacidad y estado.", "danger")
            return redirect(url_for('main.editar_vehiculo', id_vehiculo=id_vehiculo))

        # Asignar cambios al objeto existente
        vehiculo.unidad_numero = unidad_numero
        vehiculo.placa = placa
        vehiculo.marca = marca
        vehiculo.modelo = modelo
        vehiculo.anio = anio
        vehiculo.capacidad_kg = capacidad
        vehiculo.tipo_id = tipo_id
        vehiculo.estado_id = estado_id
        vehiculo.vin = vin
        vehiculo.km_actual = km
        vehiculo.seguro_vigente = seguro_vigente
        vehiculo.aseguradora = aseguradora
        vehiculo.poliza_numero = poliza
        vehiculo.fecha_venc_seguro = fecha_seguro
        vehiculo.observaciones = obs

        try:
            db.session.commit()
            flash("Vehículo actualizado correctamente.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el vehículo: {e}", "danger")

        return redirect(url_for('main.vehiculos'))

    # GET → mostrar formulario de edición
    tipos = CatTipoVehiculo.query.order_by(CatTipoVehiculo.nombre).all()
    estados = CatEstadoVehiculo.query.order_by(CatEstadoVehiculo.nombre).all()

    return render_template(
        'Modules/Gestion_Vehiculos/EditarVehiculo.html',
        title='Editar Vehículo',
        vehiculo=vehiculo,
        tipos=tipos,
        estados=estados
    )


# ============================================================
# ELIMINAR VEHÍCULO
# ============================================================
@bp.route('/vehiculos/eliminar/<int:id_vehiculo>', methods=['POST'])
def eliminar_vehiculo(id_vehiculo):
    vehiculo = Vehiculos.query.get_or_404(id_vehiculo)

    try:
        db.session.delete(vehiculo)
        db.session.commit()
        flash(f"Vehículo {vehiculo.placa} eliminado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar el vehículo: {e}", "danger")

    return redirect(url_for('main.vehiculos'))

