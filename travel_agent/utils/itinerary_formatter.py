"""
Utility functions for formatting travel itineraries.
"""

import json
from datetime import datetime, timedelta


def format_itinerary(
    destination: str,
    num_days: int,
    flight_info: dict,
    hotel_info: dict,
    places: list[dict],
    weather_data: list[dict],
    budget: dict,
    start_date: str = None,
) -> str:
    """
    Format a complete travel itinerary as a readable string.

    Args:
        destination: Destination city name
        num_days: Number of trip days
        flight_info: Dict with airline, price, departure, arrival
        hotel_info: Dict with name, stars, price_per_night, rating
        places: List of place dicts to visit
        weather_data: List of weather dicts per day
        budget: Dict with cost breakdown
        start_date: Trip start date (YYYY-MM-DD format)

    Returns:
        Formatted itinerary string
    """
    lines = []
    
    # Header
    start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.now()
    end = start + timedelta(days=num_days - 1)
    
    lines.extend([
        "=" * 60,
        f"  🌴 YOUR {num_days}-DAY TRIP TO {destination.upper()}",
        f"  📅 {start.strftime('%b %d')} – {end.strftime('%b %d, %Y')}",
        "=" * 60,
        "",
    ])
    
    # Flight
    if flight_info:
        lines.extend([
            "✈️  FLIGHT SELECTED",
            f"   Airline: {flight_info.get('airline', 'TBD')}",
            f"   Departure: {flight_info.get('departure', 'TBD')} | "
            f"Arrival: {flight_info.get('arrival', 'TBD')}",
            f"   Price: ₹{flight_info.get('price_inr', 0):,}",
            "",
        ])
    
    # Hotel
    if hotel_info:
        lines.extend([
            "🏨  HOTEL BOOKED",
            f"   {hotel_info.get('name', 'TBD')} "
            f"({hotel_info.get('stars', '?')}★ | "
            f"Rating: {hotel_info.get('rating', 'N/A')}/5)",
            f"   ₹{hotel_info.get('price_per_night_inr', 0):,}/night × {num_days} nights",
            "",
        ])
    
    # Day-wise itinerary
    lines.extend(["📋  DAY-WISE ITINERARY", ""])
    places_per_day = max(1, len(places) // num_days)
    
    for day in range(1, num_days + 1):
        day_date = start + timedelta(days=day - 1)
        day_places = places[(day - 1) * places_per_day: day * places_per_day]
        
        # Weather for this day
        weather_str = ""
        if weather_data and len(weather_data) >= day:
            w = weather_data[day - 1]
            weather_str = (
                f" | 🌡️ {w.get('max_temp', '?')}°C "
                f"| {w.get('condition', 'Variable')}"
            )
        
        lines.append(f"  📅 Day {day} — {day_date.strftime('%A, %b %d')}{weather_str}")
        
        if day_places:
            for place in day_places:
                fee = f"₹{place.get('entry_fee_inr', 0)}" if place.get("entry_fee_inr", 0) > 0 else "Free"
                lines.append(
                    f"     • {place['name']} ({place.get('type', '')}) "
                    f"— Entry: {fee} | ~{place.get('duration_hrs', 1)}hrs"
                )
        else:
            lines.append("     • Free day — explore at your own pace")
        lines.append("")
    
    # Budget
    if budget:
        lines.extend([
            "💰  BUDGET BREAKDOWN",
            f"   Flight (return): ₹{budget.get('flight', 0):,}",
            f"   Hotel:           ₹{budget.get('hotel', 0):,}",
            f"   Food:            ₹{budget.get('food', 0):,}",
            f"   Transport:       ₹{budget.get('transport', 0):,}",
            f"   Activities:      ₹{budget.get('activities', 0):,}",
            "   " + "-" * 30,
            f"   TOTAL:           ₹{budget.get('total', 0):,}",
            "",
        ])
    
    lines.extend([
        "=" * 60,
        "  Have a wonderful trip! 🎉",
        "=" * 60,
    ])
    
    return "\n".join(lines)


def parse_tool_output_to_dict(tool_output: str) -> dict:
    """
    Attempt to parse structured data from a tool output string.
    Returns a dict with extracted key-value pairs.
    """
    result = {}
    for line in tool_output.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("•"):
            key, _, value = line.partition(":")
            key_clean = key.strip().lower().replace(" ", "_")
            result[key_clean] = value.strip()
    return result
