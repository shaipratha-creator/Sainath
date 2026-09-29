import json
import os
from typing import Optional

try:
    from google import genai
except ImportError:
    genai = None


DEFAULT_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-1.5-flash",
)


# --------------------------------------------------
# Gemini client
# --------------------------------------------------

def _get_client():

    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )

    if not api_key:
        return None

    if genai is None:
        return None

    return genai.Client(
        api_key=api_key
    )


# --------------------------------------------------
# Fallback recommendations
# --------------------------------------------------

def _fallback(
    planner: str,
    data: dict
) -> dict:

    budget = float(
        data.get("budget", 0) or 0
    )

    # HOME
    if planner == "home":

        return {
            "planner": "Home Interior",
            "budget": budget,

            "summary":
                "A practical home setup organized around your budget.",

            "budget_allocation": {

                "Furniture":
                    round(budget * 0.40, 2),

                "Lighting":
                    round(budget * 0.20, 2),

                "Decor":
                    round(budget * 0.20, 2),

                "Utility":
                    round(budget * 0.20, 2),
            },

            "recommendations": [

                {
                    "category": "Furniture",
                    "item":
                        "Budget-friendly table or storage unit",
                    "platform": "Amazon",
                    "estimated_price":
                        round(budget * 0.20, 2),
                },

                {
                    "category": "Lighting",
                    "item":
                        "LED ceiling/light set",
                    "platform": "IKEA",
                    "estimated_price":
                        round(budget * 0.10, 2),
                },

                {
                    "category": "Decor",
                    "item":
                        "Wall art and indoor decor",
                    "platform": "Amazon",
                    "estimated_price":
                        round(budget * 0.10, 2),
                },
            ],
        }


    # PARTY
    if planner == "party":

        guests = int(
            data.get("guests", 0) or 0
        )

        return {

            "planner": "Party Planner",

            "budget": budget,

            "guests": guests,

            "summary":
                "A balanced party plan covering food, decoration, venue and entertainment.",

            "budget_allocation": {

                "Food":
                    round(budget * 0.45, 2),

                "Venue":
                    round(budget * 0.25, 2),

                "Decoration":
                    round(budget * 0.15, 2),

                "Entertainment":
                    round(budget * 0.15, 2),
            },

            "recommendations": [

                {
                    "category": "Food",
                    "item":
                        "Catering / food package",
                    "platform":
                        "Swiggy / Zomato",
                    "estimated_price":
                        round(budget * 0.45, 2),
                },

                {
                    "category": "Venue",
                    "item":
                        "Budget-friendly venue",
                    "platform":
                        "OYO / Local venue",
                    "estimated_price":
                        round(budget * 0.25, 2),
                },

                {
                    "category": "Decoration",
                    "item":
                        "Theme decoration package",
                    "platform":
                        "Local vendor",
                    "estimated_price":
                        round(budget * 0.15, 2),
                },
            ],
        }


    # JEWELRY

    return {

        "planner": "Jewelry Planner",

        "budget": budget,

        "occasion":
            data.get("occasion", ""),

        "summary":
            "Jewelry suggestions selected around the occasion, style and budget.",

        "recommendations": [

            {
                "category": "Earrings",
                "item":
                    "Elegant matching earrings",
                "platform":
                    "Amazon / Flipkart",
                "estimated_price":
                    round(budget * 0.30, 2),
            },

            {
                "category": "Necklace",
                "item":
                    "Occasion-appropriate necklace",
                "platform":
                    "Amazon / Flipkart",
                "estimated_price":
                    round(budget * 0.45, 2),
            },

            {
                "category": "Bracelet",
                "item":
                    "Simple matching bracelet",
                "platform":
                    "Amazon / Flipkart",
                "estimated_price":
                    round(budget * 0.20, 2),
            },
        ],
    }


# --------------------------------------------------
# Gemini prompt
# --------------------------------------------------

def _build_prompt(
    planner: str,
    data: dict
) -> str:

    return f"""
You are PocketSmart AI,
a smart budget-aware recommendation assistant.

Planner:
{planner}

User input:

{json.dumps(data, indent=2)}

Create practical recommendations
that stay within the user's total budget.

Return ONLY valid JSON.

Required structure:

{{
    "planner": "string",
    "budget": number,
    "summary": "string",
    "budget_allocation": {{}},
    "recommendations": [
        {{
            "category": "string",
            "item": "string",
            "platform": "string",
            "estimated_price": number,
            "reason": "string"
        }}
    ]
}}

Important:

Do not claim that you have live
product prices or live inventory.

Platform names such as Amazon,
Flipkart, IKEA, Swiggy, Zomato
or OYO can be used as suggested sources.
"""


# --------------------------------------------------
# Extract JSON
# --------------------------------------------------

def _extract_json(
    text: str
) -> Optional[dict]:

    text = text.strip()

    if text.startswith("```"):

        text = text.replace(
            "```json",
            "",
            1
        )

        text = text.replace(
            "```",
            "",
            1
        )

        text = text.strip()

    start = text.find("{")

    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    try:

        return json.loads(
            text[start:end + 1]
        )

    except json.JSONDecodeError:

        return None


# --------------------------------------------------
# Generate recommendations
# --------------------------------------------------

async def generate_recommendations(
    planner: str,
    data: dict
) -> dict:

    client = _get_client()

    # No Gemini key
    if client is None:

        result = _fallback(
            planner,
            data
        )

        result["source"] = "fallback"

        return result


    try:

        response = client.models.generate_content(

            model=DEFAULT_MODEL,

            contents=_build_prompt(
                planner,
                data
            ),
        )

        response_text = (
            getattr(response, "text", "")
            or ""
        )

        parsed = _extract_json(
            response_text
        )

        if parsed:

            parsed["source"] = "gemini"

            return parsed


    except Exception as exc:

        result = _fallback(
            planner,
            data
        )

        result["source"] = "fallback"

        result["warning"] = (
            f"Gemini request failed: "
            f"{type(exc).__name__}"
        )

        return result


    result = _fallback(
        planner,
        data
    )

    result["source"] = "fallback"

    return result