#!/usr/bin/env bash
# Save all project changes on the current branch and sync with GitHub:
#   1. commit every new, changed or deleted file
#   2. download other people's changes to this branch
#   3. (optional) merge the latest main into this branch
#   4. upload the result
#
# Usage:
#   ./ci/save_project.sh "Describe your change"
#   ./ci/save_project.sh                (uses DEFAULT_COMMIT_MESSAGE)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=config.sh
source "$SCRIPT_DIR/config.sh"

fail() { echo "✗ $1" >&2; exit 1; }
step() { echo "→ $1"; }
trap 'echo "✗ Stopped because a git command failed (see the message above)." >&2' ERR

MESSAGE="${1:-$DEFAULT_COMMIT_MESSAGE}"

# --- Checks --------------------------------------------------------------
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || fail "This folder is not a git repository."
cd "$REPO_ROOT"

BRANCH="$(git branch --show-current)"
[[ -n "$BRANCH" ]] || fail "You are not on a branch. Switch to one with: git switch <branch>"
git remote get-url "$REMOTE" >/dev/null 2>&1 || fail "Remote '$REMOTE' not found. Check REMOTE in ci/config.sh."

if [[ "$BRANCH" == "$MAIN_BRANCH" && "$CONFIRM_ON_MAIN" == "yes" ]]; then
  read -rp "You are on '$MAIN_BRANCH'. Save directly to it? [y/N] " ANSWER
  [[ "$ANSWER" == "y" || "$ANSWER" == "Y" ]] || fail "Cancelled. Create a branch with: ./ci/create_branch.sh <name>"
fi

# Stop if a blocked file (secrets, keys) would be committed
CHANGED_FILES="$(git ls-files --others --modified --exclude-standard)"
while IFS= read -r FILE; do
  [[ -z "$FILE" ]] && continue
  BASE="$(basename "$FILE")"
  for PATTERN in "${BLOCKED_FILES[@]}"; do
    # shellcheck disable=SC2053
    if [[ "$BASE" == $PATTERN ]]; then
      fail "'$FILE' matches a blocked file ($PATTERN). Add it to .gitignore or remove it, then try again."
    fi
  done
done <<< "$CHANGED_FILES"

# --- 1. Save (commit) ----------------------------------------------------
step "Staging all changes"
git add -A

if git diff --cached --quiet; then
  step "No new changes to commit"
else
  step "Committing: $MESSAGE"
  git commit -m "$MESSAGE"
fi

# --- 2. Get other people's changes to this branch ------------------------
if git ls-remote --exit-code --heads "$REMOTE" "$BRANCH" >/dev/null 2>&1; then
  step "Getting the latest $BRANCH from $REMOTE"
  if ! git pull --rebase "$REMOTE" "$BRANCH"; then
    fail "Conflict while updating. Fix the files git lists, then run: git add . && git rebase --continue"
  fi
fi

# --- 3. Optionally bring in the latest main ------------------------------
if [[ "$SYNC_WITH_MAIN" == "yes" && "$BRANCH" != "$MAIN_BRANCH" ]]; then
  if git ls-remote --exit-code --heads "$REMOTE" "$MAIN_BRANCH" >/dev/null 2>&1; then
    step "Merging the latest $MAIN_BRANCH into $BRANCH"
    git fetch "$REMOTE" "$MAIN_BRANCH"
    if ! git merge --no-edit "$REMOTE/$MAIN_BRANCH"; then
      fail "Conflict while merging $MAIN_BRANCH. Fix the files git lists, then run: git add . && git commit"
    fi
  fi
fi

# --- 4. Upload -----------------------------------------------------------
step "Uploading $BRANCH to $REMOTE"
git push -u "$REMOTE" "$BRANCH"

echo "✓ Project saved and '$BRANCH' is up to date on $REMOTE."
