Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

npm install --prefix frontend
npm run build --prefix frontend
Remove-Item -Recurse -Force backend/app/static/*
Copy-Item -Recurse -Force frontend/dist/* backend/app/static/
Write-Host 'Build complete'
