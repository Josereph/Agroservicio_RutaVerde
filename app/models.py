from . import db
from datatime import datetime

# app/models.py
from datetime import datetime
from app import db
from sqlalchemy import CheckConstraint, Index, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import (
    INTEGER, TINYINT, SMALLINT, VARCHAR, TEXT, DECIMAL, BOOLEAN, ENUM, DATETIME, DATE
)

# ============================================
# MÓDULO: UBICACIONES GEOGRÁFICAS
# ============================================

class Departamento(db.Model):
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

    __table_args__ = (
        CheckConstraint('capacidad_kg > 0', name='chk_capacidad_pos'),
        CheckConstraint('km_actual >= 0', name='chk_km_no_neg'),
        Index('ix_vehiculo_estado', 'estado_id'),
        Index('ix_vehiculo_tipo', 'tipo_id'),
        Index('ix_vehiculo_capacidad', 'capacidad_kg'),
    )

    def __repr__(self):
        return f"<Vehiculo {self.id_vehiculo} {self.placa}>"


# ============================================
# MÓDULO: CONDUCTORES
# ============================================

class Conductor(db.Model):
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


# ============================================
# MÓDULO: CLIENTES
# ============================================

class Clientes(db.Model):
    __tablename__ = 'Clientes'

    Id_Cliente = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    Nombre_Cliente = db.Column(VARCHAR(100), nullable=False)
    Dui = db.Column(VARCHAR(20), nullable=False, unique=True)
    CorreoElectronico = db.Column(VARCHAR(200), nullable=False)

    servicios = relationship("Servicios", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente {self.Id_Cliente} - {self.Nombre_Cliente}>"


# ============================================
# MÓDULO: CATÁLOGOS DE SERVICIOS
# ============================================

class TipoServicio(db.Model):
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


# ============================================
# MÓDULO: SERVICIOS (TABLA CENTRAL)
# ============================================

class Servicios(db.Model):
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
        Index('ix_servicios_cliente', 'Id_Cliente'),
        Index('ix_servicios_fecha', 'Fecha_Pedido', 'Fecha_Entrega'),
        Index('ix_servicios_conductor', 'id_conductor'),
    )

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


# ============================================
# MÓDULO: CONTROL DE EVIDENCIAS Y DOCUMENTACIÓN
# ============================================

class Evidencia(db.Model):
    __tablename__ = 'EVIDENCIA'

    id_evidencia = db.Column(INTEGER(unsigned=False), primary_key=True, autoincrement=True)
    id_servicio = db.Column(INTEGER(unsigned=False), ForeignKey('Servicios.Id_Servicio'), nullable=False)

    tipo_evidencia = db.Column(ENUM('foto_salida', 'foto_entrega', 'documento_firmado'), nullable=False)
    nombre_archivo = db.Column(VARCHAR(255), nullable=False)
    es_legible = db.Column(BOOLEAN, default=True)
    fecha_captura = db.Column(DATETIME, default=datetime.utcnow)

    servicio = relationship("Servicios", back_populates="evidencias")

    __table_args__ = (
        Index('ix_evidencia_servicio', 'id_servicio'),
        Index('ix_evidencia_tipo', 'tipo_evidencia'),
    )

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

    __table_args__ = (
        Index('ix_seguimiento_servicio', 'id_servicio'),
        Index('ix_seguimiento_estado', 'estado_actual'),
        Index('ix_seguimiento_fecha', 'fecha_hora'),
    )

    def __repr__(self):
        return f"<Seguimiento {self.id_seguimiento} - Serv:{self.id_servicio} - {self.estado_actual}>"
