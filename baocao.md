# Báo cáo phân tích repo `autocad-ai-mcp`

- **Repo:** https://github.com/haianhdskt-boop/autocad-ai-mcp
- **Nhánh:** `main`
- **Ngày phân tích:** 2026-09-02
- **Phạm vi:** phân tích kiến trúc, tính năng và rà soát lỗi mã nguồn

---

## 1. Tổng quan: repo chứa HAI hệ thống song song, khác thế hệ

Điểm quan trọng nhất: repo trộn lẫn 2 codebase riêng biệt, và tài liệu/mã **không khớp nhau**.

| | `autocad_mcp/` | `autocad_ai/` |
|---|---|---|
| Bản chất | MCP server thao tác **file DXF headless** (dùng `ezdxf`, không cần AutoCAD) | Bộ "Trợ lý KTS" điều khiển **AutoCAD sống** qua COM (Win) / AppleScript (Mac) |
| Entry point | `main.py` → `autocad_mcp.server:main`; `pyproject.toml` script `autocad-mcp` | `autocad_ai.servers.win_server` / `mac_server` |
| Được `pyproject.toml` đóng gói? | ✅ (`include = ["autocad_mcp*"]`) | ❌ **KHÔNG nằm trong `packages.find`** |
| README / install script trỏ tới | ❌ không nhắc | ✅ toàn bộ tài liệu nói về cái này |

→ Thứ được `pip install` đóng gói (`autocad_mcp`) **không phải** thứ mà README và installer chạy (`autocad_ai`). Đây là gốc rễ của nhiều vấn đề bên dưới.

---

## 2. Tính năng

### 2.1 `autocad_ai` — Suite KTS (8 tool tiếng Việt)
Điều khiển AutoCAD đang mở, sinh chuỗi lệnh rồi bắn qua `doc.SendCommand` (COM Windows) hoặc file `.scr` + AppleScript (Mac).

| Tool | Chức năng |
|---|---|
| `cad_ve_moi` | Vẽ mặt bằng kiến trúc mới, phân lớp layer chuẩn |
| `cad_chinh_sua` | Stretch/Move/Mirror/Rotate, đổi layer, xóa đối tượng |
| `cad_hoan_thien_ho_so` | Sinh 11+ bản vẽ TKTC (KT-01…KT-11) + khung tên A3, phân trang động |
| `cad_du_toan` | Bóc khối lượng theo định mức VN → xuất CSV/Excel |
| `cad_kiem_tra` | Audit thông thủy theo Neufert/QCVN, dọn rác (AUDIT/PURGE) |
| `cad_gui_lenh` | Gửi lệnh AutoCAD gốc |
| `cad_in_pdf` | In PDF A3 đen trắng (monochrome.ctb), batch hoặc single sheet |
| `cad_tra_cuu_quy_chuan` | Tra cứu thư viện 7 chuyên đề markdown nhúng sẵn |

### 2.2 `autocad_mcp` — DXF engine (offline, dùng `ezdxf`)
Đọc/tóm tắt/query DXF, thêm/xóa entity & layer, render SVG/PNG/PDF (matplotlib), sinh `.scr`/`.lsp`. Có thêm các server phụ: `file_server`, `render_server`, `live_win_server`, `live_mac_server`.

---

## 3. LỖI NGHIÊM TRỌNG (đã xác nhận)

### 🔴 Lỗi #1 — `cad_ve_moi` hỏng hoàn toàn (cả Win lẫn Mac)
Tool chủ lực "vẽ mặt bằng mới" **luôn ném `TypeError`**.

`autocad_ai/servers/win_server.py` và `mac_server.py` gọi:
```python
build_new_floor_plan_commands(
    frontage_width_mm=frontage_width_mm,
    depth_length_mm=depth_length_mm,   # ← tên tham số này KHÔNG tồn tại
    ...)
```
Nhưng `autocad_ai/core/drawer.py` định nghĩa:
```python
def build_new_floor_plan_commands(width_mm, length_mm, rooms, ...):
```
→ `TypeError: got an unexpected keyword argument 'frontage_width_mm'`. Không vẽ được gì.

**Cách sửa:** trong 2 file server, đổi lời gọi thành:
```python
build_new_floor_plan_commands(
    width_mm=frontage_width_mm,
    length_mm=depth_length_mm,
    ...)
```

### 🔴 Lỗi #2 — `cad_chinh_sua` hỏng hoàn toàn (cả Win lẫn Mac)
Tool "chỉnh sửa" cũng **luôn `TypeError`**.

Server gọi:
```python
build_modify_commands(action=action, target=target, dx=dx, dy=dy,
                      window_p1=..., window_p2=..., new_layer=..., rotation_deg=...)
```
Nhưng `autocad_ai/core/modifier.py` chỉ nhận:
```python
def build_modify_commands(action, target_description, parameters=None):
```
→ `TypeError` do keyword `target/dx/dy/...` không tồn tại.

Ngoài ra **tên action còn lệch**: server gửi `'stretch_room' / 'move_wall' / 'mirror_door' / 'rotate_object' / 'change_layer' / 'delete_object'`, trong khi modifier chỉ hiểu `'move' / 'stretch' / 'resize_room' / 'change_door_swing' / 'flip_door' / 'mirror' / 'change_layer' / 'delete'`. Kể cả khi sửa được kwargs, phần lớn action vẫn rơi vào nhánh generic vô nghĩa.

**Cách sửa:** viết adapter map action + gói `dx/dy/window_*` vào dict `parameters`, hoặc viết lại `build_modify_commands` theo đúng chữ ký mà server dùng.

### 🔴 Lỗi #3 — Bộ test tạo cảm giác an toàn giả
README khẳng định "16/16 unit test Passed 100%", nhưng test **không bắt được** lỗi #1 và #2:
- `test_drawer_commands` / `test_modifier_commands` gọi thẳng hàm core với **chữ ký đúng** (`width_mm=...`), bỏ qua lớp tool MCP nơi có bug.
- `test_servers_registration` chỉ kiểm tra tool **được đăng ký tên**, không **thực thi** chúng.

**Cách sửa:** thêm integration test gọi qua `mcp.call_tool("cad_ve_moi", ...)` và `cad_chinh_sua` để bắt lỗi tầng tích hợp.

---

## 4. Vấn đề đóng gói / cài đặt / tài liệu

- **`autocad_ai` không được đóng gói:** `pyproject.toml` `packages.find` chỉ gồm `autocad_mcp*`. `pip install -e .` chỉ chạy được nhờ editable + cwd; cài **non-editable** (hoặc MCP client chạy ở cwd khác) sẽ `ModuleNotFoundError: autocad_ai`. Ngoài ra file `.md` trong `knowledge/library/` không khai báo `package_data` → tool #8 mất dữ liệu khi cài thật.
- **Installer nói dối "1-chạm tự động cấu hình":** cả `install-win.ps1` và `install-mac.sh` chỉ `echo` dòng "→ Cấu hình vào Claude Desktop..." **mà không ghi bất kỳ file JSON config nào**. Người dùng phải tự tay cấu hình.
- **Ví dụ config trong README sai:**
  - macOS: hardcode đường dẫn cá nhân `/Users/haianh/Desktop/Obsidian/autocad-mcp/.venv/bin/python`.
  - Windows: trỏ `~/.autocad_ai/venv/Scripts/python.exe` nhưng installer lại tạo `.venv` trong thư mục repo → lệch đường dẫn.
- **Số lượng tool mâu thuẫn:** installer in "6 lệnh", README + server khai "8 lệnh".
- **Entry point vô dụng cho sản phẩm chính:** script `autocad-mcp` chỉ chạy DXF server `autocad_mcp`, không liên quan suite `autocad_ai` mà tài liệu quảng bá.

---

## 5. Bảo mật (theo thiết kế nhưng cần cảnh báo)

- **`execute_ezdxf_script` = RCE:** tool này `exec(script_code, ...)` mã Python tùy ý (`autocad_mcp/services/dxf_writer.py`). Bất kỳ prompt injection nào tới model đều có thể chạy code tùy ý trên máy. Nên sandbox hoặc ít nhất ghi cảnh báo rõ ràng.
- **Đường dẫn file không giới hạn:** `validate_dxf_path` chỉ `abspath/expanduser`, không giới hạn thư mục → đọc/ghi/**đè** file bất kỳ trên ổ đĩa qua `create_drawing` / `add_entities` / `delete_entities`.

---

## 6. Lỗi / điểm yếu mức thấp

- **`rgb_to_aci` (`autocad_mcp/utils/color_utils.py`) nhiều khả năng hỏng khi parse màu hex/RGB:** dùng `ezdxf.colors.int2rgb(raw_int).r`, nhưng `int2rgb` thường trả **tuple thường** (không có `.r`) → `AttributeError` (không có try/except). Đáng nghi vì chính hàm `aci_to_rgb` ngay trên lại phải `hasattr(rgb_val, "r")` để phòng thủ. **Cần kiểm chứng** và dùng indexing `rgb[0], rgb[1], rgb[2]`.
- **`import math` đặt ở cuối `autocad_mcp/live/mac_bridge.py`** (sau hàm dùng nó) — chạy được nhờ resolve lúc call-time nhưng dễ vỡ, khó đọc.
- **Độ tin cậy điều khiển AutoCAD:** `doc.SendCommand` là bất đồng bộ, bắn hàng loạt lệnh liên tiếp dễ bị nuốt/đảo lệnh; lệnh `-TEXT` chứa tiếng Việt có dấu (`Phòng Khách`) qua SendCommand dễ lỗi encoding.
- **Bản Mac dùng AppleScript "gõ phím" `_SCRIPT`** → phụ thuộc quyền Accessibility, rất mong manh (không phải COM thật như tên gọi gợi ý).

---

## 7. Khuyến nghị ưu tiên

1. **Sửa ngay lỗi #1 và #2** (chỉ vài dòng ở 2 file server) — hiện 2 tool quan trọng nhất chết hẳn.
2. **Thêm integration test gọi qua tầng MCP tool**, không chỉ test hàm core.
3. **Quyết định 1 codebase**: hoặc gộp `autocad_mcp` (DXF) làm backend cho `autocad_ai`, hoặc tách repo. Hiện tại gây nhầm lẫn lớn.
4. **Sửa `pyproject.toml`** để đóng gói `autocad_ai*` + khai `package_data` cho `knowledge/library/**/*.md`.
5. **Làm installer ghi JSON config thật**, hoặc sửa README bỏ chữ "tự động" và cung cấp đoạn config đúng (đường dẫn tương đối / biến môi trường).
6. **Cảnh báo bảo mật** cho `execute_ezdxf_script` và cân nhắc giới hạn thư mục làm việc.

---

## Phụ lục — Bảng tổng hợp lỗi

| # | Mức độ | Vị trí | Lỗi | Trạng thái |
|---|---|---|---|---|
| 1 | 🔴 Nghiêm trọng | `autocad_ai/servers/win_server.py`, `mac_server.py` (`cad_ve_moi`) | Sai tên tham số → `TypeError`, tool chết | Đã xác nhận |
| 2 | 🔴 Nghiêm trọng | `autocad_ai/servers/*` (`cad_chinh_sua`) vs `core/modifier.py` | Sai chữ ký + lệch tên action → `TypeError` | Đã xác nhận |
| 3 | 🔴 Nghiêm trọng | `tests/test_ai_suite.py` | Test không bắt được lỗi tầng tool | Đã xác nhận |
| 4 | 🟠 Trung bình | `pyproject.toml` | `autocad_ai` không được đóng gói; thiếu `package_data` | Đã xác nhận |
| 5 | 🟠 Trung bình | `install-win.ps1`, `install-mac.sh` | Không ghi config thật dù quảng cáo tự động | Đã xác nhận |
| 6 | 🟠 Trung bình | `README.md` | Config hardcode path cá nhân / lệch path | Đã xác nhận |
| 7 | 🟡 Thấp | `README.md` vs installer | Mâu thuẫn 6 vs 8 tool | Đã xác nhận |
| 8 | 🟡 Bảo mật | `autocad_mcp/services/dxf_writer.py` | `exec()` mã tùy ý (RCE) + path không giới hạn | Theo thiết kế |
| 9 | 🟡 Thấp | `autocad_mcp/utils/color_utils.py` | `int2rgb(...).r` khả năng `AttributeError` | Cần kiểm chứng |
