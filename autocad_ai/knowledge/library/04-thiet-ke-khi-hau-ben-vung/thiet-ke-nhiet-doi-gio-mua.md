# Thiết Kế Kiến Trúc Khí Hậu Nhiệt Đới Gió Mùa (Tropical Architecture)

Khí hậu nhiệt đới gió mùa tại Việt Nam đặc trưng bởi bức xạ mặt trời gay gắt, độ ẩm cao (thường xuyên >80%), lượng mưa lớn theo mùa và gió mùa đổi hướng (gió Đông Nam mát mùa hè, gió Đông Bắc lạnh mùa đông). Thiết kế thụ động (Passive Design) là chìa khóa tạo vi khí hậu mát mẻ, tiết kiệm điện năng.

---

## 1. Nguyên Tắc Che Nắng Theo 4 Hướng Nhà (Solar Shading)

```
          [ HƯỚNG BẮC ] - Ánh sáng dịu, mát quanh năm, ưu tiên mở cửa kính lớn
                 |
  [ HƯỚNG TÂY ] -+- [ HƯỚNG ĐÔNG ]
  Nắng chiều gay gắt nhất        Nắng sáng sớm góc thấp
  -> Lam đứng + Vỏ kép 2 lớp     -> Lam đứng / Lam chớp
                 |
          [ HƯỚNG NAM ] - Đón gió mát, góc nắng cao giữa trưa
          -> Mái hiên / Mái đua ngang (Overhang)
```

### 1.1 Bảng giải pháp che nắng theo từng hướng nhà
| Hướng nhà | Đặc điểm bức xạ mặt trời | Giải pháp che nắng tối ưu | Tỷ lệ kích thước cấu kiện |
|---|---|---|---|
| **Hướng Nam & Đông Nam** | Nắng chiếu góc cao vào giữa trưa; đón gió mát chủ đạo mùa hè | **Mái hiên ngang (Horizontal overhang) hoặc ô văng** | Độ vươn mái hiên đua ra bằng **$25\% – 30\%$** chiều cao cửa sổ |
| **Hướng Bắc & Đông Bắc** | Ít bị nắng trực tiếp chiếu xiên, ánh sáng tán xạ dịu; gió lạnh mùa đông | Hạn chế che chắn, ưu tiên lấy sáng tự nhiên; cửa có gioăng kín gió đông | Cửa sổ kính lớn hoặc lam kính đóng mở |
| **Hướng Đông** | Nắng sáng góc thấp chiếu sâu vào phòng gây chói | **Hệ lam đứng (Vertical louvers)** hoặc lam chéo | Lam đứng xoay góc $45°$ cản nắng xiên sáng |
| **Hướng Tây & Tây Nam** | **Nắng chiều bức xạ cực mạnh**, tích nhiệt vào bê tông tỏa nhiệt đến đêm | **Mặt đứng vỏ kép (Double-skin facade) + Lam đứng + Cây xanh + Tường 2 lớp** | Tường gạch 2 lớp (có khoang khí 50mm) hoặc lam bê tông đục lỗ |

---

## 2. Nguyên Lý Thông Gió Tự Nhiên (Natural Ventilation)

### 2.1 Thông gió chéo (Cross Ventilation)
- **Nguyên lý:** Không khí di chuyển từ vùng áp suất cao (mặt đón gió) sang vùng áp suất thấp (mặt khuất gió).
- **Yêu cầu bố trí cửa:**
  - Cửa đón gió vào (Inlet) và Cửa thoát gió ra (Outlet) phải đặt ở 2 mặt tường đối diện hoặc vuông góc nhau.
  - **Diện tích cửa thoát gió ra nên lớn hơn hoặc bằng cửa đón gió vào ($S_{out} \ge S_{in}$)** để tăng tốc độ luồng gió đi xuyên phòng (hiệu ứng Venturi).

```
       Gió vào (Inlet)                              Gió ra (Outlet)
       ===================+                  +=====================
            --->          |   PHÒNG SINH HOẠT|            --->
            --->          |   (Thông thoáng) |            --->
       ===================+                  +=====================
```

### 2.2 Hiệu ứng ống khói (Stack Effect / Thermal Buoyancy)
- **Nguyên lý:** Không khí nóng nhẹ hơn bốc lên cao và thoát ra ngoài qua đỉnh giếng trời, tạo áp suất âm ở tầng dưới hút không khí mát từ sân trước/sân sau vào nhà.
- **Ứng dụng:** Thiết kế giếng trời giữa nhà kết hợp thông tầng cầu thang, có cửa thoát nhiệt trên mái.

---

## 3. Cấu Tạo Mái Hai Lớp Thông Gió Chống Nóng (Double-Skin Roof)

```
   Ánh nắng mặt trời
        \\\\\\\\\
     =======================  <- Lớp 1: Ngói lợp / Tấm lợp che nắng
     -----------------------
     ~~~~~~~~~~~~~~~~~~~~~~~  <- KHOANG ĐỆM KHÍ THÔNG GIÓ (Hở 100 - 150mm)
     =======================  <- Lớp 2: Sàn BTCT + Xốp XPS cách nhiệt 50mm
     -----------------------
        TRẦN THẠCH CAO
```

- **Cơ chế:** Lớp mái ngoài hấp thụ bức xạ mặt trời và bức xạ nhiệt trở lại khí quyển; luồng gió lưu thông trong khoang đệm cuốn phăng nhiệt lượng trước khi nhiệt truyền xuống sàn bê tông tầng áp mái.
- **Vật liệu cách nhiệt sàn mái:** Sử dụng tấm xốp **XPS (Extruded Polystyrene)** dày **50mm** cường độ nén cao kết hợp lớp vữa tạo dốc và lát gạch chống nóng.

---

## 4. Cây Xanh & Mặt Nước Điều Hòa Vi Khí Hậu

- **Hiệu ứng làm mát bốc thoát hơi nước (Evaporative cooling):** Bố trí hồ cá Koi, thác nước mini hoặc bồn cây xanh ở hướng đón gió (sân trước hoặc đáy giếng trời). Khi gió khô nóng thổi qua mặt nước và tán lá cây, nhiệt độ không khí giảm từ **2°C – 4°C** và độ ẩm tăng thêm, mang lại cảm giác mát mẻ tự nhiên.
- **Mặt đứng xanh (Green Facade):** Trồng giàn cây dây leo (cúc tần Ấn Độ, hoa giấy, sử quân tử) tạo lớp rèm sinh học che chắn 100% tia nắng trực tiếp chiếu vào tường hướng Tây.
