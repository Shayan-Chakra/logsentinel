"""Ask Windows for administrator rights (the blue "Do you want to allow this app..." window)."""
import ctypes
import os
import subprocess
import sys


def build_command(extra_args, frozen=None, executable=None):
    """Work out how to start a second copy of this program.

    - Packaged .exe: run the exe itself with the same arguments.
    - Running from Python (your venv): run 'python -m logsentinel.cli' with the arguments.
    """
    frozen = getattr(sys, "frozen", False) if frozen is None else frozen
    executable = executable or sys.executable
    args = list(extra_args) if frozen else ["-m", "logsentinel.cli"] + list(extra_args)
    return executable, subprocess.list2cmdline(args)


def relaunch_as_admin(extra_args):
    """Ask Windows to start a new copy with administrator rights.

    Returns True if Windows started it, and False if the user clicked No or this is not Windows.
    """
    if sys.platform != "win32":
        return False

    program, params = build_command(extra_args)
    shell_execute = ctypes.windll.shell32.ShellExecuteW
    shell_execute.restype = ctypes.c_void_p
    result = shell_execute(None, "runas", program, params, os.getcwd(), 1)
    return int(result or 0) > 32  # 32 or less means Windows refused or the user cancelled