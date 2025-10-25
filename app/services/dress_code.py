"""Rule-based dress code classification logic."""

from __future__ import annotations

from typing import Tuple

from app.models.schemas import ClimateConditions


def classify_dress_code(climate: ClimateConditions) -> Tuple[str, float, str]:
    """Return a (dress_code, confidence, reasoning) tuple for the provided climate.

    The implementation is intentionally deterministic so that it can be tested easily
    while still capturing a variety of factors such as time of day, temperature, and
    event type.
    """

    temperature = climate.temperature_c
    event = (climate.event_type or "casual").lower()
    time_of_day = climate.time_of_day.lower()
    precipitation = (climate.precipitation or "none").lower()
    wind_speed = climate.wind_speed_kmh or 0

    reasoning_parts = [
        f"Detected event type: {event}.",
        f"Time of day: {time_of_day} with temperature {temperature:.1f}°C.",
    ]

    if precipitation not in {"none", "clear"}:
        reasoning_parts.append(f"Precipitation expected: {precipitation}.")
    if wind_speed > 25:
        reasoning_parts.append(f"Windy conditions at {wind_speed:.0f} km/h.")

    # Determine base dress code.
    if event in {"black_tie", "formal", "wedding"}:
        dress_code = "formal evening"
    elif event in {"business", "office", "meeting"}:
        dress_code = "business smart"
    elif event in {"sports", "outdoor", "festival"}:
        dress_code = "active casual"
    else:
        dress_code = "smart casual"

    # Adjustments based on temperature.
    if temperature <= 5:
        dress_code = f"cold weather {dress_code}"
        reasoning_parts.append(
            "Temperature under or equal to 5°C, prioritising insulation layers."
        )
    elif temperature <= 15:
        reasoning_parts.append(
            "Mild chill detected, suggest light layering or outerwear."
        )
    elif temperature >= 28:
        dress_code = f"summer {dress_code}"
        reasoning_parts.append("Hot conditions favour breathable fabrics and lighter fits.")
    else:
        reasoning_parts.append("Comfortable temperature allows standard outfit options.")

    # Weather-specific modifications.
    if precipitation in {"rain", "storm"}:
        reasoning_parts.append("Recommend waterproof or water-resistant layers.")
    elif precipitation == "snow":
        dress_code = dress_code.replace("summer ", "")
        reasoning_parts.append("Snowfall requires insulated and weatherproof pieces.")

    if wind_speed >= 35:
        reasoning_parts.append("High winds call for secure, wind-breaking outerwear.")

    # Confidence scoring is heuristic based on how many signals align clearly.
    confidence = 0.6
    if event in {"black_tie", "formal"}:
        confidence += 0.2
    if temperature <= 5 or temperature >= 28:
        confidence += 0.1
    if precipitation in {"rain", "snow", "storm"}:
        confidence += 0.05

    confidence = min(confidence, 0.95)

    reasoning = " ".join(reasoning_parts)
    return dress_code, confidence, reasoning
