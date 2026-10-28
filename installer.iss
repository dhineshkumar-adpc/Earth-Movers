#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

[Setup]
AppName=Fleet Management Software
AppVersion={#AppVersion}
AppPublisher=Dhineshkumar Adpc Murugan Trader
; Per-user install so app_data.db (saved next to the exe) stays writable
PrivilegesRequired=lowest
DefaultDirName={localappdata}\FleetManagement
DefaultGroupName=Fleet Management
DisableProgramGroupPage=yes
OutputDir=installer_out
OutputBaseFilename=FleetManagement-Setup
Compression=lzma2
SolidCompression=yes
UninstallDisplayName=Fleet Management Software
UninstallDisplayIcon={app}\FleetManagement.exe

[Files]
Source: "dist\FleetManagement\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{autodesktop}\Fleet Management"; Filename: "{app}\FleetManagement.exe"
Name: "{group}\Fleet Management"; Filename: "{app}\FleetManagement.exe"

[Run]
Filename: "{app}\FleetManagement.exe"; Description: "Launch Fleet Management"; Flags: nowait postinstall skipifsilent
