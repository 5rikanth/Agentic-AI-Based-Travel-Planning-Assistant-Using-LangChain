# ✈️ Agentic AI-Based Travel Planning Assistant

> **Capstone Project** | Domain: Travel/Tourism  
> Built with: Python · LangChain · OpenAI · Streamlit · Open-Meteo API

---

## 📋 Problem Statement

Planning a trip requires choosing flights, hotels, and attractions while balancing time, budget, weather, and personal preferences. Travelers often switch between multiple websites, compare inconsistent information, and manually build itineraries. This project solves that with an **intelligent, agentic AI system** that reasons like a travel expert and generates complete, optimized itineraries in seconds.

---

## 🏗️ Project Structure

```
travel_agent/
├── app.py                  # Streamlit web application
├── agent.py                # LangChain ReAct agent setup
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── tools/                  # LangChain tool definitions
│   ├── __init__.py
│   ├── flight_tool.py      # Flight search (flights.json)
│   ├── hotel_tool.py       # Hotel recommendations (hotels.json)
│   ├── places_tool.py      # Attractions discovery (places.json)
│   ├── weather_tool.py     # Live weather (Open-Meteo API)
│   └── budget_tool.py      # Budget estimation
│
├── data/                   # JSON datasets
│   ├── flights.json        # 20 flight routes across India
│   ├── hotels.json         # 20 hotels across major cities
│   └── places.json         # 25 tourist attractions
│
└── utils/
    └── itinerary_formatter.py  # Formatting helpers
```

---

## ⚙️ Setup Instructions

### 1. Clone / Download the project

```bash
cd travel_agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key

**Option A — Environment variable:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Option B — `.env` file:**
```
OPENAI_API_KEY=sk-your-key-here
```

**Option C — Streamlit sidebar input** (for demos)

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

### 5. (Optional) Run CLI mode

```bash
python agent.py
```

---

## 🧰 Tools Overview

| Tool | File | Description |
|------|------|-------------|
| `search_flights` | `flight_tool.py` | Searches flights.json, returns cheapest + fastest options |
| `search_hotels` | `hotel_tool.py` | Recommends hotels by city, rating, and budget tier |
| `search_places` | `places_tool.py` | Discovers top-rated attractions with day-wise suggestions |
| `get_weather` | `weather_tool.py` | Calls Open-Meteo API for 7-day forecast (no API key needed) |
| `estimate_budget` | `budget_tool.py` | Breaks down full trip cost with savings tips |

---

## 🤖 Agent Architecture

```
User Query
    │
    ▼
LangChain ReAct Agent (GPT-4o-mini)
    │
    ├── 🔍 search_flights("Delhi to Goa")
    ├── 🏨 search_hotels("Goa budget:mid")
    ├── 🗺️ search_places("Goa")
    ├── 🌤️ get_weather("Goa")
    └── 💰 estimate_budget("Goa days:3 flight:4800 hotel:3200")
    │
    ▼
Synthesized Itinerary (structured output)
```

The agent uses **ReAct (Reason + Act)** pattern:
- **Reason**: Think about what information is needed
- **Act**: Call the appropriate tool
- **Observe**: Process the tool result
- **Repeat** until all data is gathered
- **Synthesize**: Generate the final structured itinerary

---

## 📊 Data Sources

| Source | Type | Details |
|--------|------|---------|
| `flights.json` | Local JSON | 20 routes, 5 airlines, Delhi/Mumbai/Bangalore departures |
| `hotels.json` | Local JSON | 20 hotels, 2–5 stars, 7 cities, ₹1,200–₹18,000/night |
| `places.json` | Local JSON | 25 POIs, 8 types, with ratings, fees, and descriptions |
| Open-Meteo API | Live REST API | Free, no API key, 7-day forecast with WMO weather codes |

---

## 💡 Example Queries

```
"Plan a 3-day budget trip from Delhi to Goa in February"
"5-day Rajasthan heritage tour from Mumbai to Jaipur, prefer luxury hotels"
"4-day adventure trip to Manali, starting from Delhi, budget under ₹20,000"
"Weekend trip to Kerala for 2 days from Bangalore, interested in nature"
```

---

## 📤 Expected Output

```
============================================================
  🌴 YOUR 3-DAY TRIP TO GOA
  📅 Feb 12 – Feb 14, 2025
============================================================

✈️  FLIGHT SELECTED
   Airline: SpiceJet
   Departure: 20:00 | Arrival: 22:30
   Price: ₹4,200

🏨  HOTEL BOOKED
   Pousada Tauma (3★ | Rating: 4.2/5)
   ₹2,100/night × 3 nights

📋  DAY-WISE ITINERARY

  📅 Day 1 — Thursday, Feb 12 | 🌡️ 31°C | Clear sky ☀️
     • Baga Beach (Beach) — Entry: Free | ~3hrs
     • Candolim Market (Market) — Entry: Free | ~2hrs

  📅 Day 2 — Friday, Feb 13 | 🌡️ 30°C | Mainly clear 🌤️
     • Basilica of Bom Jesus (Heritage) — Entry: Free | ~1.5hrs
     • Old Goa Heritage Walk (Culture) — Entry: ₹50 | ~3hrs

  📅 Day 3 — Saturday, Feb 14 | 🌡️ 29°C | Partly cloudy ⛅
     • Calangute Beach Water Sports (Adventure) — Entry: ₹500 | ~3hrs

💰  BUDGET BREAKDOWN
   Flight (return): ₹8,400
   Hotel:           ₹6,300
   Food:            ₹1,800
   Transport:       ₹1,200
   Activities:      ₹900
   ──────────────────────────────
   TOTAL:           ₹18,600
============================================================
```

---

## 🧪 Running Individual Tools (No API Key)

```python
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels

print(search_flights.invoke("Delhi to Goa"))
print(search_hotels.invoke("Goa budget:mid"))
```

---

## 🛠️ Coding Standards Followed

- **PEP 8** compliant formatting throughout
- **Docstrings** on every function and module
- **Type hints** used where appropriate  
- **Error handling** with try/except in all tools and agent
- **Modular structure** — each tool is a self-contained module
- **Meaningful naming** — no single-letter variables

---

## 📚 References

| Resource | Link |
|----------|------|
| Streamlit Docs | https://docs.streamlit.io |
| LangChain Docs | https://docs.langchain.com |
| Open-Meteo API | https://open-meteo.com |
| Data Files | Google Drive (provided by instructor) |

---

## 🏁 Submission Checklist

- [x] Problem statement clearly explained  
- [x] flights.json, hotels.json, places.json datasets used  
- [x] Open-Meteo weather API integrated  
- [x] LangChain tools built for all data sources  
- [x] ReAct agent implemented with autonomous decision-making  
- [x] Structured itinerary output with day-wise plan  
- [x] Budget breakdown included  
- [x] Streamlit UI with interactive features  
- [x] PEP 8 compliant, modular, documented code  
- [x] README with setup instructions  
