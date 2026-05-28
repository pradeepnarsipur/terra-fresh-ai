import json
import os
import re

from groq import Groq

GROQ_MODEL = "llama-3.1-8b-instant"
MISSING_KEY_MESSAGE = "Groq API key missing"


def get_api_key() -> str | None:
    key = (os.getenv("GROQ_API_KEY") or "").strip()
    return key or None


def get_groq_client() -> Groq:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(MISSING_KEY_MESSAGE)
    return Groq(api_key=api_key)


def build_prompt(crop: str, ph: float, temp: float, humidity: float, symptoms: str) -> str:
    return f"""You are Terra Fresh AI, an expert agronomist assistant.

Analyze the following crop conditions and respond ONLY with valid JSON (no markdown fences) using this exact structure:
{{
  "plant_health_summary": "2-4 sentences on overall plant health",
  "nutrient_recommendation": "specific nutrients, amounts or ratios if applicable",
  "possible_disease_issues": "likely diseases, pests, or environmental issues",
  "suggested_action": "clear step-by-step actions the farmer should take"
}}

Crop data:
- Crop: {crop}
- Soil pH: {ph}
- Temperature (C): {temp}
- Humidity (%): {humidity}
- Plant symptoms: {symptoms or "None reported"}

Be practical, concise, and actionable. Base advice on the provided values and symptoms."""


def parse_ai_response(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {
        "plant_health_summary": text,
        "nutrient_recommendation": "Could not parse structured response. See summary above.",
        "possible_disease_issues": "-",
        "suggested_action": "Retry or check the model response format.",
    }


def get_recommendation(crop: str, ph: float, temp: float, humidity: float, symptoms: str) -> dict:
    client = get_groq_client()
    prompt = build_prompt(crop, ph, temp, humidity, symptoms)
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1024,
    )
    content = completion.choices[0].message.content or ""
    return parse_ai_response(content)
