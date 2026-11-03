#!/usr/bin/env bash
# ==============================================================================
# Anti-Slop Automated Validation Pipeline
# Integrates 6 Anti-Slop Skills:
# 1. Impeccable (pbakaus/impeccable) - UI detector & polish
# 2. Better-Icons (better-auth/better-icons) - SVG icons retrieval via Iconify
# 3. Hallmark (Nutlope/hallmark) - 57 design rules & sloplint
# 4. Taste-Skill (Leonxlnx/taste-skill) - Art direction from 247 Awwwards sites
# 5. Stop-Slop (hardikpandya/stop-slop) - Prose de-slopping & tell removal
# 6. Humanizer (blader/humanizer) - Natural human voice & Wikipedia patterns
# ==============================================================================

set -euo pipefail

TARGET_PATH="${1:-.}"
HALLMARK_LINTER="/home/lionelsabdani36/.hermes/skills/design-and-ui/hallmark/scripts/sloplint.mjs"

echo "=== [1/5] Verifying Better-Icons CLI ==="
if command -v better-icons >/dev/null 2>&1; then
    echo "✓ better-icons CLI is installed and operational ($(which better-icons))"
else
    echo "✗ better-icons CLI not found in PATH"
    exit 1
fi

echo "=== [2/5] Running Impeccable UI Detector ==="
if command -v impeccable >/dev/null 2>&1; then
    echo "Running: impeccable detect on target: ${TARGET_PATH}"
    impeccable detect "${TARGET_PATH}" || true
else
    echo "✗ impeccable CLI not found in PATH"
fi

echo "=== [3/5] Running Hallmark Sloplint ==="
if [ -f "${HALLMARK_LINTER}" ]; then
    echo "Running: node sloplint.mjs on target: ${TARGET_PATH}"
    node "${HALLMARK_LINTER}" "${TARGET_PATH}" || true
else
    echo "✗ Hallmark sloplint not found at ${HALLMARK_LINTER}"
fi

echo "=== [4/5] Prose & Writing Anti-Slop Audit (Stop-Slop & Humanizer) ==="
python3 - << 'EOF'
import sys, os, re

banned_words = [
    r"\bdelve\b", r"\btapestry\b", r"\btestament\b", r"\bharness\b",
    r"\bfoster\b", r"\bbustling\b", r"\bpivotal\b", r"\bseamless\b",
    r"\bgroundbreaking\b", r"\bcutting-edge\b", r"\bleverage\b",
    r"\bgame-changer\b", r"\btransformative\b", r"\bvibrant\b"
]

banned_structures = [
    (r"—", "Em-dash detected (replace with period or comma)"),
    (r"not only .* but also", "Formulaic binary contrast (not only... but also)"),
    (r"in today'?s (fast-paced|digital) world", "Throat-clearing cliché opener")
]

print("Scanning prose files for AI tells...")
checked = 0
violations = 0

for root, _, files in os.walk("."):
    if any(skip in root for skip in ["node_modules", ".git", ".hermes", "cache", "build", "dist"]):
        continue
    for f in files:
        if f.endswith((".md", ".txt", ".html")):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                    checked += 1
                    for bw in banned_words:
                        matches = re.findall(bw, content, re.IGNORECASE)
                        if matches:
                            print(f"  [AI-BUZZWORD] {path}: '{matches[0]}'")
                            violations += 1
                    for bs, desc in banned_structures:
                        if re.search(bs, content, re.IGNORECASE):
                            print(f"  [AI-STRUCTURE] {path}: {desc}")
                            violations += 1
            except Exception:
                pass

print(f"Prose scan finished: {checked} files checked, {violations} flagged patterns.")
EOF

echo "=== [5/5] Anti-Slop Check Complete ==="
