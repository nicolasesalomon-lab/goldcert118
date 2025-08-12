import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .extensions import Base, engine
from .routes import auth, providers, odc

app = FastAPI(title="GoldCert 2.0")

# CORS for dev - frontend proxy from Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(providers.router, prefix="/api/providers", tags=["providers"])
app.include_router(odc.router, prefix="/api/odc", tags=["odc"])


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
