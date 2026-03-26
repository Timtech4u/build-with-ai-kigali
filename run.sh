#!/bin/bash
# Build with AI — GDG Kigali 2026
# Demo launcher for Study Jam #1 (text agents) and #2 (voice AI)
#
# Usage:
#   ./run.sh          — Show menu
#   ./run.sh 1-3      — Study Jam #1 demos (ADK agents)
#   ./run.sh v1-v5    — Study Jam #2 demos (Voice AI)
#   ./run.sh check    — Verify setup

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CODE_DIR="$SCRIPT_DIR/code"
VOICE_DIR="$SCRIPT_DIR/studyjam2-demos"

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

    if command -v python3 &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Python $(python3 --version 2>&1 | awk '{print $2}')"
    else
        echo -e "  ${RED}✗${NC} Python not found"
    fi

    if python3 -c "import google.genai" 2>/dev/null; then
        VER=$(python3 -c "import google.genai; print(google.genai.__version__)" 2>/dev/null)
        echo -e "  ${GREEN}✓${NC} google-genai $VER (Voice AI)"
    else
        echo -e "  ${YELLOW}!${NC} google-genai not installed (pip install google-genai)"
    fi

    if python3 -c "import google.adk" 2>/dev/null; then
        VER=$(pip3 show google-adk 2>/dev/null | grep Version | awk '{print $2}')
        echo -e "  ${GREEN}✓${NC} google-adk $VER (Text Agents)"
    else
        echo -e "  ${YELLOW}!${NC} google-adk not installed (pip install google-adk)"
    fi

    if [ -n "$GOOGLE_API_KEY" ]; then
        echo -e "  ${GREEN}✓${NC} GOOGLE_API_KEY is set"
    else
        echo -e "  ${RED}✗${NC} GOOGLE_API_KEY not set"
    fi

    if command -v afplay &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} afplay (macOS audio playback)"
    else
        echo -e "  ${YELLOW}!${NC} afplay not found (voice demos need macOS or alternative player)"
    fi

    if curl -s http://localhost:9222/json/version &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Chrome CDP running (browser agent)"
    else
        echo -e "  ${YELLOW}!${NC} Chrome CDP not running (only needed for demo 3)"
    fi

    echo ""
    echo -e "${GREEN}Ready to demo!${NC}"
    echo ""
}

demo_menu() {
    header
    echo -e "  ${BOLD}Study Jam #1 — Text Agents${NC}"
    echo -e "  ${BOLD}1${NC}  Visual Builder    ${YELLOW}adk web${NC}"
    echo -e "  ${BOLD}2${NC}  Kigali Agent      ${YELLOW}adk run${NC} — CLI agent with tools"
    echo -e "  ${BOLD}3${NC}  Browser Agent     ${YELLOW}adk run${NC} — controls Chrome live"
    echo ""
    echo -e "  ${BOLD}Study Jam #2 — Voice AI${NC}"
    echo -e "  ${BOLD}v1${NC} Hello Gemini      Basic connection, hear AI speak"
    echo -e "  ${BOLD}v2${NC} Voice Gallery     Compare 4 different voices"
    echo -e "  ${BOLD}v3${NC} Conversation      Multi-turn with memory"
    echo -e "  ${BOLD}v4${NC} Interactive       Audience types, AI responds"
    echo -e "  ${BOLD}v5${NC} Function Calling  Voice agent with tools"
    echo ""
    echo -e "  ${BOLD}check${NC}  Pre-flight check"
    echo ""
    read -p "  Pick a demo: " choice
    run_demo "$choice"
}

run_demo() {
    case "$1" in
        1)
            echo -e "\n${CYAN}${BOLD}Demo 1: Visual Builder${NC}"
            echo -e "Open ${YELLOW}http://localhost:8000${NC} in Chrome"
            cd "$CODE_DIR"
            adk web --port 8000
            ;;
        2)
            echo -e "\n${CYAN}${BOLD}Demo 2: Kigali Agent${NC}"
            echo -e "Try: ${YELLOW}\"Convert 500 USD to RWF\"${NC}"
            cd "$CODE_DIR/kigali_agent"
            adk run kigali_agent
            ;;
        3)
            if ! curl -s http://localhost:9222/json/version &>/dev/null; then
                echo -e "${RED}Chrome CDP not running!${NC}"
                exit 1
            fi
            echo -e "\n${CYAN}${BOLD}Demo 3: Browser Agent${NC}"
            echo -e "Try: ${YELLOW}\"List my open tabs\"${NC}"
            cd "$CODE_DIR/browser_agent"
            adk run browser_agent
            ;;
        v1|V1)
            echo -e "\n${CYAN}${BOLD}Voice Demo 1: Hello Gemini${NC}"
            cd "$VOICE_DIR"
            python3 demo_hello.py
            ;;
        v2|V2)
            echo -e "\n${CYAN}${BOLD}Voice Demo 2: Voice Gallery${NC}"
            cd "$VOICE_DIR"
            python3 demo_voices.py
            ;;
        v3|V3)
            echo -e "\n${CYAN}${BOLD}Voice Demo 3: Conversation${NC}"
            cd "$VOICE_DIR"
            python3 demo_conversation.py
            ;;
        v4|V4)
            echo -e "\n${CYAN}${BOLD}Voice Demo 4: Interactive${NC}"
            cd "$VOICE_DIR"
            python3 demo_interactive.py
            ;;
        v5|V5)
            echo -e "\n${CYAN}${BOLD}Voice Demo 5: Function Calling${NC}"
            cd "$VOICE_DIR"
            python3 demo_function_calling.py
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

if [ -n "$1" ]; then
    run_demo "$1"
else
    demo_menu
fi
