"""Read Windows event logs (live Security log or a saved .evtx file) through PowerShell."""
import base64
import json
import os
import subprocess
import sys

from logsentinel.winparser import rows_to_events


class WindowsLogError(Exception):
    """A problem a normal user can understand and fix."""


# The paths and hours are passed through environment variables, never pasted into
# this script, so a strange file name cannot change what the script does.
PS_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
try {
    $filter = @{ Id = 4624, 4625 }
    if ($env:LS_PATH) { $filter['Path'] = $env:LS_PATH } else { $filter['LogName'] = 'Security' }
    if ($env:LS_HOURS) {
        $hours = [double]::Parse($env:LS_HOURS, [Globalization.CultureInfo]::InvariantCulture)
        $filter['StartTime'] = (Get-Date).AddHours(-$hours)
    }
    try {
        $events = @(Get-WinEvent -FilterHashtable $filter)
    } catch {
        if ($_.FullyQualifiedErrorId -like '*NoMatchingEventsFound*') { Write-Output '[]'; exit 0 }
        throw
    }
    $rows = foreach ($e in $events) {
        $xml = [xml]$e.ToXml()
        $d = @{}
        foreach ($item in $xml.Event.EventData.Data) { $d[$item.Name] = $item.'#text' }
        [pscustomobject]@{
            Time      = $e.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss', [Globalization.CultureInfo]::InvariantCulture)
            EventId   = $e.Id
            User      = $d['TargetUserName']
            Ip        = $d['IpAddress']
            LogonType = $d['LogonType']
        }
    }
    if (-not $rows) { Write-Output '[]' } else { Write-Output (ConvertTo-Json -InputObject @($rows) -Compress) }
} catch {
    Write-Output ('ERROR: ' + $_.Exception.Message)
    exit 2
}
"""


def _is_windows():
    return sys.platform == "win32"

def is_admin():
    """True when this program is running as Administrator on Windows."""
    if not _is_windows():
        return False
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def _encoded_script():
    return base64.b64encode(PS_SCRIPT.encode("utf-16-le")).decode("ascii")


def _run_powershell(extra_env):
    env = dict(os.environ)
    env.update(extra_env)
    command = [
        "powershell.exe", "-NoProfile", "-NonInteractive",
        "-ExecutionPolicy", "Bypass", "-EncodedCommand", _encoded_script(),
    ]
    try:
        result = subprocess.run(
            command, capture_output=True, encoding="utf-8-sig", errors="replace",
            timeout=600, env=env, stdin=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        raise WindowsLogError("PowerShell was not found on this computer.")
    except subprocess.TimeoutExpired:
        raise WindowsLogError("Reading the Windows log took too long. Try a smaller --hours value.")
    return result.stdout


def _friendly(message):
    text = message.strip()
    lowered = text.lower()
    if "unauthorized" in lowered or "access is denied" in lowered or "access denied" in lowered:
        return ("Access denied. Open PowerShell as Administrator and run the command again "
                "(the Windows Security log needs admin rights).")
    if "no such file" in lowered or "cannot find" in lowered or "could not be found" in lowered:
        return f"Windows could not find or open that log: {text}"
    return f"Windows could not read the log: {text}"


def parse_output(text):
    text = (text or "").strip()
    if text.startswith("ERROR:"):
        raise WindowsLogError(_friendly(text[len("ERROR:"):]))
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise WindowsLogError(f"Could not understand the output from PowerShell: {text[:200]}")
    if isinstance(data, dict):
        data = [data]
    return rows_to_events(data)


def read_windows_events(path=None, hours=None, runner=None):
    """Return normalized events from the live Security log (path=None) or an .evtx file."""
    if runner is None:
        if not _is_windows():
            raise WindowsLogError(
                "Reading Windows event logs only works on Windows. "
                "On other systems, export the log to CSV and use --format windows."
            )
        runner = _run_powershell

    extra_env = {}
    if path:
        extra_env["LS_PATH"] = str(path)
    if hours is not None:
        try:
            hours = float(hours)
        except (TypeError, ValueError):
            raise WindowsLogError("--hours must be a number, for example 24.")
        if hours <= 0:
            raise WindowsLogError("--hours must be greater than 0.")
        extra_env["LS_HOURS"] = f"{hours:g}"

    return parse_output(runner(extra_env))