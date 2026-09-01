"""MCP Server 3: cad-live-mac (AutoCAD for Mac 2021-2026 Controller)."""

from typing import Dict, Any, List
from fastmcp import FastMCP
from autocad_mcp.live.mac_bridge import (
    is_autocad_running_mac,
    send_commands_to_mac,
    draw_live_geometry_mac,
    zoom_extents_mac,
)

mcp = FastMCP(
    name="cad-live-mac",
    instructions="AutoCAD for Mac Controller: interactively draw on screen, execute commands, zoom, and modify drawings live in AutoCAD on macOS.",
)


@mcp.tool()
def mac_check_autocad_status() -> Dict[str, Any]:
    """Check if AutoCAD for Mac application is currently running."""
    running = is_autocad_running_mac()
    return {
        "is_running": running,
        "platform": "macOS",
        "message": "AutoCAD for Mac is active and ready." if running else "AutoCAD for Mac is not open.",
    }


@mcp.tool()
def mac_send_command(commands: List[str]) -> Dict[str, Any]:
    """
    Send raw AutoCAD commands to active AutoCAD for Mac window.
    Example: ['_.LINE 0,0 5000,0 ', '_.CIRCLE 2500,2500 500', '_.ZOOM _E']
    """
    return send_commands_to_mac(commands)


@mcp.tool()
def mac_draw_geometry(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Draw geometric entities live on AutoCAD for Mac screen in real time.
    Supports: line, circle, arc, polyline, rectangle, text, dimension_linear, block_reference.
    """
    return draw_live_geometry_mac(entities)


@mcp.tool()
def mac_zoom_extents() -> Dict[str, Any]:
    """Execute Zoom Extents in active AutoCAD for Mac window."""
    return zoom_extents_mac()


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
