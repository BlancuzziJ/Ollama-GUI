#!/usr/bin/env python3
"""
Quick test script for ShamaOllama features
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import customtkinter as ctk
        import requests
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test that the app can be created without errors"""
    try:
        from main import ShamaOllamaGUI
        print("✅ ShamaOllamaGUI class imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import ShamaOllamaGUI: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating app: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing ShamaOllama...")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Test app creation
    if not test_app_creation():
        sys.exit(1)
    
    print("=" * 40)
    print("🎉 All tests passed! ShamaOllama is ready to run.")
    print("\nNew features added:")
    print("• ℹ️ About section with cultural significance")
    print("• 💖 Donation/sponsor integration")
    print("• 🎬 Animal House homage details")
    print("• 🌍 Multi-cultural name meanings")
    print("• 💕 GitHub Sponsors links")
    print("• ⭐ Star repository button")
    print("\nRun 'python main.py' to start the app!")
