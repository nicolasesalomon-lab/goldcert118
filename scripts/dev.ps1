Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

if (-not (Test-Path '.venv')) {
    python -m venv .venv
}
. .\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
ruff check backend

try {
    alembic -c backend/alembic.ini upgrade head
} catch {
    alembic -c backend/alembic.ini revision --autogenerate -m 'init'
    alembic -c backend/alembic.ini upgrade head
}

python -m backend.seed

$api = Start-Process uvicorn -ArgumentList 'backend.app:app','--reload','--port','8000' -NoNewWindow -PassThru
Start-Sleep -Seconds 2

$odc = Invoke-RestMethod http://localhost:8000/api/odc
$odcJson = $odc | ConvertTo-Json
foreach ($n in 'IRAM','TÜV','Lenor') {
    if ($odcJson -notmatch $n) { throw "GET /api/odc missing $n" }
}

$login = Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/auth/login -Body '{"email":"admin@test.com","password":"admin"}' -ContentType 'application/json'
if (-not $login.access_token) { throw 'POST /api/auth/login failed' }

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

