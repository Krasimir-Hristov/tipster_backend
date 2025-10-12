import requests
import json

url = "http://localhost:8000/api/analyze/"
data = {
    "id": "test123",
    "sport_key": "soccer_uefa_euro",
    "home_team": "Turkey",
    "away_team": "Bulgaria",
    "commence_time": "2025-03-22T19:00:00Z"
}

print("Sending request...")
response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ Success! Check server logs for model names")
else:
    print(f"❌ Error: {response.text}")
