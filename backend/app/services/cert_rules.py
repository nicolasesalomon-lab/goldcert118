from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import models


def dates_overlap(a_start: date, a_end: date, b_start: date, b_end: date) -> bool:
    return a_start <= b_end and b_start <= a_end


def ensure_no_overlap(db: Session, cert: models.Certificacion) -> None:
    q = db.query(models.Certificacion).filter(
        models.Certificacion.producto_id == cert.producto_id,
        models.Certificacion.ambito_certificado == cert.ambito_certificado,
        models.Certificacion.fabrica_id == cert.fabrica_id,
        models.Certificacion.id != cert.id,
        models.Certificacion.valido_desde <= cert.valido_hasta,
        cert.valido_desde <= models.Certificacion.valido_hasta,
    )
    if db.query(q.exists()).scalar():
        raise HTTPException(status_code=400, detail="Superposición de vigencias")


def compute_estado(cert: models.Certificacion) -> models.EstadoCertificacionEnum:
    today = date.today()
    if cert.valido_hasta < today:
        return models.EstadoCertificacionEnum.vencido
    if (
        cert.ambito_certificado == models.AmbitoCertificadoEnum.marca
        and cert.fabrica
        and cert.fabrica.audit_valida_hasta
        and cert.fabrica.audit_valida_hasta < today
    ):
        return models.EstadoCertificacionEnum.suspendido
    return models.EstadoCertificacionEnum.vigente


def refresh_estado(cert: models.Certificacion) -> None:
    cert.estado = compute_estado(cert)
