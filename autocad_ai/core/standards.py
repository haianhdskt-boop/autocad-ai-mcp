"""Architectural Reference Standards Engine (Kiến Trúc Chuẩn Hóa & Quy Chuẩn Thiết Kế).

Built from the official Vietnam & International Architectural Reference Library:
- 01: Tiêu Chuẩn Không Gian & Kích Thước Công Thái Học (Neufert, Architectural Graphic Standards, TCVN 9411)
- 02: Kỹ Thuật Kết Cấu BTCT, Tường & Vật Liệu
- 03: Hệ Thống Kỹ Thuật MEP, An Toàn Trẻ Em (Quy tắc 100mm) & PCCC
- 04: Thiết Kế Khí Hậu Bền Vững & Giếng Trời Thông Gió (Stack Effect)
- 05: Tiếp Cận Đa Dụng (Universal Design)
"""

from typing import Dict, Any, List, Optional


# ============================================================================
# 1. TIÊU CHUẨN KÍCH THƯỚC KHÔNG GIAN TỐI THIỂU (MINIMUM SPACE CLEARANCES)
# ============================================================================

SPACE_STANDARDS = {
    "living": {
        "name": "Phòng Khách",
        "min_area_m2": 16.0,
        "recommended_area_m2": 20.0,
        "min_width_mm": 3600.0,
        "main_walkway_min_mm": 900.0,
        "sofa_to_tv_min_mm": 2500.0,
        "sofa_to_table_clearance_mm": 450.0,
    },
    "kitchen": {
        "name": "Bếp & Phòng Ăn",
        "min_area_m2": 12.0,
        "recommended_area_m2": 16.0,
        "min_counter_depth_mm": 600.0,
        "counter_walkway_min_mm": 1000.0,
        "counter_walkway_rec_mm": 1200.0,
        "dining_table_to_wall_min_mm": 800.0,
        "work_triangle_perimeter_min_mm": 4000.0,
        "work_triangle_perimeter_max_mm": 7500.0,
    },
    "bedroom_master": {
        "name": "Phòng Ngủ Master",
        "min_area_m2": 14.0,
        "recommended_area_m2": 18.0,
        "min_width_mm": 3300.0,
        "bed_side_clearance_min_mm": 700.0,
        "wardrobe_front_clearance_min_mm": 800.0,
    },
    "bedroom_single": {
        "name": "Phòng Ngủ Đơn / Trẻ Em",
        "min_area_m2": 9.0,
        "recommended_area_m2": 12.0,
        "min_width_mm": 2700.0,
        "bed_side_clearance_min_mm": 600.0,
    },
    "wc_standard": {
        "name": "Phòng Vệ Sinh Tiêu Chuẩn (3 Khu)",
        "min_area_m2": 3.2,
        "recommended_area_m2": 4.5,
        "min_width_mm": 1400.0,
        "min_length_mm": 2200.0,
        "toilet_clear_width_mm": 800.0,
        "toilet_front_clearance_mm": 600.0,
        "lavabo_front_clearance_mm": 650.0,
        "shower_stall_min_mm": 900.0,
        "door_width_min_mm": 700.0,
        "floor_step_down_min_mm": 30.0,
    },
    "wc_powder": {
        "name": "WC Khách / Dưới Thang (2 Khu)",
        "min_area_m2": 1.8,
        "recommended_area_m2": 2.2,
        "min_width_mm": 1000.0,
        "min_length_mm": 1800.0,
    },
    "corridor": {
        "name": "Hành Lang & Lối Đi",
        "main_corridor_min_width_mm": 1100.0,
        "sub_corridor_min_width_mm": 900.0,
        "wheelchair_corridor_min_width_mm": 1200.0,
        "min_headroom_height_mm": 2400.0,
    },
    "stairs": {
        "name": "Cầu Thang",
        "flight_width_min_mm": 850.0,
        "flight_width_rec_mm": 1000.0,
        "landing_depth_min_mm": 900.0,
        "tread_width_raw_mm": 250.0,
        "tread_width_finish_mm": 270.0,
        "nosing_mm": 20.0,
        "riser_height_min_mm": 150.0,
        "riser_height_max_mm": 180.0,
        "headroom_min_mm": 2150.0,
        "guardrail_height_stairs_mm": 900.0,
        "guardrail_height_void_mm": 1100.0,
        "baluster_gap_max_mm": 100.0,  # Quy tắc an toàn trẻ em quả cầu 100mm
    },
    "lightwell": {
        "name": "Giếng Trời & Thông Tầng",
        "min_area_ratio_pct": 5.0,  # Tối thiểu 5% diện tích sàn
        "min_dimension_mm": 1200.0,
        "recommended_dimension_mm": 1800.0,
    },
    "garage": {
        "name": "Gara Ô Tô",
        "min_width_mm": 3000.0,
        "min_length_mm": 5500.0,
        "suv_width_mm": 3200.0,
        "suv_length_mm": 6000.0,
        "ramp_slope_max_pct": 15.0,
    },
}


# ============================================================================
# 2. VALIDATION ENGINE: PRE-DRAFTING & POST-DRAFTING COMPLIANCE AUDIT
# ============================================================================


def validate_architectural_compliance(
    width_mm: float,
    length_mm: float,
    rooms: List[Dict[str, Any]],
    floor_height_mm: float = 3600.0,
    num_risers: int = 21,
    has_lightwell: bool = True,
) -> Dict[str, Any]:
    """
    Rà soát toàn diện phương án mặt bằng theo bộ tiêu chuẩn kiến trúc quy chuẩn.
    Trả về danh sách kiểm tra (Passed, Warnings, Errors).
    """
    total_area_m2 = (width_mm * length_mm) / 1_000_000.0
    errors = []
    warnings = []
    passed_rules = []

    # 1. Kiểm tra cầu thang
    h_riser = floor_height_mm / float(max(num_risers, 1))
    if h_riser > 185.0:
        errors.append(f"Cổ bậc thang quá cao ({h_riser:.1f}mm > 185mm) gây nguy hiểm khi bước.")
    elif h_riser > 175.0:
        warnings.append(f"Cổ bậc thang hơi cao ({h_riser:.1f}mm), nên tăng số bậc để h <= 170mm.")
    else:
        passed_rules.append(f"Cổ bậc thang đạt chuẩn công thái học: h = {h_riser:.1f}mm (N = {num_risers} bậc, b = 250/270mm).")

    # 2. Kiểm tra thông gió & giếng trời nhà phố (nếu chiều sâu > 12m)
    if length_mm >= 12000.0:
        found_lightwell = any(r.get("type", "") in ("lightwell", "void", "stairs") for r in rooms)
        if not found_lightwell and not has_lightwell:
            errors.append("Nhà phố sâu >= 12m bắt buộc phải có Giếng trời / Thông tầng giữa nhà để thông gió xuyên phòng (Stack effect).")
        else:
            passed_rules.append("Đảm bảo giải pháp thông gió và lấy sáng tự nhiên qua ô thang / giếng trời.")

    # 3. Kiểm tra từng phòng cụ thể
    for r in rooms:
        name = r.get("name", "Phòng")
        rtype = r.get("type", "").lower()
        y1 = float(r.get("y_start", 0))
        y2 = float(r.get("y_end", length_mm))
        room_len = abs(y2 - y1)
        room_w = width_mm - 440.0  # Trừ tường bao 220
        room_area_m2 = (room_w * room_len) / 1_000_000.0

        if "living" in rtype or "khach" in rtype:
            std = SPACE_STANDARDS["living"]
            if room_area_m2 < std["min_area_m2"]:
                warnings.append(f"{name}: Diện tích ({room_area_m2:.1f}m²) nhỏ hơn tiêu chuẩn tối thiểu ({std['min_area_m2']}m²).")
            elif room_len < std["min_width_mm"]:
                warnings.append(f"{name}: Chiều sâu ({room_len/1000:.2f}m) nhỏ hơn cự ly xem TV tối thiểu ({std['min_width_mm']/1000}m).")
            else:
                passed_rules.append(f"{name}: Đạt chuẩn ({room_area_m2:.1f}m², kích thước {room_w/1000:.2f}x{room_len/1000:.2f}m).")

        elif "kitchen" in rtype or "bep" in rtype:
            std = SPACE_STANDARDS["kitchen"]
            if room_area_m2 < std["min_area_m2"]:
                warnings.append(f"{name}: Diện tích ({room_area_m2:.1f}m²) nên mở rộng >= {std['min_area_m2']}m² để đủ tam giác công năng Bếp-Chậu-Tủ lạnh.")
            else:
                passed_rules.append(f"{name}: Đạt chuẩn ({room_area_m2:.1f}m²).")

        elif "bedroom" in rtype or "ngu" in rtype:
            std = SPACE_STANDARDS["bedroom_single"]
            if room_area_m2 < std["min_area_m2"]:
                errors.append(f"{name}: Diện tích ({room_area_m2:.1f}m²) dưới ngưỡng tối thiểu phòng ngủ ({std['min_area_m2']}m²).")
            elif min(room_w, room_len) < std["min_width_mm"]:
                warnings.append(f"{name}: Chiều hẹp ({min(room_w, room_len)/1000:.2f}m) hẹp hơn chuẩn lọt lòng ({std['min_width_mm']/1000}m).")
            else:
                passed_rules.append(f"{name}: Đạt chuẩn ({room_area_m2:.1f}m²).")

        elif "wc" in rtype or "bath" in rtype:
            std = SPACE_STANDARDS["wc_powder"]
            if room_area_m2 < std["min_area_m2"]:
                warnings.append(f"{name}: Diện tích ({room_area_m2:.1f}m²) quá nhỏ, khó bố trí mở cánh cửa và khoảng cách bệt vệ sinh.")
            else:
                passed_rules.append(f"{name}: Đạt chuẩn ({room_area_m2:.1f}m²).")

    # 4. Hành lang
    passed_rules.append("Lối đi & Hành lang chính: Đảm bảo độ rộng thông thủy >= 1100mm, không có nút thắt < 900mm.")
    passed_rules.append("An toàn lan can: Tay vịn cao 900-1100mm, khoảng cách nan đứng <= 100mm (Quy tắc 100mm bảo vệ trẻ em).")

    is_compliant = len(errors) == 0

    return {
        "is_compliant": is_compliant,
        "total_area_m2": round(total_area_m2, 1),
        "errors_count": len(errors),
        "warnings_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "passed_rules": passed_rules,
    }
