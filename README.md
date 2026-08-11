# VoiceForge Studio

VoiceForge is a cross-platform desktop application for recording voice samples and fine-tuning personal Text-to-Speech (TTS) models.

This guided desktop app for training a personal voice model with Coqui TTS can
Record or upload voice samples, review them, configure training, and you can get them 
back as a `.pth` model + `config.json` you can load in your own backend.

**Created by F.Ofem:**
			**([fofem.github.io](https://fofem.github.io))**
			**([forranova.github.io](https://forranova.github.io))**

**Copyright © 2026 ForraCorp**


## Features
- Native GUI built with Tkinter.
- Audio acquisition at 22,050 Hz mono WAV.
- Automatic dataset preparation with Coqui TTS compatibility.
- Automated CI/CD packaging for macOS (`.dmg`) and Windows (`.exe`).

## Local Development
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/dev.txt
pip install -e .
pytest


```
---

## What's in this folder

| File               | Purpose                                             |
|--------------------|-----------------------------------------------------|
| `main.py`          | The Tkinter application (run this)                  |
| `recorder.py`      | Microphone recording + playback helpers             |
| `trainer.py`       | Coqui TTS training logic (also runnable standalone) |
| `requirements.txt` | Python dependencies                                 |

## Requirements

- Python 3.9–3.12 (3.10+ recommended)
- A working microphone if you plan to record instead of upload
- ~4 GB free RAM minimum; a GPU is optional but speeds up training a lot

> **Note on Coqui TTS:** the original `coqui-ai/TTS` project is no longer
> maintained. This app uses the actively maintained community fork,
> installed as `coqui-tts` on PyPI (it keeps the same `TTS` import path,
> so no code changes are needed).

---

## Setup — macOS

1. Install Python 3.10+ if you don't already have it:
   ```bash
   brew install python@3.11
   ```
2. Install PortAudio (required by `sounddevice` for microphone access):
   ```bash
   brew install portaudio
   ```
3. Create and activate a virtual environment:
   ```bash
   cd VoiceForge
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   python main.py
   ```
6. The first time you record, macOS will ask for microphone permission —
   allow it in **System Settings → Privacy & Security → Microphone**.

---

## Setup — Windows

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/)
   and check **"Add python.exe to PATH"** during install.
2. Open **Command Prompt** or **PowerShell** in the `VoiceForge` folder.
3. Create and activate a virtual environment:
   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bat
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   `sounddevice` ships with prebuilt PortAudio binaries for Windows, so no
   extra driver install is normally needed.
5. Run the app:
   ```bat
   python main.py
   ```
6. If Windows Defender / SmartScreen prompts about microphone access,
   allow it for Python.

---

## Using the app

1. **Welcome** — click **Get Started**.
2. **Choose Input Method** — Record Now or Upload Audio Files.
3. **Record or Upload**
   - *Recording:* read the on-screen prompt aloud, click **Start
     Recording**, then **Stop Recording** when done. Record as many
     takes as you like — cycle prompts with **New Prompt**.
   - *Uploading:* browse for `.wav` files, then type the exact words
     spoken in each clip into the transcript field next to it. Coqui TTS
     needs matching text for every audio clip — without it, that clip is
     skipped during training.
4. **Review Your Voice Data** — check total duration (5+ minutes
   recommended) and play back clips before continuing.
5. **Configure Training** — enter a speaker name, pick a quality preset
   (Fast / Balanced / High Quality), and choose an output folder.
6. **Train Your Model** — click **Start Training** and watch the
   progress bar, live log, and time-remaining estimate. **Cancel**
   stops training immediately if needed.
7. **Training Complete** — your files are saved as:
   - `<speaker_name>_model.pth`
   - `config.json`

   Use **Open Output Folder** or **Copy Model Path** to grab them.

### Using the output in your own backend

Point your backend at the two output files, e.g. in Python:

```python
from TTS.api import TTS

tts = TTS(model_path="output/ethan_model.pth", config_path="output/config.json")
tts.tts_to_file(text="Hello from my own voice.", file_path="out.wav")
```

Your JavaScript/Node backend would call that Python service (or an
equivalent Coqui-compatible loader) with the same two file paths to
synthesize speech in the trained voice.

---

## Troubleshooting

- **`PortAudioError` / no microphone found (macOS):** confirm PortAudio
  is installed (`brew install portaudio`) and microphone permission is
  granted to your terminal or the packaged app.
- **Training seems very slow:** training runs on CPU unless a
  CUDA-capable GPU and matching PyTorch build are installed. This is
  expected — Fast quality is intended for quick tests, not final
  quality.
- **"No training samples had both audio and a transcript":** every
  uploaded clip needs a transcript typed in on the review/upload step;
  clips without one are skipped.
- **Quality isn't great:** more audio helps a lot. Aim for 5–15+ minutes
  of clean, varied speech, and use the Balanced or High Quality preset.

---

© 2026 ForraCorp. VoiceForge is provided as-is; Coqui TTS models are
subject to their own license terms (see the coqui-tts project for
details).
