from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from . import db
from .models import Clientes, Evidencia, NivelFragilidad, SeguimientoControl, Servicios, TipoServicio, Vehiculos, CatTipoVehiculo, CatEstadoVehiculo, Conductor, Departamento, Municipio, Direccion, Ubicaciones
from datetime import datetime
import os
from werkzeug.utils import secure_filename


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
    # Servicios listados para los SELECT
    servicios = (
        db.session.query(
            Servicios.Id_Servicio,
            Clientes.Nombre_Cliente.label('cliente_nombre')
        )
        .join(Clientes)
        .order_by(Servicios.Id_Servicio.desc())
        .all()
    )

    # Historial de evidencias
    evidencias = (
        db.session.query(Evidencia, Servicios, Clientes)
        .join(Servicios, Evidencia.id_servicio == Servicios.Id_Servicio)
        .join(Clientes, Servicios.Id_Cliente == Clientes.Id_Cliente)
        .order_by(Evidencia.id_evidencia.desc())
        .all()
    )

    # Historial de seguimientos
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

    
@bp.route('/seguimiento/registrar', methods=['POST'])
def registrar_seguimiento():

    id_servicio = request.form.get('id_servicio')
    estado_actual = request.form.get('estado_actual')
    control_calidad = request.form.get('control_calidad')
    incidente = request.form.get('incidente')
    nombre_receptor = request.form.get('nombre_receptor')
    notificacion = True if request.form.get('notificacion_enviada') == "1" else False

    nuevo = SeguimientoControl(
        id_servicio=id_servicio,
        estado_actual=estado_actual,
        control_calidad=control_calidad,
        incidente=incidente,
        nombre_receptor=nombre_receptor,
        notificacion_enviada=notificacion
    )

    db.session.add(nuevo)
    db.session.commit()

    flash("📊 Seguimiento registrado correctamente.", "success")
    return redirect(url_for('main.gestion_evidencia'))



@bp.route('/evidencia/registrar', methods=['POST'])
def registrar_evidencia():

    id_servicio = request.form.get('id_servicio')
    tipo_evidencia = request.form.get('tipo_evidencia')
    es_legible = True if request.form.get('es_legible') == "1" else False
    fecha_captura = request.form.get('fecha_captura')

    archivo = request.files.get('archivo')

    # Validar archivo
    if not archivo or archivo.filename == "":
        flash("Debe subir un archivo válido", "danger")
        return redirect(url_for('main.gestion_evidencia'))

    if not allowed_file(archivo.filename):
        flash("Formato no permitido. Use JPG, PNG o PDF.", "danger")
        return redirect(url_for('main.gestion_evidencia'))

    # Guardar archivo
    filename = secure_filename(archivo.filename)
    ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    archivo.save(ruta_guardado)

    # Crear evidencia
    nueva = Evidencia(
        id_servicio=id_servicio,
        tipo_evidencia=tipo_evidencia,
        nombre_archivo=filename,
        es_legible=es_legible,
        fecha_captura=fecha_captura
    )

    db.session.add(nueva)
    db.session.commit()

    flash("📸 Evidencia registrada correctamente.", "success")
    return redirect(url_for('main.gestion_evidencia'))




def allowed_file(filename):
    allowed = {'png', 'jpg', 'jpeg', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

  
# ============================================================
# UBICACIONES
# ============================================================
@bp.route('/ubicaciones')
def ubicaciones():

    departamentos = Departamento.query.all()
    municipios = Municipio.query.all()

    inventario = (
        db.session.query(Ubicaciones, Departamento, Municipio, Direccion)
        .join(Departamento, Ubicaciones.Id_Departamento == Departamento.Id_Departamento)
        .join(Municipio, Ubicaciones.Id_Municipio == Municipio.Id_Municipio)
        .join(Direccion, Ubicaciones.Id_Direccion == Direccion.Id_Direccion)
        .all()
    )

    return render_template(
        "Modules/Gestion_Ubicaciones/Vista4.html",
        departamentos=departamentos,
        municipios=municipios,
        inventario=inventario
    )



@bp.route("/registrar_ubicacion", methods=["POST"])
def registrar_ubicacion():
    dep = request.form["Id_Departamento"]
    muni = request.form["Id_Municipio"]
    direccion_texto = request.form.get("Direccion") or ""

    # 1) Crear dirección
    nueva_dir = Direccion(
        Id_Municipio=muni,
        Detalle_Direccion=direccion_texto
    )
    db.session.add(nueva_dir)
    db.session.commit()

    # 2) Crear ubicación
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

    # Sububicaciones del MISMO departamento
    sub_ubicaciones = (
        db.session.query(Ubicaciones, Municipio, Direccion)
        .join(Municipio)
        .join(Direccion)
        .filter(Ubicaciones.Id_Departamento == u.Id_Departamento)
        .filter(Ubicaciones.Id_Ubicacion != id_ubicacion)
        .all()
    )

    departamentos = Departamento.query.all()
    municipios = Municipio.query.all()
    
    return render_template(
    "Modules/Gestion_Ubicaciones/detalles.html",
    u=u,
    d=d,
    m=m,
    dir=dir,
    sub_ubicaciones=sub_ubicaciones,
    departamentos=departamentos,
    municipios=municipios
    )




# ============================================================
# SERVICIOS
# ============================================================

@property
def ultimo_estado(self):
    return self.seguimientos.order_by(SeguimientoControl.id_seguimiento.desc()).first()


@bp.route('/servicios', methods=['GET', 'POST'])
def servicios():

    clientes = Clientes.query.all()
    vehiculos = Vehiculos.query.all()
    conductores = Conductor.query.all()
    tipos_servicio = TipoServicio.query.all()
    fragilidades = NivelFragilidad.query.all()
    ubicaciones = Ubicaciones.query.all()

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

        flash("Servicio registrado correctamente.", "success")
        return redirect(url_for('main.servicios'))

    lista_servicios = Servicios.query.order_by(Servicios.Id_Servicio.desc()).all()

    return render_template(
        'Modules/Gestion_Servicio/Vista2.html',
        clientes=clientes,
        vehiculos=vehiculos,
        conductores=conductores,
        tipos_servicio=tipos_servicio,
        fragilidades=fragilidades,
        ubicaciones=ubicaciones,
        servicios=lista_servicios
    )
    
@bp.route('/servicios/editar/<int:id_servicio>', methods=['GET', 'POST'])
def editar_servicio(id_servicio):
    servicio = Servicios.query.get_or_404(id_servicio)

    vehiculos = Vehiculos.query.all()
    conductores = Conductor.query.all()

    if request.method == 'POST':
        servicio.Id_Vehiculo = request.form['id_vehiculo']
        servicio.id_conductor = request.form['id_conductor']

        nuevo_estado = request.form['estado_actual']
        comentario = request.form.get('comentario_estado')

        seg = SeguimientoControl(
            id_servicio=id_servicio,
            estado_actual=nuevo_estado,
            incidente=comentario
        )
        db.session.add(seg)

        db.session.commit()

        flash("Servicio actualizado correctamente.", "success")
        return redirect(url_for('main.servicios'))

    return render_template(
        'Modules/Gestion_Servicio/Editar_Servicio.html',
        servicio=servicio,
        vehiculos=vehiculos,
        conductores=conductores
    )
    
@bp.route('/servicios/eliminar/<int:id_servicio>', methods=['POST'])
def eliminar_servicio(id_servicio):
    servicio = Servicios.query.get_or_404(id_servicio)

    # Eliminar seguimientos y evidencias
    for s in servicio.seguimientos:
        db.session.delete(s)
    for e in servicio.evidencias:
        db.session.delete(e)

    db.session.delete(servicio)
    db.session.commit()

    flash("Servicio eliminado correctamente.", "success")
    return redirect(url_for('main.servicios'))



@bp.route('/conductores')
def conductores():
    # ---------- POST → Registrar nuevo conductor ----------
    if request.method == 'POST':
        nombre = request.form.get('nombre_completo')
        documento = request.form.get('documento_identificacion')
        tipo_licencia = request.form.get('tipo_licencia')
        fecha_venc_str = request.form.get('fecha_vencimiento_licencia')
        telefono = request.form.get('telefono') or None
        correo = request.form.get('correo') or None
        estado = request.form.get('estado') or 'Activo'
        experiencia = request.form.get('experiencia_notas') or None

        # Validar obligatorios reales de la BD
        if not all([nombre, documento, tipo_licencia, fecha_venc_str]):
            flash("Completa nombre, documento, tipo de licencia y fecha de vencimiento.", "danger")
            return redirect(url_for('main.conductores'))

        # Convertir fecha
        try:
            fecha_venc = datetime.strptime(fecha_venc_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Fecha de vencimiento inválida.", "danger")
            return redirect(url_for('main.conductores'))

        nuevo = Conductor(
            nombre_completo=nombre,
            documento_identificacion=documento,
            tipo_licencia=tipo_licencia,
            fecha_vencimiento_licencia=fecha_venc,
            telefono=telefono,
            correo=correo,
            estado=estado,
            experiencia_notas=experiencia
        )

        try:
            db.session.add(nuevo)
            db.session.commit()
            flash("Conductor registrado correctamente.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar el conductor: {e}", "danger")

        return redirect(url_for('main.conductores'))

    # ---------- GET → Mostrar lista de conductores ----------
    lista_conductores = Conductor.query.order_by(Conductor.nombre_completo).all()

    return render_template(
        "Modules/Gestion_Conductores/VistaGestionConductores.html",
        title="Gestión de Conductores",
        conductores=lista_conductores
    )


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
       # ---------- GET → Mostrar formulario y tabla con filtros ----------
    from sqlalchemy import or_

    # Leer parámetros de búsqueda desde la URL (GET)
    q = request.args.get('q', '', type=str).strip()
    tipo_filtro = request.args.get('tipo_id', type=int)
    estado_filtro = request.args.get('estado_id', type=int)

    # Consulta base
    consulta = Vehiculos.query

    # Filtro de texto: placa, marca o modelo
    if q:
        patron = f"%{q}%"
        consulta = consulta.filter(
            or_(
                Vehiculos.placa.ilike(patron),
                Vehiculos.marca.ilike(patron),
                Vehiculos.modelo.ilike(patron),
            )
        )

    # Filtro por tipo de vehículo
    if tipo_filtro:
        consulta = consulta.filter(Vehiculos.tipo_id == tipo_filtro)

    # Filtro por estado
    if estado_filtro:
        consulta = consulta.filter(Vehiculos.estado_id == estado_filtro)

    lista_vehiculos = consulta.all()

    tipos = CatTipoVehiculo.query.order_by(CatTipoVehiculo.nombre).all()
    estados = CatEstadoVehiculo.query.order_by(CatEstadoVehiculo.nombre).all()

    return render_template(
        'Modules/Gestion_Vehiculos/VistaGestionVehiculos.html',
        title='Gestión de Vehículos',
        vehiculos=lista_vehiculos,
        tipos=tipos,
        estados=estados,
        q=q,
        tipo_sel=tipo_filtro,
        estado_sel=estado_filtro,
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


    """Vista del módulo de gestión de vehículos"""
    return render_template('Modules/Gestion_Vehiculos/VistaGestionVehiculos.html', title='Gestión de Vehículos')

@bp.route('/busqueda')
def busqueda():
    """Vista busqueda"""
    return render_template('layouts/busqueda.html', title='Busqueda')


# ============================================================
# Clientes
# ============================================================
@bp.route('/clientes', methods=['GET', 'POST'])
def clientes():
    # ---------- POST → Registrar nuevo cliente ----------
    if request.method == 'POST':
        nombre = request.form.get('nombre_cliente')
        dui = request.form.get('dui_cliente')
        correo = request.form.get('correo_electronico')

        # Validación mínima
        if not nombre or not dui or not correo:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('main.clientes'))

        nuevo_cliente = Clientes(
            Nombre_Cliente=nombre,
            Dui=dui,
            CorreoElectronico=correo
        )

        try:
            db.session.add(nuevo_cliente)
            db.session.commit()
            flash("Cliente registrado correctamente.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar el cliente: {e}", "danger")

        return redirect(url_for('main.clientes'))

    # ---------- GET → Mostrar clientes existentes ----------
    lista_clientes = Clientes.query.order_by(Clientes.Nombre_Cliente).all()

    return render_template(
        "layouts/Clientes.html",
        title="Gestión de Clientes",
        clientes=lista_clientes
    )


@bp.route('/editarservicio')
def editarservicio():
    """
    Editar los servicios
    """
    return render_template('Modules/Gestion_Servicio/Editar_Servicio.html', title='Editar ServisioS')

@bp.route('/Reportes')
def reportes():
    """Vista del módulo de reportes"""
    return render_template('layouts/Reportes.html', title='Reportes')


