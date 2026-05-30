# TripSaathi — Deployment Guide

## ✅ Zero-Error Deployment Steps

### Step 1: Create GitHub Repo
1. Go to github.com → New repository
2. Name it: `tripsaathi`
3. Upload ALL these files to the repo

### Step 2: Get Free API Keys

#### OpenWeatherMap (Weather) — FREE
1. Go to openweathermap.org → Sign up free
2. Go to API Keys → copy your key

#### Anthropic API (AI) — FREE tier
1. Go to console.anthropic.com → Sign up
2. Go to API Keys → Create key → copy it

#### Google Maps API (optional)
1. Go to console.cloud.google.com
2. Enable Maps JavaScript API
3. Create credentials → API key

### Step 3: Deploy on Render
1. Go to render.com → New Web Service
2. Connect your GitHub repo
3. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Python version: 3.11

### Step 4: Add Environment Variables on Render
```
SECRET_KEY          = any_random_string_here
MONGO_URI           = mongodb+srv://...
GOOGLE_CLIENT_ID    = your_google_client_id
GOOGLE_CLIENT_SECRET = your_google_client_secret
ANTHROPIC_API_KEY   = your_anthropic_key
WEATHER_API_KEY     = your_openweather_key
GOOGLE_MAPS_API_KEY = your_maps_key (optional)
```

### Step 5: Update Google OAuth
In Google Cloud Console → OAuth credentials:
- Authorized origins: https://your-app.onrender.com
- Authorized redirect URIs: https://your-app.onrender.com/auth/callback

## ✅ Why This Won't Have Errors
- Single app.py file — no circular imports
- Only 6 packages in requirements.txt
- Correct Procfile: `gunicorn app:app`
- host="0.0.0.0" and PORT from environment
- Works even without API keys (shows sample data)
- Google login falls back to demo mode if keys missing
