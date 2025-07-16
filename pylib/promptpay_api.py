#!/usr/bin/env python3
"""
Thai PromptPay API - Python Library

A Python library for generating Thai PromptPay QR code payloads
Based on the JavaScript implementation

Author: Axiom
Version: 1.0.0
"""

import re
from typing import Optional, Dict, Any, Union


class PromptPayAPI:
    """Thai PromptPay API for generating and parsing QR code payloads"""
    
    # Constants
    ID_PAYLOAD_FORMAT = '00'
    ID_POI_METHOD = '01'
    ID_MERCHANT_INFORMATION_BOT = '29'
    ID_TRANSACTION_CURRENCY = '53'
    ID_TRANSACTION_AMOUNT = '54'
    ID_COUNTRY_CODE = '58'
    ID_CRC = '63'
    
    PAYLOAD_FORMAT_EMV_QRCPS_MERCHANT_PRESENTED_MODE = '01'
    POI_METHOD_STATIC = '11'
    POI_METHOD_DYNAMIC = '12'
    MERCHANT_INFORMATION_TEMPLATE_ID_GUID = '00'
    BOT_ID_MERCHANT_PHONE_NUMBER = '01'
    BOT_ID_MERCHANT_TAX_ID = '02'
    BOT_ID_MERCHANT_EWALLET_ID = '03'
    GUID_PROMPTPAY = 'A000000677010111'
    TRANSACTION_CURRENCY_THB = '764'
    COUNTRY_CODE_TH = 'TH'
    
    # CRC16 lookup table
    CRC_TABLE = [
        0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
        0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
        0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
        0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
        0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
        0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
        0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
        0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
        0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
        0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
        0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,
        0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
        0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
        0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
        0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
        0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
        0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
        0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
        0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
        0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
        0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
        0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
        0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
        0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
        0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
        0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,
        0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
        0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,
        0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
        0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
        0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
        0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0
    ]
    
    @staticmethod
    def _format_field(field_id: str, value: str) -> str:
        """Format a field with ID, length, and value"""
        length = f"{len(value):02d}"
        return f"{field_id}{length}{value}"
    
    @staticmethod
    def _serialize(fields: list) -> str:
        """Serialize a list of fields into a string"""
        return ''.join(filter(None, fields))
    
    @staticmethod
    def _sanitize_target(target: str) -> str:
        """Remove non-numeric characters from target"""
        return re.sub(r'[^0-9]', '', target)
    
    @staticmethod
    def _format_target(target: str) -> str:
        """Format target for PromptPay payload"""
        sanitized = PromptPayAPI._sanitize_target(target)
        if len(sanitized) >= 13:
            return sanitized
        else:
            # Phone number format: convert to 13 digits with country code
            phone = sanitized.lstrip('0')
            if phone.startswith('66'):
                formatted = phone
            else:
                formatted = '66' + phone
            return f"{'0' * (13 - len(formatted))}{formatted}"
    
    @staticmethod
    def _format_amount(amount: float) -> str:
        """Format amount to 2 decimal places"""
        return f"{amount:.2f}"
    
    @staticmethod
    def _calculate_crc16(data: str) -> int:
        """Calculate CRC16 checksum"""
        crc = 0xFFFF
        for char in data:
            c = ord(char)
            if c > 255:
                raise ValueError("Character out of range")
            j = (c ^ (crc >> 8)) & 0xFF
            crc = PromptPayAPI.CRC_TABLE[j] ^ (crc << 8)
        return crc & 0xFFFF
    
    @staticmethod
    def _format_crc(crc_value: int) -> str:
        """Format CRC value as 4-digit hex string"""
        return f"{crc_value:04X}"
    
    @classmethod
    def generate_payload(cls, target: str, amount: Optional[float] = None) -> str:
        """
        Generate PromptPay QR code payload
        
        Args:
            target: Phone number, Tax ID, or e-Wallet ID
            amount: Optional amount in THB
            
        Returns:
            PromptPay payload string
        """
        sanitized_target = cls._sanitize_target(target)
        
        # Determine target type
        if len(sanitized_target) >= 15:
            target_type = cls.BOT_ID_MERCHANT_EWALLET_ID
        elif len(sanitized_target) >= 13:
            target_type = cls.BOT_ID_MERCHANT_TAX_ID
        else:
            target_type = cls.BOT_ID_MERCHANT_PHONE_NUMBER
        
        # Build payload fields
        fields = [
            cls._format_field(cls.ID_PAYLOAD_FORMAT, cls.PAYLOAD_FORMAT_EMV_QRCPS_MERCHANT_PRESENTED_MODE),
            cls._format_field(cls.ID_POI_METHOD, cls.POI_METHOD_DYNAMIC if amount else cls.POI_METHOD_STATIC),
            cls._format_field(cls.ID_MERCHANT_INFORMATION_BOT, cls._serialize([
                cls._format_field(cls.MERCHANT_INFORMATION_TEMPLATE_ID_GUID, cls.GUID_PROMPTPAY),
                cls._format_field(target_type, cls._format_target(sanitized_target))
            ])),
            cls._format_field(cls.ID_COUNTRY_CODE, cls.COUNTRY_CODE_TH),
            cls._format_field(cls.ID_TRANSACTION_CURRENCY, cls.TRANSACTION_CURRENCY_THB),
        ]
        
        # Add amount if specified
        if amount:
            fields.append(cls._format_field(cls.ID_TRANSACTION_AMOUNT, cls._format_amount(amount)))
        
        # Calculate CRC
        data_to_crc = cls._serialize(fields) + cls.ID_CRC + '04'
        crc = cls._calculate_crc16(data_to_crc)
        fields.append(cls._format_field(cls.ID_CRC, cls._format_crc(crc)))
        
        return cls._serialize(fields)
    
    @classmethod
    def generate_from_phone_number(cls, phone_number: str, amount: Optional[float] = None) -> str:
        """
        Generate PromptPay QR code payload for phone number
        
        Args:
            phone_number: Thai phone number
            amount: Optional amount in THB
            
        Returns:
            PromptPay payload string
        """
        return cls.generate_payload(phone_number, amount)
    
    @classmethod
    def generate_from_tax_id(cls, tax_id: str, amount: Optional[float] = None) -> str:
        """
        Generate PromptPay QR code payload for Tax ID
        
        Args:
            tax_id: Thai Tax ID (13 digits)
            amount: Optional amount in THB
            
        Returns:
            PromptPay payload string
        """
        return cls.generate_payload(tax_id, amount)
    
    @classmethod
    def generate_from_ewallet_id(cls, ewallet_id: str, amount: Optional[float] = None) -> str:
        """
        Generate PromptPay QR code payload for e-Wallet ID
        
        Args:
            ewallet_id: e-Wallet ID (15+ digits)
            amount: Optional amount in THB
            
        Returns:
            PromptPay payload string
        """
        return cls.generate_payload(ewallet_id, amount)
    
    @classmethod
    def validate_target(cls, target: str) -> Dict[str, Any]:
        """
        Validate target format
        
        Args:
            target: Phone number, Tax ID, or e-Wallet ID
            
        Returns:
            Dict with validation result
        """
        sanitized = cls._sanitize_target(target)
        
        if len(sanitized) >= 15:
            return {'is_valid': True, 'type': 'ewallet'}
        elif len(sanitized) >= 13:
            return {'is_valid': True, 'type': 'taxid'}
        elif len(sanitized) >= 9:
            return {'is_valid': True, 'type': 'phone'}
        else:
            return {'is_valid': False, 'type': 'unknown'}
    
    @classmethod
    def _parse_field(cls, payload: str, position: int) -> Optional[Dict[str, Any]]:
        """Parse a field from payload at given position"""
        if position >= len(payload):
            return None
        
        try:
            field_id = payload[position:position + 2]
            length = int(payload[position + 2:position + 4])
            value = payload[position + 4:position + 4 + length]
            
            return {
                'id': field_id,
                'length': length,
                'value': value,
                'next_position': position + 4 + length
            }
        except (ValueError, IndexError):
            return None
    
    @classmethod
    def _parse_sub_fields(cls, data: str) -> Dict[str, str]:
        """Parse sub-fields from data"""
        sub_fields = {}
        position = 0
        
        while position < len(data):
            field = cls._parse_field(data, position)
            if not field:
                break
            
            sub_fields[field['id']] = field['value']
            position = field['next_position']
        
        return sub_fields
    
    @classmethod
    def _reverse_format_target(cls, formatted_target: str, target_type: str) -> str:
        """Reverse format target back to original format"""
        if target_type == cls.BOT_ID_MERCHANT_PHONE_NUMBER:
            # Remove leading zeros and convert back to phone format
            cleaned = formatted_target.lstrip('0')
            if cleaned.startswith('66'):
                return '0' + cleaned[2:]
            return cleaned
        return formatted_target
    
    @classmethod
    def parse_payload(cls, payload: str) -> Dict[str, Any]:
        """
        Parse PromptPay payload and extract information
        
        Args:
            payload: PromptPay payload string
            
        Returns:
            Dict with parsed information
        """
        try:
            result = {
                'is_valid': False,
                'payload_format': None,
                'poi_method': None,
                'target': None,
                'target_type': None,
                'amount': None,
                'currency': None,
                'country_code': None,
                'crc': None,
                'raw_data': payload
            }
            
            position = 0
            fields = {}
            
            # Parse all fields
            while position < len(payload):
                field = cls._parse_field(payload, position)
                if not field:
                    break
                
                fields[field['id']] = field['value']
                position = field['next_position']
            
            # Extract basic information
            result['payload_format'] = fields.get(cls.ID_PAYLOAD_FORMAT)
            result['poi_method'] = fields.get(cls.ID_POI_METHOD)
            result['currency'] = fields.get(cls.ID_TRANSACTION_CURRENCY)
            result['country_code'] = fields.get(cls.ID_COUNTRY_CODE)
            result['crc'] = fields.get(cls.ID_CRC)
            
            if fields.get(cls.ID_TRANSACTION_AMOUNT):
                try:
                    result['amount'] = float(fields[cls.ID_TRANSACTION_AMOUNT])
                except ValueError:
                    result['amount'] = None
            
            # Parse merchant information
            if fields.get(cls.ID_MERCHANT_INFORMATION_BOT):
                merchant_info = cls._parse_sub_fields(fields[cls.ID_MERCHANT_INFORMATION_BOT])
                
                # Find target information
                target_type_id = None
                target_value = None
                
                if merchant_info.get(cls.BOT_ID_MERCHANT_PHONE_NUMBER):
                    target_type_id = cls.BOT_ID_MERCHANT_PHONE_NUMBER
                    target_value = merchant_info[cls.BOT_ID_MERCHANT_PHONE_NUMBER]
                    result['target_type'] = 'phone'
                elif merchant_info.get(cls.BOT_ID_MERCHANT_TAX_ID):
                    target_type_id = cls.BOT_ID_MERCHANT_TAX_ID
                    target_value = merchant_info[cls.BOT_ID_MERCHANT_TAX_ID]
                    result['target_type'] = 'taxid'
                elif merchant_info.get(cls.BOT_ID_MERCHANT_EWALLET_ID):
                    target_type_id = cls.BOT_ID_MERCHANT_EWALLET_ID
                    target_value = merchant_info[cls.BOT_ID_MERCHANT_EWALLET_ID]
                    result['target_type'] = 'ewallet'
                
                if target_value:
                    result['target'] = cls._reverse_format_target(target_value, target_type_id)
            
            # Validate basic structure
            result['is_valid'] = bool(
                result['payload_format'] and 
                result['poi_method'] and 
                result['target'] and 
                result['crc']
            )
            
            return result
            
        except Exception as e:
            return {
                'is_valid': False,
                'error': str(e),
                'raw_data': payload
            }
    
    @classmethod
    def decode_payload(cls, payload: str) -> Dict[str, Any]:
        """
        Decode PromptPay payload to readable information
        
        Args:
            payload: PromptPay payload string
            
        Returns:
            Dict with decoded information
        """
        parsed = cls.parse_payload(payload)
        
        if not parsed['is_valid']:
            return {
                'success': False,
                'error': parsed.get('error', 'Invalid payload format'),
                'original_payload': payload
            }
        
        type_text = {
            'phone': 'เบอร์โทรศัพท์',
            'taxid': 'เลขประจำตัวผู้เสียภาษี',
            'ewallet': 'e-Wallet ID'
        }
        
        return {
            'success': True,
            'target': parsed['target'],
            'target_type': parsed['target_type'],
            'target_type_text': type_text.get(parsed['target_type'], parsed['target_type']),
            'amount': parsed['amount'],
            'currency': parsed['currency'],
            'country_code': parsed['country_code'],
            'is_static': parsed['poi_method'] == cls.POI_METHOD_STATIC,
            'is_dynamic': parsed['poi_method'] == cls.POI_METHOD_DYNAMIC,
            'original_payload': payload
        }
    
    @classmethod
    def payload_to_readable(cls, payload: str) -> str:
        """
        Convert payload to human-readable format
        
        Args:
            payload: PromptPay payload string
            
        Returns:
            Human-readable string
        """
        decoded = cls.decode_payload(payload)
        
        if not decoded['success']:
            return f"Invalid payload: {decoded['error']}"
        
        result = []
        result.append("PromptPay QR Code Information:")
        result.append(f"- Target: {decoded['target']} ({decoded['target_type_text']})")
        
        if decoded['amount']:
            result.append(f"- Amount: {decoded['amount']} THB")
            result.append("- Type: Dynamic QR (จำนวนเงินคงที่)")
        else:
            result.append("- Amount: Not specified")
            result.append("- Type: Static QR (ผู้ใช้ป้อนจำนวนเงินเอง)")
        
        result.append(f"- Country: {decoded['country_code']}")
        result.append(f"- Currency: {decoded['currency']}")
        
        return '\n'.join(result)


# Convenience functions for backward compatibility
def generate_payload(target: str, amount: Optional[float] = None) -> str:
    """Generate PromptPay QR code payload"""
    return PromptPayAPI.generate_payload(target, amount)


def generate_from_phone_number(phone_number: str, amount: Optional[float] = None) -> str:
    """Generate PromptPay QR code payload for phone number"""
    return PromptPayAPI.generate_from_phone_number(phone_number, amount)


def generate_from_tax_id(tax_id: str, amount: Optional[float] = None) -> str:
    """Generate PromptPay QR code payload for Tax ID"""
    return PromptPayAPI.generate_from_tax_id(tax_id, amount)


def generate_from_ewallet_id(ewallet_id: str, amount: Optional[float] = None) -> str:
    """Generate PromptPay QR code payload for e-Wallet ID"""
    return PromptPayAPI.generate_from_ewallet_id(ewallet_id, amount)


def validate_target(target: str) -> Dict[str, Any]:
    """Validate target format"""
    return PromptPayAPI.validate_target(target)


def parse_payload(payload: str) -> Dict[str, Any]:
    """Parse PromptPay payload"""
    return PromptPayAPI.parse_payload(payload)


def decode_payload(payload: str) -> Dict[str, Any]:
    """Decode PromptPay payload"""
    return PromptPayAPI.decode_payload(payload)


def payload_to_readable(payload: str) -> str:
    """Convert payload to readable format"""
    return PromptPayAPI.payload_to_readable(payload)