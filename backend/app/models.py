from __future__ import annotations

from datetime import datetime, date
from enum import Enum

from sqlalchemy import (
    Date, DateTime, Enum as SAEnum, ForeignKey, Integer, String, UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class RoleEnum(str, Enum):
    ADMIN = "Admin"
    ANALISTA = "Analista"
    CONSULTA = "Consulta"


class AmbitoCertificadoEnum(str, Enum):
    TIPO = "tipo"
    MARCA = "marca"


class EstadoEnum(str, Enum):
    VIGENTE = "vigente"
    VENCIDO = "vencido"
    SUSPENDIDO = "suspendido"


class TipoItemEnum(str, Enum):
    CB = "cb"
    TEST_REPORT = "test_report"
    MANUAL = "manual"
    ETIQUETAS = "etiquetas"
    MAPA_MODELOS = "mapa_modelos"
    DECLARACION_IDENTIDAD = "declaracion_identidad"
    VERIFICACION_IDENTIDAD = "verificacion_identidad"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[RoleEnum] = mapped_column(SAEnum(RoleEnum, name="role_enum"), nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class OrganismoCertificacion(Base):
    __tablename__ = "organismos_certificacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Proveedor(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    fabricas: Mapped[list["Fabrica"]] = relationship(back_populates="proveedor")
    productos: Mapped[list["Producto"]] = relationship(back_populates="proveedor")


class Fabrica(Base):
    __tablename__ = "fabricas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    direccion: Mapped[str | None] = mapped_column(String, nullable=True)
    audit_valida_desde: Mapped[date | None] = mapped_column(Date, nullable=True)
    audit_valida_hasta: Mapped[date | None] = mapped_column(Date, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    proveedor: Mapped[Proveedor] = relationship(back_populates="fabricas")
    certificaciones: Mapped[list["Certificacion"]] = relationship(back_populates="fabrica")


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    proveedor_id: Mapped[int] = mapped_column(ForeignKey("proveedores.id"), nullable=False)
    modelo_proveedor: Mapped[str | None] = mapped_column(String, nullable=True)
    modelo_goldmund: Mapped[str | None] = mapped_column(String, nullable=True)
    odc_id: Mapped[int | None] = mapped_column(ForeignKey("organismos_certificacion.id"), nullable=True)

    proveedor: Mapped[Proveedor] = relationship(back_populates="productos")
    certificaciones: Mapped[list["Certificacion"]] = relationship(back_populates="producto")


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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), nullable=False)
    ambito_certificado: Mapped[AmbitoCertificadoEnum] = mapped_column(
        SAEnum(AmbitoCertificadoEnum, name="ambito_certificado_enum"), nullable=False, default=AmbitoCertificadoEnum.TIPO
    )
    fabrica_id: Mapped[int | None] = mapped_column(ForeignKey("fabricas.id"), nullable=True)
    valido_desde: Mapped[date] = mapped_column(Date, nullable=False)
    valido_hasta: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[EstadoEnum] = mapped_column(
        SAEnum(EstadoEnum, name="estado_enum"), nullable=False, default=EstadoEnum.VIGENTE
    )
    creado_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    producto: Mapped[Producto] = relationship(back_populates="certificaciones")
    fabrica: Mapped[Fabrica | None] = relationship(back_populates="certificaciones")
    requisitos: Mapped[list["CertificacionRequisito"]] = relationship(back_populates="certificacion")


class CertificacionRequisito(Base):
    __tablename__ = "certificaciones_requisitos"
    __table_args__ = (
        UniqueConstraint("certificacion_id", "tipo_item", name="uq_cert_item_unico"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    certificacion_id: Mapped[int] = mapped_column(ForeignKey("certificaciones.id"), nullable=False)
    tipo_item: Mapped[TipoItemEnum] = mapped_column(SAEnum(TipoItemEnum, name="tipo_item_enum"), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    filename_original: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_by: Mapped[str | None] = mapped_column(String, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    certificacion: Mapped[Certificacion] = relationship(back_populates="requisitos")
