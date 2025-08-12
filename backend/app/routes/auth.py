from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..extensions import (
    create_access_token,
    get_current_user,
    get_db,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        email=user_in.email,
        name=user_in.name,
        role=user_in.role,
        password_hash=hash_password(user_in.password),
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return schemas.Token(access_token=token)


@router.get("/me", response_model=schemas.UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user
