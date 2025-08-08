#!/usr/bin/env python3

# Simple test to verify the native app works
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from hf_spaces_app_native import demo
    print("✅ Native app imported successfully!")
    
    # Test launch
    if __name__ == "__main__":
        print("🚀 Launching native Gradio app...")
        demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
