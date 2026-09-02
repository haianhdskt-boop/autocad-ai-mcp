"""Drawer Engine: Generates AutoCAD commands for new architectural floor plans and spaces."""

import math
from typing import Dict, Any, List, Optional


def build_new_floor_plan_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    wall_ext_mm: float = 220.0,
    wall_int_mm: float = 110.0,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    include_furniture: bool = True,
) -> List[str]:
    """
    Generate AutoCAD commands to draft a complete new architectural floor plan.
    - width_mm: House frontage width (X-axis)
    - length_mm: House depth/length (Y-axis)
    - rooms: List of room specs, e.g. [{"name": "Phòng Khách", "y_start": 2500, "y_end": 7000, "type": "living"}]
    """
    cmds = [
        ";; ==========================================================================",
        ";; AutoCAD AI: DRAW NEW ARCHITECTURAL PLAN",
        ";; ==========================================================================",
        "_.-LAYER _M KT_TUONG_220 _C 1 KT_TUONG_220  ",
        "_.-LAYER _M KT_TUONG_110 _C 2 KT_TUONG_110  ",
        "_.-LAYER _M KT_CUA_DI _C 3 KT_CUA_DI  ",
        "_.-LAYER _M KT_CUA_SO _C 4 KT_CUA_SO  ",
        "_.-LAYER _M KT_THANG _C 5 KT_THANG  ",
        "_.-LAYER _M KT_NOITHAT _C 8 KT_NOITHAT  ",
        "_.-LAYER _M KT_TEXT _C 7 KT_TEXT  ",
        "_.-LAYER _M KT_DIMS _C 9 KT_DIMS  ",
    ]

    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    # 1. Outer boundary walls (220mm)
    cmds.append("_.-LAYER _S KT_TUONG_220  ")
    # Outer polyline
    cmds.append(f"_.RECTANG {ox},{oy} {ox + w},{oy + l}")
    # Inner polyline (thickness wall_ext_mm)
    cmds.append(
        f"_.RECTANG {ox + wall_ext_mm},{oy + wall_ext_mm} {ox + w - wall_ext_mm},{oy + l - wall_ext_mm}"
    )

    # 2. Interior rooms & dividing walls
    for r in rooms:
        r_name = r.get("name", "PHÒNG")
        y1 = oy + float(r.get("y_start", 0))
        y2 = oy + float(r.get("y_end", l))
        x1 = ox + float(r.get("x_start", wall_ext_mm))
        x2 = ox + float(r.get("x_end", w - wall_ext_mm))
        rtype = r.get("type", "standard").lower()

        # Draw horizontal dividing wall at y1 if not at bottom boundary
        if y1 > oy + wall_ext_mm and y1 < oy + l - wall_ext_mm:
            cmds.append("_.-LAYER _S KT_TUONG_110  ")
            cmds.append(f"_.LINE {ox + wall_ext_mm},{y1} {ox + w - wall_ext_mm},{y1} ")

        # Room label & area (Placed in clear zone above/offset from furniture)
        area_m2 = round(((x2 - x1) * (y2 - y1)) / 1_000_000.0, 1)
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0

        # Dedicated clear zone for text to avoid overlapping furniture
        text_y = y1 + 600.0 if rtype in ("dining", "kitchen", "bep") else cy
        cmds.append("_.-LAYER _S KT_TEXT  ")
        cmds.append(f"_.-TEXT {cx - 600},{text_y + 120} 220 0 {r_name}")
        cmds.append(f"_.-TEXT {cx - 400},{text_y - 180} 160 0 (S = {area_m2}m2)")

        # Specific elements based on room type (Strictly bounded inside inner clear area)
        if rtype in ("stairs", "staircase", "thang"):
            cmds.append("_.-LAYER _S KT_THANG  ")
            stair_w = (x2 - x1)
            step_count = int(r.get("step_count", 10))
            step_depth = (y2 - y1) / max(step_count, 1)
            for s_idx in range(step_count + 1):
                sy = y1 + s_idx * step_depth
                cmds.append(f"_.LINE {x1},{sy} {x2},{sy} ")
            # Mid line
            mid_x = (x1 + x2) / 2.0
            cmds.append(f"_.LINE {mid_x},{y1} {mid_x},{y2} ")
            # Up arrow (offset from text)
            cmds.append(f"_.LINE {x1 + stair_w*0.25},{y1 + 200} {x1 + stair_w*0.25},{y2 - 200} ")
            cmds.append(f"_.-TEXT {x1 + stair_w*0.25 + 50},{cy - 200} 140 0 UP")

        elif rtype in ("living", "khach") and include_furniture:
            cmds.append("_.-LAYER _S KT_NOITHAT  ")
            # Sofa (strictly offset from walls >= 100mm)
            cmds.append(f"_.RECTANG {x1 + 100},{y1 + 400} {x1 + 950},{y2 - 400}")
            # Coffee table (centered, non-overlapping with sofa)
            cmds.append(f"_.RECTANG {x1 + 1250},{cy - 350} {x1 + 2050},{cy + 350}")
            # TV shelf (offset from right wall)
            cmds.append(f"_.RECTANG {x2 - 450},{y1 + 400} {x2 - 100},{y2 - 400}")

        elif rtype in ("dining", "kitchen", "bep") and include_furniture:
            cmds.append("_.-LAYER _S KT_NOITHAT  ")
            # Dining table 6 chairs (placed in upper half, clear of bottom text)
            table_cy = cy + 400.0
            cmds.append(f"_.RECTANG {cx - 400},{table_cy - 500} {cx + 400},{table_cy + 500}")
            # Kitchen counter L or I (offset from walls)
            cmds.append(f"_.LINE {x1 + 100},{y2 - 600} {x2 - 100},{y2 - 600} ")

        elif rtype in ("wc", "bath", "ve_sinh") and include_furniture:
            cmds.append("_.-LAYER _S KT_NOITHAT  ")
            # Toilet bowl (hở tường 100mm, không cấn góc)
            cmds.append(f"_.CIRCLE {x1 + 450},{y1 + 450} 180")
            # Lavabo (hở tường 50mm)
            cmds.append(f"_.RECTANG {x2 - 500},{y2 - 400} {x2 - 100},{y2 - 100}")

    cmds.append("_.ZOOM _E")
    return cmds
