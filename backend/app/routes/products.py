from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..extensions import get_current_user, get_db, require_role

router = APIRouter(prefix="/products", tags=["products"])

write_dep = Depends(require_role(models.RoleEnum.Admin, models.RoleEnum.Analista))


@router.get("", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Producto).all()


@router.post("", response_model=schemas.ProductOut, dependencies=[write_dep])
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = models.Producto(
        nombre=data.nombre,
        proveedor_id=data.proveedor_id,
        modelo_proveedor=data.modelo_proveedor,
        modelo_goldmund=data.modelo_goldmund,
        odc_id=data.odc_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.get(models.Producto, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@router.put("/{product_id}", response_model=schemas.ProductOut, dependencies=[write_dep])
def update_product(product_id: int, data: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = db.get(models.Producto, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for field, value in data.model_dump().items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product
