from __future__ import annotations

from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import (
    String,
    DateTime,
    Enum as SAEnum,
    Date,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from .extensions import Base


class RoleEnum(str, enum.Enum):
    Admin = "Admin"
    Analista = "Analista"
    Consulta = "Consulta"


class AmbitoCertificadoEnum(str, enum.Enum):
    tipo = "tipo"
    marca = "marca"


class EstadoCertificacionEnum(str, enum.Enum):
    vigente = "vigente"
    vencido = "vencido"
    suspendido = "suspendido"


class TipoItemEnum(str, enum.Enum):
    cb = "cb"
    test_report = "test_report"
    manual = "manual"
    etiquetas = "etiquetas"
    mapa_modelos = "mapa_modelos"
    declaracion_identidad = "declaracion_identidad"
    verificacion_identidad = "verificacion_identidad"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[Optional[str]]
    role: Mapped[RoleEnum] = mapped_column(SAEnum(RoleEnum, name="role", native_enum=False), nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class OrganismoCertificacion(Base):
    __tablename__ = "organismos_certificacion"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Proveedor(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String)
    telefono: Mapped[Optional[str]] = mapped_column(String)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    fabricas: Mapped[List["Fabrica"]] = relationship("Fabrica", back_populates="proveedor")
    productos: Mapped[List["Producto"]] = relationship("Producto", back_populates="proveedor")


class Fabrica(Base):
    __tablename__ = "fabricas"

    id: Mapped[int] = mapped_column(primary_key=True)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String)
    audit_valida_desde: Mapped[Optional[date]] = mapped_column(Date)
    audit_valida_hasta: Mapped[Optional[date]] = mapped_column(Date)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    proveedor: Mapped["Proveedor"] = relationship("Proveedor", back_populates="fabricas")
    certificaciones: Mapped[List["Certificacion"]] = relationship("Certificacion", back_populates="fabrica")


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"), nullable=False)
    modelo_proveedor: Mapped[Optional[str]] = mapped_column(String)
    modelo_goldmund: Mapped[Optional[str]] = mapped_column(String)
    odc_id: Mapped[Optional[int]] = mapped_column(ForeignKey("organismos_certificacion.id"))

    proveedor: Mapped["Proveedor"] = relationship("Proveedor", back_populates="productos")
    odc: Mapped[Optional["OrganismoCertificacion"]] = relationship("OrganismoCertificacion")
    certificaciones: Mapped[List["Certificacion"]] = relationship("Certificacion", back_populates="producto")


class Certificacion(Base):
    __tablename__ = "certificaciones"
    __table_args__ = (
        UniqueConstraint(
            "producto_id",
            "ambito_certificado",
            "fabrica_id",
            "valido_desde",
            "valido_hasta",
            name="uq_cert_rango_basico",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), nullable=False)
    ambito_certificado: Mapped[AmbitoCertificadoEnum] = mapped_column(
        SAEnum(AmbitoCertificadoEnum, name="ambito_certificado", native_enum=False),
        nullable=False,
        default=AmbitoCertificadoEnum.tipo,
    )
    fabrica_id: Mapped[Optional[int]] = mapped_column(ForeignKey("fabricas.id"))
    valido_desde: Mapped[date] = mapped_column(Date, nullable=False)
    valido_hasta: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[EstadoCertificacionEnum] = mapped_column(
        SAEnum(EstadoCertificacionEnum, name="estado_certificacion", native_enum=False),
        nullable=False,
        default=EstadoCertificacionEnum.vigente,
    )
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    producto: Mapped["Producto"] = relationship("Producto", back_populates="certificaciones")
    fabrica: Mapped[Optional["Fabrica"]] = relationship("Fabrica", back_populates="certificaciones")
    requisitos: Mapped[List["CertificacionRequisito"]] = relationship(
        "CertificacionRequisito", back_populates="certificacion"
    )


class CertificacionRequisito(Base):
    __tablename__ = "certificaciones_requisitos"
    __table_args__ = (
        UniqueConstraint("certificacion_id", "tipo_item", name="uq_cert_item_unico"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    certificacion_id: Mapped[int] = mapped_column(ForeignKey("certificaciones.id"), nullable=False)
    tipo_item: Mapped[TipoItemEnum] = mapped_column(
        SAEnum(TipoItemEnum, name="tipo_item", native_enum=False), nullable=False
    )
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    filename_original: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    certificacion: Mapped["Certificacion"] = relationship(
        "Certificacion", back_populates="requisitos"
    )
