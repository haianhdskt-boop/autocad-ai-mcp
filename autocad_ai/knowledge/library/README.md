# Thư viện Tiêu chuẩn & Hướng dẫn Thiết kế Kiến trúc (Architecture Reference Library)

Bộ tài liệu tra cứu kỹ thuật, tiêu chuẩn kích thước, nguyên lý thẩm mỹ, hệ thống kỹ thuật MEP và hướng dẫn thiết kế nhà ở dân dụng (nhà phố, biệt thự, căn hộ) tại Việt Nam.

Toàn bộ tài liệu được biên soạn theo cấu trúc **độc lập (self-contained)**, đầy đủ các bảng thông số kỹ thuật, công thức tính toán và hướng dẫn thực hành xây dựng thực tế. Không còn các liên kết phụ thuộc vào kho sách gốc hay cấu trúc tác nhân nội bộ, sẵn sàng đóng gói và tích hợp vào các hệ thống AI Agent thiết kế kiến trúc.

---

## Cấu trúc Thư mục & Mục lục Tài liệu

```
architecture-reference-library/
├── README.md                                  # Mục lục & hướng dẫn tra cứu
│
├── 01-tieu-chuan-khong-gian/                  # Tiêu chuẩn kích thước & bố cục không gian
│   ├── phong-khach.md                         # Phòng khách: diện tích, sofa, kệ TV, vách accent, cửa sổ lớn
│   ├── bep-va-phong-an.md                     # Bếp & Ăn: tam giác công năng, tủ bếp, modul thiết bị, bàn ăn
│   ├── phong-tam-ve-sinh.md                   # Phòng tắm & WC: kích thước, bố trí thiết bị, chống thấm, dốc
│   ├── phong-ngu-va-tu-ao.md                  # Phòng ngủ: giường, tủ âm tường, bàn phấn, phòng trẻ em theo lứa tuổi
│   ├── cau-thang-va-hanh-lang.md              # Cầu thang & Hành lang: bậc, chiếu nghỉ, 5 dạng thang, ô thang, thoát hiểm
│   ├── sanh-vao-va-phong-lam-viec.md          # Sảnh vào & Phòng làm việc: tủ giày, vùng đệm, bàn công thái học
│   ├── gieng-troi-va-thong-tang.md            # Giếng trời: tỷ lệ diện tích, cấu tạo kính lấy sáng, thoát nước đáy
│   └── gara-san-vuon-ban-cong.md              # Gara & Ngoại thất: bán kính quay xe, độ dốc ram hầm, ban công, sân trước/sau
│
├── 02-ky-thuat-ket-cau-vat-lieu/              # Kỹ thuật kết cấu, vật liệu & chi tiết cấu tạo
│   ├── ket-cau-be-tong-cot-thep.md            # Tiền lượng kết cấu BTCT: kích thước cột, dầm, sàn, móng theo nhịp
│   ├── vat-lieu-hoan-thien-noi-that.md        # Gạch (PEI, R-rating), đá tự nhiên, sàn gỗ (AC), kính, gỗ công nghiệp
│   ├── chi-tiet-cau-tao-kien-truc.md          # 9 mẫu hình kiểm soát nước, bậu cửa sổ, diềm mái, chân tường DPC
│   └── chong-tham-va-xu-ly-am.md              # Giải pháp chống thấm mái, ban công, nhà vệ sinh, tầng hầm
│
├── 03-he-thong-mep-dien-nuoc/                 # Hệ thống kỹ thuật cơ điện & an toàn
│   ├── he-thong-dien-va-chieu-sang.md         # Bố trí ổ cắm theo phòng, quang thông (Lux), nhiệt độ màu (CCT), CRI
│   ├── he-thong-cap-thoat-nuoc.md             # Đường kính ống cấp/thoát, độ dốc, bẫy mùi, hệ thống nước nóng
│   ├── thong-gio-va-dieu-hoa.md               # Bội số trao đổi khí (ACH), công suất BTU theo hướng, vị trí dàn nóng
│   └── an-toan-pccc-va-tre-em.md              # An toàn trẻ em (quy tắc 100mm), kính an toàn, lối thoát hiểm PCCC
│
├── 04-thiet-ke-khi-hau-ben-vung/              # Thiết kế bền vững & khí hậu nhiệt đới
│   ├── thiet-ke-nhiet-doi-gio-mua.md          # Che nắng theo hướng, thông gió chéo, stack effect, mái thông gió
│   └── tiet-kiem-nang-luong-va-cach-nhiet.md  # Trở nhiệt R-value, kính Low-E, ngắt cầu nhiệt, vật liệu xanh
│
├── 05-thiet-ke-tiep-can-da-dung/              # Thiết kế tiếp cận (Universal & Accessible Design)
│   ├── tiep-can-nguoi-cao-tuoi.md             # Bố trí không gian an toàn, thanh vịn, chiếu sáng dẫn đường, sàn chống trượt
│   └── tiep-can-xe-lan-khuyet-tat.md          # Bán kính quay 1500mm, ram dốc 1:12, WC & bếp tiếp cận xe lăn
│
├── 06-nguyen-ly-tham-my-tao-hinh/             # Nguyên lý thị giác, thẩm mỹ & phong cách
│   ├── ty-le-va-to-hop-hinh-khoi.md           # Tỷ lệ vàng, Fibonacci, Modulor, tỷ lệ đặc/rỗng mặt tiền
│   ├── ly-thuyet-mau-sac-kien-truc.md         # Quy tắc 60-30-10, tâm lý học màu sắc, tương quan màu - ánh sáng
│   ├── 8-phong-cach-thiet-ke-chu-dao.md       # Hiện đại, Tối giản, Bắc Âu, Industrial, Japandi, Indochine, Tropical, Neoclassic
│   └── rubric-danh-gia-chat-luong.md          # Ma trận Rubric 9 tiêu chí chấm điểm chất lượng thiết kế
│
└── 07-du-toan-va-quan-ly-du-an/               # Kinh tế xây dựng & tâm lý khách hàng
    ├── suat-dau-tu-va-du-toan-chi-phi.md      # 14 hạng mục chi phí, đơn giá m²XD, hệ số quy đổi m²XD / m²SD
    ├── ho-so-tam-ly-khach-hang.md             # Thói quen sống theo nghề nghiệp, lứa tuổi, phân tầng nhu cầu
    └── quy-trinh-prompt-ai-dien-hoa.md        # Cấu trúc prompt AI diễn họa kiến trúc & nội thất (Midjourney/Flux/Flow)
```

---

## Hướng dẫn Tra cứu Nhanh theo Nhiệm vụ Thiết kế

| Nhiệm vụ của Agent / KTS | Tài liệu cần đọc |
|---|---|
| **Lên ý tưởng ban đầu, thấu hiểu gia chủ** | [ho-so-tam-ly-khach-hang.md](07-du-toan-va-quan-ly-du-an/ho-so-tam-ly-khach-hang.md) · [8-phong-cach-thiet-ke-chu-dao.md](06-nguyen-ly-tham-my-tao-hinh/8-phong-cach-thiet-ke-chu-dao.md) |
| **Phân tích khu đất, hướng nắng gió** | [thiet-ke-nhiet-doi-gio-mua.md](04-thiet-ke-khi-hau-ben-vung/thiet-ke-nhiet-doi-gio-mua.md) |
| **Bố trí mặt bằng công năng, phân chia phòng** | Thư mục [01-tieu-chuan-khong-gian/](01-tieu-chuan-khong-gian/) |
| **Định kích thước sơ bộ cột, dầm, sàn, móng** | [ket-cau-be-tong-cot-thep.md](02-ky-thuat-ket-cau-vat-lieu/ket-cau-be-tong-cot-thep.md) |
| **Thiết kế chi tiết MEP (điện nước điều hòa)** | Thư mục [03-he-thong-mep-dien-nuoc/](03-he-thong-mep-dien-nuoc/) |
| **Lựa chọn vật liệu hoàn thiện sàn, tường, trần** | [vat-lieu-hoan-thien-noi-that.md](02-ky-thuat-ket-cau-vat-lieu/vat-lieu-hoan-thien-noi-that.md) |
| **Kiểm tra an toàn trẻ em & thoát nạn PCCC** | [an-toan-pccc-va-tre-em.md](03-he-thong-mep-dien-nuoc/an-toan-pccc-va-tre-em.md) |
| **Chấm điểm thẩm mỹ và chất lượng đồ án** | [rubric-danh-gia-chat-luong.md](06-nguyen-ly-tham-my-tao-hinh/rubric-danh-gia-chat-luong.md) |
| **Khái toán chi phí & tư vấn ngân sách** | [suat-dau-tu-va-du-toan-chi-phi.md](07-du-toan-va-quan-ly-du-an/suat-dau-tu-va-du-toan-chi-phi.md) |
| **Viết prompt tạo phối cảnh 3D Render AI** | [quy-trinh-prompt-ai-dien-hoa.md](07-du-toan-va-quan-ly-du-an/quy-trinh-prompt-ai-dien-hoa.md) · [ly-thuyet-mau-sac-kien-truc.md](06-nguyen-ly-tham-my-tao-hinh/ly-thuyet-mau-sac-kien-truc.md) |

---

## Nguồn Tài liệu & Cơ sở Tiêu chuẩn Tham chiếu

1. **Tiêu chuẩn Kiến trúc Quốc tế:**
   - *Neufert Architects' Data* (3rd & 4th Edition)
   - *Architectural Graphic Standards* (American Institute of Architects)
   - *The Architecture Reference & Specification Book* (Julia McMorrough)
   - *Time-Saver Standards for Interior Design and Space Planning*
2. **Tiêu chuẩn Thiết kế Bếp & Phòng tắm:**
   - *NKBA Kitchen & Bathroom Planning Guidelines with Access Standards*
3. **Quy chuẩn & Tiêu chuẩn Xây dựng Việt Nam:**
   - QCVN 06:2022/BXD (An toàn cháy cho nhà và công trình)
   - QCVN 04:2021/BXD (Nhà chung cư & công trình nhà ở)
   - QCVN 10:2014/BXD & TCVN 65/2017/QĐ-TTg (Tiếp cận cho người khuyết tật)
   - TCVN 4470:2012, TCVN 9411:2012 (Tiêu chuẩn thiết kế nhà ở liền kề / nhà phố)
4. **Nguyên lý Thẩm mỹ, Bền vững & Kỹ thuật:**
   - Francis D.K. Ching: *Architecture: Form, Space, and Order*, *Building Construction Illustrated*, *Building Structures Illustrated*, *Interior Design Illustrated*, *Green Building Illustrated*
   - Edward Allen & Patrick Rand: *Architectural Detailing: Function, Constructibility, Aesthetics*
   - Corky Binggeli: *Building Systems for Interior Designers*
   - Nick Baker & Koen Steemers: *Healthy Homes: Designing with light and air for sustainability and wellbeing*
