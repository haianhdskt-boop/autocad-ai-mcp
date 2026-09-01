"""DXF Reader Service for inspecting, summarizing, and querying CAD drawings."""

import math
from typing import Dict, Any, List, Optional
import ezdxf
from autocad_mcp.utils.color_utils import aci_to_hex, aci_to_rgb
from autocad_mcp.utils.helpers import (
    validate_dxf_path,
    insunits_to_unit_str,
    compute_bounding_box,
)


def get_dxf_summary(file_path: str) -> Dict[str, Any]:
    """
    Get high-level summary of a DXF file:
    - Version & Units
    - Layers & Blocks counts
    - Entity breakdown by type in ModelSpace & PaperSpace
    - 2D/3D Bounding Box (Extents)
    """
    abs_path = validate_dxf_path(file_path, must_exist=True)
    doc = ezdxf.readfile(abs_path)
    msp = doc.modelspace()

    # Get units
    units_code = doc.header.get("$INSUNITS", 0)
    units_name = insunits_to_unit_str(units_code)

    # Count entities by type in modelspace
    entity_counts: Dict[str, int] = {}
    for entity in msp:
        dxftype = entity.dxftype()
        entity_counts[dxftype] = entity_counts.get(dxftype, 0) + 1

    # Bounding box
    bbox = compute_bounding_box(msp)

    # Layers list
    layers = [layer.dxf.name for layer in doc.layers]

    # Block definitions (excluding internal layout blocks)
    block_names = [
        block.name for block in doc.blocks if not block.name.startswith("*")
    ]

    return {
        "file_path": abs_path,
        "dxf_version": doc.dxfversion,
        "release": doc.acad_release,
        "units": units_name,
        "units_code": units_code,
        "layers_count": len(layers),
        "blocks_count": len(block_names),
        "total_modelspace_entities": sum(entity_counts.values()),
        "entity_counts": entity_counts,
        "bounding_box": bbox,
    }


def get_layers_info(file_path: str) -> List[Dict[str, Any]]:
    """
    List all layers with detailed properties:
    - Name, Color (ACI & Hex), Linetype, Lineweight
    - Status: is_off, is_frozen, is_locked
    - Entity count per layer in modelspace
    """
    abs_path = validate_dxf_path(file_path, must_exist=True)
    doc = ezdxf.readfile(abs_path)
    msp = doc.modelspace()

    # Count entities per layer
    layer_entity_counts: Dict[str, int] = {}
    for entity in msp:
        layer_name = entity.dxf.layer
        layer_entity_counts[layer_name] = layer_entity_counts.get(layer_name, 0) + 1

    layers_list = []
    for layer in doc.layers:
        name = layer.dxf.name
        color_aci = abs(layer.dxf.color)
        is_off = layer.dxf.color < 0 or layer.is_off()
        is_frozen = layer.is_frozen()
        is_locked = layer.is_locked()
        linetype = layer.dxf.linetype
        lineweight = getattr(layer.dxf, "lineweight", None)

        layers_list.append({
            "name": name,
            "color_aci": color_aci,
            "color_hex": aci_to_hex(color_aci),
            "linetype": linetype,
            "lineweight": lineweight,
            "is_off": is_off,
            "is_frozen": is_frozen,
            "is_locked": is_locked,
            "entity_count": layer_entity_counts.get(name, 0),
        })

    return layers_list


def get_blocks_info(file_path: str) -> List[Dict[str, Any]]:
    """
    List all block definitions and count their insertions (INSERT entities) in modelspace.
    """
    abs_path = validate_dxf_path(file_path, must_exist=True)
    doc = ezdxf.readfile(abs_path)
    msp = doc.modelspace()

    # Count inserts in modelspace
    insert_counts: Dict[str, int] = {}
    for entity in msp.query("INSERT"):
        bname = entity.dxf.name
        insert_counts[bname] = insert_counts.get(bname, 0) + 1

    blocks_list = []
    for block in doc.blocks:
        if block.name.startswith("*"):
            continue  # Skip internal layout/anonymous blocks

        entity_types: Dict[str, int] = {}
        for entity in block:
            dxftype = entity.dxftype()
            entity_types[dxftype] = entity_types.get(dxftype, 0) + 1

        blocks_list.append({
            "name": block.name,
            "description": getattr(block.block_record.dxf, "description", ""),
            "base_point": list(block.base_point),
            "sub_entity_count": len(block),
            "entity_types": entity_types,
            "instances_in_modelspace": insert_counts.get(block.name, 0),
        })

    return blocks_list


def _parse_entity_details(entity) -> Dict[str, Any]:
    """Helper to convert ezdxf entity object into JSON-serializable dictionary."""
    dxftype = entity.dxftype()
    dxf = entity.dxf

    color_aci = getattr(dxf, "color", 256)  # 256 = BYLAYER
    info: Dict[str, Any] = {
        "handle": entity.dxf.handle,
        "type": dxftype,
        "layer": dxf.layer,
        "color_aci": color_aci,
        "color_hex": aci_to_hex(color_aci) if color_aci <= 255 else "BYLAYER",
        "linetype": getattr(dxf, "linetype", "BYLAYER"),
    }

    try:
        if dxftype == "LINE":
            start = dxf.start
            end = dxf.end
            length = math.dist(start, end)
            info.update({
                "start": [round(c, 4) for c in start],
                "end": [round(c, 4) for c in end],
                "length": round(length, 4),
            })
        elif dxftype == "CIRCLE":
            center = dxf.center
            radius = dxf.radius
            info.update({
                "center": [round(c, 4) for c in center],
                "radius": round(radius, 4),
                "area": round(math.pi * radius * radius, 4),
                "circumference": round(2 * math.pi * radius, 4),
            })
        elif dxftype == "ARC":
            center = dxf.center
            radius = dxf.radius
            info.update({
                "center": [round(c, 4) for c in center],
                "radius": round(radius, 4),
                "start_angle": round(dxf.start_angle, 4),
                "end_angle": round(dxf.end_angle, 4),
            })
        elif dxftype in ("LWPOLYLINE", "POLYLINE"):
            points = []
            if dxftype == "LWPOLYLINE":
                points = [[round(p[0], 4), round(p[1], 4)] for p in entity.get_points()]
            else:
                points = [[round(v.dxf.location.x, 4), round(v.dxf.location.y, 4)] for v in entity.vertices]
            info.update({
                "points": points,
                "is_closed": entity.is_closed,
                "vertex_count": len(points),
            })
        elif dxftype in ("TEXT", "MTEXT"):
            insert = getattr(dxf, "insert", [0, 0, 0])
            text_str = entity.text if hasattr(entity, "text") else getattr(dxf, "text", "")
            info.update({
                "text": text_str,
                "insert": [round(c, 4) for c in insert],
                "height": round(getattr(dxf, "height", 2.5), 4),
                "rotation": round(getattr(dxf, "rotation", 0.0), 4),
                "style": getattr(dxf, "style", "STANDARD"),
            })
        elif dxftype == "INSERT":
            insert = dxf.insert
            info.update({
                "block_name": dxf.name,
                "insert": [round(c, 4) for c in insert],
                "scale": [
                    round(getattr(dxf, "xscale", 1.0), 4),
                    round(getattr(dxf, "yscale", 1.0), 4),
                    round(getattr(dxf, "zscale", 1.0), 4),
                ],
                "rotation": round(getattr(dxf, "rotation", 0.0), 4),
            })
        elif dxftype == "DIMENSION":
            info.update({
                "dim_type": getattr(dxf, "dimtype", 0),
                "measurement": round(getattr(dxf, "actual_measurement", 0.0), 4) if getattr(dxf, "actual_measurement", None) else None,
                "text": getattr(dxf, "text", ""),
                "defpoint": [round(c, 4) for c in getattr(dxf, "defpoint", [0, 0, 0])],
            })
        elif dxftype == "ELLIPSE":
            info.update({
                "center": [round(c, 4) for c in dxf.center],
                "major_axis": [round(c, 4) for c in dxf.major_axis],
                "ratio": round(dxf.ratio, 4),
            })
        elif dxftype == "POINT":
            info.update({
                "location": [round(c, 4) for c in dxf.location],
            })
        elif dxftype == "HATCH":
            info.update({
                "pattern_name": getattr(dxf, "pattern_name", ""),
                "solid_fill": getattr(dxf, "solid_fill", False),
            })
    except Exception as e:
        info["parse_warning"] = str(e)

    return info


def query_entities(
    file_path: str,
    entity_type: Optional[str] = None,
    layer: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> Dict[str, Any]:
    """
    Search and retrieve entities with filtering by type and layer.
    """
    abs_path = validate_dxf_path(file_path, must_exist=True)
    doc = ezdxf.readfile(abs_path)
    msp = doc.modelspace()

    # Build query string
    query_parts = []
    if entity_type:
        query_parts.append(entity_type.upper().strip())
    else:
        query_parts.append("*")

    if layer:
        query_parts.append(f'[layer=="{layer}"]')

    query_str = "".join(query_parts)
    all_matched = msp.query(query_str)
    total_matched = len(all_matched)

    # Slice for pagination
    sliced = all_matched[offset : offset + limit]
    results = [_parse_entity_details(e) for e in sliced]

    return {
        "file_path": abs_path,
        "query": query_str,
        "total_matched": total_matched,
        "offset": offset,
        "limit": limit,
        "count": len(results),
        "entities": results,
    }


def extract_texts(
    file_path: str, layer: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Extract all text elements (TEXT and MTEXT) with location, style, and content.
    Ideal for drawing analysis, OCR comparisons, title block info, and bill of materials.
    """
    abs_path = validate_dxf_path(file_path, must_exist=True)
    doc = ezdxf.readfile(abs_path)
    msp = doc.modelspace()

    query_str = "TEXT MTEXT"
    if layer:
        query_str = f'TEXT MTEXT[layer=="{layer}"]'

    extracted = []
    for entity in msp.query(query_str):
        dxftype = entity.dxftype()
        dxf = entity.dxf
        text_content = entity.text if hasattr(entity, "text") else getattr(dxf, "text", "")
        insert = getattr(dxf, "insert", [0, 0, 0])

        extracted.append({
            "handle": dxf.handle,
            "type": dxftype,
            "layer": dxf.layer,
            "text": text_content,
            "position": [round(c, 4) for c in insert],
            "height": round(getattr(dxf, "height", 2.5), 4),
            "rotation": round(getattr(dxf, "rotation", 0.0), 4),
            "style": getattr(dxf, "style", "STANDARD"),
        })

    return extracted
