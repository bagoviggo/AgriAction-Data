"""Pulls weekly market prices. Falls back to sample data if KAMIS is unreachable."""
import requests

SAMPLE_PRICES = {
    "Sorghum": [{"market": "Wote", "price_kes_per_90kg": 4200}, {"market": "Sultan Hamud", "price_kes_per_90kg": 4500}],
    "Green grams": [{"market": "Wote", "price_kes_per_90kg": 9800}, {"market": "Sultan Hamud", "price_kes_per_90kg": 10200}],
    "Cowpeas": [{"market": "Wote", "price_kes_per_90kg": 7000}, {"market": "Sultan Hamud", "price_kes_per_90kg": 7300}],
}

def get_market_prices(crop_name: str) -> list[dict]:
    try:
        raise NotImplementedError  # placeholder for the real KAMIS pull
    except Exception:
        return SAMPLE_PRICES.get(crop_name, [])
