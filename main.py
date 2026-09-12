"""Entry point. Run this on a daily schedule (cron / Cloud Scheduler / ECS scheduled task).
Runs Module 1 (planting risk) and Module 3 (market price) for every configured ward."""
from dotenv import load_dotenv
load_dotenv()

from config import WARDS
from rainfall_source import get_rainfall_last_10_days
from market_source import get_market_prices
from rules import classify_rainfall, recommend_crop
from ai_message import generate_planting_sms, generate_market_sms
from sms_sender import send_sms
from db import get_connection, log_message

def run_planting_advisory(conn, ward: dict):
    rainfall = get_rainfall_last_10_days(ward)
    result = classify_rainfall(rainfall)
    crop = recommend_crop(result["decision"])
    message = generate_planting_sms(result["decision"], crop["name"])
    print(f"[{ward['name']}] {result} -> crop: {crop['name']}")
    send_sms("+254700000000", message)  # replace with real registered farmer numbers
    log_message(conn, ward["id"], "planting_advisory", message, result["decision"])
    return crop

def run_market_update(conn, ward: dict, crop: dict):
    prices = get_market_prices(crop["name"])
    message = generate_market_sms(crop["name"], prices)
    send_sms("+254700000000", message)
    log_message(conn, ward["id"], "market_update", message, "sent")

def main():
    conn = get_connection()
    for ward in WARDS:
        crop = run_planting_advisory(conn, ward)
        run_market_update(conn, ward, crop)
    if conn:
        conn.close()

if __name__ == "__main__":
    main()
