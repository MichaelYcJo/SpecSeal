#!/usr/bin/env bash
set -euo pipefail

# claude_preset uninstaller

CLAUDE_DIR="$HOME/.claude"
BACKUP_DIR="$CLAUDE_DIR/backup/$(date +%Y%m%d_%H%M%S)_uninstall"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() { echo -e "${GREEN}[info]${NC} $1"; }
warn() { echo -e "${YELLOW}[warn]${NC} $1"; }

echo ""
echo "╔══════════════════════════════════════╗"
echo "║      claude_preset uninstaller       ║"
echo "╚══════════════════════════════════════╝"
echo ""

read -rp "Remove claude_preset from $CLAUDE_DIR? [y/N] " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

mkdir -p "$BACKUP_DIR"

# Backup and remove installed files
for item in CLAUDE.md rules skills commands agents scripts; do
    if [ -e "$CLAUDE_DIR/$item" ]; then
        cp -r "$CLAUDE_DIR/$item" "$BACKUP_DIR/$item"
        rm -rf "$CLAUDE_DIR/$item"
        info "Removed $item (backed up)"
    fi
done

# Don't remove settings.json (may have user customizations)
warn "settings.json preserved (may contain custom hooks)."

echo ""
info "Uninstall complete. Backup at: $BACKUP_DIR"
echo ""

# Check for previous backup to restore
LATEST_INSTALL_BACKUP=$(ls -td "$CLAUDE_DIR"/backup/*/ 2>/dev/null | grep -v uninstall | head -1 || true)
if [ -n "$LATEST_INSTALL_BACKUP" ]; then
    echo "  Previous config found at: $LATEST_INSTALL_BACKUP"
    read -rp "  Restore previous configuration? [y/N] " restore
    if [[ "$restore" =~ ^[Yy]$ ]]; then
        for item in "$LATEST_INSTALL_BACKUP"*; do
            name="$(basename "$item")"
            cp -r "$item" "$CLAUDE_DIR/$name"
            info "Restored $name"
        done
    fi
fi

echo ""
echo "  Start a new Claude Code session to apply changes."
echo ""
