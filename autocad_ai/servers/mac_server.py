"""AutoCAD AI MCP Server - macOS Edition (2021-2026)."""

from typing import Dict, Any, List, Optional
from fastmcp import FastMCP

from autocad_ai.core.drawer import build_new_floor_plan_commands
from autocad_ai.core.modifier import build_modify_commands
from autocad_ai.core.finalizer import build_finalized_sheets_commands
from autocad_ai.core.estimator import calculate_detailed_construction_boq
from autocad_ai.core.inspector import check_room_clear_dimensions, build_inspection_commands
from autocad_ai.drivers.mac_driver import dispatch_to_autocad_mac, is_autocad_running_mac

mcp = FastMCP(
    name="autocad-ai-mac",
    instructions="AutoCAD AI Professional Architect Suite (macOS): 6 core business commands for live drafting, modification, multi-sheet construction documentation, detailed BOQ estimation, and drawing inspection.",
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
    sheet_type: str = "all",
    frontage_width_mm: float = 5000.0,
    depth_length_mm: float = 15000.0,
    rooms: Optional[List[Dict[str, Any]]] = None,
    project_name: str = "Nhà Phố Dân Dụng",
    origin_x: float = 0.0,
    origin_y: float = 0.0,
) -> Dict[str, Any]:
    """
    3. HOÀN THIỆN BỘ HỒ SƠ THI CÔNG (cad_finalize_drawing):
    Tự động phân tách và dàn trang bộ 4 bản vẽ thi công chuyên biệt kèm khung tên chuẩn A3:
    - sheet_type:
        * 'all': Xuất trọn bộ 4 bản vẽ dàn trang cạnh nhau sẵn sàng in ấn/plot!
        * 'wall_construction': Bản vẽ KT-01 Kích thước tường xây (DIM 3 lớp, hatch tường gạch, không nội thất)
        * 'floor_finishes': Bản vẽ KT-02 Định vị ốp lát sàn, cao độ phòng, mốc lát đầu tiên, mũi tên độ dốc WC
        * 'furniture_layout': Bản vẽ KT-03 Bố trí nội thất, tag mã hiệu đồ, diện tích phòng & bảng thống kê
        * 'door_window_schedule': Bản vẽ KT-04 Định vị cửa, tag D1/S1, bảng kích thước, cốt bậu dưới & lanh-tô
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
        length_mm=depth_length_mm,
        rooms=room_list,
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
    length_mm: float,
    width_mm: float,
    room_type: str = "living",
    action: str = "check_standard",
) -> Dict[str, Any]:
    """
    5. KIỂM TRA & ĐO ĐẠC (cad_inspect):
    Kiểm tra diện tích thông thủy ($m^2$), kích thước lọt lòng theo tiêu chuẩn kiến trúc & công thái học.
    - room_type: 'living', 'bedroom_master', 'bedroom_single', 'kitchen', 'wc', 'corridor', 'staircase'
    """
    res = check_room_clear_dimensions(length_mm, width_mm, room_type)
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


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
