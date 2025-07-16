#!/usr/bin/env python3
"""
Simple QR code generation test using Python PromptPay API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from promptpay_api import PromptPayAPI

def main():
    print("Testing QR Code Generation with Python PromptPay API")
    print("=" * 55)
    
    # Test cases
    test_cases = [
        ("0812345678", None, "Phone number (Static QR)"),
        ("0812345678", 100.50, "Phone number with amount"),
        ("1234567890123", 50.00, "Tax ID with amount"),
    ]
    
    for target, amount, description in test_cases:
        print(f"\n{description}:")
        print(f"Target: {target}")
        print(f"Amount: {amount if amount else 'Not specified'}")
        
        # Generate payload
        payload = PromptPayAPI.generate_payload(target, amount)
        print(f"Payload: {payload}")
        print(f"Payload length: {len(payload)} characters")
        
        # Validate by decoding
        decoded = PromptPayAPI.decode_payload(payload)
        if decoded['success']:
            print(f"[OK] Payload valid - Target: {decoded['target']}, Amount: {decoded['amount']}")
        else:
            print(f"[ERROR] Payload invalid: {decoded['error']}")
        
        # Test with QR code library
        try:
            import qrcode
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(payload)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            filename = f"qr_{target}_{amount or 'static'}.png"
            img.save(filename)
            print(f"[OK] QR code image saved as '{filename}'")
            
        except ImportError:
            print("[INFO] qrcode library not installed")
        except Exception as e:
            print(f"[ERROR] QR generation error: {e}")
    
    print(f"\n{'='*55}")
    print("Test completed!")
    print("You can scan the generated QR code images with your banking app!")

if __name__ == '__main__':
    main()