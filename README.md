# AutoCAD AI MCP - Trợ Lý Kiến Trúc Sư Chuyên Nghiệp

[![FastMCP](https://img.shields.io/badge/MCP-FastMCP%20v4.0-brightgreen.svg)](https://github.com/jlowin/fastmcp)
[![AutoCAD](https://img.shields.io/badge/AutoCAD-2021--2026-red.svg)](https://www.autodesk.com/autocad)
[![Platforms](https://img.shields.io/badge/Platforms-macOS%20%7C%20Windows-lightgrey.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

Hệ sinh thái **Model Context Protocol (MCP)** chuyên biệt hóa dành cho **Kiến Trúc Sư & Kỹ Sư Xây Dựng**. Điều khiển và tương tác trực tiếp theo thời gian thực trên màn hình **AutoCAD (2021 - 2026)** trên cả **macOS** và **Windows**.

---

## ⚡ CÀI ĐẶT 1-CHẠM TỰ ĐỘNG TỪ GITHUB (ZERO BLOAT)

### 🍎 Dành cho máy macOS (Ở nhà):
Chạy lệnh sau trong Terminal (chỉ cài module macOS, không dính mã Windows):
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/autocad-mcp/main/install-mac.sh | bash
```

### 🪟 Dành cho máy Windows (Tại văn phòng):
Chạy lệnh sau trong PowerShell (chỉ cài module COM ActiveX Windows):
```powershell
irm https://raw.githubusercontent.com/YOUR_USERNAME/autocad-mcp/main/install-win.ps1 | iex
```

---

## 🏛️ TRỌN BỘ 6 LỆNH NGHIỆP VỤ CỐT LÕI

```
                  ┌─────────────────────────────────────────────────────────────┐
                  │            TRỢ LÝ AI ĐIỀU KHIỂN AUTOCAD TRỰC TIẾP           │
                  └──────────────┬───────────────────────────────┬──────────────┘
                                 │                               │
            GIAI ĐOẠN THIẾT KẾ & SỬA ĐỔI            GIAI ĐOẠN HỒ SƠ & DỰ TOÁN
            ┌────────────────────────────┐          ┌────────────────────────────┐
            │ 1. ✍️ cad_draw_new         │          │ 3. 📐 cad_finalize_drawing │
            │ (Vẽ mới không gian/tường)  │          │ (Tách bộ 4 bản vẽ thi công)│
            │                            │          │                            │
            │ 2. 🔧 cad_modify           │          │ 4. 📊 cad_estimate         │
            │ (Sửa, dịch tường, đổi cửa) │          │ (Bóc dự toán chi tiết Excel│
            └────────────────────────────┘          └────────────────────────────┘
                                 │                               │
                                 ├───────────────────────────────┤
                                 │ 5. 🔍 cad_inspect (Đo đạc/lỗi)│
                                 │ 6. ⚡ cad_command (Lệnh CAD)  │
                                 └───────────────────────────────┘
```

---

### 1️⃣ `cad_draw_new` — Vẽ Mặt Bằng Kiến Trúc Mới
Vẽ trực tiếp mặt bằng lên không gian Model của AutoCAD theo đúng phân lớp layer chuẩn (`KT_TUONG_220`, `KT_TUONG_110`, `KT_CUA_DI`, `KT_THANG`, `KT_NOITHAT`).
* **Ví dụ ra lệnh**:
  > *"Vẽ mặt bằng nhà phố 5x15m gồm sân trước 2.5m, phòng khách 4.5m, thang 2.5m, bếp 4m, WC và sân sau 1.5m, có bố trí nội thất cơ bản."*

### 2️⃣ `cad_modify` — Sửa Đổi & Di Dời Linh Hoạt
Hiệu chỉnh, di dời mảng tường, co giãn kích thước phòng (`STRETCH`), đảo chiều mở cánh cửa (`MIRROR`), đổi layer trực tiếp trên màn hình.
* **Ví dụ ra lệnh**:
  > *"Kéo rộng phòng khách lùi về phía sau thêm 500mm và đổi cánh cửa phòng ngủ mở vào trong tường."*

### 3️⃣ `cad_finalize_drawing` — Hoàn Thiện Bộ 4 Bản Vẽ Thi Công (TKTC)
Tự động phân tách mặt bằng gốc thành **Bộ 4 bản vẽ triển khai chuyên biệt** lồng sẵn khung tên chuẩn A3:
- **`KT-01` (Kích thước tường xây)**: Tắt nội thất, DIM 3 lớp (chi tiết, tim trục, phủ bì), hatch tường gạch, ghi chú tường 220/110.
- **`KT-02` (Định vị & Ốp lát sàn)**: Tắt nội thất, ghi chú cao độ phòng (`+0.450`), đánh dấu điểm mốc lát đầu tiên ($\otimes$), mũi tên dốc thoát sàn ($i=1.5\%$) WC/ban công.
- **`KT-03` (Bố trí nội thất)**: Đầy đủ đồ nội thất, tag mã hiệu (`SF1`, `TV1`, `BA1`), tên phòng, diện tích thông thủy ($m^2$), bảng thống kê nội thất.
- **`KT-04` (Định vị & Phân loại cửa)**: Lỗ mở cửa thô, tag cửa tròn `D1`, `D2`, `S1`, Bảng chỉ dẫn thông số (Rộng $\times$ Cao, Cốt bậu dưới Sill Height, Cốt lanh-tô Header Height, vật liệu).
* **Ví dụ ra lệnh**:
  > *"Xuất trọn bộ 4 bản vẽ thi công A3 cho mặt bằng tầng 1."* (hoặc xuất riêng từng bản vẽ).

### 4️⃣ `cad_estimate` — Bóc Tách Dự Toán Thi Công Chi Tiết (BOQ)
Tính toán khối lượng toàn diện theo định mức xây dựng Việt Nam và xuất file **Excel / CSV**:
- Bê tông móng, cột, dầm, sàn ($m^3$).
- Ván khuôn phủ phim ($m^2$).
- Cốt thép chi tiết các loại (Tấn / kg).
- Xây tường bao gạch ống 220 ($m^3$) & tường ngăn 110 ($m^2$) đã trừ diện tích cửa.
- Trát tường trong/ngoài ($m^2$), ốp lát gạch nền/WC ($m^2$), sơn bả 3 lớp ($m^2$), trần thạch cao ($m^2$), hệ thống cửa ($m^2$).
- Thiết bị điện chiếu sáng/ổ cắm, thiết bị vệ sinh cấp thoát nước.
* **Ví dụ ra lệnh**:
  > *"Lập bảng dự toán chi tiết công trình 2 tầng 5x15m cao 3.6m xuất ra file Excel du_toan.csv"*

### 5️⃣ `cad_inspect` — Kiểm Tra Diện Tích & Lỗi Bản Vẽ
Kiểm tra diện tích thông thủy, kích thước lọt lòng theo tiêu chuẩn công thái học kiến trúc và chạy lệnh Audit / Purge dọn sạch file rác.
* **Ví dụ ra lệnh**:
  > *"Kiểm tra kích thước thông thủy phòng khách và dọn rác bản vẽ."*

### 6️⃣ `cad_command` — Gửi Lệnh AutoCAD Gốc
Gửi trực tiếp các lệnh AutoCAD như `_.ZOOM _E`, `-PURGE ALL * N`, `_.REGENALL`.

---

## 🔌 CẤU HÌNH VÀO AI CLIENT

### 1. Antigravity IDE / Cursor (`mcp_config.json`):
```json
{
  "mcpServers": {
    "autocad-ai": {
      "command": "/path/to/autocad-mcp/.venv/bin/python",
      "args": ["-m", "autocad_ai.servers.mac_server"]
    }
  }
}
```
*(Trên Windows thay `mac_server` bằng `win_server` và đường dẫn Python tương ứng)*

### 2. Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "autocad-ai": {
      "command": "/path/to/autocad-mcp/.venv/bin/python",
      "args": ["-m", "autocad_ai.servers.mac_server"]
    }
  }
}
```

---

## 🧪 KIỂM THỬ (TEST SUITE)

```bash
source .venv/bin/activate
pytest -v
```
