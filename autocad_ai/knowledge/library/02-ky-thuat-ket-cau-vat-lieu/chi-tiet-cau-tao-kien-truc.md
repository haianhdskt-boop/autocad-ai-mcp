# Chi Tiết Cấu Tạo Kiến Trúc Bao Che (Architectural Detailing)

Tài liệu chi tiết cấu tạo kiểm soát nước mưa, kiểm soát nhiệt, ngăn ngừa ẩm mốc và đảm bảo độ bền vững cho lớp vỏ bao che công trình (Building Envelope) theo nguyên lý Edward Allen.

---

## 1. 9 Mẫu Hình Kiểm Soát Nước Mưa Cốt Lõi (Water Control Patterns)

```
  1. TẠO DỐC (Wash)         2. CHỒNG LỚP (Overlap)     3. NHÔ RA & RỈ NƯỚC (Drip)
        \                         ===                      -------+
         \                          ===                           |  <- Rãnh Drip
          \                           ===                         +-+
  -----------------         ------------------         ------------------

  4. THOÁT & LỖ THOÁT       5. NGẮT ẨM (DPC)          6. NGẮT MAO DẪN
      |   |                     ==========                |   |
      |   v Lỗ Weep             ----------                |   | Khe hở >= 6mm
      +---+                     ==========                +---+
```

| # | Mẫu hình | Nguyên lý vật lý | Ứng dụng cấu tạo thực tế |
|---|---|---|---|
| **1** | **Tạo dốc (Wash)** | Mặt phẳng nghiêng dẫn nước chảy đi nhanh bằng trọng lực | Bậu cửa sổ dốc ra ngoài $ge 1:10$; sàn ban công dốc $1.5\%$; mái dốc |
| **2** | **Chồng lớp (Overlap)** | Lớp trên phủ mép lớp dưới theo chiều trọng lực | Ngói lợp nhà, tấm ốp tường conwood, tôn lợp |
| **3** | **Nhô ra & Rãnh rỉ nước (Overhang & Drip groove)** | Mép nhô ra khỏi mặt tường $ge 25\text{mm}$ + Rãnh soi cắt dòng nước bám đáy | Mũi bậu cửa, gờ mép ban công, diềm mái đón |
| **4** | **Thoát nước & Lỗ thoát (Drain & Weep holes)** | Thu gom nước đã vô tình xâm nhập và dẫn ra ngoài | Lỗ thoát nước đáy khung nhôm kính, ống thoát đáy bồn hoa |
| **5** | **Lớp ngắt ẩm (Moisture Break / DPC)** | Màng chống thấm liên tục ngăn ẩm thẩm thấu | Màng DPC chân tường, màng chống thấm đáy sàn WC |
| **6** | **Ngắt mao dẫn (Capillary Break)** | Khoảng hở $ge 6\text{mm}$ phá vỡ lực hút mao dẫn của khe hẹp | Khe hở giữa 2 lớp tường đôi, rãnh khuyết dưới bậu cửa sổ |
| **7** | **Đường ziczac mê cung (Labyrinth)** | Bẻ cong đường đi khiến gió mưa không thể tạt thẳng | Nẹp che khe co giãn, hèm cửa sổ nhôm đa khoang |
| **8** | **Tường rèm cân bằng áp (Rainscreen)** | Khoang không khí thông gió phía sau lớp ốp ngoài cân bằng áp suất | Mặt dựng ốp tấm nhôm/đá thông gió (Ventilated facade) |
| **9** | **Gờ chắn đứng (Upstand)** | Gờ bê tông/gạch nhô cao ngăn nước tràn ngang | Gờ chắn ban công, cổ trần giếng trời cao $ge 300\text{mm}$ |

---

## 2. Chi Tiết Bậu Cửa Sổ Chống Thấm (Window Sill Detail)

```
       [ MẶT KÍNH CỬA SỔ ]
              |
       +------|------+  <- Khung nhôm có gioăng EPDM kép
       |   KHUNG ĐÁY |
       +------|------+
         | |  |  | |    <- Keo Silicone kết cấu chịu thời tiết
    =====+=+==+==+=+===================================+
    \\ BẬU CỬA BÊ TÔNG / ĐÁ HOA CƯƠNG                 |
     \\ Độ dốc ra ngoài >= 1:10                       |  MẶT TƯỜNG TRONG
      \\                                              |
       +----+                                          |
            | <- Rãnh soi giọt nước (Drip groove 8x8mm)|
            +------------------------------------------+
                               |
                        MẶT TƯỜNG NGOÀI
```

- **Độ dốc bậu cửa sổ:** Dốc nghiêng ra phía ngoài tối thiểu **1:10 (10%)**.
- **Mũi nhô bậu cửa:** Nhô ra khỏi mặt tường ngoài tối thiểu **25 – 35mm**.
- **Rãnh rỉ nước (Drip groove):** Soi rãnh rộng **8mm x sâu 8mm** ở mặt dưới mũi nhô, cách mép ngoài 15mm.
- **Bơm keo Silicone:** Sử dụng keo Silicone trung tính chuyên dụng ngoài trời (như Dow Corning/Dowsil 791) bịt kín toàn bộ khe hở giữa khung nhôm và tường xây.

---

## 3. Chi Tiết Diềm Mái & Máng Xối (Eave & Gutter Detail)

- **Độ đua diềm mái (Overhang):** Mái hiên/mái ngói đua ra tối thiểu **600 – 800mm** khỏi mặt tường để che mưa tạt và tạo bóng đổ che nắng tường ngoài.
- **Máng xối thu nước mái (Gutter):**
  - Máng xối âm sê-nô BTCT: Đổ gờ bê tông cao $ge 200\text{mm}$, quét chống thấm 2 lớp, láng vữa tạo dốc $ge 1\%$ về phễu thu nước.
  - Phễu thu nước mái (Quả cầu chắn rác): Đặt quả cầu chắn rác inox 304 chụp trên đầu ống thu nước $\varnothing 110\text{mm}$ để chống tắc nghẽn do lá cây.

---

## 4. Chi Tiết Chân Tường Chống Ẩm Ngược (DPC Detail)

```
   SÀN GỖ NỘI THẤT               TƯỜNG GẠCH NỘI THẤT
         |                                |
         |     +--------------------------+
         |     | Gạch đặc xây chèn        |
         v     +==========================+ <- Màng ngắt ẩm DPC (Cao hơn sàn 150mm)
   [LỚP VỮA]   | Lớp vữa chống thấm       |
   [SÀN BTCT]  +--------------------------+
```

- **Vấn đề mao dẫn chân tường (Rising damp):** Nước ngầm từ đất tự nhiên ngấm qua móng bê tông hút ngược lên tường gạch gây bong tróc sơn, rêu mốc chân tường cao 0.5m – 1m.
- **Giải pháp xử lý:**
  - Đặt màng ngắt ẩm **DPC (Damp Proof Course)** bằng màng bitum dán nóng hoặc quét 3 lớp vữa xi măng chống thấm tinh thể thẩm thấu tại cao độ **+0.150m** (trên mặt sàn hoàn thiện).
  - 3 hàng gạch dưới cùng của chân tường phải xây bằng **gạch đặc (gạch thẻ nung)** thay vì gạch lỗ để giảm thiểu rỗng mao dẫn.
