#!/bin/bash
# scripts/clean.sh
# 🧹 Clean up Python, build, and editor junk files

echo "🧹 Cleaning workspace..."

# Remove Python cache files
find . -type d -name '__pycache__' -exec rm -rf {} +
find . -type f -name '*.pyc' -delete
find . -type f -name '*.pyo' -delete

# Remove common tooling caches
rm -rf .mypy_cache
rm -rf .pytest_cache
rm -rf .ruff_cache
rm -rf .venv
rm -rf .envrc
rm -rf .DS_Store

# Remove build artifacts
rm -rf dist
rm -rf build
rm -rf *.egg-info
rm -rf htmlcov

# Remove editor-specific temp files
rm -rf .vscode/.ropeproject

# Optional: clean Prisma-generated client (use with care)
# rm -rf prisma_client

echo "✅ Clean complete."
