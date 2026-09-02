# Tiền Lượng Kết Cấu Bê Tông Cốt Thép Nhà Dân Dụng (Structural Standards)

Tài liệu hướng dẫn ước tính nhanh (Rules of Thumb) kích thước cấu kiện chịu lực bê tông cốt thép (BTCT) cho nhà phố, biệt thự và nhà ở thấp tầng (1 – 7 tầng) tại Việt Nam theo TCVN 5574:2018.

---

## 1. Hệ Kết Cấu Chịu Lực Nhà Ở Dân Dụng

Tại Việt Nam, gần 100% công trình nhà ở sử dụng hệ **khung bê tông cốt thép toàn khối (Cột + Dầm + Sàn)** kết hợp tường gạch chèn (Infill walls) do điều kiện khí hậu nóng ẩm, tải trọng gió bão và tập quán xây dựng.

```
   TẢI TRỌNG SỬ DỤNG + TỰ TRỌNG
                |
                v
          [ BẢN SÀN BTCT ]
                |
                v
          [ HỆ DẦM CHÍNH / DẦM PHỤ ]
                |
                v
          [ CỘT CHỊU LỰC ]
                |
                v
          [ HỆ MÓNG (ĐƠN / BĂNG / CỌC) ]
                |
                v
          [ NỀN ĐẤT TỰ NHIÊN ]
```

---

## 2. Tiền Lượng Kích Thước Cột BTCT (Columns)

Kích thước tiết diện cột phụ thuộc vào số tầng truyền tải, diện tích sàn đón tải (Tributary area) và nhịp lưới cột (3m – 6m).

### 2.1 Bảng tra kích thước cột sơ bộ theo số tầng (Nhịp 3.5m – 5.0m)
| Số tầng công trình | Cột biên / Cột góc (mm) | Cột giữa / Chịu tải lớn (mm) | Thép chịu lực dọc khuyến nghị |
|---|---|---|---|
| **1 tầng (Trệt)** | 200 x 200 | 200 x 200 – 200 x 250 | 4Ø16 – 4Ø18 |
| **2 – 3 tầng** | 200 x 200 – 200 x 250 | 200 x 300 – 250 x 250 | 4Ø18 – 4Ø20 |
| **4 – 5 tầng** | 200 x 300 – 250 x 250 | 250 x 300 – 300 x 300 | 6Ø18 – 6Ø20 |
| **6 – 7 tầng** | 250 x 300 – 300 x 300 | 300 x 350 – 350 x 350 | 8Ø20 – 8Ø22 |
| **Nhịp lớn (≥6m) hoặc có tầng hầm** | Tăng thêm 1 cấp (300 x 300) | 300 x 400 – 350 x 400 | Tính toán kết cấu chi tiết |

*Quy tắc bố trí cột trong kiến trúc:* Giữ trục cột thẳng đứng liên tục từ móng lên mái (Vertical continuity). Hạn chế tối đa việc "cột nhảy tầng" (cột tầng trên cấy lên giữa dầm tầng dưới) gây dồn ứng suất uốn cắt nguy hiểm cho dầm.

---

## 3. Tiền Lượng Kích Thước Dầm BTCT (Beams)

### 3.1 Quy tắc ước tính nhanh (Rules of Thumb)
- **Chiều cao dầm chính ($h_d$):**
  $$h_d = \left(\frac{1}{10} \div \frac{1}{14}\right) \times L$$
  *(Trong đó $L$ là nhịp dầm - khoảng cách thông thủy giữa 2 cột)*.
- **Chiều rộng dầm ($b_d$):**
  $$b_d = \left(\frac{1}{3} \div \frac{1}{2}\right) \times h_d$$
  *(Bề rộng tối thiểu là 200mm để khớp với tường xây và đảm bảo neo cốt thép)*.
- **Chiều cao dầm phụ / dầm ban công ($h_p$):**
  $$h_p = \left(\frac{1}{12} \div \frac{1}{16}\right) \times L$$

### 3.2 Bảng tra kích thước dầm theo nhịp dầm thực tế
| Nhịp dầm ($L$) | Dầm chính chịu lực (Rộng x Cao mm) | Dầm phụ / Dầm giằng (mm) | Ghi chú |
|---|---|---|---|
| **$L \le 3.0\text{m}$** | 200 x 250 – 200 x 300 | 150 x 200 – 200 x 250 | Nhịp nhỏ phòng ngủ, giếng trời |
| **$L = 3.5\text{m} – 4.0\text{m}$** | 200 x 300 – 200 x 350 | 200 x 250 – 200 x 300 | Nhịp điển hình nhà phố 4m |
| **$L = 4.5\text{m} – 5.0\text{m}$** | 200 x 350 – 250 x 400 | 200 x 300 – 200 x 350 | Nhịp nhà phố 5m hoặc phòng khách liền bếp |
| **$L = 5.5\text{m} – 6.0\text{m}$** | 250 x 450 – 250 x 500 | 200 x 350 – 200 x 400 | Không gian mở, phòng khách rộng |
| **$L > 6.5\text{m}$** | $b \ge 300$, $h \ge 550 – 650$ | 250 x 400 | Cân nhắc dầm bẹt, dầm dự ứng lực hoặc sàn ô cờ |

---

## 4. Chiều Dày Bản Sàn BTCT (Slabs)

- **Công thức tính chiều dày sàn toàn khối ($h_s$):**
  $$h_s = \left(\frac{1}{30} \div \frac{1}{35}\right) \times L_{ngan}$$
- **Bảng chiều dày sàn thực tế nhà ở:**
  - Sàn phòng ngủ, phòng khách thông thường: **$h_s = 100\text{mm} – 120\text{mm}$**.
  - Sàn khu vực nhịp lớn (trên 5m) hoặc gara ô tô: **$h_s = 120\text{mm} – 150\text{mm}$**.
  - Sàn vệ sinh, ban công hạ cốt: **$h_s = 100\text{mm}$** (chú ý chống thấm kỹ).
  - Sàn mái BTCT chống nóng: **$h_s = 100\text{mm} – 120\text{mm}$** (kèm lớp chống nóng và tạo dốc).

---

## 5. Các Loại Móng Công Trình & Điều Kiện Ứng Dụng

| Loại móng | Cấu tạo & Đặc tính | Điều kiện áp dụng phù hợp | Chi phí tương đối |
|---|---|---|---|
| **Móng đơn (Pad footing)** | Móng độc lập dưới từng cột riêng lẻ | Nhà 1 – 2 tầng, nền đất đồi/cát tốt, cứng, không lún | Thấp nhất |
| **Móng băng (Strip footing)** | Dải bê tông chạy dài liên tục theo hàng cột (1 phương hoặc 2 phương) | Nhà 2 – 4 tầng, đất nguyên thổ tương đối tốt | Trung bình |
| **Móng bè (Raft/Mat footing)** | Bản bê tông cốt thép dày trải toàn bộ diện tích đáy nhà | Nhà có tầng hầm, nền đất yếu đồng đều, chống ngập nước | Khá cao |
| **Móng cọc ép BTCT (Driven piles)** | Cọc 200x200 hoặc 250x250mm ép vào tầng đất chịu lực sâu 10–25m | **Phổ biến nhất** cho nhà phố 3–7 tầng tại đồng bằng/đô thị đất yếu | Cao |
| **Móng cọc khoan nhồi (Bored piles)** | Khoan đất đổ bê tông trực tiếp, đường kính Ø400–Ø600mm | Nhà cao tầng (>7 tầng), công trình chen lấn hẻm sâu tránh nứt nhà bên | Cao nhất |

---

## 6. Lanh Tô Cửa & Giằng Tường (Lintels & Tie Beams)

- **Lanh tô cửa (Lintel):** Dầm bê tông cốt thép đổ trên đầu các lỗ mở cửa đi, cửa sổ.
  - Chiều dày lanh tô: Bằng chiều dày tường (110mm hoặc 220mm).
  - Chiều cao lanh tô: Tối thiểu **100 – 150mm** cho cửa rộng <1.5m; cao **200 – 250mm** cho cửa rộng 1.8m – 3.0m.
  - Đoạn gác lên tường 2 bên: **≥ 200 – 250mm** mỗi bên để phân bố tải trọng gạch lên tường.
- **Giằng tường (Tie beam):** Bê tông dày 70 – 100mm chạy vòng quanh tường ở cao độ lanh tô và cao độ áp mái để chống nứt tường khi lún lệch cục bộ.
