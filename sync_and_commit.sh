#!/usr/bin/env bash
# sync_and_commit.sh — Sync live web files to git repo and auto-commit + push
set -euo pipefail

REPO_DIR="/home/lionelsabdani36/duckvaulta"
MSG="${1:-chore: auto-sync daily project updates and telemetry}"

cd "$REPO_DIR"

# 1. Sync Portal Web
if [ -f /var/www/duckvaulta/index.html ]; then
    cp /var/www/duckvaulta/index.html "$REPO_DIR/apps/portal/index.html"
    cp -r /var/www/duckvaulta/assets/* "$REPO_DIR/apps/portal/assets/" 2>/dev/null || true
fi

# 2. Sync EdTech Web
if [ -f /var/www/edtech/index.html ]; then
    cp /var/www/edtech/index.html "$REPO_DIR/apps/edtech/index.html"
    cp -r /var/www/edtech/assets/* "$REPO_DIR/apps/edtech/assets/" 2>/dev/null || true
fi

# 3. Check for git diffs
if [ -z "$(git status --porcelain)" ]; then
    echo "[git-sync] No changes detected. Repository is up-to-date."
    exit 0
fi

# 4. Add, Commit, and Push
git add .
git commit -m "$MSG"
git push origin main
echo "[git-sync] Successfully committed and pushed changes to GitHub."
