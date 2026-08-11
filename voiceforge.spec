# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

datas = collect_data_files('src')
hiddenimports = collect_submodules('sounddevice') + collect_submodules('soundfile') + ['tkinter', 'ttk']

icon_path = 'src/resources/icon.icns' if sys.platform == 'darwin' else 'src/resources/icon.ico'
if not os.path.exists(icon_path):
    icon_path = None

a = Analysis(
    ['src/app.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VoiceForge',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VoiceForge',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='VoiceForge.app',
        icon='src/resources/icon.icns',
        bundle_identifier='com.forracorp.voiceforge',
    )