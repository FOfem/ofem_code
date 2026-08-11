; Installer script for VoiceForge Windows
[Setup]
AppName=VoiceForge
AppVersion=1.0.0
DefaultDirName={pf}\VoiceForge
DefaultGroupName=VoiceForge
UninstallDisplayIcon={app}\VoiceForge.exe
Compression=lzma2
SolidCompression=yes
OutputDir=dist
OutputBaseFilename=VoiceForgeSetup

[Files]
Source: "dist\VoiceForge.exe"; DestDir: "{app}"
Source: "README.md"; DestDir: "{app}"
Source: "LICENSE"; DestDir: "{app}"

[Icons]
Name: "{group}\VoiceForge"; Filename: "{app}\VoiceForge.exe"
Name: "{group}\Uninstall VoiceForge"; Filename: "{uninstallexe}"
Name: "{commondesktop}\VoiceForge"; Filename: "{app}\VoiceForge.exe"

[Run]
Filename: "{app}\VoiceForge.exe"; Description: "Launch VoiceForge"; Flags: postinstall nowait