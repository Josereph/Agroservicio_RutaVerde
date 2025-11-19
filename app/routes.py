from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from . import db
from .models import (
    Clientes, Evidencia, NivelFragilidad, SeguimientoControl, Servicios,
    TipoServicio, Vehiculos, CatTipoVehiculo, CatEstadoVehiculo,
    Conductor, Departamento, Municipio, Direccion, Ubicaciones
)
from datetime import datetime
import os
from werkzeug.utils import secure_filename


# ESta mrd siempre jode, ya me tiene hasta los huevos, si, esa es la gran hijueputa soluciion
bp = Blueprint('main', __name__)

# ============================================================
# RUTA PRINCIPAL
# ============================================================
@bp.route('/recursos')
def recursos():
    return render_template('layouts/MiniMenuRecursos.html', title='Recursos Operativos')


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('layouts/index.html', title='Inicio')


@bp.route('/alertas')
def alertas():
    return render_template('layouts/Alertas.html', title='Sistema de Alertas')


# ============================================================
# GESTIÓN DE EVIDENCIA
# ============================================================

def allowed_file(filename):
    allowed = {'png', 'jpg', 'jpeg', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


@bp.route('/gestion_evidencia')
def gestion_evidencia():

    # Servicios para select
    servicios = (
        db.session.query(
            Servicios.Id_Servicio,
            Clientes.Nombre_Cliente.label('cliente_nombre')
        )
        .join(Clientes)
        .order_by(Servicios.Id_Servicio.desc())
        .all()
    )

    # Evidencias en historial
    evidencias = (
        db.session.query(Evidencia, Servicios, Clientes)
        .join(Servicios, Evidencia.id_servicio == Servicios.Id_Servicio)
        .join(Clientes, Servicios.Id_Cliente == Clientes.Id_Cliente)
        .order_by(Evidencia.id_evidencia.desc())
        .all()
    )

    # Seguimientos
    seguimientos = (
        db.session.query(SeguimientoControl, Servicios, Clientes)
        .join(Servicios, SeguimientoControl.id_servicio == Servicios.Id_Servicio)
        .join(Clientes, Servicios.Id_Cliente == Clientes.Id_Cliente)
        .order_by(SeguimientoControl.id_seguimiento.desc())
        .all()
    )

    return render_template(
        'Modules/Gestion_Evidencia/Vista.html',
        servicios=servicios,
        evidencias=evidencias,
        seguimientos=seguimientos
    )


@bp.route('/evidencia/registrar', methods=['POST'])
def registrar_evidencia():

    id_servicio = request.form.get('id_servicio')
    tipo_evidencia = request.form.get('tipo_evidencia')
    es_legible = True if request.form.get('es_legible') == "1" else False
    fecha_captura = request.form.get('fecha_captura')

    archivo = request.files.get('archivo')

    if not archivo or archivo.filename == "":
        flash("Debe subir un archivo válido", "danger")
        return redirect(url_for('main.gestion_evidencia'))

    if not allowed_file(archivo.filename):
        flash("Formato no permitido. Use JPG, PNG o PDF.", "danger")
        return redirect(url_for('main.gestion_evidencia'))

    filename = secure_filename(archivo.filename)
    ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    archivo.save(ruta_guardado)

    nueva = Evidencia(
        id_servicio=id_servicio,
        tipo_evidencia=tipo_evidencia,
        nombre_archivo=filename,
        es_legible=es_legible,
        fecha_captura=fecha_captura
    )

    db.session.add(nueva)
    db.session.commit()

    flash("Evidencia registrada correctamente.", "success")
    return redirect(url_for('main.gestion_evidencia'))


# ============================================================
# SEGUIMIENTO CONTROL
# ============================================================
@bp.route('/seguimiento/registrar', methods=['POST'])
def registrar_seguimiento():

    nuevo = SeguimientoControl(
        id_servicio=request.form.get('id_servicio'),
        estado_actual=request.form.get('estado_actual'),
        control_calidad=request.form.get('control_calidad'),
        incidente=request.form.get('incidente'),
        nombre_receptor=request.form.get('nombre_receptor'),
        notificacion_enviada=True if request.form.get('notificacion_enviada') == "1" else False
    )
    db.session.add(nuevo)
    db.session.commit()

    flash("Seguimiento registrado correctamente.", "success")
    return redirect(url_for('main.gestion_evidencia'))


# ============================================================
# UBICACIONES
# ============================================================
@bp.route('/ubicaciones')
def ubicaciones():

    dep = Departamento.query.all()
    muni = Municipio.query.all()

    inventario = (
        db.session.query(Ubicaciones, Departamento, Municipio, Direccion)
        .join(Departamento)
        .join(Municipio)
        .join(Direccion)
        .all()
    )

    return render_template(
        "Modules/Gestion_Ubicaciones/Vista4.html",
        departamentos=dep,
        municipios=muni,
        inventario=inventario
    )


@bp.route("/registrar_ubicacion", methods=["POST"])
def registrar_ubicacion():

    dep = request.form["Id_Departamento"]
    muni = request.form["Id_Municipio"]
    direccion_texto = request.form.get("Direccion") or ""

    nueva_dir = Direccion(
        Id_Municipio=muni,
        Detalle_Direccion=direccion_texto
    )
    db.session.add(nueva_dir)
    db.session.commit()

    nueva = Ubicaciones(
        Id_Departamento=dep,
        Id_Municipio=muni,
        Id_Direccion=nueva_dir.Id_Direccion
    )
    db.session.add(nueva)
    db.session.commit()

    flash("Ubicación registrada correctamente", "success")
    return redirect(url_for("main.ubicaciones"))


@bp.route("/ubicaciones/<int:id_ubicacion>")
def detalles_ubicacion(id_ubicacion):

    u = Ubicaciones.query.get_or_404(id_ubicacion)
    d = Departamento.query.get(u.Id_Departamento)
    m = Municipio.query.get(u.Id_Municipio)
    dir = Direccion.query.get(u.Id_Direccion)

    sub = (
        db.session.query(Ubicaciones, Municipio, Direccion)
        .join(Municipio)
        .join(Direccion)
        .filter(Ubicaciones.Id_Departamento == u.Id_Departamento)
        .filter(Ubicaciones.Id_Ubicacion != id_ubicacion)
        .all()
    )

    return render_template(
        "Modules/Gestion_Ubicaciones/detalles.html",
        u=u,
        d=d,
        m=m,
        dir=dir,
        sub_ubicaciones=sub,
        departamentos=Departamento.query.all(),
        municipios=Municipio.query.all()
    )


@bp.route("/ubicaciones/actualizar/<int:id_ubicacion>", methods=["POST"])
def actualizar_ubicacion(id_ubicacion):

    u = Ubicaciones.query.get_or_404(id_ubicacion)
    id_direccion = request.form.get("Id_Direccion", type=int)
    dir = Direccion.query.get(id_direccion)

    if not dir:
        flash("Error: Dirección no encontrada.", "danger")
        return redirect(url_for("main.detalles_ubicacion", id_ubicacion=id_ubicacion))

    u.Id_Departamento = request.form["Id_Departamento"]
    u.Id_Municipio = request.form["Id_Municipio"]
    dir.Detalle_Direccion = request.form.get("Direccion", "").strip()

    try:
        db.session.commit()
        flash("Ubicación actualizada.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {e}", "danger")

    return redirect(url_for("main.detalles_ubicacion", id_ubicacion=id_ubicacion))


# ============================================================
# SERVICIOS
# ============================================================
@bp.route('/servicios', methods=['GET', 'POST'])
def servicios():

    clientes = Clientes.query.all()
    vehiculos = Vehiculos.query.all()
    conductores = Conductor.query.all()
    tipos = TipoServicio.query.all()
    frag = NivelFragilidad.query.all()
    ubic = Ubicaciones.query.all()

    if request.method == 'POST':
        nuevo = Servicios(
            Id_Cliente=request.form['Id_Cliente'],
            Id_Vehiculo=request.form['Id_Vehiculo'],
            id_conductor=request.form['id_conductor'],
            Id_Tipo_Servicio=request.form['Id_Tipo_Servicio'],
            Id_Fragilidad=request.form['Id_Fragilidad'],
            Id_Ubicacion=request.form['Id_Ubicacion'],
            Peso_Carga=request.form['Peso_Carga'],
            Fecha_Pedido=request.form['Fecha_Pedido'],
            Fecha_Entrega=request.form['Fecha_Entrega'],
            Precio_Total=request.form['Precio_Total']
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Servicio registrado.", "success")
        return redirect(url_for('main.servicios'))

    lista = Servicios.query.order_by(Servicios.Id_Servicio.desc()).all()

    return render_template(
        'Modules/Gestion_Servicio/Vista2.html',
        clientes=clientes,
        vehiculos=vehiculos,
        conductores=conductores,
        tipos_servicio=tipos,
        fragilidades=frag,
        ubicaciones=ubic,
        servicios=lista
    )


@bp.route('/servicios/editar/<int:id_servicio>', methods=['GET', 'POST'])
def editar_servicio(id_servicio):

    serv = Servicios.query.get_or_404(id_servicio)
    vehiculos = Vehiculos.query.all()
    conductores = Conductor.query.all()

    if request.method == 'POST':

        serv.Id_Vehiculo = request.form['id_vehiculo']
        serv.id_conductor = request.form['id_conductor']

        seg = SeguimientoControl(
            id_servicio=id_servicio,
            estado_actual=request.form['estado_actual'],
            incidente=request.form.get('comentario_estado')
        )

        db.session.add(seg)
        db.session.commit()

        flash("Servicio actualizado.", "success")
        return redirect(url_for('main.servicios'))

    return render_template(
        'Modules/Gestion_Servicio/Editar_Servicio.html',
        servicio=serv,
        vehiculos=vehiculos,
        conductores=conductores
    )


@bp.route('/servicios/eliminar/<int:id_servicio>', methods=['POST'])
def eliminar_servicio(id_servicio):

    serv = Servicios.query.get_or_404(id_servicio)

    for s in serv.seguimientos:
        db.session.delete(s)
    for e in serv.evidencias:
        db.session.delete(e)

    db.session.delete(serv)
    db.session.commit()

    flash("Servicio eliminado.", "success")
    return redirect(url_for('main.servicios'))


# ============================================================
# CONDUCTORES
# ============================================================
@bp.route('/conductores', methods=['GET', 'POST'])
def conductores_view():

    if request.method == 'POST':

        nombre = request.form.get('nombre_completo')
        documento = request.form.get('documento_identificacion')
        tipo_lic = request.form.get('tipo_licencia')
        fecha_venc = request.form.get('fecha_vencimiento_licencia')

        if not all([nombre, documento, tipo_lic, fecha_venc]):
            flash("Completa todos los campos obligatorios.", "danger")
            return redirect(url_for('main.conductores_view'))

        nuevo = Conductor(
            nombre_completo=nombre,
            documento_identificacion=documento,
            tipo_licencia=tipo_lic,
            fecha_vencimiento_licencia=datetime.strptime(fecha_venc, "%Y-%m-%d"),
            telefono=request.form.get('telefono') or None,
            correo=request.form.get('correo') or None,
            estado=request.form.get('estado') or "Activo",
            experiencia_notas=request.form.get('experiencia_notas') or None
        )

        db.session.add(nuevo)
        db.session.commit()
        flash("Conductor registrado.", "success")
        return redirect(url_for('main.conductores_view'))

    lista = Conductor.query.order_by(Conductor.nombre_completo).all()

    return render_template(
        "Modules/Gestion_Conductores/VistaGestionConductores.html",
        conductores=lista
    )


# ============================================================
# VEHÍCULOS
# ============================================================
from sqlalchemy import or_

@bp.route('/vehiculos', methods=['GET', 'POST'])
def vehiculos_view():

    if request.method == 'POST':

        nuevo = Vehiculos(
            unidad_numero=request.form.get('unidad_numero'),
            placa=request.form.get('placa'),
            marca=request.form.get('marca'),
            modelo=request.form.get('modelo'),
            anio=request.form.get('anio', type=int),
            capacidad_kg=request.form.get('capacidad', type=float),
            tipo_id=request.form.get('tipo_id', type=int),
            estado_id=request.form.get('estado_id', type=int),
            vin=request.form.get('vin') or None,
            km_actual=request.form.get('km_actual', type=int) or 0,
            seguro_vigente=True if request.form.get('seguro_vigente') == "1" else False,
            aseguradora=request.form.get('aseguradora') or None,
            poliza_numero=request.form.get('poliza_numero') or None,
            fecha_venc_seguro=request.form.get('fecha_venc_seguro') or None,
            observaciones=request.form.get('observaciones') or None
        )

        db.session.add(nuevo)
        db.session.commit()

        flash("Vehículo registrado.", "success")
        return redirect(url_for('main.vehiculos_view'))

    q = request.args.get('q', '', type=str).strip()
    tipo = request.args.get('tipo_id', type=int)
    estado = request.args.get('estado_id', type=int)

    consulta = Vehiculos.query

    if q:
        patron = f"%{q}%"
        consulta = consulta.filter(
            or_(
                Vehiculos.placa.ilike(patron),
                Vehiculos.marca.ilike(patron),
                Vehiculos.modelo.ilike(patron)
            )
        )

    if tipo:
        consulta = consulta.filter(Vehiculos.tipo_id == tipo)

    if estado:
        consulta = consulta.filter(Vehiculos.estado_id == estado)

    vehiculos_lista = consulta.all()

    return render_template(
        "Modules/Gestion_Vehiculos/VistaGestionVehiculos.html",
        vehiculos=vehiculos_lista,
        tipos=CatTipoVehiculo.query.all(),
        estados=CatEstadoVehiculo.query.all(),
        q=q,
        tipo_sel=tipo,
        estado_sel=estado
    )


@bp.route('/vehiculos/editar/<int:id_vehiculo>', methods=['GET', 'POST'])
def editar_vehiculo(id_vehiculo):

    v = Vehiculos.query.get_or_404(id_vehiculo)

    if request.method == 'POST':

        v.unidad_numero = request.form.get('unidad_numero')
        v.placa = request.form.get('placa')
        v.marca = request.form.get('marca')
        v.modelo = request.form.get('modelo')
        v.anio = request.form.get('anio', type=int)
        v.capacidad_kg = request.form.get('capacidad', type=float)
        v.tipo_id = request.form.get('tipo_id', type=int)
        v.estado_id = request.form.get('estado_id', type=int)
        v.vin = request.form.get('vin') or None
        v.km_actual = request.form.get('km_actual', type=int) or 0
        v.seguro_vigente = True if request.form.get('seguro_vigente') == "1" else False
        v.aseguradora = request.form.get('aseguradora') or None
        v.poliza_numero = request.form.get('poliza_numero') or None
        v.fecha_venc_seguro = request.form.get('fecha_venc_seguro') or None
        v.observaciones = request.form.get('observaciones') or None

        db.session.commit()
        flash("Vehículo actualizado.", "success")
        return redirect(url_for('main.vehiculos_view'))

    return render_template(
        "Modules/Gestion_Vehiculos/EditarVehiculo.html",
        vehiculo=v,
        tipos=CatTipoVehiculo.query.all(),
        estados=CatEstadoVehiculo.query.all()
    )


@bp.route('/vehiculos/eliminar/<int:id_vehiculo>', methods=['POST'])
def eliminar_vehiculo(id_vehiculo):

    v = Vehiculos.query.get_or_404(id_vehiculo)
    db.session.delete(v)
    db.session.commit()

    flash("Vehículo eliminado.", "success")
    return redirect(url_for('main.vehiculos_view'))


# ============================================================
# REPORTE Y BÚSQUEDA
# ============================================================
@bp.route('/busqueda')
def busqueda():
    return render_template('layouts/busqueda.html')


@bp.route('/reportes')
def reportes():
    return render_template('layouts/Reportes.html')