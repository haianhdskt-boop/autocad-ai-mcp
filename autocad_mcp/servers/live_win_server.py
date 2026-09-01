"""MCP Server 4: cad-live-win (AutoCAD Windows 2021-2026 COM Controller)."""

from typing import Dict, Any, List
from fastmcp import FastMCP
from autocad_mcp.live.win_bridge import (
    is_windows,
    send_commands_to_win,
    draw_live_geometry_win,
    zoom_extents_win,
)

mcp = FastMCP(
    name="cad-live-win",
    instructions="AutoCAD Windows Controller: interactively draw on screen, execute COM commands, zoom, and modify drawings live in AutoCAD on Windows.",
)


@mcp.tool()
def win_check_autocad_status() -> Dict[str, Any]:
    """Check if AutoCAD Windows is active and ready via COM."""
    on_win = is_windows()
    return {
        "is_windows": on_win,
        "platform": "Windows" if on_win else "non-Windows",
        "message": "Ready to connect via COM." if on_win else "This tool is designed for Windows environment.",
    }


@mcp.tool()
def win_send_command(commands: List[str]) -> Dict[str, Any]:
    """
    Send raw AutoCAD commands to active AutoCAD Windows instance via COM.
    Example: ['_.LINE 0,0 5000,0 ', '_.CIRCLE 2500,2500 500', '_.ZOOM _E']
    """
    return send_commands_to_win(commands)


@mcp.tool()
def win_draw_geometry(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Draw geometric entities live on AutoCAD Windows screen in real time.
    Supports: line, circle, arc, polyline, rectangle, text, dimension_linear, block_reference.
    """
    return draw_live_geometry_win(entities)


@mcp.tool()
def win_zoom_extents() -> Dict[str, Any]:
    """Execute Zoom Extents in active AutoCAD Windows."""
    return zoom_extents_win()


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
