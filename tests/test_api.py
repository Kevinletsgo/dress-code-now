import base64

from app import api


def test_outfit_pipeline_returns_virtual_image():
    payload = {
        "climate": {
            "time_of_day": "morning",
            "temperature_c": 12,
            "humidity": 45,
            "precipitation": "rain",
            "event_type": "business",
        },
        "style_preferences": ["waterproof"],
        "outfit_count": 2,
    }

    result = api.run_outfit_pipeline(payload)
    assert result["dress_code"].startswith("business")
    assert len(result["recommendations"]) == 2
    assert result["virtual_try_on_image"]
    base64.b64decode(result["virtual_try_on_image"])  # ensure valid base64


def test_recommendations_not_found_when_invalid_code():
    try:
        api.recommend_outfit({"dress_code": "nonexistent code"})
    except ValueError as exc:
        assert "No recommendations" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing dress code recommendations")
