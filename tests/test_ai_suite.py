"""Unit tests for AutoCAD AI MCP Suite."""

import os
import pytest
import tempfile
import asyncio

from autocad_ai.core.drawer import build_new_floor_plan_commands
from autocad_ai.core.modifier import build_modify_commands
from autocad_ai.core.finalizer import (
    build_finalized_sheets_commands,
    build_wall_construction_sheet_commands,
    build_floor_finishes_sheet_commands,
    build_furniture_layout_sheet_commands,
    build_door_schedule_sheet_commands,
)
from autocad_ai.core.estimator import calculate_detailed_construction_boq
from autocad_ai.core.inspector import check_room_clear_dimensions
from autocad_ai.servers.mac_server import mcp as mac_mcp
from autocad_ai.servers.win_server import mcp as win_mcp


def test_drawer_commands():
    """Test generating commands for new floor plan."""
    rooms = [
        {"name": "Phòng Khách", "y_start": 2500, "y_end": 7000, "type": "living"},
        {"name": "Cầu Thang", "y_start": 7000, "y_end": 9500, "type": "stairs"},
    ]
    cmds = build_new_floor_plan_commands(width_mm=5000, length_mm=15000, rooms=rooms)
    cmd_str = " ".join(cmds)

    assert "KT_TUONG_220" in cmd_str
    assert "KT_TUONG_110" in cmd_str
    assert "_.RECTANG" in cmd_str
    assert "Phòng Khách" in cmd_str
    assert "KT_THANG" in cmd_str


def test_modifier_commands():
    """Test modification command generation."""
    move_cmds = build_modify_commands("move", "dịch tường 500mm", {"dx": 500, "dy": 0})
    assert any("_.MOVE" in c for c in move_cmds)

    mirror_cmds = build_modify_commands("flip_door", "đảo chiều cửa phòng")
    assert any("_.MIRROR" in c for c in mirror_cmds)

    stretch_cmds = build_modify_commands("stretch", "kéo dài phòng", {"dx": 300})
    assert any("_.STRETCH" in c for c in stretch_cmds)


def test_finalizer_4_sheets():
    """Test generating all 4 construction documentation sheets."""
    rooms = [
        {"name": "PHÒNG KHÁCH", "y_start": 2500, "y_end": 7000, "type": "living"},
        {"name": "WC", "y_start": 13500, "y_end": 15000, "type": "wc"},
    ]

    # Sheet 1: KT-01 Wall construction
    s1 = build_wall_construction_sheet_commands(5000, 15000, rooms)
    s1_str = " ".join(s1)
    assert "KT-01" in s1_str
    assert "MẶT BẰNG KÍCH THƯỚC TƯỜNG XÂY" in s1_str
    assert "_.DIMLINEAR" in s1_str
    assert "KT_NOITHAT" in s1_str  # Frozen

    # Sheet 2: KT-02 Floor finishes
    s2 = build_floor_finishes_sheet_commands(5000, 15000, rooms)
    s2_str = " ".join(s2)
    assert "KT-02" in s2_str
    assert "MẶT BẰNG ĐỊNH VỊ & ỐP LÁT SÀN" in s2_str
    assert "COT SAN" in s2_str
    assert "DIEM LAT DAU TIEN" in s2_str
    assert "DO DOC" in s2_str

    # Sheet 3: KT-03 Furniture layout
    s3 = build_furniture_layout_sheet_commands(5000, 15000, rooms)
    s3_str = " ".join(s3)
    assert "KT-03" in s3_str
    assert "BANG THONG KE NOI THAT" in s3_str

    # Sheet 4: KT-04 Door schedule
    s4 = build_door_schedule_sheet_commands(5000, 15000, [])
    s4_str = " ".join(s4)
    assert "KT-04" in s4_str
    assert "BANG CHI DAN THONG SO CUA" in s4_str
    assert "D1" in s4_str

    # Full set of 4 sheets
    s_all = build_finalized_sheets_commands("all", 5000, 15000, rooms)
    s_all_str = " ".join(s_all)
    assert "KT-01" in s_all_str
    assert "KT-02" in s_all_str
    assert "KT-03" in s_all_str
    assert "KT-04" in s_all_str


def test_detailed_estimator():
    """Test detailed construction BOQ calculation and CSV export."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        csv_path = tmp.name

    try:
        res = calculate_detailed_construction_boq(
            frontage_w_m=5.0,
            depth_l_m=15.0,
            num_floors=2,
            floor_height_m=3.6,
            num_bedrooms=3,
            num_bathrooms=2,
            output_csv_path=csv_path,
        )

        assert res["project_scope"]["total_floor_area_m2"] == 150.0
        assert res["summary"]["total_concrete_m3"] > 0
        assert res["summary"]["total_steel_ton"] > 0
        assert res["summary"]["brick_wall_220_m3"] > 0
        assert res["boq_items_count"] >= 10
        assert os.path.exists(csv_path)
        assert os.path.getsize(csv_path) > 100
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)


def test_inspector_compliance():
    """Test architectural compliance checking."""
    # Compliant living room
    res_pass = check_room_clear_dimensions(length_mm=5000, width_mm=4000, room_type="living")
    assert res_pass["is_standard_compliant"] is True
    assert res_pass["actual_area_m2"] == 20.0

    # Non-compliant tiny room
    res_fail = check_room_clear_dimensions(length_mm=2000, width_mm=2000, room_type="living")
    assert res_fail["is_standard_compliant"] is False
    assert len(res_fail["warnings"]) > 0


def test_plotter_commands():
    """Test standardized PDF plot command generation."""
    from autocad_ai.core.plotter import build_plot_single_sheet_commands, build_batch_plot_commands

    single = build_plot_single_sheet_commands(
        sheet_code="KT-01",
        window_p1=[-2000, -3000],
        window_p2=[12000, 17000],
        output_pdf_path="/tmp/test_kt01.pdf",
        paper_size="A3",
        plot_style="monochrome.ctb",
    )
    cmd_str = " ".join(single)
    assert "-PLOT" in cmd_str
    assert "DWG To PDF.pc3" in cmd_str
    assert "ISO full bleed A3" in cmd_str
    assert "monochrome.ctb" in cmd_str

    batch = build_batch_plot_commands(output_directory="/tmp/cad_test_batch")
    assert batch["sheet_count"] == 4
    assert len(batch["pdf_files"]) == 4


def test_servers_registration():
    """Test that all 7 core business commands are registered on Mac and Win servers."""
    expected_tools = {
        "cad_draw_new",
        "cad_modify",
        "cad_finalize_drawing",
        "cad_estimate",
        "cad_inspect",
        "cad_command",
        "cad_plot",
    }

    mac_tools = {t.name for t in asyncio.run(mac_mcp.list_tools())}
    assert expected_tools.issubset(mac_tools)

    win_tools = {t.name for t in asyncio.run(win_mcp.list_tools())}
    assert expected_tools.issubset(win_tools)

