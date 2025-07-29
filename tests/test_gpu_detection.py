#!/usr/bin/env python3
"""
Test script to demonstrate GPU detection with and without optional dependencies
"""

import sys
from pathlib import Path

# Add parent directory to path to find main modules
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_basic_detection():
    """Test basic GPU detection (always available)"""
    print("=" * 60)
    print("TESTING BASIC GPU DETECTION (No optional dependencies)")
    print("=" * 60)

    try:
        from gpu_info import get_gpu_info, check_gpu_dependencies

        # Check what's available
        deps = check_gpu_dependencies()
        print(f"Dependencies available: {deps}")
        print()

        # Get GPU info
        gpu_info = get_gpu_info()
        print(f"GPU Summary: {gpu_info.get_summary()}")
        print()

        # Show recommendations
        recommendations = gpu_info.get_ai_recommendations()
        print(f"Performance Tier: {recommendations['performance_tier']}")
        print("Suitable Models:")
        for model in recommendations["suitable_models"][:3]:  # Show first 3
            print(f"  • {model}")

        if recommendations["limitations"]:
            print("Limitations:")
            for limitation in recommendations["limitations"][:2]:  # Show first 2
                print(f"  • {limitation}")

        print("\n✅ Basic detection working correctly!")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    return True


def test_enhanced_detection():
    """Test enhanced GPU detection (requires optional dependencies)"""
    print("\n" + "=" * 60)
    print("TESTING ENHANCED GPU DETECTION (With optional dependencies)")
    print("=" * 60)

    try:
        # Try to import the enhanced dependencies
        import GPUtil
        import psutil

        print("✅ Enhanced dependencies available!")

        from gpu_info import get_gpu_info, format_gpu_info_for_display

        gpu_info = get_gpu_info()
        print("Enhanced GPU information:")
        print(gpu_info.get_summary())

        return True

    except ImportError as e:
        print(f"⚠️ Enhanced dependencies not available: {e}")
        print("Run: pip install -r requirements-gpu.txt")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("ShamaOllama GPU Detection Test")
    print("Testing the plugin-like architecture for optional dependencies")

    # Test basic functionality (should always work)
    basic_works = test_basic_detection()

    # Test enhanced functionality (works only if dependencies installed)
    enhanced_works = test_enhanced_detection()

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Basic Detection:    {'✅ Working' if basic_works else '❌ Failed'}")
    print(
        f"Enhanced Detection: {'✅ Working' if enhanced_works else '⚠️ Dependencies needed'}"
    )

    if basic_works and not enhanced_works:
        print(
            "\n💡 Recommendation: Install optional dependencies for enhanced features:"
        )
        print("   pip install -r requirements-gpu.txt")
        print("   Or run: install-gpu-support.bat (Windows)")

    print(
        "\nThis demonstrates how ShamaOllama gracefully handles optional dependencies!"
    )


if __name__ == "__main__":
    main()
