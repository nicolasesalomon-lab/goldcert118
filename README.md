PROMPT MAESTRO — “GoldCert 2.0: app funcional y robusta sin fricción”
Actuás como un arquitecto full-stack senior y generador de repos. Quiero un repo nuevo llamado goldcert-2.0 que funcione out-of-the-box en Windows y Linux, sin preguntas. Tomá todas las decisiones. Entregá una web funcional con los flujos clave de certificaciones. Evitá configuraciones frágiles. No pidas aclaraciones; si algo no está, decidilo con criterio y documentalo.

0) Principios duros
Cero fricción para correr local: ./scripts/dev.ps1 (Windows) y ./scripts/dev.sh (Linux/Mac) hacen todo (instalar deps, migrar, seedear, levantar front+back).

Una fuente de verdad de API y un solo origen en dev para evitar CORS: el frontend sirve al backend como reverse proxy (Vite proxy a /api → http://localhost:8000). En prod, el backend sirve los estáticos del build.

DB simple en dev: SQLite (archivo local). Postgres opcional por DATABASE_URL.

Estabilidad > “último hype”: FastAPI + SQLAlchemy 2 + Alembic + Pydantic v2; React + Vite + TS + Tailwind + shadcn/ui + React Query + react-hook-form + Zod.

Ergonomía: toasts para éxito/error, loaders decentes, tablas con búsqueda/orden/paginación, combobox “creatable”.

Seguridad: JWT (Bearer), roles Admin | Analista | Consulta, guardas en front y back.

Tests mínimos: 1 unit de regla de negocio (no superposición de vigencias) y 1 e2e “crear proveedor → aparece en listado”.

Docs completas: README con pasos, scripts, rutas, roles y pantallazos.

1) Estructura de repo (monorepo simple)
bash
Copiar
Editar
goldcert-2.0/
  backend/
    app/
      __init__.py
      config.py
      extensions.py
      models.py
      schemas.py
      services/
        cert_rules.py
      routes/
        auth.py
        dashboard.py
        providers.py
        factories.py
        products.py
        certifications.py
        odc.py
      uploads/          # .gitkeep
    migrations/         # Alembic
    tests/
      test_cert_rules.py
    requirements.txt
    alembic.ini         # generado
    manage.py           # entry CLI si hace falta
  frontend/
    index.html
    vite.config.ts
    tsconfig.json
    src/
      main.tsx
      App.tsx
      lib/axios.ts
      lib/auth.ts
      components/
        DataTable.tsx
        FileUploader.tsx
        ComboboxCreatable.tsx
      components/ui/...   # shadcn
      screens/
        Login.tsx
        Dashboard.tsx
        providers/ProvidersList.tsx
        providers/ProviderForm.tsx
        providers/ProviderDetail.tsx
        providers/FactoryCreate.tsx
        products/ProductForm.tsx
        cert/CertificationWizard.tsx
      routes.tsx
  scripts/
    dev.ps1
    dev.sh
  .env.example        # raíz (opcional)
  README.md
2) Stack decidido
Backend
FastAPI (uvicorn), SQLAlchemy 2.0, Alembic, Pydantic v2, python-jose (JWT), passlib (hash), python-multipart (uploads).

SQLite por defecto: sqlite:///./goldcert.db. Postgres al exportar DATABASE_URL.

Estructura DTO/Schema con Pydantic; errores HTTP coherentes; logging básico.

Subidas a backend/app/uploads (bind a disco). Descargas con FileResponse y Content-Disposition.

Frontend
Vite + React + TypeScript, Tailwind + shadcn/ui, React Query, axios, react-hook-form + @hookform/resolvers + Zod, sonner (toasts).

Vite proxy: toda request a /api va a http://localhost:8000.

Estilo visual inspirado en oro/negro, con header, nav y secciones como en el HTML de muestra (no copiar 1:1, pero respetar paleta y jerarquía visual). Fronthtml_grok4

3) Modelado mínimo imprescindible
Tablas (SQLAlchemy):

User: id, email (unique), name, role (Enum: Admin/Analista/Consulta), password_hash, created_at.

OrganismoCertificacion (odc): id, nombre (unique), creado_en.

Proveedor: id, nombre (unique), email, telefono, creado_en.

Fabrica: id, proveedor_id (FK), nombre, direccion, audit_valida_desde, audit_valida_hasta, creado_en.

Producto: id, nombre, proveedor_id (FK), modelo_proveedor, modelo_goldmund, odc_id (FK).

Certificacion: id, producto_id (FK), ambito_certificado (Enum: tipo|marca), fabrica_id (FK nullable), valido_desde, valido_hasta, estado (Enum: vigente|vencido|suspendido), creado_en.

CertificacionRequisito: id, certificacion_id (FK), tipo_item (Enum: cb|test_report|manual|etiquetas|mapa_modelos|declaracion_identidad|verificacion_identidad), file_path, filename_original, uploaded_by, uploaded_at. Unique(certificacion_id, tipo_item).

Reglas de negocio (servicio cert_rules.py)
No superposición de vigencias por (producto, ámbito, fábrica si aplica): si (a.start ≤ b.end) ∧ (b.start ≤ a.end) → 400.

Estado:

vencido si valido_hasta < hoy.

suspendido si ambito=marca y audit_valida_hasta de la fábrica < hoy.

vigente en caso contrario.

Recalcular estado en GET y save.

4) API REST (FastAPI)
Prefijo /api. JSON snake_case en DB / camelCase opcional en front si lo preferís, pero no te enredes: usa lo que venga de FastAPI.

Auth

POST /api/auth/register (admin-only para real; dev permite crear si no hay usuarios)

POST /api/auth/login → {access_token}

GET /api/auth/me (JWT)

Dashboard

GET /api/dashboard/summary → KPIs: vigente, vencido, suspendido, p90, p180, p365; listas vencen_90/180/365 y suspendidos; serie 12 meses por valido_hasta.

Organismos (OdC): GET /api/odc, POST /api/odc

Proveedores: GET /api/providers?page&size&search&sort&order, POST /api/providers, GET/PUT/PATCH/DELETE /api/providers/{id}

Fábricas: GET /api/factories?provider_id=, POST /api/factories

Productos: GET /api/products, POST /api/products, GET/PUT /api/products/{id}

Certificaciones

POST /api/certifications (valida reglas; setea estado)

GET /api/certifications/{id} (recalcula estado)

PUT/PATCH /api/certifications/{id} (revalida)

POST /api/certifications/{id}/items/{tipo} (form-data file) → guarda/replace; responde meta

GET /api/certifications/{id}/items/{tipo}/download (descarga con download_name)

Seguridad
JWT obligatorio para todo salvo POST /auth/register (solo si no hay usuarios) y GET /odc para el combobox.

RBAC básico por dependencia (Admin/Analista editan; Consulta read-only). Dev: relajado para QA.

5) Frontend — rutas y UX
/login (credentials → guarda token en localStorage).

/dashboard (post-login default):

KPIs en tarjetas.

Listas: “Vencen 90/180/365”, “Suspendidos” (links a detalle de cert).

Gráfico simple de vencimientos por mes (12) — usa Recharts o lista si no hay datos.

/proveedores (listado con búsqueda/orden/paginación; acción “Nuevo”; cada fila link al detalle).

/proveedores/nuevo (form zod; al guardar → redirect a /proveedores + toast “Proveedor creado”).

/proveedores/:id (detalle con pestañas: Fábricas (tabla + “Crear fábrica” inline), Productos, Certificados).

Crear fábrica: form inline, redirige manteniendo el detalle; lista actualizada y toast.

/productos/nuevo y /productos/:id (form orden exacto: Nombre, Proveedor (combobox por nombre), Modelo proveedor, Modelo padre Goldmund, OdC (combobox creatable: IRAM, TÜV, Lenor + agregar nuevo). Guardar con zod + toasts; redirect a /productos o back previo).

/certificaciones/:id (wizard/detalle):

7 filas (CB, test report, manual, etiquetas, mapa de modelos, declaración de identidad, verificación de identidad), con chip “pendiente/completo”, botón “Subir/Reemplazar” y link Descargar. Estado global visible.

6) Seeds
Usuario admin: admin@test.com / admin (hash).

OdC base: IRAM, TÜV, Lenor.

Demo mínima: 1 proveedor, 1 fábrica (auditoría caducada para probar “suspendido”), 1 producto, 2 certificaciones (una vigente, una vencida).

7) Scripts 1-click
scripts/dev.ps1 (Windows, PowerShell):

Crea venv Python, instala requirements.txt.

Inicializa Alembic si hace falta; upgrade head; corre seed.

npm i en frontend; levanta vite con proxy a :8000.

Levanta backend con uvicorn app.__init__:app --reload --port 8000.

scripts/dev.sh (Linux/Mac, bash): idem.

scripts/build.ps1|sh:

vite build; copia dist/ a backend/app/static y configura FastAPI para servir.

Sin Docker necesario. Si querés Docker, incluí docker-compose.yml (FastAPI + Postgres + pgadmin + Vite proxy), pero que no sea obligatorio.

8) Calidad
Linter: ruff (py) y ESLint+Prettier (ts).

Pre-commit hooks (opcional).

Tests:

Back (pytest): test_no_superposicion_vigencias.

Front (Vitest+RTL): “crear proveedor → aparece en listado”.

9) README (obligatorio y claro)
Debe cubrir:

Requisitos (Python 3.11+, Node 20+).

Cómo correr local (Windows y Linux) con un solo comando.

Variables de entorno (opcional): DATABASE_URL, JWT_SECRET, PORTS.

Rutas de API + roles.

Capturas: dashboard, proveedores flow, wizard de certificación.

Troubleshooting (puertos, permisos de archivos, etc.).

10) Entregables
Repo completo listo para clonar.

Todo lo anterior funcionando out-of-the-box:

./scripts/dev.ps1 (Windows) o ./scripts/dev.sh (Linux/Mac) → abre:

Front en http://localhost:5173 (auto proxy a /api).

Back en http://localhost:8000 (docs en /docs).

Login con admin@test.com / admin.

Crear proveedor → redirect y aparece en lista.

Crear fábrica desde proveedor → aparece en pestaña.

Producto con OdC creatable.

Wizard certificación: subir/descargar cada ítem, ver chips.

Dashboard con KPIs, listas y serie 12 meses.

11) Autochequeos obligatorios (CI local simple)
Al levantar el script dev:

Crear DB si no existe.

alembic upgrade head sin error.

Hacer GET /api/odc → contiene IRAM/TÜV/Lenor.

Test mini (“crear proveedor” vía API) y assert en listado.

Log de “todo ok” con URLs.

12) Estilo UI
Paleta “GoldCert”: oro/dorado + gris oscuro/negro, tipografía sistema, cards con sombras suaves, layout con header + nav y secciones (inspirado en tu HTML). No copiar código tal cual; reinterpretar con Tailwind y shadcn/ui. Fronthtml_grok4


## Base de datos

1. Instalar dependencias backend:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Aplicar la migración inicial:
   ```bash
   alembic -c backend/alembic.ini upgrade head
   ```
3. Cargar los datos de ejemplo:
   ```bash
   python -m backend.seed
   ```

La base usa SQLite por defecto (`sqlite:///./goldcert.db`). Si la variable de entorno `DATABASE_URL` está definida, se usará esa conexión.

## Backend API

1. Install dependencies and apply migrations:
   ```bash
   pip install -r backend/requirements.txt
   alembic -c backend/alembic.ini upgrade head
   python -m backend.seed
   ```
2. Start the server:
   ```bash
   uvicorn backend.app:app --reload --port 8000
   ```
3. Docs available at `http://localhost:8000/docs`.
