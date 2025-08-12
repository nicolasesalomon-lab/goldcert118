#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
alembic -c backend/alembic.ini upgrade head
python backend/manage.py
cd frontend && npm install && npm run dev &
cd ..
uvicorn backend.app.__init__:app --reload --port 8000
