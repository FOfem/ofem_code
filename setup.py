"""
Setup script for VoiceForge application.
"""

from setuptools import setup, find_packages
import sys
import os

__version__ = "1.0.0"

# Read requirements
requirements = [
    "torch>=2.0.0",
    "sounddevice>=0.4.0",
    "soundfile>=0.10.0",
    "numpy>=1.21.0",
    "scipy>=1.7.0",
    "TTS>=0.14.0",
    "pyyaml>=6.0",
    "requests>=2.28.0"
]

setup(
    name='voiceforge',
    version=__version__,
    description='Personal Voice Model Training Studio',
    author='F.Ofem',
    author_email='fofem@forracorp.com',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.9,<3.12',
    entry_points={
        'console_scripts': [
            'voiceforge=src.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)