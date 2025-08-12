import os, sys
sys.path.append(os.path.abspath("."))
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.extensions import Base
from backend.app import models
from backend.app.services.cert_rules import validate_no_overlap


def create_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def test_no_superposicion_vigencias():
    db = create_session()
    prod = models.Producto(nombre="p1", proveedor_id=1, odc_id=1)
    db.add(prod)
    db.commit()
    cert1 = models.Certificacion(
        producto_id=prod.id,
        ambito_certificado=models.AmbitoCertificado.TIPO,
        valido_desde=date(2023, 1, 1),
        valido_hasta=date(2023, 12, 31),
    )
    db.add(cert1)
    db.commit()
    try:
        validate_no_overlap(db, prod.id, models.AmbitoCertificado.TIPO, None, date(2023, 6, 1), date(2023, 7, 1))
    except ValueError:
        assert True
    else:
        assert False
