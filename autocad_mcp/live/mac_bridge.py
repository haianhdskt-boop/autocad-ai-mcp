"""macOS Live Controller for AutoCAD for Mac (2021-2026)."""

import os
import subprocess
import tempfile
from typing import Dict, Any, List, Optional
from autocad_mcp.utils.color_utils import parse_color


def is_autocad_running_mac() -> bool:
    """Check if AutoCAD for Mac application is currently running."""
    try:
        res = subprocess.run(
            ["pgrep", "-if", "AutoCAD"],
            capture_output=True,
            text=True,
        )
        return res.returncode == 0 and len(res.stdout.strip()) > 0
    except Exception:
        return False


def _execute_applescript(script: str) -> str:
    """Run an AppleScript command via osascript."""
    res = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        raise RuntimeError(f"AppleScript error: {res.stderr.strip()}")
    return res.stdout.strip()


def send_commands_to_mac(commands: List[str]) -> Dict[str, Any]:
    """
    Send raw AutoCAD commands to active AutoCAD for Mac application.
    Executes commands via queued script file and AppleScript activation.
    """
    if not commands:
        return {"status": "error", "message": "No commands provided"}

    # Prepare command buffer directory
    cmd_dir = os.path.expanduser("~/.autocad_mcp")
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
            "message": "AutoCAD for Mac is not currently running. Script written to queue.",
            "script_file": scr_file,
            "command_count": len(clean_cmds),
            "how_to_run": "Launch AutoCAD for Mac, then type 'SCRIPT' and choose ~/.autocad_mcp/live_command.scr",
        }

    # If running, activate AutoCAD window and execute script
    try:
        # AppleScript to bring AutoCAD to front and send SCRIPT command
        as_script = f'''
        tell application "System Events"
            set autocadProc to (first process whose name contains "AutoCAD")
            set frontmost of autocadProc to true
            delay 0.2
            keystroke "_SCRIPT "
            delay 0.2
            keystroke "{scr_file}"
            keystroke return
        end tell
        '''
        _execute_applescript(as_script)
        return {
            "status": "success",
            "message": "Commands sent directly to AutoCAD for Mac.",
            "command_count": len(clean_cmds),
            "script_file": scr_file,
        }
    except Exception as e:
        return {
            "status": "partial_success",
            "message": f"Script written to {scr_file}, but automatic GUI trigger encountered: {str(e)}",
            "script_file": scr_file,
            "how_to_run": "In AutoCAD, type 'SCRIPT' and choose ~/.autocad_mcp/live_command.scr or run (c:MCPSCR)",
        }


def convert_entity_to_cad_commands(entity: Dict[str, Any]) -> List[str]:
    """Convert JSON entity specification to raw AutoCAD command strings."""
    etype = entity.get("type", "").lower().strip()
    layer = entity.get("layer")
    color = parse_color(entity.get("color"))

    cmds = []
    if layer:
        if color is not None:
            cmds.append(f"_.-LAYER _M {layer} _C {color} {layer}  ")
        else:
            cmds.append(f"_.-LAYER _M {layer}  ")

    if etype == "line":
        x1, y1 = entity["start"][0], entity["start"][1]
        x2, y2 = entity["end"][0], entity["end"][1]
        cmds.append(f"_.LINE {x1},{y1} {x2},{y2} ")

    elif etype == "circle":
        cx, cy = entity["center"][0], entity["center"][1]
        r = entity["radius"]
        cmds.append(f"_.CIRCLE {cx},{cy} {r}")

    elif etype == "arc":
        cx, cy = entity["center"][0], entity["center"][1]
        r = entity["radius"]
        a1 = entity.get("start_angle", 0)
        a2 = entity.get("end_angle", 90)
        # Use ARC with Center, Start, End points
        rad1 = a1 * 3.1415926535 / 180.0
        rad2 = a2 * 3.1415926535 / 180.0
        sx = cx + r * math.cos(rad1)
        sy = cy + r * math.sin(rad1)
        ex = cx + r * math.cos(rad2)
        ey = cy + r * math.sin(rad2)
        cmds.append(f"_.ARC _C {cx},{cy} {sx},{sy} {ex},{ey}")

    elif etype in ("lwpolyline", "polyline"):
        pts = entity["points"]
        pt_strs = [f"{p[0]},{p[1]}" for p in pts]
        close_flag = " _C" if entity.get("is_closed", False) else " "
        cmds.append(f"_.PLINE {' '.join(pt_strs)}{close_flag}")

    elif etype == "rectangle":
        x1, y1 = entity["corner1"][0], entity["corner1"][1]
        x2, y2 = entity["corner2"][0], entity["corner2"][1]
        cmds.append(f"_.RECTANG {x1},{y1} {x2},{y2}")

    elif etype == "text":
        txt = str(entity["text"])
        ix, iy = entity.get("insert", [0, 0])[0], entity.get("insert", [0, 0])[1]
        h = entity.get("height", 250)
        rot = entity.get("rotation", 0)
        cmds.append(f"_.-TEXT {ix},{iy} {h} {rot} {txt}")

    elif etype == "dimension_linear":
        bx, by = entity["base"][0], entity["base"][1]
        p1x, p1y = entity["p1"][0], entity["p1"][1]
        p2x, p2y = entity["p2"][0], entity["p2"][1]
        cmds.append(f"_.DIMLINEAR {p1x},{p1y} {p2x},{p2y} {bx},{by}")

    elif etype == "block_reference":
        bname = entity["block_name"]
        ix, iy = entity.get("insert", [0, 0])[0], entity.get("insert", [0, 0])[1]
        scale = entity.get("scale", 1.0)
        rot = entity.get("rotation", 0.0)
        cmds.append(f"_.-INSERT {bname} {ix},{iy} {scale} {scale} {rot}")

    return cmds


import math


def draw_live_geometry_mac(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Draw entities live on active AutoCAD for Mac screen."""
    all_cmds = []
    for ent in entities:
        all_cmds.extend(convert_entity_to_cad_commands(ent))

    all_cmds.append("_.ZOOM _E")
    return send_commands_to_mac(all_cmds)


def zoom_extents_mac() -> Dict[str, Any]:
    """Trigger Zoom Extents on active AutoCAD for Mac window."""
    return send_commands_to_mac(["_.ZOOM _E"])
