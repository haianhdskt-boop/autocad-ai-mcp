"""AutoCAD AI MCP Server - macOS Edition (2021-2026)."""

from typing import Dict, Any, List, Optional
from fastmcp import FastMCP

from autocad_ai.core.drawer import build_new_floor_plan_commands
from autocad_ai.core.modifier import build_modify_commands
from autocad_ai.core.finalizer import build_finalized_sheets_commands
from autocad_ai.core.estimator import calculate_detailed_construction_boq
from autocad_ai.core.inspector import check_room_clear_dimensions, audit_full_floor_plan, build_inspection_commands
from autocad_ai.core.plotter import build_plot_single_sheet_commands, build_batch_plot_commands
from autocad_ai.drivers.mac_driver import dispatch_to_autocad_mac, is_autocad_running_mac

SERVER_INSTRUCTIONS = """AutoCAD AI Professional Architect Suite (macOS).

TUÂN THỦ BỘ QUY CHUẨN KIẾN TRÚC TRƯỚC KHI VẼ (architecture-reference-library):
- Hành lang & Lối đi: Hành lang chính >= 1100mm, phụ >= 900mm.
- Cầu thang: Vế thang >= 900mm, chiếu nghỉ >= 900mm, h = H/N (150-175mm), b = 250mm (hoàn thiện 270mm).
- Lan can an toàn: Cao 900mm (thang), 1100mm (thông tầng), nan đứng hở <= 100mm (Quy tắc quả cầu 100mm bảo vệ trẻ em).
- Phòng Khách: Diện tích >= 16m2, bề rộng >= 3.6m, cự ly TV >= 2.5m.
- Bếp & Ăn: Diện tích >= 12m2, lối đi bếp >= 1000-1200mm, tam giác công năng chu vi 4.0-7.5m.
- Phòng Ngủ: Master >= 14m2 (rộng >= 3.3m), phòng đơn/con >= 9m2 (rộng >= 2.7m).
- Vệ Sinh: WC 3 khu >= 3.2m2 (rộng >= 1.4m), hạ cốt 30-50mm, độ dốc thoát nước i=1.5%.
- Giếng Trời: Nhà sâu >= 12m bắt buộc có giếng trời/thông tầng >= 5% diện tích sàn tạo hiệu ứng Stack Effect.

TUÂN THỦ 2 QUY TRÌNH CHUẨN CỦA KIẾN TRÚC SƯ:
🏛️ QUY TRÌNH 1: THIẾT KẾ MỚI (5 BƯỚC)
1. Bước 1: Tiếp nhận diện tích, công năng, sở thích, ảnh mẫu.
2. Bước 2: Đối chiếu quy chuẩn & Đề xuất phương án. DỪNG LẠI CHỜ KTS CHỐT PHƯƠNG ÁN trước khi vẽ.
3. Bước 3: Gọi 'cad_draw_new' vẽ trực tiếp lên AutoCAD theo phương án đã chốt.
4. Bước 4: Gọi 'cad_inspect' (action='audit_full_plan') tự kiểm tra toàn diện thông thủy & tự sửa nếu có lệch.
5. Bước 5: Báo cáo hoàn thành bảng diện tích m2 và thông số cho KTS.

🔧 QUY TRÌNH 2: CHỈNH SỬA / HIỆU CHỈNH (4 BƯỚC)
1. Bước 1: Tiếp nhận yêu cầu chỉnh sửa từ KTS.
2. Bước 2: Gọi 'cad_modify' để Stretch, Move, Mirror, Rotate trực tiếp trên AutoCAD.
3. Bước 3: Rà soát không gian ảnh hưởng, đảm bảo không làm phòng lân cận bị hẹp dưới ngưỡng tiêu chuẩn.
4. Bước 4: Zoom đến vị trí sửa và thông báo kích thước mới cho KTS.
"""

mcp = FastMCP(
    name="autocad-ai-mac",
    instructions=SERVER_INSTRUCTIONS,
)


@mcp.tool()
def cad_draw_new(
    frontage_width_mm: float,
    depth_length_mm: float,
    rooms: List[Dict[str, Any]],
    wall_ext_mm: float = 220.0,
    wall_int_mm: float = 110.0,
    include_furniture: bool = True,
    origin_x: float = 0.0,
    origin_y: float = 0.0,
) -> Dict[str, Any]:
    """
    1. VẼ MỚI (cad_draw_new):
    Vẽ trực tiếp mặt bằng kiến trúc mới lên AutoCAD for Mac.
    - frontage_width_mm: Chiều rộng mặt tiền (mm), ví dụ 5000
    - depth_length_mm: Chiều sâu công trình (mm), ví dụ 15000
    - rooms: Danh sách các phòng [{"name": "Phòng Khách", "y_start": 2500, "y_end": 7000, "type": "living"}]
    - include_furniture: Bố trí nội thất cơ bản (Sofa, TV, Thang, Bếp, Bệt, Lavabo)
    """
    cmds = build_new_floor_plan_commands(
        width_mm=frontage_width_mm,
        length_mm=depth_length_mm,
        rooms=rooms,
        wall_ext_mm=wall_ext_mm,
        wall_int_mm=wall_int_mm,
        origin_x=origin_x,
        origin_y=origin_y,
        include_furniture=include_furniture,
    )
    return dispatch_to_autocad_mac(cmds)


@mcp.tool()
def cad_modify(
    action: str,
    target_description: str,
    parameters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    2. SỬA ĐỔI / DI DỜI (cad_modify):
    Chỉnh sửa, dịch tường, co giãn kích thước phòng, đảo chiều cửa trên AutoCAD.
    - action: 'move', 'stretch', 'resize_room', 'flip_door', 'change_layer', 'delete'
    - target_description: Mô tả đối tượng cần sửa (ví dụ: 'kéo rộng phòng khách thêm 500mm')
    - parameters: Thông số (dx, dy, base_point, crossing_corner1, crossing_corner2)
    """
    cmds = build_modify_commands(action, target_description, parameters)
    return dispatch_to_autocad_mac(cmds)


@mcp.tool()
def cad_finalize_drawing(
    sheet_type: str = "full_project_set",
    frontage_width_mm: float = 5000.0,
    depth_length_mm: float = 15000.0,
    floor_height_mm: float = 3600.0,
    num_floors: int = 2,
    num_risers: int = 21,
    rooms: Optional[List[Dict[str, Any]]] = None,
    doors: Optional[List[Dict[str, Any]]] = None,
    wc_count: int = 2,
    project_name: str = "Nhà Phố Dân Dụng",
    origin_x: float = 0.0,
    origin_y: float = 0.0,
) -> Dict[str, Any]:
    """
    3. HOÀN THIỆN BỘ HỒ SƠ THI CÔNG KIẾN TRÚC (cad_finalize_drawing):
    Tự động phân trang và hoàn thiện trọn bộ bản vẽ kỹ thuật thi công chuẩn A3:
    - Tính toán ĐỘNG thông số cầu thang: Chiều cao cổ bậc h = H / N (ví dụ 3600/21 = 171.4mm, 3900/23 = 169.5mm), mặt bậc b theo công thức Blondel.
    - Phân trang ĐỘNG chi tiết cửa: Tự động chia tối đa 3-4 bộ cửa / 1 tờ A3 để đảm bảo tỷ lệ 1/25 rõ nét (KT-11.01, KT-11.02...).
    - sheet_type:
        * 'full_project_set' / 'all': Dàn trang toàn bộ hồ sơ thi công động.
        * 'all_floor_plans': Dàn trang bộ 4 mặt bằng tầng (KT-01 đến KT-04).
        * 'wall_construction': KT-01 Kích thước tường xây.
        * 'floor_finishes': KT-02 Định vị & ốp lát sàn, mốc lát, độ dốc.
        * 'furniture_layout': KT-03 Bố trí nội thất & bảng thống kê.
        * 'door_window_schedule': KT-04 Định vị cửa & bảng bậu/lanh-tô.
        * 'elevation': KT-05 Mặt đứng chính công trình kèm vật liệu.
        * 'section': KT-06 Mặt cắt dọc 1-1 qua thang.
        * 'ceiling_lighting': KT-07 Mặt bằng trần thạch cao & đèn.
        * 'roof_drainage': KT-08 Mặt bằng mái & thoát nước.
        * 'stair_detail': KT-09 Chi tiết thang tính động h và b.
        * 'wc_detail': KT-10 Chi tiết WC trích 1/25 & 4 vách.
        * 'door_detail': KT-11 Chi tiết cấu tạo cửa phân trang động.
    """
    room_list = rooms or [
        {"name": "SÂN TRƯỚC", "y_start": 0, "y_end": 2500, "type": "yard"},
        {"name": "PHÒNG KHÁCH", "y_start": 2500, "y_end": 7000, "type": "living"},
        {"name": "CẦU THANG", "y_start": 7000, "y_end": 9500, "type": "stairs"},
        {"name": "BẾP & ĂN", "y_start": 9500, "y_end": 13500, "type": "kitchen"},
        {"name": "WC & SÂN SAU", "y_start": 13500, "y_end": 15000, "type": "wc"},
    ]
    cmds = build_finalized_sheets_commands(
        sheet_type=sheet_type,
        width_mm=frontage_width_mm,
        depth_length_mm=depth_length_mm,
        floor_height_mm=floor_height_mm,
        num_floors=num_floors,
        num_risers=num_risers,
        rooms=room_list,
        doors=doors,
        wc_count=wc_count,
        origin_x=origin_x,
        origin_y=origin_y,
        project_name=project_name,
    )
    return dispatch_to_autocad_mac(cmds)


@mcp.tool()
def cad_estimate(
    frontage_width_m: float,
    depth_length_m: float,
    num_floors: int = 2,
    floor_height_m: float = 3.6,
    num_bedrooms: int = 3,
    num_bathrooms: int = 2,
    output_csv_file: Optional[str] = None,
) -> Dict[str, Any]:
    """
    4. LẬP BẢNG DỰ TOÁN THI CÔNG CHI TIẾT (cad_estimate):
    Bóc tách khối lượng toàn diện (Bê tông, ván khuôn, cốt thép, xây tường 220/110, trát trong/ngoài, ốp lát, sơn bả, cửa, MEP) theo định mức xây dựng Việt Nam và xuất file CSV/Excel.
    """
    return calculate_detailed_construction_boq(
        frontage_w_m=frontage_width_m,
        depth_l_m=depth_length_m,
        num_floors=num_floors,
        floor_height_m=floor_height_m,
        num_bedrooms=num_bedrooms,
        num_bathrooms=num_bathrooms,
        output_csv_path=output_csv_file,
    )


@mcp.tool()
def cad_inspect(
    length_mm: Optional[float] = None,
    width_mm: Optional[float] = None,
    room_type: str = "living",
    action: str = "check_standard",
    rooms: Optional[List[Dict[str, Any]]] = None,
    frontage_width_mm: float = 5000.0,
    depth_length_mm: float = 15000.0,
    floor_height_mm: float = 3600.0,
    num_risers: int = 21,
) -> Dict[str, Any]:
    """
    5. KIỂM TRA & RÀ SOÁT QUY CHUẨN KIẾN TRÚC (cad_inspect):
    Rà soát toàn diện phương án theo bộ tiêu chuẩn Neufert & Quy chuẩn Xây Dựng VN (architecture-reference-library).
    - action:
        * 'check_standard': Kiểm tra kích thước thông thủy 1 phòng (diện tích, chiều hẹp).
        * 'audit_full_plan': Rà soát toàn bộ mặt bằng (hành lang, giếng trời, tam giác bếp, cầu thang, an toàn trẻ em).
        * 'audit_purge': Thực hiện lệnh AUDIT và PURGE dọn sạch rác bản vẽ trên AutoCAD.
    """
    if action == "audit_full_plan" and rooms:
        res = audit_full_floor_plan(
            width_mm=frontage_width_mm,
            length_mm=depth_length_mm,
            rooms=rooms,
            floor_height_mm=floor_height_mm,
            num_risers=num_risers,
        )
    else:
        l = length_mm or depth_length_mm
        w = width_mm or frontage_width_mm
        res = check_room_clear_dimensions(l, w, room_type)

    if action == "audit_purge":
        cmds = build_inspection_commands("audit_purge")
        dispatch_to_autocad_mac(cmds)
        res["cad_clean_status"] = "Executed AUDIT & PURGE on AutoCAD"
    return res


@mcp.tool()
def cad_command(commands: List[str]) -> Dict[str, Any]:
    """
    6. GỬI LỆNH AUTOCAD TRỰC TIẾP (cad_command):
    Gửi bất kỳ chuỗi lệnh AutoCAD gốc nào vào cửa sổ AutoCAD for Mac đang mở.
    Ví dụ: ['_.ZOOM _E', '-PURGE ALL * N', '_.REGENALL']
    """
    return dispatch_to_autocad_mac(commands)


@mcp.tool()
def cad_plot(
    plot_scope: str = "batch_all",
    sheet_code: str = "KT-01",
    output_pdf_file: Optional[str] = None,
    output_directory: Optional[str] = None,
    project_name: str = "NHA_PHO",
    paper_size: str = "A3",
    plot_style: str = "monochrome.ctb",
    window_p1: Optional[List[float]] = None,
    window_p2: Optional[List[float]] = None,
) -> Dict[str, Any]:
    """
    7. IN & XUẤT HỒ SƠ PDF CHUẨN KỸ THUẬT (cad_plot):
    In trực tiếp từ AutoCAD ra file PDF với đầy đủ độ dày nét phân cấp và màu đen chuẩn (monochrome.ctb).
    - plot_scope:
        * 'batch_all': In hàng loạt toàn bộ 4 bản vẽ KT-01 đến KT-04 ra các file PDF chuẩn A3 trong thư mục chỉ định.
        * 'single_sheet': In 1 bản vẽ cụ thể theo tọa độ window hoặc mã hiệu bản vẽ.
    - paper_size: 'A3' (mặc định 420x297mm), 'A2', 'A4'
    - plot_style: 'monochrome.ctb' (in đen trắng nét kỹ thuật), 'acad.ctb' (in theo màu layer)
    - output_directory: Thư mục lưu file PDF xuất ra
    """
    if plot_scope == "batch_all":
        batch_res = build_batch_plot_commands(
            output_directory=output_directory,
            project_name=project_name,
            paper_size=paper_size,
            plot_style=plot_style,
        )
        dispatch_res = dispatch_to_autocad_mac(batch_res["commands"])
        batch_res["dispatch_status"] = dispatch_res
        return batch_res
    else:
        out_pdf = output_pdf_file or f"~/Desktop/{project_name}_{sheet_code}.pdf"
        p1 = window_p1 or [-2000.0, -3000.0]
        p2 = window_p2 or [12000.0, 17000.0]
        cmds = build_plot_single_sheet_commands(
            sheet_code=sheet_code,
            window_p1=p1,
            window_p2=p2,
            output_pdf_path=out_pdf,
            paper_size=paper_size,
            plot_style=plot_style,
        )
        cmds.append("_.ZOOM _E")
        dispatch_res = dispatch_to_autocad_mac(cmds)
        return {
            "status": "success",
            "sheet_code": sheet_code,
            "output_pdf": out_pdf,
            "paper_size": paper_size,
            "plot_style": plot_style,
            "dispatch_status": dispatch_res,
        }


# ============================================================================
# WORKFLOW PROMPTS (QUY TRÌNH CHUẨN)
# ============================================================================


@mcp.prompt()
def new_design_proposal(project_brief: str) -> str:
    """Quy trình 1: Hướng dẫn AI tiếp nhận nhiệm vụ thiết kế, phân tích, đề xuất phương án và chờ KTS chốt."""
    return f"""Bạn là Trợ lý Kiến Trúc Sư AI chuyên nghiệp. Hãy tuân thủ QUY TRÌNH THIẾT KẾ MỚI (5 BƯỚC) cho nhiệm vụ sau:
Nhiệm vụ thiết kế: "{project_brief}"

CÁC BƯỚC THỰC HIỆN:
1. BƯỚC 1: Phân tích kỹ diện tích khu đất (rộng x dài), số tầng, nhu cầu các phòng, phong thủy, phong cách.
2. BƯỚC 2 (QUAN TRỌNG): Lập bảng mô tả chi tiết phương án bố trí mặt bằng (phân bổ diện tích, vị trí thang, giếng trời, lối đi). DỪNG LẠI VÀ HỎI KIẾN TRÚC SƯ ĐỂ CHỐT PHƯƠNG ÁN. CHƯA ĐƯỢC VẼ KHI KTS CHƯA CHỐT!
3. BƯỚC 3: Sau khi KTS đồng ý chốt, gọi 'cad_draw_new' vẽ trực tiếp lên AutoCAD.
4. BƯỚC 4: Tự kiểm tra lại bằng 'cad_inspect' (kích thước thông thủy, đối chiếu ý đồ chốt) và tự sửa nếu có lệch.
5. BƯỚC 5: Báo cáo hoàn thành bảng diện tích từng phòng cho KTS.
"""


@mcp.prompt()
def modify_design_request(modification_brief: str) -> str:
    """Quy trình 2: Hướng dẫn AI tiếp nhận yêu cầu chỉnh sửa từ KTS, sửa trực tiếp trên AutoCAD, tự kiểm tra và báo cáo."""
    return f"""Bạn là Trợ lý Kiến Trúc Sư AI chuyên nghiệp. Hãy tuân thủ QUY TRÌNH CHỈNH SỬA (4 BƯỚC) cho yêu cầu sau:
Yêu cầu chỉnh sửa: "{modification_brief}"

CÁC BƯỚC THỰC HIỆN:
1. BƯỚC 1: Phân tích đối tượng cần sửa và phạm vi ảnh hưởng (tường nào, phòng nào bị co giãn).
2. BƯỚC 2: Gọi 'cad_modify' để thực hiện lệnh Stretch, Move, Mirror, Rotate trực tiếp trên AutoCAD.
3. BƯỚC 3: Tự kiểm tra lại diện tích phòng mới và các không gian lân cận để đảm bảo không phát sinh xung đột.
4. BƯỚC 4: Báo cáo hoàn thành, thông báo kích thước mới và zoom đến vị trí vừa sửa cho KTS xem.
"""


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()


