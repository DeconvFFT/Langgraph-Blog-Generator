#!/usr/bin/env python3
"""
Quick test script to check if the FastAPI backend is running
"""

import requests
import time

def test_api_connection():
    """Test connection to the FastAPI backend"""
    
    # Test URLs
    test_urls = [
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    for base_url in test_urls:
        print(f"🔍 Testing connection to: {base_url}")
        
        try:
            # Test health endpoint
            health_url = f"{base_url}/health"
            response = requests.get(health_url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ API is running at: {base_url}")
                print(f"📊 Health check response: {response.json()}")
                return base_url
            else:
                print(f"⚠️ API responded with status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to: {base_url}")
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout connecting to: {base_url}")
        except Exception as e:
            print(f"❌ Error testing {base_url}: {e}")
    
    return None

def start_local_api():
    """Instructions to start the local API"""
    print("\n🚀 To start the local FastAPI backend:")
    print("1. Open a new terminal")
    print("2. Navigate to your project directory")
    print("3. Run: python app_fastapi.py")
    print("4. The API will start on http://localhost:8000")
    print("5. Keep this terminal running")
    print("6. Then test your Gradio app again")

if __name__ == "__main__":
    print("🔧 FastAPI Backend Connection Test")
    print("=" * 40)
    
    # Test connection
    api_url = test_api_connection()
    
    if api_url:
        print(f"\n🎉 Success! Your API is running at: {api_url}")
        print("Your Gradio app should work now.")
    else:
        print("\n❌ No API connection found.")
        start_local_api()
