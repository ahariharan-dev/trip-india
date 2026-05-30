import os
import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import json
from groq import Groq

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "tripsaathi_dev_secret")

@app.template_filter('format_number')
def format_number(value):
    try:
        return "{:,}".format(int(value))
    except:
        return value

# ── MongoDB ──────────────────────────────────────────────
MONGO_URI = os.environ.get("MONGO_URI", "")
db = None
if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client["tripsaathi"]
    except Exception as e:
        print(f"MongoDB connection error: {e}")

# ── Weather ──────────────────────────────────────────────
def get_weather(city):
    api_key = os.environ.get("WEATHER_API_KEY", "")
    if not api_key:
        return None
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return {
                "temp": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "icon": data["weather"][0]["icon"]
            }
    except:
        pass
    return None

# ── AI Itinerary using Groq ───────────────────────────────
def generate_itinerary(destination, days, budget, travelers, travel_style):
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        print("No Groq API key found, using sample itinerary")
        return get_sample_itinerary(destination, days, budget)

    try:
        prompt = f"""Create a detailed {days}-day budget travel itinerary for {destination}, India.
Budget: Rs.{budget} total for {travelers} person(s). Travel style: {travel_style}.

IMPORTANT: Make EVERY day completely different with UNIQUE activities specific to {destination}.

Return ONLY a valid JSON object. No explanation, no markdown, just JSON:
{{
  "destination": "{destination}",
  "days": {days},
  "total_budget": {budget},
  "budget_breakdown": {{
    "accommodation": {int(budget * 0.35)},
    "food": {int(budget * 0.25)},
    "transport": {int(budget * 0.20)},
    "activities": {int(budget * 0.15)},
    "miscellaneous": {int(budget * 0.05)}
  }},
  "best_time_to_visit": "best months to visit {destination}",
  "tips": [
    "specific budget tip for {destination}",
    "specific transport tip for {destination}",
    "specific food tip for {destination}"
  ],
  "itinerary": [
    {{
      "day": 1,
      "title": "Arrival and first exploration",
      "morning": "specific morning activity unique to day 1",
      "afternoon": "specific afternoon activity unique to day 1",
      "evening": "specific evening activity unique to day 1",
      "accommodation": "specific budget stay name and price in {destination}",
      "food": "specific local dish or restaurant for day 1",
      "estimated_cost": {budget // max(days, 1)}
    }}
  ]
}}

Generate all {days} days, each with completely different activities."""

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        text = response.choices[0].message.content
        text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end > start:
            return json.loads(text[start:end])

    except Exception as e:
        print(f"Groq error: {e}")

    return get_sample_itinerary(destination, days, budget)


def get_sample_itinerary(destination, days, budget):
    per_day = budget // max(days, 1)
    return {
        "destination": destination,
        "days": days,
        "total_budget": budget,
        "budget_breakdown": {
            "accommodation": int(budget * 0.35),
            "food": int(budget * 0.25),
            "transport": int(budget * 0.20),
            "activities": int(budget * 0.15),
            "miscellaneous": int(budget * 0.05)
        },
        "best_time_to_visit": "October to March",
        "tips": [
            "Book trains in advance via IRCTC for cheaper fares",
            "Carry cash as many local places don't accept cards",
            "Use local buses instead of autos to save money"
        ],
        "itinerary": [
            {
                "day": i + 1,
                "title": f"Day {i+1} - Explore {destination}",
                "morning": f"Visit the most famous attraction in {destination}. Start early to avoid crowds.",
                "afternoon": f"Explore local market and try street food. Budget Rs.100-150 for lunch.",
                "evening": f"Sunset point or local park. Try local chai and snacks.",
                "accommodation": f"Budget hostel or guesthouse - Rs.{int(per_day * 0.35)}/night",
                "food": f"Street food + local restaurant - Rs.{int(per_day * 0.25)}/day",
                "estimated_cost": per_day
            }
            for i in range(days)
        ]
    }


# ── Routes ───────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/plan")
def plan():
    return render_template("plan.html")

@app.route("/generate", methods=["POST"])
def generate():
    destination = request.form.get("destination", "").strip()
    days = int(request.form.get("days", 3))
    budget = int(request.form.get("budget", 5000))
    travelers = int(request.form.get("travelers", 1))
    travel_style = request.form.get("travel_style", "adventure")

    if not destination:
        flash("Please enter a destination.")
        return redirect(url_for("plan"))

    days = max(1, min(days, 14))
    budget = max(500, min(budget, 200000))

    itinerary = generate_itinerary(destination, days, budget, travelers, travel_style)
    weather = get_weather(destination)

    session["last_itinerary"] = itinerary
    session["last_weather"] = weather

    return render_template("itinerary.html",
        itinerary=itinerary,
        weather=weather,
        maps_key=""
    )

@app.route("/destinations")
def destinations():
    popular = [
        {"name": "Manali", "state": "Himachal Pradesh", "type": "Mountains", "budget": "Rs.5,000-15,000", "emoji": "🏔️"},
        {"name": "Goa", "state": "Goa", "type": "Beach", "budget": "Rs.8,000-20,000", "emoji": "🏖️"},
        {"name": "Jaipur", "state": "Rajasthan", "type": "Heritage", "budget": "Rs.4,000-12,000", "emoji": "🏰"},
        {"name": "Rishikesh", "state": "Uttarakhand", "type": "Adventure", "budget": "Rs.3,000-8,000", "emoji": "🌊"},
        {"name": "Darjeeling", "state": "West Bengal", "type": "Hills", "budget": "Rs.5,000-12,000", "emoji": "🍵"},
        {"name": "Hampi", "state": "Karnataka", "type": "Ruins", "budget": "Rs.3,000-8,000", "emoji": "🏛️"},
        {"name": "Spiti Valley", "state": "Himachal Pradesh", "type": "Remote", "budget": "Rs.10,000-25,000", "emoji": "❄️"},
        {"name": "Varanasi", "state": "Uttar Pradesh", "type": "Spiritual", "budget": "Rs.3,000-8,000", "emoji": "🪔"},
        {"name": "Coorg", "state": "Karnataka", "type": "Nature", "budget": "Rs.5,000-12,000", "emoji": "☕"},
        {"name": "Andaman", "state": "Andaman & Nicobar", "type": "Island", "budget": "Rs.15,000-35,000", "emoji": "🐠"},
        {"name": "Ladakh", "state": "Jammu & Kashmir", "type": "Himalayan", "budget": "Rs.12,000-30,000", "emoji": "🏕️"},
        {"name": "Munnar", "state": "Kerala", "type": "Tea Gardens", "budget": "Rs.5,000-12,000", "emoji": "🌿"},
    ]
    return render_template("destinations.html", destinations=popular)

@app.route("/tips")
def tips():
    return render_template("tips.html")

@app.route("/api/weather")
def api_weather():
    city = request.args.get("city", "")
    if not city:
        return jsonify({"error": "City required"}), 400
    weather = get_weather(city)
    if weather:
        return jsonify(weather)
    return jsonify({"error": "Weather not available"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)