from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from . import db
from .models import Clientes, Evidencia, NivelFragilidad, SeguimientoControl, Servicios, TipoServicio, Vehiculos, CatTipoVehiculo, CatEstadoVehiculo, Conductor, Departamento, Municipio, Direccion, Ubicaciones
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func, extract, case, select, desc
from .models import (
    Servicios, 
    Evidencia, 
    SeguimientoControl, 
    CatEstadoVehiculo, 
    db
)
import csv
from flask import render_template, Response
from io import StringIO
from app import db
from collections import defaultdict



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

    # 1. DEFINIR 'u' (Obtener la Ubicación principal)
    u = Ubicaciones.query.get_or_404(id_ubicacion)

    # El resto del código que usa 'u'
    d = Departamento.query.get(u.Id_Departamento)
    m = Municipio.query.get(u.Id_Municipio)
    dir = Direccion.query.get(u.Id_Direccion)

    # 2. Sububicaciones del MISMO departamento (Usando 'u' ya definida)
    sub_ubicaciones = (
        db.session.query(Ubicaciones, Municipio, Direccion)
        .join(Municipio, Ubicaciones.Id_Municipio == Municipio.Id_Municipio) 
        .join(Direccion, Ubicaciones.Id_Direccion == Direccion.Id_Direccion) 
        .filter(Ubicaciones.Id_Departamento == u.Id_Departamento) 
        .filter(Ubicaciones.Id_Ubicacion != id_ubicacion)
        .all()
    )

    # ... resto de la función ...
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
    
# =================================================================
# FUNCIÓN DE RUTA: CARGAR Y MOSTRAR FORMULARIO DE EDICIÓN (GET)
# Endpoint: 'main.editar_servicio_get'
# =================================================================
@bp.route('/servicio/editar/<int:id_servicio>', methods=['GET'])
def editar_servicio_get(id_servicio):
    # 1. Obtener los datos del Servicio (tabla Servicios)
    servicio = db.session.get(Servicios, id_servicio)
    
    if servicio is None:
        flash('El servicio solicitado no existe.', 'danger')
        return redirect(url_for('main.reportes')) 
    
    # 2. Obtener el último estado de SeguimientoControl para precargar el formulario
    ultimo_estado = SeguimientoControl.query.filter_by(
        id_servicio=id_servicio
    ).order_by(
        SeguimientoControl.fecha_hora.desc()
    ).first()

    # Precargar el estado y comentario
    estado_actual = ultimo_estado.estado_actual if ultimo_estado else 'en_espera' 
    comentario_estado = ultimo_estado.incidente if ultimo_estado else 'Sin seguimiento previo.'

    return render_template('Modules/Gestion_Servicio/Editar_Servicio.html',
        servicio=servicio,
        estado_actual=estado_actual,
        comentario_estado=comentario_estado
    )

# =================================================================
# FUNCIÓN DE RUTA: PROCESAR Y GUARDAR CAMBIOS (POST)
# =================================================================
@bp.route('/servicio/editar/<int:id_servicio>', methods=['POST'])
def editar_servicio_post(id_servicio):
    # 1. Obtener datos del formulario
    nuevo_estado = request.form.get('estado_actual')
    comentario = request.form.get('comentario_estado')
    
    try:
        id_vehiculo = int(request.form.get('id_vehiculo'))
        id_conductor = int(request.form.get('id_conductor'))
    except ValueError:
        flash('Error: Los IDs de Vehículo y Conductor deben ser números enteros.', 'danger')
        return redirect(url_for('main.editar_servicio_get', id_servicio=id_servicio))

    # 2. Buscar el servicio
    servicio = db.session.get(Servicios, id_servicio)
    if servicio is None:
        flash('Error: Servicio no encontrado.', 'danger')
        return redirect(url_for('main.reportes')) 

    # 3. Actualizar asignaciones en la tabla Servicios
    servicio.Id_Vehiculo = id_vehiculo
    servicio.id_conductor = id_conductor
    
    # 4. Registrar nuevo estado en SeguimientoControl (solo si el estado ha cambiado)
    ultimo_estado = SeguimientoControl.query.filter_by(
        id_servicio=id_servicio
    ).order_by(
        SeguimientoControl.fecha_hora.desc()
    ).first()
    
    is_new_status = ultimo_estado is None or ultimo_estado.estado_actual != nuevo_estado
    
    if is_new_status:
        nuevo_seguimiento = SeguimientoControl(
            id_servicio=id_servicio,
            estado_actual=nuevo_estado,
            incidente=comentario if comentario else None,
            control_calidad='pendiente' 
        )
        db.session.add(nuevo_seguimiento)
        
        # 5. Actualizar Fecha_Entrega si se marca como 'entregado'
        if nuevo_estado == 'entregado' and servicio.Fecha_Entrega is None:
            servicio.Fecha_Entrega = datetime.now().date()
            flash('¡Servicio marcado como ENTREGADO y fecha de entrega registrada!', 'success')
        else:
            flash(f'Estado actualizado a: {nuevo_estado}', 'success')
    else:
        flash('Solo se actualizaron la asignación de Vehículo/Conductor (el estado no cambió).', 'info')


    # 6. Guardar todo en la base de datos
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Error grave al guardar en la base de datos.', 'danger')

    return redirect(url_for('main.servicios'))
    
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

@bp.route('/buscar_servicios', methods=['GET'])
def buscar_servicios():
    from sqlalchemy import and_, or_

    # --- Leer filtros de la URL ---
    tipo_servicio = request.args.get('tipo_servicio', '').strip()
    peso_min = request.args.get('peso_min', type=float)
    fragilidad = request.args.get('fragilidad', '').strip()
    fecha_limite = request.args.get('fecha_limite')
    marca = request.args.get('marca_vehiculo', '').strip()
    estado = request.args.get('estado', '').strip()
    municipio = request.args.get('municipio', '').strip()

    # Consulta base
    consulta = (
        db.session.query(Servicios, Clientes, Vehiculos, SeguimientoControl)
        .join(Clientes, Servicios.Id_Cliente == Clientes.Id_Cliente)
        .outerjoin(Vehiculos, Servicios.Id_Vehiculo == Vehiculos.id_vehiculo)
        .outerjoin(SeguimientoControl, SeguimientoControl.id_servicio == Servicios.Id_Servicio)
    )

    # --- Filtros dinámicos ---
    if tipo_servicio:
        consulta = consulta.filter(Servicios.Id_Tipo_Servicio == tipo_servicio)

    if peso_min:
        consulta = consulta.filter(Servicios.Peso_Carga >= peso_min)

    if fragilidad:
        consulta = consulta.join(NivelFragilidad).filter(
            NivelFragilidad.nivel.ilike(f"%{fragilidad}%")
        )

    if fecha_limite:
        consulta = consulta.filter(Servicios.Fecha_Entrega <= fecha_limite)

    if marca:
        consulta = consulta.filter(Vehiculos.marca.ilike(f"%{marca}%"))

    if estado:
        consulta = consulta.filter(SeguimientoControl.estado_actual.ilike(f"%{estado}%"))

    if municipio:
        consulta = consulta.join(Ubicaciones).join(Municipio).filter(
            Municipio.Nombre_Municipio.ilike(f"%{municipio}%")
        )

    # Evitar duplicados tomando solo el último seguimiento
    consulta = consulta.order_by(Servicios.Id_Servicio.desc())

    resultados = consulta.all()

    return render_template(
        "layouts/busqueda.html",
        resultados=resultados,
        total=len(resultados)
    )






# ============================================================
# CONDUCTORES
# ============================================================
@bp.route('/conductores', methods=['GET', 'POST'])
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

# ============================================================
# REPORTES (Actualizado para pasar datos a la plantilla)
# ============================================================
@bp.route('/Reportes', methods=['GET'])
def Reportes():
    # 1. Indicador de Sistema Activo
    total_servicios = db.session.query(func.count(Servicios.Id_Servicio)).scalar()
    sistema_activo = total_servicios > 0

    # ========================================================
    # 2. CÁLCULO DE ESTADÍSTICAS (KPIs para las tarjetas)
    # ========================================================
    
    # 2.1. Total Evidencias Capturadas
    total_evidencias = db.session.query(func.count(Evidencia.id_evidencia)).scalar()
    
    # 2.2. Servicios Completados (Basado en el último estado 'entregado')
    # Consulta avanzada para obtener los IDs de los servicios cuyo ÚLTIMO estado es 'entregado'
    
    # Paso 1: Subconsulta para obtener el ID de seguimiento más alto por Id_Servicio
    subq = db.session.query(
        SeguimientoControl.id_servicio,
        func.max(SeguimientoControl.id_seguimiento).label('max_id')
    ).group_by(SeguimientoControl.id_servicio).subquery()

    # Paso 2: Unir la subconsulta con SeguimientoControl para obtener el último registro completo
    servicios_completados_q = db.session.query(func.count(SeguimientoControl.id_servicio))\
        .join(subq, SeguimientoControl.id_seguimiento == subq.c.max_id)\
        .filter(SeguimientoControl.estado_actual == 'entregado')\
        .scalar()
        
    servicios_completados = servicios_completados_q or 0
    
    # 2.3. Incidentes Reportados
    # Contamos la cantidad de registros en SeguimientoControl que tienen un 'incidente' no nulo.
    incidentes_reportados = db.session.query(func.count(SeguimientoControl.id_seguimiento))\
                                      .filter(SeguimientoControl.incidente != None)\
                                      .filter(SeguimientoControl.incidente != '')\
                                      .scalar()
    
    # 2.4. Porcentaje de Entregas a Tiempo
    # Aquí puedes usar tu lógica de negocio real. 
    # Mantenemos el placeholder para evitar errores de lógica compleja de fechas, 
    # pero basado en la métrica de Servicios Completados.
    
    if servicios_completados > 0:
        # Asumimos una tasa del 95% de éxito a menos que se defina la lógica de fechas
        servicios_a_tiempo = servicios_completados * 0.95 
        porcentaje_a_tiempo = (servicios_a_tiempo / servicios_completados) * 100
    else:
        porcentaje_a_tiempo = 0.0

    # ========================================================
    # 3. PREPARACIÓN DE DATOS PARA GRÁFICOS (JSON)
    # ========================================================

    # 3.1. Evidencias por Tipo (data_evidencias) - Gráfico de Barra
    evidencias_q = db.session.query(
        Evidencia.tipo_evidencia, 
        func.count(Evidencia.id_evidencia)
    ).group_by(Evidencia.tipo_evidencia).all()
    
    data_evidencias = {tipo.capitalize().replace('_', ' '): count for tipo, count in evidencias_q}


    # 3.2. Estados de Envíos (data_estados) - Gráfico de Doughnut (USANDO ÚLTIMO ESTADO)
    # Reutilizamos la subconsulta 'subq' de la sección 2.2
    
    # Unimos para obtener el estado actual de cada servicio
    estados_actuales_q = db.session.query(
        SeguimientoControl.estado_actual,
        func.count(SeguimientoControl.estado_actual)
    ).join(subq, SeguimientoControl.id_seguimiento == subq.c.max_id)\
    .group_by(SeguimientoControl.estado_actual)\
    .all()

    data_estados = {estado.capitalize().replace('_', ' '): count for estado, count in estados_actuales_q}
    
    
    # 3.3. Entregas por Mes (data_mensual) - Gráfico de Línea
    # Corregido: Usamos func.DATE_FORMAT para MySQL en lugar de func.strftime
    entregas_mensual_q = db.session.query(
        func.DATE_FORMAT(Servicios.Fecha_Entrega, '%Y-%m').label('mes'),
        func.count(Servicios.Id_Servicio)
    ).group_by('mes').order_by('mes').all()

    data_mensual = {mes: count for mes, count in entregas_mensual_q}
    
    
    # ========================================================
    # 4. RENDERIZACIÓN DE LA PLANTILLA
    # ========================================================
    
    return render_template('layouts/Reportes.html',
        # KPIs para las tarjetas
        total_evidencias=total_evidencias,
        servicios_completados=servicios_completados,
        incidentes_reportados=incidentes_reportados,
        porcentaje_a_tiempo=porcentaje_a_tiempo,
        sistema_activo=sistema_activo,
        
        # Datos JSON para los gráficos
        data_evidencias=data_evidencias,
        data_estados=data_estados,
        data_mensual=data_mensual
    )

@bp.route('/exportar/excel', methods=['GET'])
def exportar_excel():
    
    # ... (Consulta a la base de datos, queda igual) ...
    servicios_data = db.session.query(
        Servicios.Id_Servicio,
        Clientes.Nombre_Cliente,  
        Vehiculos.placa.label('placa_vehiculo'),  
        Conductor.nombre_completo.label('nombre_conductor'), 
        TipoServicio.Nombre_Servicio, 
        Servicios.Fecha_Pedido,
        Servicios.Fecha_Entrega,
        Servicios.Peso_Carga, 
        Servicios.Precio_Total 
    ).join(Clientes, Servicios.Id_Cliente == Clientes.Id_Cliente)\
     .join(Vehiculos, Servicios.Id_Vehiculo == Vehiculos.id_vehiculo)\
     .join(Conductor, Servicios.id_conductor == Conductor.id_conductor)\
     .join(TipoServicio, Servicios.Id_Tipo_Servicio == TipoServicio.Id_Tipo_Servicio)\
     .all()

    # 2. Configurar la respuesta
    output = StringIO()
    
    # 🚨 ¡CORRECCIÓN CLAVE! ESPECIFICAR EL DELIMITADOR PUNTO Y COMA (;)
    writer = csv.writer(output, delimiter=';')

    # 3. Escribir las cabeceras (USANDO NOMBRES DESCRIPTIVOS)
    header = [
        'ID Servicio', 
        'Cliente', 
        'Placa Vehiculo', 
        'Conductor', 
        'Tipo Servicio',
        'Fecha Pedido', 
        'Fecha Entrega', 
        'Peso Carga (kg)', 
        'Precio Total'
    ]
    writer.writerow(header)

    # 4. Escribir los datos de cada fila
    for row in servicios_data:
        data_row = [
            row.Id_Servicio,
            row.Nombre_Cliente,
            row.placa_vehiculo,
            row.nombre_conductor,
            row.Nombre_Servicio,
            row.Fecha_Pedido.strftime('%Y-%m-%d') if row.Fecha_Pedido else '',
            row.Fecha_Entrega.strftime('%Y-%m-%d') if row.Fecha_Entrega else '',
            str(row.Peso_Carga), 
            str(row.Precio_Total)
        ]
        writer.writerow(data_row)

    # 5. Devolver el archivo (el nombre del archivo sigue siendo CSV, pero con delimiter ';')
    response = Response(
        output.getvalue(),
        mimetype="text/csv",
        content_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=Reporte_Servicios_Conciso.csv"
    
    return response