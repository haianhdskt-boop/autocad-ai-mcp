"""General helper functions for AutoCAD DXF manipulation."""

import os
from typing import Dict, Any, Tuple, Optional
import ezdxf
from ezdxf.bbox import extents

# AutoCAD $INSUNITS mapping
INSUNITS_MAP = {
    0: "Unitless",
    1: "Inches",
    2: "Feet",
    3: "Miles",
    4: "Millimeters",
    5: "Centimeters",
    6: "Meters",
    7: "Kilometers",
    8: "Microinches",
    9: "Mils",
    10: "Yards",
    11: "Angstroms",
    12: "Nanometers",
    13: "Microns",
    14: "Decimeters",
    15: "Decameters",
    16: "Hectometers",
    17: "Gigameters",
    18: "Astronomical Units",
    19: "Light Years",
    20: "Parsecs",
}

UNIT_NAME_TO_CODE = {
    "unitless": 0,
    "none": 0,
    "in": 1,
    "inch": 1,
    "inches": 1,
    "ft": 2,
    "feet": 2,
    "foot": 2,
    "mm": 4,
    "millimeter": 4,
    "millimeters": 4,
    "cm": 5,
    "centimeter": 5,
    "centimeters": 5,
    "m": 6,
    "meter": 6,
    "meters": 6,
    "km": 7,
    "kilometer": 7,
    "kilometers": 7,
}


def unit_str_to_insunits(unit_str: str) -> int:
    """Convert common unit string to AutoCAD $INSUNITS integer code."""
    cleaned = (unit_str or "").strip().lower()
    return UNIT_NAME_TO_CODE.get(cleaned, 4)  # Default: Millimeters (4)


def insunits_to_unit_str(code: int) -> str:
    """Convert AutoCAD $INSUNITS integer code to human readable unit string."""
    return INSUNITS_MAP.get(code, f"Unknown ({code})")


def validate_dxf_path(file_path: str, must_exist: bool = True) -> str:
    """
    Validate and return absolute DXF file path.
    Raises FileNotFoundError or ValueError if invalid.
    """
    if not file_path:
        raise ValueError("File path cannot be empty.")

    abs_path = os.path.abspath(os.path.expanduser(file_path))
    if must_exist and not os.path.exists(abs_path):
        raise FileNotFoundError(f"DXF file not found at: {abs_path}")

    # Ensure parent directory exists if writing
    if not must_exist:
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    return abs_path


def compute_bounding_box(entities) -> Optional[Dict[str, float]]:
    """Compute 2D bounding box (min_x, min_y, max_x, max_y, width, height) of entities."""
    try:
        box = extents(entities)
        if box.has_data:
            min_pt = box.extmin
            max_pt = box.extmax
            return {
                "min_x": round(float(min_pt.x), 4),
                "min_y": round(float(min_pt.y), 4),
                "min_z": round(float(min_pt.z), 4),
                "max_x": round(float(max_pt.x), 4),
                "max_y": round(float(max_pt.y), 4),
                "max_z": round(float(max_pt.z), 4),
                "width": round(float(max_pt.x - min_pt.x), 4),
                "height": round(float(max_pt.y - min_pt.y), 4),
                "depth": round(float(max_pt.z - min_pt.z), 4),
            }
    except Exception:
        pass
    return None
