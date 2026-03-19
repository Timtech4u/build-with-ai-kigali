"""Kigali AI — A helpful agent for entrepreneurs and developers in Kigali, Rwanda.

Build with AI: Study Jam #1 — GDG Kigali, March 20, 2026
Speaker: Timothy Olaleke, Google Developer Expert — Cloud
"""

import json
import urllib.request
from google.adk.agents import Agent
from google.adk.tools import google_search


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert between currencies using live exchange rates.

    Args:
        amount: The amount to convert.
        from_currency: Source currency code (e.g. USD, EUR, RWF, KES, NGN).
        to_currency: Target currency code (e.g. USD, EUR, RWF, KES, NGN).

    Returns:
        dict: Conversion result with rate and converted amount.
    """
    try:
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
    except Exception as e:
        return {"error": str(e)}


def calculate_business_metrics(
    revenue: float, costs: float, num_customers: int
) -> dict:
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


root_agent = Agent(
    name="kigali_ai",
    model="gemini-3-flash-preview",
    instruction=(
        "You are a smart, friendly AI assistant for entrepreneurs and developers "
        "in Kigali, Rwanda. You help with business questions, currency conversions, "
        "market research, and technical topics.\n\n"
        "You speak English, French, and Kinyarwanda fluently.\n\n"
        "When asked about prices or costs, always convert to RWF for local context.\n"
        "Use Google Search for current information about markets, trends, or regulations.\n"
        "Keep answers practical, actionable, and concise."
    ),
    tools=[google_search, convert_currency, calculate_business_metrics],
)
