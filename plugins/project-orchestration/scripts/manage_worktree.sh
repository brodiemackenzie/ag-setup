#!/usr/bin/env bash
# Generic Git Worktree Lifecycle Manager Script
# Handles creation, Hub registration, syncing, diffing, merging, and clean closing of workspaces.
set -euo pipefail

usage() {
  echo "Git Worktree Lifecycle Manager"
  echo "Usage: $0 <action> [branch-name] [worktree-path] [--force]"
  echo ""
  echo "Actions:"
  echo "  create    Create a new Git worktree and register it in Jetski Hub."
  echo "  sync      Sync the worktree branch by merging the parent branch into it."
  echo "  diff      Show changes in the feature branch compared to the parent branch."
  echo "  merge     Merge the feature branch into the parent branch."
  echo "  close     Dismantle the worktree and clean up branches (safe by default)."
  echo "  finish    Combined workflow: sync, diff, merge, and close."
  echo "  list      List all active worktrees and their Hub registration status."
  echo "  help      Print this usage manual."
  exit 1
}

if [ "$#" -lt 1 ]; then
  usage
fi

ACTION="$1"
BRANCH_NAME="${2:-}"
WORKTREE_PATH="${3:-}"

# Parse optional arguments/flags
FORCE=false
if [[ "$WORKTREE_PATH" =~ ^- ]]; then
  if [ "$WORKTREE_PATH" = "--force" ] || [ "$WORKTREE_PATH" = "-f" ]; then
    FORCE=true
  fi
  WORKTREE_PATH=""
fi

for arg in "$@"; do
  if [ "$arg" = "--force" ] || [ "$arg" = "-f" ]; then
    FORCE=true
  fi
done


# Help action
if [ "$ACTION" = "help" ] || [ "$ACTION" = "--help" ] || [ "$ACTION" = "-h" ]; then
  usage
fi

# Resolve parent Git root and Project Name
PARENT_ROOT="$(git rev-parse --show-toplevel)"
PROJECT_NAME="$(basename "$PARENT_ROOT")"

# Actions that don't require a branch name
if [ "$ACTION" != "list" ]; then
  if [ -z "$BRANCH_NAME" ]; then
    echo "Error: branch-name is required for action '$ACTION'" >&2
    usage
  fi

  # Default worktree path under ~/.gemini/jetski/worktrees/<project>/<branch>
  if [ -z "$WORKTREE_PATH" ]; then
    WORKTREE_PATH="$HOME/.gemini/jetski/worktrees/$PROJECT_NAME/$BRANCH_NAME"
  fi

  # Expand ~ if present
  if [[ "$WORKTREE_PATH" =~ ^~ ]]; then
      WORKTREE_PATH="${WORKTREE_PATH/#\~/$HOME}"
  fi

  # Ensure worktree path is absolute
  if [[ ! "$WORKTREE_PATH" =~ ^/ ]]; then
      WORKTREE_PATH="$PARENT_ROOT/$WORKTREE_PATH"
  fi
  WORKTREE_PATH="$(readlink -f "$WORKTREE_PATH" || echo "$WORKTREE_PATH")"
fi

log() {
  echo -e "\033[1;36m[Worktree]\033[0m $1"
}

log_err() {
  echo -e "\033[1;31m[Error]\033[0m $1" >&2
}

# Get current branch of parent repo (e.g. main)
cd "$PARENT_ROOT"
CURRENT_BRANCH="$(git branch --show-current)"

case "$ACTION" in
  create)
    log "Creating Git worktree for branch '$BRANCH_NAME' at '$WORKTREE_PATH'..."
    if [ -d "$WORKTREE_PATH" ]; then
      log_err "Worktree folder already exists: $WORKTREE_PATH"
      exit 1
    fi

    # Create parent dir of worktree if it doesn't exist
    mkdir -p "$(dirname "$WORKTREE_PATH")"

    # Add Git worktree
    # If branch already exists locally, check it out. Otherwise create it.
    if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
      log "Branch '$BRANCH_NAME' already exists. Checking it out in worktree..."
      git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"
    else
      log "Creating new branch '$BRANCH_NAME' and checking out in worktree..."
      git worktree add -b "$BRANCH_NAME" "$WORKTREE_PATH"
    fi

    # Register Workspace in Jetski Hub
    log "Registering worktree as a new isolated Project in Jetski Hub..."
    HUB_CONFIG_DIR="$HOME/.gemini/config/projects"
    mkdir -p "$HUB_CONFIG_DIR"
    
    if command -v uuidgen >/dev/null 2>&1; then
      UUID=$(uuidgen | tr '[:upper:]' '[:lower:]')
    else
      UUID=$(cat /proc/sys/kernel/random/uuid)
    fi

    CONFIG_FILE="$HUB_CONFIG_DIR/${UUID}.json"

    # Write Hub configuration (enforcing write access inside worktree, denying .agents to protect rules)
    cat <<EOF > "$CONFIG_FILE"
{
  "id": "$UUID",
  "name": "$PROJECT_NAME ($BRANCH_NAME)",
  "projectResources": {
    "resources": [
      {
        "gitFolder": {
          "folderUri": "file://$WORKTREE_PATH",
          "defaultBranch": "$BRANCH_NAME",
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
      "deny": [
        "write_file($WORKTREE_PATH/.agents)"
      ]
    }
  }
}
EOF
    echo "Registered worktree in Jetski Hub: $CONFIG_FILE"
    echo "Worktree created successfully."
    ;;

  sync)
    log "Syncing worktree branch '$BRANCH_NAME' by merging parent branch '$CURRENT_BRANCH' into it..."
    if [ ! -d "$WORKTREE_PATH" ]; then
      log_err "Worktree directory does not exist: $WORKTREE_PATH"
      exit 1
    fi
    
    # Run merge inside the worktree
    if ! git -C "$WORKTREE_PATH" merge "$CURRENT_BRANCH"; then
      log_err "Conflicts detected during sync! Please open the worktree workspace and resolve them."
      exit 1
    fi
    log "Sync complete. Worktree branch '$BRANCH_NAME' is up to date with '$CURRENT_BRANCH'."
    ;;

  diff)
    log "Showing diff summary for branch '$BRANCH_NAME' compared to '$CURRENT_BRANCH'..."
    if ! git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
      log_err "Branch '$BRANCH_NAME' does not exist."
      exit 1
    fi
    
    # Show diffstat
    git diff "$CURRENT_BRANCH...$BRANCH_NAME" --stat
    
    # Show full diff
    echo -e "\n--- Full Diff ---"
    git diff "$CURRENT_BRANCH...$BRANCH_NAME"
    ;;

  merge)
    log "Merging branch '$BRANCH_NAME' into parent branch '$CURRENT_BRANCH'..."
    if [ "$CURRENT_BRANCH" = "$BRANCH_NAME" ]; then
      log_err "Cannot merge branch into itself. Switch to the target branch (e.g. main) first."
      exit 1
    fi

    log "Merging '$BRANCH_NAME' into '$CURRENT_BRANCH'..."
    if ! git merge "$BRANCH_NAME"; then
      log_err "Merge conflict detected! Please resolve conflicts manually in the parent repository."
      exit 1
    fi
    log "Merged successfully."
    ;;

  close)
    log "Closing worktree for branch '$BRANCH_NAME'..."
    
    # Check for uncommitted changes in worktree before removing (safety check)
    if [ -d "$WORKTREE_PATH" ]; then
      if [ -n "$(git -C "$WORKTREE_PATH" status --porcelain)" ] && [ "$FORCE" = false ]; then
        log_err "Worktree at '$WORKTREE_PATH' has uncommitted changes!"
        log_err "Commit your changes or run with --force to discard them."
        exit 1
      fi
    fi

    # Remove Workspace from Jetski Hub
    log "Deleting project config from Jetski Hub..."
    HUB_CONFIG_DIR="$HOME/.gemini/config/projects"
    
    found=false
    for file in "$HUB_CONFIG_DIR"/*.json; do
      if [ -f "$file" ]; then
        if grep -q "file://$WORKTREE_PATH" "$file"; then
          log "Removing Hub config: $file"
          rm "$file"
          found=true
          break
        fi
      fi
    done
    if [ "$found" = false ]; then
      log "No Hub config found matching worktree path '$WORKTREE_PATH'"
    fi

    # Prune worktrees
    git worktree prune

    # Safely dismantle worktree folder
    if [ -d "$WORKTREE_PATH" ]; then
      log "Removing worktree directory..."
      git worktree remove --force "$WORKTREE_PATH"
    fi

    # Delete local branch if merged
    log "Cleaning up local branch '$BRANCH_NAME'..."
    if git branch -d "$BRANCH_NAME" 2>/dev/null; then
      log "Branch '$BRANCH_NAME' deleted successfully."
    else
      if [ "$FORCE" = true ]; then
        git branch -D "$BRANCH_NAME"
        log "Force deleted branch '$BRANCH_NAME'."
      else
        log "Branch '$BRANCH_NAME' is not fully merged yet."
        log "If you want to force delete it, run: /worktree close $BRANCH_NAME --force"
      fi
    fi

    log "Worktree close complete."
    ;;

  finish)
    log "Integrating and closing worktree branch '$BRANCH_NAME'..."
    
    # 1. Sync
    log "Step 1/4: Syncing parent changes into worktree..."
    if ! "$0" sync "$BRANCH_NAME" "$WORKTREE_PATH"; then
      log_err "Sync failed! Resolve conflicts inside the worktree before running finish."
      exit 1
    fi
    
    # 2. Diff
    log "Step 2/4: Previewing changes stat:"
    git diff "$CURRENT_BRANCH...$BRANCH_NAME" --stat
    
    # 3. Merge
    log "Step 3/4: Merging feature branch into parent..."
    if ! "$0" merge "$BRANCH_NAME" "$WORKTREE_PATH"; then
      log_err "Merge failed! Resolve conflicts in the parent repo."
      exit 1
    fi
    
    # 4. Close
    log "Step 4/4: Dismantling worktree and deleting branch..."
    "$0" close "$BRANCH_NAME" "$WORKTREE_PATH"
    
    log "Worktree branch '$BRANCH_NAME' integrated and cleaned up successfully!"
    ;;

  list)
    log "Active Git worktrees for project '$PROJECT_NAME':"
    # Parse git worktree list
    git worktree list --porcelain | while read -r line; do
      if [[ "$line" =~ ^worktree\ (.*) ]]; then
        wt_path="${BASH_REMATCH[1]}"
      elif [[ "$line" =~ ^branch\ refs/heads/(.*) ]]; then
        wt_branch="${BASH_REMATCH[1]}"
        
        # Check Hub config
        HUB_CONFIG_DIR="$HOME/.gemini/config/projects"
        registered="Unregistered"
        if [ -d "$HUB_CONFIG_DIR" ]; then
          for file in "$HUB_CONFIG_DIR"/*.json; do
            if [ -f "$file" ]; then
              if grep -q "file://$wt_path" "$file"; then
                registered="Registered"
                break
              fi
            fi
          done
        fi
        
        # Omit parent root
        if [ "$wt_path" != "$PARENT_ROOT" ]; then
          echo -e "  - \033[1;33m$wt_branch\033[0m -> $wt_path [$registered]"
        fi
      fi
    done
    ;;

  *)
    log_err "Unknown action: $ACTION"
    usage
    ;;
esac
