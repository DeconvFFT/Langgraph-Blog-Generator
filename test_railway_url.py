#!/usr/bin/env python3
"""
Test Railway URL and custom domain issues
"""

import requests
import sys

def test_railway_url():
    """Test Railway URL and help with domain issues"""
    
    print("🔍 Railway URL Test")
    print("=" * 40)
    
    # Get Railway URL
    railway_url = input("Enter your Railway URL (e.g., https://your-app.railway.app): ").strip()
    
    if not railway_url:
        print("❌ No URL provided")
        return
    
    railway_url = railway_url.rstrip('/')
    
    print(f"🔍 Testing: {railway_url}")
    print()
    
    # Test health endpoint
    health_url = f"{railway_url}/health"
    print(f"Testing health endpoint: {health_url}")
    
    try:
        response = requests.get(health_url, timeout=10)
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"📊 Response: {data}")
                print("✅ Railway API is working!")
                
                if data.get('groq_key_set'):
                    print("✅ GROQ_API_KEY is set")
                else:
                    print("❌ GROQ_API_KEY is not set")
                    
            except:
                print(f"📄 Response: {response.text[:200]}...")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot connect to Railway")
        print("\n🔧 Possible solutions:")
        print("1. Check if the Railway URL is correct")
        print("2. Make sure Railway service is running")
        print("3. Try the Railway-provided URL, not custom domain")
        
    except requests.exceptions.Timeout:
        print("⏰ Timeout: Railway is not responding")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("🌐 Domain Configuration:")
    print("If you're using a custom domain, make sure:")
    print("1. Domain is configured in Railway → Settings → Domains")
    print("2. DNS points to Railway")
    print("3. SSL certificate is issued")
    print()
    print("💡 Quick fix: Use Railway URL instead of custom domain")
    print("   Railway URL format: https://your-app-name.railway.app")

if __name__ == "__main__":
    test_railway_url()
