"""MCP Server 2: cad-render-mcp (CAD Visualization & Exporter)."""

from typing import Dict, Any, Optional
from fastmcp import FastMCP
from autocad_mcp.services.dxf_renderer import (
    export_to_svg,
    export_to_png,
    export_to_pdf,
)

mcp = FastMCP(
    name="cad-render-mcp",
    instructions="CAD Visualization Engine: render DXF drawings to high-res PNG, vector SVG, and PDF with dark/light themes.",
)


@mcp.tool()
def render_to_png(
    file_path: str,
    output_path: Optional[str] = None,
    dpi: int = 300,
    bg_color: str = "white",
    dark_mode: bool = False,
    layout_name: str = "Model",
) -> Dict[str, Any]:
    """Render a DXF CAD drawing into a high-resolution PNG image."""
    return export_to_png(file_path, output_path, dpi, bg_color, dark_mode, layout_name)


@mcp.tool()
def render_to_svg(
    file_path: str,
    output_path: Optional[str] = None,
    bg_color: str = "white",
    dark_mode: bool = False,
    layout_name: str = "Model",
) -> Dict[str, Any]:
    """Render a DXF CAD drawing into crisp vector SVG format."""
    return export_to_svg(file_path, output_path, bg_color, dark_mode, layout_name)


@mcp.tool()
def render_to_pdf(
    file_path: str,
    output_path: Optional[str] = None,
    bg_color: str = "white",
    layout_name: str = "Model",
) -> Dict[str, Any]:
    """Export a DXF CAD drawing into PDF format."""
    return export_to_pdf(file_path, output_path, bg_color, layout_name)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
