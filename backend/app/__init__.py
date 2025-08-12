from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.on_event("startup")
async def startup_event():
    import logging

    logging.getLogger("uvicorn").info(f"DB: {settings.DATABASE_URL}")
    logging.getLogger("uvicorn").info(f"Uploads: {settings.UPLOAD_FOLDER}")
