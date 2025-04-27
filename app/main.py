from fastapi import FastAPI
import socket
from datetime import datetime
import requests
import os

app = FastAPI()

# Load environment variables
VERSION = os.getenv("API_VERSION", "v1.0.0")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@app.get("/api/hello")
def hello():
    hostname = socket.gethostname()
    now = datetime.utcnow().strftime("%y%m%d%H%M")
    try:
        weather_response = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Dhaka",
            timeout=10
        )
        weather_data = weather_response.json()
        temperature = weather_data["current"]["temp_c"]
    except Exception:
        temperature = "N/A"
    return {
        "hostname": hostname,
        "datetime": now,
        "version": VERSION,
        "weather": {
            "dhaka": {
                "temperature": temperature,
                "temp_unit": "c"
            }
        }
    }

@app.get("/api/health")
def health():
    if not WEATHER_API_KEY:
        return {"status": "unhealthy", "details": "Missing WEATHER_API_KEY"}

    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Dhaka"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return {"status": "healthy"}
        else:
            return {
                "status": "unhealthy",
                "details": f"Weather API returned {response.status_code}",
            }
    except Exception as e:
        return {"status": "unhealthy", "details": str(e)}

