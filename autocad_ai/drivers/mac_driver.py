"""macOS Driver: Communicates directly with AutoCAD for Mac (2021-2026)."""

import os
import subprocess
from typing import Dict, Any, List


def is_autocad_running_mac() -> bool:
    """Check if AutoCAD or any DWG CAD (ZWCAD, BricsCAD) is running on macOS."""
    for cad_app in ("AutoCAD", "ZWCAD", "BricsCAD"):
        try:
            res = subprocess.run(["pgrep", "-if", cad_app], capture_output=True, text=True)
            if res.returncode == 0 and len(res.stdout.strip()) > 0:
                return True
        except Exception:
            continue
    return False


def dispatch_to_autocad_mac(commands: List[str]) -> Dict[str, Any]:
    """Execute command list directly in active AutoCAD / ZWCAD / BricsCAD for Mac."""
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
            "message": "Phần mềm CAD (AutoCAD/ZWCAD/BricsCAD) chưa mở. File kịch bản đã được lưu sẵn.",
            "script_file": scr_file,
            "command_count": len(clean_cmds),
            "how_to_run": f"Mở CAD lên -> Gõ lệnh 'SCRIPT' -> Chọn file '{scr_file}'",
        }

    try:
        as_script = f'''
        tell application "System Events"
            set cadProc to (first process whose name contains "AutoCAD" or name contains "ZWCAD" or name contains "BricsCAD")
            set frontmost of cadProc to true
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
            "message": "Đã thực thi trực tiếp trên màn hình CAD (macOS).",
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
