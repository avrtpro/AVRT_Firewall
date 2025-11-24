#!/usr/bin/env python3
"""
AVRT™ Firewall Setup Configuration
For pip distribution: pip install avrt-firewall

© 2025 Jason I. Proper, BGBH Threads LLC
Licensed under CC BY-NC 4.0
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='avrt-firewall',
    version='1.0.0',
    description='AVRT™ — The Voice Firewall for Safer AI. Ethical middleware using SPIEL™ and THT™ protocols.',
    long_description=read_file('SDK_README.md'),
    long_description_content_type='text/markdown',
    author='Jason I. Proper',
    author_email='info@avrt.pro',
    url='https://avrt.pro',
    project_urls={
        'Source': 'https://github.com/avrtpro/AVRT_Firewall',
        'Documentation': 'https://docs.avrt.pro',
        'Licensing': 'https://buy.stripe.com/8wMaGE3kV0f61jW6oo',
        'Bug Reports': 'https://github.com/avrtpro/AVRT_Firewall/issues',
    },
    license='CC BY-NC 4.0',
    classifiers=[
        # Development Status
        'Development Status :: 4 - Beta',

        # Intended Audience
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',

        # License
        'License :: Other/Proprietary License',

        # Programming Languages
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',

        # Topics
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',

        # Operating Systems
        'Operating System :: OS Independent',

        # Framework
        'Framework :: FastAPI',
    ],
    keywords=[
        'ai-safety',
        'ethical-ai',
        'voice-first',
        'middleware',
        'content-moderation',
        'ai-firewall',
        'spiel',
        'tht',
        'voice-reasoning',
        'llm-safety',
        'ai-ethics',
        'transparency',
        'audit-trail',
    ],
    packages=find_packages(exclude=['tests', 'docs', 'examples']),
    py_modules=['middleware'],
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.28.0',
        'python-dotenv>=1.0.0',
        'stripe>=5.0.0',
        'pydantic>=2.0.0',
        'fastapi>=0.100.0',
        'uvicorn>=0.23.0',
        'sqlalchemy>=2.0.0',
        'psycopg2-binary>=2.9.0',
    ],
    extras_require={
        'voice': [
            'SpeechRecognition>=3.10.0',
            'pydub>=0.25.0',
            'pyaudio>=0.2.13',
        ],
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'docs': [
            'sphinx>=6.0.0',
            'sphinx-rtd-theme>=1.2.0',
        ],
        'all': [
            'SpeechRecognition>=3.10.0',
            'pydub>=0.25.0',
            'pyaudio>=0.2.13',
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
            'sphinx>=6.0.0',
            'sphinx-rtd-theme>=1.2.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'avrt=middleware:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.json', '*.md', 'LICENSE'],
    },
    zip_safe=False,
    platforms='any',
)
