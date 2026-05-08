# 🎯 Dashboard & DAX: Ma trận Chiến lược Ngành - Sản phẩm

Góc nhìn thứ 6 là góc nhìn về **Chiến lược thâm nhập (Strategic Fit)**. Chúng ta đi tìm sự giao thoa hoàn hảo giữa "Ngành nghề" và "Dòng sản phẩm" để trả lời câu hỏi: *"Sản phẩm của chúng ta đang thực sự thắng ở đâu và thua ở đâu?"*

---

## 📈 Trực quan hóa (Dashboards)

````carousel
![Ma trận Chiến lược Ngành - Sản phẩm](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/strategic_matrix.png)
<!-- slide -->
![Top 10 Cặp Ngành - Sản phẩm (Pareto)](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/pareto_combos.png)
<!-- slide -->
![Hiệu quả Ngành: Tốc độ vs Tỷ lệ thắng](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/industry_efficiency.png)
````

---

## 🔢 Công thức DAX cho Chiến lược Ngành - Sản phẩm

### 1. Tỷ trọng Doanh thu của Cặp Industry-Product (Pareto Pct)
*Giúp xác định nhóm 20% các cặp mang lại 80% doanh thu:*
```dax
Cumulative Revenue Pct = 
VAR CurrentRevenue = [Total Revenue]
VAR TotalAll = CALCULATE([Total Revenue], ALL('CRM_data'))
RETURN DIVIDE(CurrentRevenue, TotalAll, 0)
```

### 2. Chỉ số Market Fit Index (MFI)
*Điểm số đánh giá mức độ "hợp" của sản phẩm với ngành (Kết hợp Win Rate và Speed):*
```dax
Market Fit Index = 
VAR WinRateScore = [Win Rate %] / 100
VAR SpeedScore = 1 - DIVIDE([Avg Days to Won], MAXX(ALL('CRM_data'), [Avg Days to Won]))
RETURN (WinRateScore * 0.7) + (SpeedScore * 0.3)
```

### 3. Tỷ lệ rớt đơn theo Ngành (Industry Loss Rate)
```dax
Industry Loss Rate = 
CALCULATE(
    COUNTROWS('CRM_data'),
    'CRM_data'[Status] IN {"Disqualified", "Churned Customer"}
) / CALCULATE(COUNTROWS('CRM_data'), ALL('CRM_data'[Product]))
```

---

## 💡 Giải thích ý nghĩa Quản trị (Perspective)

1.  **Ma trận Chiến lược (Heatmap):** 
    *   Bạn sẽ thấy những "vùng xanh" (Win rate cao) và "vùng đỏ" (Win rate thấp).
    *   **Insight:** Ngành **Education & Science** khi kết hợp với sản phẩm **SAAS** có tỷ lệ thắng cực cao (gần 65%). Đây là thị trường bạn nên "đánh mạnh". Ngược lại, ngành **Energy & Utilities** khi mua **Services** lại có tỷ lệ thắng bằng 0. Đừng phí thời gian chào mời gói Services cho ngành này nữa.
2.  **Quy luật 80/20 (Pareto Analysis):** 
    *   Chỉ có **10 cặp Ngành - Sản phẩm** đứng đầu đã đóng góp tới **hơn 52% tổng doanh thu** của toàn công ty. 
    *   **Insight:** Thay vì dàn trải Sales khắp 20-30 ngành, hãy tập trung tối ưu hóa quy trình cho 10 cặp "mỏ vàng" này (đặc biệt là Logistics + Services và Healthcare + SAAS).
3.  **Bản đồ Hiệu quả Ngành:** 
    *   Giúp bạn nhận diện những ngành "ngon" nhất: nằm ở góc trên bên trái (Thời gian chốt ngắn + Tỷ lệ thắng cao). 
    *   **Education & Science** là ngành nằm ở vị trí đẹp nhất trong bản đồ này.

---
> [!TIP]
> **Hành động đề xuất:** Hãy xây dựng các bộ "Case Study" thành công của ngành Education và Logistics để nhân rộng cho đội Sales. Đồng thời, yêu cầu đội Sản phẩm nghiên cứu tại sao ngành Energy lại không mặn mà với các gói dịch vụ (Services) của chúng ta để điều chỉnh tính năng.
