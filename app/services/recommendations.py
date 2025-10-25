"""Outfit recommendation service based on dress code."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from random import sample
from typing import Iterable, List

from app.models.schemas import RecommendationItem

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "garments.json"


@lru_cache(maxsize=1)
def _load_garments() -> dict:
    with DATA_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def get_recommendations(
    dress_code: str, style_preferences: Iterable[str] | None = None, *, limit: int = 3
) -> List[RecommendationItem]:
    """Return a curated list of garments for the dress code.

    The function optionally filters by style preferences by matching keywords in the
    description field. If there are fewer than ``limit`` matching items the function
    gracefully falls back to the whole dress code collection.
    """

    dress_code_key = dress_code.lower()
    garments = _load_garments()

    if dress_code_key not in garments:
        # Attempt to gracefully degrade by removing modifiers such as "summer".
        if " " in dress_code_key:
            base_key = " ".join(dress_code_key.split(" ")[1:])
            garments_for_code = garments.get(base_key, [])
        else:
            garments_for_code = []
    else:
        garments_for_code = garments[dress_code_key]

    if not garments_for_code:
        return []

    style_prefs = [pref.lower() for pref in (style_preferences or [])]

    if style_prefs:
        filtered = [
            item
            for item in garments_for_code
            if any(pref in item["description"].lower() for pref in style_prefs)
        ]
    else:
        filtered = garments_for_code

    pool = filtered or garments_for_code
    k = min(limit, len(pool))
    chosen = sample(pool, k=k) if len(pool) > k else list(pool)

    return [RecommendationItem(**item) for item in chosen]
