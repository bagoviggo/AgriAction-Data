"""Sends SMS via Africa's Talking. Falls back to console logging (dry run)
if credentials are not set, so the pipeline runs end to end without an account."""
import os

def send_sms(phone_number: str, message: str) -> dict:
    username = os.getenv("AT_USERNAME")
    api_key = os.getenv("AT_API_KEY")
    if not username or not api_key:
        print(f"[DRY RUN] SMS to {phone_number}: {message}")
        return {"status": "dry_run", "phone": phone_number, "message": message}
    try:
        import africastalking
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS
        response = sms.send(message, [phone_number])
        return response
    except Exception as e:
        print(f"[SEND FAILED] {e}")
        return {"status": "error", "detail": str(e)}
