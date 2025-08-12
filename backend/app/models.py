from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, ForeignKey, Date
from sqlalchemy.orm import relationship
from .extensions import Base

class Role(str, Enum):
    ADMIN = "Admin"
    ANALISTA = "Analista"
    CONSULTA = "Consulta"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(SAEnum(Role), default=Role.ANALISTA)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class OrganismoCertificacion(Base):
    __tablename__ = "odc"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, index=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

class Proveedor(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    email = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    factories = relationship("Fabrica", back_populates="proveedor")

class Fabrica(Base):
    __tablename__ = "factories"
    id = Column(Integer, primary_key=True)
    proveedor_id = Column(Integer, ForeignKey("providers.id"))
    nombre = Column(String)
    direccion = Column(String)
    audit_valida_desde = Column(Date, nullable=True)
    audit_valida_hasta = Column(Date, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    proveedor = relationship("Proveedor", back_populates="factories")

class Producto(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    proveedor_id = Column(Integer, ForeignKey("providers.id"))
    modelo_proveedor = Column(String, nullable=True)
    modelo_goldmund = Column(String, nullable=True)
    odc_id = Column(Integer, ForeignKey("odc.id"))

class AmbitoCertificado(str, Enum):
    TIPO = "tipo"
    MARCA = "marca"

class EstadoCertificacion(str, Enum):
    VIGENTE = "vigente"
    VENCIDO = "vencido"
    SUSPENDIDO = "suspendido"

class Certificacion(Base):
    __tablename__ = "certifications"
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("products.id"))
    ambito_certificado = Column(SAEnum(AmbitoCertificado))
    fabrica_id = Column(Integer, ForeignKey("factories.id"), nullable=True)
    valido_desde = Column(Date)
    valido_hasta = Column(Date)
    estado = Column(SAEnum(EstadoCertificacion), default=EstadoCertificacion.VIGENTE)
    creado_en = Column(DateTime, default=datetime.utcnow)

class TipoItem(str, Enum):
    CB = "cb"
    TEST_REPORT = "test_report"
    MANUAL = "manual"
    ETIQUETAS = "etiquetas"
    MAPA_MODELOS = "mapa_modelos"
    DECLARACION_IDENTIDAD = "declaracion_identidad"
    VERIFICACION_IDENTIDAD = "verificacion_identidad"

class CertificacionRequisito(Base):
    __tablename__ = "certification_items"
    id = Column(Integer, primary_key=True)
    certificacion_id = Column(Integer, ForeignKey("certifications.id"))
    tipo_item = Column(SAEnum(TipoItem))
    file_path = Column(String)
    filename_original = Column(String)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
