#!/usr/bin/env bash

# Usage: ./scripts/delmod.sh <target_model>
# Example: ./scripts/delmod.sh lineitem

set -e

TARGET="$1"

if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 <target_model>"
  exit 1
fi

echo "🗑  Deleting all files/folders related to model: $TARGET"

paths=(
  "app/routes/view/${TARGET}.py"
  "app/schemas/${TARGET}.py"
  "app/utils/db/${TARGET}.py"
  "app/utils/validators/${TARGET}.py"
  "app/templates/${TARGET}/"
)

for path in "${paths[@]}"; do
  if [[ -e "$path" ]]; then
    rm -rf "$path"
    echo "✅ Deleted: $path"
  else
    echo "⚠️  Not found: $path"
  fi
done

echo
echo "🧹 Cleanup complete. Files for model '$TARGET' removed."
