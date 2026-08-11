@echo off
echo === Building VoiceForge for Windows ===

python assets/generate_icons.py
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

pyinstaller --clean voiceforge.spec
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

echo Windows standalone build finished successfully.