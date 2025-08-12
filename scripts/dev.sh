#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

PYTHON=${PYTHON:-python3}
VENV=.venv
if [ ! -d "$VENV" ]; then
  $PYTHON -m venv "$VENV"
fi
source "$VENV/bin/activate"
pip install -r backend/requirements.txt
ruff check backend

cd backend
alembic upgrade head || { alembic revision --autogenerate -m "init"; alembic upgrade head; }
$PYTHON -m backend.seed
uvicorn app:app --reload --port 8000 &
API_PID=$!
sleep 2
curl -sf http://localhost:8000/api/odc | grep -E 'IRAM|TÜV|Lenor' >/dev/null && echo "GET /api/odc OK"
curl -sf -X POST http://localhost:8000/api/auth/login -H 'Content-Type: application/json' -d '{"email":"admin@test.com","password":"admin"}' | grep access_token >/dev/null && echo "POST /api/auth/login OK"
cd ..

cd frontend
npm install
npm run lint

echo "Front http://localhost:5173"
echo "API docs http://localhost:8000/docs"
trap 'kill $API_PID' EXIT
npm run dev
