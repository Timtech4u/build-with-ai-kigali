# Build with AI: Study Jam #1 — GDG Kigali

This repo contains materials from the "Build with AI" study jam by Timothy Olaleke (GDE Cloud).

## Project Structure

- `code/kigali_agent/` — AI agent with currency conversion & business metrics tools (Google ADK + Gemini)
- `code/browser_agent/` — AI agent that controls Chrome via DevTools Protocol
- `code/ten_line_agent/` — Minimal 10-line agent example
- `code/Dockerfile` — Deploys any agent to Google Cloud Run
- `slides/` — Presentation slides
- `study-materials/` — Step-by-step guide & cheat sheet

## Tech Stack

- **Framework:** Google Agent Development Kit (ADK) — `google-adk`
- **Model:** Gemini 2.5 Flash
- **Language:** Python 3.12
- **Deployment:** Google Cloud Run

## Quick Start

```bash
pip install google-adk
export GOOGLE_API_KEY="your_key_from_aistudio.google.com/apikey"
cd code
adk web
```

## Key Patterns

- Agents are defined in `agent.py` with a `root_agent` variable
- Each agent folder has `__init__.py` and `agent.py`
- Tools are plain Python functions with docstrings (ADK uses docstrings for tool descriptions)
- Deploy with: `gcloud run deploy --source ./code --region us-central1 --allow-unauthenticated`

## Live Demo

- Agent UI: https://kigali-agent-617693036026.us-central1.run.app/dev-ui/?app=kigali_agent
