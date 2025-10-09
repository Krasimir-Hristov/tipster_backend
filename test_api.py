import requests
import json

# Test the API endpoint
url = "http://127.0.0.1:8001/api/analyze/"
data = {
    "team1": "Scotland",
    "team2": "Greece"
}

print("🏴󠁧󠁢󠁳󠁣󠁴󠁿⚽🇬🇷 Testing Scotland vs Greece analysis...")
print("-" * 60)

try:
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print("-" * 60)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS!")
        print("\n📊 ANALYSIS RESULTS:\n")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("❌ ERROR!")
        print(response.text)
        
except Exception as e:
    print(f"❌ Connection Error: {e}")
