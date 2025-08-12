from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .routes import auth, odc, providers, factories, products, certifications, dashboard

settings = get_settings()

app = FastAPI(title="GoldCert API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(odc.router, prefix="/api")
app.include_router(providers.router, prefix="/api")
app.include_router(factories.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(certifications.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

# Serve built frontend if present
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


@app.on_event("startup")
async def startup_event():
    import logging

    logging.getLogger("uvicorn").info(f"DB: {settings.DATABASE_URL}")
    logging.getLogger("uvicorn").info(f"Uploads: {settings.UPLOAD_FOLDER}")
