# ForraCorp VoiceForge - Personal Voice Model Training Studio
# Version: 1.0.0

import sys
import threading
import time
from pathlib import Path
from typing import Optional, Tuple, Callable
import numpy as np

try:
    import sounddevice as sd
    import soundfile as sf
except ImportError as e:
    sd = None
    sf = None

from .utils import AudioUtils, FileManager, logger


class AudioRecorder:
    def __init__(self, sample_rate: int = 22050, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.audio_data = []
        self.stream = None
        self.recording_lock = threading.Lock()
        self.recording_start_time = None
        self.recording_duration = 0.0
        self.error_callback = None
        self.has_device = False
        
        self._validate_audio_device()
    
    def _validate_audio_device(self):
        if sd is None:
            self.has_device = False
            return
        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d.get('max_input_channels', 0) > 0]
            self.has_device = len(input_devices) > 0
        except Exception as e:
            self.has_device = False
            logger.warning(f"Audio device check bypassed: {e}")
    
    def start_recording(self) -> bool:
        if sd is None:
            logger.error("sounddevice package missing.")
            return False

        with self.recording_lock:
            if self.is_recording:
                return False
            
            try:
                self.audio_data = []
                self.is_recording = True
                self.recording_start_time = time.time()
                
                self.stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    callback=self._audio_callback,
                    dtype='float32'
                )
                self.stream.start()
                return True
            except Exception as e:
                self.is_recording = False
                logger.error(f"Failed to start recording: {e}")
                return False
    
    def _audio_callback(self, indata, frames, time_info, status):
        if self.is_recording:
            self.audio_data.append(indata.copy())
    
    def stop_recording(self) -> Optional[np.ndarray]:
        with self.recording_lock:
            if not self.is_recording:
                return None
            
            self.is_recording = False
            try:
                if self.stream:
                    self.stream.stop()
                    self.stream.close()
                    self.stream = None
                
                if not self.audio_data:
                    return None
                
                audio_array = np.concatenate(self.audio_data, axis=0)
                self.audio_data = []
                return audio_array
            except Exception as e:
                logger.error(f"Failed to stop recording: {e}")
                return None

    def save_recording(self, audio_data: np.ndarray, filename: str, output_dir: Optional[Path] = None) -> Optional[Path]:
        if sf is None:
            return None
        try:
            if output_dir is None:
                output_dir = Path.home() / '.voiceforge' / 'recordings'
            
            FileManager.ensure_directory(output_dir)
            if not filename.endswith('.wav'):
                filename = f"{filename}.wav"
            
            safe_filename = FileManager.get_safe_filename(filename)
            filepath = output_dir / safe_filename
            sf.write(str(filepath), audio_data, self.sample_rate)
            return filepath
        except Exception as e:
            logger.error(f"Failed to save recording: {e}")
            return None

    def get_audio_duration(self, audio_data: np.ndarray) -> float:
        if audio_data is not None and len(audio_data) > 0:
            return len(audio_data) / self.sample_rate
        return 0.0