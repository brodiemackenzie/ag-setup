#!/bin/bash
# manage_worktree.sh
# Automates the Git Worktree lifecycle aligned with Spec-Driven Development (SDD).
# Supported stacks: Node.js (npm), Python (venv), Rust (Cargo), Go.

ACTION=$1
EPIC=$2
FEATURE=$3
LINK_FLAG=$4

if [ -z "$ACTION" ]; then
  echo "Usage: $0 [draft-spec|prototype|provision-from-spec|link-env|sync-worktree|close-feature] [epic] [feature] [--link]"
  exit 1
fi

# 1. Calculate absolute directories
MAIN_DIR=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$MAIN_DIR" ]; then
  echo "Error: Not inside a Git repository."
  exit 1
fi

WORKTREES_ROOT="$MAIN_DIR/worktrees"
WORKTREE_PATH="$WORKTREES_ROOT/$EPIC/$FEATURE"
BRANCH_NAME="feature/$EPIC/$FEATURE"
SPEC_FILE="docs/sdd/$EPIC/$FEATURE.md"

# Ensure workspace hygiene (.gitignore has worktrees/)
ensure_gitignore() {
  if ! grep -q "^worktrees/" "$MAIN_DIR/.gitignore" 2>/dev/null; then
    echo "" >> "$MAIN_DIR/.gitignore"
    echo "# Local isolated Git worktrees" >> "$MAIN_DIR/.gitignore"
    echo "worktrees/" >> "$MAIN_DIR/.gitignore"
    echo "Added worktrees/ to main repository .gitignore."
  fi
}

# Generate a standard SDD template
write_sdd_template() {
  local target=$1
  local epic_name=$2
  local feature_name=$3
  
  mkdir -p "$(dirname "$target")"
  cat << EOF > "$target"
# SDD Specification: ${feature_name^}

* **Epic**: ${epic_name^}
* **Feature**: ${feature_name^}
* **Status**: Draft

---

## 🎯 Objective & Requirements

Detailed description of the feature objective and core business requirements.

* Requirement 1...
* Requirement 2...

## 🏗️ Architecture & Interfaces

* Data models, schema definitions, or state representations.
* API boundaries and function contracts.

## 📋 Verification Strategy & Task List

### Phase 1: Upfront Spec Design
- [x] Draft the initial SDD specification and get user alignment.

### Phase 2: Spec-Based Code Generation
- [ ] Implement feature files matching the specification.
- [ ] Ensure imports and file names match design exactly.

### Phase 3: Verification & Done
- [ ] Write unit / integration tests covering normal paths and edge cases.
- [ ] Execute tests and verify they pass.
- [ ] Present passing test outputs as proof.
EOF
  echo "Created specification template at $target"
}

# Auto-detect and link environment dependencies (Open Source Stacks)
link_environments() {
  echo "Auto-detecting stacks to resolve environments..."
  ensure_gitignore

  if [ ! -d "$WORKTREE_PATH" ]; then
    echo "Error: Worktree folder does not exist at $WORKTREE_PATH"
    exit 1
  fi

  # A. Node.js Auto-Detection
  if [ -f "$MAIN_DIR/package.json" ]; then
    if [ -d "$MAIN_DIR/node_modules" ]; then
      echo "Detected Node.js project. Symlinking node_modules..."
      ln -sfn "$MAIN_DIR/node_modules" "$WORKTREE_PATH/node_modules"
    else
      echo "package.json found, but node_modules is missing on main. Run npm/yarn install first."
    fi
  fi

  # B. Python Auto-Detection
  if [ -f "$MAIN_DIR/requirements.txt" ] || [ -f "$MAIN_DIR/pyproject.toml" ]; then
    local MAIN_VENV=""
    for dir in ".venv" "venv" "env"; do
      if [ -d "$MAIN_DIR/$dir" ]; then
        MAIN_VENV="$MAIN_DIR/$dir"
        break
      fi
    done

    if [ -n "$MAIN_VENV" ]; then
      echo "Detected Python project. Creating inherited virtual env..."
      python3 -m venv --system-site-packages "$WORKTREE_PATH/.venv"
      # Symlink requirements for local visibility
      ln -sfn "$MAIN_DIR/requirements.txt" "$WORKTREE_PATH/requirements.txt"
    else
      echo "Python project detected, but no virtual environment (.venv) found on main."
    fi
  fi

  # C. Rust Auto-Detection
  if [ -f "$MAIN_DIR/Cargo.toml" ]; then
    echo "Detected Rust project. Symlinking target directory to share build cache..."
    mkdir -p "$MAIN_DIR/target"
    ln -sfn "$MAIN_DIR/target" "$WORKTREE_PATH/target"
  fi

  # D. Go Auto-Detection
  if [ -f "$MAIN_DIR/go.mod" ]; then
    echo "Detected Go project. Go natively uses global module caches; no action required."
  fi

  echo "Environment linking complete."
}

# ==========================================
# Action Commands
# ==========================================
case "$ACTION" in
  "draft-spec")
    if [ -z "$EPIC" ] || [ -z "$FEATURE" ]; then
      echo "Usage: $0 draft-spec <epic> <feature>"
      exit 1
    fi
    write_sdd_template "$MAIN_DIR/$SPEC_FILE" "$EPIC" "$FEATURE"
    ;;

  "prototype")
    if [ -z "$EPIC" ] || [ -z "$FEATURE" ]; then
      echo "Usage: $0 prototype <epic> <feature> [--link]"
      exit 1
    fi
    ensure_gitignore
    echo "Creating branch $BRANCH_NAME..."
    git branch "$BRANCH_NAME" 2>/dev/null || echo "Branch already exists. Reusing."
    
    echo "Provisioning worktree at $WORKTREE_PATH..."
    git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"
    
    # Write spec into the worktree
    write_sdd_template "$WORKTREE_PATH/$SPEC_FILE" "$EPIC" "$FEATURE"

    if [[ "$LINK_FLAG" == "--link" ]]; then
      link_environments
    fi
    echo "Worktree prototype successfully provisioned!"
    ;;

  "provision-from-spec")
    # Spec file path is passed as EPIC parameter
    local spec_rel_path=$EPIC
    local spec_abs_path="$MAIN_DIR/$spec_rel_path"
    
    if [ -z "$spec_rel_path" ] || [ ! -f "$spec_abs_path" ]; then
      echo "Usage: $0 provision-from-spec <relative_spec_file_path> [--link]"
      exit 1
    fi
    
    ensure_gitignore
    
    # Extract Epic/Feature from spec path (e.g., docs/sdd/epic/feature.md)
    # spec_rel_path is docs/sdd/epic/feature.md
    local epic_parsed=$(echo "$spec_rel_path" | awk -F'/' '{print $(NF-1)}')
    local feature_parsed=$(echo "$spec_rel_path" | awk -F'/' '{print $NF}' | sed 's/\.md$//')
    
    local wt_path="$WORKTREES_ROOT/$epic_parsed/$feature_parsed"
    local branch="feature/$epic_parsed/$feature_parsed"
    
    echo "Parsed Epic: $epic_parsed, Feature: $feature_parsed"
    echo "Creating branch $branch..."
    git branch "$branch" 2>/dev/null || echo "Branch already exists. Reusing."
    
    echo "Provisioning worktree at $wt_path..."
    git worktree add "$wt_path" "$branch"
    
    # Symlink rules and custom configs into worktree
    mkdir -p "$wt_path/.agents"
    ln -sfn "$MAIN_DIR/.agents/rules" "$wt_path/.agents/rules"
    ln -sfn "$MAIN_DIR/.agents/agents" "$wt_path/.agents/agents"

    if [[ "$FEATURE" == "--link" ]]; then
      # Re-run path bindings for detected stacks
      WORKTREE_PATH=$wt_path
      EPIC=$epic_parsed
      FEATURE=$feature_parsed
      link_environments
    fi
    echo "Worktree provisioned from spec: $wt_path"
    ;;

  "link-env")
    if [ -z "$EPIC" ] || [ -z "$FEATURE" ]; then
      echo "Usage: $0 link-env <epic> <feature>"
      exit 1
    fi
    link_environments
    ;;

  "sync-worktree")
    if [ -z "$EPIC" ] || [ -z "$FEATURE" ]; then
      echo "Usage: $0 sync-worktree <epic> <feature>"
      exit 1
    fi
    echo "Synchronizing worktree: fetching origin and rebasing..."
    git fetch origin
    cd "$WORKTREE_PATH" || exit 1
    git rebase origin/main
    echo "Rebase complete."
    ;;

  "close-feature")
    if [ -z "$EPIC" ] || [ -z "$FEATURE" ]; then
      echo "Usage: $0 close-feature <epic> <feature>"
      exit 1
    fi
    echo "Merging branch $BRANCH_NAME to main..."
    git checkout main
    git merge "$BRANCH_NAME"
    
    # Reconcile dependencies back to main
    if [ -f "$MAIN_DIR/requirements.txt" ] && [ -f "$WORKTREE_PATH/requirements.txt" ]; then
      # If python venv is active on main, sync packages
      local VENV_BIN=""
      for dir in ".venv/bin/pip" "venv/bin/pip" "env/bin/pip"; do
        if [ -f "$MAIN_DIR/$dir" ]; then
          VENV_BIN="$MAIN_DIR/$dir"
          break
        fi
      done
      if [ -n "$VENV_BIN" ]; then
        echo "Reconciling python dependencies..."
        $VENV_BIN install -r "$MAIN_DIR/requirements.txt"
      fi
    fi
    
    if [ -f "$MAIN_DIR/package.json" ]; then
      echo "Reconciling npm dependencies..."
      npm install
    fi

    echo "Deleting worktree folder..."
    git worktree remove "$WORKTREE_PATH"
    git branch -d "$BRANCH_NAME"
    echo "Feature closed and cleaned up successfully!"
    ;;

  *)
    echo "Invalid command: $ACTION"
    exit 1
    ;;
esac
