# Build with AI: Study Guide

## GDG Kigali — Study Jam #1 | March 20, 2026

**Talk:** Building Personalized AI Agents with Gemini, ADK, and MCP
**Speaker:** Timothy Olaleke, Google Developer Expert — Cloud

---

## Part 1: What is Google ADK?

Google's **Agent Development Kit (ADK)** is an open-source framework for building AI agents. Unlike simple chatbot wrappers, ADK gives you a complete stack:

| Component | What It Does |
|-----------|-------------|
| **Agent Framework** | Core Python/TS/Go/Java library for building agents |
| **Visual Builder** | No-code drag-and-drop agent creation |
| **Tools Catalog** | 50+ integrations (Google Search, GitHub, Stripe, etc.) |
| **AG-UI Protocol** | Turn any agent into a full web app |
| **Computer Use** | Agents can control web browsers |
| **A2A Protocol** | Agent-to-agent communication |
| **Sessions & Memory** | Persistent conversations across sessions |
| **Evaluation** | Test agents with criteria and simulated users |

### Key Concepts

- **Agent** — An AI-powered entity that can use tools to accomplish tasks
- **Tool** — A function the agent can call (search, calculate, browse, etc.)
- **Model** — The AI brain (Gemini 3 Flash, Gemini 3 Pro, etc.)
- **Instruction** — Plain English description of what the agent should do
- **Session** — A conversation with persistent memory

---

## Part 2: Setup

### Prerequisites
- Python 3.10 or later
- A Google account (Gmail)

### Step 1: Install ADK

```bash
pip install google-adk
```

### Step 2: Get a Free API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Gmail account
3. Click "Create API Key"
4. Copy the key

No credit card required. Free tier is generous for learning and prototyping.

### Step 3: Set Environment Variable

```bash
export GOOGLE_API_KEY="your_key_here"
```

Or create a `.env` file:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_key_here
```

### Verify Installation

```bash
adk --version
adk web --port 8000
```

If the web UI opens at localhost:8000, you're ready!

---

## Part 3: Building Your First Agent

### Method A: Visual Builder (No Code)

1. Run `adk web --port 8000`
2. Open http://localhost:8000
3. Click the **+** button
4. Set:
   - **Name:** `my_first_agent`
   - **Model:** Gemini 3 Flash
   - **Instruction:** "You are a helpful assistant that can search the web for current information."
5. Add the **Google Search** tool
6. Click Save and test in the chat panel

### Method B: Python Code

Create this file structure:
```
kigali_agent/
  __init__.py
  agent.py
  .env
```

**kigali_agent/__init__.py:**
```python
from . import agent
```

**kigali_agent/agent.py:**
```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="kigali_ai",
    model="gemini-3-flash-preview",
    instruction=(
        "You are a helpful AI assistant for entrepreneurs "
        "in Kigali, Rwanda. Use Google Search for current data. "
        "You speak English, French, and Kinyarwanda."
    ),
    tools=[google_search],
)
```

**kigali_agent/.env:**
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_key_here
```

Run it:
```bash
adk run kigali_agent
```

### Test Prompts
- "What is the current population of Kigali?"
- "What are the top 3 tech hubs in Rwanda?"
- "What is the exchange rate from USD to RWF today?"
- "Who are the GDG organizers in Kigali?"

---

## Part 4: Adding Custom Tools

Any Python function can be a tool. ADK reads the docstring and type hints to understand what the function does.

### Example: Currency Converter

```python
import json
import urllib.request

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert between currencies using live exchange rates.

    Args:
        amount: The amount to convert.
        from_currency: Source currency code (e.g. USD, EUR, RWF).
        to_currency: Target currency code (e.g. USD, EUR, RWF).

    Returns:
        dict: Conversion result with rate and converted amount.
    """
    url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
    with urllib.request.urlopen(url, timeout=5) as r:
        data = json.loads(r.read())
    rate = data["rates"].get(to_currency.upper())
    if not rate:
        return {"error": f"Unknown currency: {to_currency}"}
    return {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "rate": rate,
        "original": amount,
        "converted": round(amount * rate, 2),
    }
```

### Example: Business Metrics Calculator

```python
def calculate_business_metrics(revenue: float, costs: float, num_customers: int) -> dict:
    """Calculate key business metrics from basic inputs.

    Args:
        revenue: Total revenue in any currency.
        costs: Total costs/expenses in the same currency.
        num_customers: Number of customers served.

    Returns:
        dict: Profit, margin, revenue per customer, and health rating.
    """
    profit = revenue - costs
    margin = (profit / revenue * 100) if revenue > 0 else 0
    rpc = revenue / num_customers if num_customers > 0 else 0
    health = "Healthy" if margin > 20 else "Okay" if margin > 0 else "Needs attention"
    return {
        "profit": round(profit, 2),
        "margin_percent": round(margin, 1),
        "revenue_per_customer": round(rpc, 2),
        "health": health,
    }
```

### Add tools to your agent:

```python
root_agent = Agent(
    name="kigali_ai",
    model="gemini-3-flash-preview",
    instruction="You are a business assistant for Kigali entrepreneurs.",
    tools=[google_search, convert_currency, calculate_business_metrics],
)
```

### Rules for Custom Tools
1. Use **type hints** for all parameters
2. Write a **clear docstring** with Args section
3. Return a **dict** (ADK converts it for the model)
4. Keep functions **simple and focused** — one tool = one job

---

## Part 5: Browser Agent (ADK + Chrome CDP)

This is the advanced section. We'll build an AI agent that controls your real Chrome browser.

### How it works

```
You → ADK Agent (Gemini) → CDP commands → Your Chrome browser
```

**Chrome DevTools Protocol (CDP)** is Chrome's built-in remote control API. When Chrome runs with `--remote-debugging-port=9222`, it exposes HTTP and WebSocket endpoints for full browser control.

### Setup

Start Chrome with debugging enabled:
```bash
# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222

# Windows
chrome.exe --remote-debugging-port=9222
```

Install dependencies:
```bash
pip install google-adk requests websocket-client
```

### The Code

See `code/browser_agent/agent.py` for the full implementation. Key tools:

| Tool | What It Does |
|------|-------------|
| `list_tabs()` | List all open browser tabs |
| `open_url(url)` | Open a new tab with a URL |
| `get_page_text()` | Read the visible text of the current page |
| `take_screenshot()` | Capture the screen to a PNG file |
| `click_element(selector)` | Click an element by CSS selector |
| `run_javascript(code)` | Execute JavaScript on the page |

### Test It

```bash
cd code/browser_agent
adk run browser_agent
```

Try:
- "List my open tabs"
- "Open https://gdg.community.dev and tell me what's on the page"
- "Take a screenshot"
- "Click the login button"

---

## Part 6: AG-UI — Agent as a Web App

Turn your agent into a full React web app with one command:

```bash
npx copilotkit@latest create -f adk
```

This scaffolds:
- React frontend with chat interface
- Streaming responses
- Shared state between UI and agent
- Your ADK agent as the backend

```bash
export GOOGLE_API_KEY="your_key"
npm install && npm run dev
```

Open http://localhost:3000 — your agent is now a web app!

---

## Part 7: Deploy to Cloud Run

### Create a Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install google-adk
EXPOSE 8080
CMD ["adk", "api_server", "--port", "8080", "kigali_agent"]
```

### Deploy

```bash
gcloud run deploy kigali-agent \
  --source . \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY \
  --allow-unauthenticated
```

Your agent is now live with a public URL!

---

## Exercises

### Exercise 1: Build Your Own Agent (Beginner)
Create an agent that helps students find scholarships in East Africa. It should:
- Use Google Search to find current scholarship opportunities
- Filter by country and field of study
- Provide application deadlines

### Exercise 2: Add a Custom Tool (Intermediate)
Add a tool to the kigali_agent that fetches weather data:
```python
def get_weather(city: str) -> dict:
    """Get current weather for a city."""
    # Use wttr.in free API
    url = f"https://wttr.in/{city}?format=j1"
    # ... implement this
```

### Exercise 3: Multi-Agent System (Advanced)
Create two agents that work together:
1. A **researcher** agent that searches the web
2. An **analyst** agent that processes the research

Use ADK's multi-agent features to connect them.

### Exercise 4: Browser Automation (Advanced)
Extend the browser agent with a new tool:
```python
def fill_form(selector: str, value: str) -> dict:
    """Fill a form field with a value."""
    # ... implement using CDP
```

---

## Cheat Sheet

### ADK CLI Commands
```bash
adk web --port 8000        # Launch Visual Builder
adk run <agent_folder>     # Run agent in terminal
adk api_server <agent>     # Start API server
adk eval <agent>           # Run evaluations
```

### Agent Template
```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="agent_name",
    model="gemini-3-flash-preview",
    instruction="What the agent should do.",
    tools=[google_search],
)
```

### File Structure
```
my_agent/
  __init__.py          # from . import agent
  agent.py             # Agent definition
  .env                 # API keys
```

### Useful Models
| Model | Best For |
|-------|---------|
| `gemini-3-flash-preview` | Fast, cheap, great for most tasks |
| `gemini-3-pro-preview` | Complex reasoning, longer context |
| `gemini-2.5-flash` | Stable, well-tested |

---

## Resources

| Resource | Link |
|----------|------|
| ADK Documentation | google.github.io/adk-docs/ |
| ADK GitHub | github.com/google/adk-python |
| Google AI Studio | aistudio.google.com |
| AG-UI Protocol | docs.ag-ui.com |
| Gemini Docs | ai.google.dev/gemini-api/docs |
| This Repo | github.com/Timtech4u/build-with-ai-kigali |

### Blog Posts by Timothy (Published)
- [Building and Deploying AI Agents with Google's ADK — Part 1](https://timtech4u.medium.com/building-and-deploying-ai-agents-in-minutes-with-googles-adk-part-1-abbf2ed43486)
- [Enhancing Agents with Multimodal Capabilities: ADK + MCP — Part 2](https://timtech4u.medium.com/enhancing-agents-with-multimodal-capabilities-adk-mcp-part-2-of-3-25d6eb243d42)
- [Usebelha — Multi-Tenant AI Customer Support with Google ADK](https://timtech4u.medium.com/usebelha-multi-tenant-ai-customer-support-with-google-adk-5b46e2575f25)
- [Building AI Agents with Google ADK, FastAPI, and MCP](https://dev.to/timtech4u/building-ai-agents-with-google-adk-fastapi-and-mcp-26h7)

---

**Next Session:** Study Jam #2 — March 27, 2026 at the same venue!

*Prepared by Timothy Olaleke | Google Developer Expert — Cloud | GDG Kigali*
