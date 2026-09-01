"""macOS Driver: Communicates directly with AutoCAD for Mac (2021-2026)."""

import os
import subprocess
from typing import Dict, Any, List


def is_autocad_running_mac() -> bool:
    """Check if AutoCAD for Mac is running."""
    try:
        res = subprocess.run(["pgrep", "-if", "AutoCAD"], capture_output=True, text=True)
        return res.returncode == 0 and len(res.stdout.strip()) > 0
    except Exception:
        return False


def dispatch_to_autocad_mac(commands: List[str]) -> Dict[str, Any]:
    """Execute command list directly in active AutoCAD for Mac."""
    if not commands:
        return {"status": "error", "message": "No commands provided"}

    cmd_dir = os.path.expanduser("~/.autocad_ai")
    os.makedirs(cmd_dir, exist_ok=True)
    scr_file = os.path.join(cmd_dir, "live_command.scr")

    clean_cmds = [cmd.strip() for cmd in commands if cmd.strip()]
    scr_content = "\n".join(clean_cmds) + "\n\n"

    with open(scr_file, "w", encoding="utf-8") as f:
        f.write(scr_content)

    is_running = is_autocad_running_mac()
    if not is_running:
        return {
            "status": "warning",
            "message": "AutoCAD for Mac is not running. Script written to queue.",
            "script_file": scr_file,
            "command_count": len(clean_cmds),
            "how_to_run": f"Open AutoCAD for Mac -> Type 'SCRIPT' -> Select '{scr_file}'",
        }

    try:
        as_script = f'''
        tell application "System Events"
            set autocadProc to (first process whose name contains "AutoCAD")
            set frontmost of autocadProc to true
            delay 0.15
            keystroke "_SCRIPT "
            delay 0.15
            keystroke "{scr_file}"
            keystroke return
        end tell
        '''
        subprocess.run(["osascript", "-e", as_script], capture_output=True, text=True)
        return {
            "status": "success",
            "message": "Commands executed live on AutoCAD for Mac.",
            "command_count": len(clean_cmds),
            "script_file": scr_file,
        }
    except Exception as e:
        return {
            "status": "partial_success",
            "message": f"Script saved to {scr_file}, trigger note: {str(e)}",
            "script_file": scr_file,
            "how_to_run": "In AutoCAD, type 'SCRIPT' and choose ~/.autocad_ai/live_command.scr",
        }
