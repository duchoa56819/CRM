# 📊 Hướng dẫn xây dựng CRM Dashboard trên Power BI

Tài liệu này sẽ hướng dẫn bạn cách đưa file Excel `CRM and Sales Pipelines.xlsx` vào Power BI, tạo các chỉ số đo lường (Measures) bằng DAX và thiết lập các biểu đồ trực quan như đã phân tích.

---

## 1. Chuẩn bị dữ liệu (Data Preparation)

1. Mở Power BI Desktop -> Chọn **Get Data** -> **Excel Workbook**.
2. Trỏ đến file `CRM and Sales Pipelines.xlsx` -> Chọn sheet `CRM_data` -> Click **Load** (hoặc **Transform Data** nếu bạn muốn dọn dẹp dữ liệu trước).
3. **Tạo Calculated Column (Cột tính toán):** 
   Đầu tiên, bạn cần tính số ngày đóng Deal để đo lường Response Time. Chuyển sang Data View, chọn **New Column** và dán công thức DAX sau:
   ```dax
   Days_to_Close = DATEDIFF('CRM_data'[Lead acquisition date], 'CRM_data'[Actual close date], DAY)
   ```

---

## 2. Các công thức DAX (Measures) quan trọng

Chuyển sang tab Report View, chọn **New Measure** để tạo lần lượt các chỉ số sau. Việc dùng Measure thay vì kéo thả cột thô sẽ giúp Dashboard tương tác chuẩn xác khi bạn bấm lọc (Filter) dữ liệu.

**1. Tổng số Leads**
```dax
Total Leads = COUNTROWS('CRM_data')
```

**2. Số lượng khách hàng chốt thành công (Won Deals)**
*(Đã bao gồm khách hàng mua rồi churn)*
```dax
Total Won Deals = 
CALCULATE(
    COUNTROWS('CRM_data'),
    'CRM_data'[Status] IN {"Customer", "Churned Customer"}
)
```

**3. Số lượng Deal bị thất bại (Lost Deals)**
```dax
Total Lost Deals = 
CALCULATE(
    COUNTROWS('CRM_data'),
    'CRM_data'[Status] IN {"Disqualified", "Churned Customer"} || 'CRM_data'[Stage] = "Lost"
)
```

**4. Tỷ lệ chốt đơn (Win Rate)**
*(Được tính trên số lượng các deal ĐÃ ĐÓNG)*
```dax
Win Rate % = 
VAR ClosedDeals = 
    CALCULATE(
        COUNTROWS('CRM_data'),
        'CRM_data'[Status] IN {"Customer", "Churned Customer", "Disqualified"}
    )
RETURN DIVIDE([Total Won Deals], ClosedDeals, 0)
```

**5. Tổng Doanh thu (Revenue)**
```dax
Total Revenue = 
CALCULATE(
    SUM('CRM_data'[Deal Value, $]),
    'CRM_data'[Status] IN {"Customer", "Churned Customer"}
)
```

**6. Giá trị Pipeline hiện tại (Open Deals Value)**
```dax
Open Pipeline Value = 
CALCULATE(
    SUM('CRM_data'[Deal Value, $]),
    NOT('CRM_data'[Status] IN {"Customer", "Churned Customer", "Disqualified"})
)
```

**7. Thời gian xử lý trung bình (Avg Days to Close)**
```dax
Avg Days to Close = AVERAGE('CRM_data'[Days_to_Close])
```

---

## 3. Hướng dẫn thiết kế Biểu đồ (Visualizations)

### 📈 Biểu đồ 1: Sales Pipeline Funnel (Phễu bán hàng)
- **Visual type:** Funnel
- **Category:** Kéo cột `Status` vào.
- **Values:** Kéo measure `[Total Leads]` vào.
- **Lưu ý Sort:** Để phễu chạy đúng thứ tự (New -> Qualified -> Sales Accepted -> ...), bạn cần click chọn cột `Status` ở thẻ Data, trên menu chọn **Sort by column** và chọn cột `Status sequence`.

### 🌍 Biểu đồ 2: Lead Distribution (Phân bổ Quốc gia/Ngành)
Bạn có thể tạo 2 biểu đồ Bar Chart song song:
- **Visual type:** Stacked Bar Chart
- **Y-axis:** Kéo cột `Country` (hoặc `Industry`) vào.
- **X-axis:** Kéo measure `[Total Leads]` vào.
- *Tip:* Bạn có thể bật **Data labels** để hiển thị số lượng cụ thể và dùng Filter Panel (Top N = 5) để chỉ hiển thị 5 quốc gia/ngành đứng đầu.

### 👤 Biểu đồ 3: Agent Performance (Hiệu suất Sales)
Kết hợp doanh thu và Win Rate để đánh giá toàn diện nhân viên.
- **Visual type:** Line and Clustered Column Chart (Biểu đồ cột kết hợp đường)
- **X-axis:** `Owner`
- **Column y-axis:** Kéo measure `[Total Revenue]` vào.
- **Line y-axis:** Kéo measure `[Win Rate %]` vào.
- *Định dạng:* Nhấp vào định dạng của `[Win Rate %]` ở menu Modeling, đổi thành dạng Percentage (%). Cột sẽ thể hiện tiền USD, đường sẽ thể hiện %.

### 📉 Biểu đồ 4: Phân tích Lost Opportunities
Tạo một Donut Chart để phân tích lý do rớt đơn theo sản phẩm:
- **Visual type:** Donut Chart
- **Legend:** Kéo cột `Product` vào.
- **Values:** Kéo measure `[Total Lost Deals]` vào.
- *Phân tích bổ sung:* Tạo thêm một Bar Chart với **Y-axis** là `Industry` và **X-axis** là `[Total Lost Deals]` để biết ngành nào đang mất khách nhiều nhất.

---
> [!TIP]
> **Thêm Slicers (Bộ lọc):** Để Dashboard linh hoạt, hãy thêm các Visual **Slicer**. Bạn có thể kéo các trường như `Date` (Lead acquisition date), `Owner`, hoặc `Country` vào Slicer. Khi click vào 1 nhân viên hay 1 quốc gia, toàn bộ các biểu đồ và DAX Measures sẽ tự động tính toán lại cực kì sinh động!
