#!/usr/bin/env python3
"""
Setup script for Thai PromptPay API Python Library
"""

from setuptools import setup, find_packages

# Read README file
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = """
Thai PromptPay API - Python Library

A Python library for generating Thai PromptPay QR code payloads.
Supports phone numbers, tax IDs, and e-Wallet IDs with optional amounts.
"""

setup(
    name='thai-promptpay-api',
    version='1.0.0',
    author='Axiom',
    author_email='axiom@example.com',
    description='Thai PromptPay API for generating QR code payloads',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/axiom/thai-promptpay-api',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Point-Of-Sale',
        'Topic :: Utilities',
    ],
    keywords='promptpay qr code thailand payment thai',
    python_requires='>=3.7',
    install_requires=[
        # No external dependencies - pure Python
    ],
    extras_require={
        'qr': ['qrcode[pil]>=7.0.0'],
        'dev': ['pytest>=6.0.0', 'black>=21.0.0', 'flake8>=3.9.0'],
        'docs': ['sphinx>=4.0.0', 'sphinx-rtd-theme>=1.0.0'],
    },
    entry_points={
        'console_scripts': [
            'promptpay-cli=promptpay_api.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        'Bug Reports': 'https://github.com/axiom/thai-promptpay-api/issues',
        'Source': 'https://github.com/axiom/thai-promptpay-api',
        'Documentation': 'https://thai-promptpay-api.readthedocs.io',
    },
)