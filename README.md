# GoldCert 2.0 (minimal demo)

## Requisitos
- Python 3.11+
- Node 20+

## Desarrollo

En Linux/Mac:
```bash
./scripts/dev.sh
```

En Windows PowerShell:
```powershell
./scripts/dev.ps1
```

Los scripts instalan dependencias, migran la base SQLite, ejecutan seeds y levantan backend (http://localhost:8000) y frontend (http://localhost:5173) con proxy /api.

Usuario inicial: `admin@test.com` / `admin`.

## Tests

Backend:
```bash
pytest backend/tests
```

Frontend:
```bash
cd frontend
npm test
```
