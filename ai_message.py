"""Turns a rule-based decision into a short Kiswahili SMS.
Uses Anthropic if a key is set, otherwise falls back to a fixed template
so the pipeline is fully testable offline."""
import os

TEMPLATES = {
    "PLANT_NOW": "Mvua za sasa zinatosha kupanda {crop}. Panda sasa.",
    "WAIT": "Mvua bado haitoshi. Subiri kabla ya kupanda {crop}.",
    "STAGGER": "Mvua haina uhakika. Panda {crop} kidogo kidogo, si shamba lote mara moja.",
}

def generate_planting_sms(decision: str, crop_name: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return TEMPLATES[decision].format(crop=crop_name)
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        prompt = (
            f"Write one short SMS (under 140 characters) in simple Kiswahili for a "
            f"smallholder farmer. Decision: {decision}. Recommended crop: {crop_name}. "
            f"Be direct and practical, no greetings."
        )
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    except Exception:
        return TEMPLATES[decision].format(crop=crop_name)

def generate_market_sms(crop_name: str, prices: list[dict]) -> str:
    if not prices:
        return f"Hakuna bei ya {crop_name} wiki hii."
    lines = ", ".join(f"{p['market']}: KES {p['price_kes_per_90kg']}" for p in prices)
    return f"Bei ya {crop_name} wiki hii: {lines}."
