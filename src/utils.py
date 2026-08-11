# ForraCorp VoiceForge - Personal Voice Model Training Studio
# Version: 1.0.0

import sys
import re
import json
import logging
import platform
from pathlib import Path
from typing import Dict, Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('VoiceForge')


class SystemInfo:
    @staticmethod
    def get_os() -> str:
        system = platform.system().lower()
        if system == 'darwin':
            return 'macos'
        return system

    @staticmethod
    def get_architecture() -> str:
        return platform.machine()

    @staticmethod
    def get_python_version() -> str:
        return sys.version


class FileManager:
    @staticmethod
    def ensure_directory(path: Path) -> Path:
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def get_safe_filename(filename: str) -> str:
        filename = re.sub(r'[^\w\s-]', '', filename).strip()
        return re.sub(r'[-\s]+', '_', filename)


class AudioUtils:
    @staticmethod
    def validate_audio_file(filepath: Path) -> bool:
        filepath = Path(filepath)
        valid_extensions = {'.wav', '.mp3', '.flac', '.ogg', '.m4a'}
        return filepath.exists() and filepath.suffix.lower() in valid_extensions


class ConfigManager:
    CONFIG_FILE = Path.home() / '.voiceforge' / 'config.json'

    DEFAULT_CONFIG = {
        "app_name": "VoiceForge",
        "version": "1.0.0",
        "sample_rate": 22050,
        "output_dir": str(Path.home() / 'VoiceForge_Models'),
        "recording_prompts": [
            "Hello, my name is [your name].",
            "The quick brown fox jumps over the lazy dog.",
            "Good morning. How are you today?",
            "I enjoy creating new technologies and learning new things.",
            "The weather is beautiful today, perfect for a walk outside.",
            "Thank you for using VoiceForge to create your personal voice model.",
            "Artificial intelligence is transforming how we interact with computers.",
            "ForraCorp is here to build the system that is \"Resilience in innovation. Precision in design and Durability in service\".",
            "ForraNova, on its part, makes the training of the trainers possible because, \"Knowledge is for the Living!\"",
            "Please read these sentences clearly and at a natural pace.",
            "The future of communication is being shaped by voice technology.",
            "VoiceForge makes it easy to create your own voice model."
        ]
    }

    @classmethod
    def get_config(cls, config_path: Optional[Path] = None) -> Dict[str, Any]:
        target_path = config_path or cls.CONFIG_FILE
        try:
            if target_path.exists():
                with open(target_path, 'r', encoding='utf-8') as f:
                    return {**cls.DEFAULT_CONFIG, **json.load(f)}
        except Exception as e:
            logger.error(f"Error reading config: {e}")
        return cls.DEFAULT_CONFIG