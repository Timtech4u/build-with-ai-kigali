# Build with AI: Study Jam #1 — GDG Kigali

> **Build an AI agent that controls your browser, searches the web, and converts currencies — in under 30 minutes. No experience needed.**

| | |
|---|---|
| **Event** | Build with AI: Study Jam #1 |
| **Date** | Friday, March 20, 2026 at 6:00 PM EAT |
| **Venue** | Digital Transformation Center Rwanda, KG 541 St, Career Center 7th Floor, Kigali |
| **Speaker** | [Timothy Olaleke](https://timtech4u.dev) — Google Developer Expert for Cloud |
| **Slides** | [View Live Slides](https://timtech4u.dev/build-with-ai-kigali/slides/slides.html) |
| **Live Agent** | [Try the Kigali Agent](https://kigali-agent-617693036026.us-central1.run.app/dev-ui/) |

---

## What You'll Learn

In this hands-on study jam, you'll build **real AI agents** that can:

1. **Search the web** and answer questions using Google Search
2. **Convert currencies** with live exchange rates (USD to RWF and more)
3. **Control your Chrome browser** — open tabs, read pages, click buttons, take screenshots
4. **Deploy to the cloud** with a single command

All of this using **Google's Agent Development Kit (ADK)** and **Gemini** — completely free, no credit card needed.

---

## What's In This Repo

| Folder | What's Inside | Who It's For |
|--------|--------------|--------------|
| [`slides/`](slides/) | Presentation slides ([view online](https://timtech4u.dev/build-with-ai-kigali/slides/slides.html)) | Everyone |
| [`study-materials/`](study-materials/) | Step-by-step study guide + cheat sheet | Self-study after the event |
| [`code/kigali_agent/`](code/kigali_agent/) | Your first AI agent — 10 lines of Python | Beginners |
| [`code/browser_agent/`](code/browser_agent/) | AI agent that controls Chrome | Intermediate |
| [`DEMO-GUIDE.md`](DEMO-GUIDE.md) | Live demo walkthrough | Speakers / self-learners |

---

## Get Started (5 Minutes)

### What You Need
- **Python 3.10+** installed on your computer
- A **Gmail account** (for the free API key)
- That's it!

### Step 1: Install Google ADK

```bash
pip install google-adk
```

### Step 2: Get Your Free API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Gmail
3. Click **"Create API Key"** — copy it

### Step 3: Set Your Key

```bash
export GOOGLE_API_KEY="paste_your_key_here"
```

### Step 4: Run Your First Agent

```bash
git clone https://github.com/Timtech4u/build-with-ai-kigali.git
cd build-with-ai-kigali/code/kigali_agent
adk run kigali_agent
```

Try asking it:
- *"What is the population of Kigali?"*
- *"Convert 500 USD to RWF"*
- *"I have revenue of 50000, costs of 35000, and 200 customers. How's my business?"*

### Step 5: Try the Visual Builder (No Code)

```bash
adk web --port 8000
```

Open http://localhost:8000 — drag, drop, and build agents visually!

---

## The Browser Agent (The Cool Part)

Want your AI to control your actual Chrome browser? Start Chrome with debugging enabled:

```bash
# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222

# Windows
chrome.exe --remote-debugging-port=9222
```

Then run the browser agent:

```bash
cd code/browser_agent
pip install requests websocket-client
adk run browser_agent
```

Try:
- *"List my open tabs"*
- *"Open https://gdg.community.dev and tell me what's on the page"*
- *"Take a screenshot"*

Your AI agent can now see and interact with your real browser!

---

## Exercises

After the study jam, try these challenges:

| Level | Challenge |
|-------|-----------|
| Beginner | Build an agent using only the Visual Builder |
| Beginner | Add a weather tool using the [wttr.in API](https://wttr.in) |
| Intermediate | Add a new custom tool to `kigali_agent` |
| Intermediate | Make the browser agent fill out a form |
| Advanced | Connect an [MCP server](https://github.com/modelcontextprotocol) to your agent |
| Advanced | Deploy your agent to [Google Cloud Run](https://cloud.google.com/run) |

---

## Resources

| Resource | Link |
|----------|------|
| ADK Documentation | [google.github.io/adk-docs](https://google.github.io/adk-docs/) |
| ADK GitHub | [github.com/google/adk-python](https://github.com/google/adk-python) |
| Free API Key | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| Gemini Developer Guide | [ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs) |
| Chrome DevTools Protocol | [chromedevtools.github.io/devtools-protocol](https://chromedevtools.github.io/devtools-protocol/) |
| Google Workspace CLI (MCP) | [github.com/googleworkspace/cli](https://github.com/googleworkspace/cli) |

### Blog Posts
- [Building and Deploying AI Agents with Google's ADK — Part 1](https://timtech4u.medium.com/building-and-deploying-ai-agents-in-minutes-with-googles-adk-part-1-abbf2ed43486)
- [Enhancing Agents with Multimodal Capabilities: ADK + MCP — Part 2](https://timtech4u.medium.com/enhancing-agents-with-multimodal-capabilities-adk-mcp-part-2-of-3-25d6eb243d42)
- [Building AI Agents with Google ADK, FastAPI, and MCP](https://dev.to/timtech4u/building-ai-agents-with-google-adk-fastapi-and-mcp-26h7)
- [Multi-Tenant AI Customer Support with Google ADK](https://timtech4u.medium.com/usebelha-multi-tenant-ai-customer-support-with-google-adk-5b46e2575f25)

---

## Speaker

**Timothy Olaleke** — [timtech4u.dev](https://timtech4u.dev) | [@timtech4u](https://x.com/timtech4u) | [GitHub](https://github.com/Timtech4u)

Google Developer Expert for Cloud | GDG Kigali
