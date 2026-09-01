"""Comprehensive unit tests for AutoCAD MCP Server."""

import os
import pytest
import tempfile
import shutil

from autocad_mcp.services.dxf_writer import (
    create_blank_drawing,
    add_layer,
    add_entities,
    delete_entities,
    execute_ezdxf_script,
)
from autocad_mcp.services.dxf_reader import (
    get_dxf_summary,
    get_layers_info,
    get_blocks_info,
    query_entities,
    extract_texts,
)
from autocad_mcp.services.dxf_renderer import (
    export_to_svg,
    export_to_png,
    export_to_pdf,
)
from autocad_mcp.services.cad_scripting import (
    generate_scr_script,
    generate_autolisp_script,
)
from autocad_mcp.utils.color_utils import parse_color, aci_to_hex, rgb_to_aci


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test DXF and export files."""
    tmp = tempfile.mkdtemp(prefix="cad_mcp_test_")
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


def test_color_utilities():
    """Test color conversions and parser."""
    assert parse_color("red") == 1
    assert parse_color("yellow") == 2
    assert parse_color("green") == 3
    assert parse_color("cyan") == 4
    assert parse_color("blue") == 5
    assert parse_color("#FF0000") == 1
    assert parse_color(1) == 1
    assert aci_to_hex(1).upper() == "#FF0000"


def test_dxf_lifecycle(temp_dir):
    """Test creating, modifying, inspecting, and exporting a DXF file."""
    dxf_path = os.path.join(temp_dir, "floor_plan.dxf")

    # 1. Create drawing
    res_create = create_blank_drawing(
        file_path=dxf_path,
        dxf_version="R2018",
        units="mm",
        layers=[
            {"name": "WALLS", "color": 1},
            {"name": "DOORS", "color": 3},
            {"name": "ANNOTATIONS", "color": 7},
        ],
    )
    assert res_create["status"] == "success"
    assert os.path.exists(dxf_path)

    # 2. Add another layer
    res_layer = add_layer(
        file_path=dxf_path,
        name="FURNITURE",
        color="cyan",
        description="Furniture items",
    )
    assert res_layer["status"] == "success"
    assert res_layer["color_aci"] == 4

    # 3. Add entities
    entities_to_add = [
        # Outer room rectangle
        {"type": "rectangle", "corner1": [0, 0], "corner2": [6000, 4000], "layer": "WALLS"},
        # Partition wall
        {"type": "line", "start": [3000, 0], "end": [3000, 4000], "layer": "WALLS"},
        # Door swing arc
        {"type": "arc", "center": [3000, 1000], "radius": 900, "start_angle": 0, "end_angle": 90, "layer": "DOORS"},
        # Room labels
        {"type": "text", "text": "Living Room", "insert": [1500, 2000], "height": 250, "layer": "ANNOTATIONS"},
        {"type": "text", "text": "Bedroom", "insert": [4500, 2000], "height": 250, "layer": "ANNOTATIONS"},
        # Dimension
        {"type": "dimension_linear", "base": [0, -500], "p1": [0, 0], "p2": [6000, 0], "text": "6000 mm", "layer": "ANNOTATIONS"},
    ]
    res_entities = add_entities(file_path=dxf_path, entities=entities_to_add)
    assert res_entities["status"] == "success"
    assert res_entities["added_count"] == 6

    # 4. Inspect Summary
    summary = get_dxf_summary(file_path=dxf_path)
    assert summary["units"] == "Millimeters"
    assert summary["layers_count"] >= 4
    assert summary["total_modelspace_entities"] >= 5
    assert summary["bounding_box"] is not None
    assert summary["bounding_box"]["width"] >= 6000

    # 5. List Layers
    layers_info = get_layers_info(file_path=dxf_path)
    layer_names = [l["name"] for l in layers_info]
    assert "WALLS" in layer_names
    assert "DOORS" in layer_names
    assert "FURNITURE" in layer_names

    # 6. Extract Texts
    texts = extract_texts(file_path=dxf_path)
    assert len(texts) >= 2
    text_contents = [t["text"] for t in texts]
    assert "Living Room" in text_contents
    assert "Bedroom" in text_contents

    # 7. Query entities
    lines = query_entities(file_path=dxf_path, entity_type="LINE")
    assert lines["total_matched"] >= 1

    # 8. Export to SVG, PNG, PDF
    svg_res = export_to_svg(file_path=dxf_path)
    assert svg_res["status"] == "success"
    assert os.path.exists(svg_res["output_path"])
    assert svg_res["size_bytes"] > 0

    png_res = export_to_png(file_path=dxf_path, dpi=150)
    assert png_res["status"] == "success"
    assert os.path.exists(png_res["output_path"])
    assert png_res["size_bytes"] > 0

    pdf_res = export_to_pdf(file_path=dxf_path)
    assert pdf_res["status"] == "success"
    assert os.path.exists(pdf_res["output_path"])
    assert pdf_res["size_bytes"] > 0

    # 9. Delete entities
    del_res = delete_entities(file_path=dxf_path, layer="DOORS")
    assert del_res["status"] == "success"
    assert del_res["deleted_count"] >= 1


def test_script_execution(temp_dir):
    """Test custom ezdxf Python script execution."""
    target_dxf = os.path.join(temp_dir, "parametric_gear.dxf")
    script = """
import math
radius = 50.0
teeth = 8
doc.layers.add('GEAR', color=2)
for i in range(teeth):
    angle = i * (2 * math.pi / teeth)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    msp.add_circle((x, y), radius=5, dxfattribs={'layer': 'GEAR'})
result = f'Generated {teeth} teeth gear'
"""
    res = execute_ezdxf_script(script_code=script, target_file=target_dxf)
    assert res["status"] == "success"
    assert "8 teeth" in res["result"]
    assert os.path.exists(target_dxf)


def test_autocad_scripts(temp_dir):
    """Test generating .scr and .lsp files."""
    scr_path = os.path.join(temp_dir, "batch_clean.scr")
    scr_res = generate_scr_script(
        commands=["-PURGE ALL * N", "AUDIT Y", "ZOOM E", "QSAVE"],
        output_path=scr_path,
    )
    assert scr_res["status"] == "success"
    assert os.path.exists(scr_path)

    lsp_path = os.path.join(temp_dir, "grid_tool.lsp")
    lsp_res = generate_autolisp_script(
        routine_name="drawgrid",
        template_type="create_grid",
        parameters={"rows": 4, "cols": 4, "spacing_x": 50, "spacing_y": 50},
        output_path=lsp_path,
    )
    assert lsp_res["status"] == "success"
    assert os.path.exists(lsp_path)


def test_fastmcp_server_tools():
    """Test that all FastMCP tools are registered properly."""
    import asyncio
    from autocad_mcp.server import mcp

    tools = asyncio.run(mcp.list_tools())
    tool_names = [t.name for t in tools]

    assert "read_dxf_summary" in tool_names
    assert "create_drawing" in tool_names
    assert "add_entities" in tool_names
    assert "export_drawing_to_svg" in tool_names
    assert "export_drawing_to_png" in tool_names
    assert len(tool_names) >= 15


def test_modular_servers():
    """Test that all 4 specialized modular servers load and register tools."""
    import asyncio
    from autocad_mcp.servers.file_server import mcp as file_mcp
    from autocad_mcp.servers.render_server import mcp as render_mcp
    from autocad_mcp.servers.live_mac_server import mcp as live_mac_mcp
    from autocad_mcp.servers.live_win_server import mcp as live_win_mcp

    file_tools = [t.name for t in asyncio.run(file_mcp.list_tools())]
    assert "file_create_drawing" in file_tools
    assert "file_read_summary" in file_tools

    render_tools = [t.name for t in asyncio.run(render_mcp.list_tools())]
    assert "render_to_png" in render_tools
    assert "render_to_svg" in render_tools

    mac_tools = [t.name for t in asyncio.run(live_mac_mcp.list_tools())]
    assert "mac_send_command" in mac_tools
    assert "mac_draw_geometry" in mac_tools

    win_tools = [t.name for t in asyncio.run(live_win_mcp.list_tools())]
    assert "win_send_command" in win_tools
    assert "win_draw_geometry" in win_tools


def test_cad_command_generation():
    """Test converting geometry dict to AutoCAD command strings."""
    from autocad_mcp.live.mac_bridge import convert_entity_to_cad_commands

    line_cmds = convert_entity_to_cad_commands({"type": "line", "start": [0, 0], "end": [100, 100], "layer": "WALL"})
    assert any("_.LINE" in c for c in line_cmds)
    assert any("WALL" in c for c in line_cmds)

    circle_cmds = convert_entity_to_cad_commands({"type": "circle", "center": [50, 50], "radius": 25})
    assert any("_.CIRCLE" in c for c in circle_cmds)

