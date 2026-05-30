"""
Places & Points of Interest Discovery Tool for the AI Travel Planning Agent.
Searches places.json and returns top-rated attractions.
"""

import json
import os
from langchain.tools import tool


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "places.json")


def _load_places() -> list[dict]:
    """Load places data from JSON file."""
    with open(DATA_PATH, "r") as f:
        return json.load(f)


@tool
def search_places(query: str) -> str:
    """
    Search for tourist attractions and points of interest in a city.

    Input format: "city" or "city type:beach/heritage/adventure/nature/market"
    Examples:
        "Goa"
        "Jaipur type:heritage"
        "Manali type:adventure"
        "Kerala type:nature"

    Returns top-rated places with descriptions, entry fees, and recommended visit duration.
    """
    try:
        places = _load_places()

        parts = query.strip().split()
        city = parts[0].title()
        place_type = None

        for part in parts[1:]:
            if part.lower().startswith("type:"):
                place_type = part.split(":")[1].lower()

        # Filter by city
        matching = [p for p in places if p["city"].lower() == city.lower()]

        if not matching:
            cities = list(set(p["city"] for p in places))
            return (
                f"No attractions found in {city}. "
                f"Available cities: {', '.join(sorted(cities))}"
            )

        # Filter by type if specified
        if place_type:
            type_filtered = [
                p for p in matching
                if place_type in p["type"].lower()
            ]
            if type_filtered:
                matching = type_filtered

        # Sort by rating
        matching_sorted = sorted(matching, key=lambda x: x["rating"], reverse=True)

        result_lines = [
            f"🗺️ Top Attractions in {city}:",
            f"",
        ]

        for i, place in enumerate(matching_sorted, 1):
            fee_str = f"₹{place['entry_fee_inr']}" if place["entry_fee_inr"] > 0 else "Free"
            result_lines.extend([
                f"  {i}. {place['name']} ({place['type']})",
                f"     Rating: {place['rating']}/5 | Entry: {fee_str} | Duration: ~{place['duration_hrs']}hrs",
                f"     Best Time: {place['best_time']}",
                f"     {place['description']}",
                f"",
            ])

        # Suggest day-wise split
        if len(matching_sorted) >= 3:
            result_lines.append("📅 SUGGESTED DAILY GROUPING:")
            items_per_day = max(2, len(matching_sorted) // 3)
            for day_num in range(1, 4):
                start = (day_num - 1) * items_per_day
                end = start + items_per_day
                day_places = matching_sorted[start:end]
                if day_places:
                    names = ", ".join(p["name"] for p in day_places)
                    result_lines.append(f"   Day {day_num}: {names}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error searching places: {str(e)}"
