"""Finalizer Engine: Generates the 4 Professional Construction Documentation Sheets.

1. Wall Construction Sheet (Mặt bằng Kích thước tường xây - KT01)
2. Floor Finishes Sheet (Mặt bằng Định vị & Ốp lát sàn, cao độ, mốc lát, độ dốc - KT02)
3. Furniture Layout Sheet (Mặt bằng Bố trí nội thất & Bảng thống kê - KT03)
4. Door & Window Schedule Sheet (Mặt bằng Định vị & Phân loại cửa, bậu, lanh-tô - KT04)
"""

from typing import Dict, Any, List, Optional


def build_title_block_commands(
    origin_x: float,
    origin_y: float,
    sheet_title: str,
    sheet_code: str,
    project_name: str = "NHÀ PHỐ DÂN DỤNG",
    scale_str: str = "1/100",
    paper_size: str = "A3",
) -> List[str]:
    """Generate AutoCAD commands for a standard A3/A2 Architectural Title Block."""
    # Standard A3 border at 1/100 scale = 42000 x 29700 mm
    # Scaled down to fit typical floor plan workspace (e.g. 15000 x 22000 mm around drawing)
    bw = 14000.0
    bh = 20000.0
    ox, oy = origin_x - 2000.0, origin_y - 3000.0

    cmds = [
        "_.-LAYER _M KT_KHUNG_TEN _C 7 KT_KHUNG_TEN  ",
        "_.-LAYER _S KT_KHUNG_TEN  ",
        # Outer Border
        f"_.RECTANG {ox},{oy} {ox + bw},{oy + bh}",
        # Inner Border
        f"_.RECTANG {ox + 200},{oy + 200} {ox + bw - 200},{oy + bh - 200}",
        # Title box at bottom
        f"_.RECTANG {ox + 200},{oy + 200} {ox + bw - 200},{oy + 2200}",
        # Lines inside title box
        f"_.LINE {ox + 200},{oy + 1200} {ox + bw - 200},{oy + 1200} ",
        f"_.LINE {ox + bw - 3500},{oy + 200} {ox + bw - 3500},{oy + 2200} ",
        # Texts
        f"_.-TEXT {ox + 500},{oy + 1500} 350 0 DU AN: {project_name.upper()}",
        f"_.-TEXT {ox + 500},{oy + 600} 400 0 HANG MUC: {sheet_title.upper()}",
        f"_.-TEXT {ox + bw - 3200},{oy + 1500} 250 0 TY LE: {scale_str}",
        f"_.-TEXT {ox + bw - 3200},{oy + 600} 450 0 SO: {sheet_code}",
    ]
    return cmds


def build_wall_construction_sheet_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """1. Mặt bằng kích thước tường xây (KT-01): Clean walls, 3-tier dims, wall thickness notes, no furniture."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; 1. SHEET KT-01: MAT BANG KICH THUOC TUONG XAY",
        ";; ==========================================================================",
        # Freeze furniture for clean masonry drawing
        "_.-LAYER _F KT_NOITHAT  ",
        "_.-LAYER _M KT_DIMS_TUONG _C 1 KT_DIMS_TUONG  ",
        "_.-LAYER _M KT_HATCH_TUONG _C 8 KT_HATCH_TUONG  ",
        "_.-LAYER _M KT_TRUC _C 6 KT_TRUC  ",
    ]

    # Dim Layer 1: Exterior dimensions (Bottom & Left)
    cmds.append("_.-LAYER _S KT_DIMS_TUONG  ")
    # Overall frontage & length
    cmds.append(f"_.DIMLINEAR {ox},{oy} {ox + w},{oy} {ox},{oy - 1200}")
    cmds.append(f"_.DIMLINEAR {ox},{oy} {ox},{oy + l} {ox - 1400},{oy}")

    # Dim Layer 2: Room by room masonry segments (Left side)
    prev_y = oy
    for r in rooms:
        y_end = oy + float(r.get("y_end", l))
        r_name = r.get("name", "Tường")
        cmds.append(f"_.DIMLINEAR {ox},{prev_y} {ox},{y_end} {ox - 600},{prev_y}")
        prev_y = y_end

    # Wall thickness notes
    cmds.append("_.-LAYER _S KT_TEXT  ")
    cmds.append(f"_.-TEXT {ox + 300},{oy + 400} 180 0 TUONG BAO 220mm (GẠCH ĐẶC)")
    cmds.append(f"_.-TEXT {ox + 300},{oy + l*0.5} 180 0 TUONG NGAN 110mm (GẠCH LỖ)")

    # Title Block
    cmds.extend(
        build_title_block_commands(
            ox, oy, "MẶT BẰNG KÍCH THƯỚC TƯỜNG XÂY", "KT-01", project_name
        )
    )
    return cmds


def build_floor_finishes_sheet_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """2. Mặt bằng ốp lát sàn & cao độ (KT-02): Starting tile markers, slope arrows, elevations, clean room areas."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; 2. SHEET KT-02: MAT BANG DINH VI & OP LAT SAN",
        ";; ==========================================================================",
        "_.-LAYER _F KT_NOITHAT  ",
        "_.-LAYER _M KT_SAN_HATCH _C 9 KT_SAN_HATCH  ",
        "_.-LAYER _M KT_SAN_NOTE _C 3 KT_SAN_NOTE  ",
    ]

    for r in rooms:
        r_name = r.get("name", "").upper()
        y1 = oy + float(r.get("y_start", 0))
        y2 = oy + float(r.get("y_end", l))
        cx = ox + w * 0.5
        cy = (y1 + y2) * 0.5
        rtype = r.get("type", "").lower()

        cmds.append("_.-LAYER _S KT_SAN_NOTE  ")

        # Elevation tag & finish material
        if "khach" in rtype or "living" in rtype:
            cmds.append(f"_.-TEXT {cx - 1000},{cy + 400} 200 0 SAN GACH GRANITE 800x800")
            cmds.append(f"_.-TEXT {cx - 600},{cy} 250 0 COT SAN: +0.450")
            # Starting tile marker (circle with cross)
            cmds.append(f"_.CIRCLE {ox + 500},{y1 + 500} 150")
            cmds.append(f"_.LINE {ox + 350},{y1 + 500} {ox + 650},{y1 + 500} ")
            cmds.append(f"_.LINE {ox + 500},{y1 + 350} {ox + 500},{y1 + 650} ")
            cmds.append(f"_.-TEXT {ox + 700},{y1 + 450} 150 0 DIEM LAT DAU TIEN")

        elif "ngu" in rtype or "bed" in rtype:
            cmds.append(f"_.-TEXT {cx - 1000},{cy + 400} 200 0 SAN GO CONG NGHIEP 12mm")
            cmds.append(f"_.-TEXT {cx - 600},{cy} 250 0 COT SAN: +0.450")

        elif "wc" in rtype or "ve_sinh" in rtype or "bath" in rtype:
            cmds.append(f"_.-TEXT {cx - 800},{cy + 400} 180 0 GACH CHONG TRUON 300x300")
            cmds.append(f"_.-TEXT {cx - 600},{cy} 220 0 COT SAN: +0.400 (HA COT 50mm)")
            # Slope arrow towards floor drain
            cmds.append(f"_.LINE {cx - 300},{cy - 300} {cx + 300},{cy - 300} ")
            cmds.append(f"_.LINE {cx + 300},{cy - 300} {cx + 150},{cy - 200} ")
            cmds.append(f"_.LINE {cx + 300},{cy - 300} {cx + 150},{cy - 400} ")
            cmds.append(f"_.-TEXT {cx - 200},{cy - 600} 140 0 DO DOC i = 1.5% -> THOAT SAN")

        elif "san" in rtype or "yard" in rtype:
            cmds.append(f"_.-TEXT {cx - 800},{cy + 300} 180 0 SAN GACH CO CHONG TRUON")
            cmds.append(f"_.-TEXT {cx - 500},{cy - 100} 220 0 COT SAN: +0.050")

    # Title Block
    cmds.extend(
        build_title_block_commands(
            ox, oy, "MẶT BẰNG ĐỊNH VỊ & ỐP LÁT SÀN", "KT-02", project_name
        )
    )
    return cmds


def build_furniture_layout_sheet_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """3. Mặt bằng bố trí nội thất & bảng thống kê (KT-03): Full furniture layout, item tags, space labels, schedule table."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; 3. SHEET KT-03: MAT BANG BO TRI NOI THAT",
        ";; ==========================================================================",
        "_.-LAYER _T KT_NOITHAT  ",
        "_.-LAYER _S KT_NOITHAT  ",
        "_.-LAYER _M KT_TAG_NOITHAT _C 4 KT_TAG_NOITHAT  ",
    ]

    # Furniture tags
    tag_y = oy + 1000
    cmds.append("_.-LAYER _S KT_TAG_NOITHAT  ")
    # Living room tag
    cmds.append(f"_.CIRCLE {ox + 800},{oy + 4500} 180")
    cmds.append(f"_.-TEXT {ox + 680},{oy + 4420} 160 0 SF1")
    # TV tag
    cmds.append(f"_.CIRCLE {ox + w - 800},{oy + 4500} 180")
    cmds.append(f"_.-TEXT {ox + w - 920},{oy + 4420} 160 0 TV1")
    # Dining tag
    cmds.append(f"_.CIRCLE {ox + w*0.5},{oy + l*0.7} 180")
    cmds.append(f"_.-TEXT {ox + w*0.5 - 120},{oy + l*0.7 - 80} 160 0 BA1")

    # Schedule Table for furniture beside title block
    tx = ox + w + 800
    ty = oy + l - 1000
    cmds.append(f"_.RECTANG {tx},{ty - 3500} {tx + 3000},{ty}")
    cmds.append(f"_.-TEXT {tx + 200},{ty - 400} 200 0 BANG THONG KE NOI THAT")
    cmds.append(f"_.LINE {tx},{ty - 600} {tx + 3000},{ty - 600} ")
    cmds.append(f"_.-TEXT {tx + 150},{ty - 1000} 160 0 SF1: Sofa bang 2.2m (1 bo)")
    cmds.append(f"_.-TEXT {tx + 150},{ty - 1400} 160 0 TV1: Ke TV phong khach (1 bo)")
    cmds.append(f"_.-TEXT {tx + 150},{ty - 1800} 160 0 BA1: Ban an 6 ghe (1 bo)")
    cmds.append(f"_.-TEXT {tx + 150},{ty - 2200} 160 0 BP1: Tu bep chu L (1 he)")

    # Title Block
    cmds.extend(
        build_title_block_commands(
            ox, oy, "MẶT BẰNG BỐ TRÍ NỘI THẤT", "KT-03", project_name
        )
    )
    return cmds


def build_door_schedule_sheet_commands(
    width_mm: float,
    length_mm: float,
    doors: List[Dict[str, Any]],
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """4. Mặt bằng định vị & phân loại cửa (KT-04): Opening widths, door tags (D1, D2, S1), sill/header height specs."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; 4. SHEET KT-04: MAT BANG DINH VI & PHAN LOAI CUA",
        ";; ==========================================================================",
        "_.-LAYER _F KT_NOITHAT  ",
        "_.-LAYER _M KT_TAG_CUA _C 3 KT_TAG_CUA  ",
        "_.-LAYER _M KT_BANG_CUA _C 7 KT_BANG_CUA  ",
    ]

    cmds.append("_.-LAYER _S KT_TAG_CUA  ")
    # Door Tags on Floor Plan
    # Main door tag (D1)
    cmds.append(f"_.CIRCLE {ox + w*0.5},{oy + 2500} 220")
    cmds.append(f"_.-TEXT {ox + w*0.5 - 120},{oy + 2420} 180 0 D1")

    # WC door tag (D2)
    cmds.append(f"_.CIRCLE {ox + w*0.7},{oy + l - 1500} 200")
    cmds.append(f"_.-TEXT {ox + w*0.7 - 100},{oy + l - 1580} 160 0 D2")

    # Window tag (S1)
    cmds.append(f"_.CIRCLE {ox + w*0.3},{oy + l} 200")
    cmds.append(f"_.-TEXT {ox + w*0.3 - 100},{oy + l - 80} 160 0 S1")

    # Door Specs Matrix Table (Bảng chỉ dẫn thông số kỹ thuật cửa)
    tx = ox + w + 800
    ty = oy + l - 500
    cmds.append("_.-LAYER _S KT_BANG_CUA  ")
    cmds.append(f"_.RECTANG {tx},{ty - 4500} {tx + 3600},{ty}")
    cmds.append(f"_.-TEXT {tx + 200},{ty - 400} 220 0 BANG CHI DAN THONG SO CUA")
    cmds.append(f"_.LINE {tx},{ty - 600} {tx + 3600},{ty - 600} ")

    cmds.append(f"_.-TEXT {tx + 100},{ty - 1000} 160 0 D1: 2800x2600 (4C, Bau 0.0, Lanh-to +2.6)")
    cmds.append(f"_.-TEXT {tx + 100},{ty - 1500} 160 0 D2: 800x2200 (1C WC, Bau 0.0, Lanh-to +2.2)")
    cmds.append(f"_.-TEXT {tx + 100},{ty - 2000} 160 0 D3: 900x2200 (1C P.Ngu, Bau 0.0, Lanh-to +2.2)")
    cmds.append(f"_.-TEXT {tx + 100},{ty - 2500} 160 0 S1: 1600x1400 (2C, Bau +0.9, Lanh-to +2.3)")
    cmds.append(f"_.-TEXT {tx + 100},{ty - 3000} 160 0 S2: 1200x1400 (2C, Bau +0.9, Lanh-to +2.3)")
    cmds.append(f"_.-TEXT {tx + 100},{ty - 3800} 150 0 * VẬT LIỆU: NHÔM XINGFA NHẬP KHẨU")

    # Title Block
    cmds.extend(
        build_title_block_commands(
            ox, oy, "MẶT BẰNG ĐỊNH VỊ & PHÂN LOẠI CỬA", "KT-04", project_name
        )
    )
    return cmds


def build_finalized_sheets_commands(
    sheet_type: str,
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """
    Generate construction documentation sheets based on sheet_type:
    - 'wall_construction': KT-01 Masonry dimensions
    - 'floor_finishes': KT-02 Floor tiling, elevations, slope, start point
    - 'furniture_layout': KT-03 Furniture layout & schedule
    - 'door_window_schedule': KT-04 Door tags & opening specs
    - 'all': Generates all 4 sheets arranged horizontally side-by-side!
    """
    stype = sheet_type.lower().strip()
    cmds = []

    if stype == "wall_construction":
        cmds = build_wall_construction_sheet_commands(
            width_mm, length_mm, rooms, origin_x, origin_y, project_name
        )
    elif stype == "floor_finishes":
        cmds = build_floor_finishes_sheet_commands(
            width_mm, length_mm, rooms, origin_x, origin_y, project_name
        )
    elif stype == "furniture_layout":
        cmds = build_furniture_layout_sheet_commands(
            width_mm, length_mm, rooms, origin_x, origin_y, project_name
        )
    elif stype in ("door_window_schedule", "doors"):
        cmds = build_door_schedule_sheet_commands(
            width_mm, length_mm, [], origin_x, origin_y, project_name
        )
    elif stype in ("all", "full_set"):
        # Generate all 4 sheets side-by-side with 18000mm spacing
        spacing_x = width_mm + 12000.0
        cmds.extend(
            build_wall_construction_sheet_commands(
                width_mm, length_mm, rooms, origin_x, origin_y, project_name
            )
        )
        cmds.extend(
            build_floor_finishes_sheet_commands(
                width_mm, length_mm, rooms, origin_x + spacing_x, origin_y, project_name
            )
        )
        cmds.extend(
            build_furniture_layout_sheet_commands(
                width_mm,
                length_mm,
                rooms,
                origin_x + spacing_x * 2,
                origin_y,
                project_name,
            )
        )
        cmds.extend(
            build_door_schedule_sheet_commands(
                width_mm,
                length_mm,
                [],
                origin_x + spacing_x * 3,
                origin_y,
                project_name,
            )
        )
    else:
        cmds = build_wall_construction_sheet_commands(
            width_mm, length_mm, rooms, origin_x, origin_y, project_name
        )

    cmds.append("_.ZOOM _E")
    return cmds
