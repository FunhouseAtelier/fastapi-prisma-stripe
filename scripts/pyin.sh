#!/bin/bash
source .venv/bin/activate

echo "📦 Installing production dependencies..."
pip install -r requirements.txt

echo "🧪 Installing development dependencies..."
pip install -r requirements.dev.txt

echo "✅ All dependencies installed."
