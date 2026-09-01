"""Color conversion utilities between AutoCAD Color Index (ACI) and RGB/HEX."""

from typing import Tuple, Union, Optional
import ezdxf.colors

# Standard ACI basic names
ACI_NAMES = {
    1: "red",
    2: "yellow",
    3: "green",
    4: "cyan",
    5: "blue",
    6: "magenta",
    7: "white/black",
    8: "dark_gray",
    9: "light_gray",
}

NAME_TO_ACI = {
    "red": 1,
    "yellow": 2,
    "green": 3,
    "cyan": 4,
    "blue": 5,
    "magenta": 6,
    "white": 7,
    "black": 7,
    "dark_gray": 8,
    "light_gray": 9,
}


def aci_to_rgb(aci: int) -> Tuple[int, int, int]:
    """Convert AutoCAD Color Index (1-255) to (R, G, B) tuple (0-255)."""
    if 0 <= aci <= 255:
        rgb_val = ezdxf.colors.aci2rgb(aci)
        if hasattr(rgb_val, "r"):
            return (rgb_val.r, rgb_val.g, rgb_val.b)
        elif isinstance(rgb_val, (tuple, list)):
            return (int(rgb_val[0]), int(rgb_val[1]), int(rgb_val[2]))
        elif isinstance(rgb_val, int):
            r = (rgb_val >> 16) & 0xFF
            g = (rgb_val >> 8) & 0xFF
            b = rgb_val & 0xFF
            return (r, g, b)
    return (255, 255, 255)


def aci_to_hex(aci: int) -> str:
    """Convert AutoCAD Color Index to hexadecimal color string '#RRGGBB'."""
    r, g, b = aci_to_rgb(aci)
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_aci(r: int, g: int, b: int) -> int:
    """Find the closest AutoCAD Color Index (1-255) for an RGB tuple."""
    import math
    min_dist = float("inf")
    best_aci = 7
    for aci, raw_int in enumerate(ezdxf.colors.DXF_DEFAULT_COLORS):
        if aci == 0:
            continue
        rgb = ezdxf.colors.int2rgb(raw_int)
        dist = math.dist((r, g, b), (rgb.r, rgb.g, rgb.b))
        if dist < min_dist:
            min_dist = dist
            best_aci = aci
    return best_aci


def parse_color(color_input: Optional[Union[int, str, list, tuple]]) -> Optional[int]:
    """
    Parse various color representations into an ACI color index (1-255) or None.
    Supports:
    - int: 1..255 (ACI)
    - str: "red", "cyan", "#FF0000", "255,0,0"
    - list/tuple: [255, 0, 0]
    """
    if color_input is None:
        return None

    if isinstance(color_input, int):
        if 1 <= color_input <= 255:
            return color_input
        return 7

    if isinstance(color_input, (list, tuple)) and len(color_input) >= 3:
        return rgb_to_aci(int(color_input[0]), int(color_input[1]), int(color_input[2]))

    if isinstance(color_input, str):
        cleaned = color_input.strip().lower()
        if cleaned in NAME_TO_ACI:
            return NAME_TO_ACI[cleaned]
        if cleaned.startswith("#"):
            hex_str = cleaned.lstrip("#")
            if len(hex_str) == 6:
                r = int(hex_str[0:2], 16)
                g = int(hex_str[2:4], 16)
                b = int(hex_str[4:6], 16)
                return rgb_to_aci(r, g, b)
        if "," in cleaned:
            parts = [int(p.strip()) for p in cleaned.split(",")]
            if len(parts) >= 3:
                return rgb_to_aci(parts[0], parts[1], parts[2])
        try:
            val = int(cleaned)
            if 1 <= val <= 255:
                return val
        except ValueError:
            pass

    return 7  # default white/black
