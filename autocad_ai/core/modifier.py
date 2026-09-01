"""Modifier Engine: Modifies, stretches, moves, mirrors, or updates CAD objects on screen."""

from typing import Dict, Any, List, Optional


def build_modify_commands(
    action: str,
    target_description: str,
    parameters: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """
    Generate AutoCAD commands to modify or adjust existing drawing elements.
    - action: 'move', 'stretch', 'resize_room', 'change_door_swing', 'delete', 'change_layer'
    - parameters: details such as dx, dy, target_layer, new_width, center_point
    """
    params = parameters or {}
    cmds = [
        ";; ==========================================================================",
        f";; AutoCAD AI: MODIFY ELEMENT ({action.upper()} - {target_description})",
        ";; ==========================================================================",
    ]

    act = action.lower().strip()

    if act == "move":
        dx = params.get("dx", 0.0)
        dy = params.get("dy", 0.0)
        p1 = params.get("base_point", [0, 0])
        cmds.append(f";; Move elements by vector ({dx}, {dy})")
        cmds.append(f"_.MOVE _P  {p1[0]},{p1[1]} {p1[0] + dx},{p1[1] + dy}")

    elif act in ("stretch", "resize_room"):
        dx = params.get("dx", 500.0)
        dy = params.get("dy", 0.0)
        c1 = params.get("crossing_corner1", [0, 0])
        c2 = params.get("crossing_corner2", [1000, 1000])
        cmds.append(f";; Stretch crossing window from {c1} to {c2}")
        cmds.append(f"_.STRETCH _C {c1[0]},{c1[1]} {c2[0]},{c2[1]}  0,0 {dx},{dy}")

    elif act in ("change_door_swing", "flip_door", "mirror"):
        p1 = params.get("axis_p1", [0, 0])
        p2 = params.get("axis_p2", [0, 1000])
        delete_source = "Y" if params.get("delete_original", True) else "N"
        cmds.append(f";; Mirror door swing along axis ({p1} -> {p2})")
        cmds.append(f"_.MIRROR _P  {p1[0]},{p1[1]} {p2[0]},{p2[1]} {delete_source}")

    elif act in ("change_layer", "set_layer"):
        new_layer = params.get("layer", "0")
        cmds.append(f";; Change layer of previous selection to {new_layer}")
        cmds.append(f"_.-CHANGE _P  _P _LA {new_layer}  ")

    elif act in ("delete", "erase"):
        cmds.append(";; Erase previous selection")
        cmds.append("_.ERASE _P ")

    else:
        # Generic custom command
        custom_cmd = params.get("command", "_.ZOOM _E")
        cmds.append(custom_cmd)

    cmds.append("_.ZOOM _E")
    return cmds
