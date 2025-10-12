"""
Quick test to verify Bulgarian language responses
"""
import requests
import json

def test_bulgarian_response():
    url = "http://localhost:8000/api/analyze/"
    data = {
        "team1": "CSKA Sofia",
        "team2": "Levski Sofia"
    }
    
    print("Testing Bulgarian language response...")
    print(f"Request: {json.dumps(data, indent=2)}")
    print("\nSending request to API...")
    
    try:
        response = requests.post(url, json=data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("\n" + "="*80)
            print("✅ SUCCESS! Response received:")
            print("="*80)
            
            # Check if responses are in Bulgarian
            analysis = result.get("analysis", {})
            
            print("\n📊 GOALS PREDICTION (should be in Bulgarian):")
            print(analysis.get("goals_prediction", "N/A")[:200] + "...")
            
            print("\n🏆 WINNER PREDICTION (should be in Bulgarian):")
            print(analysis.get("winner_prediction", "N/A")[:200] + "...")
            
            print("\n⚽ SCORE PREDICTION (should be in Bulgarian):")
            print(analysis.get("score_prediction", "N/A")[:200] + "...")
            
            # Check for Bulgarian characters
            full_text = str(analysis)
            bulgarian_chars = "абвгдежзийклмнопрстуфхцчшщъьюя"
            has_bulgarian = any(char in full_text.lower() for char in bulgarian_chars)
            
            print("\n" + "="*80)
            if has_bulgarian:
                print("✅ Detected Bulgarian characters in response!")
            else:
                print("⚠️ WARNING: No Bulgarian characters detected!")
            print("="*80)
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_bulgarian_response()
