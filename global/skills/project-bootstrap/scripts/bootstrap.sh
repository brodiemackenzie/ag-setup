#!/usr/bin/env bash
#
# Project Bootstrap Script
# Automates greenfield repository provisioning, boilerplate cleaning, remote binds,
# and safe copying of process templates without git metadata duplication.
#
# Usage:
#   bootstrap.sh <project_name> <github_repo_url> [--process <process_slug>] [--scaffold <framework>]
#

set -euo pipefail

# Helper to log output
log() {
  echo -e "\033[1;32m[Bootstrap]\033[0m $1"
}

log_err() {
  echo -e "\033[1;31m[Error]\033[0m $1" >&2
}

# Print usage
usage() {
  echo "Usage: $0 <project_name> [<github_repo_url>] [--git-remote <url>] [--process <process_slug>]"
  echo ""
  echo "Arguments:"
  echo "  project_name     Name of the project directory (created under ~/projects/)"
  echo "  github_repo_url  The GitHub remote repository URL to bind (optional)"
  echo ""
  echo "Options:"
  echo "  --git-remote     Alternative way to specify GitHub remote URL"
  echo "  --process        Process template to copy (default: sdd-anchored)"
  exit 1
}

PROJECT_NAME=""
GITHUB_REPO_URL=""
PROCESS_SLUG="sdd-anchored"

# Parse arguments
if [ "$#" -lt 1 ]; then
  usage
fi

PROJECT_NAME="$1"
shift

# Check if next arg is positional GITHUB_REPO_URL (doesn't start with --)
if [ "$#" -gt 0 ] && [[ ! "$1" =~ ^-- ]]; then
  GITHUB_REPO_URL="$1"
  shift
fi

while [ "$#" -gt 0 ]; do
  case "$1" in
    --git-remote)
      GITHUB_REPO_URL="$2"
      shift 2
      ;;
    --process)
      PROCESS_SLUG="$2"
      shift 2
      ;;
    *)
      log_err "Unknown parameter: $1"
      usage
      ;;
  esac
done

if [ -z "$PROJECT_NAME" ]; then
  log_err "Project Name is required."
  usage
fi

if [[ "$PROJECT_NAME" =~ ^[./] ]]; then
  PROJECT_DIR="$(readlink -f "$PROJECT_NAME")"
else
  PROJECT_DIR="$HOME/projects/$PROJECT_NAME"
fi
TEMPLATES_DIR="${GEMINI_WORKSPACE_DIR:-${GEMINI_TEMPLATES_DIR:-$HOME/.gemini/config/workspace}}/templates/$PROCESS_SLUG"

# 1. Validation Checks
if [ -d "$PROJECT_DIR" ]; then
  log_err "Directory already exists: $PROJECT_DIR"
  exit 1
fi

if [ ! -d "$TEMPLATES_DIR" ]; then
  log_err "Process template not found: $TEMPLATES_DIR"
  log_err "Please ensure your workspace templates are symlinked to ~/.gemini/config/workspace/ first:"
  log_err "  mkdir -p ~/.gemini/config/"
  log_err "  ln -s ~/projects/ag-setup/workspace/ ~/.gemini/config/workspace"
  exit 1
fi

# 2. Create Workspace Directory & Init Git
log "Creating project folder at $PROJECT_DIR..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

log "Initializing Git repository..."
git init


# 3. Bind Git Remote Origin
if [ -n "$GITHUB_REPO_URL" ] && [ "$GITHUB_REPO_URL" != "none" ]; then
  log "Configuring remote Git origin to $GITHUB_REPO_URL..."
  git remote add origin "$GITHUB_REPO_URL"
else
  log "Skipping remote Git origin configuration (none provided)."
fi

# 4. Safe Template RSync copying without git history metadata duplication
log "Safely copying $PROCESS_SLUG process templates to .agents/..."
mkdir -p .agents
rsync -av --exclude='.git' "$TEMPLATES_DIR/_agents/" ".agents/"

# 5. Setup GitIgnore additions
log "Updating .gitignore to exclude local agent telemetry and worktree files..."
cat << 'EOF' >> .gitignore

# Jetski / Antigravity Custom Folders
.agents/history/checkpoint.md
.docs_build/
worktrees/
spec_change_proposal.md
EOF

log "Initialization complete! Project scaffolded successfully at $PROJECT_DIR."

# 6. Open the new workspace in a new window (JetSki IDE only)
JETSKI_CLI="/opt/jetski-ide/bin/jetski"
if [ -f "$JETSKI_CLI" ]; then
  log "Launching new JetSki IDE window for workspace: $PROJECT_DIR..."
  "$JETSKI_CLI" -n "$PROJECT_DIR"
else
  log "Note: JetSki IDE command-line launcher not found. Please open $PROJECT_DIR manually."
fi

log "Next steps: Switch to your new JetSki window, open a new chat, and start the SDD discovery process!"
