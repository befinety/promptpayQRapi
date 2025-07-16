#!/usr/bin/env python3
"""
Test script for Thai PromptPay API Python Library
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from promptpay_api import PromptPayAPI


def test_basic_functionality():
    """Test basic functionality of the PromptPay API"""
    print("=== Testing Basic Functionality ===")
    
    # Test phone number without amount
    payload1 = PromptPayAPI.generate_from_phone_number('0812345678')
    print(f"Phone (no amount): {payload1}")
    
    # Test phone number with amount
    payload2 = PromptPayAPI.generate_from_phone_number('0812345678', 100.00)
    print(f"Phone (with amount): {payload2}")
    
    # Test tax ID
    payload3 = PromptPayAPI.generate_from_tax_id('1234567890123', 50.00)
    print(f"Tax ID: {payload3}")
    
    # Test e-Wallet ID
    payload4 = PromptPayAPI.generate_from_ewallet_id('123456789012345', 25.50)
    print(f"e-Wallet: {payload4}")
    
    print()


def test_validation():
    """Test target validation"""
    print("=== Testing Validation ===")
    
    test_cases = [
        ('0812345678', 'phone'),
        ('1234567890123', 'taxid'),
        ('123456789012345', 'ewallet'),
        ('123', 'unknown'),
        ('', 'unknown')
    ]
    
    for target, expected_type in test_cases:
        result = PromptPayAPI.validate_target(target)
        status = "PASS" if result['type'] == expected_type else "FAIL"
        print(f"{status} Target: '{target}' -> Type: {result['type']}, Valid: {result['is_valid']}")
    
    print()


def test_payload_conversion():
    """Test payload parsing and decoding"""
    print("=== Testing Payload Conversion ===")
    
    # Test round-trip conversion
    test_cases = [
        ('0812345678', None),
        ('0812345678', 100.50),
        ('1234567890123', 50.00),
        ('66812345678', 25.75)
    ]
    
    for target, amount in test_cases:
        print(f"\nTesting: {target} {'(no amount)' if amount is None else f'({amount} THB)'}")
        
        # Generate payload
        payload = PromptPayAPI.generate_payload(target, amount)
        print(f"Generated payload: {payload}")
        
        # Parse payload
        parsed = PromptPayAPI.parse_payload(payload)
        if parsed['is_valid']:
            print(f"Parsed - Target: {parsed['target']}, Type: {parsed['target_type']}, Amount: {parsed['amount']}")
        else:
            print(f"Parse failed: {parsed.get('error', 'Unknown error')}")
        
        # Decode payload
        decoded = PromptPayAPI.decode_payload(payload)
        if decoded['success']:
            print(f"Decoded - Target: {decoded['target']}, Type: {decoded['target_type_text']}")
            print(f"Amount: {decoded['amount']}, Static: {decoded['is_static']}")
        else:
            print(f"Decode failed: {decoded['error']}")
        
        # Test readable format
        readable = PromptPayAPI.payload_to_readable(payload)
        print(f"Readable format:")
        for line in readable.split('\n'):
            print(f"  {line}")


def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n=== Testing Edge Cases ===")
    
    # Test invalid payloads
    invalid_payloads = [
        '',
        '123',
        'invalid_payload',
        '00020101011102160016A000000677010111013006681234567890580258764063'  # incomplete
    ]
    
    for payload in invalid_payloads:
        decoded = PromptPayAPI.decode_payload(payload)
        status = "PASS" if not decoded['success'] else "FAIL"
        print(f"{status} Invalid payload handled: '{payload[:20]}...'")
    
    # Test invalid amounts
    try:
        PromptPayAPI.generate_payload('0812345678', -100)
        print("FAIL: Negative amount should be handled")
    except Exception as e:
        print(f"PASS: Negative amount handled: {str(e)}")
    
    print()


def test_compatibility():
    """Test compatibility with JavaScript version"""
    print("=== Testing JavaScript Compatibility ===")
    
    # Known payloads from JavaScript version
    test_payloads = [
        # Phone number without amount
        ('0812345678', None, '00020101011102160016A00000067701011101300066812345678058027653037640630445C4'),
        
        # Phone number with amount
        ('0812345678', 100.00, '00020101021102160016A00000067701011101300066812345678058027653037645406100.006304'),
    ]
    
    for target, amount, expected_start in test_payloads:
        payload = PromptPayAPI.generate_payload(target, amount)
        # Check if payload starts with expected pattern (without CRC)
        if payload.startswith(expected_start[:70]):  # Check first 70 chars
            print(f"PASS: {target} {'(no amount)' if amount is None else f'({amount} THB)'}")
        else:
            print(f"FAIL: {target} {'(no amount)' if amount is None else f'({amount} THB)'}")
            print(f"  Expected: {expected_start[:70]}...")
            print(f"  Got:      {payload[:70]}...")


def main():
    """Run all tests"""
    print("Thai PromptPay API Python Library - Test Suite")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_validation()
        test_payload_conversion()
        test_edge_cases()
        test_compatibility()
        
        print("All tests completed!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()