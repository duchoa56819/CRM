# 📊 Dashboard & DAX: Phân khúc Khách hàng & Sản phẩm

Dưới đây là các biểu đồ trực quan hóa chuyên sâu cho góc nhìn Phân khúc (Segmentation) cùng các công thức DAX tương ứng để bạn áp dụng vào Power BI.

---

## 📈 Trực quan hóa (Dashboards)

````carousel
![Hiệu suất theo Quy mô Doanh nghiệp](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/segment_performance.png)
<!-- slide -->
![Cơ cấu Doanh thu theo Sản phẩm](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/product_revenue_pie.png)
<!-- slide -->
![Ma trận ICP: Quy mô vs Sản phẩm](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/icp_heatmap.png)
````

---

## 🔢 Công thức DAX cho Phân khúc & Sản phẩm

Để xây dựng dashboard này trên Power BI, bạn có thể sử dụng các công thức DAX nâng cao sau:

### 1. Phân loại Quy mô Khách hàng (Nếu file chưa có cột này)
*Nếu bạn muốn tự định nghĩa lại quy mô dựa trên doanh thu hoặc số nhân sự:*
```dax
Segment Group = 
SWITCH( TRUE(),
    'CRM_data'[Organization size] = "Enterprise (1001+)", "High Value",
    'CRM_data'[Organization size] = "Large (501-1000)", "High Potential",
    'CRM_data'[Organization size] = "Medium (201-500)", "Core Market",
    "Small/Micro"
)
```

### 2. Tỷ lệ thắng theo Phân khúc (Win Rate by Segment)
```dax
Win Rate % by Segment = 
DIVIDE(
    CALCULATE(COUNTROWS('CRM_data'), 'CRM_data'[Status] IN {"Customer", "Churned Customer"}),
    CALCULATE(COUNTROWS('CRM_data'), 'CRM_data'[Status] IN {"Customer", "Churned Customer", "Disqualified"}),
    0
)
```

### 3. Giá trị đơn hàng trung bình (Avg Ticket Size)
```dax
Avg Deal Value = AVERAGE('CRM_data'[Deal Value, $])
```

### 4. Thời gian chốt đơn theo phân khúc (Avg Days to Won)
*Lưu ý: Chỉ tính cho các deal thành công để đo lường tốc độ chốt đơn thực tế.*
```dax
Avg Days to Won = 
CALCULATE(
    AVERAGE('CRM_data'[Days_to_Close]),
    'CRM_data'[Status] IN {"Customer", "Churned Customer"}
)
```

### 5. Chỉ số ICP Score (Chỉ số ưu tiên khách hàng lý tưởng)
*Công thức này kết hợp Win Rate và Doanh thu để tìm ra nhóm khách hàng "ngon" nhất:*
```dax
ICP Score = ([Win Rate % by Segment] * 0.6) + (([Total Revenue] / MAXX(ALL('CRM_data'), [Total Revenue])) * 0.4)
```

---

## 💡 Hướng dẫn thiết lập Visuals

1.  **Biểu đồ Ma trận (Heatmap):** 
    -   Sử dụng Visual **Matrix**. 
    -   Rows: `Organization size`
    -   Columns: `Product`
    -   Values: `Total Revenue`
    -   *Định dạng:* Vào tab Format -> Cell elements -> Bật **Background color** để tạo hiệu ứng Heatmap. Nhóm nào màu càng đậm nghĩa là càng mang lại nhiều tiền.

2.  **Biểu đồ Kết hợp (Dual Axis):**
    -   Sử dụng **Line and clustered column chart**.
    -   X-axis: `Organization size`
    -   Column values: `Win Rate %`
    -   Line values: `Avg Days to Won`
    -   *Insight:* Tìm những cột cao (Win rate cao) nhưng đường thấp (Thời gian chốt ngắn) -> Đó chính là phân khúc "dễ ăn" nhất.

3.  **Biểu đồ Tròn (Pie Chart):**
    -   Sử dụng để xem cơ cấu doanh thu theo `Product` hoặc `Industry`. Thường dùng để trình bày cho ban lãnh đạo về sự đóng góp của các dòng sản phẩm.
