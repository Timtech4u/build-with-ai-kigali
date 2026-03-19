---
marp: true
theme: default
paginate: true
backgroundColor: #ffffff
color: #202124
style: |
  section {
    font-family: 'Google Sans', 'Segoe UI', sans-serif;
    padding: 40px 60px;
  }
  h1 {
    color: #1a73e8;
    font-size: 2.2em;
    margin-bottom: 0.3em;
  }
  h2 {
    color: #1a73e8;
    font-size: 1.6em;
  }
  h3 {
    color: #137333;
    font-size: 1.2em;
  }
  code {
    background: #f1f3f4;
    color: #37474f;
    padding: 2px 6px;
    border-radius: 4px;
  }
  pre {
    background: #f8f9fa;
    border: 1px solid #dadce0;
    border-radius: 8px;
    font-size: 0.75em;
  }
  a { color: #1a73e8; }
  strong { color: #d93025; }
  em { color: #5f6368; font-style: normal; }
  table { font-size: 0.82em; width: 100%; }
  th { background: #e8f0fe; color: #1a73e8; }
  td { padding: 8px 12px; }
  blockquote {
    border-left: 4px solid #1a73e8;
    background: #e8f0fe;
    padding: 12px 20px;
    margin: 16px 0;
    border-radius: 0 8px 8px 0;
    font-size: 1.1em;
  }
  blockquote p { margin: 0; }
  .small { font-size: 0.7em; color: #5f6368; }
---

# Building Personalized AI Agents
# with Gemini, ADK, and MCP

**Timothy Olaleke**
Google Developer Expert — Cloud

*GDG Kigali — Build with AI: Study Jam #1*
*March 20, 2026*

---

# What if your AI assistant...

Knew **your browser tabs**?

Could **click buttons** and **fill forms** for you?

Could **search the web** with your context?

Could **remember** your preferences across sessions?

Today, you'll build exactly that — in **under 30 minutes**.

---

# What We're Building

### Three levels, one toolkit

| | What | How |
|---|------|-----|
| 1 | A personalized AI assistant | **10 lines of Python** |
| 2 | An agent that controls your browser | **ADK + Chrome CDP** |
| 3 | Deploy your agent | **One command** |

All **free**. All **open source**. No credit card.

---

# What Makes an Agent "Personalized"?

A chatbot gives **generic** answers.

A personalized agent knows **your context**:

> Your tools. Your data. Your browser. Your preferences.

### How ADK makes this possible:

- **Custom tools** — wrap any Python function
- **Memory** — remembers across sessions
- **MCP** — connects to your existing tools
- **Chrome CDP** — sees and controls your real browser

---

# Meet Google ADK

**Agent Development Kit** — the complete toolkit for AI agents

| | |
|---|---|
| **Code-first** | Agents are Python objects, not prompt chains |
| **Visual Builder** | No-code drag-and-drop creation |
| **50+ integrations** | Google Search, GitHub, Stripe, BigQuery... |
| **MCP support** | Connect any tool, consume or expose |
| **Memory** | Short-term sessions + long-term recall |
| **v1.26** | Production-stable, used at scale |

```bash
pip install google-adk
```

*Python, TypeScript, Java — open source*

---

# ADK vs. The Rest

| | ADK | LangChain | CrewAI |
|---|:---:|:---------:|:------:|
| Visual Builder | Yes | — | — |
| Free Gemini access | Yes | — | — |
| Browser control | Yes | — | — |
| MCP (bidirectional) | Yes | Partial | — |
| Agent-to-Agent (A2A) | Yes | — | — |
| Built-in Web UI | Yes | — | — |

**ADK is a complete platform, not just a library.**

---

# Setup — 2 Minutes

### Step 1: Install

```bash
pip install google-adk
```

### Step 2: Free API key

Go to **aistudio.google.com/apikey** — sign in with Gmail, create key.

### Step 3: Set it

```bash
export GOOGLE_API_KEY="your_key_here"
```

### Step 4: Verify

```bash
adk web --port 8000    # Opens the Visual Builder
```

---

# Visual Builder — Zero Code

Launch it:
```bash
adk web --port 8000
```

Then in your browser:

1. Click **+** to create an agent
2. Pick **Gemini 3 Flash** as the model
3. Write instructions in plain English
4. Add tools from the catalog
5. Test it live in the chat panel

![w:700](img/adk-web-ui.png)

---

# Your First Agent — 10 Lines

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="kigali_ai",
    model="gemini-3-flash-preview",
    instruction=(
        "You are a helpful AI assistant for entrepreneurs "
        "in Kigali. Use Google Search for current data. "
        "You speak English, French, and Kinyarwanda."
    ),
    tools=[google_search],
)
```

```bash
adk run kigali_agent
```

*Ask it: "What's the mobile money market size in Rwanda?"*

---

# Make It Personal — Custom Tools

Any Python function becomes a tool. ADK reads the docstring automatically.

```python
def convert_currency(amount: float, from_cur: str, to_cur: str) -> dict:
    """Convert between currencies using live exchange rates."""
    url = f"https://open.er-api.com/v6/latest/{from_cur}"
    data = json.loads(urllib.request.urlopen(url).read())
    rate = data["rates"][to_cur.upper()]
    return {"converted": round(amount * rate, 2), "rate": rate}
```

Add it to your agent:

```python
tools=[google_search, convert_currency]
```

*"Convert 500 USD to RWF" — and it just works.*

---

<!-- _backgroundColor: #e8f0fe -->

# The Highlight

## Give Your AI Eyes and Hands

### Chrome DevTools Protocol (CDP)

---

# What is Chrome CDP?

Chrome has a **built-in remote control API**.

Every Chrome browser. Already installed. Free.

```bash
# Start Chrome with debugging enabled
google-chrome --remote-debugging-port=9222
```

Now any program can:

| Action | How |
|--------|-----|
| List open tabs | `GET /json/list` |
| Open a new tab | `PUT /json/new?https://google.com` |
| Run JavaScript | WebSocket + `Runtime.evaluate` |
| Take screenshots | WebSocket + `Page.captureScreenshot` |
| Click elements | WebSocket + JS injection |

![w:600](img/cdp-json-list.png)

---

# Why CDP is a Game-Changer

> *"Give your AI agent eyes and hands in the browser"*
> — Addy Osmani, Google Chrome team

### Before CDP:
Your agent generates code **blindly** — it can't see the result.

### With CDP:
Your agent can **see the page**, **interact with it**, and **verify** what happened.

**Closed-loop**: Generate → Execute → Observe → Fix → Repeat

Google launched **Chrome DevTools MCP** — an official MCP server with **29 browser tools**. This is the direction Google is investing in.

---

# Build a Browser Agent

```python
root_agent = Agent(
    name="browser_agent",
    model="gemini-2.5-flash",
    instruction="You control Chrome via CDP. Be concise.",
    tools=[
        list_tabs,        # See what's open
        open_url,         # Navigate anywhere
        get_page_text,    # Read page content
        take_screenshot,  # Capture the screen
        click_element,    # Click by CSS selector
        run_javascript,   # Run any JS on the page
    ],
)
```

Each tool is a simple Python function that talks to Chrome over CDP.

**Full code in the repo** — `code/browser_agent/agent.py`

---

# How It Works

```
You: "Open gdg.community.dev and find upcoming events"

   ┌─────────────────────────────┐
   │   ADK Agent (Gemini 3)      │
   │   Decides which tools to    │
   │   call and in what order    │
   └──────────┬──────────────────┘
              │
   ┌──────────▼──────────────────┐
   │  1. open_url(gdg.community) │──► Chrome opens new tab
   │  2. get_page_text()         │──► Reads the page
   │  3. click_element(".events")│──► Clicks events link
   │  4. get_page_text()         │──► Reads event list
   └─────────────────────────────┘
              │
   ┌──────────▼──────────────────┐
   │  "Here are 3 upcoming       │
   │   events in Kigali..."      │
   └─────────────────────────────┘
```

**Your real Chrome. Your cookies. Your logged-in sessions.**

---

# MCP — Connect to Everything

**Model Context Protocol** — the universal plug for AI agents.

Your ADK agent can **consume** MCP tools and **expose** itself as an MCP server.

### What this means:

```
Your Agent
   ├── Google Search (built-in)
   ├── Chrome CDP tools (your code)
   ├── GitHub MCP server
   ├── Slack MCP server
   ├── Google Workspace MCP tools
   └── Any MCP server you want
```

### Example: Google Workspace CLI

The `@googleworkspace/cli` has **49 MCP-compatible skills** — Gmail, Drive, Calendar, Sheets, Docs. Your agent can read your email and update your spreadsheets.

---

# Sessions — Conversational Memory

ADK agents remember context **within a conversation** using sessions.

```python
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
# Agent keeps context across multiple turns
# Knows what you asked before, what tools returned
```

### What this enables:
- Multi-turn conversations with context
- Tool results carry forward between turns
- Agent builds on previous answers

### Coming soon:
- **Long-term memory** across sessions (Memory Bank API)
- Store user preferences, past interactions

*Sessions + custom tools = personalization without complexity.*

---

# Web App & Deployment Options

### Option 1: ADK Web UI (Built-in)
```bash
adk web --port 8000    # Chat UI + Visual Builder included
```

### Option 2: AG-UI Protocol (React App)
```bash
npx copilotkit@latest create -f adk
npm install && npm run dev
```
Scaffolds a **React frontend** with streaming chat, shared state, and your ADK agent as backend.

### Option 3: API Server
```bash
adk api_server kigali_agent --port 8080
```
Exposes your agent as a REST API — connect any frontend.

---

# Deploy to Cloud Run

```bash
gcloud run deploy kigali-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

Your agent is **live on the internet**. Public URL. Free tier.

### The full stack:

```
ADK Agent (Python)
   + Gemini 3 Flash (free API key)
   + Custom tools (your code)
   + Chrome CDP (browser control)
   + MCP (external integrations)
   + Cloud Run (deployment)
```

**Zero to production in 25 minutes.**

---

# What You Built Today

| What | How | Time |
|------|-----|------|
| Personalized AI assistant | 10 lines of Python | 5 min |
| No-code agent | Visual Builder | 2 min |
| Browser-controlling agent | ADK + Chrome CDP | 10 min |
| API server / Web UI | `adk web` or `adk api_server` | 3 min |
| Cloud deployment | `gcloud run deploy` | 5 min |

**Total: ~25 minutes. All free. All open source.**

---

# Your Turn — Exercises

### Beginner
1. Install ADK, get your API key
2. Build an agent with the Visual Builder

### Intermediate
3. Modify `kigali_agent` — add your own custom tool
4. Try the browser agent with your Chrome

### Advanced
5. Connect an MCP server to your agent
6. Deploy to Cloud Run

**Code + study guide:** github.com/Timtech4u/build-with-ai-kigali

---

# Resources

| | |
|---|---|
| **ADK Docs** | google.github.io/adk-docs/ |
| **ADK GitHub** | github.com/google/adk-python |
| **Free API Key** | aistudio.google.com/apikey |
| **Chrome DevTools MCP** | github.com/AidenYuanDev/chrome-devtools-mcp |
| **AG-UI Protocol** | docs.ag-ui.com |
| **GWS CLI (MCP tools)** | github.com/googleworkspace/cli |
| **Code + Study Guide** | github.com/Timtech4u/build-with-ai-kigali |

### Blog posts by Timothy
- Building and Deploying AI Agents with Google ADK (Part 1 & 2)
- Build an AI Agent That Controls Your Browser (ADK + CDP)

---

<!-- _backgroundColor: #e8f0fe -->

# Thank You!

## Timothy Olaleke

**Google Developer Expert — Cloud**

timtech4u.dev | @timtech4u | github.com/Timtech4u

*See you at Study Jam #2 on March 27!*

*Slides, code, and study guide:*
**github.com/Timtech4u/build-with-ai-kigali**
