from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..extensions import get_current_user, get_db, require_role

router = APIRouter(prefix="/odc", tags=["odc"])


@router.get("", response_model=list[schemas.ODCOut])
def list_odc(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.OrganismoCertificacion).all()


@router.post(
    "",
    response_model=schemas.ODCOut,
    dependencies=[Depends(require_role(models.RoleEnum.Admin, models.RoleEnum.Analista))],
)
def create_odc(data: schemas.ODCBase, db: Session = Depends(get_db)):
    if db.query(models.OrganismoCertificacion).filter_by(nombre=data.nombre).first():
        raise HTTPException(status_code=400, detail="ODC existente")
    odc = models.OrganismoCertificacion(nombre=data.nombre, creado_en=datetime.utcnow())
    db.add(odc)
    db.commit()
    db.refresh(odc)
    return odc
