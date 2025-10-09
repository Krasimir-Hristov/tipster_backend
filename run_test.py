"""
Simple test script ttry:
    # Test the API
    url = "http://127.0.0.1:8002/api/analyze/"
    data = {
        "team1": "Kosovo",
        "team2": "Slovenia"
    }
    
    print("\n" + "=" * 70)
    print("🇽🇰⚽🇸🇮 TESTING: Kosovo vs Slovenia")
    print("=" * 70)e server and tests the API
"""
import subprocess
import time
import requests
import json
import sys

print("=" * 70)
print("[STARTING DJANGO SERVER]")
print("=" * 70)

# Start Django server in background
server_process = subprocess.Popen(
    [r".\.venv\Scripts\python.exe", "manage.py", "runserver", "8002"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait for server to start
print("[WAITING] Server starting...")
time.sleep(5)

try:
    # Test the API
    url = "http://127.0.0.1:8002/api/analyze/"
    data = {
        "team1": "Scotland",
        "team2": "Greece"
    }
    
    print("\n" + "=" * 70)
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿⚽🇬🇷 TESTING: Scotland vs Greece")
    print("=" * 70)
    print(f"📡 Sending POST request to: {url}")
    print(f"📦 Data: {json.dumps(data, indent=2)}")
    print("\n⏳ This may take 30-60 seconds (AI is thinking)...\n")
    
    # Make the request with longer timeout (AI analysis takes time)
    response = requests.post(url, json=data, timeout=120)
    
    print("=" * 70)
    print(f"✅ Response Status: {response.status_code}")
    print("=" * 70)
    
    if response.status_code == 200:
        result = response.json()
        print("\n🎉 SUCCESS! Here's the AI analysis:\n")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n❌ ERROR Response:")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("\n⏰ Request timed out - the AI is taking too long to respond")
    print("This might be normal for the first request. Try running again.")
    
except requests.exceptions.ConnectionError:
    print("\n❌ Could not connect to server")
    print("The server might not have started properly.")
    
except Exception as e:
    print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")
    
finally:
    # Stop the server
    print("\n" + "=" * 70)
    print("🛑 Stopping server...")
    print("=" * 70)
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except:
        server_process.kill()
    print("✅ Server stopped")
    
print("\n" + "=" * 70)
print("🏁 TEST COMPLETE")
print("=" * 70)
