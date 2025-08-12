from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..extensions import get_db
from .. import models, schemas
from .auth import get_current_user

router = APIRouter()


@router.get("/", response_model=list[schemas.OdcOut])
def list_odc(db: Session = Depends(get_db)):
    return db.query(models.OrganismoCertificacion).all()


@router.post("/", response_model=schemas.OdcOut)
def create_odc(
    odc: schemas.OdcCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_odc = models.OrganismoCertificacion(**odc.dict())
    db.add(db_odc)
    db.commit()
    db.refresh(db_odc)
    return db_odc
