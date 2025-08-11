from __future__ import annotations

import hashlib
from datetime import datetime, date, UTC

from sqlalchemy.orm import Session

from app.database import engine
from app import models


def seed() -> None:
    with Session(engine) as session:
        # Admin user
        if not session.query(models.User).filter_by(email="admin@test.com").first():
            password_hash = hashlib.sha256("admin".encode()).hexdigest()
            session.add(
                models.User(
                    email="admin@test.com",
                    name="Admin",
                    role=models.RoleEnum.ADMIN,
                    password_hash=password_hash,
                    created_at=datetime.now(UTC),
                )
            )

        # Organismos de certificación
        for nombre in ["IRAM", "TÜV", "Lenor"]:
            if not session.query(models.OrganismoCertificacion).filter_by(nombre=nombre).first():
                session.add(
                    models.OrganismoCertificacion(
                        nombre=nombre, creado_en=datetime.now(UTC)
                    )
                )

        session.flush()

        # Demo data
        proveedor = (
            session.query(models.Proveedor)
            .filter_by(nombre="Proveedor Demo")
            .first()
        )
        if not proveedor:
            proveedor = models.Proveedor(
                nombre="Proveedor Demo",
                email="proveedor@example.com",
                telefono="123456",
                creado_en=datetime.now(UTC),
            )
            session.add(proveedor)
            session.flush()

        fabrica = (
            session.query(models.Fabrica)
            .filter_by(nombre="Fabrica Demo", proveedor_id=proveedor.id)
            .first()
        )
        if not fabrica:
            fabrica = models.Fabrica(
                proveedor_id=proveedor.id,
                nombre="Fabrica Demo",
                direccion="Calle Falsa 123",
                audit_valida_desde=date(2020, 1, 1),
                audit_valida_hasta=date(2021, 1, 1),
                creado_en=datetime.now(UTC),
            )
            session.add(fabrica)
            session.flush()

        producto = (
            session.query(models.Producto)
            .filter_by(nombre="Producto Demo")
            .first()
        )
        if not producto:
            odc = (
                session.query(models.OrganismoCertificacion)
                .filter_by(nombre="IRAM")
                .first()
            )
            producto = models.Producto(
                nombre="Producto Demo",
                proveedor_id=proveedor.id,
                modelo_proveedor="P-001",
                modelo_goldmund="G-001",
                odc_id=odc.id if odc else None,
            )
            session.add(producto)
            session.flush()

        cert_vigente = (
            session.query(models.Certificacion)
            .filter_by(
                producto_id=producto.id,
                valido_desde=date(2023, 1, 1),
                valido_hasta=date(2025, 1, 1),
            )
            .first()
        )
        if not cert_vigente:
            cert_vigente = models.Certificacion(
                producto_id=producto.id,
                ambito_certificado=models.AmbitoCertificadoEnum.TIPO,
                fabrica_id=fabrica.id,
                valido_desde=date(2023, 1, 1),
                valido_hasta=date(2025, 1, 1),
                estado=models.EstadoEnum.VIGENTE,
                creado_en=datetime.now(UTC),
            )
            session.add(cert_vigente)

        cert_vencido = (
            session.query(models.Certificacion)
            .filter_by(
                producto_id=producto.id,
                valido_desde=date(2020, 1, 1),
                valido_hasta=date(2021, 1, 1),
            )
            .first()
        )
        if not cert_vencido:
            cert_vencido = models.Certificacion(
                producto_id=producto.id,
                ambito_certificado=models.AmbitoCertificadoEnum.TIPO,
                fabrica_id=fabrica.id,
                valido_desde=date(2020, 1, 1),
                valido_hasta=date(2021, 1, 1),
                estado=models.EstadoEnum.VENCIDO,
                creado_en=datetime.now(UTC),
            )
            session.add(cert_vencido)

        session.commit()


if __name__ == "__main__":
    seed()
