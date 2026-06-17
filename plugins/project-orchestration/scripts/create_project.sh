#!/usr/bin/env bash
# Script to create a project directory, initialize Git, and register in Jetski Hub.
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <project-name> [project-path]" >&2
    exit 1
fi

PROJECT_NAME="$1"
PROJECT_PATH="${2:-}"

# Default path to ~/projects/<name>
if [ -z "$PROJECT_PATH" ]; then
    PROJECT_PATH="$HOME/projects/$PROJECT_NAME"
fi

# Expand ~ if present
if [[ "$PROJECT_PATH" =~ ^~ ]]; then
    PROJECT_PATH="${PROJECT_PATH/#\~/$HOME}"
fi

# Ensure it is absolute
if [[ ! "$PROJECT_PATH" =~ ^/ ]]; then
    echo "Error: Project path must be absolute (start with / or ~)" >&2
    exit 1
fi

echo "Creating project '$PROJECT_NAME' at '$PROJECT_PATH'..."

# 1. Verify directory doesn't exist
if [ -d "$PROJECT_PATH" ]; then
    echo "Error: Directory already exists at '$PROJECT_PATH'" >&2
    exit 1
fi

# 2. Create directory
if ! mkdir -p "$PROJECT_PATH"; then
    echo "Error: Failed to create directory '$PROJECT_PATH'" >&2
    exit 1
fi

# 3. Initialize Git
if ! git init "$PROJECT_PATH" > /dev/null; then
    echo "Error: Failed to initialize Git repository in '$PROJECT_PATH'" >&2
    exit 1
fi
echo "Initialized empty Git repository."

# 4. Provision UUID
if command -v uuidgen >/dev/null 2>&1; then
  UUID=$(uuidgen | tr '[:upper:]' '[:lower:]')
else
  UUID=$(cat /proc/sys/kernel/random/uuid)
fi

# 5. Register in Jetski Hub
HUB_CONFIG_DIR="$HOME/.gemini/config/projects"
if ! mkdir -p "$HUB_CONFIG_DIR"; then
    echo "Error: Failed to create Hub config directory '$HUB_CONFIG_DIR'" >&2
    exit 1
fi

CONFIG_FILE="$HUB_CONFIG_DIR/${UUID}.json"

# Write Hub configuration with precise structure
cat <<EOF > "$CONFIG_FILE"
{
  "id": "$UUID",
  "name": "$PROJECT_NAME",
  "projectResources": {
    "resources": [
      {
        "gitFolder": {
          "folderUri": "file://$PROJECT_PATH",
          "allowWrite": true
        }
      }
    ]
  },
  "permissionGrants": {
    "permissionGrants": {
      "allow": [
        "command(git)"
      ],
      "deny": []
    }
  }
}
EOF

echo "Registered project in Jetski Hub: $CONFIG_FILE"
echo "Project created successfully."
