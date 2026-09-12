# agriaction-data

Python service: pulls rainfall + market data, applies the rule-based planting
classifier, generates SMS text, and sends it. Designed to run on a daily
schedule (cron, GCP Cloud Scheduler + Cloud Run, or an AWS ECS scheduled task).

## Run locally
```
pip install -r requirements.txt
cp .env.example .env   # fill in keys, or leave blank to run in dry-run mode
python main.py
```

With no ANTHROPIC_API_KEY, AT_API_KEY, or DATABASE_URL set, everything still
runs end to end using template messages, console-logged "SMS", and console-logged
DB writes, so you can test the full pipeline logic with zero external accounts.

## Files
- `config.py` - ward list and rule thresholds
- `rainfall_source.py` / `market_source.py` - data pulls (CHIRPS/KAMIS placeholders + sample fallback)
- `rules.py` - the actual planting decision logic (Module 1)
- `ai_message.py` - decision -> SMS text (Modules 1 and 3)
- `sms_sender.py` - Africa's Talking wrapper with dry-run fallback
- `db.py` / `main.py` - orchestration and logging
