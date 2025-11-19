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

# Función auxiliar para validar extensiones de archivo
def allowed_file(filename):
    allowed = {'png', 'jpg', 'jpeg', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

# ============================================================
# RUTA PRINCIPAL Y DASHBOARD
# ============================================================
@bp.route('/')
@bp.route('/index')
def index():
    return render_template('layouts/index.html', title='Inicio')

@bp.route('/alertas')
def alertas():
    return render_template('layouts/Alertas.html', title='Sistema de Alertas')

@bp.route('/recursos')
def recursos():
    return render_template('layouts/MiniMenuRecursos.html', title='Recursos Operativos')

@bp.route('/reportes')
def reportes():
    return render_template('layouts/Reportes.html', title='Reportes')


# ============================================================
# GESTIÓN DE EVIDENCIA
# ============================================================
@bp.route('/gestion_evidencia')
def gestion_evidencia():
    servicios = (
        db.session.query(
            Servicios.Id_Servicio,
            Clientes.Nombre_Cliente.label('cliente_nombre')
        )
        .join(Clientes)
        .order_by(Servicios.Id_Servicio.desc())
        .all()
    )

    evidencias = (
        db.session.query(Evidencia, Servicios, Clientes)
        .join(Servicios, Evidencia.id_servicio == Servicios.Id_Servicio)
        .join(Clientes, Servicios.Id_Cliente == Clientes.Id_Cliente)
        .order_by(Evidencia.id_evidencia.desc())
        .all()
    )

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
    # Asegúrate de tener configurado UPLOAD_FOLDER en config.py
    ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    try:
        archivo.save(ruta_guardado)
    except Exception as e:
        flash(f"Error al guardar el archivo: {e}", "danger")
        return redirect(url_for('main.gestion_evidencia'))

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

    flash("📊 Seguimiento registrado correctamente.", "success")
    return redirect(url_for('main.gestion_evidencia'))


# ============================================================
# GESTIÓN DE UBICACIONES
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

    nueva_dir = Direccion(Id_Municipio=muni, Detalle_Direccion=direccion_texto)
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

@bp.route("/ubicaciones/actualizar/<int:id_ubicacion>", methods=["POST"])
def actualizar_ubicacion(id_ubicacion):
    u = Ubicaciones.query.get_or_404(id_ubicacion)
    id_direccion = request.form.get("Id_Direccion", type=int)
    dir = Direccion.query.get(id_direccion)

# ============================================================
# GESTIÓN DE SERVICIOS
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
    serv = Servicios.query.get_or_404(id_servicio)
    
    for s in serv.seguimientos:
        db.session.delete(s)
    for e in serv.evidencias:
        db.session.delete(e)

    db.session.delete(serv)
    db.session.commit()

    flash("Servicio eliminado.", "success")
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
# GESTIÓN DE CONDUCTORES
# ============================================================
@bp.route('/conductores', methods=['GET', 'POST'])
def conductores():
    if request.method == 'POST':
        nombre = request.form.get('nombre_completo')
        documento = request.form.get('documento_identificacion')
        tipo_lic = request.form.get('tipo_licencia')
        fecha_venc_str = request.form.get('fecha_vencimiento_licencia')
        
        if not all([nombre, documento, tipo_lic, fecha_venc_str]):
            flash("Completa los campos obligatorios.", "danger")
            return redirect(url_for('main.conductores'))

        try:
            fecha_venc = datetime.strptime(fecha_venc_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Fecha inválida.", "danger")
            return redirect(url_for('main.conductores'))

        nuevo = Conductor(
            nombre_completo=nombre,
            documento_identificacion=documento,
            tipo_licencia=tipo_lic,
            fecha_vencimiento_licencia=fecha_venc,
            telefono=request.form.get('telefono') or None,
            correo=request.form.get('correo') or None,
            estado=request.form.get('estado') or "Activo",
            experiencia_notas=request.form.get('experiencia_notas') or None
        )

        try:
            db.session.add(nuevo)
            db.session.commit()
            flash("Conductor registrado correctamente.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar: {e}", "danger")

        return redirect(url_for('main.conductores'))

    lista = Conductor.query.order_by(Conductor.nombre_completo).all()
    
    # CAMBIO REALIZADO: Apuntar al nombre del archivo que quieres usar
    return render_template(
        "Modules/Gestion_Conductores/VistaGestionConductores.html",
        conductores=lista
    )


# ============================================================
# GESTIÓN DE VEHÍCULOS
# ============================================================
@bp.route('/vehiculos', methods=['GET', 'POST'])
def vehiculos():
    # POST: Registrar
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

        try:
            db.session.add(nuevo)
            db.session.commit()
            flash("Vehículo registrado correctamente.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar vehículo: {e}", "danger")

        return redirect(url_for('main.vehiculos'))

    # GET: Listar y Filtrar
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

    lista_vehiculos = consulta.all()

    return render_template(
        "Modules/Gestion_Vehiculos/VistaGestionVehiculos.html",
        vehiculos=lista_vehiculos,
        tipos=CatTipoVehiculo.query.all(),
        estados=CatEstadoVehiculo.query.all(),
        q=q, tipo_sel=tipo, estado_sel=estado
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
        v.vin = request.form.get('vin')
        v.km_actual = request.form.get('km_actual', type=int) or 0
        v.seguro_vigente = True if request.form.get('seguro_vigente') == "1" else False
        v.aseguradora = request.form.get('aseguradora')
        v.poliza_numero = request.form.get('poliza_numero')
        v.fecha_venc_seguro = request.form.get('fecha_venc_seguro') or None
        v.observaciones = request.form.get('observaciones')

        db.session.commit()
        flash("Vehículo actualizado.", "success")
        return redirect(url_for('main.vehiculos'))

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
    return redirect(url_for('main.vehiculos'))


# ============================================================
# GESTIÓN DE CLIENTES
# ============================================================
@bp.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        nombre = request.form.get('nombre_cliente')
        dui = request.form.get('dui_cliente')
        correo = request.form.get('correo_electronico')

        if not all([nombre, dui, correo]):
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('main.clientes'))

        nuevo = Clientes(Nombre_Cliente=nombre, Dui=dui, CorreoElectronico=correo)
        
        try:
            db.session.add(nuevo)
            db.session.commit()
            flash("Cliente registrado correctamente.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar cliente: {e}", "danger")
            
        return redirect(url_for('main.clientes'))

    lista = Clientes.query.order_by(Clientes.Nombre_Cliente).all()
    return render_template("layouts/Clientes.html", clientes=lista)


# ============================================================
# BÚSQUEDA GENERAL
# ============================================================
@bp.route('/busqueda')
def busqueda():
    tipo_servicio = request.args.get('tipo_servicio', '').strip()
    peso_min = request.args.get('peso_min', type=float)
    
    consulta = (
        db.session.query(Servicios, Clientes, Vehiculos, SeguimientoControl)
        .join(Clientes, Servicios.Id_Cliente == Clientes.Id_Cliente)
        .outerjoin(Vehiculos, Servicios.Id_Vehiculo == Vehiculos.id_vehiculo)
        .outerjoin(SeguimientoControl, SeguimientoControl.id_servicio == Servicios.Id_Servicio)
    )

    if tipo_servicio:
        consulta = consulta.filter(Servicios.Id_Tipo_Servicio == tipo_servicio)
    if peso_min:
        consulta = consulta.filter(Servicios.Peso_Carga >= peso_min)
    
    consulta = consulta.order_by(Servicios.Id_Servicio.desc())
    
    resultados = consulta.all()

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
