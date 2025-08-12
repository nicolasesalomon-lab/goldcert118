Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

if (-not (Test-Path '.venv')) {
    python -m venv .venv
}
. .\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
ruff check backend

alembic -c backend/alembic.ini upgrade head 2>&1 | Out-Host
if ($LASTEXITCODE -ne 0) {
    alembic -c backend/alembic.ini revision --autogenerate -m 'init' 2>&1 | Out-Host
    alembic -c backend/alembic.ini upgrade head 2>&1 | Out-Host
}
python -m backend.seed
$api = Start-Process uvicorn -ArgumentList 'backend.app:app','--reload','--port','8000' -NoNewWindow -PassThru
Start-Sleep -Seconds 2
Invoke-RestMethod http://localhost:8000/api/odc | Out-Null
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/auth/login -Body '{"email":"admin@test.com","password":"admin"}' -ContentType 'application/json' | Out-Null

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
