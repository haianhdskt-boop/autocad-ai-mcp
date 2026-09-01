"""DXF Writer Service for creating, updating, and modifying CAD drawings."""

import os
import math
from typing import Dict, Any, List, Optional, Union
import ezdxf
from autocad_mcp.utils.color_utils import parse_color
from autocad_mcp.utils.helpers import (
    validate_dxf_path,
    unit_str_to_insunits,
)


def create_blank_drawing(
    file_path: str,
    dxf_version: str = "R2018",
    units: str = "mm",
    layers: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Create a new blank DXF drawing with specified version and units.
    Supported versions: 'R12', 'R2000', 'R2004', 'R2007', 'R2010', 'R2013', 'R2018'.
    """
    abs_path = validate_dxf_path(file_path, must_exist=False)

    doc = ezdxf.new(dxfversion=dxf_version, setup=True)

    # Set Units
    insunits = unit_str_to_insunits(units)
    doc.header["$INSUNITS"] = insunits
    # 1 = Metric, 0 = Imperial
    doc.header["$MEASUREMENT"] = 1 if insunits in (4, 5, 6, 7, 14) else 0

    # Add custom initial layers if provided
    created_layers = ["0"]
    if layers:
        for l in layers:
            name = l.get("name", "").strip()
            if not name:
                continue
            color = parse_color(l.get("color", 7))
            linetype = l.get("linetype", "CONTINUOUS")
            doc.layers.add(name=name, color=color, linetype=linetype)
            created_layers.append(name)

    doc.saveas(abs_path)

    return {
        "status": "success",
        "file_path": abs_path,
        "dxf_version": dxf_version,
        "units": units,
        "insunits_code": insunits,
        "layers": created_layers,
    }


def add_layer(
    file_path: str,
    name: str,
    color: Optional[Union[int, str, list]] = 7,
    linetype: str = "CONTINUOUS",
    lineweight: Optional[int] = None,
    description: str = "",
) -> Dict[str, Any]:
    """
    Add or update a layer in an existing DXF drawing.
    """
    abs_path = validate_dxf_path(file_path, must_exist=True)
    doc = ezdxf.readfile(abs_path)

    color_aci = parse_color(color) or 7

    if name in doc.layers:
        layer = doc.layers.get(name)
        layer.dxf.color = color_aci
        layer.dxf.linetype = linetype
        if lineweight is not None:
            layer.dxf.lineweight = lineweight
        if description:
            layer.description = description
        action = "updated"
    else:
        layer = doc.layers.add(
            name=name,
            color=color_aci,
            linetype=linetype,
        )
        if lineweight is not None:
            layer.dxf.lineweight = lineweight
        if description:
            layer.description = description
        action = "created"

    doc.saveas(abs_path)

    return {
        "status": "success",
        "action": action,
        "layer_name": name,
        "color_aci": color_aci,
        "linetype": linetype,
        "file_path": abs_path,
    }


def _add_single_entity(msp, entity_dict: Dict[str, Any]) -> Any:
    """Helper to dispatch single entity creation into modelspace."""
    etype = entity_dict.get("type", "").lower().strip()
    layer = entity_dict.get("layer", "0")
    color = parse_color(entity_dict.get("color"))

    dxfattribs: Dict[str, Any] = {"layer": layer}
    if color is not None:
        dxfattribs["color"] = color
    if "linetype" in entity_dict:
        dxfattribs["linetype"] = entity_dict["linetype"]
    if "lineweight" in entity_dict:
        dxfattribs["lineweight"] = entity_dict["lineweight"]

    if etype == "line":
        start = entity_dict["start"]
        end = entity_dict["end"]
        return msp.add_line(start=start, end=end, dxfattribs=dxfattribs)

    elif etype == "circle":
        center = entity_dict["center"]
        radius = float(entity_dict["radius"])
        return msp.add_circle(center=center, radius=radius, dxfattribs=dxfattribs)

    elif etype == "arc":
        center = entity_dict["center"]
        radius = float(entity_dict["radius"])
        start_angle = float(entity_dict.get("start_angle", 0.0))
        end_angle = float(entity_dict.get("end_angle", 360.0))
        return msp.add_arc(
            center=center,
            radius=radius,
            start_angle=start_angle,
            end_angle=end_angle,
            dxfattribs=dxfattribs,
        )

    elif etype in ("lwpolyline", "polyline"):
        points = entity_dict["points"]
        is_closed = bool(entity_dict.get("is_closed", False))
        return msp.add_lwpolyline(
            points=points,
            close=is_closed,
            dxfattribs=dxfattribs,
        )

    elif etype == "rectangle":
        c1 = entity_dict["corner1"]
        c2 = entity_dict["corner2"]
        x1, y1 = c1[0], c1[1]
        x2, y2 = c2[0], c2[1]
        pts = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        return msp.add_lwpolyline(points=pts, close=True, dxfattribs=dxfattribs)

    elif etype == "text":
        text_str = str(entity_dict["text"])
        insert = entity_dict.get("insert", [0, 0, 0])
        height = float(entity_dict.get("height", 2.5))
        rotation = float(entity_dict.get("rotation", 0.0))
        dxfattribs["height"] = height
        dxfattribs["rotation"] = rotation
        if "style" in entity_dict:
            dxfattribs["style"] = entity_dict["style"]
        return msp.add_text(text=text_str, dxfattribs=dxfattribs).set_placement(insert)

    elif etype == "mtext":
        text_str = str(entity_dict["text"])
        insert = entity_dict.get("insert", [0, 0, 0])
        height = float(entity_dict.get("height", 2.5))
        rotation = float(entity_dict.get("rotation", 0.0))
        dxfattribs["char_height"] = height
        dxfattribs["rotation"] = rotation
        if "attachment_point" in entity_dict:
            dxfattribs["attachment_point"] = entity_dict["attachment_point"]
        mtext = msp.add_mtext(text=text_str, dxfattribs=dxfattribs)
        mtext.dxf.insert = insert
        return mtext

    elif etype == "point":
        location = entity_dict["location"]
        return msp.add_point(location=location, dxfattribs=dxfattribs)

    elif etype == "ellipse":
        center = entity_dict["center"]
        major_axis = entity_dict.get("major_axis", [10, 0, 0])
        ratio = float(entity_dict.get("ratio", 0.5))
        return msp.add_ellipse(
            center=center,
            major_axis=major_axis,
            ratio=ratio,
            dxfattribs=dxfattribs,
        )

    elif etype == "dimension_linear":
        base = entity_dict["base"]
        p1 = entity_dict["p1"]
        p2 = entity_dict["p2"]
        override_text = entity_dict.get("text", None)
        dim = msp.add_linear_dim(
            base=base,
            p1=p1,
            p2=p2,
            text=override_text,
            dxfattribs=dxfattribs,
        )
        dim.render()
        return dim

    elif etype == "block_reference":
        block_name = entity_dict["block_name"]
        insert = entity_dict.get("insert", [0, 0, 0])
        scale = entity_dict.get("scale", [1.0, 1.0, 1.0])
        rotation = float(entity_dict.get("rotation", 0.0))
        dxfattribs["rotation"] = rotation
        if isinstance(scale, (list, tuple)):
            dxfattribs["xscale"] = scale[0]
            dxfattribs["yscale"] = scale[1] if len(scale) > 1 else scale[0]
            dxfattribs["zscale"] = scale[2] if len(scale) > 2 else scale[0]
        else:
            dxfattribs["xscale"] = float(scale)
            dxfattribs["yscale"] = float(scale)
            dxfattribs["zscale"] = float(scale)
        return msp.add_blockref(name=block_name, insert=insert, dxfattribs=dxfattribs)

    else:
        raise ValueError(f"Unsupported entity type: '{etype}'")


def add_entities(
    file_path: str,
    entities: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Batch add geometric entities to modelspace in an existing DXF file.
    """
    abs_path = validate_dxf_path(file_path, must_exist=True)
    doc = ezdxf.readfile(abs_path)
    msp = doc.modelspace()

    # Ensure referenced layers exist
    existing_layers = {layer.dxf.name for layer in doc.layers}
    for ent in entities:
        layer_name = ent.get("layer")
        if layer_name and layer_name not in existing_layers:
            color = parse_color(ent.get("color")) or 7
            doc.layers.add(name=layer_name, color=color)
            existing_layers.add(layer_name)

    added_handles = []
    errors = []

    for idx, ent_spec in enumerate(entities):
        try:
            created = _add_single_entity(msp, ent_spec)
            if hasattr(created, "dxf") and hasattr(created.dxf, "handle"):
                added_handles.append(created.dxf.handle)
            else:
                added_handles.append(f"entity_{idx}")
        except Exception as e:
            errors.append({"index": idx, "spec": ent_spec, "error": str(e)})

    doc.saveas(abs_path)

    return {
        "status": "success" if not errors else "partial_success",
        "file_path": abs_path,
        "added_count": len(added_handles),
        "handles": added_handles,
        "errors": errors,
    }


def delete_entities(
    file_path: str,
    handles: Optional[List[str]] = None,
    layer: Optional[str] = None,
    entity_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Delete entities matching specific handles or layer/entity_type filter.
    """
    abs_path = validate_dxf_path(file_path, must_exist=True)
    doc = ezdxf.readfile(abs_path)
    msp = doc.modelspace()

    deleted_count = 0
    deleted_handles = []

    if handles:
        handle_set = set(handles)
        for entity in list(msp):
            if entity.dxf.handle in handle_set:
                deleted_handles.append(entity.dxf.handle)
                msp.delete_entity(entity)
                deleted_count += 1
    else:
        query_parts = []
        if entity_type:
            query_parts.append(entity_type.upper().strip())
        else:
            query_parts.append("*")

        if layer:
            query_parts.append(f'[layer=="{layer}"]')

        query_str = "".join(query_parts)
        for entity in list(msp.query(query_str)):
            deleted_handles.append(entity.dxf.handle)
            msp.delete_entity(entity)
            deleted_count += 1

    doc.saveas(abs_path)

    return {
        "status": "success",
        "file_path": abs_path,
        "deleted_count": deleted_count,
        "deleted_handles": deleted_handles,
    }


def execute_ezdxf_script(
    script_code: str,
    target_file: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute custom ezdxf Python script for complex parametric drawing generation.
    Available globals: `ezdxf`, `math`, `doc`, `msp`, `target_file`, `os`.
    If target_file is provided and doc exists, it will be automatically saved.
    """
    if target_file:
        target_path = validate_dxf_path(target_file, must_exist=False)
        if os.path.exists(target_path):
            doc = ezdxf.readfile(target_path)
        else:
            doc = ezdxf.new("R2018", setup=True)
    else:
        target_path = None
        doc = ezdxf.new("R2018", setup=True)

    msp = doc.modelspace()

    local_scope: Dict[str, Any] = {
        "ezdxf": ezdxf,
        "math": math,
        "os": os,
        "doc": doc,
        "msp": msp,
        "target_file": target_path,
        "result": None,
    }

    try:
        exec(script_code, local_scope)

        # Save doc if target_file is specified
        if target_path:
            doc.saveas(target_path)

        result_val = local_scope.get("result")
        return {
            "status": "success",
            "file_path": target_path,
            "result": str(result_val) if result_val is not None else "Execution completed successfully.",
        }
    except Exception as e:
        return {
            "status": "error",
            "file_path": target_path,
            "error": str(e),
        }
