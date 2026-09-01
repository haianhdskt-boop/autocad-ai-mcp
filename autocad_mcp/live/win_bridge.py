"""Windows Live Controller for AutoCAD Windows (2021-2026) using COM ActiveX API."""

import sys
import os
from typing import Dict, Any, List, Optional
from autocad_mcp.live.mac_bridge import convert_entity_to_cad_commands


def is_windows() -> bool:
    """Check if current operating system is Windows."""
    return sys.platform.startswith("win")


def get_active_autocad_win():
    """Connect to active AutoCAD Windows application instance via COM."""
    if not is_windows():
        raise RuntimeError("Windows COM API is only supported on Windows OS.")

    try:
        import win32com.client
    except ImportError:
        raise ImportError("pywin32 is required on Windows. Install via: pip install pywin32")

    prog_ids = [
        "AutoCAD.Application",
        "AutoCAD.Application.24.3",  # 2024
        "AutoCAD.Application.24.2",  # 2023
        "AutoCAD.Application.24.1",  # 2022
        "AutoCAD.Application.24.0",  # 2021
        "AutoCAD.Application.25.0",  # 2025
        "AutoCAD.Application.25.1",  # 2026
    ]

    for pid in prog_ids:
        try:
            acad = win32com.client.GetActiveObject(pid)
            return acad
        except Exception:
            continue

    # Try starting AutoCAD if not active
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        acad.Visible = True
        return acad
    except Exception as e:
        raise RuntimeError(f"Could not connect to AutoCAD on Windows: {str(e)}")


def send_commands_to_win(commands: List[str]) -> Dict[str, Any]:
    """Send raw AutoCAD commands to active AutoCAD Windows application."""
    if not is_windows():
        # Fallback for non-windows: write to queue file
        cmd_dir = os.path.expanduser("~/.autocad_mcp")
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
        acad = get_active_autocad_win()
        doc = acad.ActiveDocument
        for cmd in commands:
            clean_cmd = cmd.strip()
            if clean_cmd:
                doc.SendCommand(clean_cmd + "\n")

        return {
            "status": "success",
            "message": "Commands executed directly in AutoCAD Windows.",
            "command_count": len(commands),
            "active_doc": doc.Name,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send commands to AutoCAD Windows: {str(e)}",
        }


def draw_live_geometry_win(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Draw entities live on active AutoCAD Windows screen."""
    all_cmds = []
    for ent in entities:
        all_cmds.extend(convert_entity_to_cad_commands(ent))

    all_cmds.append("_.ZOOM _E")
    return send_commands_to_win(all_cmds)


def zoom_extents_win() -> Dict[str, Any]:
    """Trigger Zoom Extents on active AutoCAD Windows."""
    return send_commands_to_win(["_.ZOOM _E"])
