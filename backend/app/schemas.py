from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from .models import Role, EstadoCertificacion, AmbitoCertificado, TipoItem

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: Role

    class Config:
        orm_mode = True

class ProviderBase(BaseModel):
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None

class ProviderCreate(ProviderBase):
    pass

class ProviderOut(ProviderBase):
    id: int

    class Config:
        orm_mode = True

class OdcBase(BaseModel):
    nombre: str

class OdcCreate(OdcBase):
    pass

class OdcOut(OdcBase):
    id: int

    class Config:
        orm_mode = True
