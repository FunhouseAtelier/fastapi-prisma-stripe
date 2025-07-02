#!/usr/bin/env bash
source .venv/bin/activate

echo "🧪 Running validation checks..."

./scripts/lint.sh || exit 1
./scripts/fmt.sh || exit 1
./scripts/compreq.sh || exit 1

echo "✅ All checks passed."
