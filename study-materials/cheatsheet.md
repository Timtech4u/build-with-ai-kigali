# ADK Cheat Sheet

## CLI Commands
```bash
pip install google-adk          # Install
adk web --port 8000             # Visual Builder
adk run <agent_folder>          # Run in terminal
adk api_server <agent> --port 8080  # API server
```

## Agent Template
```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="my_agent",
    model="gemini-3-flash-preview",
    instruction="What the agent does.",
    tools=[google_search],
)
```

## File Structure
```
my_agent/
  __init__.py     # from . import agent
  agent.py        # Agent definition
  .env            # GOOGLE_API_KEY=xxx
```

## Custom Tool Template
```python
def my_tool(param1: str, param2: int) -> dict:
    """One-line description of what this tool does.

    Args:
        param1: What param1 is.
        param2: What param2 is.
    """
    # Your logic here
    return {"result": "value"}
```

## Models
| Model | Use Case |
|-------|----------|
| gemini-3-flash-preview | Fast, cheap, most tasks |
| gemini-3-pro-preview | Complex reasoning |
| gemini-2.5-flash | Stable, well-tested |

## Free API Key
1. Go to aistudio.google.com/apikey
2. Sign in with Gmail
3. Create key — done!

## AG-UI Web App
```bash
npx copilotkit@latest create -f adk
npm install && npm run dev
```

## Deploy to Cloud Run
```bash
gcloud run deploy my-agent \
  --source . --region us-central1 \
  --allow-unauthenticated
```

## Chrome CDP (Browser Agent)
```bash
# Start Chrome with debugging
google-chrome --remote-debugging-port=9222

# Check it works
curl http://localhost:9222/json/version
```

## Resources
- ADK Docs: google.github.io/adk-docs/
- AI Studio: aistudio.google.com
- AG-UI: docs.ag-ui.com
- This Repo: github.com/Timtech4u/build-with-ai-kigali
