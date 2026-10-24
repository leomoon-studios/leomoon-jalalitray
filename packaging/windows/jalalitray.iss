#define AppName "LeoMoon JalaliTray"
#define AppExeName "LeoMoon JalaliTray.exe"
#define AppId "{{5E4CAD2F-7266-47CC-9DCE-4DF97CF83EC7}"

#ifndef AppVersion
  #error AppVersion must be passed with /DAppVersion.
#endif
#ifndef StageDir
  #error StageDir must be passed with /DStageDir.
#endif
#ifndef OutputDir
  #error OutputDir must be passed with /DOutputDir.
#endif
#ifndef AppArchitecture
  #error AppArchitecture must be passed with /DAppArchitecture.
#endif

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
VersionInfoVersion={#AppVersion}
AppPublisher=LeoMoon Studios
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir={#OutputDir}
OutputBaseFilename=leomoon-jalalitray-{#AppVersion}-windows-{#AppArchitecture}-setup
ArchitecturesAllowed={#AppArchitecture}
ArchitecturesInstallIn64BitMode={#AppArchitecture}
CloseApplications=yes
CloseApplicationsFilter={#AppExeName}
RestartApplications=no
Compression=lzma2/ultra64
SolidCompression=yes
UninstallDisplayIcon={app}\{#AppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startup"; Description: "Start LeoMoon JalaliTray with Windows"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#StageDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "LeoMoon JalaliTray"; ValueData: """{app}\{#AppExeName}"""; Tasks: startup; Flags: uninsdeletevalue

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
