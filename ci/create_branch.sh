#!/usr/bin/env bash
# Create a new branch from the latest main branch and upload it to GitHub.
#
# Usage:
#   ./ci/create_branch.sh my-branch
#   ./ci/create_branch.sh            (asks for the name)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=config.sh
source "$SCRIPT_DIR/config.sh"

fail() { echo "✗ $1" >&2; exit 1; }
step() { echo "→ $1"; }

# --- Branch name ---------------------------------------------------------
NAME="${1:-}"
if [[ -z "$NAME" ]]; then
  read -rp "New branch name: " NAME
fi
[[ -n "$NAME" ]] || fail "No branch name given."
BRANCH="${BRANCH_PREFIX}${NAME}"

# --- Checks --------------------------------------------------------------
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || fail "This folder is not a git repository."
cd "$REPO_ROOT"

git check-ref-format --branch "$BRANCH" >/dev/null 2>&1 || fail "'$BRANCH' is not a valid branch name."
git remote get-url "$REMOTE" >/dev/null 2>&1 || fail "Remote '$REMOTE' not found. Check REMOTE in ci/config.sh."
git show-ref --verify --quiet "refs/heads/$MAIN_BRANCH" || fail "Branch '$MAIN_BRANCH' not found. Check MAIN_BRANCH in ci/config.sh."

if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  fail "Branch '$BRANCH' already exists locally. Switch to it with: git switch $BRANCH"
fi
if git ls-remote --exit-code --heads "$REMOTE" "$BRANCH" >/dev/null 2>&1; then
  fail "Branch '$BRANCH' already exists on $REMOTE."
fi

# --- Create the branch ---------------------------------------------------
step "Switching to $MAIN_BRANCH"
git switch "$MAIN_BRANCH"

if git ls-remote --exit-code --heads "$REMOTE" "$MAIN_BRANCH" >/dev/null 2>&1; then
  step "Getting the latest $MAIN_BRANCH from $REMOTE"
  git pull --ff-only "$REMOTE" "$MAIN_BRANCH"
fi

step "Creating branch $BRANCH"
git switch -c "$BRANCH"

step "Uploading $BRANCH to $REMOTE"
git push -u "$REMOTE" "$BRANCH"

echo "✓ Branch '$BRANCH' created and uploaded. You are now on it."
