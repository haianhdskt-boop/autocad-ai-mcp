"""Plotter Engine: Standardized PDF Plotting for Single Sheets and Batch Production Sets.

Applies Vietnamese architectural plotting standards:
- Driver: DWG To PDF.pc3 / AutoCAD PDF (High Quality Print)
- Paper: ISO full bleed A3 (420.00 x 297.00 MM) / A2 / A4
- Plot Style Table: monochrome.ctb (Monochrome black print with hierarchical lineweights)
- Plot with Lineweights: ON (Cột/Tường đậm 0.40mm, Nét thấy 0.20mm, Dim/Trục 0.13mm, Hatch 0.09mm)
- Scale: 1:1 (Layout) or Fit/Scaled (Model)
- Offset: Center (C)
"""

import os
from typing import Dict, Any, List, Optional

# Standard Lineweight Hierarchy Mapping (ACI Color -> Lineweight in mm)
STANDARD_LINEWEIGHT_MAP = {
    1: 0.40,  # Đỏ (Tường bao, cột cắt chính) - Nét ĐẬM
    2: 0.25,  # Vàng (Tường ngăn, vách) - Nét VỪA
    3: 0.20,  # Xanh lá (Cửa đi, cửa sổ) - Nét VỪA
    4: 0.18,  # Cyan (Ký hiệu, Tag cửa, Tag phòng) - Nét MẢNH
    5: 0.20,  # Blue (Cầu thang, lan can) - Nét VỪA
    6: 0.13,  # Magenta (Trục tim cột, nét đứt CENTER) - Nét MẢNH
    7: 0.30,  # Trắng/Đen (Khung tên, tiêu đề bản vẽ) - Nét ĐẬM
    8: 0.09,  # Xám đậm (Hatch gạch, hatch sàn) - Nét SIÊU MẢNH
    9: 0.13,  # Xám nhạt (Đường gióng DIM, chân DIM) - Nét MẢNH
}


def build_plot_single_sheet_commands(
    sheet_code: str,
    window_p1: List[float],
    window_p2: List[float],
    output_pdf_path: str,
    paper_size: str = "A3",
    plot_style: str = "monochrome.ctb",
    orientation: str = "Landscape",
) -> List[str]:
    """
    Generate exact AutoCAD -PLOT command sequence for a single sheet with window coordinates.
    """
    abs_pdf = os.path.abspath(os.path.expanduser(output_pdf_path))
    os.makedirs(os.path.dirname(abs_pdf), exist_ok=True)

    # Standard paper definition
    if paper_size.upper() == "A3":
        media_name = "ISO full bleed A3 (420.00 x 297.00 MM)"
    elif paper_size.upper() == "A2":
        media_name = "ISO full bleed A2 (594.00 x 420.00 MM)"
    elif paper_size.upper() == "A4":
        media_name = "ISO full bleed A4 (297.00 x 210.00 MM)"
    else:
        media_name = "ISO full bleed A3 (420.00 x 297.00 MM)"

    orient_flag = "L" if orientation.lower().startswith("l") else "P"
    x1, y1 = window_p1[0], window_p1[1]
    x2, y2 = window_p2[0], window_p2[1]

    # Command sequence for AutoCAD -PLOT in Model space:
    # 1. Detailed plot config? -> Yes (Y)
    # 2. Layout name -> Model ("")
    # 3. Output device -> DWG To PDF.pc3
    # 4. Paper size -> ISO full bleed A3 (420.00 x 297.00 MM)
    # 5. Paper units -> Millimeters (M)
    # 6. Drawing orientation -> Landscape (L) / Portrait (P)
    # 7. Plot upside down? -> No (N)
    # 8. Plot area -> Window (W) -> P1 -> P2
    # 9. Plot scale -> Fit (F)
    # 10. Plot offset -> Center (C)
    # 11. Plot with plot styles? -> Yes (Y)
    # 12. Plot style table name -> monochrome.ctb
    # 13. Plot with lineweights? -> Yes (Y)
    # 14. Scale lineweights? -> No (N)
    # 15. Plot paper space first? -> No (N)
    # 16. Hide paperspace objects? -> No (N)
    # 17. Output file name -> abs_pdf
    # 18. Save changes to page setup? -> No (N)
    # 19. Proceed with plot? -> Yes (Y)

    cmds = [
        f";; ==========================================================================",
        f";; AutoCAD AI: PLOT SHEET {sheet_code} TO PDF ({paper_size})",
        f";; ==========================================================================",
        f'-PLOT Y "" "DWG To PDF.pc3" "{media_name}" M {orient_flag} N W {x1},{y1} {x2},{y2} F C Y "{plot_style}" Y N N N "{abs_pdf}" N Y',
    ]
    return cmds


def build_batch_plot_commands(
    sheets: Optional[List[Dict[str, Any]]] = None,
    output_directory: Optional[str] = None,
    project_name: str = "NHA_PHO",
    paper_size: str = "A3",
    plot_style: str = "monochrome.ctb",
    base_width_mm: float = 5000.0,
    base_length_mm: float = 15000.0,
    batch_scope: str = "full_project_set",
) -> Dict[str, Any]:
    """
    Generate batch plotting commands for architectural construction documentation sheets.
    - batch_scope: 'all_floor_plans' (KT-01 to KT-04) or 'full_project_set' (KT-01 to KT-11).
    """
    out_dir = os.path.abspath(os.path.expanduser(output_directory or "~/Desktop/CAD_PDF_Exports"))
    os.makedirs(out_dir, exist_ok=True)

    if sheets:
        sheet_list = sheets
    elif batch_scope == "all_floor_plans":
        sheet_list = [
            {"code": "KT-01", "title": "Tuong_Xay", "col_idx": 0, "row_idx": 0},
            {"code": "KT-02", "title": "Lat_San", "col_idx": 1, "row_idx": 0},
            {"code": "KT-03", "title": "Noi_That", "col_idx": 2, "row_idx": 0},
            {"code": "KT-04", "title": "Cua", "col_idx": 3, "row_idx": 0},
        ]
    else:
        # Full 11 construction sheets
        sheet_list = [
            # Row 1: Floor plans
            {"code": "KT-01", "title": "Tuong_Xay", "col_idx": 0, "row_idx": 0},
            {"code": "KT-02", "title": "Lat_San", "col_idx": 1, "row_idx": 0},
            {"code": "KT-03", "title": "Noi_That", "col_idx": 2, "row_idx": 0},
            {"code": "KT-04", "title": "Cua", "col_idx": 3, "row_idx": 0},
            # Row 2: Elevations, Sections, Ceiling, Roof
            {"code": "KT-05", "title": "Mat_Dung_Chinh", "col_idx": 0, "row_idx": 1},
            {"code": "KT-06", "title": "Mat_Cat_Doc_1-1", "col_idx": 1, "row_idx": 1},
            {"code": "KT-07", "title": "Tran_Den", "col_idx": 2, "row_idx": 1},
            {"code": "KT-08", "title": "Mai_Thoat_Nuoc", "col_idx": 3, "row_idx": 1},
            # Row 3: Details
            {"code": "KT-09", "title": "Chi_Tiet_Thang", "col_idx": 0, "row_idx": 2},
            {"code": "KT-10", "title": "Chi_Tiet_WC", "col_idx": 1, "row_idx": 2},
            {"code": "KT-11", "title": "Chi_Tiet_Cua", "col_idx": 2, "row_idx": 2},
        ]

    all_cmds = [
        ";; ==========================================================================",
        f";; AutoCAD AI: BATCH PLOT {len(sheet_list)} SHEETS TO PDF ({batch_scope.upper()})",
        ";; ==========================================================================",
    ]

    spacing_x = base_width_mm + 12000.0
    spacing_y = base_length_mm + 12000.0
    bw = 14000.0
    bh = 20000.0
    generated_files = []

    for s in sheet_list:
        code = s.get("code", "KT-01")
        title = s.get("title", "Sheet")
        c_idx = s.get("col_idx", 0)
        r_idx = s.get("row_idx", 0)

        ox = c_idx * spacing_x
        oy = r_idx * spacing_y
        p1 = [ox - 2000.0, oy - 3000.0]
        p2 = [ox - 2000.0 + bw, oy - 3000.0 + bh]

        pdf_filename = f"{project_name}_{code}_{title}.pdf"
        pdf_path = os.path.join(out_dir, pdf_filename)
        generated_files.append(pdf_path)

        all_cmds.extend(
            build_plot_single_sheet_commands(
                sheet_code=code,
                window_p1=p1,
                window_p2=p2,
                output_pdf_path=pdf_path,
                paper_size=paper_size,
                plot_style=plot_style,
            )
        )

    all_cmds.append("_.ZOOM _E")

    return {
        "commands": all_cmds,
        "sheet_count": len(sheet_list),
        "output_directory": out_dir,
        "pdf_files": generated_files,
        "plot_style": plot_style,
        "paper_size": paper_size,
    }
