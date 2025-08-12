from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .models import (
    RoleEnum,
    AmbitoCertificadoEnum,
    EstadoCertificacionEnum,
    TipoItemEnum,
)


class Token(BaseModel):
    access_token: str


class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    role: RoleEnum = RoleEnum.Consulta


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Login(BaseModel):
    email: str
    password: str


class ODCBase(BaseModel):
    nombre: str


class ODCOut(ODCBase):
    id: int
    creado_en: datetime
    model_config = ConfigDict(from_attributes=True)


class ProviderBase(BaseModel):
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None


class ProviderCreate(ProviderBase):
    pass


class ProviderOut(ProviderBase):
    id: int
    creado_en: datetime
    model_config = ConfigDict(from_attributes=True)


class FactoryBase(BaseModel):
    proveedor_id: int
    nombre: str
    direccion: Optional[str] = None
    audit_valida_desde: Optional[date] = None
    audit_valida_hasta: Optional[date] = None


class FactoryCreate(FactoryBase):
    pass


class FactoryOut(FactoryBase):
    id: int
    creado_en: datetime
    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    nombre: str
    proveedor_id: int
    modelo_proveedor: Optional[str] = None
    modelo_goldmund: Optional[str] = None
    odc_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CertificationBase(BaseModel):
    producto_id: int
    ambito_certificado: AmbitoCertificadoEnum = AmbitoCertificadoEnum.tipo
    fabrica_id: Optional[int] = None
    valido_desde: date
    valido_hasta: date


class CertificationCreate(CertificationBase):
    pass


class CertificationOut(CertificationBase):
    id: int
    estado: EstadoCertificacionEnum
    creado_en: datetime
    model_config = ConfigDict(from_attributes=True)


class CertificationItemOut(BaseModel):
    id: int
    tipo_item: TipoItemEnum
    filename_original: str
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)
