"""Estimator Engine: Deep Quantity Takeoff (QTO) & Construction BOQ Generation."""

import os
import csv
from typing import Dict, Any, List, Optional


def calculate_detailed_construction_boq(
    frontage_w_m: float,
    depth_l_m: float,
    num_floors: int = 2,
    floor_height_m: float = 3.6,
    num_bedrooms: int = 3,
    num_bathrooms: int = 2,
    has_elevator: bool = False,
    output_csv_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Calculate comprehensive civil construction quantity takeoff according to Vietnamese construction norms.
    """
    w = float(frontage_w_m)
    l = float(depth_l_m)
    floors = int(num_floors)
    h = float(floor_height_m)

    footprint_area = w * l
    total_floor_area = footprint_area * floors
    perimeter_ext = 2 * (w + l)

    # 1. Structure Quantities (Kết cấu)
    # Be tong mong & be tong lot
    vol_concrete_footing = round(footprint_area * 0.35, 2)  # m3
    vol_concrete_columns = round(footprint_area * floors * 0.045, 2)  # m3
    vol_concrete_beams = round(footprint_area * floors * 0.065, 2)  # m3
    vol_concrete_slabs = round(footprint_area * (floors - 1) * 0.10, 2)  # m3
    total_concrete = round(
        vol_concrete_footing + vol_concrete_columns + vol_concrete_beams + vol_concrete_slabs, 2
    )

    # Van khuon (Formwork) ~ 8.5 m2 per m3 concrete
    area_formwork = round(total_concrete * 8.5, 2)  # m2

    # Rebar (Cot thep) ~ 120 - 140 kg per m3 concrete
    weight_steel_kg = round(total_concrete * 135.0, 1)  # kg
    weight_steel_ton = round(weight_steel_kg / 1000.0, 3)

    # 2. Architecture & Masonry (Kiến trúc & Xây hoàn thiện)
    # Tuong bao 220
    door_window_area_per_floor = 18.0  # m2
    area_ext_wall = round((perimeter_ext * h * floors) - (door_window_area_per_floor * floors), 2)
    vol_brick_220_m3 = round(area_ext_wall * 0.22, 2)

    # Tuong ngan 110 (estimate based on rooms)
    length_int_walls = (w * 2 + l * 1.5) * floors
    area_int_wall = round((length_int_walls * h) - (12.0 * floors), 2)  # m2

    # Trat tuong (Plastering)
    area_plaster_ext = round(perimeter_ext * h * floors - (door_window_area_per_floor * floors), 2)
    area_plaster_int = round(area_int_wall * 2.0 + area_ext_wall, 2)
    total_plaster = round(area_plaster_ext + area_plaster_int, 2)

    # Son ba (Painting) ~ 3 layers
    area_paint = round(total_plaster + total_floor_area, 2)  # Including ceiling

    # Op lat san & WC (Tiling)
    area_floor_tile = round(total_floor_area * 0.85, 2)
    area_wc_wall_tile = round(num_bathrooms * 18.5, 2)  # 18.5 m2 wall tile per WC

    # Tran thach cao (Gypsum ceiling)
    area_ceiling = round(total_floor_area * 0.80, 2)

    # 3. Doors & Windows
    main_doors_count = 1
    room_doors_count = num_bedrooms + num_bathrooms + 1
    windows_count = floors * 4
    total_door_area = round(main_doors_count * 7.2 + room_doors_count * 2.0 + windows_count * 2.2, 2)

    # 4. MEP Quantities
    outlets_count = floors * 18
    switches_count = floors * 8
    lights_count = floors * 16
    wire_length_m = round(total_floor_area * 14.5, 1)  # m
    pipe_water_m = round(total_floor_area * 3.8, 1)  # m

    # Build structured BOQ item rows
    boq_items = [
        # Phần Kết cấu
        {"stt": "I", "code": "KC-01", "name": "Bê tông lót móng đá 4x6 M100", "unit": "m3", "qty": round(footprint_area * 0.08, 2), "notes": "Dày 100mm"},
        {"stt": "1", "code": "KC-02", "name": "Bê tông móng, giằng móng thương phẩm M250", "unit": "m3", "qty": vol_concrete_footing, "notes": "Móng đài cọc/móng băng"},
        {"stt": "2", "code": "KC-03", "name": "Bê tông cột, dầm, sàn các tầng M250", "unit": "m3", "qty": round(vol_concrete_columns + vol_concrete_beams + vol_concrete_slabs, 2), "notes": "Bê tông thương phẩm R28"},
        {"stt": "3", "code": "KC-04", "name": "Ván khuôn móng, cột, dầm, sàn", "unit": "m2", "qty": area_formwork, "notes": "Ván phủ phim 18mm"},
        {"stt": "4", "code": "KC-05", "name": "Cốt thép các loại (CB300/CB400, d <= 18mm)", "unit": "Tấn", "qty": weight_steel_ton, "notes": f"Tổng cộng {weight_steel_kg} kg"},
        # Phần Xây & Hoàn thiện
        {"stt": "II", "code": "KT-01", "name": "Xây tường bao gạch ống 220 dày 220mm VXM M75", "unit": "m3", "qty": vol_brick_220_m3, "notes": f"DT tường {area_ext_wall} m2 trừ cửa"},
        {"stt": "5", "code": "KT-02", "name": "Xây tường ngăn gạch ống 110 dày 110mm VXM M75", "unit": "m2", "qty": area_int_wall, "notes": "Đã trừ các lỗ cửa đi"},
        {"stt": "6", "code": "KT-03", "name": "Trát tường ngoài nhà dày 1.5cm VXM M75", "unit": "m2", "qty": area_plaster_ext, "notes": "Kèm phụ gia chống thấm"},
        {"stt": "7", "code": "KT-04", "name": "Trát tường trong nhà dày 1.5cm VXM M75", "unit": "m2", "qty": area_plaster_int, "notes": "Trát phẳng chuẩn bị sơn"},
        {"stt": "8", "code": "KT-05", "name": "Láng nền & Lát gạch sàn Granite 800x800", "unit": "m2", "qty": area_floor_tile, "notes": "Phòng khách, bếp, hành lang"},
        {"stt": "9", "code": "KT-06", "name": "Ốp gạch men tường vệ sinh cao kịch trần", "unit": "m2", "qty": area_wc_wall_tile, "notes": f"{num_bathrooms} phòng WC"},
        {"stt": "10", "code": "KT-07", "name": "Sơn bả tường và trần nhà (1 lót 2 phủ Dulux/Jotun)", "unit": "m2", "qty": area_paint, "notes": "Trong & ngoài nhà"},
        {"stt": "11", "code": "KT-08", "name": "Trần thạch cao khung xương chìm Vĩnh Tường", "unit": "m2", "qty": area_ceiling, "notes": "Tấm thạch cao Gyproc 9mm"},
        {"stt": "12", "code": "KT-09", "name": "Hệ thống cửa đi, cửa sổ nhôm kính Xingfa", "unit": "m2", "qty": total_door_area, "notes": "Kính dán an toàn 8.38mm"},
        # Phần MEP
        {"stt": "III", "code": "MEP-01", "name": "Điện chiếu sáng & ổ cắm (Dây Cadivi, Sino/Panasonic)", "unit": "Bộ", "qty": outlets_count + switches_count + lights_count, "notes": f"Gồm {outlets_count} ổ cắm, {lights_count} đèn"},
        {"stt": "13", "code": "MEP-02", "name": "Cấp thoát nước & thiết bị WC (Inax/Toto)", "unit": "Gói", "qty": num_bathrooms, "notes": "Bệt, lavabo, sen tắm, phễu thu sàn"},
    ]

    # Export to CSV if requested
    if output_csv_path:
        abs_csv = os.path.abspath(os.path.expanduser(output_csv_path))
        os.makedirs(os.path.dirname(abs_csv), exist_ok=True)
        with open(abs_csv, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["STT", "Mã hiệu", "Nội dung công việc", "Đơn vị tính", "Khối lượng", "Ghi chú & Công thức tính"])
            for row in boq_items:
                writer.writerow([row["stt"], row["code"], row["name"], row["unit"], row["qty"], row["notes"]])
    else:
        abs_csv = None

    return {
        "project_scope": {
            "frontage_m": w,
            "depth_m": l,
            "footprint_m2": footprint_area,
            "floors": floors,
            "total_floor_area_m2": total_floor_area,
            "floor_height_m": h,
            "bedrooms": num_bedrooms,
            "bathrooms": num_bathrooms,
        },
        "summary": {
            "total_concrete_m3": total_concrete,
            "total_formwork_m2": area_formwork,
            "total_steel_ton": weight_steel_ton,
            "brick_wall_220_m3": vol_brick_220_m3,
            "brick_wall_110_m2": area_int_wall,
            "total_plaster_m2": total_plaster,
            "total_paint_m2": area_paint,
            "total_floor_tile_m2": area_floor_tile,
            "total_doors_m2": total_door_area,
        },
        "boq_items_count": len(boq_items),
        "boq_items": boq_items,
        "csv_export_file": abs_csv,
    }
