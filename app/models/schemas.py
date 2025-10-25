"""Lightweight data models for the Dress Code Now service."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional


def _optional_str(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)


@dataclass
class ClimateConditions:
    time_of_day: str
    temperature_c: float
    humidity: Optional[int] = None
    precipitation: Optional[str] = None
    wind_speed_kmh: Optional[float] = None
    event_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ClimateConditions":
        return cls(
            time_of_day=str(data["time_of_day"]).strip(),
            temperature_c=float(data["temperature_c"]),
            humidity=int(data["humidity"]) if data.get("humidity") is not None else None,
            precipitation=_optional_str(data.get("precipitation")),
            wind_speed_kmh=(
                float(data["wind_speed_kmh"]) if data.get("wind_speed_kmh") is not None else None
            ),
            event_type=_optional_str(data.get("event_type")),
        )


@dataclass
class DressCodeResponse:
    dress_code: str
    confidence: float
    reasoning: str

    def to_dict(self) -> dict:
        return {
            "dress_code": self.dress_code,
            "confidence": round(self.confidence, 3),
            "reasoning": self.reasoning,
        }


@dataclass
class RecommendationItem:
    name: str
    category: str
    color_palette: List[str]
    description: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "color_palette": list(self.color_palette),
            "description": self.description,
        }


@dataclass
class RecommendationsResponse:
    dress_code: str
    items: List[RecommendationItem] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "dress_code": self.dress_code,
            "items": [item.to_dict() for item in self.items],
        }


@dataclass
class OutfitPipelineResponse:
    dress_code: str
    recommendations: List[RecommendationItem]
    virtual_try_on_image: str

    def to_dict(self) -> dict:
        return {
            "dress_code": self.dress_code,
            "recommendations": [item.to_dict() for item in self.recommendations],
            "virtual_try_on_image": self.virtual_try_on_image,
        }


def normalise_preferences(preferences: Optional[Iterable[str]]) -> List[str]:
    if not preferences:
        return []
    return [str(pref).strip().lower() for pref in preferences if str(pref).strip()]
