Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

if (-not (Test-Path '.venv')) {
    python -m venv .venv
}
. .\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
ruff check backend

Set-Location backend
try {
    alembic upgrade head
} catch {
    alembic revision --autogenerate -m 'init'
    alembic upgrade head
}
python -m backend.seed
$api = Start-Process uvicorn -ArgumentList 'app:app','--reload','--port','8000' -NoNewWindow -PassThru
Start-Sleep -Seconds 2
Invoke-RestMethod http://localhost:8000/api/odc | Out-Null
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/auth/login -Body '{"email":"admin@test.com","password":"admin"}' -ContentType 'application/json' | Out-Null
Set-Location ..

Set-Location frontend
npm install
npm run lint
Write-Host 'Front http://localhost:5173'
Write-Host 'API docs http://localhost:8000/docs'
try {
    npm run dev
} finally {
    Stop-Process $api.Id
}
