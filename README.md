# 🗺️ Trip India — AI-Powered India Travel Planner

> Generate day-by-day India travel itineraries with budget breakdown, weather & local tips — powered by Groq AI ⚡

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)
![Groq](https://img.shields.io/badge/AI-Groq%20LLaMA-orange)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🤖 **AI Itinerary Generator** — Powered by Groq LLaMA 3.3 70B
- 📅 **Day-by-Day Planning** — Unique activities for each day
- 💰 **Budget Breakdown** — Accommodation, food, transport & more
- 🌤️ **Live Weather** — Real-time weather for your destination
- 🏕️ **50+ Indian Destinations** — Mountains, beaches, heritage & more
- 💡 **Local Travel Tips** — Budget hacks specific to each destination
- 📱 **Fully Responsive** — Works on mobile & desktop

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| AI Model | Groq API (LLaMA 3.3 70B) |
| Database | MongoDB Atlas |
| Weather | OpenWeatherMap API |
| Frontend | HTML, CSS, Jinja2 |
| Deploy | Render / Railway |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/tripsaathi.git
cd tripsaathi
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_api_key
MONGO_URI=your_mongodb_connection_string
WEATHER_API_KEY=your_openweathermap_key
SECRET_KEY=your_secret_key
```

### 5. Run the app

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 🔑 Getting API Keys

| Service | Link | Free? |
|---------|------|-------|
| Groq API | [console.groq.com](https://console.groq.com) | ✅ Free |
| MongoDB Atlas | [atlas.mongodb.com](https://atlas.mongodb.com) | ✅ Free |
| OpenWeatherMap | [openweathermap.org/api](https://openweathermap.org/api) | ✅ Free |

---

## 📁 Project Structure

```
tripsaathi/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Procfile               # For deployment
├── .env                   # Environment variables (not committed)
├── static/
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript files
└── templates/
    ├── base.html          # Base layout
    ├── home.html          # Landing page
    ├── plan.html          # Trip planning form
    ├── itinerary.html     # Generated itinerary
    ├── destinations.html  # Popular destinations
    └── tips.html          # Travel tips
```

---

## 🌍 Deploying to Render (Free)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repository
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Add all environment variables from `.env`
6. Click **Deploy** ✅

---

## 📸 Screenshots

> _Add screenshots of your app here_

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ for Indian budget travelers</p>
