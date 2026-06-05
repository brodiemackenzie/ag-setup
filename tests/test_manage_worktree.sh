#!/usr/bin/env bash
#
# Automated Unit Test for manage_worktree.sh
# Verifies worktree creation, branch naming, environment linking, and cleanup subcommands.
#

set -euo pipefail

# Text formatting helper
log_info() {
  echo -e "\033[1;34m[Test Info]\033[0m $1"
}

log_pass() {
  echo -e "\033[1;32m[PASS]\033[0m $1"
}

log_fail() {
  echo -e "\033[1;31m[FAIL]\033[0m $1" >&2
  exit 1
}

# 1. Setup Workspace and Mock Repository
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

TEST_REPO="$WORKSPACE_DIR/sandbox/temp-test-repo"
PROJECT_NAME="temp-test-repo"
EPIC_SLUG="ep-billing"
FEATURE_SLUG="ft-stripe-checkout"
BRANCH_NAME="${EPIC_SLUG}-${FEATURE_SLUG}"
WORKTREE_PATH="$HOME/.gemini/jetski/worktrees/$PROJECT_NAME/$BRANCH_NAME"

log_info "Cleaning previous test residues..."
rm -rf "$TEST_REPO"
rm -rf "$WORKTREE_PATH"

log_info "Creating mock repository at $TEST_REPO..."
mkdir -p "$TEST_REPO"
cd "$TEST_REPO"

# Init git and configure mock identity for testing
git init -q
git config user.email "test-agent@google.com"
git config user.name "Test Agent"

# Copy templates into the mock repo
log_info "Copying process templates into mock repository .agents/..."
mkdir -p .agents
cp -r "$WORKSPACE_DIR/workspace/templates/sdd-anchored/_agents/"* .agents/

# Create initial commit
touch README.md
git add .
git commit -m "initial commit" -q

# Create mock specifications
log_info "Creating dummy spec files..."
SPEC_DIR="docs/sdd/$EPIC_SLUG/$FEATURE_SLUG"
mkdir -p "$SPEC_DIR"
echo "# SPEC" > "$SPEC_DIR/SPEC.md"
echo "# DESIGN" > "$SPEC_DIR/DESIGN.md"
echo "# TASKS" > "$SPEC_DIR/TASKS.md"

# Commit specs
git add .
git commit -m "add specifications" -q

# 2. Run Test: PROTOTYPE
log_info "Testing PROTOTYPE subcommand..."
./.agents/skills/worktree-manager/scripts/manage_worktree.sh prototype "$EPIC_SLUG" "$FEATURE_SLUG" > /dev/null

# Assertions for PROTOTYPE
if [ ! -d "$WORKTREE_PATH" ]; then
  log_fail "Worktree directory was not created at: $WORKTREE_PATH"
fi
log_pass "Worktree folder created at the expected location."

if ! git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
  log_fail "Git branch '$BRANCH_NAME' was not created."
fi
log_pass "Git branch '$BRANCH_NAME' created successfully."

if [ ! -f "$WORKTREE_PATH/docs/sdd/$EPIC_SLUG/$FEATURE_SLUG/SPEC.md" ]; then
  log_fail "Specification file did not check out in worktree."
fi
log_pass "Specifications successfully checked out inside worktree root."

# 3. Run Test: LINK-ENV (Selective Linking)
log_info "Testing LINK-ENV subcommand (Selective Linking)..."
# Create mock environments in parent
mkdir -p node_modules
touch package.json
mkdir -p .venv

# Test A: Link ONLY 'node'
log_info "Link ONLY 'node' environment..."
./.agents/skills/worktree-manager/scripts/manage_worktree.sh link-env "$EPIC_SLUG" "$FEATURE_SLUG" node > /dev/null

if [ ! -L "$WORKTREE_PATH/node_modules" ]; then
  log_fail "Node modules symlink was not created in worktree."
fi
if [ -d "$WORKTREE_PATH/.venv" ] || [ -L "$WORKTREE_PATH/.venv" ]; then
  log_fail "Python virtual env should not have been created/linked."
fi
log_pass "Only node_modules linked successfully. Python ignored."

# Clean links for next check
rm -rf "$WORKTREE_PATH/node_modules"
rm -rf "$WORKTREE_PATH/.venv"

# Test B: Link ONLY 'python'
log_info "Link ONLY 'python' environment..."
./.agents/skills/worktree-manager/scripts/manage_worktree.sh link-env "$EPIC_SLUG" "$FEATURE_SLUG" python > /dev/null

if [ -L "$WORKTREE_PATH/node_modules" ]; then
  log_fail "Node modules should not have been linked."
fi
if [ ! -d "$WORKTREE_PATH/.venv" ]; then
  log_fail "Python virtual env was not created in worktree."
fi
log_pass "Only python virtualenv created successfully. Node ignored."

# 4. Run Test: CLOSE-FEATURE
log_info "Testing CLOSE-FEATURE subcommand..."
./.agents/skills/worktree-manager/scripts/manage_worktree.sh close-feature "$EPIC_SLUG" "$FEATURE_SLUG" > /dev/null

# Assertions for CLOSE-FEATURE
if [ -d "$WORKTREE_PATH" ]; then
  log_fail "Worktree folder was not deleted after closing feature."
fi
log_pass "Worktree folder dismantled and deleted successfully."

if git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
  log_fail "Git branch '$BRANCH_NAME' was not deleted after closing feature."
fi
log_pass "Git branch '$BRANCH_NAME' deleted successfully."

# 5. Cleanup
log_info "Cleaning up mock repository..."
rm -rf "$TEST_REPO"

echo ""
echo -e "\033[1;32m===============================\033[0m"
echo -e "\033[1;32m ALL TESTS PASSED SUCCESSFULLY \033[0m"
echo -e "\033[1;32m===============================\033[0m"
