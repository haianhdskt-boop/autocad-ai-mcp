"""AutoCAD MCP Server implementation using FastMCP."""

from typing import Dict, Any, List, Optional, Union
from fastmcp import FastMCP

from autocad_mcp.services.dxf_reader import (
    get_dxf_summary,
    get_layers_info,
    get_blocks_info,
    query_entities,
    extract_texts,
)
from autocad_mcp.services.dxf_writer import (
    create_blank_drawing as svc_create_blank,
    add_layer as svc_add_layer,
    add_entities as svc_add_entities,
    delete_entities as svc_delete_entities,
    execute_ezdxf_script as svc_exec_script,
)
from autocad_mcp.services.dxf_renderer import (
    export_to_svg as svc_export_svg,
    export_to_png as svc_export_png,
    export_to_pdf as svc_export_pdf,
)
from autocad_mcp.services.cad_scripting import (
    generate_scr_script as svc_generate_scr,
    generate_autolisp_script as svc_generate_lisp,
)

mcp = FastMCP(
    name="AutoCAD MCP Server",
    instructions="A comprehensive Model Context Protocol server for AutoCAD and DXF drawings: inspect, create, edit, render (SVG/PNG/PDF), and generate automation scripts.",
)


# ============================================================================
# 1. Inspection & Analysis Tools
# ============================================================================


@mcp.tool()
def read_dxf_summary(file_path: str) -> Dict[str, Any]:
    """
    Get a comprehensive high-level summary of a DXF CAD drawing.
    Returns: DXF version, units, layer count, block count, entity breakdown by type, total entities, and bounding box.
    """
    return get_dxf_summary(file_path=file_path)


@mcp.tool()
def list_layers(file_path: str) -> List[Dict[str, Any]]:
    """
    List all layers in a DXF drawing with properties (name, color ACI/Hex, linetype, lineweight, status on/frozen/locked, entity count).
    """
    return get_layers_info(file_path=file_path)


@mcp.tool()
def list_blocks(file_path: str) -> List[Dict[str, Any]]:
    """
    List all block definitions and their usage/instance count in modelspace.
    """
    return get_blocks_info(file_path=file_path)


@mcp.tool()
def query_drawing_entities(
    file_path: str,
    entity_type: Optional[str] = None,
    layer: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> Dict[str, Any]:
    """
    Query entities in the drawing with optional filtering by type (e.g. 'LINE', 'CIRCLE', 'LWPOLYLINE', 'TEXT', 'INSERT') and/or layer.
    Returns coordinates, dimensions, layers, and properties for each matched entity.
    """
    return query_entities(
        file_path=file_path,
        entity_type=entity_type,
        layer=layer,
        limit=limit,
        offset=offset,
    )


@mcp.tool()
def extract_drawing_texts(
    file_path: str, layer: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Extract all textual annotations, notes, and labels (TEXT & MTEXT) with exact coordinates, heights, rotations, and layers.
    """
    return extract_texts(file_path=file_path, layer=layer)


# ============================================================================
# 2. Creation & Geometry Modification Tools
# ============================================================================


@mcp.tool()
def create_drawing(
    file_path: str,
    dxf_version: str = "R2018",
    units: str = "mm",
    layers: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Create a new blank DXF CAD drawing file.
    - dxf_version: e.g. 'R2018', 'R2013', 'R2010', 'R2007', 'R2000'
    - units: 'mm', 'cm', 'm', 'in', 'ft', or 'unitless'
    - layers: optional list of initial layers, e.g. [{"name": "WALL", "color": 1, "linetype": "CONTINUOUS"}]
    """
    return svc_create_blank(
        file_path=file_path,
        dxf_version=dxf_version,
        units=units,
        layers=layers,
    )


@mcp.tool()
def add_layer(
    file_path: str,
    name: str,
    color: Union[int, str] = 7,
    linetype: str = "CONTINUOUS",
    lineweight: Optional[int] = None,
    description: str = "",
) -> Dict[str, Any]:
    """
    Add a new layer or update an existing layer in a DXF drawing.
    - color: ACI number (1-255), color name ('red', 'cyan', 'green'), or hex ('#FF0000').
    """
    return svc_add_layer(
        file_path=file_path,
        name=name,
        color=color,
        linetype=linetype,
        lineweight=lineweight,
        description=description,
    )


@mcp.tool()
def add_entities(
    file_path: str,
    entities: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Batch add geometric entities to a DXF drawing's modelspace.
    Supported entity types:
    - line: {"type": "line", "start": [x1, y1], "end": [x2, y2], "layer": "WALL", "color": 1}
    - circle: {"type": "circle", "center": [x, y], "radius": r, "layer": "HOLES"}
    - arc: {"type": "arc", "center": [x, y], "radius": r, "start_angle": a1, "end_angle": a2}
    - lwpolyline: {"type": "lwpolyline", "points": [[x1, y1], [x2, y2], ...], "is_closed": true}
    - rectangle: {"type": "rectangle", "corner1": [x1, y1], "corner2": [x2, y2], "layer": "FRAME"}
    - text: {"type": "text", "text": "Label", "insert": [x, y], "height": 3.5}
    - mtext: {"type": "mtext", "text": "Multi\nLine", "insert": [x, y], "height": 3.5}
    - point: {"type": "point", "location": [x, y]}
    - ellipse: {"type": "ellipse", "center": [x, y], "major_axis": [dx, dy, 0], "ratio": 0.5}
    - dimension_linear: {"type": "dimension_linear", "base": [x, y], "p1": [x1, y1], "p2": [x2, y2], "text": "100mm"}
    - block_reference: {"type": "block_reference", "block_name": "DOOR", "insert": [x, y], "scale": 1.0, "rotation": 0.0}
    """
    return svc_add_entities(file_path=file_path, entities=entities)


@mcp.tool()
def delete_entities(
    file_path: str,
    handles: Optional[List[str]] = None,
    layer: Optional[str] = None,
    entity_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Delete entities from a DXF file by handle list, or by layer/entity type filter.
    """
    return svc_delete_entities(
        file_path=file_path,
        handles=handles,
        layer=layer,
        entity_type=entity_type,
    )


@mcp.tool()
def execute_ezdxf_script(
    script_code: str,
    target_file: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute custom Python code using `ezdxf` for advanced parametric drafting or calculations.
    Variables provided in scope: `doc`, `msp`, `ezdxf`, `math`, `target_file`, `result`.
    Assign any final output message to variable `result`.
    """
    return svc_exec_script(script_code=script_code, target_file=target_file)


# ============================================================================
# 3. Rendering & Export Tools
# ============================================================================


@mcp.tool()
def export_drawing_to_svg(
    file_path: str,
    output_path: Optional[str] = None,
    bg_color: str = "white",
    dark_mode: bool = False,
    layout_name: str = "Model",
) -> Dict[str, Any]:
    """
    Render DXF CAD drawing to vector SVG format for crisp browser viewing.
    """
    return svc_export_svg(
        file_path=file_path,
        output_path=output_path,
        bg_color=bg_color,
        dark_mode=dark_mode,
        layout_name=layout_name,
    )


@mcp.tool()
def export_drawing_to_png(
    file_path: str,
    output_path: Optional[str] = None,
    dpi: int = 300,
    bg_color: str = "white",
    dark_mode: bool = False,
    layout_name: str = "Model",
) -> Dict[str, Any]:
    """
    Render DXF CAD drawing to a high-resolution PNG image.
    """
    return svc_export_png(
        file_path=file_path,
        output_path=output_path,
        dpi=dpi,
        bg_color=bg_color,
        dark_mode=dark_mode,
        layout_name=layout_name,
    )


@mcp.tool()
def export_drawing_to_pdf(
    file_path: str,
    output_path: Optional[str] = None,
    bg_color: str = "white",
    layout_name: str = "Model",
) -> Dict[str, Any]:
    """
    Render and export DXF CAD drawing to PDF format.
    """
    return svc_export_pdf(
        file_path=file_path,
        output_path=output_path,
        bg_color=bg_color,
        layout_name=layout_name,
    )


# ============================================================================
# 4. AutoCAD Automation Scripts (.SCR & .LSP)
# ============================================================================


@mcp.tool()
def generate_autocad_scr(
    commands: List[str],
    output_path: str,
    comment: str = "Generated by AutoCAD MCP",
) -> Dict[str, Any]:
    """
    Generate an AutoCAD Script file (.scr) for batch automation inside AutoCAD.
    """
    return svc_generate_scr(
        commands=commands,
        output_path=output_path,
        comment=comment,
    )


@mcp.tool()
def generate_autocad_lisp(
    routine_name: str,
    custom_lisp_code: Optional[str] = None,
    template_type: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None,
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate an AutoLISP (.lsp) routine file for AutoCAD users.
    - template_type: 'clean_drawing', 'create_grid', 'batch_export_pdf', or None (with custom_lisp_code).
    """
    return svc_generate_lisp(
        routine_name=routine_name,
        custom_lisp_code=custom_lisp_code,
        template_type=template_type,
        parameters=parameters,
        output_path=output_path,
    )


# ============================================================================
# Prompts
# ============================================================================


@mcp.prompt()
def analyze_cad_drawing(file_path: str) -> str:
    """Prompt template for systematically analyzing a CAD drawing."""
    return f"""Please perform a thorough architectural/engineering analysis of the CAD drawing at '{file_path}':
1. Check overall drawing metadata (units, DXF version, bounding box extents) using `read_dxf_summary`.
2. Inspect layers and layer conventions using `list_layers`.
3. Check for text annotations and titles using `extract_drawing_texts`.
4. Review key geometric elements with `query_drawing_entities`.
5. Optionally export a PNG or SVG preview using `export_drawing_to_png` to inspect visually.
Provide a clear structured report summarizing the findings, dimensions, layers, and any potential issues or recommendations."""


def main():
    """Run the FastMCP server via stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
