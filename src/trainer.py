# ForraCorp VoiceForge - Personal Voice Model Training Studio
# Version: 1.0.0

import csv
import shutil
from pathlib import Path
from typing import List, Optional, Callable

from .utils import FileManager, logger


class VoiceTrainer:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir) if output_dir else Path.home() / 'VoiceForge_Models'
        self.is_training = False
        self.progress_callback: Optional[Callable[[int, str], None]] = None
        FileManager.ensure_directory(self.output_dir)

    def prepare_training_data(
        self, 
        audio_files: List[Path], 
        transcripts: List[str], 
        speaker_name: str
    ) -> Optional[Path]:
        try:
            dataset_dir = self.output_dir / "datasets" / FileManager.get_safe_filename(speaker_name)
            wavs_dir = dataset_dir / "wavs"
            FileManager.ensure_directory(wavs_dir)
            metadata_path = dataset_dir / "metadata.csv"
            
            with open(metadata_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter='|')
                for i, (audio_path, text) in enumerate(zip(audio_files, transcripts)):
                    dest_filename = f"{speaker_name}_{i:04d}.wav"
                    dest_path = wavs_dir / dest_filename
                    
                    if Path(audio_path).exists():
                        shutil.copy2(audio_path, dest_path)
                        writer.writerow([dest_filename, text, text])

            return dataset_dir
        except Exception as e:
            logger.error(f"Failed to prepare training data: {e}")
            return None

    @staticmethod
    def estimate_training_time(quality: str, file_count: int) -> str:
        base_minutes = {"fast": 0.5, "balanced": 1.2, "high": 2.5}.get(quality, 1.0)
        total_minutes = int(file_count * base_minutes)
        if total_minutes < 60:
            return f"{max(total_minutes, 1)} minutes"
        return f"{total_minutes // 60} hr {total_minutes % 60} min"