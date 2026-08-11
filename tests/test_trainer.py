import pytest
from pathlib import Path
from src.trainer import VoiceTrainer

class TestVoiceTrainer:
    def test_init(self, tmp_path):
        trainer = VoiceTrainer(output_dir=tmp_path)
        assert trainer.output_dir == tmp_path

    def test_estimate_time(self):
        est = VoiceTrainer.estimate_training_time("fast", 10)
        assert "minutes" in est