from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..extensions import get_current_user, get_db, require_role

router = APIRouter(prefix="/factories", tags=["factories"])

write_dep = Depends(require_role(models.RoleEnum.Admin, models.RoleEnum.Analista))


@router.get("", response_model=list[schemas.FactoryOut])
def list_factories(
    provider_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(models.Fabrica)
    if provider_id:
        query = query.filter_by(proveedor_id=provider_id)
    return query.all()


@router.post("", response_model=schemas.FactoryOut, dependencies=[write_dep])
def create_factory(data: schemas.FactoryCreate, db: Session = Depends(get_db)):
    factory = models.Fabrica(
        proveedor_id=data.proveedor_id,
        nombre=data.nombre,
        direccion=data.direccion,
        audit_valida_desde=data.audit_valida_desde,
        audit_valida_hasta=data.audit_valida_hasta,
        creado_en=datetime.utcnow(),
    )
    db.add(factory)
    db.commit()
    db.refresh(factory)
    return factory
