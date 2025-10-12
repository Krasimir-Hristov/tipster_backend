"""
Test script for The Odds API integration
Simulates match data coming from The Odds API
"""

import requests
import json
from datetime import datetime

# API endpoint
API_URL = "http://localhost:8000/api/analyze/"

# Test match 1: The Odds API format (RECOMMENDED)
print("=" * 70)
print("TEST 1: The Odds API Format (Home: Turkey, Away: Bulgaria)")
print("=" * 70)

odds_api_match = {
    "id": "abc123xyz789test001",
    "sport_key": "soccer_uefa_european_championship_qualifying",
    "sport_title": "UEFA Euro Qualifying",
    "commence_time": "2025-10-12T19:00:00Z",
    "home_team": "Turkey",
    "away_team": "Bulgaria"
}

print("\n📤 Sending request with The Odds API format:")
print(json.dumps(odds_api_match, indent=2))

try:
    response = requests.post(API_URL, json=odds_api_match, timeout=180)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Success! Response:")
        print(f"   Match ID: {result.get('match_id')}")
        print(f"   Teams: {result.get('team1')} vs {result.get('team2')}")
        print(f"   Commence Time: {result.get('commence_time')}")
        print(f"   Sport: {result.get('sport_key')}")
        print(f"\n🏆 Финална прогноза:")
        print(result['analysis']['score_prediction'][:200] + "...")
        
        # Save full response
        with open("test_odds_api_response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\n💾 Пълен отговор записан в: test_odds_api_response.json")
    else:
        print(f"\n❌ Error {response.status_code}:")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("\n⏱️ Request timeout - анализът отнема твърде дълго време")
except requests.exceptions.ConnectionError:
    print("\n❌ Connection error - уверете се че Django сървърът работи на http://localhost:8000")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

# Test match 2: Legacy format (still works)
print("\n" + "=" * 70)
print("TEST 2: Legacy Format (team1/team2)")
print("=" * 70)

legacy_match = {
    "team1": "Spain",
    "team2": "Bulgaria"
}

print("\n📤 Sending request with legacy format:")
print(json.dumps(legacy_match, indent=2))

try:
    response = requests.post(API_URL, json=legacy_match, timeout=180)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Success! Response:")
        print(f"   Teams: {result.get('team1')} vs {result.get('team2')}")
        print(f"   Match ID: {result.get('match_id')} (should be None for legacy format)")
        print(f"\n🏆 Финална прогноза:")
        print(result['analysis']['score_prediction'][:200] + "...")
    else:
        print(f"\n❌ Error {response.status_code}:")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("\n⏱️ Request timeout")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "=" * 70)
print("Tests completed!")
print("=" * 70)
