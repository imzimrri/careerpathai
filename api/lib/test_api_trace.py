"""
Test script to verify Opik tracing works through the actual API endpoint.
"""

import requests
import json
import time

def test_api_with_tracing():
    """Test the API endpoint and verify tracing works."""
    print("\n" + "="*60)
    print("TESTING API ENDPOINT WITH OPIK TRACING")
    print("="*60)
    
    # API endpoint
    url = "http://localhost:8000/api/generate-career-path"
    
    # Test payload
    payload = {
        "currentRole": "Frontend Developer",
        "targetRole": "ML Engineer"
    }
    
    print(f"\n📤 Sending request to: {url}")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Make the request
        print("\n⏳ Waiting for response...")
        start_time = time.time()
        
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Response received in {elapsed:.2f}s")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS!")
            print(f"📝 Title: {data.get('title')}")
            print(f"🎯 Skills to Learn: {', '.join(data.get('skillsToLearn', []))}")
            print(f"\n✨ Check your Opik dashboard at: https://www.comet.com/opik/")
            print(f"   Project: careerpathai")
            print(f"   You should see a new trace for this request!")
            return True
        else:
            print(f"\n❌ FAILED with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print("   Make sure the server is running:")
        print("   cd api && python index.py")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_api_with_tracing()
    
    if success:
        print("\n" + "="*60)
        print("✅ TEST PASSED - Check your Opik dashboard!")
        print("="*60)
        exit(0)
    else:
        print("\n" + "="*60)
        print("❌ TEST FAILED - See errors above")
        print("="*60)
        exit(1)