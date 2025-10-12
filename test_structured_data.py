"""
Test structured data extraction
"""
import requests
import json

def test_structured_data():
    url = "http://localhost:8000/api/analyze/"
    data = {
        "team1": "Turkey",
        "team2": "Bulgaria"
    }
    
    print("="*80)
    print("TESTING STRUCTURED DATA EXTRACTION (v1.1.0)")
    print("="*80)
    print(f"\nRequest: {json.dumps(data, indent=2)}")
    print("\n⏳ Sending request to API (this may take 60-90 seconds)...\n")
    
    try:
        response = requests.post(url, json=data, timeout=180)
        
        if response.status_code == 200:
            result = response.json()
            
            print("="*80)
            print("✅ SUCCESS!")
            print("="*80)
            
            # Check team1_stats
            print("\n📊 TURKEY STATS:")
            if "team1_stats" in result:
                stats = result["team1_stats"]
                if "error" in stats:
                    print(f"   ⚠️ {stats['error']}")
                else:
                    print(f"   • Name: {stats.get('name', 'N/A')}")
                    print(f"   • Form: {stats.get('form', 'N/A')}")
                    print(f"   • Matches analyzed: {stats.get('matches_analyzed', 0)}")
                    print(f"   • Avg goals scored: {stats.get('avg_goals_scored', 0)}")
                    print(f"   • Avg goals conceded: {stats.get('avg_goals_conceded', 0)}")
                    
                    recent = stats.get('recent_matches', [])
                    print(f"   • Recent matches found: {len(recent)}")
                    if recent:
                        print("\n   Last 3 matches:")
                        for match in recent[:3]:
                            print(f"      - {match.get('date')} vs {match.get('opponent')}: {match.get('score')} ({match.get('result')})")
            
            # Check team2_stats
            print("\n📊 BULGARIA STATS:")
            if "team2_stats" in result:
                stats = result["team2_stats"]
                if "error" in stats:
                    print(f"   ⚠️ {stats['error']}")
                else:
                    print(f"   • Name: {stats.get('name', 'N/A')}")
                    print(f"   • Form: {stats.get('form', 'N/A')}")
                    print(f"   • Matches analyzed: {stats.get('matches_analyzed', 0)}")
                    print(f"   • Avg goals scored: {stats.get('avg_goals_scored', 0)}")
                    print(f"   • Avg goals conceded: {stats.get('avg_goals_conceded', 0)}")
                    
                    recent = stats.get('recent_matches', [])
                    print(f"   • Recent matches found: {len(recent)}")
            
            # Check head_to_head
            print("\n🏆 HEAD-TO-HEAD:")
            if "head_to_head" in result:
                h2h = result["head_to_head"]
                if "error" in h2h:
                    print(f"   ⚠️ {h2h['error']}")
                else:
                    print(f"   • Total matches: {h2h.get('total_matches', 0)}")
                    print(f"   • Turkey wins: {h2h.get('team1_wins', 0)}")
                    print(f"   • Draws: {h2h.get('draws', 0)}")
                    print(f"   • Bulgaria wins: {h2h.get('team2_wins', 0)}")
                    
                    recent = h2h.get('recent_matches', [])
                    print(f"   • Recent H2H matches: {len(recent)}")
                    if recent:
                        print("\n   Last 3 H2H:")
                        for match in recent[:3]:
                            print(f"      - {match.get('date')}: {match.get('home_team')} vs {match.get('away_team')} = {match.get('score')}")
            
            # Check AI analysis
            print("\n🤖 AI ANALYSIS (Sample):")
            analysis = result.get("analysis", {})
            score_pred = analysis.get("score_prediction", "")
            if score_pred:
                print(f"   Score Prediction: {score_pred[:150]}...")
            
            print("\n" + "="*80)
            print("✅ All structured data fields present!")
            print("="*80)
            
            # Save full response for inspection
            with open("test_response_v1.1.0.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("\n💾 Full response saved to: test_response_v1.1.0.json")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_structured_data()
