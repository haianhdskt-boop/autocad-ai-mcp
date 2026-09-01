"""DXF Renderer Service for exporting CAD drawings to SVG, PNG, and PDF formats."""

import os
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy
from autocad_mcp.utils.helpers import validate_dxf_path


def _render_layout_to_file(
    doc: ezdxf.document.Drawing,
    layout_name: str,
    output_path: str,
    dpi: int = 300,
    bg_color: str = "white",
    dark_mode: bool = False,
) -> str:
    """Internal helper to render a DXF layout to file via matplotlib backend."""
    abs_output = os.path.abspath(os.path.expanduser(output_path))
    os.makedirs(os.path.dirname(abs_output), exist_ok=True)

    layout = doc.layout(layout_name) if layout_name != "Model" else doc.modelspace()

    # Determine background and color policy
    if dark_mode or bg_color.lower() in ("black", "#000000", "#1e1e1e", "#121212"):
        actual_bg = "#1e1e1e" if bg_color.lower() in ("black", "#000000") else bg_color
        config = Configuration(
            background_policy=BackgroundPolicy.CUSTOM,
            custom_bg_color=actual_bg,
            color_policy=ColorPolicy.COLOR,
        )
    else:
        actual_bg = "#ffffff" if bg_color.lower() == "white" else bg_color
        config = Configuration(
            background_policy=BackgroundPolicy.CUSTOM,
            custom_bg_color=actual_bg,
            color_policy=ColorPolicy.COLOR_SWAP_BW,
        )

    fig = plt.figure(figsize=(12, 9), facecolor=actual_bg)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=actual_bg)
    ax.set_aspect("equal", adjustable="datalim")

    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    frontend = Frontend(ctx, out, config=config)
    frontend.draw_layout(layout)

    # Clean axes
    ax.set_axis_off()

    # Determine if transparent background
    transparent = bg_color.lower() == "transparent"
    fig.savefig(
        abs_output,
        dpi=dpi,
        facecolor=fig.get_facecolor() if not transparent else "none",
        edgecolor="none",
        bbox_inches="tight",
        pad_inches=0.05,
        transparent=transparent,
    )
    plt.close(fig)

    return abs_output


def export_to_svg(
    file_path: str,
    output_path: Optional[str] = None,
    bg_color: str = "white",
    dark_mode: bool = False,
    layout_name: str = "Model",
) -> Dict[str, Any]:
    """
    Render and export a DXF drawing to SVG vector graphic.
    """
    abs_dxf = validate_dxf_path(file_path, must_exist=True)
    if not output_path:
        base, _ = os.path.splitext(abs_dxf)
        output_path = f"{base}.svg"

    doc = ezdxf.readfile(abs_dxf)
    out_file = _render_layout_to_file(
        doc=doc,
        layout_name=layout_name,
        output_path=output_path,
        dpi=150,
        bg_color=bg_color,
        dark_mode=dark_mode,
    )

    file_size_bytes = os.path.getsize(out_file)

    return {
        "status": "success",
        "format": "svg",
        "output_path": out_file,
        "size_bytes": file_size_bytes,
        "layout": layout_name,
    }


def export_to_png(
    file_path: str,
    output_path: Optional[str] = None,
    dpi: int = 300,
    bg_color: str = "white",
    dark_mode: bool = False,
    layout_name: str = "Model",
) -> Dict[str, Any]:
    """
    Render and export a DXF drawing to high-resolution raster PNG image.
    """
    abs_dxf = validate_dxf_path(file_path, must_exist=True)
    if not output_path:
        base, _ = os.path.splitext(abs_dxf)
        output_path = f"{base}.png"

    doc = ezdxf.readfile(abs_dxf)
    out_file = _render_layout_to_file(
        doc=doc,
        layout_name=layout_name,
        output_path=output_path,
        dpi=dpi,
        bg_color=bg_color,
        dark_mode=dark_mode,
    )

    file_size_bytes = os.path.getsize(out_file)

    return {
        "status": "success",
        "format": "png",
        "output_path": out_file,
        "dpi": dpi,
        "size_bytes": file_size_bytes,
        "layout": layout_name,
    }


def export_to_pdf(
    file_path: str,
    output_path: Optional[str] = None,
    bg_color: str = "white",
    layout_name: str = "Model",
) -> Dict[str, Any]:
    """
    Render and export a DXF drawing to PDF format.
    """
    abs_dxf = validate_dxf_path(file_path, must_exist=True)
    if not output_path:
        base, _ = os.path.splitext(abs_dxf)
        output_path = f"{base}.pdf"

    doc = ezdxf.readfile(abs_dxf)
    out_file = _render_layout_to_file(
        doc=doc,
        layout_name=layout_name,
        output_path=output_path,
        dpi=300,
        bg_color=bg_color,
        dark_mode=False,
    )

    file_size_bytes = os.path.getsize(out_file)

    return {
        "status": "success",
        "format": "pdf",
        "output_path": out_file,
        "size_bytes": file_size_bytes,
        "layout": layout_name,
    }
