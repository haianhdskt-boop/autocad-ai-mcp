"""Inspector Engine: Checks dimensions, ergonomic standards, validates architectural compliance, and cleans drawing."""

from typing import Dict, Any, List, Optional
from autocad_ai.core.standards import SPACE_STANDARDS, validate_architectural_compliance


def check_room_clear_dimensions(
    length_mm: float,
    width_mm: float,
    room_type: str = "living",
) -> Dict[str, Any]:
    """
    Check if room dimensions satisfy Vietnamese architectural and ergonomic standards from architecture-reference-library.
    """
    area_m2 = round((length_mm * width_mm) / 1_000_000.0, 2)
    min_w = min(length_mm, width_mm)

    std = SPACE_STANDARDS.get(room_type.lower())
    if not std:
        # Fallback mappings
        if "master" in room_type.lower():
            std = SPACE_STANDARDS["bedroom_master"]
        elif "bedroom" in room_type.lower() or "ngu" in room_type.lower():
            std = SPACE_STANDARDS["bedroom_single"]
        elif "kitchen" in room_type.lower() or "bep" in room_type.lower():
            std = SPACE_STANDARDS["kitchen"]
        elif "wc" in room_type.lower() or "bath" in room_type.lower():
            std = SPACE_STANDARDS["wc_standard"]
        elif "corridor" in room_type.lower() or "hanh_lang" in room_type.lower():
            std = {"name": "Hành Lang", "min_area_m2": 1.0, "min_width_mm": 900.0}
        else:
            std = {"name": "Phòng Tiêu Chuẩn", "min_area_m2": 6.0, "min_width_mm": 2000.0}

    min_area = std.get("min_area_m2", 6.0)
    min_width_limit = std.get("min_width_mm", 2000.0)

    passed_area = area_m2 >= min_area
    passed_width = min_w >= min_width_limit
    is_valid = passed_area and passed_width

    warnings = []
    if not passed_area:
        warnings.append(f"Diện tích {area_m2}m² nhỏ hơn tiêu chuẩn tối thiểu ({min_area}m²)")
    if not passed_width:
        warnings.append(f"Chiều rộng lọt lòng {min_w}mm hẹp hơn tiêu chuẩn ({min_width_limit}mm)")

    return {
        "room_type": room_type,
        "room_desc": std.get("name", "Phòng"),
        "actual_area_m2": area_m2,
        "actual_min_width_mm": min_w,
        "standard_min_area_m2": min_area,
        "standard_min_width_mm": min_width_limit,
        "is_standard_compliant": is_valid,
        "warnings": warnings,
    }


def audit_full_floor_plan(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    floor_height_mm: float = 3600.0,
    num_risers: int = 21,
) -> Dict[str, Any]:
    """Audit an entire floor plan against all architectural reference standards."""
    return validate_architectural_compliance(
        width_mm=width_mm,
        length_mm=length_mm,
        rooms=rooms,
        floor_height_mm=floor_height_mm,
        num_risers=num_risers,
    )


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
