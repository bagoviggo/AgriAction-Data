"""Pulls 10-day rainfall history for a ward. Falls back to sample data
if CHIRPS is unreachable, so the pipeline is testable without network access."""
import requests

def get_rainfall_last_10_days(ward: dict) -> list[float]:
    try:
        # Placeholder for a real CHIRPS endpoint / downscaled GeoTIFF read.
        # Left unimplemented on purpose for the hackathon MVP.
        raise NotImplementedError
    except Exception:
        # Sample fallback: a realistic false-start pattern (rain, then dry spell)
        return [4.0, 6.5, 1.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0]
