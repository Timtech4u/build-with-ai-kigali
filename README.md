# Build with AI: Study Jam #1 - GDG Kigali

**Event:** Build with AI: Study Jam #1
**Date:** Friday, March 20, 2026 | 6:00 PM EAT
**Venue:** Digital Transformation Center Rwanda, KG 541 St, Career Center 7th Floor, Kigali
**Speaker:** Timothy Olaleke — Google Developer Expert for Cloud
**Series:** Part 1 of 2 study jams + hackathon

## Talk: Building Personalized AI Agents with Gemini, ADK, and MCP

Learn to build AI agents using Google's Agent Development Kit (ADK) and Gemini — from zero code to full deployment in under 30 minutes. SOLD OUT (149 RSVPs).

## Contents

```
slides/              # Presentation slides (Marp markdown → HTML/PDF)
study-materials/     # Student study guide, cheat sheet, exercises
code/
  kigali_agent/      # Method 1 & 2: Basic ADK agent with Google Search
  browser_agent/     # Bonus: Browser-controlling agent with ADK + CDP
```

## Quick Start

```bash
# 1. Install ADK
pip install google-adk

# 2. Get a free API key
# → https://aistudio.google.com/apikey

# 3. Set your key
export GOOGLE_API_KEY="your_key_here"

# 4. Run the basic agent
cd code/kigali_agent
adk run kigali_agent

# 5. Or launch the visual builder
adk web --port 8000
```

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK GitHub](https://github.com/google/adk-python)
- [Google AI Studio](https://aistudio.google.com/) (free API key)
- [AG-UI Protocol](https://docs.ag-ui.com)
- [Gemini Developer Guide](https://ai.google.dev/gemini-api/docs)

## Blog Posts by Timothy
- [Building and Deploying AI Agents with Google's ADK — Part 1](https://timtech4u.medium.com/building-and-deploying-ai-agents-in-minutes-with-googles-adk-part-1-abbf2ed43486)
- [Enhancing Agents with Multimodal Capabilities: ADK + MCP — Part 2](https://timtech4u.medium.com/enhancing-agents-with-multimodal-capabilities-adk-mcp-part-2-of-3-25d6eb243d42)
- [Building AI Agents with Google ADK, FastAPI, and MCP](https://dev.to/timtech4u/building-ai-agents-with-google-adk-fastapi-and-mcp-26h7)
- [Multi-Tenant AI Customer Support with Google ADK](https://timtech4u.medium.com/usebelha-multi-tenant-ai-customer-support-with-google-adk-5b46e2575f25)

## Speaker

Timothy Olaleke | [timtech4u.dev](https://timtech4u.dev) | [@timtech4u](https://x.com/timtech4u)
Google Developer Expert — Cloud | GDG Kigali
