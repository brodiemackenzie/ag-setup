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

# 4. Stage assets to root-level discovery paths as first-class citizens
echo "[Info] Copying plugin assets directly to native discovery paths..."

# Copy Agents
if [ -d "$SOURCE_PLUGIN/agents" ]; then
  mkdir -p "$TARGET_PROJECT/.agents/agents"
  cp -f "$SOURCE_PLUGIN/agents/"*.json "$TARGET_PROJECT/.agents/agents/" 2>/dev/null || true
fi

# Copy Skills (Playbooks)
if [ -d "$SOURCE_PLUGIN/skills" ]; then
  mkdir -p "$TARGET_PROJECT/.agents/skills"
  cp -rf "$SOURCE_PLUGIN/skills/"* "$TARGET_PROJECT/.agents/skills/" 2>/dev/null || true
fi

# Copy Rules
if [ -d "$SOURCE_PLUGIN/rules" ]; then
  mkdir -p "$TARGET_PROJECT/.agents/rules"
  cp -f "$SOURCE_PLUGIN/rules/"*.md "$TARGET_PROJECT/.agents/rules/" 2>/dev/null || true
fi

# Copy Scripts
if [ -d "$SOURCE_PLUGIN/scripts" ]; then
  mkdir -p "$TARGET_PROJECT/.agents/scripts"
  cp -f "$SOURCE_PLUGIN/scripts/"* "$TARGET_PROJECT/.agents/scripts/" 2>/dev/null || true
fi

# Copy Commands
if [ -d "$SOURCE_PLUGIN/commands" ]; then
  mkdir -p "$TARGET_PROJECT/.agents/commands"
  cp -f "$SOURCE_PLUGIN/commands/"*.toml "$TARGET_PROJECT/.agents/commands/" 2>/dev/null || true
fi

echo "[Success] Plugin $PLUGIN_NAME successfully staged to first-class paths under $TARGET_PROJECT/.agents/"
echo "Note: It is highly recommended to commit your target project's .agents/ directory to track these changes in Git."
