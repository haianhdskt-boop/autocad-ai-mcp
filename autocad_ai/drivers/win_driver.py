"""Windows Driver: Communicates directly with AutoCAD Windows (2021-2026) via COM."""

import sys
import os
from typing import Dict, Any, List


def is_windows() -> bool:
    """Check if running on Windows OS."""
    return sys.platform.startswith("win")


def dispatch_to_autocad_win(commands: List[str]) -> Dict[str, Any]:
    """Execute command list directly in active AutoCAD Windows."""
    if not is_windows():
        cmd_dir = os.path.expanduser("~/.autocad_ai")
        os.makedirs(cmd_dir, exist_ok=True)
        scr_file = os.path.join(cmd_dir, "live_command_win.scr")
        with open(scr_file, "w", encoding="utf-8") as f:
            f.write("\n".join(commands) + "\n\n")

        return {
            "status": "warning",
            "message": "Current environment is not Windows. Script generated and saved for Windows AutoCAD.",
            "script_file": scr_file,
            "command_count": len(commands),
        }

    try:
        import win32com.client
    except ImportError:
        return {
            "status": "error",
            "message": "pywin32 library is required on Windows. Run: pip install pywin32",
        }

    try:
        prog_ids = [
            "AutoCAD.Application",
            "AutoCAD.Application.24.3",  # 2024
            "AutoCAD.Application.24.2",  # 2023
            "AutoCAD.Application.24.1",  # 2022
            "AutoCAD.Application.24.0",  # 2021
            "AutoCAD.Application.25.0",  # 2025
            "AutoCAD.Application.25.1",  # 2026
        ]
        acad = None
        for pid in prog_ids:
            try:
                acad = win32com.client.GetActiveObject(pid)
                if acad:
                    break
            except Exception:
                continue

        if not acad:
            acad = win32com.client.Dispatch("AutoCAD.Application")
            acad.Visible = True

        doc = acad.ActiveDocument
        for cmd in commands:
            c = cmd.strip()
            if c and not c.startswith(";;"):
                doc.SendCommand(c + "\n")

        return {
            "status": "success",
            "message": "Commands executed live on AutoCAD Windows.",
            "command_count": len(commands),
            "active_doc": doc.Name,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to execute commands on AutoCAD Windows: {str(e)}",
        }
