[Setup]
AppName=LogSentinel
AppVersion=1.3.1
DefaultDirName={autopf}\LogSentinel
DefaultGroupName=LogSentinel
OutputDir=installer
OutputBaseFilename=LogSentinel-Setup
PrivilegesRequired=lowest
ChangesEnvironment=yes
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\logsentry.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\LogSentinel"; Filename: "{app}\logsentry.exe"
Name: "{group}\LogSentinel Demo"; Filename: "{app}\logsentry.exe"; Parameters: "demo"

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; \
  ValueData: "{olddata};{app}"; Check: NeedsAddPath('{app}')

[Code]
function NeedsAddPath(Param: string): Boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', OrigPath) then
  begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Uppercase(ExpandConstant(Param)) + ';',
                ';' + Uppercase(OrigPath) + ';') = 0;
end;