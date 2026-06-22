#!/usr/bin/env bash
# local plugin-copy executor
set -euo pipefail

# Argument defaults
SOURCE_RAW=""
TARGET_RAW=""
FORCE=false

# Simple argument parser
while [[ $# -gt 0 ]]; do
  case "$1" in
    --source|-s)
      SOURCE_RAW="$2"
      shift 2
      ;;
    --target|-t)
      TARGET_RAW="$2"
      shift 2
      ;;
    --force|-f)
      FORCE=true
      shift
      ;;
    *)
      echo "[Error] Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

# Expand tilde (~) and resolve paths helper
expand_path() {
  local path="$1"
  if [[ "$path" == ~* ]]; then
    echo "${path/#\~/$HOME}"
  elif [[ "$path" == /* ]]; then
    echo "$path"
  else
    echo "$(pwd)/$path"
  fi
}

# 1. Resolve target project directory (default to current directory)
if [ -z "$TARGET_RAW" ]; then
  TARGET_PROJECT="$(pwd)"
else
  TARGET_PROJECT=$(expand_path "$TARGET_RAW")
fi
TARGET_PROJECT=$(realpath "$TARGET_PROJECT")

# 2. Resolve source plugin directory (must be provided)
if [ -z "$SOURCE_RAW" ]; then
  echo "[Error] Missing required parameter: --source or -s" >&2
  exit 1
fi

SOURCE_PLUGIN=$(expand_path "$SOURCE_RAW")
SOURCE_PLUGIN=$(realpath "$SOURCE_PLUGIN")

# Validate source exists
if [ ! -d "$SOURCE_PLUGIN" ]; then
  echo "[Error] Source directory does not exist: $SOURCE_PLUGIN" >&2
  exit 1
fi

# 3. Validate source is a plugin (contains plugin.json or gemini-extension.json)
if [ ! -f "$SOURCE_PLUGIN/plugin.json" ] && [ ! -f "$SOURCE_PLUGIN/gemini-extension.json" ]; then
  echo "[Error] Source folder does not contain a valid plugin manifest (plugin.json or gemini-extension.json): $SOURCE_PLUGIN" >&2
  exit 1
fi

PLUGIN_NAME=$(basename "$SOURCE_PLUGIN")
DESTINATION_DIR="$TARGET_PROJECT/.agents/plugins/$PLUGIN_NAME"

# 4. Safety Overwrite Check
if [ -d "$DESTINATION_DIR" ]; then
  if [ "$FORCE" = false ]; then
    echo "[Blocked] Target plugin directory already exists: $DESTINATION_DIR" >&2
    echo "To overwrite the existing local plugin and apply updates, re-run the command with the --force or -f flag." >&2
    exit 2
  else
    echo "[Info] Target folder exists and --force is enabled. Overwriting existing plugin..."
    rm -rf "$DESTINATION_DIR"
  fi
fi

# 5. Execute copy
echo "[Info] Copying plugin from $SOURCE_PLUGIN to $DESTINATION_DIR..."
mkdir -p "$DESTINATION_DIR"

# Copy files excluding .git metadata and temporary checkouts
rsync -av --exclude='.git' --exclude='node_modules' "$SOURCE_PLUGIN/" "$DESTINATION_DIR/"

echo "[Success] Local plugin successfully staged!"
echo "Target path: $DESTINATION_DIR"
echo "Note: It is highly recommended to commit your target project's .agents/ directory to track these changes in Git."
