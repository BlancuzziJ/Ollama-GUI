#!/usr/bin/env python3
"""
Run all ShamaOllama tests
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test(test_file):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=False, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ {test_file} - PASSED")
            return True
        else:
            print(f"❌ {test_file} - FAILED")
            return False
    except Exception as e:
        print(f"❌ {test_file} - ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("🎸 ShamaOllama Test Suite")
    print("Paying homage to 'Shama Lama Ding Dong' from Animal House (1978)")
    print("")
    
    # Test files to run
    test_files = [
        'test_thinking_filter.py',
        'test_gpu_detection.py',
        'test_dependencies.py',
        'test_security.py',
        'test_app.py'
    ]
    
    # Track results
    passed = 0
    failed = 0
    
    # Run each test
    for test_file in test_files:
        if os.path.exists(test_file):
            if run_test(test_file):
                passed += 1
            else:
                failed += 1
        else:
            print(f"⚠️ {test_file} not found, skipping...")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📋 Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! ShamaOllama is ready to rock! 🎸")
        return 0
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please review and fix issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
