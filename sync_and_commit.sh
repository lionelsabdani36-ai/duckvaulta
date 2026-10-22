#!/usr/bin/env bash
# sync_and_commit.sh — Sync live web files to git repos and auto-commit + push
set -euo pipefail

REPO_DIR="/home/lionelsabdani36/duckvaulta"
EDTECH_REPO="/home/lionelsabdani36/edtech-ai-platform"
MSG="${1:-chore: auto-sync daily project updates and telemetry}"

# 1. Sync & Push Monorepo (duckvaulta)
cd "$REPO_DIR"
if [ -f /var/www/duckvaulta/index.html ]; then
    cp /var/www/duckvaulta/index.html "$REPO_DIR/apps/portal/index.html"
    cp -r /var/www/duckvaulta/assets/* "$REPO_DIR/apps/portal/assets/" 2>/dev/null || true
fi
if [ -d /var/www/edtech ]; then
    cp /var/www/edtech/*.html "$REPO_DIR/apps/edtech/" 2>/dev/null || true
    cp -r /var/www/edtech/assets/* "$REPO_DIR/apps/edtech/assets/" 2>/dev/null || true
fi
if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "$MSG"
    git push origin main
    echo "[git-sync] Pushed updates to lionelsabdani36-ai/duckvaulta"
fi

# 2. Sync & Push Dedicated EdTech Repo (edtech-ai-platform)
if [ -d "$EDTECH_REPO" ]; then
    cd "$EDTECH_REPO"
    if [ -d /var/www/edtech ]; then
        cp /var/www/edtech/*.html "$EDTECH_REPO/" 2>/dev/null || true
        cp -r /var/www/edtech/assets/* "$EDTECH_REPO/assets/" 2>/dev/null || true
    fi
    if [ -n "$(git status --porcelain)" ]; then
        git add .
        git commit -m "$MSG"
        git push origin main
        echo "[git-sync] Pushed updates to lionelsabdani36-ai/edtech-ai-platform"
    fi
fi

echo "[git-sync] Sync and commit process completed."
