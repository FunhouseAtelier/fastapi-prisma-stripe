#!/bin/bash
source .venv/bin/activate
echo "🚀 Launching FastAPI server..."
uvicorn app.main:app --reload --port 8080 --forwarded-allow-ips '*'
