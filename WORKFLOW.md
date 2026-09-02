# Quy Trình Làm Việc Tiêu Chuẩn (SOP) & Bộ Quy Chuẩn Thiết Kế

Tài liệu này quy định **Cấu trúc kiểm soát quy chuẩn kiến trúc trước khi vẽ** và **2 Quy trình làm việc chuẩn mực (SOP)** giữa Kiến Trúc Sư và Trợ lý AI dựa trên thư viện chuẩn [architecture-reference-library](https://github.com/haianhdskt-boop/architecture-reference-library) được đóng gói trực tiếp trong mã nguồn (`autocad_ai/knowledge/`).

---

## 📐 BỘ QUY CHUẨN KIỂM SOÁT KIẾN TRÚC TRƯỚC KHI VẼ (PRE-DRAFTING RULES)

Trước khi đề xuất phương án, vẽ mặt bằng hoặc chỉnh sửa, AI **BẮT BUỘC** phải rà soát qua bảng ngưỡng tiêu chuẩn công thái học & kỹ thuật sau để không bao giờ vẽ sai:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               BẢNG THÔNG SỐ CÔNG THÁI HỌC & KÍCH THƯỚC TỐI THIỂU            │
├───────────────────────┬───────────────────────────────┬─────────────────────┤
│ HẠNG MỤC KHÔNG GIAN   │ KÍCH THƯỚC THÔNG THỦY TỐI THIỂU│ TIÊU CHUẨN THAM CHIẾU│
├───────────────────────┼───────────────────────────────┼─────────────────────┤
│ 1. Hành lang chính    │ Rộng >= 1100mm (phụ >= 900mm) │ Neufert & QCVN 04   │
│ 2. Cầu thang bộ       │ Vế thang >= 900mm; Chiếu nghỉ │ h = H/N (150-175mm) │
│                       │ >= 900mm; b = 250mm           │ b_hoàn thiện = 270mm│
│ 3. Lan can an toàn    │ Cao >= 900mm (vế), >= 1100mm  │ Khe hở nan đứng     │
│                       │ (thông tầng); Nan đứng <= 100mm│ an toàn trẻ em <=100│
│ 4. Phòng Khách        │ Diện tích >= 16m2; Rộng >=3.6m│ Cự ly xem TV >= 2.5m│
│ 5. Bếp & Phòng Ăn     │ Diện tích >= 12m2; Lối đi bếp │ Tam giác công năng  │
│                       │ >= 1000..1200mm; Bàn-tường 800│ Chu vi 4.0 - 7.5m   │
│ 6. Phòng Ngủ Master   │ Diện tích >= 14m2; Rộng >=3.3m│ Hở 2 bên giường 700 │
│ 7. Phòng Ngủ Đơn/Con  │ Diện tích >= 9m2; Rộng >= 2.7m│ Kê giường 1.2 - 1.4m│
│ 8. Vệ Sinh Tiêu Chuẩn │ Diện tích >= 3.2m2; Rộng >=1.4m│ Bệt hở trước >=600mm│
│                       │ Khoang tắm đứng >= 900x900mm  │ Hạ cốt sàn 30-50mm  │
│ 9. Giếng trời / Thông │ Nhà sâu >= 12m: Bắt buộc có ô │ Hiệu ứng ống khói   │
│    tầng lấy sáng      │ thang/giếng trời >= 5% sàn    │ Stack Effect        │
│ 10. Gara ô tô         │ Rộng >= 3.0m x Dài >= 5.5m    │ Độ dốc ram <= 15%   │
└───────────────────────┴───────────────────────────────┴─────────────────────┘
```

---

## 🏛️ QUY TRÌNH 1: THIẾT KẾ MẶT BẰNG MỚI (5 BƯỚC)

```mermaid
flowchart TD
    A["Bước 1: Nạp Nhiệm Vụ Thiết Kế\n(Khu đất, nhu cầu phòng, phong cách, ảnh mẫu)"] --> B["Bước 2: Phân Tích Quy Chuẩn & Đề Xuất Bố Trí\n(Tra cứu cad_tra_cuu_quy_chuan; Mô tả giao thông, giếng trời)"]
    B --> C{"KTS Chốt\nPhương Án?"}
    C -- "Chưa / Cần chỉnh" --> B
    C -- "ĐÃ CHỐT" --> D["Bước 3: Triển Khai Vẽ Trực Tiếp Lên AutoCAD\n(Gọi cad_ve_moi theo đúng phân lớp layer)"]
    D --> E["Bước 4: Tự Kiểm Tra (QA/QC) & Tự Nắn Chỉnh\n(Gọi cad_kiem_tra đối chiếu toàn diện quy chuẩn)"]
    E --> F["Bước 5: Báo Cáo Hoàn Thành Cho KTS\n(Bảng diện tích m2, danh sách chuẩn đã đạt)"]
```

### Chi tiết từng bước:

#### 🔹 Bước 1: Nạp Nhiệm Vụ Thiết Kế
* **KTS cung cấp**:
  - **Quy mô & Kích thước**: Chiều rộng mặt tiền ($W$), chiều sâu khu đất ($L$), số tầng, chiều cao tầng.
  - **Nhu cầu công năng**: Danh sách các phòng (Khách, Bếp, Thang, số lượng Phòng ngủ, WC, Sân trước/sau, Giếng trời, Phòng thờ).
  - **Sở thích & Phong cách**: Hiện đại, tối giản, Indochine, phong thủy (vị trí bếp, hướng ban thờ, cung bậc thang).
  - **Tài liệu đính kèm**: Ảnh chụp hiện trạng, ảnh phối cảnh tham khảo đặt trong thư mục dự án hoặc gửi trực tiếp lên khung chat.

#### 🔹 Bước 2: Phân Tích Quy Chuẩn & Đề Xuất Phương Án (Concept Proposal)
* **AI thực hiện**:
  - Gọi công cụ **`cad_tra_cuu_quy_chuan`** để tra cứu:
    - *Mặt tiền & Sân trước*: Kích thước để xe (Gara $\ge 3.0 \times 5.5\text{m}$), khoảng lùi.
    - *Phòng khách*: Diện tích $\ge 16\text{m}^2$, bề ngang $\ge 3.6\text{m}$, cự ly xem TV $2.5 - 4.0\text{m}$.
    - *Cầu thang & Giếng trời*: Số bậc theo cung Sinh ($h = H/N$, $b=250/270\text{mm}$), ô giếng trời $\ge 5\%$ diện tích sàn tạo hiệu ứng ống khói (Stack Effect) hút gió tầng lầu.
    - *Bếp & Phòng ăn*: Tam giác công năng (Tủ lạnh - Chậu rửa - Bếp nấu) chu vi $4.0 - 7.5\text{m}$, lối đi giữa 2 dãy tủ $\ge 1.0 - 1.2\text{m}$.
    - *Phòng ngủ*: Master $\ge 14\text{m}^2$ (hở 2 bên giường $\ge 700\text{mm}$), phòng ngủ con $\ge 9\text{m}^2$.
    - *Vệ sinh*: WC 3 khu khô-ướt tách biệt $\ge 3.2\text{m}^2$, hạ cốt sàn $30 - 50\text{mm}$, độ dốc thoát nước $i = 1.5\%$.
    - *Hành lang*: Đảm bảo thông thủy $\ge 1100\text{mm}$ (hành lang chính) và $\ge 900\text{mm}$ (hành lang phụ).
  - **QUY TẮC BẮT BUỘC**: AI trình bày phương án rõ ràng để thảo luận cùng KTS và **CHỜ KTS XÁC NHẬN "CHỐT PHƯƠNG ÁN"** mới được vẽ. Không tự ý vẽ khi chưa có sự đồng thuận.

#### 🔹 Bước 3: Triển Khai Vẽ Trực Tiếp Lên AutoCAD
* **AI thực hiện**:
  - Gọi công cụ **`cad_ve_moi`** để vẽ trực tiếp từng đối tượng lên AutoCAD theo đúng phương án đã chốt.
  - Phân loại đúng các lớp layer chuẩn:
    - `KT_TUONG_220`: Tường bao ngoài, cột chịu lực (Màu 1 - Đỏ).
    - `KT_TUONG_110`: Tường ngăn phòng (Màu 2 - Vàng).
    - `KT_CUA_DI`: Cửa đi chính, cửa phòng, cửa WC (Màu 3 - Xanh lá).
    - `KT_CUA_SO`: Cửa sổ lấy sáng, lấy gió (Màu 4 - Cyan).
    - `KT_THANG`: Bậc thang, tim thang, mũi tên UP (Màu 5 - Blue).
    - `KT_NOITHAT`: Sofa, bàn ăn, bếp, bệt, lavabo (Màu 8 - Xám).
    - `KT_TEXT`: Tên phòng và diện tích (Màu 7 - Trắng).

#### 🔹 Bước 4: Tự Kiểm Tra (QA/QC) & Tự Hiệu Chỉnh
* **AI thực hiện**:
  - Tự động gọi **`cad_kiem_tra` (action: 'audit_full_plan')** kiểm tra:
    - Rà soát toàn bộ kích thước lọt lòng và diện tích phòng xem có phòng nào bị hẹp dưới ngưỡng tiêu chuẩn không.
    - Kiểm tra nút thắt giao thông hành lang, khoảng mở cánh cửa không bị va đập vào thiết bị vệ sinh hay giường tủ.
    - Đối chiếu tọa độ các phòng trên AutoCAD với phương án đã chốt ở Bước 2.
  - Nếu phát hiện nét hở hoặc phòng chưa khớp, AI **tự động nắn chỉnh sửa lại ngay** trước khi bàn giao.

#### 🔹 Bước 5: Báo Cáo Hoàn Thành Cho KTS
* **AI thực hiện**:
  - Báo cáo rõ ràng:
    - Bảng tổng hợp diện tích xây dựng và diện tích thông thủy chi tiết từng phòng.
    - Danh sách các tiêu chuẩn công thái học và an toàn đã được đáp ứng.
    - Mời KTS kiểm tra thực tế trên màn hình AutoCAD.

---

## 🔧 QUY TRÌNH 2: CHỈNH SỬA & HIỆU CHỈNH BẢN VẼ (4 BƯỚC)

```mermaid
flowchart TD
    M1["Bước 1: KTS Kiểm Tra & Ra Lệnh Chỉnh Sửa\n(Dịch tường, đổi kích thước, đảo cửa)"] --> M2["Bước 2: AI Thực Hiện Sửa Trực Tiếp Trên AutoCAD\n(Gọi cad_chinh_sua - Stretch, Move, Mirror)"]
    M2 --> M3["Bước 3: Tự Kiểm Tra Quy Chuẩn Sau Sửa\n(Gọi cad_kiem_tra đảm bảo phòng bị co lại vẫn đạt chuẩn)"]
    M3 --> M4["Bước 4: Báo Cáo Hoàn Thành Cho KTS\n(Zoom đến vị trí vừa sửa, báo kích thước mới)"]
```

### Chi tiết từng bước:

#### 🔹 Bước 1: KTS Tiếp Nhận & Yêu Cầu Chỉnh Sửa
* KTS quan sát bản vẽ trên màn hình AutoCAD và đưa ra phản hồi:
  - *"Kéo phòng khách rộng thêm 500mm lùi về phía sau."*
  - *"Đảo cánh cửa phòng ngủ mở vào trong góc tường bên trái."*

#### 🔹 Bước 2: AI Thực Hiện Chỉnh Sửa Trực Tiếp
* AI phân tích đối tượng và vùng ảnh hưởng $\rightarrow$ Gọi công cụ **`cad_chinh_sua`**:
  - Dùng lệnh `STRETCH` co giãn mảng tường và không gian phòng.
  - Dùng lệnh `MOVE` di dời vị trí thiết bị nội thất / cửa.
  - Dùng lệnh `MIRROR` / `ROTATE` đảo chiều mở cửa.

#### 🔹 Bước 3: Tự Kiểm Tra Lại Kết Quả Sau Sửa (Rà Soát Xung Đột)
* AI tự động gọi **`cad_kiem_tra`**:
  - Việc nới rộng phòng này có làm **phòng bên cạnh bị bóp hẹp dưới diện tích tối thiểu** hay không (ví dụ dời tường phòng khách làm phòng bếp bị hẹp < 12m² hoặc hành lang bị hẹp < 900mm).
  - Tự động nắn chỉnh lại các đối tượng nội thất và đường Dim liên quan.

#### 🔹 Bước 4: Báo Cáo Hoàn Thành Cho KTS
* AI gửi lệnh `_.ZOOM _E` (qua `cad_gui_lenh`) hoặc zoom vào vùng vừa sửa.
* Thông báo cho KTS: Đối tượng nào đã được thay đổi, kích thước mới sau khi sửa và mời KTS nghiệm thu.
