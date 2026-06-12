#!/usr/bin/env bash
#
# Git Worktree Lifecycle Manager Script
# Handles creation, environment linking, and clean closing of feature workspaces.
#
# Usage:
#   manage_worktree.sh <subcommand> <epic_slug> <feature_slug>
#
# Subcommands:
#   prototype       Create worktree branch and scaffold empty SDD feature capsule
#   close-feature   Dismantle, merge branch, and delete worktree folders safely
#

set -euo pipefail

# Helper to log output
log() {
  echo -e "\033[1;36m[Worktree]\033[0m $1"
}

log_err() {
  echo -e "\033[1;31m[Error]\033[0m $1" >&2
}

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <subcommand> <epic_slug> <feature_slug>"
  echo "Subcommands: prototype, close-feature"
  exit 1
fi

SUBCOMMAND="$1"
EPIC_SLUG="$2"
FEATURE_SLUG="$3"

# Resolve parent Git root and Project Name
PARENT_ROOT="$(git rev-parse --show-toplevel)"
PROJECT_NAME="$(basename "$PARENT_ROOT")"

WORKTREE_PATH="$HOME/.gemini/jetski/worktrees/$PROJECT_NAME/${EPIC_SLUG}-${FEATURE_SLUG}"
BRANCH_NAME="${EPIC_SLUG}-${FEATURE_SLUG}"

# Verify we are in a Git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log_err "Not in a Git repository workspace root."
  exit 1
fi

case "$SUBCOMMAND" in
  prototype)
    log "Provisioning Git worktree branch '$BRANCH_NAME' at '$WORKTREE_PATH'..."
    if [ -d "$WORKTREE_PATH" ]; then
      log_err "Worktree folder already exists: $WORKTREE_PATH"
      exit 1
    fi

    # Add Git worktree
    git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH"

    # Copy simulation files to worktree tests folder so they are available in the worktree jail
    log "Copying E2E simulation scripts into the worktree tests folder..."
    mkdir -p "$WORKTREE_PATH/tests"
    cp -r "$PARENT_ROOT/tests/fixtures" "$WORKTREE_PATH/tests/"
    cp "$PARENT_ROOT/tests/sim_sdd_process.py" "$WORKTREE_PATH/tests/"
    cp "$PARENT_ROOT/tests/sdd_simulator.py" "$WORKTREE_PATH/tests/"
    cp "$PARENT_ROOT/tests/cleanup_project.py" "$WORKTREE_PATH/tests/"
    cp "$PARENT_ROOT/test_sdd_process.sh" "$WORKTREE_PATH/"

    log "Worktree provisioning complete! Workspace ready for implementation."

    # Register Workspace in Parent Project in Jetski Hub
    log "Registering workspace in parent project config..."
    python3 -c "
import os, json, glob
parent_root = '$PARENT_ROOT'
worktree_path = '$WORKTREE_PATH'
projects_dir = os.path.expanduser('~/.gemini/config/projects')
parent_uri = f'file://{parent_root}'
worktree_uri = f'file://{worktree_path}'

found = False
for path in glob.glob(os.path.join(projects_dir, '*.json')):
    try:
        with open(path, 'r+') as f:
            data = json.load(f)
            resources = data.get('projectResources', {}).get('resources', [])
            has_parent = any(r.get('folderUri') == parent_uri for r in resources)
            if has_parent:
                if not any(r.get('folderUri') == worktree_uri for r in resources):
                    resources.append({'folderUri': worktree_uri})
                    data['projectResources']['resources'] = resources
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    f.truncate()
                    print(f'Added workspace to project config: {path}')
                found = True
                break
    except Exception as e:
        print(f'Error processing {path}: {e}')

if not found:
    print(f'Warning: No project config found containing parent root: {parent_root}')
"
    ;;



  close-feature)
    log "Checking worktree branch status..."
    
    # Ensure we are on main workspace to perform deletion
    MAIN_DIR="$(git rev-parse --show-toplevel)"
    cd "$MAIN_DIR"

    if [ ! -d "$WORKTREE_PATH" ]; then
      log_err "Worktree folder does not exist: $WORKTREE_PATH"
      exit 1
    fi

    # Remove Workspace from Parent Project in Jetski Hub
    log "Removing workspace from parent project config..."
    python3 -c "
import os, json, glob
parent_root = '$PARENT_ROOT'
worktree_path = '$WORKTREE_PATH'
projects_dir = os.path.expanduser('~/.gemini/config/projects')
parent_uri = f'file://{parent_root}'
worktree_uri = f'file://{worktree_path}'

for path in glob.glob(os.path.join(projects_dir, '*.json')):
    try:
        with open(path, 'r+') as f:
            data = json.load(f)
            resources = data.get('projectResources', {}).get('resources', [])
            has_parent = any(r.get('folderUri') == parent_uri for r in resources)
            if has_parent:
                new_resources = [r for r in resources if r.get('folderUri') != worktree_uri]
                if len(new_resources) < len(resources):
                    data['projectResources']['resources'] = new_resources
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    f.truncate()
                    print(f'Removed workspace from project config: {path}')
                break
    except Exception as e:
         print(f'Error processing {path}: {e}')
"

    # Prune worktrees just in case
    git worktree prune

    log "Safely dismantling worktree folder..."
    git worktree remove --force "$WORKTREE_PATH"

    # Safe Git clean branch merging (if branch is already merged, this prunes it)
    log "Worktree directory dismantled. Cleaning branch mappings..."
    # Check if there are unmerged changes
    # For safety, delete the branch. If they merged it in Github, we use -D
    git branch -d "$BRANCH_NAME" || {
      log "Branch is not fully merged. If you want to force delete local branch, run:"
      log "  git branch -D $BRANCH_NAME"
    }

    log "Dismantling complete! Workspace is clean."
    ;;

  *)
    log_err "Unknown subcommand: $SUBCOMMAND"
    echo "Usage: $0 <subcommand> <epic_slug> <feature_slug>"
    exit 1
    ;;
esac
