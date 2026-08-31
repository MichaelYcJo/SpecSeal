#!/usr/bin/env bash
set -euo pipefail

# specseal installer — CLAUDE.md marker-block merge only.
#
# Skills / agents / hooks / commands are distributed as a Claude Code plugin
# (see README: /plugin install). The one thing a plugin cannot carry is a
# CLAUDE.md block, so this script manages exactly that:
#
#   1. Back up the existing ~/.claude/CLAUDE.md to CLAUDE.md.bak
#   2. Insert or update the <!-- specseal:start/end --> block
#   3. NEVER touch content outside the markers — if something outside looks
#      like it overlaps with the block, print a warning and leave it alone.
#      (Semantic dedup is /specseal:preset-setup's job, with your approval, not ours.)
#
# Usage: bash install.sh                      → global (~/.claude/CLAUDE.md)
#        bash install.sh --project            → this project (./CLAUDE.md, committed with the repo)
#        bash install.sh <target-CLAUDE.md>   → explicit path
# Pick ONE scope — global and project CLAUDE.md both load, so installing the
# block in both duplicates it.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "${1:-}" = "--project" ]; then
    TARGET="$(pwd)/CLAUDE.md"
elif [ -n "${1:-}" ]; then
    TARGET="$1"
else
    # No argument: ask when a terminal is available, otherwise default to global.
    # Read from /dev/tty, not stdin — `curl | bash` occupies stdin with the script.
    TARGET="$HOME/.claude/CLAUDE.md"
    if { exec 3< /dev/tty; } 2>/dev/null; then
        echo "Install scope:"
        echo "  1) Global  — $HOME/.claude/CLAUDE.md  (every project on this machine)"
        echo "  2) Project — $(pwd)/CLAUDE.md  (committed, teammates get it via git)"
        printf "Choose [1/2] (default 1): "
        read -r choice <&3 || choice=""
        exec 3<&-
        [ "$choice" = "2" ] && TARGET="$(pwd)/CLAUDE.md"
    else
        echo "(non-interactive: installing globally — use --project for project scope)"
    fi
fi
SOURCE="$REPO_DIR/CLAUDE.md"
START='<!-- specseal:start -->'
END='<!-- specseal:end -->'

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { echo -e "${GREEN}[info]${NC} $1"; }
warn()  { echo -e "${YELLOW}[warn]${NC} $1"; }
error() { echo -e "${RED}[error]${NC} $1"; exit 1; }

[ -f "$SOURCE" ] || error "Run this script from the specseal directory (CLAUDE.md not found)."
grep -qF "$START" "$SOURCE" || error "Source CLAUDE.md has no preset markers."

# Extract the managed block (markers included) from the repo file.
BLOCK="$(awk -v s="$START" -v e="$END" '
  index($0, s) { in_block = 1 }
  in_block     { print }
  index($0, e) { exit }
' "$SOURCE")"

mkdir -p "$(dirname "$TARGET")"

if [ ! -f "$TARGET" ]; then
    printf '%s\n' "$BLOCK" > "$TARGET"
    info "Created $TARGET with the preset block."
else
    cp "$TARGET" "$TARGET.bak"
    info "Backed up existing file to $TARGET.bak"

    if grep -qF "$START" "$TARGET"; then
        # A start marker without its end marker means the block is damaged;
        # the update below would silently drop everything after START.
        grep -qF "$END" "$TARGET" || error \
            "Found the start marker but no end marker in $TARGET — refusing to edit. Repair the block (or delete it) and rerun."
        # Replace everything between the markers (inclusive) with the new block.
        # BSD awk rejects multi-line -v strings, so assemble in three parts.
        awk -v s="$START" 'index($0, s) { exit } { print }' "$TARGET.bak" > "$TARGET"
        printf '%s\n' "$BLOCK" >> "$TARGET"
        awk -v e="$END" 'after { print } index($0, e) { after = 1 }' "$TARGET.bak" >> "$TARGET"
        info "Updated the preset block in $TARGET"
    else
        { cat "$TARGET.bak"; echo ""; printf '%s\n' "$BLOCK"; } > "$TARGET"
        info "Appended the preset block to $TARGET"
    fi

    # Warn (never edit) when user-owned content outside the block may overlap.
    OUTSIDE="$(awk -v s="$START" -v e="$END" '
      index($0, s) { in_block = 1 }
      !in_block    { print }
      index($0, e) { in_block = 0 }
    ' "$TARGET")"
    for kw in 'uv' 'pnpm' 'worktree' 'Verification' 'Fix Rule'; do
        if printf '%s\n' "$OUTSIDE" | grep -qiw -- "$kw"; then
            warn "Outside the preset block, '$kw' appears — check for overlap with the block."
        fi
    done
fi

echo ""
info "CLAUDE.md done. Remaining components install as a plugin:"
echo "       claude → /plugin marketplace add MichaelYcJo/SpecSeal"
echo "                /plugin install specseal@specseal"
echo ""
info "For a reviewed, deduplicated merge instead of this mechanical one:"
echo "       restore $TARGET.bak, then run /specseal:preset-setup inside Claude Code."
