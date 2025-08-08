#!/usr/bin/env python3
"""
Quick Railway deployment test
"""

import requests
import sys

def test_railway():
    """Test Railway deployment"""
    
    # Get Railway URL from user
    railway_url = input("Enter your Railway URL (e.g., https://your-app.railway.app): ").strip()
    
    if not railway_url:
        print("❌ No URL provided")
        return
    
    railway_url = railway_url.rstrip('/')
    
    print(f"🔍 Testing Railway deployment at: {railway_url}")
    print()
    
    # Test endpoints
    endpoints = [
        ("Health Check", f"{railway_url}/health"),
        ("Test Endpoint", f"{railway_url}/test"),
        ("Root", f"{railway_url}/"),
    ]
    
    for name, url in endpoints:
        print(f"Testing {name}: {url}")
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"📊 Response: {data}")
                except:
                    print(f"📄 Response: {response.text[:200]}...")
            else:
                print(f"❌ Error: {response.text}")
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Cannot connect to Railway")
        except requests.exceptions.Timeout:
            print("⏰ Timeout: Railway is not responding")
        except Exception as e:
            print(f"❌ Error: {e}")
        print()
    
    print("🔧 If you see connection errors:")
    print("1. Check Railway dashboard for deployment status")
    print("2. Verify GROQ_API_KEY is set in Railway environment variables")
    print("3. Check Railway logs for any error messages")
    print("4. Make sure the service is not paused")

if __name__ == "__main__":
    test_railway()
