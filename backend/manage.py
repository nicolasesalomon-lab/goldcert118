from backend.app.extensions import SessionLocal
from backend.app import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    db = SessionLocal()
    if not db.query(models.User).first():
        admin = models.User(
            email="admin@test.com",
            name="Admin",
            role=models.Role.ADMIN,
            password_hash=pwd_context.hash("admin"),
        )
        db.add(admin)
    if db.query(models.OrganismoCertificacion).count() == 0:
        for nombre in ["IRAM", "TÜV", "Lenor"]:
            db.add(models.OrganismoCertificacion(nombre=nombre))
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
