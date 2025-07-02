#!/usr/bin/env bash
echo "🔎 Linting all code..."

# Python linting
ruff check app/

# Template linting
djlint app/templates/

echo "✅ Linting finished. Fix any issues above."
