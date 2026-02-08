def calculate_risk_score(
    diameter_km: float,
    miss_distance_km: float,
    velocity_km_s: float,
    hazardous: bool,
) -> tuple[int, str]:
    """
    Working risk model (heuristic, not absolute truth):
    - Bigger objects are more dangerous
    - Closer miss distance increases risk
    - Higher velocity increases risk
    - NASA hazardous flag boosts risk
    """

    score = 0

    # Size contribution (0–40)
    score += min(diameter_km * 30, 40)

    # Distance contribution (0–30)
    if miss_distance_km > 0:
        score += min((1 / (miss_distance_km / 1_000_000)) * 15, 30)

    # Velocity contribution (0–20)
    score += min(velocity_km_s * 0.8, 20)

    # Hazardous flag bonus (0 or 10)
    if hazardous:
        score += 10

    score = int(round(score))

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level
