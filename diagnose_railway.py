#!/usr/bin/env python3
"""
Railway deployment diagnostics script
Run this to check what's causing the 502 errors
"""

import sys
import os

def check_imports():
    """Check if all required modules can be imported"""
    print("🔍 Checking module imports...")
    
    try:
        import fastapi
        print(f"✅ fastapi: {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ fastapi: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✅ uvicorn: {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ uvicorn: {e}")
        return False
    
    try:
        import pydantic
        print(f"✅ pydantic: {pydantic.__version__}")
    except ImportError as e:
        print(f"❌ pydantic: {e}")
        return False
    
    try:
        from src.graphs.graph_builder import GraphBuilder
        print("✅ GraphBuilder imported successfully")
    except ImportError as e:
        print(f"❌ GraphBuilder: {e}")
        print("⚠️  This suggests your src/ directory structure isn't being found")
        return False
    
    try:
        from src.llms.groqllm import GroqLLM
        print("✅ GroqLLM imported successfully")
    except ImportError as e:
        print(f"❌ GroqLLM: {e}")
        return False
    
    try:
        from src.states.blogstate import BlogState
        print("✅ BlogState imported successfully")
    except ImportError as e:
        print(f"❌ BlogState: {e}")
        return False
    
    return True

def check_environment():
    """Check environment variables"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = ['PORT', 'GROQ_API_KEY']
    optional_vars = ['HOST', 'RAILWAY_ENVIRONMENT', 'LANGSMITH_API_KEY']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'GROQ_API_KEY':
                print(f"✅ {var}: {'*' * min(len(value), 20)} (length: {len(value)})")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET (REQUIRED)")
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"ℹ️  {var}: {value}")
        else:
            print(f"⚪ {var}: not set (optional)")

def check_file_structure():
    """Check if required files exist"""
    print("\n🔍 Checking file structure...")
    
    required_files = [
        'app_fastapi.py',
        'requirements.txt',
        'Procfile',
        'src/__init__.py',
        'src/graphs/__init__.py',
        'src/graphs/graph_builder.py',
        'src/llms/__init__.py',
        'src/llms/groqllm.py',
        'src/states/__init__.py',
        'src/states/blogstate.py',
        'src/nodes/__init__.py',
        'src/nodes/blog_node.py'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")

def test_groq_connection():
    """Test if Groq API key works"""
    print("\n🔍 Testing Groq connection...")
    
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("❌ GROQ_API_KEY not set - cannot test connection")
        return False
    
    try:
        from src.llms.groqllm import GroqLLM
        groqllm = GroqLLM()
        llm = groqllm.get_llm()
        
        # Test with a simple call
        result = llm.invoke("Hello, please respond with just 'OK'")
        print(f"✅ Groq API test successful: {result}")
        return True
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")
        return False

def main():
    """Run all diagnostics"""
    print("🔧 Railway Deployment Diagnostics")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"📂 Directory contents: {os.listdir('.')}")
    
    # Run all checks
    imports_ok = check_imports()
    check_environment()
    check_file_structure()
    
    if imports_ok:
        groq_ok = test_groq_connection()
    else:
        groq_ok = False
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSIS SUMMARY")
    print("=" * 50)
    
    if imports_ok and groq_ok:
        print("✅ All checks passed - deployment should work")
        print("💡 If you're still getting 502, check Railway logs for runtime errors")
    elif imports_ok:
        print("⚠️  Imports work but Groq connection failed")
        print("💡 Check your GROQ_API_KEY in Railway environment variables")
    else:
        print("❌ Import failures detected")
        print("💡 Check your requirements.txt and file structure in Railway")
    
    print("\n🔧 RECOMMENDED FIXES:")
    print("1. Ensure all files are uploaded to Railway")
    print("2. Set GROQ_API_KEY environment variable in Railway")
    print("3. Use the minimal app (app_minimal.py) to test basic deployment")
    print("4. Check Railway build logs for detailed error messages")

if __name__ == '__main__':
    main()
