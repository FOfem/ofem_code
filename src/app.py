"""
Main Application Entry Point for VoiceForge Desktop Application GUI.
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from src.utils import ConfigManager, SystemInfo, logger
from src.recorder import AudioRecorder
from src.trainer import VoiceTrainer


class VoiceForgeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ForraCorp VoiceForge Studio")
        self.geometry("850x600")
        self.minsize(700, 500)

        self.config_data = ConfigManager.get_config()
        self.recorder = AudioRecorder()
        self.trainer = VoiceTrainer()

        self._setup_ui()

    def _setup_ui(self):
        # Apply TTK Styling
        style = ttk.Style(self)
        style.theme_use('clam')

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_label = ttk.Label(
            main_frame, 
            text="VoiceForge Model Studio", 
            font=("Helvetica", 18, "bold")
        )
        header_label.pack(anchor=tk.W, pady=(0, 10))

        info_label = ttk.Label(
            main_frame,
            text=f"OS: {SystemInfo.get_os()} | Python: {SystemInfo.get_python_version().split()[0]}",
            font=("Helvetica", 10)
        )
        info_label.pack(anchor=tk.W, pady=(0, 20))

        # Action Area
        action_frame = ttk.LabelFrame(main_frame, text=" Controls ", padding="15")
        action_frame.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="Ready")
        status_lbl = ttk.Label(action_frame, textvariable=self.status_var, font=("Helvetica", 12))
        status_lbl.pack(pady=20)

        record_btn = ttk.Button(action_frame, text="Start Recording Prompt", command=self._toggle_recording)
        record_btn.pack(pady=10)

    def _toggle_recording(self):
        if not self.recorder.is_recording:
            if self.recorder.start_recording():
                self.status_var.set("Recording in progress...")
            else:
                messagebox.showerror("Error", "Could not start audio device.")
        else:
            data = self.recorder.stop_recording()
            self.status_var.set(f"Recorded {len(data) if data is not None else 0} samples.")


def main():
    app = VoiceForgeApp()
    app.mainloop()


if __name__ == "__main__":
    main()