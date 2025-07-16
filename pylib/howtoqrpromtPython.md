# Thai PromptPay API - Python Library Documentation

## Overview
ไลบรารี Python สำหรับสร้าง QR Code PromptPay ที่สามารถใช้งานได้จริงกับแอปธนาคารไทย

## Installation
```bash
# Install the library
pip install -e .

# Install with QR code generation support
pip install qrcode[pil]
```

## Basic Usage

### 1. Import Library
```python
from promptpay_api import PromptPayAPI
```

### 2. Generate PromptPay Payload

#### Phone Number (Static QR - ไม่ระบุจำนวน)
```python
payload = PromptPayAPI.generate_from_phone_number('0812345678')
print(payload)
# Output: 00020101021129370016A000000677010111011300668123456785802TH530376463045D82
```

#### Phone Number with Amount (Dynamic QR - ระบุจำนวน)
```python
payload = PromptPayAPI.generate_from_phone_number('0812345678', 100.50)
print(payload)
# Output: 00020101021229370016A000000677010111011300668123456785802TH53037645406100.506304F88B
```

#### Tax ID (เลขประจำตัวผู้เสียภาษี)
```python
payload = PromptPayAPI.generate_from_tax_id('1234567890123', 50.00)
print(payload)
# Output: 00020101021229370016A000000677010111021312345678901235802TH5303764540550.006304BD2C
```

#### e-Wallet ID
```python
payload = PromptPayAPI.generate_from_ewallet_id('123456789012345', 25.75)
print(payload)
# Output: 00020101021229390016A00000067701011103151234567890123455802TH5303764540525.756304A33F
```

### 3. Generate QR Code Image

```python
import qrcode
from promptpay_api import PromptPayAPI

# Generate payload
payload = PromptPayAPI.generate_payload('0812345678', 100.00)

# Create QR code
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(payload)
qr.make(fit=True)

# Save as image
img = qr.make_image(fill_color="black", back_color="white")
img.save("promptpay_qr.png")
```

### 4. Validate Target

```python
# Validate phone number
validation = PromptPayAPI.validate_target('0812345678')
print(validation)
# Output: {'is_valid': True, 'type': 'phone'}

# Validate tax ID
validation = PromptPayAPI.validate_target('1234567890123')
print(validation)
# Output: {'is_valid': True, 'type': 'taxid'}

# Validate e-Wallet ID
validation = PromptPayAPI.validate_target('123456789012345')
print(validation)
# Output: {'is_valid': True, 'type': 'ewallet'}
```

### 5. Parse and Decode Payload

```python
# Parse payload
parsed = PromptPayAPI.parse_payload(payload)
print(f"Target: {parsed['target']}")
print(f"Amount: {parsed['amount']}")
print(f"Type: {parsed['target_type']}")

# Decode payload to readable format
decoded = PromptPayAPI.decode_payload(payload)
if decoded['success']:
    print(f"Target: {decoded['target']}")
    print(f"Amount: {decoded['amount']} THB")
    print(f"Type: {'Static' if decoded['is_static'] else 'Dynamic'}")
```

### 6. Convert to Human-Readable Format

```python
readable = PromptPayAPI.payload_to_readable(payload)
print(readable)
```

Output:
```
PromptPay QR Code Information:
- Target: 0812345678 (เบอร์โทรศัพท์)
- Amount: 100.0 THB
- Type: Dynamic QR (จำนวนเงินคงที่)
- Country: TH
- Currency: 764
```

## Complete Example

```python
from promptpay_api import PromptPayAPI
import qrcode

def create_promptpay_qr(target, amount=None):
    """Create PromptPay QR code"""
    
    # Validate target
    validation = PromptPayAPI.validate_target(target)
    if not validation['is_valid']:
        print(f"Invalid target: {target}")
        return None
    
    # Generate payload
    payload = PromptPayAPI.generate_payload(target, amount)
    print(f"Generated payload: {payload}")
    
    # Create QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(payload)
    qr.make(fit=True)
    
    # Save as image
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"promptpay_{target}_{amount or 'static'}.png"
    img.save(filename)
    
    print(f"QR code saved as: {filename}")
    
    # Show readable info
    readable = PromptPayAPI.payload_to_readable(payload)
    print(f"\\nQR Code Information:\\n{readable}")
    
    return payload

# Usage examples
if __name__ == '__main__':
    # Static QR (no amount)
    create_promptpay_qr('0812345678')
    
    # Dynamic QR (with amount)
    create_promptpay_qr('0812345678', 100.50)
    
    # Tax ID
    create_promptpay_qr('1234567890123', 50.00)
```

## API Reference

### Class: PromptPayAPI

#### Methods

##### `generate_payload(target, amount=None)`
- **Parameters:**
  - `target` (str): Phone number, Tax ID, or e-Wallet ID
  - `amount` (float, optional): Amount in THB
- **Returns:** PromptPay payload string

##### `generate_from_phone_number(phone_number, amount=None)`
- **Parameters:**
  - `phone_number` (str): Thai phone number
  - `amount` (float, optional): Amount in THB
- **Returns:** PromptPay payload string

##### `generate_from_tax_id(tax_id, amount=None)`
- **Parameters:**
  - `tax_id` (str): Thai Tax ID (13 digits)
  - `amount` (float, optional): Amount in THB
- **Returns:** PromptPay payload string

##### `generate_from_ewallet_id(ewallet_id, amount=None)`
- **Parameters:**
  - `ewallet_id` (str): e-Wallet ID (15+ digits)
  - `amount` (float, optional): Amount in THB
- **Returns:** PromptPay payload string

##### `validate_target(target)`
- **Parameters:**
  - `target` (str): Phone number, Tax ID, or e-Wallet ID
- **Returns:** Dict with validation result

##### `parse_payload(payload)`
- **Parameters:**
  - `payload` (str): PromptPay payload string
- **Returns:** Dict with parsed information

##### `decode_payload(payload)`
- **Parameters:**
  - `payload` (str): PromptPay payload string
- **Returns:** Dict with decoded information

##### `payload_to_readable(payload)`
- **Parameters:**
  - `payload` (str): PromptPay payload string
- **Returns:** Human-readable string

## Testing

### Run Basic Tests
```bash
python test.py
```

### Run Comprehensive Tests
```bash
python test_promptpay.py
```

### Test QR Code Generation
```bash
python test_qr_simple.py
```

## File Structure
```
pylib/
├── __init__.py              # Package initialization
├── promptpay_api.py         # Main API class
├── setup.py                 # Package setup
├── test.py                  # Simple test
├── test_promptpay.py        # Comprehensive test
├── test_qr_simple.py        # QR generation test
└── howtoqrpromtPython.md    # This documentation
```

## Features

### ✅ Supported Features
- Phone number payload generation
- Tax ID payload generation  
- e-Wallet ID payload generation
- Static QR (no amount specified)
- Dynamic QR (with amount)
- Payload validation and parsing
- Bidirectional conversion (encode/decode)
- QR code image generation
- Human-readable format conversion

### 📱 Compatible with
- Thai banking apps (KBank, SCB, BBL, etc.)
- PromptPay standard
- EMV QR Code specification
- Any QR code scanner

### 🔒 Security
- Pure Python implementation
- No external dependencies for core functionality
- CRC16 checksum validation
- Input sanitization

## Dependencies

### Core (no dependencies)
- Pure Python 3.7+

### Optional (for QR code generation)
- `qrcode[pil]` - QR code image generation
- `Pillow` - Image processing

## License
MIT License

## Author
Axiom

---

**Note:** This library generates valid PromptPay payloads that comply with the official Thai PromptPay standard and can be scanned by all Thai banking applications.