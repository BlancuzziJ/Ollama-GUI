#!/usr/bin/env python3
"""
Quick test for the security fix
"""

from security import security

# Test messages that were previously blocked
test_messages = [
    'I don\'t have a personal name, but I am referred to as "Assistant." How can I help you today?',
    'Nice to meet you, John! I\'d be happy to help you with that.',
    'Here are the definitions of your name "John"',
    'What\'s the weather like today?',
    'Can you help me with <topic>?',
    '<script>alert("hack")</script>',  # This should still be blocked
]

print("🔒 Testing Security Validation Fix")
print("=" * 50)

for i, msg in enumerate(test_messages, 1):
    result = security.validate_message_input(msg)
    status = "✅ PASS" if result else "❌ BLOCK"
    print(f"{i}. {status} - {msg[:50]}{'...' if len(msg) > 50 else ''}")

print("\nExpected results:")
print("- Messages 1-5 should PASS (normal conversation)")
print("- Message 6 should be BLOCKED (actual security threat)")
