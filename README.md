# Build with AI — GDG Kigali 2026

> **A 2-part hands-on series: build AI agents that think, act, and speak.**

| | |
|---|---|
| **Event** | Build with AI — GDG Cloud Kigali |
| **Venue** | Digital Transformation Center Rwanda, KG 541 St, Career Center 7th Floor, Kigali |
| **Speaker** | [Timothy Olaleke](https://timtech4u.dev) — Google Developer Expert for Cloud |
| **Participants** | ~150 per session |

---

## Sessions

### Study Jam #1 — AI Agents (March 20, 2026)

**Topic:** Building Personalized AI Agents with Gemini, ADK, and MCP

Build text-based AI agents that search the web, convert currencies, control Chrome, and deploy to the cloud.

- **Slides:** [View online](https://timtech4u.dev/build-with-ai-kigali/slides/slides.html) | [`slides/slides.html`](slides/slides.html)
- **Code:** [`code/`](code/) (kigali_agent, browser_agent)
- **Run:** `./run.sh` (demos 1-3)

### Study Jam #2 — Voice AI (March 27, 2026)

**Topic:** Building Real-Time Voice AI with Gemini 3.1 Flash Live

Give your agents a voice. Real-time audio streaming, 30 HD voices, multi-turn conversations, function calling with voice.

- **Slides:** [View online](https://timtech4u.dev/build-with-ai-kigali/slides/studyjam2.html) | [`slides/studyjam2.html`](slides/studyjam2.html)
- **Code:** [`studyjam2-demos/`](studyjam2-demos/) (5 Python demos)
- **Run:** `./run.sh voice` (demos v1-v5)

---

## Quick Start

### Prerequisites

```bash
# Python 3.10+
python3 --version

# Get a free API key from https://aistudio.google.com/apikey
export GOOGLE_API_KEY="your-key-here"
```

### Clone and run

```bash
git clone https://github.com/Timtech4u/build-with-ai-kigali.git
cd build-with-ai-kigali
```

#### Study Jam #1 (Text Agents)
```bash
pip install google-adk
./run.sh 1    # Visual Builder (adk web)
./run.sh 2    # Kigali Agent (CLI)
./run.sh 3    # Browser Agent (CLI)
```

#### Study Jam #2 (Voice AI)
```bash
pip install google-genai
./run.sh v1   # Hello Gemini — hear the AI speak
./run.sh v2   # Voice Gallery — compare 4 voices
./run.sh v3   # Conversation — AI remembers across turns
./run.sh v4   # Interactive — audience types, AI responds with voice
./run.sh v5   # Function Calling — voice agent with tools
```

---

## What's In This Repo

```
build-with-ai-kigali/
├── README.md                  ← You are here
├── run.sh                     ← Demo launcher (both sessions)
│
├── slides/
│   ├── slides.md / .html      ← Study Jam #1 slides (Marp)
│   ├── studyjam2.md / .html   ← Study Jam #2 slides (Marp)
│   └── img/                   ← Screenshots for slides
│
├── code/                      ← Study Jam #1 code
│   ├── kigali_agent/          ← Text agent with tools
│   └── browser_agent/         ← Chrome-controlling agent
│
├── studyjam2-demos/           ← Study Jam #2 code
│   ├── demo_hello.py          ← Basic Live API connection + audio
│   ├── demo_voices.py         ← Compare 4 voices side by side
│   ├── demo_conversation.py   ← Multi-turn with memory
│   ├── demo_interactive.py    ← Audience-driven prompts
│   └── demo_function_calling.py ← Voice + tools (weather, currency)
│
├── study-materials/           ← Self-study guides
├── DEMO-GUIDE.md              ← Live demo walkthrough
└── AGENTS.md                  ← Agent architecture notes
```

---

## Resources

| Resource | Link |
|----------|------|
| **Google AI Studio** | [aistudio.google.com](https://aistudio.google.com) |
| **Voice Library (30 voices)** | [aistudio.google.com/apps/bundled/voice-library](https://aistudio.google.com/apps/bundled/voice-library) |
| **Live API Docs** | [ai.google.dev/gemini-api/docs/live](https://ai.google.dev/gemini-api/docs/live) |
| **ADK Docs** | [google.github.io/adk-docs](https://google.github.io/adk-docs/) |
| **Gemini API** | [ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs) |

### Blog Posts
- [Building and Deploying AI Agents with Google's ADK — Part 1](https://timtech4u.medium.com/building-and-deploying-ai-agents-in-minutes-with-googles-adk-part-1-abbf2ed43486)
- [Enhancing Agents with Multimodal Capabilities: ADK + MCP — Part 2](https://timtech4u.medium.com/enhancing-agents-with-multimodal-capabilities-adk-mcp-part-2-of-3-25d6eb243d42)
- [Your Browser Has a Remote Control — And Nobody Told You](https://dev.to/timtech4u/your-browser-has-a-remote-control-and-nobody-told-you-5e97)

---

## Speaker

**Timothy Olaleke** — [timtech4u.dev](https://timtech4u.dev) | [@timtech4u](https://x.com/timtech4u) | [GitHub](https://github.com/Timtech4u)

Google Developer Expert for Cloud | GDG Kigali
