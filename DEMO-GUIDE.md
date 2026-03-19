# Demo Guide — Build with AI: Study Jam #1

Step-by-step flow for the live demo. Follow this during the talk.

---

## Pre-Talk Setup (Do before audience arrives)

```bash
# 1. Open a terminal with your API key set
export GOOGLE_API_KEY="your_key_here"

# 2. Start Chrome with CDP enabled (if not already running)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222

# 3. Verify CDP is working
curl http://localhost:9222/json/version

# 4. Have the repo open
cd ~/TimTech/build-with-ai-kigali/code
```

---

## Demo 1: Visual Builder (Slide 8 — ~2 min)

```bash
adk web --port 8000
```

1. Open http://localhost:8000 in Chrome
2. Click **+** to create a new agent
3. Name it `demo_agent`
4. Select **Gemini 3 Flash** as the model
5. Type instruction: "You are a helpful assistant that can search the web."
6. Add **Google Search** tool
7. Test it: "What is the population of Kigali?"
8. Show the generated code in the sidebar

**Talking point:** "No code written. Real agent. Real search results."

---

## Demo 2: Code Agent (Slide 9 — ~5 min)

```bash
cd kigali_agent
adk run kigali_agent
```

### Test prompts (in order):
1. `What's the mobile money market size in Rwanda?`
   → Shows Google Search tool in action
2. `Convert 500 USD to RWF`
   → Shows custom tool (convert_currency)
3. `I have revenue of 50000 USD, costs of 35000, and 200 customers. How's my business?`
   → Shows calculate_business_metrics tool

**Talking point:** "Any Python function becomes a tool. The agent decides when to use it."

Press `Ctrl+C` to exit.

---

## Demo 3: Browser Agent (Slides 12-15 — ~10 min)

**This is the highlight. Take your time here.**

```bash
cd ../browser_agent
adk run browser_agent
```

### Test prompts (in order):
1. `List my open tabs`
   → Shows CDP reading real browser state
2. `Open https://gdg.community.dev and tell me what's on the page`
   → Watch Chrome open a new tab live
3. `Take a screenshot`
   → Saves a PNG to disk, show it
4. `Click on the "Find a chapter" link`
   → Agent interacts with the page

**Talking point:** "This is YOUR Chrome. YOUR cookies. YOUR logged-in sessions. The agent has eyes and hands."

Press `Ctrl+C` to exit.

---

## Demo 4: Show CDP Directly (Slide 12)

Open in Chrome: `http://localhost:9222/json/list`

**Talking point:** "This is all Chrome CDP is — a JSON endpoint. Every Chrome browser has this built in. Google officially supports using it for AI agents."

---

## Demo 5: Deploy (Slide 17 — ~3 min)

Show the Dockerfile:
```bash
cat ../Dockerfile
```

Show the deploy command (don't run it live unless you have time):
```bash
# Just show the command
echo 'gcloud run deploy kigali-agent --source . --region us-central1 --allow-unauthenticated'
```

**Talking point:** "One command. Your agent is live on the internet. Free tier."

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| ADK rate limit (429) | Use a fresh API key or wait 60s |
| Chrome CDP not connecting | Check `curl http://localhost:9222/json/version` |
| Agent not finding tools | Make sure you're in the right directory |
| `adk run` can't find agent | Run from the parent of the agent folder |
| Slow responses | Gemini 3 Flash is fast, but first call may take 2-3s |

---

## Slide-to-Demo Mapping

| Slide | Content | Demo |
|-------|---------|------|
| 1-3 | Intro, hook, overview | — |
| 4-5 | What's personalized, Meet ADK | — |
| 6 | ADK vs Rest | — |
| 7 | Setup | — |
| 8 | Visual Builder | **Demo 1** |
| 9 | First Agent code | **Demo 2** |
| 10 | Custom Tools | Part of Demo 2 |
| 11 | CDP intro section | — |
| 12 | What is CDP | **Demo 4** |
| 13 | Why CDP matters | — |
| 14 | Browser Agent code | **Demo 3** |
| 15 | How it works diagram | — |
| 16 | MCP | — |
| 17 | Sessions | — |
| 18 | Web App & Deploy options | **Demo 5** |
| 19 | Deploy to Cloud Run | Part of Demo 5 |
| 20 | What You Built | — |
| 21 | Exercises | — |
| 22 | Resources | — |
| 23 | Thank You | — |
