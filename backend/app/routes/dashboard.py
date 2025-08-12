from collections import Counter
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models
from ..extensions import get_current_user, get_db
from ..services import cert_rules

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    certs = db.query(models.Certificacion).all()
    for c in certs:
        db.refresh(c, attribute_names=["fabrica"])
        cert_rules.refresh_estado(c)
    db.commit()

    today = date.today()
    kpis = {"vigente": 0, "vencido": 0, "suspendido": 0, "p90": 0, "p180": 0, "p365": 0}
    vencen_90 = []
    vencen_180 = []
    vencen_365 = []
    suspendidos = []
    month_counts = Counter()

    for c in certs:
        month_counts[c.valido_hasta.strftime("%Y-%m")] += 1
        if c.estado == models.EstadoCertificacionEnum.vigente:
            kpis["vigente"] += 1
        elif c.estado == models.EstadoCertificacionEnum.vencido:
            kpis["vencido"] += 1
        else:
            kpis["suspendido"] += 1
            suspendidos.append(c.id)
        delta = (c.valido_hasta - today).days
        if 0 <= delta <= 90:
            kpis["p90"] += 1
            vencen_90.append(c.id)
        if 0 <= delta <= 180:
            kpis["p180"] += 1
            vencen_180.append(c.id)
        if 0 <= delta <= 365:
            kpis["p365"] += 1
            vencen_365.append(c.id)

    serie = []
    year = today.year
    month = today.month
    for _ in range(12):
        key = f"{year:04d}-{month:02d}"
        serie.append({"month": key, "count": month_counts.get(key, 0)})
        month += 1
        if month > 12:
            month = 1
            year += 1

    return {
        "kpis": kpis,
        "vencen_90": vencen_90,
        "vencen_180": vencen_180,
        "vencen_365": vencen_365,
        "suspendidos": suspendidos,
        "serie": serie,
    }
