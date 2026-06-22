#!/usr/bin/env bash
# Programmatic SDD Workspace Status Reporter
set -euo pipefail

# Path resolution: Find project root relative to .agents/ folder
PROJECT_ROOT="$(pwd)"

# Check if we are inside a Git worktree sandbox
IS_SANDBOX=false
if git rev-parse --verify HEAD &>/dev/null; then
    CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
else
    CURRENT_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo "main (unborn)")"
fi
WORKTREE_NAME="None"

if git worktree list | grep -q "$(pwd)"; then
    IS_SANDBOX=true
    WORKTREE_NAME="$(basename "$(pwd)")"
fi

# Helper function to extract metadata from files
get_metadata_status() {
    local file_path="$1"
    if [ ! -f "$file_path" ]; then
        echo "Missing"
        return
    fi
    # Parse status using simple pattern match, fallback to Found if no status block
    local status
    status=$(grep -i "^Status:" "$file_path" | head -n1 | cut -d':' -f2 | tr -d '[:space:]' || true)
    if [ -n "$status" ]; then
        echo "$status"
    else
        echo "Found"
    fi
}

# 1. Gather specification states
PROJECT_STATUS=$(get_metadata_status "docs/PROJECT.md")

# Find spec capsule directory to scan features
SPEC_STATUS="None"
CODE_ANALYSIS_STATUS=$(get_metadata_status "docs/sdd/CODE_ANALYSIS.md")
DESIGN_STATUS="None"
TASKS_STATUS="None"
VERIFY_STATUS="None"

# If in a sandbox worktree, we look for feature specs in docs/sdd/
# Sandbox branch naming structure: feature/<epic_slug>/<feature_slug>
if [ "$IS_SANDBOX" = true ]; then
    # Attempt to locate active feature docs path
    if [ -d "docs/sdd" ]; then
        FEATURE_DOCS_DIR=$(find docs/sdd -mindepth 2 -maxdepth 2 -type d | head -n1 || true)
        if [ -n "$FEATURE_DOCS_DIR" ]; then
            SPEC_STATUS=$(get_metadata_status "$FEATURE_DOCS_DIR/SPEC.md")
            DESIGN_STATUS=$(get_metadata_status "$FEATURE_DOCS_DIR/DESIGN.md")
            TASKS_STATUS=$(get_metadata_status "$FEATURE_DOCS_DIR/TASKS.md")
            VERIFY_STATUS=$(get_metadata_status "$FEATURE_DOCS_DIR/VERIFICATION_REPORT.md")
        fi
    fi
fi

# Print markdown status report table
cat <<EOF
| Project Dimension | Current Status |
| :--- | :--- |
| Current Directory | ${PROJECT_ROOT} |
| Git Sandbox | $( [ "$IS_SANDBOX" = true ] && echo "Active ($WORKTREE_NAME)" || echo "Inactive (Parent Repository)" ) |
| Git Branch | ${CURRENT_BRANCH} |
| Project Blueprint | ${PROJECT_STATUS} |
| Codebase Analysis | ${CODE_ANALYSIS_STATUS} |
| Feature Specification | ${SPEC_STATUS} |
| Technical Design | ${DESIGN_STATUS} |
| Task Checklist | ${TASKS_STATUS} |
| Verification Report | ${VERIFY_STATUS} |
EOF
