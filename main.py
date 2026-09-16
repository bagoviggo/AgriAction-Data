"""Entry point. Run this on a daily schedule (cron / Cloud Scheduler / ECS scheduled task).
Wards and farmers are read from the shared Postgres database (owned by agriaction-web's
Prisma schema), not hardcoded here. Add wards via /admin/wards and farmers via /register
in the web app before running this."""
from dotenv import load_dotenv
load_dotenv()

from rainfall_source import get_rainfall_last_10_days
from market_source import get_market_prices
from rules import classify_rainfall, recommend_crop
from ai_message import generate_planting_sms, generate_market_sms
from crop_tips import get_storage_tip
from sms_sender import send_sms
from db import get_connection, log_message, get_active_wards, get_farmers_for_ward

FALLBACK_PHONE = ["+254700000000"]  # used only in dry-run testing when no farmers are registered yet

def run_planting_advisory(conn, ward, recipients):
    rainfall = get_rainfall_last_10_days(ward)
    result = classify_rainfall(rainfall)
    crop = recommend_crop(result["decision"])
    message = generate_planting_sms(result["decision"], crop["name"])
    print(f"[{ward['name']}] {result} -> crop: {crop['name']} -> {len(recipients)} farmer(s)")
    for phone in recipients:
        send_sms(phone, message)
    log_message(conn, ward["id"], "planting_advisory", message, result["decision"])
    return crop

def run_loss_reduction_tip(conn, ward, crop, recipients):
    tip = get_storage_tip(crop["name"])
    for phone in recipients:
        send_sms(phone, tip)
    log_message(conn, ward["id"], "loss_reduction", tip, "sent")

def run_market_update(conn, ward, crop, recipients):
    prices = get_market_prices(crop["name"])
    message = generate_market_sms(crop["name"], prices)
    for phone in recipients:
        send_sms(phone, message)
    log_message(conn, ward["id"], "market_update", message, "sent")

def main():
    conn = get_connection()
    wards = get_active_wards(conn)
    if not wards:
        print("No wards found in the database. Add one via /admin/wards in agriaction-web first.")
        return
    for ward in wards:
        recipients = get_farmers_for_ward(conn, ward["id"]) or FALLBACK_PHONE
        crop = run_planting_advisory(conn, ward, recipients)
        run_loss_reduction_tip(conn, ward, crop, recipients)
        run_market_update(conn, ward, crop, recipients)
    if conn:
        conn.close()

if __name__ == "__main__":
    main()