import cmd
import os
from pathlib import Path
from types import SimpleNamespace

from logsentinel.cli import analyze, history, show_incidents
from logsentinel.monitor import monitor

BANNER = r"""
 =========================================
   LOGSENTINEL  -  Suspicious Activity Analyzer
 =========================================
 Type 'help' to see commands, 'exit' to quit.
"""


class LogSentryConsole(cmd.Cmd):
    intro = BANNER
    prompt = "logsentry > "

    def __init__(self):
        super().__init__()
        self.options = {
            "logfile": "",
            "rules": None,
            "json": "report.json",
            "csv": None,
            "html": None,
        }

    def _check_logfile(self):
        """Return True when logfile points at a real file."""
        path = self.options["logfile"]
        if not path:
            print("[ERROR] logfile is not set. Use: set logfile <path>")
            return False
        if Path(path).is_dir():
            print("[ERROR] That is a folder. Add the file name, for example ...\\examples\\auth.log")
            return False
        return True

    def do_set(self, arg):
        """set <option> <value>   - example: set logfile examples\\auth.log"""
        parts = arg.split(maxsplit=1)
        if len(parts) != 2:
            print("Usage: set <option> <value>")
            return
        name, value = parts[0].lower(), parts[1].strip().strip('"')
        if name not in self.options:
            print(f"Unknown option '{name}'. Use 'show options'.")
            return
        self.options[name] = value
        print(f"{name} => {value}")

    def do_unset(self, arg):
        """unset <option>   - clear an option (csv, html, logfile)"""
        name = arg.strip().lower()
        if name in ("csv", "html", "logfile"):
            self.options[name] = None if name != "logfile" else ""
            print(f"{name} cleared")
        else:
            print("You can unset: logfile, csv, html")

    def do_show(self, arg):
        """show options   - show current settings"""
        if arg.strip() != "options":
            print("Usage: show options")
            return
        print(f"\n  {'Name':<10} {'Current value'}")
        print(f"  {'-' * 10} {'-' * 30}")
        for name, value in self.options.items():
            print(f"  {name:<10} {value or '(not set)'}")
        print()

    def do_run(self, arg):
        """run   - analyze the log file set in 'logfile' (.log, .csv or .evtx)"""
        if not self._check_logfile():
            return
        try:
            analyze(SimpleNamespace(**self.options))
        except SystemExit:
            pass  # analyze() already printed the error
        except Exception as error:
            print(f"[ERROR] {error}")

    def do_windows(self, arg):
        """windows [hours]   - analyze THIS PC's Windows Security log (needs Administrator)"""
        text = arg.strip() or "24"
        try:
            hours = float(text)
            if hours <= 0:
                raise ValueError
        except ValueError:
            print("Usage: windows [hours]     example: windows 24")
            return
        options = {**self.options, "logfile": None, "live_windows": True, "hours": hours}
        try:
            analyze(SimpleNamespace(**options))
        except SystemExit:
            pass
        except Exception as error:
            print(f"[ERROR] {error}")

    def do_monitor(self, arg):
        """monitor   - watch the log file live (Ctrl+C to stop)"""
        if not self._check_logfile():
            return
        try:
            monitor(self.options["logfile"], self.options["rules"])
        except Exception as error:
            print(f"[ERROR] {error}")

    def do_history(self, arg):
        """history   - show stored alerts"""
        history(SimpleNamespace(limit=20))

    def do_incidents(self, arg):
        """incidents   - show one case per attacker IP"""
        show_incidents(None)

    def do_clear(self, arg):
        """clear   - clear the screen"""
        os.system("cls" if os.name == "nt" else "clear")

    def do_exit(self, arg):
        """exit   - leave the console"""
        print("Bye!")
        return True

    do_quit = do_exit

    def do_EOF(self, arg):
        """Ctrl+Z then Enter (or Ctrl+D) leaves the console."""
        print()
        return True

    def emptyline(self):
        pass


def start_console():
    LogSentryConsole().cmdloop()