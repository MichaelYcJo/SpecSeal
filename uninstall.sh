#!/usr/bin/env bash
set -euo pipefail

# specseal uninstaller — the exact inverse of install.sh.
#
# install.sh only ever writes the marker block into a CLAUDE.md, so this
# removes only that block. It never touches skills/, agents/, commands/, or
# settings — under the plugin distribution those are either plugin-managed
# (removed by /plugin uninstall) or the user's own files, which no
# uninstaller has any business deleting.
#
# Usage: bash uninstall.sh [target-CLAUDE.md]   (default: ~/.claude/CLAUDE.md)

TARGET="${1:-$HOME/.claude/CLAUDE.md}"
START='<!-- specseal:start -->'
END='<!-- specseal:end -->'

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info() { echo -e "${GREEN}[info]${NC} $1"; }
warn() { echo -e "${YELLOW}[warn]${NC} $1"; }

if [ ! -f "$TARGET" ]; then
    warn "$TARGET not found — nothing to remove."
else
    if grep -qF "$START" "$TARGET"; then
        cp "$TARGET" "$TARGET.bak"
        info "Backed up to $TARGET.bak"
        awk -v s="$START" -v e="$END" '
          index($0, s) { in_block = 1; next }
          index($0, e) { in_block = 0; next }
          !in_block    { print }
        ' "$TARGET.bak" > "$TARGET"
        info "Removed the preset block from $TARGET"
    else
        info "No preset block in $TARGET — nothing to remove."
    fi
fi

echo ""
info "The plugin uninstalls separately:"
echo "       claude → /plugin uninstall specseal"
