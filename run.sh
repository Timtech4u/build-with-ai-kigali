#!/bin/bash
# Build with AI: Study Jam #1 — GDG Kigali
# Quick launcher for live demos during the talk
#
# Usage:
#   ./run.sh          — Show menu
#   ./run.sh 1        — Demo 1: Visual Builder (adk web)
#   ./run.sh 2        — Demo 2: Kigali Agent (CLI)
#   ./run.sh 3        — Demo 3: Browser Agent (CLI)
#   ./run.sh check    — Verify everything is ready

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CODE_DIR="$SCRIPT_DIR/code"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

header() {
    echo ""
    echo -e "${CYAN}${BOLD}═══════════════════════════════════════════${NC}"
    echo -e "${CYAN}${BOLD}  Build with AI — GDG Kigali Demo Runner${NC}"
    echo -e "${CYAN}${BOLD}═══════════════════════════════════════════${NC}"
    echo ""
}

check() {
    header
    echo -e "${BOLD}Pre-flight check:${NC}"
    echo ""

    # Python
    if command -v python3 &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Python $(python3 --version 2>&1 | awk '{print $2}')"
    else
        echo -e "  ${RED}✗${NC} Python not found"
    fi

    # google-adk
    if python3 -c "import google.adk" 2>/dev/null; then
        VER=$(pip3 show google-adk 2>/dev/null | grep Version | awk '{print $2}')
        echo -e "  ${GREEN}✓${NC} google-adk $VER"
    else
        echo -e "  ${RED}✗${NC} google-adk not installed (pip install google-adk)"
    fi

    # API key
    if [ -n "$GOOGLE_API_KEY" ]; then
        echo -e "  ${GREEN}✓${NC} GOOGLE_API_KEY is set"
    else
        echo -e "  ${RED}✗${NC} GOOGLE_API_KEY not set"
    fi

    # Chrome CDP
    if curl -s http://localhost:9222/json/version &>/dev/null; then
        BROWSER=$(curl -s http://localhost:9222/json/version | python3 -c "import sys,json; print(json.load(sys.stdin)['Browser'])" 2>/dev/null)
        echo -e "  ${GREEN}✓${NC} Chrome CDP running ($BROWSER)"
    else
        echo -e "  ${YELLOW}!${NC} Chrome CDP not running (needed for Demo 3 only)"
        echo -e "      Start with: ${CYAN}chrome-cdp status${NC}"
    fi

    # websocket-client
    if python3 -c "import websocket" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} websocket-client installed"
    else
        echo -e "  ${RED}✗${NC} websocket-client not installed (pip install websocket-client)"
    fi

    echo ""
    echo -e "${GREEN}Ready to demo!${NC}"
    echo ""
}

demo_menu() {
    header
    echo -e "  ${BOLD}1${NC}  Visual Builder    ${YELLOW}adk web${NC} — no-code agent builder"
    echo -e "  ${BOLD}2${NC}  Kigali Agent      ${YELLOW}adk run${NC} — CLI agent with tools"
    echo -e "  ${BOLD}3${NC}  Browser Agent     ${YELLOW}adk run${NC} — controls Chrome live"
    echo ""
    echo -e "  ${BOLD}check${NC}  Pre-flight check"
    echo -e "  ${BOLD}q${NC}      Quit"
    echo ""
    read -p "  Pick a demo [1-3]: " choice
    run_demo "$choice"
}

run_demo() {
    case "$1" in
        1)
            echo ""
            echo -e "${CYAN}${BOLD}Demo 1: Visual Builder${NC}"
            echo -e "Open ${YELLOW}http://localhost:8000${NC} in Chrome after it starts"
            echo -e "Press Ctrl+C to stop"
            echo ""
            cd "$CODE_DIR"
            adk web --port 8000
            ;;
        2)
            echo ""
            echo -e "${CYAN}${BOLD}Demo 2: Kigali Agent${NC}"
            echo -e "Try: ${YELLOW}\"Convert 500 USD to RWF\"${NC}"
            echo -e "Try: ${YELLOW}\"What's the mobile money market size in Rwanda?\"${NC}"
            echo -e "Press Ctrl+C to stop"
            echo ""
            cd "$CODE_DIR/kigali_agent"
            adk run kigali_agent
            ;;
        3)
            # Verify CDP first
            if ! curl -s http://localhost:9222/json/version &>/dev/null; then
                echo -e "${RED}Chrome CDP not running!${NC}"
                echo -e "Start Chrome with: ${CYAN}chrome-cdp status${NC}"
                exit 1
            fi
            echo ""
            echo -e "${CYAN}${BOLD}Demo 3: Browser Agent${NC}"
            echo -e "Try: ${YELLOW}\"List my open tabs\"${NC}"
            echo -e "Try: ${YELLOW}\"Open https://gdg.community.dev and tell me what's on the page\"${NC}"
            echo -e "Try: ${YELLOW}\"Take a screenshot\"${NC}"
            echo -e "Press Ctrl+C to stop"
            echo ""
            cd "$CODE_DIR/browser_agent"
            adk run browser_agent
            ;;
        check)
            check
            ;;
        q|Q)
            exit 0
            ;;
        *)
            demo_menu
            ;;
    esac
}

# Entry point
if [ -n "$1" ]; then
    run_demo "$1"
else
    demo_menu
fi
