<<<<<<< HEAD
# app/models.py
from datetime import datetime
from . import db  # usa el db que inicializas en __init__.py

from sqlalchemy import CheckConstraint, Index, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import (
    INTEGER, TINYINT, SMALLINT, VARCHAR, TEXT, DECIMAL, BOOLEAN, ENUM, DATETIME, DATE
)
=======
from . import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import CheckConstraint, Index

db = SQLAlchemy()
>>>>>>> Gestion_Evidencia_Documentacion


# ============================================
# MÓDULO: UBICACIONES GEOGRÁFICAS
# ============================================

class Departamento(db.Model):
<<<<<<< HEAD
    __tablename__ = 'Departamento'

    Id_Departamento = db.Column(INTEGER(unsigned=False), primary_key=True)
    Nombre_Departamento = db.Column(VARCHAR(100), nullable=False)

    municipios = relationship("Municipio", back_populates="departamento", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Departamento {self.Id_Departamento} - {self.Nombre_Departamento}>"


class Municipio(db.Model):
    __tablename__ = 'Municipio'

    Id_Municipio = db.Column(INTEGER(unsigned=False), primary_key=True)
    Id_Departamento = db.Column(INTEGER(unsigned=False), ForeignKey('Departamento.Id_Departamento'), nullable=False)
    Nombre_Municipio = db.Column(VARCHAR(100), nullable=False)

    departamento = relationship("Departamento", back_populates="municipios")
    direcciones = relationship("Direccion", back_populates="municipio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Municipio {self.Id_Municipio} - {self.Nombre_Municipio}>"


class Direccion(db.Model):
    __tablename__ = 'Direccion'

    Id_Direccion = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    Id_Municipio = db.Column(INTEGER(unsigned=False), ForeignKey('Municipio.Id_Municipio'), nullable=False)
    Detalle_Direccion = db.Column(TEXT, nullable=True)

    municipio = relationship("Municipio", back_populates="direcciones")

    def __repr__(self):
        return f"<Direccion {self.Id_Direccion} - Mun:{self.Id_Municipio}>"


class Ubicaciones(db.Model):
    __tablename__ = 'Ubicaciones'

    Id_Ubicacion = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    Id_Departamento = db.Column(INTEGER(unsigned=False), ForeignKey('Departamento.Id_Departamento'), nullable=False)
    Id_Municipio = db.Column(INTEGER(unsigned=False), ForeignKey('Municipio.Id_Municipio'), nullable=False)
    Id_Direccion = db.Column(INTEGER(unsigned=False), ForeignKey('Direccion.Id_Direccion'), nullable=False)

    departamento = relationship("Departamento")
    municipio = relationship("Municipio")
    direccion = relationship("Direccion")

    def __repr__(self):
        return f"<Ubicacion {self.Id_Ubicacion} D:{self.Id_Departamento} M:{self.Id_Municipio} Dir:{self.Id_Direccion}>"


# ============================================
# MÓDULO: VEHÍCULOS
# ============================================

class CatTipoVehiculo(db.Model):
    __tablename__ = 'Cat_Tipo_Vehiculo'

    tipo_id = db.Column(TINYINT(unsigned=True), primary_key=True, autoincrement=True)
    nombre = db.Column(VARCHAR(30), nullable=False, unique=True)
    descripcion = db.Column(VARCHAR(120), nullable=True)

    vehiculos = relationship("Vehiculos", back_populates="tipo")

    def __repr__(self):
        return f"<CatTipoVehiculo {self.tipo_id} - {self.nombre}>"


class CatEstadoVehiculo(db.Model):
    __tablename__ = 'Cat_Estado_Vehiculo'

    estado_id = db.Column(TINYINT(unsigned=True), primary_key=True, autoincrement=True)
    nombre = db.Column(VARCHAR(30), nullable=False, unique=True)
    es_operativo = db.Column(BOOLEAN, nullable=False, default=True)

    vehiculos = relationship("Vehiculos", back_populates="estado")

    def __repr__(self):
        return f"<CatEstadoVehiculo {self.estado_id} - {self.nombre}>"


class Vehiculos(db.Model):
    __tablename__ = 'Vehiculos'

    id_vehiculo = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    unidad_numero = db.Column(VARCHAR(10), nullable=False, unique=True)
    placa = db.Column(VARCHAR(10), nullable=False, unique=True)
    vin = db.Column(VARCHAR(17), nullable=True, unique=True)

    tipo_id = db.Column(TINYINT(unsigned=True), ForeignKey('Cat_Tipo_Vehiculo.tipo_id'), nullable=False)
    marca = db.Column(VARCHAR(40), nullable=True)
    modelo = db.Column(VARCHAR(40), nullable=True)
    anio = db.Column(SMALLINT, nullable=True)

    capacidad_kg = db.Column(DECIMAL(10, 2), nullable=False)
    estado_id = db.Column(TINYINT(unsigned=True), ForeignKey('Cat_Estado_Vehiculo.estado_id'), nullable=False)
    km_actual = db.Column(INTEGER(unsigned=True), nullable=False, default=0)

    seguro_vigente = db.Column(BOOLEAN, nullable=False, default=False)
    aseguradora = db.Column(VARCHAR(60), nullable=True)
    poliza_numero = db.Column(VARCHAR(40), nullable=True)
    fecha_venc_seguro = db.Column(DATE, nullable=True)

    observaciones = db.Column(TEXT, nullable=True)
    fecha_registro = db.Column(DATETIME, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(DATETIME, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    tipo = relationship("CatTipoVehiculo", back_populates="vehiculos")
    estado = relationship("CatEstadoVehiculo", back_populates="vehiculos")

=======
    """Departamentos de El Salvador"""
    __tablename__ = 'Departamento'
    
    Id_Departamento = db.Column(db.Integer, primary_key=True)
    Nombre_Departamento = db.Column(db.String(100), nullable=False)
    
    # Relaciones
    municipios = db.relationship('Municipio', back_populates='departamento', lazy='dynamic')
    ubicaciones = db.relationship('Ubicaciones', back_populates='departamento', lazy='dynamic')
    
    def __repr__(self):
        return f'<Departamento {self.Nombre_Departamento}>'


class Municipio(db.Model):
    """Municipios de El Salvador"""
    __tablename__ = 'Municipio'
    
    Id_Municipio = db.Column(db.Integer, primary_key=True)
    Id_Departamento = db.Column(db.Integer, db.ForeignKey('Departamento.Id_Departamento'), nullable=False)
    Nombre_Municipio = db.Column(db.String(100), nullable=False)
    
    # Relaciones
    departamento = db.relationship('Departamento', back_populates='municipios')
    direcciones = db.relationship('Direccion', back_populates='municipio', lazy='dynamic')
    ubicaciones = db.relationship('Ubicaciones', back_populates='municipio', lazy='dynamic')
    
    def __repr__(self):
        return f'<Municipio {self.Nombre_Municipio}>'


class Direccion(db.Model):
    """Direcciones específicas"""
    __tablename__ = 'Direccion'
    
    Id_Direccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_Municipio = db.Column(db.Integer, db.ForeignKey('Municipio.Id_Municipio'), nullable=False)
    Detalle_Direccion = db.Column(db.Text, nullable=True)
    
    # Relaciones
    municipio = db.relationship('Municipio', back_populates='direcciones')
    ubicaciones = db.relationship('Ubicaciones', back_populates='direccion', lazy='dynamic')
    
    def __repr__(self):
        return f'<Direccion {self.Id_Direccion}>'


class Ubicaciones(db.Model):
    """Ubicaciones completas para envíos"""
    __tablename__ = 'Ubicaciones'
    
    Id_Ubicacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_Departamento = db.Column(db.Integer, db.ForeignKey('Departamento.Id_Departamento'), nullable=False)
    Id_Municipio = db.Column(db.Integer, db.ForeignKey('Municipio.Id_Municipio'), nullable=False)
    Id_Direccion = db.Column(db.Integer, db.ForeignKey('Direccion.Id_Direccion'), nullable=False)
    
    # Relaciones
    departamento = db.relationship('Departamento', back_populates='ubicaciones')
    municipio = db.relationship('Municipio', back_populates='ubicaciones')
    direccion = db.relationship('Direccion', back_populates='ubicaciones')
    servicios = db.relationship('Servicios', back_populates='ubicacion', lazy='dynamic')
    
    def __repr__(self):
        return f'<Ubicacion {self.Id_Ubicacion}>'


# ============================================
# MÓDULO: VEHÍCULOS DE CARGA
# ============================================

class CatTipoVehiculo(db.Model):
    """Catálogo de tipos de vehículo"""
    __tablename__ = 'Cat_Tipo_Vehiculo'
    
    tipo_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False, unique=True)
    descripcion = db.Column(db.String(120), nullable=True)
    
    # Relaciones
    vehiculos = db.relationship('Vehiculos', back_populates='tipo', lazy='dynamic')
    
    def __repr__(self):
        return f'<TipoVehiculo {self.nombre}>'


class CatEstadoVehiculo(db.Model):
    """Catálogo de estados operativos de los vehículos"""
    __tablename__ = 'Cat_Estado_Vehiculo'
    
    estado_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False, unique=True)
    es_operativo = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relaciones
    vehiculos = db.relationship('Vehiculos', back_populates='estado', lazy='dynamic')
    
    def __repr__(self):
        return f'<EstadoVehiculo {self.nombre}>'


class Vehiculos(db.Model):
    """Registro maestro de vehículos de carga del agroservicio"""
    __tablename__ = 'Vehiculos'
>>>>>>> Gestion_Evidencia_Documentacion
    __table_args__ = (
        CheckConstraint('capacidad_kg > 0', name='chk_capacidad_pos'),
        CheckConstraint('km_actual >= 0', name='chk_km_no_neg'),
        Index('ix_vehiculo_estado', 'estado_id'),
        Index('ix_vehiculo_tipo', 'tipo_id'),
        Index('ix_vehiculo_capacidad', 'capacidad_kg'),
    )
<<<<<<< HEAD

    def __repr__(self):
        return f"<Vehiculo {self.id_vehiculo} {self.placa}>"
=======
    
    id_vehiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unidad_numero = db.Column(db.String(10), nullable=False, unique=True)
    placa = db.Column(db.String(10), nullable=False, unique=True)
    vin = db.Column(db.String(17), nullable=True, unique=True)
    tipo_id = db.Column(db.SmallInteger, db.ForeignKey('Cat_Tipo_Vehiculo.tipo_id'), nullable=False)
    marca = db.Column(db.String(40), nullable=True)
    modelo = db.Column(db.String(40), nullable=True)
    anio = db.Column(db.SmallInteger, nullable=True)
    capacidad_kg = db.Column(db.Numeric(10, 2), nullable=False)
    estado_id = db.Column(db.SmallInteger, db.ForeignKey('Cat_Estado_Vehiculo.estado_id'), nullable=False)
    km_actual = db.Column(db.Integer, nullable=False, default=0)
    seguro_vigente = db.Column(db.Boolean, nullable=False, default=False)
    aseguradora = db.Column(db.String(60), nullable=True)
    poliza_numero = db.Column(db.String(40), nullable=True)
    fecha_venc_seguro = db.Column(db.Date, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    tipo = db.relationship('CatTipoVehiculo', back_populates='vehiculos')
    estado = db.relationship('CatEstadoVehiculo', back_populates='vehiculos')
    servicios = db.relationship('Servicios', back_populates='vehiculo', lazy='dynamic')
    
    def __repr__(self):
        return f'<Vehiculo {self.unidad_numero} - {self.placa}>'
>>>>>>> Gestion_Evidencia_Documentacion


# ============================================
# MÓDULO: CONDUCTORES
# ============================================

class Conductor(db.Model):
<<<<<<< HEAD
    __tablename__ = 'conductor'

    id_conductor = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    nombre_completo = db.Column(VARCHAR(100), nullable=False)
    documento_identificacion = db.Column(VARCHAR(20), nullable=False, unique=True)
    tipo_licencia = db.Column(ENUM('Liviana', 'Pesada', 'Pesada T'), nullable=False)
    fecha_vencimiento_licencia = db.Column(DATE, nullable=False)
    telefono = db.Column(VARCHAR(15), nullable=True)
    correo = db.Column(VARCHAR(100), nullable=True)
    estado = db.Column(ENUM('Activo', 'De Vacaciones', 'Suspendido'), default='Activo')
    experiencia_notas = db.Column(VARCHAR(255), nullable=True)
    fecha_registro = db.Column(DATETIME, default=datetime.utcnow)
    fecha_actualizacion = db.Column(DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)

    servicios = relationship("Servicios", back_populates="conductor")

    def __repr__(self):
        return f"<Conductor {self.id_conductor} - {self.nombre_completo}>"
=======
    """Registro de conductores del agroservicio"""
    __tablename__ = 'conductor'
    
    id_conductor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    documento_identificacion = db.Column(db.String(20), nullable=False, unique=True)
    tipo_licencia = db.Column(db.Enum('Liviana', 'Pesada', 'Pesada T', name='tipo_licencia_enum'), nullable=False)
    fecha_vencimiento_licencia = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(15), nullable=True)
    correo = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.Enum('Activo', 'De Vacaciones', 'Suspendido', name='estado_conductor_enum'), default='Activo')
    experiencia_notas = db.Column(db.String(255), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    servicios = db.relationship('Servicios', back_populates='conductor', lazy='dynamic')
    
    def __repr__(self):
        return f'<Conductor {self.nombre_completo}>'
>>>>>>> Gestion_Evidencia_Documentacion


# ============================================
# MÓDULO: CLIENTES
# ============================================

class Clientes(db.Model):
<<<<<<< HEAD
    __tablename__ = 'Clientes'

    Id_Cliente = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    Nombre_Cliente = db.Column(VARCHAR(100), nullable=False)
    Dui = db.Column(VARCHAR(20), nullable=False, unique=True)
    CorreoElectronico = db.Column(VARCHAR(200), nullable=False)

    servicios = relationship("Servicios", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente {self.Id_Cliente} - {self.Nombre_Cliente}>"
=======
    """Clientes del agroservicio"""
    __tablename__ = 'Clientes'
    
    Id_Cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre_Cliente = db.Column(db.String(100), nullable=False)
    Dui = db.Column(db.String(20), nullable=False, unique=True)
    CorreoElectronico = db.Column(db.String(200), nullable=False)
    
    # Relaciones
    servicios = db.relationship('Servicios', back_populates='cliente', lazy='dynamic')
    
    def __repr__(self):
        return f'<Cliente {self.Nombre_Cliente}>'
>>>>>>> Gestion_Evidencia_Documentacion


# ============================================
# MÓDULO: CATÁLOGOS DE SERVICIOS
# ============================================

class TipoServicio(db.Model):
<<<<<<< HEAD
    __tablename__ = 'Tipo_Servicio'

    Id_Tipo_Servicio = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    Nombre_Servicio = db.Column(VARCHAR(20), nullable=False, unique=True)

    servicios = relationship("Servicios", back_populates="tipo_servicio")

    def __repr__(self):
        return f"<TipoServicio {self.Id_Tipo_Servicio} - {self.Nombre_Servicio}>"


class NivelFragilidad(db.Model):
    __tablename__ = 'Nivel_Fragilidad'

    Id_Fragilidad = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    Nivel = db.Column(VARCHAR(30), nullable=False, unique=True)
    Detalle_Impacto = db.Column(TEXT, nullable=True)

    servicios = relationship("Servicios", back_populates="fragilidad")

    def __repr__(self):
        return f"<NivelFragilidad {self.Id_Fragilidad} - {self.Nivel}>"
=======
    """Tipos de servicio disponibles"""
    __tablename__ = 'Tipo_Servicio'
    
    Id_Tipo_Servicio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre_Servicio = db.Column(db.String(20), nullable=False, unique=True)
    
    # Relaciones
    servicios = db.relationship('Servicios', back_populates='tipo_servicio', lazy='dynamic')
    
    def __repr__(self):
        return f'<TipoServicio {self.Nombre_Servicio}>'


class NivelFragilidad(db.Model):
    """Niveles de fragilidad para cargamentos"""
    __tablename__ = 'Nivel_Fragilidad'
    
    Id_Fragilidad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nivel = db.Column(db.String(30), nullable=False, unique=True)
    Detalle_Impacto = db.Column(db.Text, nullable=True)
    
    # Relaciones
    servicios = db.relationship('Servicios', back_populates='fragilidad', lazy='dynamic')
    
    def __repr__(self):
        return f'<NivelFragilidad {self.Nivel}>'
>>>>>>> Gestion_Evidencia_Documentacion


# ============================================
# MÓDULO: SERVICIOS (TABLA CENTRAL)
# ============================================

class Servicios(db.Model):
<<<<<<< HEAD
    __tablename__ = 'Servicios'

    Id_Servicio = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    Id_Cliente = db.Column(INTEGER(unsigned=False), ForeignKey('Clientes.Id_Cliente'), nullable=False)
    Id_Vehiculo = db.Column(INTEGER(unsigned=True), ForeignKey('Vehiculos.id_vehiculo'), nullable=False)
    id_conductor = db.Column(INTEGER(unsigned=False), ForeignKey('conductor.id_conductor'), nullable=False)
    Id_Tipo_Servicio = db.Column(INTEGER(unsigned=False), ForeignKey('Tipo_Servicio.Id_Tipo_Servicio'), nullable=False)
    Id_Fragilidad = db.Column(INTEGER(unsigned=False), ForeignKey('Nivel_Fragilidad.Id_Fragilidad'), nullable=False)
    Id_Ubicacion = db.Column(INTEGER(unsigned=False), ForeignKey('Ubicaciones.Id_Ubicacion'), nullable=False)

    Peso_Carga = db.Column(DECIMAL(10, 2), nullable=False)
    Fecha_Pedido = db.Column(DATE, nullable=False)
    Fecha_Entrega = db.Column(DATE, nullable=False)
    Precio_Total = db.Column(DECIMAL(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint('Peso_Carga > 0', name='chk_serv_peso_pos'),
        CheckConstraint('Precio_Total >= 0', name='chk_serv_precio_no_neg'),
=======
    """Registro de servicios de envío solicitados"""
    __tablename__ = 'Servicios'
    __table_args__ = (
        CheckConstraint('Peso_Carga > 0', name='chk_peso_pos'),
        CheckConstraint('Precio_Total >= 0', name='chk_precio_pos'),
>>>>>>> Gestion_Evidencia_Documentacion
        Index('ix_servicios_cliente', 'Id_Cliente'),
        Index('ix_servicios_fecha', 'Fecha_Pedido', 'Fecha_Entrega'),
        Index('ix_servicios_conductor', 'id_conductor'),
    )
<<<<<<< HEAD

    # Relaciones
    cliente = relationship("Clientes", back_populates="servicios")
    vehiculo = relationship("Vehiculos")
    conductor = relationship("Conductor", back_populates="servicios")
    tipo_servicio = relationship("TipoServicio", back_populates="servicios")
    fragilidad = relationship("NivelFragilidad", back_populates="servicios")
    ubicacion = relationship("Ubicaciones")

    evidencias = relationship("Evidencia", back_populates="servicio", cascade="all, delete-orphan")
    seguimientos = relationship("SeguimientoControl", back_populates="servicio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Servicio {self.Id_Servicio} Cliente:{self.Id_Cliente}>"
=======
    
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
    
    # Relaciones
    cliente = db.relationship('Clientes', back_populates='servicios')
    vehiculo = db.relationship('Vehiculos', back_populates='servicios')
    conductor = db.relationship('Conductor', back_populates='servicios')
    tipo_servicio = db.relationship('TipoServicio', back_populates='servicios')
    fragilidad = db.relationship('NivelFragilidad', back_populates='servicios')
    ubicacion = db.relationship('Ubicaciones', back_populates='servicios')
    evidencias = db.relationship('Evidencia', back_populates='servicio', lazy='dynamic', cascade='all, delete-orphan')
    seguimientos = db.relationship('SeguimientoControl', back_populates='servicio', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Servicio {self.Id_Servicio}>'
>>>>>>> Gestion_Evidencia_Documentacion


# ============================================
# MÓDULO: CONTROL DE EVIDENCIAS Y DOCUMENTACIÓN
# ============================================

class Evidencia(db.Model):
<<<<<<< HEAD
    __tablename__ = 'EVIDENCIA'

    id_evidencia = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    id_servicio = db.Column(INTEGER(unsigned=False), ForeignKey('Servicios.Id_Servicio'), nullable=False)

    tipo_evidencia = db.Column(ENUM('foto_salida', 'foto_entrega', 'documento_firmado'), nullable=False)
    nombre_archivo = db.Column(VARCHAR(255), nullable=False)
    es_legible = db.Column(BOOLEAN, default=True)
    fecha_captura = db.Column(DATETIME, default=datetime.utcnow)

    servicio = relationship("Servicios", back_populates="evidencias")

=======
    """Evidencias fotográficas y documentos de envíos"""
    __tablename__ = 'EVIDENCIA'
>>>>>>> Gestion_Evidencia_Documentacion
    __table_args__ = (
        Index('ix_evidencia_servicio', 'id_servicio'),
        Index('ix_evidencia_tipo', 'tipo_evidencia'),
    )
<<<<<<< HEAD

    def __repr__(self):
        return f"<Evidencia {self.id_evidencia} - Serv:{self.id_servicio} - {self.tipo_evidencia}>"


class SeguimientoControl(db.Model):
    __tablename__ = 'SEGUIMIENTO_CONTROL'

    id_seguimiento = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    id_servicio = db.Column(INTEGER(unsigned=False), ForeignKey('Servicios.Id_Servicio'), nullable=False)

    estado_actual = db.Column(ENUM('cargando', 'en_ruta', 'en_espera', 'entregado'), nullable=False)
    control_calidad = db.Column(ENUM('aprobado', 'rechazado', 'pendiente'), default='pendiente')
    incidente = db.Column(VARCHAR(200), nullable=True)
    notificacion_enviada = db.Column(BOOLEAN, default=False)
    nombre_receptor = db.Column(VARCHAR(100), nullable=True)
    fecha_hora = db.Column(DATETIME, default=datetime.utcnow)

    servicio = relationship("Servicios", back_populates="seguimientos")

=======
    
    id_evidencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_servicio = db.Column(db.Integer, db.ForeignKey('Servicios.Id_Servicio'), nullable=False)
    tipo_evidencia = db.Column(db.Enum('foto_salida', 'foto_entrega', 'documento_firmado', name='tipo_evidencia_enum'), nullable=False)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    es_legible = db.Column(db.Boolean, default=True)
    fecha_captura = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    servicio = db.relationship('Servicios', back_populates='evidencias')
    
    def __repr__(self):
        return f'<Evidencia {self.tipo_evidencia} - Servicio {self.id_servicio}>'


class SeguimientoControl(db.Model):
    """Seguimiento y control de estados de envíos"""
    __tablename__ = 'SEGUIMIENTO_CONTROL'
>>>>>>> Gestion_Evidencia_Documentacion
    __table_args__ = (
        Index('ix_seguimiento_servicio', 'id_servicio'),
        Index('ix_seguimiento_estado', 'estado_actual'),
        Index('ix_seguimiento_fecha', 'fecha_hora'),
    )
<<<<<<< HEAD

    def __repr__(self):
        return f"<Seguimiento {self.id_seguimiento} - Serv:{self.id_servicio} - {self.estado_actual}>"
=======
    
    id_seguimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_servicio = db.Column(db.Integer, db.ForeignKey('Servicios.Id_Servicio'), nullable=False)
    estado_actual = db.Column(db.Enum('cargando', 'en_ruta', 'en_espera', 'entregado', name='estado_envio_enum'), nullable=False)
    control_calidad = db.Column(db.Enum('aprobado', 'rechazado', 'pendiente', name='control_calidad_enum'), default='pendiente')
    incidente = db.Column(db.String(200), nullable=True)
    notificacion_enviada = db.Column(db.Boolean, default=False)
    nombre_receptor = db.Column(db.String(100), nullable=True)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    servicio = db.relationship('Servicios', back_populates='seguimientos')
    
    def __repr__(self):
        return f'<Seguimiento {self.estado_actual} - Servicio {self.id_servicio}>'
>>>>>>> Gestion_Evidencia_Documentacion
