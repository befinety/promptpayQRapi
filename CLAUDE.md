# Thai PromptPay QR API - Project Documentation

## Project Overview
This project provides a comprehensive Thai PromptPay QR code generation API in both JavaScript and Python, capable of creating scannable QR codes for Thai banking applications.

## Project Structure

```
promptpayQRapi/
├── CLAUDE.md                           # This documentation
├── js/
│   └── promptpay.js                   # Original PromptPay implementation
├── jsmodule/
│   ├── thaipromptpayapi.js           # JavaScript UMD module
│   ├── qr_final.html                 # QR code generator web interface
│   ├── payload_converter.html        # Payload conversion tool
│   └── howtoqrapi.md                 # JavaScript documentation
└── pylib/
    ├── __init__.py                   # Python package init
    ├── promptpay_api.py              # Python API class
    ├── setup.py                      # Package setup
    ├── test.py                       # Simple test
    ├── test_promptpay.py             # Comprehensive test suite
    ├── test_qr_simple.py             # QR generation test
    ├── howtoqrpromtPython.md         # Python documentation
    └── Generated QR images (*.png)
```

## Key Features

### ✅ JavaScript Implementation
- **UMD Module**: Compatible with browsers, Node.js, and AMD
- **Payload Generation**: Phone numbers, Tax IDs, e-Wallet IDs
- **Bidirectional Conversion**: Encode and decode payloads
- **QR Code Generation**: Working HTML interface with proper QR library
- **Validation**: Target format validation
- **Static/Dynamic QR**: Support for both payment types

### ✅ Python Implementation
- **Class-based API**: Clean, object-oriented design
- **Type Hints**: Full typing support for Python 3.7+
- **QR Image Generation**: PNG file output with qrcode library
- **Comprehensive Testing**: Multiple test files covering all functionality
- **Package Structure**: Proper Python package with setup.py
- **Documentation**: Complete API reference and examples

## Supported Targets

### 📱 Phone Numbers
- Format: `0812345678` or `66812345678`
- Auto-converts to 13-digit format with country code
- Example: `0812345678` → `0066812345678`

### 🏢 Tax IDs
- Format: 13-digit Thai Tax ID
- Example: `1234567890123`

### 💳 e-Wallet IDs
- Format: 15+ digit e-Wallet ID
- Example: `123456789012345`

## Usage Examples

### JavaScript
```javascript
// Generate static QR (no amount)
const payload = ThaiPromptPayAPI.generatePayload('0812345678');

// Generate dynamic QR (with amount)
const payload = ThaiPromptPayAPI.generatePayload('0812345678', 100.50);

// Decode payload
const decoded = ThaiPromptPayAPI.decodePayload(payload);
```

### Python
```python
from promptpay_api import PromptPayAPI

# Generate static QR
payload = PromptPayAPI.generate_payload('0812345678')

# Generate dynamic QR
payload = PromptPayAPI.generate_payload('0812345678', 100.50)

# Generate QR code image
import qrcode
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(payload)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("promptpay_qr.png")
```

## Testing

### JavaScript Testing
- **Web Interface**: `jsmodule/qr_final.html`
- **Payload Converter**: `jsmodule/payload_converter.html`
- **Manual Testing**: Open HTML files in browser

### Python Testing
```bash
cd pylib

# Basic functionality test
python test.py

# Comprehensive test suite
python test_promptpay.py

# QR code generation test
python test_qr_simple.py
```

## Development History

### Phase 1: JavaScript Implementation
1. **Base Implementation**: Analyzed existing `promptpay.js`
2. **UMD Module**: Created `thaipromptpayapi.js` with enhanced API
3. **QR Generation**: Fixed QR code generation using proper library
4. **Payload Conversion**: Added bidirectional payload conversion
5. **Web Interface**: Created working HTML test interfaces

### Phase 2: Python Implementation
1. **Port to Python**: Converted JavaScript logic to Python class
2. **Enhanced API**: Added type hints and proper error handling
3. **Package Structure**: Created proper Python package
4. **QR Integration**: Added QR code image generation
5. **Comprehensive Testing**: Created full test suite
6. **Documentation**: Complete API documentation

## Technical Specifications

### PromptPay Payload Format
- **Standard**: EMV QR Code Specification
- **Currency**: Thai Baht (THB) - Code 764
- **Country**: Thailand (TH)
- **CRC**: CRC16 checksum validation
- **Encoding**: UTF-8 compatible

### QR Code Generation
- **JavaScript**: Uses `qrcode-generator` library from CDN
- **Python**: Uses `qrcode[pil]` library
- **Format**: PNG images with customizable size and border
- **Compatibility**: Scannable by all Thai banking apps

## Commands for Development

### JavaScript Development
```bash
# Test in browser
open jsmodule/qr_final.html

# Test payload conversion
open jsmodule/payload_converter.html
```

### Python Development
```bash
# Install package for development
cd pylib
pip install -e .

# Install QR code support
pip install qrcode[pil]

# Run tests
python test_qr_simple.py
```

## Common Issues and Solutions

### JavaScript
- **QR Code not scannable**: Ensure using proper QR library, not custom patterns
- **Library loading**: Use CDN-hosted qrcode-generator library
- **Unicode display**: Thai text may display incorrectly in some browsers

### Python
- **Console encoding**: Thai text may show as garbled in Windows console
- **QR library**: Install `qrcode[pil]` for image generation
- **Path issues**: Use absolute paths for file operations

## Banking App Compatibility

### ✅ Tested Compatible
- Thai banking apps (KBank, SCB, BBL, etc.)
- PromptPay standard compliance
- EMV QR Code specification
- Static and Dynamic QR codes

### QR Code Types
- **Static QR**: No amount specified, user enters amount
- **Dynamic QR**: Fixed amount embedded in QR code

## License
MIT License

## Maintenance Notes

### For Future Updates
- Keep CRC16 lookup table synchronized between JS and Python
- Maintain EMV QR Code standard compliance
- Update QR library versions as needed
- Test with latest banking app versions

### Code Quality
- Both implementations follow their respective language conventions
- Comprehensive error handling and validation
- Full test coverage for critical functionality
- Clear documentation and examples

---

**Project Status**: ✅ Complete and functional
**Last Updated**: Python library implementation completed
**Next Steps**: Optional CLI interface or web API server