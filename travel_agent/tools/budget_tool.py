"""
Budget Estimation Tool for the AI Travel Planning Agent.
Calculates total trip cost including flight, hotel, food, and local expenses.
"""

from langchain.tools import tool


# Per-person per-day local expense estimates (INR) by city
DAILY_LOCAL_EXPENSES = {
    "Goa": {"food": 600, "transport": 400, "activities": 300},
    "Mumbai": {"food": 800, "transport": 500, "activities": 200},
    "Delhi": {"food": 600, "transport": 350, "activities": 200},
    "Jaipur": {"food": 500, "transport": 300, "activities": 400},
    "Kerala": {"food": 500, "transport": 400, "activities": 300},
    "Manali": {"food": 500, "transport": 500, "activities": 600},
    "Agra": {"food": 450, "transport": 350, "activities": 500},
    "Bangalore": {"food": 700, "transport": 350, "activities": 200},
    "Chennai": {"food": 600, "transport": 300, "activities": 200},
    "Hyderabad": {"food": 550, "transport": 300, "activities": 200},
    "Default": {"food": 550, "transport": 350, "activities": 300},
}


@tool
def estimate_budget(query: str) -> str:
    """
    Estimate the total trip budget including flight, hotel, food, and activities.

    Input format: "destination days:<N> flight:<price> hotel:<price_per_night>"
    Examples:
        "Goa days:3 flight:4800 hotel:3200"
        "Jaipur days:5 flight:1800 hotel:2200"
        "Manali days:4 flight:4200 hotel:2500"

    Returns a detailed cost breakdown and total estimated budget.
    """
    try:
        parts = query.strip().split()
        destination = parts[0].title()

        days = 3
        flight_cost = 0
        hotel_per_night = 0

        for part in parts[1:]:
            if part.startswith("days:"):
                try:
                    days = int(part.split(":")[1])
                except ValueError:
                    pass
            elif part.startswith("flight:"):
                try:
                    flight_cost = int(part.split(":")[1])
                except ValueError:
                    pass
            elif part.startswith("hotel:"):
                try:
                    hotel_per_night = int(part.split(":")[1])
                except ValueError:
                    pass

        local = DAILY_LOCAL_EXPENSES.get(destination, DAILY_LOCAL_EXPENSES["Default"])

        # Calculations
        hotel_total = hotel_per_night * days
        food_total = local["food"] * days
        transport_total = local["transport"] * days
        activities_total = local["activities"] * days
        local_total = food_total + transport_total + activities_total
        grand_total = flight_cost + hotel_total + local_total

        # Budget tier classification
        if grand_total < 15000:
            tier = "🟢 Budget-Friendly"
        elif grand_total < 35000:
            tier = "🟡 Mid-Range"
        else:
            tier = "🔴 Premium"

        result_lines = [
            f"💰 Budget Breakdown for {days}-Day Trip to {destination}:",
            f"{'='*50}",
            f"",
            f"  ✈️  Flight (round trip estimate): ₹{flight_cost * 2:,}",
            f"      (Outbound: ₹{flight_cost:,} × 2 for return)",
            f"",
            f"  🏨  Accommodation:",
            f"      ₹{hotel_per_night:,}/night × {days} nights = ₹{hotel_total:,}",
            f"",
            f"  🍽️  Food & Dining:",
            f"      ₹{local['food']:,}/day × {days} days = ₹{food_total:,}",
            f"",
            f"  🚌  Local Transport:",
            f"      ₹{local['transport']:,}/day × {days} days = ₹{transport_total:,}",
            f"",
            f"  🎡  Activities & Entry Fees:",
            f"      ₹{local['activities']:,}/day × {days} days = ₹{activities_total:,}",
            f"",
            f"{'='*50}",
            f"  📊  TOTAL ESTIMATE: ₹{grand_total + flight_cost:,}",
            f"      (Including return flight)",
            f"",
            f"  {tier}",
            f"",
            f"💡 Tips to save money:",
        ]

        if flight_cost > 5000:
            result_lines.append("  • Book flights 4-6 weeks in advance for lower prices")
        if hotel_per_night > 4000:
            result_lines.append("  • Consider 3-star hotels or guesthouses for better value")
        result_lines.append("  • Use local autos/buses instead of cabs to cut transport costs")
        result_lines.append("  • Eat at local restaurants instead of hotel restaurants")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error estimating budget: {str(e)}"
