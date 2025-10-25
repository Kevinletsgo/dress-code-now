"""High-level API helpers that wire the services together."""

from __future__ import annotations

from typing import Any, Dict

from app.models.schemas import (
    ClimateConditions,
    DressCodeResponse,
    OutfitPipelineResponse,
    RecommendationsResponse,
    normalise_preferences,
)
from app.services.dress_code import classify_dress_code
from app.services.recommendations import get_recommendations
from app.services.virtual_try_on import generate_virtual_try_on


def infer_dress_code(payload: Dict[str, Any]) -> Dict[str, Any]:
    climate = ClimateConditions.from_dict(payload)
    dress_code, confidence, reasoning = classify_dress_code(climate)
    return DressCodeResponse(dress_code, confidence, reasoning).to_dict()


def recommend_outfit(payload: Dict[str, Any]) -> Dict[str, Any]:
    dress_code = payload["dress_code"]
    style_preferences = normalise_preferences(payload.get("style_preferences"))
    items = get_recommendations(dress_code, style_preferences)
    response = RecommendationsResponse(dress_code, items)
    if not response.items:
        raise ValueError("No recommendations available for the requested dress code")
    return response.to_dict()


def run_outfit_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]:
    climate = ClimateConditions.from_dict(payload["climate"])
    style_preferences = normalise_preferences(payload.get("style_preferences"))
    outfit_count = int(payload.get("outfit_count", 3))
    generate_try_on = bool(payload.get("generate_virtual_try_on", True))

    dress_code, _, _ = classify_dress_code(climate)
    recommendations = get_recommendations(
        dress_code, style_preferences, limit=outfit_count
    )
    if not recommendations:
        raise ValueError("No outfit recommendations available for the inferred dress code")

    virtual_image = ""
    if generate_try_on:
        virtual_image = generate_virtual_try_on(
            dress_code, [item.name for item in recommendations], payload.get("user_profile")
        )

    return OutfitPipelineResponse(dress_code, recommendations, virtual_image).to_dict()
