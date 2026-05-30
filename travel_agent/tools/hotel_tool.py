"""
Hotel Recommendation Tool for the AI Travel Planning Agent.
Searches hotels.json and returns options filtered by city, rating, and price.
"""

import json
import os
from langchain.tools import tool


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hotels.json")


def _load_hotels() -> list[dict]:
    """Load hotel data from JSON file."""
    with open(DATA_PATH, "r") as f:
        return json.load(f)


@tool
def search_hotels(query: str) -> str:
    """
    Search for hotels in a city with optional budget filter.

    Input format: "city" or "city budget:low/mid/high" or "city max:5000"
    Examples:
        "Goa"
        "Jaipur budget:mid"
        "Mumbai max:8000"

    Returns top hotel recommendations with ratings, amenities, and pricing.
    """
    try:
        hotels = _load_hotels()

        # Parse query for city and optional budget
        parts = query.strip().split()
        city = parts[0].title()
        max_price = None
        budget_tier = None

        for part in parts[1:]:
            if part.lower().startswith("max:"):
                try:
                    max_price = int(part.split(":")[1])
                except ValueError:
                    pass
            elif part.lower().startswith("budget:"):
                budget_tier = part.split(":")[1].lower()

        # Budget tier mapping
        if budget_tier == "low":
            max_price = 2500
        elif budget_tier == "mid":
            max_price = 6000
        elif budget_tier == "high":
            max_price = None  # No limit

        # Filter by city
        matching = [h for h in hotels if h["city"].lower() == city.lower()]

        if not matching:
            cities = list(set(h["city"] for h in hotels))
            return (
                f"No hotels found in {city}. "
                f"Available cities: {', '.join(sorted(cities))}"
            )

        # Apply budget filter if provided
        if max_price:
            matching = [h for h in matching if h["price_per_night_inr"] <= max_price]

        if not matching:
            return f"No hotels in {city} within the budget of ₹{max_price:,}/night."

        # Sort by rating descending
        matching_sorted = sorted(matching, key=lambda x: x["rating"], reverse=True)

        # Top pick
        top = matching_sorted[0]
        # Best budget pick (cheapest with rating > 3.5)
        budget_options = [h for h in matching if h["rating"] >= 3.5]
        cheapest = sorted(budget_options, key=lambda x: x["price_per_night_inr"])[0] if budget_options else matching_sorted[-1]

        result_lines = [
            f"🏨 Hotels in {city}:",
            f"",
            f"⭐ TOP RATED PICK:",
            f"   {top['name']} ({top['stars']}★)",
            f"   Price: ₹{top['price_per_night_inr']:,}/night | Rating: {top['rating']}/5",
            f"   Type: {top['type']}",
            f"   Amenities: {', '.join(top['amenities'])}",
            f"",
            f"💸 BEST VALUE PICK:",
            f"   {cheapest['name']} ({cheapest['stars']}★)",
            f"   Price: ₹{cheapest['price_per_night_inr']:,}/night | Rating: {cheapest['rating']}/5",
            f"   Type: {cheapest['type']}",
            f"   Amenities: {', '.join(cheapest['amenities'])}",
            f"",
            f"📋 ALL OPTIONS ({len(matching_sorted)} found):",
        ]

        for h in matching_sorted:
            result_lines.append(
                f"   • {h['name']} | ₹{h['price_per_night_inr']:,}/night | "
                f"{h['rating']}⭐ | {h['stars']}★ | {h['type']}"
            )

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error searching hotels: {str(e)}"
