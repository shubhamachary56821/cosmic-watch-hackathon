import httpx
from datetime import date
from app.core.config import settings
from app.services.risk import calculate_risk_score

NASA_FEED_URL = "https://api.nasa.gov/neo/rest/v1/feed"


async def fetch_today_neos():
    today = date.today().isoformat()

    params = {
        "start_date": today,
        "end_date": today,
        "api_key": settings.NASA_API_KEY,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(NASA_FEED_URL, params=params)
        response.raise_for_status()
        data = response.json()

    neos = []

    for neo_list in data["near_earth_objects"].values():
        for neo in neo_list:
            approach = neo["close_approach_data"][0]

            diameter = round(
                neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"], 3
            )
            velocity = round(
                float(approach["relative_velocity"]["kilometers_per_second"]), 2
            )
            miss_distance = round(
                float(approach["miss_distance"]["kilometers"])
            )
            hazardous = neo["is_potentially_hazardous_asteroid"]

            # Calculate risk ONCE
            risk_score, risk_level = calculate_risk_score(
                diameter_km=diameter,
                miss_distance_km=miss_distance,
                velocity_km_s=velocity,
                hazardous=hazardous,
            )

            neos.append({
                "id": neo["id"],
                "name": neo["name"],
                "hazardous": hazardous,
                "estimated_diameter_km": diameter,
                "velocity_km_s": velocity,
                "miss_distance_km": miss_distance,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "close_approach_date": approach["close_approach_date"],
            })

    return neos
