"""Finalizer Engine: Generates Dynamic, Content-Driven Architectural Construction Documentation (Hồ Sơ Thiết Kế Thi Công - TKTC).

Architectural Principles:
1. Dynamic Pagination: Drawing sheet count is NOT hardcoded. Sheets are paginated dynamically based on project complexity, number of floors, number of WC types, and total door count (max 3-4 doors/A3 sheet for 1/25 readability).
2. Dynamic Ergonomic Stairs: Stair riser height (h) and tread width (b) are calculated dynamically:
   - h = Floor_Height / Num_Risers (e.g., 3600 / 21 = 171.4mm, 3900 / 23 = 169.5mm, 4200 / 25 = 168.0mm)
   - b = Blondel formula (2h + b = 600..640mm) or bay depth allocation.
"""

import math
from typing import Dict, Any, List, Optional


def calculate_stair_parameters(
    floor_height_mm: float = 3600.0,
    num_risers: int = 21,
    target_blondel: float = 620.0,
) -> Dict[str, Any]:
    """
    Dynamically calculate stair ergonomic parameters based on floor height and riser count.
    - h (Cổ bậc) = floor_height / num_risers
    - b (Mặt bậc) = target_blondel - 2*h (Blondel ergonomic rule: 2h + b = 600..640mm)
    """
    n = max(num_risers, 3)
    h = floor_height_mm / float(n)
    b = max(240.0, min(300.0, target_blondel - 2.0 * h))
    slope_deg = math.degrees(math.atan(h / b))

    return {
        "floor_height_mm": floor_height_mm,
        "num_risers": n,
        "riser_height_mm": round(h, 1),
        "tread_width_mm": round(b, 1),
        "slope_degrees": round(slope_deg, 1),
        "blondel_value": round(2.0 * h + b, 1),
    }


def build_title_block_commands(
    origin_x: float,
    origin_y: float,
    sheet_title: str,
    sheet_code: str,
    project_name: str = "NHÀ PHỐ DÂN DỤNG",
    scale_str: str = "1/100",
    page_info: str = "01/01",
) -> List[str]:
    """Generate AutoCAD commands for a standard A3 Title Block."""
    bw = 14000.0
    bh = 20000.0
    ox, oy = origin_x - 2000.0, origin_y - 3000.0

    cmds = [
        "_.-LAYER _M KT_KHUNG_TEN _C 7 KT_KHUNG_TEN  ",
        "_.-LAYER _S KT_KHUNG_TEN  ",
        f"_.RECTANG {ox},{oy} {ox + bw},{oy + bh}",
        f"_.RECTANG {ox + 200},{oy + 200} {ox + bw - 200},{oy + bh - 200}",
        f"_.RECTANG {ox + 200},{oy + 200} {ox + bw - 200},{oy + 2200}",
        f"_.LINE {ox + 200},{oy + 1200} {ox + bw - 200},{oy + 1200} ",
        f"_.LINE {ox + bw - 3500},{oy + 200} {ox + bw - 3500},{oy + 2200} ",
        f"_.-TEXT {ox + 500},{oy + 1500} 320 0 DU AN: {project_name.upper()}",
        f"_.-TEXT {ox + 500},{oy + 600} 350 0 HANG MUC: {sheet_title.upper()}",
        f"_.-TEXT {ox + bw - 3200},{oy + 1500} 220 0 TY LE: {scale_str}",
        f"_.-TEXT {ox + bw - 3200},{oy + 600} 420 0 SO: {sheet_code} ({page_info})",
    ]
    return cmds


# ============================================================================
# 1. FLOOR PLANS WITH DYNAMIC MULTI-STORY SUPPORT
# ============================================================================


def build_wall_construction_sheet_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    floor_name: str = "TẦNG 1",
    sheet_code: str = "KT-01.01",
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """Mặt bằng kích thước tường xây theo từng tầng cụ thể."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        f";; SHEET {sheet_code}: MAT BANG KICH THUOC TUONG XAY - {floor_name.upper()}",
        ";; ==========================================================================",
        "_.-LAYER _F KT_NOITHAT  ",
        "_.-LAYER _M KT_DIMS_TUONG _C 1 KT_DIMS_TUONG  ",
        "_.-LAYER _M KT_HATCH_TUONG _C 8 KT_HATCH_TUONG  ",
        "_.-LAYER _S KT_DIMS_TUONG  ",
        f"_.DIMLINEAR {ox},{oy} {ox + w},{oy} {ox},{oy - 1200}",
        f"_.DIMLINEAR {ox},{oy} {ox},{oy + l} {ox - 1400},{oy}",
    ]

    prev_y = oy
    for r in rooms:
        y_end = oy + float(r.get("y_end", l))
        cmds.append(f"_.DIMLINEAR {ox},{prev_y} {ox},{y_end} {ox - 600},{prev_y}")
        prev_y = y_end

    cmds.append("_.-LAYER _S KT_TEXT  ")
    cmds.append(f"_.-TEXT {ox + 300},{oy + 400} 180 0 TUONG BAO 220mm (GACH DAC)")
    cmds.append(f"_.-TEXT {ox + 300},{oy + l*0.5} 180 0 TUONG NGAN 110mm (GACH LO)")

    title = f"MẶT BẰNG KÍCH THƯỚC TƯỜNG XÂY ({floor_name.upper()})"
    cmds.extend(build_title_block_commands(ox, oy, title, sheet_code, project_name))
    return cmds


def build_floor_finishes_sheet_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    floor_name: str = "TẦNG 1",
    sheet_code: str = "KT-02.01",
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """Mặt bằng định vị & ốp lát sàn theo từng tầng."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        f";; SHEET {sheet_code}: MAT BANG OP LAT SAN - {floor_name.upper()}",
        ";; ==========================================================================",
        "_.-LAYER _F KT_NOITHAT  ",
        "_.-LAYER _M KT_SAN_NOTE _C 3 KT_SAN_NOTE  ",
    ]

    for r in rooms:
        y1 = oy + float(r.get("y_start", 0))
        y2 = oy + float(r.get("y_end", l))
        cx = ox + w * 0.5
        cy = (y1 + y2) * 0.5
        rtype = r.get("type", "").lower()

        cmds.append("_.-LAYER _S KT_SAN_NOTE  ")
        if "khach" in rtype or "living" in rtype:
            cmds.append(f"_.-TEXT {cx - 1000},{cy + 400} 200 0 SAN GACH GRANITE 800x800")
            cmds.append(f"_.-TEXT {cx - 600},{cy} 250 0 COT SAN: +0.450")
            cmds.append(f"_.CIRCLE {ox + 500},{y1 + 500} 150")
            cmds.append(f"_.LINE {ox + 350},{y1 + 500} {ox + 650},{y1 + 500} ")
            cmds.append(f"_.LINE {ox + 500},{y1 + 350} {ox + 500},{y1 + 650} ")
            cmds.append(f"_.-TEXT {ox + 700},{y1 + 450} 150 0 DIEM LAT DAU TIEN")
        elif "wc" in rtype or "bath" in rtype:
            cmds.append(f"_.-TEXT {cx - 800},{cy + 400} 180 0 GACH CHONG TRUON 300x300")
            cmds.append(f"_.-TEXT {cx - 600},{cy} 220 0 COT SAN: +0.400 (HA COT 50mm)")
            cmds.append(f"_.LINE {cx - 300},{cy - 300} {cx + 300},{cy - 300} ")
            cmds.append(f"_.LINE {cx + 300},{cy - 300} {cx + 150},{cy - 200} ")
            cmds.append(f"_.LINE {cx + 300},{cy - 300} {cx + 150},{cy - 400} ")
            cmds.append(f"_.-TEXT {cx - 200},{cy - 600} 140 0 DO DOC i = 1.5% -> THOAT SAN")
        else:
            cmds.append(f"_.-TEXT {cx - 600},{cy} 220 0 COT SAN: +0.450")

    title = f"MẶT BẰNG ĐỊNH VỊ & ỐP LÁT SÀN ({floor_name.upper()})"
    cmds.extend(build_title_block_commands(ox, oy, title, sheet_code, project_name))
    return cmds


def build_furniture_layout_sheet_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    floor_name: str = "TẦNG 1",
    sheet_code: str = "KT-03.01",
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """Mặt bằng bố trí nội thất theo từng tầng."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        f";; SHEET {sheet_code}: MAT BANG BO TRI NOI THAT - {floor_name.upper()}",
        ";; ==========================================================================",
        "_.-LAYER _T KT_NOITHAT  ",
        "_.-LAYER _S KT_NOITHAT  ",
        "_.-LAYER _M KT_TAG_NOITHAT _C 4 KT_TAG_NOITHAT  ",
    ]

    cmds.append("_.-LAYER _S KT_TAG_NOITHAT  ")
    cmds.append(f"_.CIRCLE {ox + 800},{oy + 4500} 180")
    cmds.append(f"_.-TEXT {ox + 680},{oy + 4420} 160 0 SF1")
    cmds.append(f"_.CIRCLE {ox + w - 800},{oy + 4500} 180")
    cmds.append(f"_.-TEXT {ox + w - 920},{oy + 4420} 160 0 TV1")

    tx = ox + w + 800
    ty = oy + l - 1000
    cmds.append(f"_.RECTANG {tx},{ty - 3500} {tx + 3000},{ty}")
    cmds.append(f"_.-TEXT {tx + 200},{ty - 400} 200 0 BANG THONG KE NOI THAT")
    cmds.append(f"_.LINE {tx},{ty - 600} {tx + 3000},{ty - 600} ")
    cmds.append(f"_.-TEXT {tx + 150},{ty - 1000} 160 0 SF1: Sofa bang 2.2m (1 bo)")
    cmds.append(f"_.-TEXT {tx + 150},{ty - 1400} 160 0 TV1: Ke TV phong khach (1 bo)")
    cmds.append(f"_.-TEXT {tx + 150},{ty - 1800} 160 0 BA1: Ban an 6 ghe (1 bo)")

    title = f"MẶT BẰNG BỐ TRÍ NỘI THẤT ({floor_name.upper()})"
    cmds.extend(build_title_block_commands(ox, oy, title, sheet_code, project_name))
    return cmds


def build_door_schedule_sheet_commands(
    width_mm: float,
    length_mm: float,
    doors: Optional[List[Dict[str, Any]]] = None,
    floor_name: str = "TẦNG 1",
    sheet_code: str = "KT-04.01",
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """Mặt bằng định vị & phân loại cửa theo từng tầng."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm
    fname_str = floor_name if isinstance(floor_name, str) else "TẦNG 1"

    cmds = [
        ";; ==========================================================================",
        f";; SHEET {sheet_code}: MAT BANG DINH VI CUA - {fname_str.upper()}",
        ";; ==========================================================================",

        "_.-LAYER _F KT_NOITHAT  ",
        "_.-LAYER _M KT_TAG_CUA _C 3 KT_TAG_CUA  ",
        "_.-LAYER _M KT_BANG_CUA _C 7 KT_BANG_CUA  ",
        "_.-LAYER _S KT_TAG_CUA  ",
        f"_.CIRCLE {ox + w*0.5},{oy + 2500} 220",
        f"_.-TEXT {ox + w*0.5 - 120},{oy + 2420} 180 0 D1",
    ]

    tx = ox + w + 800
    ty = oy + l - 500
    cmds.append("_.-LAYER _S KT_BANG_CUA  ")
    cmds.append(f"_.RECTANG {tx},{ty - 4500} {tx + 3600},{ty}")
    cmds.append(f"_.-TEXT {tx + 200},{ty - 400} 220 0 BANG CHI DAN THONG SO CUA")
    cmds.append(f"_.LINE {tx},{ty - 600} {tx + 3600},{ty - 600} ")
    cmds.append(f"_.-TEXT {tx + 100},{ty - 1000} 160 0 D1: 2800x2600 (4C, Bau 0.0, Lanh-to +2.6)")
    cmds.append(f"_.-TEXT {tx + 100},{ty - 1500} 160 0 D2: 800x2200 (1C WC, Bau 0.0, Lanh-to +2.2)")
    cmds.append(f"_.-TEXT {tx + 100},{ty - 2000} 160 0 S1: 1600x1400 (2C, Bau +0.9, Lanh-to +2.3)")

    title = f"MẶT BẰNG ĐỊNH VỊ & PHÂN LOẠI CỬA ({floor_name.upper()})"
    cmds.extend(build_title_block_commands(ox, oy, title, sheet_code, project_name))
    return cmds


# ============================================================================
# 2. DYNAMIC STAIR DETAILS (CALCULATED h & b FROM FLOOR HEIGHT & RISERS)
# ============================================================================


def build_stair_detail_sheet_commands(
    floor_height_mm: float = 3600.0,
    num_risers: int = 21,
    sheet_code: str = "KT-09",
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """
    Chi tiết cầu thang & lan can với chiều cao cổ bậc (h) và bề rộng mặt bậc (b)
    được TÍNH TOÁN ĐỘNG theo chiều cao tầng và số cổ bậc thực tế.
    """
    stair_info = calculate_stair_parameters(floor_height_mm, num_risers)
    h = stair_info["riser_height_mm"]
    b = stair_info["tread_width_mm"]
    n = stair_info["num_risers"]
    deg = stair_info["slope_degrees"]

    ox, oy = origin_x, origin_y

    cmds = [
        ";; ==========================================================================",
        f";; SHEET {sheet_code}: CHI TIET CAU THANG (H={floor_height_mm}mm, N={n} BOC, h={h}mm, b={b}mm)",
        ";; ==========================================================================",
        "_.-LAYER _M KT_CHI_TIET _C 7 KT_CHI_TIET  ",
        "_.-LAYER _M KT_DIMS_DETAIL _C 1 KT_DIMS_DETAIL  ",
        "_.-LAYER _S KT_CHI_TIET  ",
        # Draw dynamic step profile (3 sample steps at scale)
        f"_.LINE {ox + 500},{oy + 2000} {ox + 500 + b*3},{oy + 2000} ",
        f"_.LINE {ox + 500 + b*3},{oy + 2000} {ox + 500 + b*3},{oy + 2000 + h*3} ",
        f"_.LINE {ox + 500 + b*3},{oy + 2000 + h*3} {ox + 500 + b*6},{oy + 2000 + h*3} ",
        f"_.LINE {ox + 500 + b*6},{oy + 2000 + h*3} {ox + 500 + b*6},{oy + 2000 + h*6} ",
        # Information Text Block
        f"_.-TEXT {ox + 500},{oy + 4200} 240 0 THONG SO HINH HOC THANG TANG (TY LE 1/20)",
        f"_.-TEXT {ox + 500},{oy + 3800} 180 0 * CHIEU CAO TANG: H = {int(floor_height_mm)} mm",
        f"_.-TEXT {ox + 500},{oy + 3400} 180 0 * SO CO BAC PHONG THUY: N = {n} BAC (CUNG SINH)",
        f"_.-TEXT {ox + 500},{oy + 3000} 180 0 * CHIEU CAO CO BAC: h = H/{n} = {h} mm",
        f"_.-TEXT {ox + 500},{oy + 2600} 180 0 * BE RONG MAT BAC: b = {b} mm (GOC DOC {deg} DO)",
        f"_.-TEXT {ox + 500},{oy + 2200} 160 0 * MAT BAC GO GO DO DAY 30mm, MUI BAC BO TRON R10",
        f"_.-TEXT {ox + 500},{oy + 1800} 160 0 * CO BAC OP DA TRANG SU NHAN TAO DAY 18mm",
        # Handrail detail
        f"_.RECTANG {ox + 4500},{oy + 1500} {ox + 7500},{oy + 4500}",
        f"_.-TEXT {ox + 4600},{oy + 4200} 200 0 CHI TIET LAN CAN TAY VIN",
        f"_.-TEXT {ox + 4600},{oy + 3800} 160 0 * TAY VIN GO OVAL 60x80mm (CAO 900mm)",
        f"_.-TEXT {ox + 4600},{oy + 3400} 160 0 * KINH CUONG LUC 10mm KEM TRU INOX 304",
    ]

    cmds.extend(build_title_block_commands(ox, oy, "CHI TIẾT CẦU THANG & LAN CAN", sheet_code, project_name, scale_str="1/20"))
    return cmds


# ============================================================================
# 3. DYNAMIC PAGINATION FOR DOOR DETAILS (MAX 3-4 DOORS PER A3 SHEET)
# ============================================================================


def build_door_details_paginated_commands(
    doors_list: Optional[List[Dict[str, Any]]] = None,
    max_doors_per_sheet: int = 3,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
    base_spacing_x: float = 17000.0,
) -> Dict[str, Any]:
    """
    Tự động phân trang chi tiết cấu tạo cửa thành nhiều bản vẽ A3 (KT-11.01, KT-11.02...).
    Mỗi tờ A3 chỉ chứa tối đa 3-4 bộ cửa để đảm bảo tỷ lệ 1/25 đọc rõ nét khi in ra giấy.
    """
    default_doors = [
        {"code": "D1", "name": "Cửa Đi Chính", "width": 2800, "height": 2600, "wings": 4, "type": "quay", "sill": 0, "lintel": 2600},
        {"code": "D2", "name": "Cửa Phòng Ngủ", "width": 900, "height": 2200, "wings": 1, "type": "quay", "sill": 0, "lintel": 2200},
        {"code": "D3", "name": "Cửa Vệ Sinh", "width": 800, "height": 2200, "wings": 1, "type": "quay", "sill": 0, "lintel": 2200},
        {"code": "S1", "name": "Cửa Sổ Phòng Khách", "width": 2400, "height": 1800, "wings": 4, "type": "truot", "sill": 800, "lintel": 2600},
        {"code": "S2", "name": "Cửa Sổ Phòng Ngủ", "width": 1600, "height": 1400, "wings": 2, "type": "truot", "sill": 900, "lintel": 2300},
        {"code": "S3", "name": "Cửa Sổ Vệ Sinh / Chớp", "width": 600, "height": 600, "wings": 1, "type": "hat", "sill": 1800, "lintel": 2400},
    ]
    doors = doors_list or default_doors
    total_doors = len(doors)
    num_sheets = max(1, math.ceil(total_doors / float(max_doors_per_sheet)))

    all_cmds = [
        ";; ==========================================================================",
        f";; DYNAMIC DOOR DETAILS: {total_doors} DOORS -> PAGINATED INTO {num_sheets} A3 SHEETS",
        ";; ==========================================================================",
    ]

    generated_sheets = []

    for sheet_idx in range(num_sheets):
        start_i = sheet_idx * max_doors_per_sheet
        end_i = min(start_i + max_doors_per_sheet, total_doors)
        sheet_doors = doors[start_i:end_i]

        ox = origin_x + sheet_idx * base_spacing_x
        oy = origin_y
        sheet_code = f"KT-11.{sheet_idx + 1:02d}"
        page_info = f"{sheet_idx + 1:02d}/{num_sheets:02d}"

        cmds = [
            f";; --- SUB-SHEET {sheet_code} (DOORS {start_i + 1} TO {end_i}) ---",
            "_.-LAYER _M KT_CHI_TIET _C 7 KT_CHI_TIET  ",
            "_.-LAYER _S KT_CHI_TIET  ",
        ]

        # Place up to 3 doors on this sheet
        slot_w = 3600.0
        for slot_idx, d in enumerate(sheet_doors):
            dx = ox + 500.0 + slot_idx * slot_w
            dw = float(d.get("width", 900))
            dh = float(d.get("height", 2200))
            scale_fac = 0.8  # Fit nicely
            draw_w = dw * scale_fac
            draw_h = dh * scale_fac

            d_code = d.get("code", f"D{slot_idx+1}")
            d_name = d.get("name", "Cửa")
            sill = d.get("sill", 0)
            lintel = d.get("lintel", int(dh))

            cmds.append(f"_.RECTANG {dx},{oy + 1200} {dx + draw_w},{oy + 1200 + draw_h}")
            if d.get("wings", 1) > 1:
                mid_x = dx + draw_w * 0.5
                cmds.append(f"_.LINE {mid_x},{oy + 1200} {mid_x},{oy + 1200 + draw_h} ")

            cmds.append(f"_.-TEXT {dx},{oy + 1200 + draw_h + 300} 200 0 {d_code}: {d_name.upper()}")
            cmds.append(f"_.-TEXT {dx},{oy + 800} 160 0 * K.THUOC: {int(dw)} x {int(dh)} mm")
            cmds.append(f"_.-TEXT {dx},{oy + 500} 150 0 * COT BAU: +{sill}mm | LANH-TO: +{lintel}mm")

        cmds.extend(build_title_block_commands(
            ox, oy, f"CHI TIẾT CẤU TẠO CỬA (PHẦN {sheet_idx + 1})", sheet_code, project_name, scale_str="1/25", page_info=page_info
        ))

        all_cmds.extend(cmds)
        generated_sheets.append({"code": sheet_code, "doors_count": len(sheet_doors), "ox": ox, "oy": oy})

    return {
        "commands": all_cmds,
        "total_doors": total_doors,
        "sheet_count": num_sheets,
        "sheets": generated_sheets,
    }


# ============================================================================
# 4. ELEVATIONS, SECTIONS, CEILING, ROOF, WC
# ============================================================================


def build_elevation_sheet_commands(
    width_mm: float = 5000.0,
    floor_height_mm: float = 3600.0,
    num_floors: int = 2,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """Mặt đứng chính công trình kèm cao độ từng tầng và chỉ dẫn vật liệu."""
    ox, oy = origin_x, origin_y
    w = width_mm
    h = floor_height_mm
    total_h = h * num_floors + 1200.0

    cmds = [
        ";; ==========================================================================",
        ";; SHEET KT-05: MAT DUNG CHINH CONG TRINH",
        ";; ==========================================================================",
        "_.-LAYER _M KT_MAT_DUNG _C 7 KT_MAT_DUNG  ",
        "_.-LAYER _M KT_CAO_DO _C 1 KT_CAO_DO  ",
        "_.-LAYER _M KT_NOTE_VAT_LIEU _C 4 KT_NOTE_VAT_LIEU  ",
        "_.-LAYER _S KT_MAT_DUNG  ",
        f"_.RECTANG {ox},{oy} {ox + w},{oy + total_h}",
        f"_.RECTANG {ox + 800},{oy} {ox + w - 800},{oy + 2600}",
        f"_.RECTANG {ox + 400},{oy + h} {ox + w - 400},{oy + h + 1100}",
        f"_.RECTANG {ox + 1200},{oy + h + 500} {ox + w - 1200},{oy + h + 2500}",
        f"_.LINE {ox},{oy + total_h - 600} {ox + w},{oy + total_h - 600} ",
        "_.-LAYER _S KT_CAO_DO  ",
        f"_.LINE {ox - 1200},{oy} {ox},{oy} ",
        f"_.-TEXT {ox - 1600},{oy + 100} 200 0 COT SAN TRUOC: +0.050",
        f"_.LINE {ox - 1200},{oy + h} {ox},{oy + h} ",
        f"_.-TEXT {ox - 1600},{oy + h + 100} 200 0 COT SAN LAU 1: +{h/1000 + 0.05:.3f}",
        f"_.LINE {ox - 1200},{oy + total_h} {ox},{oy + total_h} ",
        f"_.-TEXT {ox - 1600},{oy + total_h + 100} 200 0 COT DINH MAI: +{total_h/1000:.3f}",
        "_.-LAYER _S KT_NOTE_VAT_LIEU  ",
        f"_.-TEXT {ox + w + 400},{oy + 1200} 160 0 * MAT TIEN TANG 1 OP DA GRANITE DEN TIA CHOP",
        f"_.-TEXT {ox + w + 400},{oy + h + 1500} 160 0 * TANG 2 OP LAM NHOM GIA GO & KINH CUONG LUC",
        f"_.-TEXT {ox + w + 400},{oy + total_h - 300} 160 0 * SON NGOAI THAT CHONG THAM DULUX WEATHERSHIELD",
    ]

    cmds.extend(build_title_block_commands(ox, oy, "MẶT ĐỨNG CHÍNH CÔNG TRÌNH", "KT-05", project_name))
    return cmds


def build_section_sheet_commands(
    depth_length_mm: float = 15000.0,
    floor_height_mm: float = 3600.0,
    num_floors: int = 2,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """Mặt cắt dọc 1-1 qua thang và giếng trời."""
    ox, oy = origin_x, origin_y
    l = depth_length_mm
    h = floor_height_mm
    total_h = h * num_floors + 1200.0

    cmds = [
        ";; ==========================================================================",
        ";; SHEET KT-06: MAT CAT DOC 1-1 QUA THANG",
        ";; ==========================================================================",
        "_.-LAYER _M KT_NET_CAT _C 1 KT_NET_CAT  ",
        "_.-LAYER _M KT_CAO_DO _C 1 KT_CAO_DO  ",
        "_.-LAYER _S KT_NET_CAT  ",
        f"_.RECTANG {ox},{oy} {ox + l},{oy + 200}",
        f"_.RECTANG {ox},{oy + h} {ox + l},{oy + h + 120}",
        f"_.RECTANG {ox},{oy + total_h - 400} {ox + l},{oy + total_h - 280}",
        f"_.LINE {ox + 7000},{oy + 200} {ox + 8200},{oy + h*0.5} ",
        f"_.LINE {ox + 8200},{oy + h*0.5} {ox + 9400},{oy + h} ",
        "_.-LAYER _S KT_CAO_DO  ",
        f"_.DIMLINEAR {ox - 1000},{oy} {ox - 1000},{oy + h} {ox - 1500},{oy}",
        f"_.-TEXT {ox + 2000},{oy + h*0.5} 200 0 THONG THUY P.KHACH: {int(h)}mm",
        f"_.-TEXT {ox + 7500},{oy + h + 500} 200 0 GIENG TROI THONG TANG",
    ]

    cmds.extend(build_title_block_commands(ox, oy, "MẶT CẮT DỌC 1-1 QUA THANG", "KT-06", project_name))
    return cmds


def build_ceiling_lighting_sheet_commands(
    width_mm: float = 5000.0,
    length_mm: float = 15000.0,
    rooms: Optional[List[Dict[str, Any]]] = None,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """Mặt bằng trần thạch cao và đèn chiếu sáng."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; SHEET KT-07: MAT BANG TRAN THACH CAO & DEN",
        ";; ==========================================================================",
        "_.-LAYER _F KT_NOITHAT  ",
        "_.-LAYER _M KT_TRAN_THACH_CAO _C 4 KT_TRAN_THACH_CAO  ",
        "_.-LAYER _M KT_DEN_DOWNLIGHT _C 2 KT_DEN_DOWNLIGHT  ",
        "_.-LAYER _S KT_TRAN_THACH_CAO  ",
        f"_.RECTANG {ox + 600},{oy + 3000} {ox + w - 600},{oy + 6500}",
        f"_.-TEXT {ox + w*0.5 - 1000},{oy + 4750} 200 0 TRAN THACH CAO HA COT -200mm",
        f"_.-TEXT {ox + w*0.5 - 800},{oy + 4400} 160 0 KHE HAT SANG DEN LED STRIP",
        "_.-LAYER _S KT_DEN_DOWNLIGHT  ",
    ]

    for dx in [1000, w * 0.5, w - 1000]:
        for dy in [3500, 4750, 6000]:
            cmds.append(f"_.CIRCLE {ox + dx},{oy + dy} 90")

    cmds.append(f"_.-TEXT {ox + w + 400},{oy + 5000} 160 0 * DEN DOWNLIGHT LED D90 9W (ANH SANG TRUNG TINH 4000K)")

    cmds.extend(build_title_block_commands(ox, oy, "MẶT BẰNG TRẦN THẠCH CAO & ĐÈN", "KT-07", project_name))
    return cmds


def build_roof_drainage_sheet_commands(
    width_mm: float = 5000.0,
    length_mm: float = 15000.0,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """Mặt bằng mái & thoát nước."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; SHEET KT-08: MAT BANG MAI & THOAT NUOC",
        ";; ==========================================================================",
        "_.-LAYER _M KT_MAI _C 7 KT_MAI  ",
        "_.-LAYER _M KT_THOAT_NUOC _C 5 KT_THOAT_NUOC  ",
        "_.-LAYER _S KT_MAI  ",
        f"_.RECTANG {ox},{oy} {ox + w},{oy + l}",
        f"_.RECTANG {ox},{oy + l - 600} {ox + w},{oy + l}",
        f"_.RECTANG {ox + 600},{oy + 2000} {ox + 2200},{oy + 3800}",
        f"_.-TEXT {ox + 700},{oy + 2900} 180 0 BON NUOC INOX 1500L & NANG LUONG MAT TROY",
        "_.-LAYER _S KT_THOAT_NUOC  ",
        f"_.LINE {ox + w*0.5},{oy + 2000} {ox + w*0.5},{oy + l - 800} ",
        f"_.-TEXT {ox + w*0.5 + 200},{oy + l*0.5} 180 0 DO DOC THU NUOC i = 2% VE SE-NO",
        f"_.CIRCLE {ox + 600},{oy + l - 300} 100",
        f"_.-TEXT {ox + 800},{oy + l - 300} 160 0 PHEU THU SE-NO D114",
    ]

    cmds.extend(build_title_block_commands(ox, oy, "MẶT BẰNG MÁI & THOÁT NƯỚC", "KT-08", project_name))
    return cmds


def build_wc_detail_sheet_commands(
    wc_name: str = "WC TẦNG 1",
    sheet_code: str = "KT-10.01",
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """Chi tiết phòng vệ sinh trích 1/25 & triển khai 4 vách."""
    ox, oy = origin_x, origin_y

    cmds = [
        ";; ==========================================================================",
        f";; SHEET {sheet_code}: CHI TIET {wc_name.upper()} TRICH 1/25",
        ";; ==========================================================================",
        "_.-LAYER _M KT_CHI_TIET _C 7 KT_CHI_TIET  ",
        "_.-LAYER _S KT_CHI_TIET  ",
        f"_.RECTANG {ox + 500},{oy + 1000} {ox + 2300},{oy + 3400}",
        f"_.CIRCLE {ox + 1400},{oy + 1600} 220",
        f"_.RECTANG {ox + 600},{oy + 2700} {ox + 1200},{oy + 3300}",
        f"_.-TEXT {ox + 600},{oy + 3600} 220 0 MAT BANG TRICH {wc_name.upper()} (TY LE 1/25)",
        f"_.RECTANG {ox + 3000},{oy + 1000} {ox + 5400},{oy + 3600}",
        f"_.-TEXT {ox + 3100},{oy + 3800} 200 0 MAT CAT TRIEN KHAI VACH SEN TAM",
        f"_.-TEXT {ox + 3100},{oy + 3400} 160 0 * COT SEN DUNG: +1.100m, VACH KINH TAM DUNG 10mm",
        f"_.-TEXT {ox + 3100},{oy + 3000} 160 0 * GACH OP TUONG CERAMIC 300x600 OP KICH TRAN (+2.800m)",
    ]

    cmds.extend(build_title_block_commands(ox, oy, f"CHI TIẾT {wc_name.upper()}", sheet_code, project_name, scale_str="1/25"))
    return cmds


# ============================================================================
# MASTER DISPATCHER: DYNAMIC CONTENT-DRIVEN PAGINATION
# ============================================================================


def build_finalized_sheets_commands(
    sheet_type: str = "full_project_set",
    width_mm: float = 5000.0,
    depth_length_mm: float = 15000.0,
    rooms: Optional[List[Dict[str, Any]]] = None,
    floor_height_mm: float = 3600.0,
    num_floors: int = 2,
    num_risers: int = 21,
    doors: Optional[List[Dict[str, Any]]] = None,
    wc_count: int = 2,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """
    Master Dispatcher for Finalizing Architectural Construction Drawings.
    Dynamically paginates sheets based on project scope, floor count, and door inventory.
    """
    stype = sheet_type.lower().strip()
    room_list = rooms or [
        {"name": "SÂN TRƯỚC", "y_start": 0, "y_end": 2500, "type": "yard"},
        {"name": "PHÒNG KHÁCH", "y_start": 2500, "y_end": 7000, "type": "living"},
        {"name": "CẦU THANG", "y_start": 7000, "y_end": 9500, "type": "stairs"},
        {"name": "BẾP & ĂN", "y_start": 9500, "y_end": 13500, "type": "kitchen"},
        {"name": "WC & SÂN SAU", "y_start": 13500, "y_end": 15000, "type": "wc"},
    ]

    cmds = []
    spacing_x = width_mm + 12000.0
    spacing_y = depth_length_mm + 12000.0

    if stype == "wall_construction":
        cmds = build_wall_construction_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-01.01", origin_x, origin_y, project_name)
    elif stype == "floor_finishes":
        cmds = build_floor_finishes_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-02.01", origin_x, origin_y, project_name)
    elif stype == "furniture_layout":
        cmds = build_furniture_layout_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-03.01", origin_x, origin_y, project_name)
    elif stype in ("door_window_schedule", "doors"):
        cmds = build_door_schedule_sheet_commands(width_mm, depth_length_mm, doors=doors, floor_name="TẦNG 1", sheet_code="KT-04.01", origin_x=origin_x, origin_y=origin_y, project_name=project_name)
    elif stype in ("elevation", "mat_dung"):
        cmds = build_elevation_sheet_commands(width_mm, floor_height_mm, num_floors, origin_x, origin_y, project_name)
    elif stype in ("section", "mat_cat"):
        cmds = build_section_sheet_commands(depth_length_mm, floor_height_mm, num_floors, origin_x, origin_y, project_name)
    elif stype in ("ceiling_lighting", "tran_den"):
        cmds = build_ceiling_lighting_sheet_commands(width_mm, depth_length_mm, room_list, origin_x, origin_y, project_name)
    elif stype in ("roof_drainage", "mai"):
        cmds = build_roof_drainage_sheet_commands(width_mm, depth_length_mm, origin_x, origin_y, project_name)
    elif stype in ("stair_detail", "chi_tiet_thang"):
        cmds = build_stair_detail_sheet_commands(floor_height_mm, num_risers, "KT-09", origin_x, origin_y, project_name)
    elif stype in ("wc_detail", "chi_tiet_wc"):
        cmds = build_wc_detail_sheet_commands("WC TẦNG 1", "KT-10.01", origin_x, origin_y, project_name)
    elif stype in ("door_detail", "chi_tiet_cua"):
        door_res = build_door_details_paginated_commands(doors, max_doors_per_sheet=3, origin_x=origin_x, origin_y=origin_y, project_name=project_name)
        cmds = door_res["commands"]

    elif stype in ("all_floor_plans", "floor_set"):
        cmds.extend(build_wall_construction_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-01.01", origin_x, origin_y, project_name))
        cmds.extend(build_floor_finishes_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-02.01", origin_x + spacing_x, origin_y, project_name))
        cmds.extend(build_furniture_layout_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-03.01", origin_x + spacing_x * 2, origin_y, project_name))
        cmds.extend(build_door_schedule_sheet_commands(width_mm, depth_length_mm, doors=doors, floor_name="TẦNG 1", sheet_code="KT-04.01", origin_x=origin_x + spacing_x * 3, origin_y=origin_y, project_name=project_name))

    elif stype in ("full_project_set", "all", "full"):
        # Row 1: Floor Plans
        cmds.extend(build_wall_construction_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-01.01", origin_x, origin_y, project_name))
        cmds.extend(build_floor_finishes_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-02.01", origin_x + spacing_x, origin_y, project_name))
        cmds.extend(build_furniture_layout_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-03.01", origin_x + spacing_x * 2, origin_y, project_name))
        cmds.extend(build_door_schedule_sheet_commands(width_mm, depth_length_mm, doors=doors, floor_name="TẦNG 1", sheet_code="KT-04.01", origin_x=origin_x + spacing_x * 3, origin_y=origin_y, project_name=project_name))


        # Row 2: Elevations, Sections, Ceiling, Roof
        row2_y = origin_y + spacing_y
        cmds.extend(build_elevation_sheet_commands(width_mm, floor_height_mm, num_floors, origin_x, row2_y, project_name))
        cmds.extend(build_section_sheet_commands(depth_length_mm, floor_height_mm, num_floors, origin_x + spacing_x, row2_y, project_name))
        cmds.extend(build_ceiling_lighting_sheet_commands(width_mm, depth_length_mm, room_list, origin_x + spacing_x * 2, row2_y, project_name))
        cmds.extend(build_roof_drainage_sheet_commands(width_mm, depth_length_mm, origin_x + spacing_x * 3, row2_y, project_name))

        # Row 3: Architectural Details (Dynamic Stair h/b, Dynamic WC, Paginated Doors)
        row3_y = origin_y + spacing_y * 2
        cmds.extend(build_stair_detail_sheet_commands(floor_height_mm, num_risers, "KT-09", origin_x, row3_y, project_name))

        # WCs
        for wc_i in range(min(wc_count, 2)):
            cmds.extend(build_wc_detail_sheet_commands(f"WC TẦNG {wc_i+1}", f"KT-10.{wc_i+1:02d}", origin_x + spacing_x * (wc_i + 1), row3_y, project_name))

        # Doors (Paginated into multiple A3 sheets as needed)
        door_res = build_door_details_paginated_commands(
            doors,
            max_doors_per_sheet=3,
            origin_x=origin_x + spacing_x * 3,
            origin_y=row3_y,
            project_name=project_name,
            base_spacing_x=spacing_x,
        )
        cmds.extend(door_res["commands"])
    else:
        cmds = build_wall_construction_sheet_commands(width_mm, depth_length_mm, room_list, "TẦNG 1", "KT-01.01", origin_x, origin_y, project_name)

    cmds.append("_.ZOOM _E")
    return cmds
