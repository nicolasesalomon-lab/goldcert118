from datetime import datetime, date

from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from .app.extensions import SessionLocal
from .app import models


def seed() -> None:
    session: Session = SessionLocal()
    try:
        # Admin user
        if not session.query(models.User).filter_by(email="admin@test.com").first():
            admin = models.User(
                email="admin@test.com",
                name="Admin",
                role=models.RoleEnum.Admin,
                password_hash=bcrypt.hash("admin"),
                created_at=datetime.utcnow(),
            )
            session.add(admin)

        # Organismos de certificación
        for nombre in ["IRAM", "TÜV", "Lenor"]:
            if not session.query(models.OrganismoCertificacion).filter_by(nombre=nombre).first():
                session.add(
                    models.OrganismoCertificacion(
                        nombre=nombre, creado_en=datetime.utcnow()
                    )
                )
        session.flush()

        # Proveedor demo
        proveedor = (
            session.query(models.Proveedor)
            .filter_by(nombre="Proveedor Demo")
            .first()
        )
        if not proveedor:
            proveedor = models.Proveedor(
                nombre="Proveedor Demo",
                email="demo@proveedor.com",
                telefono="123456789",
                creado_en=datetime.utcnow(),
            )
            session.add(proveedor)
            session.flush()

        # Fábrica demo con auditoría caducada
        fabrica = (
            session.query(models.Fabrica)
            .filter_by(nombre="Fábrica Demo")
            .first()
        )
        if not fabrica:
            fabrica = models.Fabrica(
                proveedor_id=proveedor.id,
                nombre="Fábrica Demo",
                direccion="Calle Falsa 123",
                audit_valida_desde=date(2020, 1, 1),
                audit_valida_hasta=date(2021, 1, 1),
                creado_en=datetime.utcnow(),
            )
            session.add(fabrica)
            session.flush()

        # Producto demo
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
                modelo_proveedor="M-Prov-1",
                modelo_goldmund="GM-1",
                odc_id=odc.id if odc else None,
            )
            session.add(producto)
            session.flush()

        # Certificaciones demo
        if not session.query(models.Certificacion).filter_by(
            producto_id=producto.id, estado=models.EstadoCertificacionEnum.vigente
        ).first():
            session.add(
                models.Certificacion(
                    producto_id=producto.id,
                    ambito_certificado=models.AmbitoCertificadoEnum.tipo,
                    fabrica_id=fabrica.id,
                    valido_desde=date(2023, 1, 1),
                    valido_hasta=date(2030, 1, 1),
                    estado=models.EstadoCertificacionEnum.vigente,
                    creado_en=datetime.utcnow(),
                )
            )

        if not session.query(models.Certificacion).filter_by(
            producto_id=producto.id, estado=models.EstadoCertificacionEnum.vencido
        ).first():
            session.add(
                models.Certificacion(
                    producto_id=producto.id,
                    ambito_certificado=models.AmbitoCertificadoEnum.tipo,
                    fabrica_id=fabrica.id,
                    valido_desde=date(2020, 1, 1),
                    valido_hasta=date(2021, 1, 1),
                    estado=models.EstadoCertificacionEnum.vencido,
                    creado_en=datetime.utcnow(),
                )
            )

        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    seed()
