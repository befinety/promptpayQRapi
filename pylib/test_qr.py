#!/usr/bin/env python3
"""
Test QR code generation using Python PromptPay API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from promptpay_api import PromptPayAPI

def test_qr_generation():
    print("Testing QR Code Generation with Python PromptPay API")
    print("=" * 55)
    
    # Test cases
    test_cases = [
        ("0812345678", None, "Phone number (Static QR)"),
        ("0812345678", 100.50, "Phone number with amount"),
        ("1234567890123", 50.00, "Tax ID with amount"),
        ("123456789012345", 25.75, "e-Wallet ID with amount")
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
        
        # Test with QR code library if available
        try:
            import qrcode
            qr = qrcode.QRCode(version=1, box_size=1, border=4)
            qr.add_data(payload)
            qr.make(fit=True)
            print("[OK] QR code generated successfully with qrcode library")
        except ImportError:
            print("[INFO] qrcode library not installed (pip install qrcode[pil])")
        except Exception as e:
            print(f"[ERROR] QR generation error: {e}")

def test_manual_qr():
    print("\n" + "=" * 55)
    print("Manual QR Code Test")
    print("=" * 55)
    
    # Interactive test
    try:
        target = input("Enter phone number or tax ID: ").strip()
        amount_str = input("Enter amount (or press Enter for no amount): ").strip()
        
        amount = float(amount_str) if amount_str else None
        
        # Generate payload
        payload = PromptPayAPI.generate_payload(target, amount)
        
        print(f"\nGenerated payload: {payload}")
        
        # Show readable info
        readable = PromptPayAPI.payload_to_readable(payload)
        print(f"\nReadable format:\n{readable}")
        
        # Try to generate QR code
        try:
            import qrcode
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(payload)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("promptpay_qr.png")
            print(f"\n[OK] QR code image saved as 'promptpay_qr.png'")
            print("You can scan this QR code with your banking app!")
            
        except ImportError:
            print(f"\n[INFO] To generate QR code image, install: pip install qrcode[pil]")
            print("Then you can use the payload with any QR code generator:")
            print(f"Payload: {payload}")
            
    except KeyboardInterrupt:
        print("\nTest cancelled by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_qr_generation()
    
    # Ask user if they want to test manual QR generation
    print("\n" + "=" * 55)
    response = input("Do you want to test manual QR generation? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        test_manual_qr()
    
    print("\nTest completed!")