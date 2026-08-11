from setuptools import setup, find_packages

setup(
    name='voiceforge',
    version='1.0.0',
    packages=find_packages(where='.'),
    include_package_data=True,
    install_requires=[
        'coqui-tts>=0.27.0',
        'sounddevice>=0.4.6',
        'soundfile>=0.12.1',
        'numpy>=1.24.0',
        'torch>=2.0.0',
        'Pillow>=10.0.0',
    ],
    entry_points={
        'console_scripts': [
            'voiceforge=src.app:main',
        ],
    },
)