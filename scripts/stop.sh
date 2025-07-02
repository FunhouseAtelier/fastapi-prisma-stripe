#!/bin/bash
source .venv/bin/activate
echo "🛑 Stopping FastAPI server..."
pkill -f "uvicorn app.main:app"
