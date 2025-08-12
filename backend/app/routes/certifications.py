from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .. import models, schemas
from ..extensions import get_current_user, get_db, require_role, settings
from ..services import cert_rules

router = APIRouter(prefix="/certifications", tags=["certifications"])

write_dep = Depends(require_role(models.RoleEnum.Admin, models.RoleEnum.Analista))


@router.post("", response_model=schemas.CertificationOut, dependencies=[write_dep])
def create_cert(data: schemas.CertificationCreate, db: Session = Depends(get_db)):
    cert = models.Certificacion(
        producto_id=data.producto_id,
        ambito_certificado=data.ambito_certificado,
        fabrica_id=data.fabrica_id,
        valido_desde=data.valido_desde,
        valido_hasta=data.valido_hasta,
        creado_en=datetime.utcnow(),
    )
    cert_rules.ensure_no_overlap(db, cert)
    db.add(cert)
    db.flush()
    db.refresh(cert)
    db.refresh(cert, attribute_names=["fabrica"])
    cert_rules.refresh_estado(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.get("/{cert_id}", response_model=schemas.CertificationOut)
def get_cert(cert_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cert = db.get(models.Certificacion, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificación no encontrada")
    db.refresh(cert, attribute_names=["fabrica"])
    cert_rules.refresh_estado(cert)
    db.commit()
    return cert


@router.put("/{cert_id}", response_model=schemas.CertificationOut, dependencies=[write_dep])
def update_cert(cert_id: int, data: schemas.CertificationCreate, db: Session = Depends(get_db)):
    cert = db.get(models.Certificacion, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificación no encontrada")
    for field, value in data.model_dump().items():
        setattr(cert, field, value)
    cert_rules.ensure_no_overlap(db, cert)
    db.refresh(cert, attribute_names=["fabrica"])
    cert_rules.refresh_estado(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.post("/{cert_id}/items/{tipo}", response_model=schemas.CertificationItemOut, dependencies=[write_dep])
async def upload_item(
    cert_id: int,
    tipo: models.TipoItemEnum,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    cert = db.get(models.Certificacion, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificación no encontrada")
    content = await file.read()
    if len(content) > settings.MAX_CONTENT_LENGTH:
        raise HTTPException(status_code=400, detail="Archivo demasiado grande")
    filename = f"cert_{cert_id}_{tipo}_{int(datetime.utcnow().timestamp())}_{file.filename}"
    path = Path(settings.UPLOAD_FOLDER) / filename
    path.write_bytes(content)
    item = (
        db.query(models.CertificacionRequisito)
        .filter_by(certificacion_id=cert_id, tipo_item=tipo)
        .first()
    )
    if item:
        item.file_path = str(path)
        item.filename_original = file.filename
        item.uploaded_by = user.id
        item.uploaded_at = datetime.utcnow()
    else:
        item = models.CertificacionRequisito(
            certificacion_id=cert_id,
            tipo_item=tipo,
            file_path=str(path),
            filename_original=file.filename,
            uploaded_by=user.id,
            uploaded_at=datetime.utcnow(),
        )
        db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{cert_id}/items/{tipo}/download")
def download_item(
    cert_id: int,
    tipo: models.TipoItemEnum,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    item = (
        db.query(models.CertificacionRequisito)
        .filter_by(certificacion_id=cert_id, tipo_item=tipo)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(item.file_path, filename=item.filename_original)
