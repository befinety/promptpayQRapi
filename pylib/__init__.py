"""
Thai PromptPay API - Python Library

A Python library for generating Thai PromptPay QR code payloads

Usage:
    from promptpay_api import PromptPayAPI
    
    # Generate QR code payload
    payload = PromptPayAPI.generate_payload('0812345678', 100.00)
    
    # Decode payload
    decoded = PromptPayAPI.decode_payload(payload)
    
    # Validate target
    validation = PromptPayAPI.validate_target('0812345678')
"""

from .promptpay_api import (
    PromptPayAPI,
    generate_payload,
    generate_from_phone_number,
    generate_from_tax_id,
    generate_from_ewallet_id,
    validate_target,
    parse_payload,
    decode_payload,
    payload_to_readable
)

__version__ = "1.0.0"
__author__ = "Axiom"
__email__ = "axiom@example.com"
__description__ = "Thai PromptPay API for generating QR code payloads"

__all__ = [
    'PromptPayAPI',
    'generate_payload',
    'generate_from_phone_number',
    'generate_from_tax_id',
    'generate_from_ewallet_id',
    'validate_target',
    'parse_payload',
    'decode_payload',
    'payload_to_readable'
]