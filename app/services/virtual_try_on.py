"""Synthetic virtual try-on generator using SVG placeholders."""

from __future__ import annotations

import base64
from typing import Iterable

TEMPLATE = """<svg xmlns='http://www.w3.org/2000/svg' width='512' height='768'>
  <rect width='100%' height='100%' fill='{background}'/>
  <rect x='32' y='32' width='448' height='120' rx='12' fill='white'/>
  <text x='48' y='96' font-family='Arial, sans-serif' font-size='36' fill='black'>Dress Code AI</text>
  <text x='48' y='160' font-family='Arial, sans-serif' font-size='20' fill='white'>Dress code: {dress_code}</text>
  {profile_block}
  {items_block}
  <rect x='196' y='320' width='120' height='280' rx='40' fill='none' stroke='white' stroke-width='6'/>
  <text x='210' y='360' font-family='Arial, sans-serif' font-size='18' fill='white'>AI silhouette</text>
</svg>"""

BACKGROUND_BY_CODE = {
    "formal": "#111111",
    "business": "#1b263b",
    "casual": "#e6ebf2",
    "active": "#d2ecff",
}


def _resolve_background(dress_code: str) -> str:
    code = dress_code.lower()
    for key, color in BACKGROUND_BY_CODE.items():
        if key in code:
            return color
    return BACKGROUND_BY_CODE["casual"]


def generate_virtual_try_on(
    dress_code: str, selected_items: Iterable[str], user_profile: str | None = None
) -> str:
    """Generate a synthetic virtual try-on SVG and return it as a base64 string."""

    background = _resolve_background(dress_code)
    profile_block = (
        "<text x='48' y='190' font-family='Arial, sans-serif' font-size='18' fill='white'>"
        f"Profile: {user_profile}</text>"
        if user_profile
        else ""
    )
    start_y = 230 if user_profile else 210
    lines = []
    for idx, item in enumerate(selected_items, start=1):
        y = start_y + (idx - 1) * 28
        safe_item = str(item).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        lines.append(
            "<text x='60' y='{y}' font-family='Arial, sans-serif' font-size='18' fill='white'>Look piece {idx}: {item}</text>".format(
                y=y, idx=idx, item=safe_item
            )
        )
    items_block = (
        "\n  ".join(lines)
        if lines
        else "<text x='60' y='230' font-family='Arial, sans-serif' font-size='18' fill='white'>No items selected</text>"
    )

    svg = TEMPLATE.format(
        background=background,
        dress_code=dress_code.title(),
        profile_block=profile_block,
        items_block=items_block,
    )
    return base64.b64encode(svg.encode("utf-8")).decode("ascii")
