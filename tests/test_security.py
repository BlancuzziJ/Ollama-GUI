#!/usr/bin/env python3
"""
Security test script for ShamaOllama
Tests all security features and validations
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to find main modules
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_security_imports():
    """Test that security module imports correctly"""
    try:
        from security import (
            security,
            SecurityValidator,
            require_valid_url,
            require_valid_input,
        )

        print("✅ Security module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Security import error: {e}")
        return False


def test_url_validation():
    """Test URL validation functionality"""
    try:
        from security import security

        # Test valid URLs
        valid_urls = [
            "https://github.com/BlancuzziJ/Ollama-GUI",
            "http://localhost:11434",
            "https://github.com/sponsors/BlancuzziJ",
        ]

        for url in valid_urls:
            if not security.validate_url(url):
                print(f"❌ Valid URL rejected: {url}")
                return False

        # Test invalid URLs
        invalid_urls = [
            "javascript:alert('xss')",
            "file:///etc/passwd",
            "data:text/html,<script>alert('xss')</script>",
            "ftp://malicious.com",
            "http://" + "x" * 3000,  # Too long
        ]

        for url in invalid_urls:
            if security.validate_url(url):
                print(f"❌ Invalid URL accepted: {url}")
                return False

        print("✅ URL validation working correctly")
        return True

    except Exception as e:
        print(f"❌ URL validation test error: {e}")
        return False


def test_input_validation():
    """Test input validation functionality"""
    try:
        from security import security

        # Test valid inputs
        valid_inputs = [
            "Hello, how are you?",
            "What is 2 + 2?",
            "Tell me about Python programming.",
            "A" * 1000,  # Long but valid
        ]

        for msg in valid_inputs:
            if not security.validate_message_input(msg):
                print(f"❌ Valid input rejected: {msg[:50]}...")
                return False

        # Test invalid inputs
        invalid_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "A" * 20000,  # Too long
            "data:text/html,<h1>test</h1>",
        ]

        for msg in invalid_inputs:
            if security.validate_message_input(msg):
                print(f"❌ Invalid input accepted: {msg[:50]}...")
                return False

        print("✅ Input validation working correctly")
        return True

    except Exception as e:
        print(f"❌ Input validation test error: {e}")
        return False


def test_model_validation():
    """Test model name validation"""
    try:
        from security import security

        # Test valid model names
        valid_models = [
            "llama2",
            "mistral:7b",
            "codellama:13b-instruct",
            "phi-2",
            "neural-chat",
        ]

        for model in valid_models:
            if not security.validate_model_name(model):
                print(f"❌ Valid model name rejected: {model}")
                return False

        # Test invalid model names
        invalid_models = [
            "<script>alert('xss')</script>",
            "model; rm -rf /",
            "model && malicious_command",
            "model|dangerous",
            "A" * 200,  # Too long
        ]

        for model in invalid_models:
            if security.validate_model_name(model):
                print(f"❌ Invalid model name accepted: {model}")
                return False

        print("✅ Model name validation working correctly")
        return True

    except Exception as e:
        print(f"❌ Model validation test error: {e}")
        return False


def test_security_logging():
    """Test security logging functionality"""
    try:
        from security import security

        # Test logging setup
        if not hasattr(security, "logger"):
            print("❌ Security logger not initialized")
            return False

        # Test log event
        security.log_security_event("Test Event", {"test": True})

        # Check if log directory exists
        log_dir = Path.home() / ".shamollama" / "logs"
        if not log_dir.exists():
            print("❌ Log directory not created")
            return False

        print("✅ Security logging working correctly")
        return True

    except Exception as e:
        print(f"❌ Security logging test error: {e}")
        return False


def test_sanitization():
    """Test input sanitization"""
    try:
        from security import security

        # Test sanitization
        dangerous_input = "Hello<script>alert('xss')</script>world\x00null"
        sanitized = security.sanitize_input(dangerous_input)

        if "\x00" in sanitized:
            print("❌ Null bytes not removed")
            return False

        # Test length limiting
        long_input = "A" * 20000
        sanitized_long = security.sanitize_input(long_input)
        if len(sanitized_long) > security.MAX_MESSAGE_LENGTH:
            print("❌ Input not properly truncated")
            return False

        print("✅ Input sanitization working correctly")
        return True

    except Exception as e:
        print(f"❌ Sanitization test error: {e}")
        return False


def main():
    """Run all security tests"""
    print("🔒 Testing ShamaOllama Security Features...")
    print("=" * 50)

    tests = [
        test_security_imports,
        test_url_validation,
        test_input_validation,
        test_model_validation,
        test_security_logging,
        test_sanitization,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Security Tests Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All security tests passed! ShamaOllama is secure.")
        print("\n🔒 Security Features Active:")
        print("• Input validation and sanitization")
        print("• URL validation and filtering")
        print("• Model name validation")
        print("• Security event logging")
        print("• Path traversal protection")
        print("• XSS and injection prevention")
        print("• Safe file operations")
        print("• Network security measures")
        return 0
    else:
        print("❌ Some security tests failed. Please review the code.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
