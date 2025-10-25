from app.models.schemas import ClimateConditions
from app.services.dress_code import classify_dress_code


def test_formal_evening_high_confidence():
    climate = ClimateConditions(
        time_of_day="evening",
        temperature_c=18,
        humidity=60,
        precipitation="none",
        event_type="formal",
    )
    dress_code, confidence, reasoning = classify_dress_code(climate)
    assert dress_code == "formal evening"
    assert confidence > 0.7
    assert "formal" in reasoning.lower()


def test_cold_weather_prefix_added():
    climate = ClimateConditions(
        time_of_day="morning",
        temperature_c=0,
        humidity=40,
        precipitation="snow",
        event_type="business",
        wind_speed_kmh=15,
    )
    dress_code, confidence, reasoning = classify_dress_code(climate)
    assert dress_code.startswith("cold weather")
    assert "snowfall" in reasoning.lower()
    assert confidence >= 0.75
