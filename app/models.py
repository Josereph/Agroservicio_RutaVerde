# app/models.py
from datetime import datetime
from . import db
from sqlalchemy import CheckConstraint, Index

# ============================================================
# MÓDULO: UBICACIONES GEOGRÁFICAS
# ============================================================

class Departamento(db.Model):
    __tablename__ = 'Departamento'

    Id_Departamento = db.Column(db.Integer, primary_key=True)
    Nombre_Departamento = db.Column(db.String(100), nullable=False)

    municipios = db.relationship('Municipio', backref='departamento', lazy=True)
    ubicaciones = db.relationship('Ubicaciones', backref='departamento', lazy=True)

    def __repr__(self):
        return f'<Departamento {self.Nombre_Departamento}>'


class Municipio(db.Model):
    __tablename__ = 'Municipio'

    Id_Municipio = db.Column(db.Integer, primary_key=True)
    Id_Departamento = db.Column(
        db.Integer,
        db.ForeignKey('Departamento.Id_Departamento'),
        nullable=False
    )
    Nombre_Municipio = db.Column(db.String(100), nullable=False)

    direcciones = db.relationship('Direccion', backref='municipio', lazy=True)
    ubicaciones = db.relationship('Ubicaciones', backref='municipio', lazy=True)

    def __repr__(self):
        return f'<Municipio {self.Nombre_Municipio}>'


class Direccion(db.Model):
    __tablename__ = 'Direccion'

    Id_Direccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_Municipio = db.Column(
        db.Integer,
        db.ForeignKey('Municipio.Id_Municipio'),
        nullable=False
    )
    Detalle_Direccion = db.Column(db.Text, nullable=True)

    ubicaciones = db.relationship('Ubicaciones', backref='direccion', lazy=True)

    def __repr__(self):
        return f'<Direccion {self.Id_Direccion}>'


class Ubicaciones(db.Model):
    __tablename__ = 'Ubicaciones'

    Id_Ubicacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_Departamento = db.Column(
        db.Integer,
        db.ForeignKey('Departamento.Id_Departamento'),
        nullable=False
    )
    Id_Municipio = db.Column(
        db.Integer,
        db.ForeignKey('Municipio.Id_Municipio'),
        nullable=False
    )
    Id_Direccion = db.Column(
        db.Integer,
        db.ForeignKey('Direccion.Id_Direccion'),
        nullable=False
    )

    def __repr__(self):
        return f'<Ubicacion {self.Id_Ubicacion}>'


# ============================================================
# MÓDULO: VEHÍCULOS DE CARGA
# ============================================================

class CatTipoVehiculo(db.Model):
    __tablename__ = 'Cat_Tipo_Vehiculo'

    tipo_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False, unique=True)
    descripcion = db.Column(db.String(120), nullable=True)

    vehiculos = db.relationship('Vehiculos', back_populates='tipo', lazy='dynamic')

    def __repr__(self):
        return f'<TipoVehiculo {self.nombre}>'


class CatEstadoVehiculo(db.Model):
    __tablename__ = 'Cat_Estado_Vehiculo'

    estado_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False, unique=True)
    es_operativo = db.Column(db.Boolean, nullable=False, default=True)

    vehiculos = db.relationship('Vehiculos', back_populates='estado', lazy='dynamic')

    def __repr__(self):
        return f'<EstadoVehiculo {self.nombre}>'


class Vehiculos(db.Model):
    __tablename__ = 'Vehiculos'

    __table_args__ = (
        CheckConstraint('capacidad_kg > 0', name='chk_capacidad_pos'),
        CheckConstraint('km_actual >= 0', name='chk_km_no_neg'),
        Index('ix_vehiculo_estado', 'estado_id'),
        Index('ix_vehiculo_tipo', 'tipo_id'),
        Index('ix_vehiculo_capacidad', 'capacidad_kg'),
    )

    id_vehiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unidad_numero = db.Column(db.String(10), nullable=False, unique=True)
    placa = db.Column(db.String(10), nullable=False, unique=True)
    vin = db.Column(db.String(17), nullable=True, unique=True)

    tipo_id = db.Column(
        db.SmallInteger,
        db.ForeignKey('Cat_Tipo_Vehiculo.tipo_id'),
        nullable=False
    )
    marca = db.Column(db.String(40), nullable=True)
    modelo = db.Column(db.String(40), nullable=True)
    anio = db.Column(db.SmallInteger, nullable=True)

    capacidad_kg = db.Column(db.Numeric(10, 2), nullable=False)
    estado_id = db.Column(
        db.SmallInteger,
        db.ForeignKey('Cat_Estado_Vehiculo.estado_id'),
        nullable=False
    )
    km_actual = db.Column(db.Integer, nullable=False, default=0)

    seguro_vigente = db.Column(db.Boolean, nullable=False, default=False)
    aseguradora = db.Column(db.String(60), nullable=True)
    poliza_numero = db.Column(db.String(40), nullable=True)
    fecha_venc_seguro = db.Column(db.Date, nullable=True)

    observaciones = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    tipo = db.relationship('CatTipoVehiculo', back_populates='vehiculos')
    estado = db.relationship('CatEstadoVehiculo', back_populates='vehiculos')
    servicios = db.relationship('Servicios', back_populates='vehiculo', lazy='dynamic')

    def __repr__(self):
        return f'<Vehiculo {self.unidad_numero} - {self.placa}>'


# ============================================================
# MÓDULO: CONDUCTORES
# ============================================================

class Conductor(db.Model):
    __tablename__ = 'conductor'

    id_conductor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    documento_identificacion = db.Column(db.String(20), nullable=False, unique=True)

    tipo_licencia = db.Column(
        db.Enum('Liviana', 'Pesada', 'Pesada T', name='tipo_licencia_enum'),
        nullable=False
    )

    fecha_vencimiento_licencia = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(15), nullable=True)
    correo = db.Column(db.String(100), nullable=True)

    estado = db.Column(
        db.Enum('Activo', 'De Vacaciones', 'Suspendido', name='estado_conductor_enum'),
        default='Activo'
    )

    experiencia_notas = db.Column(db.String(255), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    servicios = db.relationship('Servicios', back_populates='conductor', lazy='dynamic')

    def __repr__(self):
        return f'<Conductor {self.nombre_completo}>'


# ============================================================
# MÓDULO: CLIENTES
# ============================================================

class Clientes(db.Model):
    __tablename__ = 'Clientes'

    Id_Cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre_Cliente = db.Column(db.String(100), nullable=False)
    Dui = db.Column(db.String(20), nullable=False, unique=True)
    CorreoElectronico = db.Column(db.String(200), nullable=False)

    servicios = db.relationship('Servicios', back_populates='cliente', lazy='dynamic')

    def __repr__(self):
        return f'<Cliente {self.Nombre_Cliente}>'


# ============================================================
# MÓDULO: CATÁLOGOS DE SERVICIOS
# ============================================================

class TipoServicio(db.Model):
    __tablename__ = 'Tipo_Servicio'

    Id_Tipo_Servicio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre_Servicio = db.Column(db.String(20), nullable=False, unique=True)

    servicios = db.relationship('Servicios', back_populates='tipo_servicio', lazy='dynamic')

    def __repr__(self):
        return f'<TipoServicio {self.Nombre_Servicio}>'


class NivelFragilidad(db.Model):
    __tablename__ = 'Nivel_Fragilidad'

    Id_Fragilidad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nivel = db.Column(db.String(30), nullable=False, unique=True)
    Detalle_Impacto = db.Column(db.Text, nullable=True)

    servicios = db.relationship('Servicios', back_populates='fragilidad', lazy='dynamic')

    def __repr__(self):
        return f'<NivelFragilidad {self.Nivel}>'


# ============================================================
# MÓDULO: SERVICIOS (TABLA CENTRAL)
# ============================================================

class Servicios(db.Model):
    __tablename__ = 'Servicios'

    __table_args__ = (
        CheckConstraint('Peso_Carga > 0', name='chk_peso_pos'),
        CheckConstraint('Precio_Total >= 0', name='chk_precio_pos'),
        Index('ix_servicios_cliente', 'Id_Cliente'),
        Index('ix_servicios_fecha', 'Fecha_Pedido', 'Fecha_Entrega'),
        Index('ix_servicios_conductor', 'id_conductor'),
    )

    Id_Servicio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_Cliente = db.Column(db.Integer, db.ForeignKey('Clientes.Id_Cliente'), nullable=False)
    Id_Vehiculo = db.Column(db.Integer, db.ForeignKey('Vehiculos.id_vehiculo'), nullable=False)
    id_conductor = db.Column(db.Integer, db.ForeignKey('conductor.id_conductor'), nullable=False)
    Id_Tipo_Servicio = db.Column(db.Integer, db.ForeignKey('Tipo_Servicio.Id_Tipo_Servicio'), nullable=False)
    Id_Fragilidad = db.Column(db.Integer, db.ForeignKey('Nivel_Fragilidad.Id_Fragilidad'), nullable=False)
    Id_Ubicacion = db.Column(db.Integer, db.ForeignKey('Ubicaciones.Id_Ubicacion'), nullable=False)

    Peso_Carga = db.Column(db.Numeric(10, 2), nullable=False)
    Fecha_Pedido = db.Column(db.Date, nullable=False)
    Fecha_Entrega = db.Column(db.Date, nullable=False)
    Precio_Total = db.Column(db.Numeric(10, 2), nullable=False)

    cliente = db.relationship('Clientes', back_populates='servicios')
    vehiculo = db.relationship('Vehiculos', back_populates='servicios')
    conductor = db.relationship('Conductor', back_populates='servicios')
    tipo_servicio = db.relationship('TipoServicio', back_populates='servicios')
    fragilidad = db.relationship('NivelFragilidad', back_populates='servicios')

    evidencias = db.relationship(
        'Evidencia',
        back_populates='servicio',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    seguimientos = db.relationship(
        'SeguimientoControl',
        back_populates='servicio',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Servicio {self.Id_Servicio}>'


# ============================================================
# MÓDULO: CONTROL DE EVIDENCIAS Y SEGUIMIENTO
# ============================================================

class Evidencia(db.Model):
    __tablename__ = 'EVIDENCIA'

    __table_args__ = (
        Index('ix_evidencia_servicio', 'id_servicio'),
        Index('ix_evidencia_tipo', 'tipo_evidencia'),
    )

    id_evidencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_servicio = db.Column(
        db.Integer,
        db.ForeignKey('Servicios.Id_Servicio'),
        nullable=False
    )
    tipo_evidencia = db.Column(
        db.Enum('foto_salida', 'foto_entrega', 'documento_firmado', name='tipo_evidencia_enum'),
        nullable=False
    )
    nombre_archivo = db.Column(db.String(255), nullable=False)
    es_legible = db.Column(db.Boolean, default=True)
    fecha_captura = db.Column(db.DateTime, default=datetime.utcnow)

    servicio = db.relationship('Servicios', back_populates='evidencias')

    def __repr__(self):
        return f'<Evidencia {self.tipo_evidencia} - Servicio {self.id_servicio}>'


class SeguimientoControl(db.Model):
    __tablename__ = 'SEGUIMIENTO_CONTROL'

    __table_args__ = (
        Index('ix_seguimiento_servicio', 'id_servicio'),
        Index('ix_seguimiento_estado', 'estado_actual'),
        Index('ix_seguimiento_fecha', 'fecha_hora'),
    )

    id_seguimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_servicio = db.Column(db.Integer, db.ForeignKey('Servicios.Id_Servicio'), nullable=False)

    estado_actual = db.Column(
        db.Enum('cargando', 'en_ruta', 'en_espera', 'entregado', name='estado_envio_enum'),
        nullable=False
    )

    control_calidad = db.Column(
        db.Enum('aprobado', 'rechazado', 'pendiente', name='control_calidad_enum'),
        default='pendiente'
    )

    incidente = db.Column(db.String(200), nullable=True)
    notificacion_enviada = db.Column(db.Boolean, default=False)
    nombre_receptor = db.Column(db.String(100), nullable=True)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)

    servicio = db.relationship('Servicios', back_populates='seguimientos')

    def __repr__(self):
        return f'<Seguimiento {self.estado_actual} - Servicio {self.id_servicio}>'
