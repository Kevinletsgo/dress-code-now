# Dress Code Now

An end-to-end web service that generates dress code guidance, curates outfit
recommendations, and synthesises an AI-inspired virtual try-on graphic. The
system combines deterministic heuristics for climate-aware dress code inference
with a small knowledge base of curated garments and a lightweight SVG composer.

## Features

- **Dress code inference** – rule-based reasoning that accounts for temperature,
  precipitation, event type, and time of day.
- **Garment recommendations** – curated outfit pieces per dress code with optional
  filtering via style keywords.
- **Virtual try-on** – synthetic SVG generator that annotates selected items on a
  stylised silhouette, ready to be displayed by a frontend.
- **Unified pipeline endpoint** – single HTTP call that chains the above steps for
  streamlined client consumption.

## Project layout

```
app/
  api.py                # High-level helpers orchestrating the pipeline
  server.py             # Minimal HTTP server for manual experimentation
  main.py               # (Unused placeholder retained for compatibility)
  models/schemas.py     # Dataclasses shared across the API
  services/
    dress_code.py       # Dress code classifier logic
    recommendations.py  # Garment recommendation engine
    virtual_try_on.py   # SVG-based synthetic try-on generator
  data/garments.json    # Dress code knowledge base
```

## Getting started

1. (Optional) create a virtual environment and install the development tooling:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]
   ```

2. Run the automated test suite to verify everything is configured correctly:

   ```bash
   pytest
   ```

3. Launch the development server:

   ```bash
   python -m app.server
   ```

   The server listens on <http://127.0.0.1:8000> and accepts JSON `POST` payloads.

## Example pipeline request

```http
POST /api/outfit-pipeline
Content-Type: application/json

{
  "climate": {
    "time_of_day": "morning",
    "temperature_c": 16,
    "humidity": 55,
    "precipitation": "drizzle",
    "event_type": "business"
  },
  "style_preferences": ["breathable", "waterproof"],
  "outfit_count": 3
}
```

Response:

```json
{
  "dress_code": "business smart",
  "recommendations": [
    {
      "name": "Structured blazer",
      "category": "outerwear",
      "color_palette": ["midnight", "graphite"],
      "description": "Two-button blazer with subtle texture suitable for boardrooms."
    },
    {
      "name": "Tailored trousers",
      "category": "bottom",
      "color_palette": ["charcoal", "navy"],
      "description": "Wool blend trousers with crease-resistant finish."
    },
    {
      "name": "Monk strap shoes",
      "category": "footwear",
      "color_palette": ["oxblood", "black"],
      "description": "Statement footwear that remains professional."
    }
  ],
  "virtual_try_on_image": "<base64 SVG string>"
}
```

The `virtual_try_on_image` field contains a base64-encoded SVG that can be
rendered directly in a web frontend to provide a visual preview of the
recommended outfit (e.g. `data:image/svg+xml;base64,...`).

## Extending the system

- Replace the rule-based classifier in `dress_code.py` with a machine learning model
  trained on historical outfit success data.
- Expand `garments.json` with richer metadata such as fabrics, price ranges, or
  gender-specific fits, and wire that into the recommendation filters.
- Swap the SVG generator in `virtual_try_on.py` for a diffusion-based try-on
  inference call to produce photorealistic composites.
- Build a React or Vue frontend that consumes `/api/outfit-pipeline` to deliver a
  fully interactive user experience.
