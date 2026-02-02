#!/usr/bin/env bash

# CDD SKILL Auto-Push Script
#
# This script pushes CDD SKILL updates to GitHub repository.
#
# Usage: ./push-cdd-skill.sh [commit_message]
#
# Default message: "Update: CDD SKILL v1.5.0 - $(date)"
#
# Prerequisites:
#   - Must be run in the CDD SKILL directory
#   - Git remote must be configured
#   - GitHub PAT must have repo scope

set -e

# Get script directory
SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CDD_DIR="/home/wsman/桌面/openclaw/skills/cdd"
REMOTE_URL="https://github.com/wsman/Constitution-Driven-Development-Skill.git"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if in CDD SKILL directory
    if [[ ! -d "$CDD_DIR/.git" ]]; then
        log_error "Not in CDD SKILL directory or .git not found"
        log_info "Expected directory: $CDD_DIR"
        exit 1
    fi
    
    # Check git remote
    cd "$CDD_DIR"
    CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
    
    if [[ "$CURRENT_REMOTE" != *"$REMOTE_URL"* ]]; then
        log_warn "Remote URL doesn't match expected GitHub repository"
        log_info "Current remote: $CURRENT_REMOTE"
        log_info "Expected: $REMOTE_URL"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    log_info "Prerequisites check passed!"
}

# Get commit message
get_commit_message() {
    local msg="$1"
    
    if [[ -n "$msg" ]]; then
        echo "$msg"
    else
        # Get current version from SKILL.md
        local version=$(grep -m1 "version:" "$CDD_DIR/SKILL.md" | sed 's/.*version: *//' | tr -d ' ')
        echo "Update: CDD SKILL v${version} - $(date '+%Y-%m-%d %H:%M')"
    fi
}

# Main push function
push_cdd_skill() {
    local commit_msg="${1:-}"
    
    cd "$CDD_DIR"
    
    log_info "=== CDD SKILL Auto-Push ==="
    echo ""
    
    # Show status
    log_info "Git Status:"
    git status --short
    echo ""
    
    # Get commit message
    local msg
    msg=$(get_commit_message "$commit_msg")
    log_info "Commit message: $msg"
    echo ""
    
    # Stage all changes
    log_info "Staging all changes..."
    git add -A
    
    # Check if there are changes
    if git diff --cached --quiet; then
        log_warn "No changes to commit"
        exit 0
    fi
    
    # Commit
    log_info "Committing changes..."
    git commit -m "$msg"
    
    # Push
    log_info "Pushing to GitHub..."
    if git push origin main 2>&1; then
        log_info "✅ Successfully pushed to GitHub!"
        echo ""
        echo "Repository: $REMOTE_URL"
        echo "Commit: $(git rev-parse --short HEAD)"
    else
        log_error "Failed to push to GitHub"
        exit 1
    fi
}

# Show help
show_help() {
    echo "CDD SKILL Auto    echo ""
    echo "Usage:-Push Script"
 $0 [commit_message]"
    echo ""
    echo "Arguments:"
    echo "  commit_message    Optional commit message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Auto-generate message"
    echo "  $0 \"Fix: Typo in SKILL.md\"  # Custom message"
    echo ""
    echo "Environment:"
    echo "  CDD_DIR: $CDD_DIR"
    echo "  REMOTE: $REMOTE_URL"
}

# Main
main() {
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        show_help
        exit 0
    fi
    
    check_prerequisites
    push_cdd_skill "$1"
}

main "$@"
