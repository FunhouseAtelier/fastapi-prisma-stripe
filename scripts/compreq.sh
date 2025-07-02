#!/bin/bash
source .venv/bin/activate

echo "🔧 Compiling production requirements..."
pip-compile requirements.in -o requirements.txt

echo "🔧 Compiling development requirements..."
pip-compile requirements.dev.in -o requirements.dev.txt

echo "✅ Done."
