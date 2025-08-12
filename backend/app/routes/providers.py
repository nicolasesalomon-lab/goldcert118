from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from .. import models, schemas
from ..extensions import get_current_user, get_db, require_role

router = APIRouter(prefix="/providers", tags=["providers"])

write_dep = Depends(require_role(models.RoleEnum.Admin, models.RoleEnum.Analista))


@router.get("", response_model=list[schemas.ProviderOut])
def list_providers(
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
    sort: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(models.Proveedor)
    if search:
        query = query.filter(models.Proveedor.nombre.ilike(f"%{search}%"))
    sort_col = getattr(models.Proveedor, sort, models.Proveedor.id)
    sort_col = desc(sort_col) if order == "desc" else asc(sort_col)
    query = query.order_by(sort_col)
    return query.offset((page - 1) * size).limit(size).all()


@router.post("", response_model=schemas.ProviderOut, dependencies=[write_dep])
def create_provider(data: schemas.ProviderCreate, db: Session = Depends(get_db)):
    if db.query(models.Proveedor).filter_by(nombre=data.nombre).first():
        raise HTTPException(status_code=400, detail="Proveedor existente")
    provider = models.Proveedor(
        nombre=data.nombre,
        email=data.email,
        telefono=data.telefono,
        creado_en=datetime.utcnow(),
    )
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


@router.get("/{provider_id}", response_model=schemas.ProviderOut)
def get_provider(provider_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    provider = db.get(models.Proveedor, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return provider


@router.put("/{provider_id}", response_model=schemas.ProviderOut, dependencies=[write_dep])
def update_provider(provider_id: int, data: schemas.ProviderCreate, db: Session = Depends(get_db)):
    provider = db.get(models.Proveedor, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    for field, value in data.model_dump().items():
        setattr(provider, field, value)
    db.commit()
    db.refresh(provider)
    return provider


@router.patch("/{provider_id}", response_model=schemas.ProviderOut, dependencies=[write_dep])
def patch_provider(provider_id: int, data: dict, db: Session = Depends(get_db)):
    provider = db.get(models.Proveedor, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    for field, value in data.items():
        if hasattr(provider, field):
            setattr(provider, field, value)
    db.commit()
    db.refresh(provider)
    return provider


@router.delete("/{provider_id}", status_code=204, dependencies=[write_dep])
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.get(models.Proveedor, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(provider)
    db.commit()
