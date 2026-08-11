"""
Main Application Entry Point for VoiceForge Desktop Application GUI.
"""

import sys
import os
import threading
import queue
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
except ImportError as e:
    print(f"Error: tkinter not found: {e}")
    print("On macOS: brew install python-tk")
    print("On Windows/Linux: Install python-tk via your package manager")
    sys.exit(1)

from .utils import ConfigManager, SystemInfo, FileManager, AudioUtils, logger
from .recorder import AudioRecorder
from .trainer import VoiceTrainer


class VoiceForgeApp(tk.Tk):
    """Main application class for VoiceForge."""
    
    def __init__(self):
        super().__init__()
        
        self.title("VoiceForge - Personal Voice Model Training Studio")
        self.geometry("1000x800")
        self.minsize(900, 700)
        
        # Load configuration
        self.config = ConfigManager.get_config()
        
        # Application state
        self.audio_recorder = AudioRecorder(
            sample_rate=self.config.get('sample_rate', 22050)
        )
        self.voice_trainer = None
        self.current_step = 0
        self.total_steps = 6
        self.recorded_files = []
        self.uploaded_files = []
        self.transcripts = []
        self.input_method = None
        self.is_recording = False
        self.recording_timer = "00:00"
        self.recording_start_time = None
        self.current_prompt_index = 0
        self.prompts = self.config.get('recording_prompts', [
            "Hello, my name is [your name].",
            "The quick brown fox jumps over the lazy dog.",
            "Good morning. How are you today?",
            "I enjoy creating new technologies and learning new things.",
            "The weather is beautiful today, perfect for a walk outside.",
            "Thank you for using VoiceForge to create your personal voice model.",
            "Artificial intelligence is transforming how we interact with computers.",
            "Please read these sentences clearly and at a natural pace."
        ])
        
        # Queue for thread-safe UI updates
        self.ui_queue = queue.Queue()
        
        # Setup styles and UI
        self._setup_styles()
        self._create_menu_bar()
        self._create_main_layout()
        self._show_welcome_screen()
        
        # Process UI queue
        self.after(100, self._process_ui_queue)
        
        # Set up cleanup on close
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Check system requirements
        self._check_requirements()
        
        logger.info("VoiceForge application initialized")
    
    def _setup_styles(self):
        """Configure ttk styles."""
        # ✅ FIX: Create style object correctly
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Colors as a dictionary (NOT a callable)
        self.colors = {
            'primary': '#4A90D9',
            'secondary': '#2C3E50',
            'success': '#27AE60',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'light': '#ECF0F1',
            'dark': '#34495E',
            'white': '#FFFFFF',
            'bg': '#F5F6FA',
            'card_bg': '#FFFFFF'
        }
        
        # ✅ FIX: Configure styles using the style object, not as a callable on self
        style.configure('Title.TLabel', font=('Helvetica', 28, 'bold'), foreground=self.colors['secondary'])
        style.configure('Subtitle.TLabel', font=('Helvetica', 14), foreground=self.colors['dark'])
        style.configure('Step.TLabel', font=('Helvetica', 18, 'bold'), foreground=self.colors['primary'])
        style.configure('Instruction.TLabel', font=('Helvetica', 12), wraplength=900)
        style.configure('Success.TLabel', font=('Helvetica', 16, 'bold'), foreground=self.colors['success'])
        style.configure('Warning.TLabel', font=('Helvetica', 12, 'bold'), foreground=self.colors['warning'])
        style.configure('Error.TLabel', font=('Helvetica', 12, 'bold'), foreground=self.colors['danger'])
        
        style.configure('Primary.TButton', font=('Helvetica', 12, 'bold'), padding=10)
        style.configure('Nav.TButton', font=('Helvetica', 11), padding=8)
        style.configure('Record.TButton', font=('Helvetica', 14, 'bold'), padding=20)
        style.configure('Card.TFrame', background=self.colors['card_bg'], relief='raised', borderwidth=1)
    
    def _create_menu_bar(self):
        """Create application menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Project", command=self._reset_app)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
    
    def _create_main_layout(self):
        """Create main application layout."""
        # Main container
        self.main_container = ttk.Frame(self, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self._create_header()
        
        # Content area
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Footer
        self._create_footer()
        
        # Navigation
        self._create_navigation()
    
    def _create_header(self):
        """Create application header."""
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(
            title_frame,
            text="VoiceForge",
            style='Title.TLabel'
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Personal Voice Model Training Studio",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack(anchor=tk.W)
    
    def _create_footer(self):
        """Create application footer."""
        footer_frame = ttk.Frame(self.main_container)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        footer_text = ttk.Label(
            footer_frame,
            text="VoiceForge - Created by F.Ofem - (c) 2026 ForraCorp",
            font=('Helvetica', 9),
            foreground='gray'
        )
        footer_text.pack()
    
    def _create_navigation(self):
        """Create navigation buttons and step indicator."""
        self.nav_frame = ttk.Frame(self.main_container)
        self.nav_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.back_button = ttk.Button(
            self.nav_frame,
            text="<- Back",
            style='Nav.TButton',
            command=self._go_back,
            state='disabled'
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.step_indicator = ttk.Label(
            self.nav_frame,
            text="",
            font=('Helvetica', 12, 'bold')
        )
        self.step_indicator.pack(side=tk.LEFT, expand=True)
        
        self.next_button = ttk.Button(
            self.nav_frame,
            text="Next ->",
            style='Primary.TButton',
            command=self._go_next,
            state='disabled'
        )
        self.next_button.pack(side=tk.RIGHT)
    
    def _process_ui_queue(self):
        """Process UI updates from threads."""
        try:
            while True:
                callback = self.ui_queue.get_nowait()
                callback()
        except queue.Empty:
            pass
        finally:
            self.after(100, self._process_ui_queue)
    
    def _show_welcome_screen(self):
        """Display the welcome screen."""
        self._clear_content()
        self.current_step = 0
        self._update_navigation()
        
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(expand=True, fill=tk.BOTH)
        
        center_frame = ttk.Frame(welcome_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        welcome_title = ttk.Label(
            center_frame,
            text="Welcome to VoiceForge!",
            style='Title.TLabel'
        )
        welcome_title.pack(pady=(0, 10))
        
        welcome_text = """Create your own personal voice model with ease.

VoiceForge guides you through the process of recording or uploading
voice samples and training an AI model that can speak in your voice.

Let's get started with just a few simple steps!"""
        
        welcome_label = ttk.Label(
            center_frame,
            text=welcome_text,
            style='Instruction.TLabel',
            justify=tk.CENTER
        )
        welcome_label.pack(pady=(0, 20))
        
        get_started_btn = ttk.Button(
            center_frame,
            text="Get Started ->",
            style='Primary.TButton',
            command=self._start_workflow
        )
        get_started_btn.pack(pady=(10, 0))
    
    def _start_workflow(self):
        """Begin the step-by-step workflow."""
        self.current_step = 1
        self._show_step1()
    
    def _show_step1(self):
        """Step 1: Choose Input Method."""
        self._clear_content()
        self._update_navigation()
        
        step_frame = ttk.Frame(self.content_frame)
        step_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        step_title = ttk.Label(
            step_frame,
            text="Step 1: Choose Input Method",
            style='Step.TLabel'
        )
        step_title.pack(pady=(20, 10))
        
        instruction = ttk.Label(
            step_frame,
            text="How would you like to provide your voice data?",
            style='Instruction.TLabel'
        )
        instruction.pack(pady=(0, 30))
        
        options_frame = ttk.Frame(step_frame)
        options_frame.pack(expand=True, fill=tk.BOTH)
        
        # Create two columns
        left_frame = ttk.Frame(options_frame)
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        
        right_frame = ttk.Frame(options_frame)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10)
        
        # Record option
        record_card = ttk.Frame(left_frame, style='Card.TFrame', padding=30)
        record_card.pack(expand=True, fill=tk.BOTH)
        
        record_icon = ttk.Label(record_card, text="[Mic]", font=('Helvetica', 56))
        record_icon.pack(pady=(0, 10))
        
        record_title = ttk.Label(record_card, text="Record Now", font=('Helvetica', 18, 'bold'))
        record_title.pack()
        
        record_desc = ttk.Label(
            record_card,
            text="Record voice samples directly\nin the application\nusing your microphone.",
            justify=tk.CENTER,
            font=('Helvetica', 11)
        )
        record_desc.pack(pady=(10, 20))
        
        record_btn = ttk.Button(
            record_card,
            text="Record Now",
            style='Primary.TButton',
            command=lambda: self._select_input_method("record")
        )
        record_btn.pack(pady=(10, 0))
        
        # Upload option
        upload_card = ttk.Frame(right_frame, style='Card.TFrame', padding=30)
        upload_card.pack(expand=True, fill=tk.BOTH)
        
        upload_icon = ttk.Label(upload_card, text="[Folder]", font=('Helvetica', 56))
        upload_icon.pack(pady=(0, 10))
        
        upload_title = ttk.Label(upload_card, text="Upload Audio Files", font=('Helvetica', 18, 'bold'))
        upload_title.pack()
        
        upload_desc = ttk.Label(
            upload_card,
            text="Browse and select\npre-recorded .wav files\nfrom your computer.",
            justify=tk.CENTER,
            font=('Helvetica', 11)
        )
        upload_desc.pack(pady=(10, 20))
        
        upload_btn = ttk.Button(
            upload_card,
            text="Upload Files",
            style='Primary.TButton',
            command=lambda: self._select_input_method("upload")
        )
        upload_btn.pack(pady=(10, 0))
        
        # Info text
        info_frame = ttk.Frame(step_frame)
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_text = ttk.Label(
            info_frame,
            text="Tip: For best results, use 5-10 minutes of clear, varied speech recordings.",
            font=('Helvetica', 11),
            foreground='gray'
        )
        info_text.pack()
    
    def _select_input_method(self, method):
        """Handle input method selection."""
        self.input_method = method
        self.current_step = 2
        if method == "record":
            self._show_step2_record()
        else:
            self._show_step2_upload()
    
    def _show_step2_record(self):
        """Step 2: Record Audio."""
        self._clear_content()
        self._update_navigation()
        
        step_frame = ttk.Frame(self.content_frame)
        step_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        step_title = ttk.Label(
            step_frame,
            text="Step 2: Record Your Voice",
            style='Step.TLabel'
        )
        step_title.pack(pady=(20, 10))
        
        # Placeholder content
        content_label = ttk.Label(
            step_frame,
            text="Recording functionality coming soon...",
            font=('Helvetica', 14)
        )
        content_label.pack(expand=True)
    
    def _show_step2_upload(self):
        """Step 2: Upload Audio Files."""
        self._clear_content()
        self._update_navigation()
        
        step_frame = ttk.Frame(self.content_frame)
        step_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        step_title = ttk.Label(
            step_frame,
            text="Step 2: Upload Audio Files",
            style='Step.TLabel'
        )
        step_title.pack(pady=(20, 10))
        
        # Placeholder content
        content_label = ttk.Label(
            step_frame,
            text="File upload functionality coming soon...",
            font=('Helvetica', 14)
        )
        content_label.pack(expand=True)
    
    def _clear_content(self):
        """Clear the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _update_navigation(self):
        """Update navigation buttons and step indicator."""
        if self.current_step == 0:
            self.step_indicator.config(text="")
        else:
            self.step_indicator.config(text=f"Step {self.current_step} of {self.total_steps}")
        
        self.back_button.config(state='normal' if self.current_step > 0 else 'disabled')
        
        if self.current_step == 0:
            self.next_button.config(text="Next ->", state='disabled')
        elif self.current_step == self.total_steps:
            self.next_button.config(state='disabled')
        else:
            self.next_button.config(text="Next ->", state='normal')
    
    def _go_back(self):
        """Navigate to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self._navigate_to_step()
    
    def _go_next(self):
        """Navigate to next step."""
        if self.current_step < self.total_steps:
            self.current_step += 1
            self._navigate_to_step()
    
    def _navigate_to_step(self):
        """Navigate to the current step."""
        if self.current_step == 0:
            self._show_welcome_screen()
        elif self.current_step == 1:
            self._show_step1()
        elif self.current_step == 2:
            if hasattr(self, 'input_method'):
                if self.input_method == "record":
                    self._show_step2_record()
                else:
                    self._show_step2_upload()
        else:
            # Placeholder for other steps
            self._clear_content()
            self._update_navigation()
            step_frame = ttk.Frame(self.content_frame)
            step_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
            
            step_title = ttk.Label(
                step_frame,
                text=f"Step {self.current_step}: Coming Soon",
                style='Step.TLabel'
            )
            step_title.pack(pady=(20, 10))
            
            placeholder = ttk.Label(
                step_frame,
                text="This step will be implemented in the next version.",
                font=('Helvetica', 14)
            )
            placeholder.pack(expand=True)
    
    def _check_requirements(self):
        """Check system requirements."""
        issues = []
        
        if sys.version_info < (3, 9):
            issues.append("Python 3.9 or higher required")
        
        try:
            import sounddevice
            devices = sounddevice.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            if not input_devices:
                issues.append("No microphone found")
        except:
            pass
        
        if issues:
            warning_text = "System checks completed with warnings:\n\n" + "\n".join(f"* {issue}" for issue in issues)
            messagebox.showwarning("System Check", warning_text)
    
    def _show_about(self):
        """Show About dialog."""
        about_text = """VoiceForge
Version 1.0.0

Personal Voice Model Training Studio
Powered by Coqui TTS

Created by F.Ofem
Copyright (c) 2026 ForraCorp
All rights reserved."""
        
        messagebox.showinfo("About VoiceForge", about_text)
    
    def _reset_app(self):
        """Reset the application to initial state."""
        if messagebox.askyesno("New Project", "Start a new project? Current progress will be lost."):
            self.recorded_files = []
            self.uploaded_files = []
            self.transcripts = []
            self.input_method = None
            self.voice_trainer = None
            self.current_step = 0
            self._show_welcome_screen()
    
    def _on_closing(self):
        """Handle window closing."""
        if self.audio_recorder:
            self.audio_recorder.cleanup()
        self.destroy()


def main():
    """Main application entry point."""
    try:
        app = VoiceForgeApp()
        app.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}")
        messagebox.showerror("Application Error", f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
