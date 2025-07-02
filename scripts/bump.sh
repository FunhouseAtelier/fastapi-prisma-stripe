#!/bin/bash
source .venv/bin/activate

VERSION_FILE="VERSION"
INIT_FILE="app/__init__.py"
PACKAGE_FILE="package.json"

if [ ! -f "$VERSION_FILE" ]; then
  echo "❌ VERSION file not found."
  exit 1
fi

if [ ! -f "$INIT_FILE" ]; then
  echo "❌ $INIT_FILE not found."
  exit 1
fi

if [ ! -f "$PACKAGE_FILE" ]; then
  echo "❌ $PACKAGE_FILE not found. Run: npm init -y"
  exit 1
fi

current_version=$(cat "$VERSION_FILE")
IFS='.' read -r major minor patch <<< "$current_version"

case "$1" in
  patch)
    ((patch++))
    ;;
  minor)
    ((minor++))
    patch=0
    ;;
  major)
    ((major++))
    minor=0
    patch=0
    ;;
  *)
    echo "❌ Usage: ./bump.sh [patch|minor|major]"
    exit 1
    ;;
esac

new_version="${major}.${minor}.${patch}"
echo "$new_version" > "$VERSION_FILE"

# Update __version__ in app/__init__.py
sed -i "s/^__version__ = \".*\"/__version__ = \"$new_version\"/" "$INIT_FILE"

# Update version in package.json
jq --arg v "$new_version" '.version = $v' "$PACKAGE_FILE" > "$PACKAGE_FILE.tmp" && mv "$PACKAGE_FILE.tmp" "$PACKAGE_FILE"

echo "✅ Version bumped: $current_version → $new_version"
echo "🔁 Updated $INIT_FILE"
echo "🔁 Updated $PACKAGE_FILE"
