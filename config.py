WARDS = [
    {"id": "kathonzweni", "name": "Kathonzweni", "lat": -1.99, "lon": 37.85},
]

GERMINATION_THRESHOLD_MM = 20   # cumulative rain needed over 10 days to trust an onset
DRY_DAY_LIMIT = 5               # consecutive dry days that flags a false start

CROPS = [
    {"name": "Sorghum", "min_season_days": 90},
    {"name": "Green grams", "min_season_days": 75},
    {"name": "Cowpeas", "min_season_days": 70},
]
