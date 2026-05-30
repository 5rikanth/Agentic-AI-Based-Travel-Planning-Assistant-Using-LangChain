"""
Flight Search Tool for the AI Travel Planning Agent.
Searches flights.json and returns the best options.
"""

import json
import os
from langchain.tools import tool


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "flights.json")


def _load_flights() -> list[dict]:
    """Load flight data from JSON file."""
    with open(DATA_PATH, "r") as f:
        return json.load(f)


@tool
def search_flights(query: str) -> str:
    """
    Search for available flights between two cities.

    Input format: "source to destination"
    Example: "Delhi to Goa" or "Mumbai to Jaipur"

    Returns cheapest, fastest, and best-rated flight options.
    """
    try:
        flights = _load_flights()

        # Parse source and destination from query
        query_lower = query.lower().strip()
        parts = [p.strip() for p in query_lower.replace(" to ", "|").split("|")]
        if len(parts) < 2:
            return "Invalid query. Please provide source and destination. Example: 'Delhi to Goa'"

        source = parts[0].title()
        destination = parts[1].title()

        # Filter matching flights
        matching = [
            f for f in flights
            if f["source"].lower() == source.lower()
            and f["destination"].lower() == destination.lower()
        ]

        if not matching:
            return (
                f"No flights found from {source} to {destination}. "
                f"Available routes include Delhi-Goa, Mumbai-Goa, Bangalore-Goa, Delhi-Jaipur, etc."
            )

        # Sort by price to get cheapest
        cheapest = sorted(matching, key=lambda x: x["price_inr"])[0]
        # Sort by duration to get fastest
        fastest = sorted(matching, key=lambda x: x["duration_hrs"])[0]

        result_lines = [
            f"✈️ Flights from {source} to {destination}:",
            f"",
            f"💰 CHEAPEST OPTION:",
            f"   Airline: {cheapest['airline']} ({cheapest['flight_id']})",
            f"   Price: ₹{cheapest['price_inr']:,}",
            f"   Departure: {cheapest['departure']} → Arrival: {cheapest['arrival']}",
            f"   Duration: {cheapest['duration_hrs']} hrs | Class: {cheapest['class']}",
            f"",
            f"⚡ FASTEST OPTION:",
            f"   Airline: {fastest['airline']} ({fastest['flight_id']})",
            f"   Price: ₹{fastest['price_inr']:,}",
            f"   Departure: {fastest['departure']} → Arrival: {fastest['arrival']}",
            f"   Duration: {fastest['duration_hrs']} hrs | Class: {fastest['class']}",
            f"",
            f"📋 ALL AVAILABLE FLIGHTS ({len(matching)} found):",
        ]

        for f in sorted(matching, key=lambda x: x["price_inr"]):
            result_lines.append(
                f"   • {f['airline']} | ₹{f['price_inr']:,} | "
                f"{f['departure']}-{f['arrival']} | {f['duration_hrs']}hrs"
            )

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error searching flights: {str(e)}"
