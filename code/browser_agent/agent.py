"""Browser Agent — AI agent that controls your Chrome browser via CDP.

Build with AI: Study Jam #1 — GDG Kigali, March 20, 2026
Speaker: Timothy Olaleke, Google Developer Expert — Cloud

Prerequisites:
  - Chrome running with: --remote-debugging-port=9222
  - pip install google-adk requests websocket-client
"""

import json
import base64
import requests
import websocket
from google.adk.agents import Agent

CHROME_HOST = "http://localhost:9222"


def _cdp_send(ws_url: str, method: str, params: dict = None) -> dict:
    """Send a CDP command over WebSocket and return the result."""
    ws = websocket.create_connection(ws_url)
    try:
        msg = {"id": 1, "method": method, "params": params or {}}
        ws.send(json.dumps(msg))
        while True:
            data = json.loads(ws.recv())
            if data.get("id") == 1:
                return data.get("result", {})
    finally:
        ws.close()


def _get_tabs() -> list:
    """Get all open Chrome tabs via CDP HTTP endpoint."""
    resp = requests.get(f"{CHROME_HOST}/json/list")
    return resp.json()


def _get_first_page_ws() -> str | None:
    """Get the WebSocket URL for the first page tab."""
    tabs = _get_tabs()
    pages = [t for t in tabs if t.get("type") == "page"]
    return pages[0]["webSocketDebuggerUrl"] if pages else None


# --- Tool Functions ---


def list_tabs() -> dict:
    """List all open browser tabs with their titles and URLs."""
    tabs = _get_tabs()
    result = []
    for i, tab in enumerate(tabs):
        if tab.get("type") == "page":
            result.append({
                "index": i,
                "title": tab.get("title", ""),
                "url": tab.get("url", "")
            })
    return {"tabs": result, "count": len(result)}


def open_url(url: str) -> dict:
    """Open a new browser tab with the given URL.

    Args:
        url: The full URL to open (e.g. https://example.com).
    """
    resp = requests.put(f"{CHROME_HOST}/json/new?{url}")
    tab = resp.json()
    return {"status": "success", "opened": url, "title": tab.get("title", "")}


def get_page_text() -> dict:
    """Get the visible text content of the current page (first 3000 characters)."""
    ws_url = _get_first_page_ws()
    if not ws_url:
        return {"error": "No tabs open"}
    result = _cdp_send(
        ws_url, "Runtime.evaluate",
        {"expression": "document.body.innerText.substring(0, 3000)"}
    )
    text = result.get("result", {}).get("value", "")
    return {"status": "success", "text": text, "length": len(text)}


def take_screenshot() -> dict:
    """Take a screenshot of the current page and save it to /tmp."""
    ws_url = _get_first_page_ws()
    if not ws_url:
        return {"error": "No tabs open"}
    result = _cdp_send(ws_url, "Page.captureScreenshot")
    img_data = base64.b64decode(result.get("data", ""))
    path = "/tmp/agent-screenshot.png"
    with open(path, "wb") as f:
        f.write(img_data)
    return {"status": "success", "saved": path, "size_bytes": len(img_data)}


def click_element(selector: str) -> dict:
    """Click an element on the page using a CSS selector.

    Args:
        selector: CSS selector for the element to click (e.g. 'button.submit', '#login').
    """
    ws_url = _get_first_page_ws()
    if not ws_url:
        return {"error": "No tabs open"}
    js = f"""(() => {{
        const el = document.querySelector('{selector}');
        if (!el) return 'Element not found: {selector}';
        el.click();
        return 'Clicked: ' + el.tagName + ' ' + (el.textContent || '').substring(0, 50);
    }})()"""
    result = _cdp_send(ws_url, "Runtime.evaluate", {"expression": js})
    return {"status": "success", "result": result.get("result", {}).get("value", "")}


def run_javascript(code: str) -> dict:
    """Execute JavaScript code on the current page and return the result.

    Args:
        code: JavaScript code to evaluate in the page context.
    """
    ws_url = _get_first_page_ws()
    if not ws_url:
        return {"error": "No tabs open"}
    result = _cdp_send(ws_url, "Runtime.evaluate", {"expression": code})
    return {"status": "success", "result": result.get("result", {}).get("value", "")}


# --- The Agent ---

root_agent = Agent(
    name="browser_agent",
    model="gemini-3-flash-preview",
    description="An AI agent that controls your Chrome browser via CDP.",
    instruction="""You are a browser control agent. You can open tabs, read page content,
take screenshots, click elements, and run JavaScript — all in the user's real Chrome browser.

When the user asks you to do something with their browser, use the appropriate tool.
Always confirm what you did after each action. Be concise but informative.""",
    tools=[
        list_tabs,
        open_url,
        get_page_text,
        take_screenshot,
        click_element,
        run_javascript,
    ],
)
