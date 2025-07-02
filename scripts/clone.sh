#!/bin/bash
# scripts/clone.sh

# Usage: ./scripts/clone.sh associate lineitem

set -e

SOURCE="$1"
TARGET="$2"

if [[ -z "$SOURCE" || -z "$TARGET" ]]; then
  echo "Usage: $0 <source_model> <target_model>"
  exit 1
fi

CAP_SOURCE="$(tr '[:lower:]' '[:upper:]' <<< ${SOURCE:0:1})${SOURCE:1}"
CAP_TARGET="$(tr '[:lower:]' '[:upper:]' <<< ${TARGET:0:1})${TARGET:1}"

echo "Cloning model: $SOURCE → $TARGET"
echo "              $CAP_SOURCE → $CAP_TARGET"
echo

# Paths to copy
paths=(
  "app/routes/view/${SOURCE}.py"
  "app/schemas/${SOURCE}.py"
  "app/utils/db/${SOURCE}.py"
  "app/utils/validators/${SOURCE}.py"
  "app/templates/${SOURCE}/"
)

for path in "${paths[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "⚠️  Skipping missing path: $path"
    continue
  fi

  target_path="${path//$SOURCE/$TARGET}"

  if [[ -e "$target_path" ]]; then
    echo "❌ Target already exists: $target_path"
    continue
  fi

  # Copy files/directories
  if [[ -d "$path" ]]; then
    cp -r "$path" "$target_path"
  else
    mkdir -p "$(dirname "$target_path")"
    cp "$path" "$target_path"
  fi

  echo "🛠  Rewriting contents in $target_path..."

  # Substitutions (in order of specificity)
  find "$target_path" -type f -print0 | while IFS= read -r -d '' file; do
    sed -i \
      -e "s/get_all_${SOURCE}/get_all_${TARGET}/g" \
      -e "s/get_new_${SOURCE}/get_new_${TARGET}/g" \
      -e "s/get_edit_${SOURCE}/get_edit_${TARGET}/g" \
      -e "s/get_delete_${SOURCE}/get_delete_${TARGET}/g" \
      -e "s/get_${SOURCE}/get_${TARGET}/g" \
      -e "s/post_new_${SOURCE}/post_new_${TARGET}/g" \
      -e "s/post_edit_${SOURCE}/post_edit_${TARGET}/g" \
      -e "s/post_delete_${SOURCE}/post_delete_${TARGET}/g" \
      -e "s/create_${SOURCE}/create_${TARGET}/g" \
      -e "s/read_all_${SOURCE}s/read_all_${TARGET}s/g" \
      -e "s/read_one_${SOURCE}/read_one_${TARGET}/g" \
      -e "s/update_${SOURCE}/update_${TARGET}/g" \
      -e "s/delete_${SOURCE}/delete_${TARGET}/g" \
      -e "s/${SOURCE}/${TARGET}/g" \
      -e "s/${CAP_SOURCE}/${CAP_TARGET}/g" \
      "$file"
  done

  echo "✅ Cloned and patched: $target_path"
done

echo
echo "🎉 Clone complete. Review and edit field names manually in $TARGET files."

