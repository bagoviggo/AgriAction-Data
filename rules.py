from config import GERMINATION_THRESHOLD_MM, DRY_DAY_LIMIT, CROPS

def classify_rainfall(daily_mm: list[float]) -> dict:
    cumulative = sum(daily_mm)
    dry_streak = 0
    max_dry_streak = 0
    for day in daily_mm:
        if day == 0:
            dry_streak += 1
            max_dry_streak = max(max_dry_streak, dry_streak)
        else:
            dry_streak = 0

    if cumulative >= GERMINATION_THRESHOLD_MM and max_dry_streak < DRY_DAY_LIMIT:
        decision = "PLANT_NOW"
    elif max_dry_streak >= DRY_DAY_LIMIT:
        decision = "WAIT"
    else:
        decision = "STAGGER"

    return {"decision": decision, "cumulative_mm": cumulative, "max_dry_streak": max_dry_streak}

def recommend_crop(decision: str) -> dict:
    # Below-normal or uncertain seasons favour the shortest-cycle crop.
    if decision == "PLANT_NOW":
        return CROPS[0]
    return min(CROPS, key=lambda c: c["min_season_days"])
