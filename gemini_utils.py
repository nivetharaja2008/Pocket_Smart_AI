import json
import re

from typing import Any

from google import genai
from google.genai import types

from ..config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

from .fallback import (
    home_fallback,
    party_fallback,
    jewelry_fallback
)


client = (
    genai.Client(
        api_key=GEMINI_API_KEY
    )
    if GEMINI_API_KEY
    else None
)


SYSTEM = """
You are PocketSmart AI,
a practical budget planning assistant.

Return ONLY valid JSON.

Never invent a live product listing,
stock status,
exact current price,
or verified availability.

Treat platform names as source categories,
not proof that an item exists at the stated price.

Use Indian rupees (INR) unless the user
explicitly asks otherwise.

Keep recommendations realistic
and budget-aware.

JSON keys:

planner,
source,
summary,
budget_allocation,
recommendations,
tips.

Each recommendation must contain:

name,
category,
price,
rating,
discount,
platform,
emoji,
unit,
reason.
"""


def _json_from_text(
    text: str
) -> dict[str, Any]:

    text = (
        text or ""
    ).strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.I
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    start = text.find("{")

    end = text.rfind("}")

    if start == -1 or end == -1:

        raise ValueError(
            "Gemini did not return JSON"
        )

    return json.loads(
        text[start:end + 1]
    )


def _call(contents):

    if not client:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured"
        )

    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=contents,

        config=types.GenerateContentConfig(

            system_instruction=SYSTEM,

            temperature=0.4,

            max_output_tokens=5000,

            response_mime_type="application/json"
        )
    )

    return _json_from_text(
        response.text
    )


def _normalize(
    data,
    planner
):

    data["planner"] = planner

    data.setdefault(
        "source",
        "gemini"
    )

    data.setdefault(
        "summary",
        "AI-generated budget plan"
    )

    data.setdefault(
        "budget_allocation",
        {}
    )

    data.setdefault(
        "tips",
        []
    )

    normalized = []

    for recommendation in data.get(
        "recommendations",
        []
    ):

        if not isinstance(
            recommendation,
            dict
        ):
            continue

        recommendation.setdefault(
            "name",
            "Recommended option"
        )

        recommendation.setdefault(
            "category",
            "general"
        )

        recommendation.setdefault(
            "price",
            0
        )

        recommendation.setdefault(
            "rating",
            0
        )

        recommendation.setdefault(
            "discount",
            0
        )

        recommendation.setdefault(
            "platform",
            "General"
        )

        recommendation.setdefault(
            "emoji",
            "✨"
        )

        recommendation.setdefault(
            "unit",
            "item"
        )

        recommendation.setdefault(
            "reason",
            "Fits the stated preferences."
        )

        normalized.append(
            recommendation
        )

    data["recommendations"] = (
        normalized[:12]
    )

    return data


def generate_home(req):

    fallback = home_fallback(req)

    prompt = f"""
Create a home interior budget plan.

Budget:
₹{req.budget}

Rooms:
{req.rooms}

Quantities:
{req.quantities}

Style:
{req.style}

Location:
{req.location}

Allocate the budget across useful categories.

Provide 6-10 example recommendations
from Amazon, IKEA or Flipkart-style sources.

Clearly mark that exact prices must be verified.

Return JSON only.
"""

    try:

        return _normalize(
            _call(prompt),
            "home"
        )

    except Exception:

        return fallback


def generate_party(req):

    fallback = party_fallback(req)

    prompt = f"""
Create a party budget plan.

Budget:
₹{req.budget}

Guests:
{req.guests}

Event type:
{req.event_type}

Venue:
{req.venue}

Theme:
{req.theme}

Location:
{req.location}

Allocate the budget across:

food,
decoration,
entertainment,
gifts,
miscellaneous.

Include 6-10 example options using:

Amazon,
Flipkart,
Swiggy,
Zomato,
OYO-style sources.

Exact vendor prices and availability
must be verified.

Return JSON only.
"""

    try:

        return _normalize(
            _call(prompt),
            "party"
        )

    except Exception:

        return fallback


def generate_jewelry(
    req,
    image_bytes=None,
    mime_type=None
):

    fallback = jewelry_fallback(req)

    prompt = f"""
Create a jewelry recommendation plan.

Budget:
₹{req.budget}

Occasion:
{req.occasion}

Style:
{req.style}

Outfit color:
{req.outfit_color}

Outfit description:
{req.outfit_description}

If an outfit image is provided,
analyze only broad colors,
overall visual style and formality.

Do not identify the person.

Recommend 5-8 example jewelry
options from Amazon/Flipkart-style
sources.

Explain the matching reason.

Exact prices must be verified.

Return JSON only.
"""

    contents = [prompt]

    if image_bytes and mime_type:

        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
        )

    try:

        return _normalize(
            _call(contents),
            "jewelry"
        )

    except Exception:

        return fallback