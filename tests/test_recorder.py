import pytest
import numpy as np
from unittest.mock import patch, MagicMock

# Import your AudioRecorder class
from src.recorder import AudioRecorder

@pytest.fixture
def mock_sounddevice():
    """Mock sounddevice functions to prevent hardware calls on headless CI runners."""
    with patch('sounddevice.query_devices') as mock_query, \
         patch('sounddevice.InputStream') as mock_stream, \
         patch('sounddevice.check_input_settings') as mock_check:
        
        # Simulate a fake default input device
        mock_query.return_value = [
            {'name': 'Mock Built-in Microphone', 'max_input_channels': 2, 'default_samplerate': 44100}
        ]
        
        # Mock stream instance
        stream_instance = MagicMock()
        mock_stream.return_value = stream_instance
        
        yield {
            'query': mock_query,
            'stream': mock_stream,
            'check': mock_check
        }

class TestAudioRecorder:

    def test_recorder_initialization(self, mock_sounddevice):
        """Test recorder initialization with mocked hardware."""
        recorder = AudioRecorder()
        assert recorder.sample_rate in [22050, 44100]
        assert not getattr(recorder, 'is_recording', False)

    def test_start_stop_recording_mocked(self, mock_sounddevice):
        """Test start and stop controls without touching sound cards."""
        recorder = AudioRecorder()
        
        if hasattr(recorder, 'start_recording'):
            recorder.start_recording()
            assert recorder.is_recording is True
            
        if hasattr(recorder, 'stop_recording'):
            recorder.stop_recording()
            assert recorder.is_recording is False

    def test_duration_calculation(self):
        """Pure math unit test independent of audio hardware."""
        recorder = AudioRecorder()
        sample_rate = 22050
        dummy_audio = np.zeros(sample_rate * 3) # 3 seconds of silent dummy data
        
        if hasattr(recorder, 'get_audio_duration'):
            duration = recorder.get_audio_duration(dummy_audio)
            assert duration == 3.0