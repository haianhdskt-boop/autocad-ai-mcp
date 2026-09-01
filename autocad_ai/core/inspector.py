"""Inspector Engine: Checks dimensions, calculates clear areas, inspects drawing hygiene and layer standards."""

from typing import Dict, Any, List, Optional


def check_room_clear_dimensions(
    length_mm: float,
    width_mm: float,
    room_type: str = "living",
) -> Dict[str, Any]:
    """
    Check if room dimensions satisfy Vietnamese architectural and ergonomic standards.
    """
    area_m2 = round((length_mm * width_mm) / 1_000_000.0, 2)
    min_w = min(length_mm, width_mm)

    standards = {
        "living": {"min_area": 12.0, "min_width": 3000.0, "desc": "Phòng Khách"},
        "bedroom_master": {"min_area": 14.0, "min_width": 3200.0, "desc": "Phòng Ngủ Master"},
        "bedroom_single": {"min_area": 9.0, "min_width": 2600.0, "desc": "Phòng Ngủ Đơn"},
        "kitchen": {"min_area": 8.0, "min_width": 2200.0, "desc": "Bếp + Ăn"},
        "wc": {"min_area": 2.5, "min_width": 1200.0, "desc": "Vệ Sinh"},
        "corridor": {"min_area": 1.0, "min_width": 900.0, "desc": "Hành Lang / Lối Đi"},
        "staircase": {"min_area": 4.0, "min_width": 900.0, "desc": "Vế Thang"},
    }

    std = standards.get(room_type.lower(), {"min_area": 6.0, "min_width": 2000.0, "desc": "Phòng Tiêu Chuẩn"})

    passed_area = area_m2 >= std["min_area"]
    passed_width = min_w >= std["min_width"]
    is_valid = passed_area and passed_width

    warnings = []
    if not passed_area:
        warnings.append(f"Diện tích {area_m2}m2 nhỏ hơn tiêu chuẩn tối thiểu ({std['min_area']}m2)")
    if not passed_width:
        warnings.append(f"Chiều rộng lọt lòng {min_w}mm hẹp hơn tiêu chuẩn ({std['min_width']}mm)")

    return {
        "room_type": room_type,
        "room_desc": std["desc"],
        "actual_area_m2": area_m2,
        "actual_min_width_mm": min_w,
        "standard_min_area_m2": std["min_area"],
        "standard_min_width_mm": std["min_width"],
        "is_standard_compliant": is_valid,
        "warnings": warnings,
    }


def build_inspection_commands(action_type: str = "audit_purge") -> List[str]:
    """Generate AutoCAD commands for inspecting and cleaning drawing."""
    if action_type == "audit_purge":
        return [
            ";; ==========================================================================",
            ";; AutoCAD AI: INSPECT & CLEAN DRAWING",
            ";; ==========================================================================",
            "_.AUDIT _Y",
            "_.-PURGE _ALL * _N",
            "_.REGENALL",
            "_.ZOOM _E",
        ]
    elif action_type == "check_layer":
        return [
            ";; List non-standard layers",
            "_.-LAYER _? *  ",
        ]
    else:
        return ["_.ZOOM _E"]
