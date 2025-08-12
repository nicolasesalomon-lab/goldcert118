from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..extensions import get_db
from .. import models, schemas
from .auth import get_current_user

router = APIRouter()


@router.get("/", response_model=list[schemas.ProviderOut])
def list_providers(
    page: int = 1,
    size: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Proveedor)
    if search:
        query = query.filter(models.Proveedor.nombre.contains(search))
    providers = query.offset((page - 1) * size).limit(size).all()
    return providers


@router.post("/", response_model=schemas.ProviderOut, status_code=201)
def create_provider(
    provider: schemas.ProviderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_provider = models.Proveedor(**provider.dict())
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


@router.get("/{provider_id}", response_model=schemas.ProviderOut)
def get_provider(provider_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    provider = db.get(models.Proveedor, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider
