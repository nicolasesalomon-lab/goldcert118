from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Certificacion


def validate_no_overlap(db: Session, producto_id: int, ambito, fabrica_id, desde: date, hasta: date, cert_id: int | None = None):
    stmt = select(Certificacion).where(
        Certificacion.producto_id == producto_id,
        Certificacion.ambito_certificado == ambito,
    )
    if fabrica_id:
        stmt = stmt.where(Certificacion.fabrica_id == fabrica_id)
    else:
        stmt = stmt.where(Certificacion.fabrica_id.is_(None))
    if cert_id:
        stmt = stmt.where(Certificacion.id != cert_id)
    existing = db.execute(stmt).scalars().all()
    for cert in existing:
        if (desde <= cert.valido_hasta) and (cert.valido_desde <= hasta):
            raise ValueError("Superposición de vigencias")
