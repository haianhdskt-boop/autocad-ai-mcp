# AutoCAD & CAD MCP Ecosystem (4 Modular Servers)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastMCP](https://img.shields.io/badge/MCP-FastMCP%20v4.0-brightgreen.svg)](https://github.com/jlowin/fastmcp)
[![AutoCAD](https://img.shields.io/badge/AutoCAD-2021--2026-red.svg)](https://www.autodesk.com/autocad)
[![Platforms](https://img.shields.io/badge/Platforms-macOS%20%7C%20Windows-lightgrey.svg)]()

Hệ sinh thái **Model Context Protocol (MCP)** chuyên biệt hóa dành cho AutoCAD và bản vẽ kỹ thuật CAD (Kiến Trúc - Kết Cấu - Điện Nước), được chia làm **4 Server độc lập** theo nhu cầu công việc.

---

## 📦 4 CẤU TRÚC MCP SERVER CHUYÊN BIỆT

```
                                    ┌───────────────────────┐
                                    │    AUTOCAD MCP SUITE  │
                                    └───────────┬───────────┘
              ┌─────────────────────┬───────────┴───────────┬─────────────────────┐
              ▼                     ▼                       ▼                     ▼
      ┌───────────────┐     ┌───────────────┐       ┌───────────────┐     ┌───────────────┐
      │  cad-file-mcp │     │ cad-render-mcp│       │  cad-live-mac │     │  cad-live-win │
      └───────────────┘     └───────────────┘       └───────────────┘     └───────────────┘
      (Xử lý DXF ngầm)      (Xuất ảnh/PDF)          (AutoCAD for Mac)     (AutoCAD Win COM)
```

---

### 1️⃣ `cad-file-mcp` (Headless File Engine)
- **Mục đích**: Đọc, phân tích, tạo mới, chỉnh sửa cấu trúc hình học và layers trong file DXF.
- **Môi trường**: Mọi OS (Mac, Win, Linux). **Không cần cài hoặc mở AutoCAD**.
- **Lệnh chạy**: `python -m autocad_mcp.servers.file_server`
- **Công cụ**: `file_read_summary`, `file_create_drawing`, `file_add_entities`, `file_extract_texts`, `file_add_layer`, `file_delete_entities`, `file_execute_ezdxf_script`, `file_generate_scr`, `file_generate_lisp`.

### 2️⃣ `cad-render-mcp` (CAD Visualizer & Exporter)
- **Mục đích**: Render bản vẽ CAD ra hình ảnh **PNG 300 DPI** (hỗ trợ dark/light mode), vector **SVG**, hoặc **PDF**.
- **Môi trường**: Mọi OS.
- **Lệnh chạy**: `python -m autocad_mcp.servers.render_server`
- **Công cụ**: `render_to_png`, `render_to_svg`, `render_to_pdf`.

### 3️⃣ `cad-live-mac` (AutoCAD for Mac 2021-2026 Controller)
- **Mục đích**: Điều khiển và vẽ trực tiếp theo thời gian thực trên cửa sổ AutoCAD đang mở trên **macOS** qua AutoLISP / AppleScript.
- **Môi trường**: macOS có cài AutoCAD.
- **Lệnh chạy**: `python -m autocad_mcp.servers.live_mac_server`
- **Công cụ**: `mac_check_autocad_status`, `mac_send_command`, `mac_draw_geometry`, `mac_zoom_extents`.

### 4️⃣ `cad-live-win` (AutoCAD Windows 2021-2026 COM Controller)
- **Mục đích**: Điều khiển và vẽ trực tiếp theo thời gian thực trên cửa sổ AutoCAD đang mở trên **Windows** qua COM ActiveX API (`AutoCAD.Application`).
- **Môi trường**: Windows có cài AutoCAD.
- **Lệnh chạy**: `python -m autocad_mcp.servers.live_win_server`
- **Công cụ**: `win_check_autocad_status`, `win_send_command`, `win_draw_geometry`, `win_zoom_extents`.

---

## 🔌 CẤU HÌNH VÀO MCP CLIENT

Thêm vào file cấu hình của Claude Desktop, Cursor hoặc Antigravity:

### Cấu hình khi làm việc trên macOS (Ở nhà):
```json
{
  "mcpServers": {
    "cad-file": {
      "command": "/Users/haianh/Desktop/Obsidian/autocad-mcp/.venv/bin/python",
      "args": ["-m", "autocad_mcp.servers.file_server"]
    },
    "cad-render": {
      "command": "/Users/haianh/Desktop/Obsidian/autocad-mcp/.venv/bin/python",
      "args": ["-m", "autocad_mcp.servers.render_server"]
    },
    "cad-live-mac": {
      "command": "/Users/haianh/Desktop/Obsidian/autocad-mcp/.venv/bin/python",
      "args": ["-m", "autocad_mcp.servers.live_mac_server"]
    }
  }
}
```

### Cấu hình khi làm việc trên Windows (Tại văn phòng):
```json
{
  "mcpServers": {
    "cad-file": {
      "command": "C:/path/to/autocad-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "autocad_mcp.servers.file_server"]
    },
    "cad-render": {
      "command": "C:/path/to/autocad-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "autocad_mcp.servers.render_server"]
    },
    "cad-live-win": {
      "command": "C:/path/to/autocad-mcp/.venv/Scripts/python.exe",
      "args": ["-m", "autocad_mcp.servers.live_win_server"]
    }
  }
}
```

---

## ⚡ THIẾT LẬP AUTOLISP BRIDGE TRÊN AUTOCAD (Chỉ cần 1 lần)

1. Mở phần mềm AutoCAD.
2. Gõ lệnh `APPLOAD` $\rightarrow$ Chọn file [`autocad_mcp/live/live_bridge.lsp`](file:///Users/haianh/Desktop/Obsidian/autocad-mcp/autocad_mcp/live/live_bridge.lsp).
3. (Tùy chọn) Thêm vào **Startup Suite** để tự động kích hoạt mỗi khi mở AutoCAD.

---

## 🧪 CHẠY KIỂM THỬ (TEST SUITE)

```bash
source .venv/bin/activate
pytest -v
```
