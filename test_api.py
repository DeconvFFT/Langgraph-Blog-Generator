#!/usr/bin/env python3
"""
Test script for the Blog Generator API
"""

import requests
import json
from typing import Dict, Any, Optional


def test_blog_api(topic: Optional[str] = None, language: str = "English") -> Dict[str, Any]:
    """
    Test the blog generation API
    
    Args:
        topic (str, optional): Topic for the blog
        language (str): Language for the blog
        
    Returns:
        Dict[str, Any]: API response
    """
    base_url = "http://localhost:8000"
    
    # Test data
    payload = {
        "topic": topic,
        "language": language
    }
    
    try:
        print(f"🔄 Testing blog generation with topic: '{topic}'")
        response = requests.post(
            f"{base_url}/blogs",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ Response Status: {response.status_code}")
        print(f"📊 Response Data:")
        print(json.dumps(result, indent=2))
        
        return result
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API. Make sure the server is running.")
        print("   Run: python app.py")
        return {"error": "Connection failed"}
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        return {"error": f"HTTP Error: {e}"}
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {"error": f"Unexpected error: {e}"}


def test_health_endpoint() -> Dict[str, Any]:
    """Test the health endpoint"""
    base_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{base_url}/health")
        response.raise_for_status()
        result = response.json()
        
        print("✅ Health check passed")
        print(json.dumps(result, indent=2))
        return result
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    print("🚀 Blog Generator API Test Suite")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    test_health_endpoint()
    
    # Test with topic
    print("\n2. Testing blog generation with topic...")
    test_blog_api("The Future of Artificial Intelligence")
    
    # Test without topic (should prompt for user input)
    print("\n3. Testing blog generation without topic...")
    test_blog_api(None)
    
    print("\n🎉 Tests completed!")
