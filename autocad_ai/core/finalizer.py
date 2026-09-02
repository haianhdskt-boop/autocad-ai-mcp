"""Finalizer Engine: Generates Complete Architectural Construction Documentation Packages (Hồ Sơ Thiết Kế Thi Công - TKTC).

Full Set of Specialized Construction Sheets:
1. Floor Plans:
   - KT-01: Wall Construction (Mặt bằng Kích thước tường xây, DIM 3 lớp, hatch tường, không nội thất)
   - KT-02: Floor Finishes (Mặt bằng Định vị ốp lát sàn, cao độ phòng, mốc lát, độ dốc thoát nước)
   - KT-03: Furniture Layout (Mặt bằng Bố trí nội thất, tag mã hiệu đồ, diện tích phòng & bảng thống kê)
   - KT-04: Door Layout (Mặt bằng Định vị & Phân loại cửa, bảng chỉ dẫn bậu dưới/lanh-tô trên)
2. Elevations & Sections:
   - KT-05: Front Elevation (Mặt đứng chính công trình, cốt cao độ các tầng, chỉ dẫn vật liệu ngoại thất)
   - KT-06: Longitudinal Section 1-1 (Mặt cắt dọc qua thang & giếng trời, cấu tạo sàn, chiều cao thông thủy)
3. Ceiling & Roof Plans:
   - KT-07: Reflected Ceiling Plan (Mặt bằng Trần thạch cao giật cấp, khe hắt LED, bố trí đèn downlight)
   - KT-08: Roof & Drainage Plan (Mặt bằng Mái, độ dốc thu nước sê-nô, lớp chống thấm, bồn nước)
4. Architectural Detail Sets:
   - KT-09: Stair Details (Chi tiết thang các tầng, mặt cắt thang, chi tiết mũi bậc, lan can tay vịn)
   - KT-10: Restroom Details (Chi tiết WC trích tỷ lệ 1/25, triển khai 4 vách tường ốp lát & thiết bị)
   - KT-11: Door & Window Details (Chi tiết cấu tạo từng bộ cửa D1, D2, S1 kèm đố cửa & phụ kiện)
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
        f"_.-TEXT {ox + 500},{oy + 1500} 350 0 DU AN: {project_name.upper()}",
        f"_.-TEXT {ox + 500},{oy + 600} 380 0 HANG MUC: {sheet_title.upper()}",
        f"_.-TEXT {ox + bw - 3200},{oy + 1500} 250 0 TY LE: {scale_str}",
        f"_.-TEXT {ox + bw - 3200},{oy + 600} 450 0 SO: {sheet_code}",
    ]
    return cmds


# ============================================================================
# 1. NHÓM BẢN VẼ MẶT BẰNG (KT-01 ĐẾN KT-04)
# ============================================================================


def build_wall_construction_sheet_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """1. KT-01: Mặt bằng kích thước tường xây (Masonry Plan)."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; 1. SHEET KT-01: MAT BANG KICH THUOC TUONG XAY",
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

    cmds.extend(build_title_block_commands(ox, oy, "MẶT BẰNG KÍCH THƯỚC TƯỜNG XÂY", "KT-01", project_name))
    return cmds


def build_floor_finishes_sheet_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """2. KT-02: Mặt bằng định vị & ốp lát sàn (Floor Finish Plan)."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; 2. SHEET KT-02: MAT BANG DINH VI & OP LAT SAN",
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

    cmds.extend(build_title_block_commands(ox, oy, "MẶT BẰNG ĐỊNH VỊ & ỐP LÁT SÀN", "KT-02", project_name))
    return cmds


def build_furniture_layout_sheet_commands(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """3. KT-03: Mặt bằng bố trí nội thất & bảng thống kê (Furniture Layout)."""
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

    cmds.extend(build_title_block_commands(ox, oy, "MẶT BẰNG BỐ TRÍ NỘI THẤT", "KT-03", project_name))
    return cmds


def build_door_schedule_sheet_commands(
    width_mm: float,
    length_mm: float,
    doors: Optional[List[Dict[str, Any]]] = None,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """4. KT-04: Mặt bằng định vị & phân loại cửa (Door Layout)."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; 4. SHEET KT-04: MAT BANG DINH VI & PHAN LOAI CUA",
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

    cmds.extend(build_title_block_commands(ox, oy, "MẶT BẰNG ĐỊNH VỊ & PHÂN LOẠI CỬA", "KT-04", project_name))
    return cmds


# ============================================================================
# 2. NHÓM MẶT ĐỨNG & MẶT CẮT (KT-05, KT-06)
# ============================================================================


def build_elevation_sheet_commands(
    width_mm: float = 5000.0,
    floor_height_mm: float = 3600.0,
    num_floors: int = 2,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """5. KT-05: Mặt đứng chính công trình (Front Elevation)."""
    ox, oy = origin_x, origin_y
    w = width_mm
    h = floor_height_mm
    total_h = h * num_floors + 1200.0  # + Roof parapet

    cmds = [
        ";; ==========================================================================",
        ";; 5. SHEET KT-05: MAT DUNG CHINH CONG TRINH",
        ";; ==========================================================================",
        "_.-LAYER _M KT_MAT_DUNG _C 7 KT_MAT_DUNG  ",
        "_.-LAYER _M KT_CAO_DO _C 1 KT_CAO_DO  ",
        "_.-LAYER _M KT_NOTE_VAT_LIEU _C 4 KT_NOTE_VAT_LIEU  ",
        "_.-LAYER _S KT_MAT_DUNG  ",
        # Main Facade Outline
        f"_.RECTANG {ox},{oy} {ox + w},{oy + total_h}",
        # Floor 1 Boundary & Main Door
        f"_.RECTANG {ox + 800},{oy} {ox + w - 800},{oy + 2600}",
        # Floor 2 Balcony & Window
        f"_.RECTANG {ox + 400},{oy + h} {ox + w - 400},{oy + h + 1100}",  # Balcony railing
        f"_.RECTANG {ox + 1200},{oy + h + 500} {ox + w - 1200},{oy + h + 2500}",  # Glass door/window
        # Parapet / Roof crown
        f"_.LINE {ox},{oy + total_h - 600} {ox + w},{oy + total_h - 600} ",
        # Elevation Level Markers
        "_.-LAYER _S KT_CAO_DO  ",
        f"_.LINE {ox - 1200},{oy} {ox},{oy} ",
        f"_.-TEXT {ox - 1600},{oy + 100} 200 0 COT SAN TRUOC: +0.050",
        f"_.LINE {ox - 1200},{oy + h} {ox},{oy + h} ",
        f"_.-TEXT {ox - 1600},{oy + h + 100} 200 0 COT SAN LAU 1: +3.650",
        f"_.LINE {ox - 1200},{oy + total_h} {ox},{oy + total_h} ",
        f"_.-TEXT {ox - 1600},{oy + total_h + 100} 200 0 COT DINH MAI: +8.400",
        # Material notes
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
    """6. KT-06: Mặt cắt dọc 1-1 qua thang & giếng trời (Longitudinal Section)."""
    ox, oy = origin_x, origin_y
    l = depth_length_mm
    h = floor_height_mm
    total_h = h * num_floors + 1200.0

    cmds = [
        ";; ==========================================================================",
        ";; 6. SHEET KT-06: MAT CAT DOC 1-1 QUA THANG",
        ";; ==========================================================================",
        "_.-LAYER _M KT_NET_CAT _C 1 KT_NET_CAT  ",
        "_.-LAYER _M KT_CAO_DO _C 1 KT_CAO_DO  ",
        "_.-LAYER _S KT_NET_CAT  ",
        # Section floor slabs (Cut lines)
        f"_.RECTANG {ox},{oy} {ox + l},{oy + 200}",  # Ground slab
        f"_.RECTANG {ox},{oy + h} {ox + l},{oy + h + 120}",  # Floor 2 slab
        f"_.RECTANG {ox},{oy + total_h - 400} {ox + l},{oy + total_h - 280}",  # Roof slab
        # Stair profile in section (X: 7000 to 9500)
        f"_.LINE {ox + 7000},{oy + 200} {ox + 8200},{oy + h*0.5} ",
        f"_.LINE {ox + 8200},{oy + h*0.5} {ox + 9400},{oy + h} ",
        # Elevation Tags
        "_.-LAYER _S KT_CAO_DO  ",
        f"_.DIMLINEAR {ox - 1000},{oy} {ox - 1000},{oy + h} {ox - 1500},{oy}",
        f"_.-TEXT {ox + 2000},{oy + h*0.5} 200 0 THONG THUY P.KHACH: 3600mm",
        f"_.-TEXT {ox + 7500},{oy + h + 500} 200 0 GIENG TROI THONG TANG",
    ]

    cmds.extend(build_title_block_commands(ox, oy, "MẶT CẮT DỌC 1-1 QUA THANG", "KT-06", project_name))
    return cmds


# ============================================================================
# 3. NHÓM TRẦN ĐÈN & MÁI (KT-07, KT-08)
# ============================================================================


def build_ceiling_lighting_sheet_commands(
    width_mm: float = 5000.0,
    length_mm: float = 15000.0,
    rooms: Optional[List[Dict[str, Any]]] = None,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """7. KT-07: Mặt bằng trần thạch cao & đèn chiếu sáng (Ceiling & Lighting Plan)."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; 7. SHEET KT-07: MAT BANG TRAN THACH CAO & DEN",
        ";; ==========================================================================",
        "_.-LAYER _F KT_NOITHAT  ",
        "_.-LAYER _M KT_TRAN_THACH_CAO _C 4 KT_TRAN_THACH_CAO  ",
        "_.-LAYER _M KT_DEN_DOWNLIGHT _C 2 KT_DEN_DOWNLIGHT  ",
        "_.-LAYER _S KT_TRAN_THACH_CAO  ",
        # Living Room Dropped Ceiling (Trần giật cấp)
        f"_.RECTANG {ox + 600},{oy + 3000} {ox + w - 600},{oy + 6500}",
        f"_.-TEXT {ox + w*0.5 - 1000},{oy + 4750} 200 0 TRAN THACH CAO HA COT -200mm",
        f"_.-TEXT {ox + w*0.5 - 800},{oy + 4400} 160 0 KHE HAT SANG DEN LED STRIP",
        # Downlight grid
        "_.-LAYER _S KT_DEN_DOWNLIGHT  ",
    ]

    for dx in [1000, w*0.5, w - 1000]:
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
    """8. KT-08: Mặt bằng mái & thoát nước (Roof Drainage Plan)."""
    ox, oy = origin_x, origin_y
    w, l = width_mm, length_mm

    cmds = [
        ";; ==========================================================================",
        ";; 8. SHEET KT-08: MAT BANG MAI & THOAT NUOC",
        ";; ==========================================================================",
        "_.-LAYER _M KT_MAI _C 7 KT_MAI  ",
        "_.-LAYER _M KT_THOAT_NUOC _C 5 KT_THOAT_NUOC  ",
        "_.-LAYER _S KT_MAI  ",
        f"_.RECTANG {ox},{oy} {ox + w},{oy + l}",
        # Sê-nô thu nước phía sau
        f"_.RECTANG {ox},{oy + l - 600} {ox + w},{oy + l}",
        # Bồn nước và thái dương năng
        f"_.RECTANG {ox + 600},{oy + 2000} {ox + 2200},{oy + 3800}",
        f"_.-TEXT {ox + 700},{oy + 2900} 180 0 BON NUOC INOX 1500L & NANG LUONG MAT TROY",
        # Drainage slope arrows towards scupper drain
        "_.-LAYER _S KT_THOAT_NUOC  ",
        f"_.LINE {ox + w*0.5},{oy + 2000} {ox + w*0.5},{oy + l - 800} ",
        f"_.-TEXT {ox + w*0.5 + 200},{oy + l*0.5} 180 0 DO DOC THU NUOC i = 2% VE SE-NO",
        f"_.CIRCLE {ox + 600},{oy + l - 300} 100",
        f"_.-TEXT {ox + 800},{oy + l - 300} 160 0 PHEU THU SE-NO D114",
    ]

    cmds.extend(build_title_block_commands(ox, oy, "MẶT BẰNG MÁI & THOÁT NƯỚC", "KT-08", project_name))
    return cmds


# ============================================================================
# 4. NHÓM CHI TIẾT KIẾN TRÚC CHUYÊN SÂU (KT-09 ĐẾN KT-11)
# ============================================================================


def build_stair_detail_sheet_commands(
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """9. KT-09: Chi tiết cầu thang, mặt bậc & lan can tay vịn (Stair Details)."""
    ox, oy = origin_x, origin_y

    cmds = [
        ";; ==========================================================================",
        ";; 9. SHEET KT-09: CHI TIET CAU THANG & LAN CAN",
        ";; ==========================================================================",
        "_.-LAYER _M KT_CHI_TIET _C 7 KT_CHI_TIET  ",
        "_.-LAYER _S KT_CHI_TIET  ",
        # Detail 1: Stair step profile (h=171mm, b=260mm)
        f"_.LINE {ox + 500},{oy + 2000} {ox + 1020},{oy + 2000} ",
        f"_.LINE {ox + 1020},{oy + 2000} {ox + 1020},{oy + 2342} ",
        f"_.LINE {ox + 1020},{oy + 2342} {ox + 1540},{oy + 2342} ",
        f"_.LINE {ox + 1540},{oy + 2342} {ox + 1540},{oy + 2684} ",
        f"_.-TEXT {ox + 500},{oy + 3000} 220 0 CHI TIET MAT BAC THANG (1/10)",
        f"_.-TEXT {ox + 500},{oy + 2600} 160 0 * MAT BAC GO GO DO DAY 30mm, MUI BAC BO TRON R10",
        f"_.-TEXT {ox + 500},{oy + 2200} 160 0 * CO BAC OP DA TRANG SU NHAN TAO DAY 18mm",
        # Detail 2: Glass Handrail (Lan can kính tay vịn gỗ)
        f"_.RECTANG {ox + 3500},{oy + 1500} {ox + 6000},{oy + 4500}",
        f"_.-TEXT {ox + 3600},{oy + 4200} 200 0 CHI TIET LAN CAN TAY VIN",
        f"_.-TEXT {ox + 3600},{oy + 3800} 160 0 * TAY VIN GO OVAL 60x80mm",
        f"_.-TEXT {ox + 3600},{oy + 3400} 160 0 * KINH CUONG LUC 10mm KEM TRU INOX 304",
    ]

    cmds.extend(build_title_block_commands(ox, oy, "CHI TIẾT CẦU THANG & LAN CAN", "KT-09", project_name, scale_str="1/20"))
    return cmds


def build_wc_detail_sheet_commands(
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """10. KT-10: Chi tiết phòng vệ sinh trích 1/25 & triển khai 4 vách (Restroom Details)."""
    ox, oy = origin_x, origin_y

    cmds = [
        ";; ==========================================================================",
        ";; 10. SHEET KT-10: CHI TIET PHONG VE SINH TRICH 1/25",
        ";; ==========================================================================",
        "_.-LAYER _M KT_CHI_TIET _C 7 KT_CHI_TIET  ",
        "_.-LAYER _S KT_CHI_TIET  ",
        # Enlarged Plan (Mặt bằng trích 1/25: 1800 x 2400)
        f"_.RECTANG {ox + 500},{oy + 1000} {ox + 2300},{oy + 3400}",
        f"_.CIRCLE {ox + 1400},{oy + 1600} 220",  # Toilet
        f"_.RECTANG {ox + 600},{oy + 2700} {ox + 1200},{oy + 3300}",  # Lavabo
        f"_.-TEXT {ox + 600},{oy + 3600} 220 0 MAT BANG TRICH VE SINH (TY LE 1/25)",
        # 4 Wall Elevations (Mặt cắt 4 vách tường ốp lát)
        f"_.RECTANG {ox + 3000},{oy + 1000} {ox + 5400},{oy + 3600}",
        f"_.-TEXT {ox + 3100},{oy + 3800} 200 0 MAT CAT TRIEN KHAI VACH SEN TAM",
        f"_.-TEXT {ox + 3100},{oy + 3400} 160 0 * COT SEN DUNG: +1.100m, VACH KINH TAM DUNG 10mm",
        f"_.-TEXT {ox + 3100},{oy + 3000} 160 0 * GACH OP TUONG CERAMIC 300x600 OP KICH TRAN (+2.800m)",
    ]

    cmds.extend(build_title_block_commands(ox, oy, "CHI TIẾT PHÒNG VỆ SINH", "KT-10", project_name, scale_str="1/25"))
    return cmds


def build_door_details_sheet_commands(
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """11. KT-11: Chi tiết cấu tạo cửa đi & cửa sổ (Door & Window Details)."""
    ox, oy = origin_x, origin_y

    cmds = [
        ";; ==========================================================================",
        ";; 11. SHEET KT-11: CHI TIET CAU TAO CUA D1, D2, S1",
        ";; ==========================================================================",
        "_.-LAYER _M KT_CHI_TIET _C 7 KT_CHI_TIET  ",
        "_.-LAYER _S KT_CHI_TIET  ",
        # Door D1 Elevation (2800 x 2600 - 4 wings)
        f"_.RECTANG {ox + 500},{oy + 1000} {ox + 3300},{oy + 3600}",
        f"_.LINE {ox + 1200},{oy + 1000} {ox + 1200},{oy + 3600} ",
        f"_.LINE {ox + 1900},{oy + 1000} {ox + 1900},{oy + 3600} ",
        f"_.LINE {ox + 2600},{oy + 1000} {ox + 2600},{oy + 3600} ",
        f"_.-TEXT {ox + 500},{oy + 3800} 220 0 CUA DI CHINH D1 (2800 x 2600 - 4 CANH MO QUAY)",
        # Window S1 Elevation (1600 x 1400 - 2 wings)
        f"_.RECTANG {ox + 4200},{oy + 1500} {ox + 5800},{oy + 2900}",
        f"_.LINE {ox + 5000},{oy + 1500} {ox + 5000},{oy + 2900} ",
        f"_.-TEXT {ox + 4200},{oy + 3200} 200 0 CUA SO S1 (1600 x 1400 - 2 CANH MO TRUOT)",
        f"_.-TEXT {ox + 500},{oy + 500} 160 0 * PHU KIEN: KINLONG DONG BO, KINH AN TOAN 8.38mm",
    ]

    cmds.extend(build_title_block_commands(ox, oy, "CHI TIẾT CẤU TẠO CỬA ĐI & SỔ", "KT-11", project_name, scale_str="1/25"))
    return cmds


# ============================================================================
# MASTER DISPATCHER: GENERATES ANY SHEET OR THE FULL PROJECT SET
# ============================================================================


def build_finalized_sheets_commands(
    sheet_type: str,
    width_mm: float = 5000.0,
    depth_length_mm: float = 15000.0,
    rooms: Optional[List[Dict[str, Any]]] = None,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
    project_name: str = "Nhà Phố Dân Dụng",
) -> List[str]:
    """
    Master Dispatcher for Finalizing Architectural Construction Drawings.
    Supported sheet_type:
    - 'wall_construction' (KT-01)
    - 'floor_finishes' (KT-02)
    - 'furniture_layout' (KT-03)
    - 'door_window_schedule' (KT-04)
    - 'elevation' (KT-05 Mặt đứng chính)
    - 'section' (KT-06 Mặt cắt 1-1)
    - 'ceiling_lighting' (KT-07 Trần đèn)
    - 'roof_drainage' (KT-08 Mái)
    - 'stair_detail' (KT-09 Chi tiết thang)
    - 'wc_detail' (KT-10 Chi tiết vệ sinh)
    - 'door_detail' (KT-11 Chi tiết cửa)
    - 'all_floor_plans' (Bộ 4 mặt bằng tầng KT-01 đến KT-04)
    - 'full_project_set' / 'all' (Trọn bộ toàn bộ 11 bản vẽ thi công KT-01 đến KT-11)
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
        cmds = build_wall_construction_sheet_commands(width_mm, depth_length_mm, room_list, origin_x, origin_y, project_name)
    elif stype == "floor_finishes":
        cmds = build_floor_finishes_sheet_commands(width_mm, depth_length_mm, room_list, origin_x, origin_y, project_name)
    elif stype == "furniture_layout":
        cmds = build_furniture_layout_sheet_commands(width_mm, depth_length_mm, room_list, origin_x, origin_y, project_name)
    elif stype in ("door_window_schedule", "doors"):
        cmds = build_door_schedule_sheet_commands(width_mm, depth_length_mm, [], origin_x, origin_y, project_name)
    elif stype in ("elevation", "mat_dung"):
        cmds = build_elevation_sheet_commands(width_mm, 3600.0, 2, origin_x, origin_y, project_name)
    elif stype in ("section", "mat_cat"):
        cmds = build_section_sheet_commands(depth_length_mm, 3600.0, 2, origin_x, origin_y, project_name)
    elif stype in ("ceiling_lighting", "tran_den"):
        cmds = build_ceiling_lighting_sheet_commands(width_mm, depth_length_mm, room_list, origin_x, origin_y, project_name)
    elif stype in ("roof_drainage", "mai"):
        cmds = build_roof_drainage_sheet_commands(width_mm, depth_length_mm, origin_x, origin_y, project_name)
    elif stype in ("stair_detail", "chi_tiet_thang"):
        cmds = build_stair_detail_sheet_commands(origin_x, origin_y, project_name)
    elif stype in ("wc_detail", "chi_tiet_wc"):
        cmds = build_wc_detail_sheet_commands(origin_x, origin_y, project_name)
    elif stype in ("door_detail", "chi_tiet_cua"):
        cmds = build_door_details_sheet_commands(origin_x, origin_y, project_name)

    elif stype in ("all_floor_plans", "floor_set"):
        # 4 Floor plan sheets horizontally
        cmds.extend(build_wall_construction_sheet_commands(width_mm, depth_length_mm, room_list, origin_x, origin_y, project_name))
        cmds.extend(build_floor_finishes_sheet_commands(width_mm, depth_length_mm, room_list, origin_x + spacing_x, origin_y, project_name))
        cmds.extend(build_furniture_layout_sheet_commands(width_mm, depth_length_mm, room_list, origin_x + spacing_x * 2, origin_y, project_name))
        cmds.extend(build_door_schedule_sheet_commands(width_mm, depth_length_mm, [], origin_x + spacing_x * 3, origin_y, project_name))

    elif stype in ("full_project_set", "all", "full"):
        # Grid layout: Row 1 (Floor Plans 1-4), Row 2 (Elevations, Sections, Ceiling, Roof 5-8), Row 3 (Details 9-11)
        # Row 1: Floor Plans
        cmds.extend(build_wall_construction_sheet_commands(width_mm, depth_length_mm, room_list, origin_x, origin_y, project_name))
        cmds.extend(build_floor_finishes_sheet_commands(width_mm, depth_length_mm, room_list, origin_x + spacing_x, origin_y, project_name))
        cmds.extend(build_furniture_layout_sheet_commands(width_mm, depth_length_mm, room_list, origin_x + spacing_x * 2, origin_y, project_name))
        cmds.extend(build_door_schedule_sheet_commands(width_mm, depth_length_mm, [], origin_x + spacing_x * 3, origin_y, project_name))

        # Row 2: Elevations, Sections, Ceiling, Roof
        row2_y = origin_y + spacing_y
        cmds.extend(build_elevation_sheet_commands(width_mm, 3600.0, 2, origin_x, row2_y, project_name))
        cmds.extend(build_section_sheet_commands(depth_length_mm, 3600.0, 2, origin_x + spacing_x, row2_y, project_name))
        cmds.extend(build_ceiling_lighting_sheet_commands(width_mm, depth_length_mm, room_list, origin_x + spacing_x * 2, row2_y, project_name))
        cmds.extend(build_roof_drainage_sheet_commands(width_mm, depth_length_mm, origin_x + spacing_x * 3, row2_y, project_name))

        # Row 3: Architectural Details
        row3_y = origin_y + spacing_y * 2
        cmds.extend(build_stair_detail_sheet_commands(origin_x, row3_y, project_name))
        cmds.extend(build_wc_detail_sheet_commands(origin_x + spacing_x, row3_y, project_name))
        cmds.extend(build_door_details_sheet_commands(origin_x + spacing_x * 2, row3_y, project_name))
    else:
        cmds = build_wall_construction_sheet_commands(width_mm, depth_length_mm, room_list, origin_x, origin_y, project_name)

    cmds.append("_.ZOOM _E")
    return cmds
