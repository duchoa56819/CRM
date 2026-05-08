# ⚡ Dashboard & DAX: Tốc độ bán hàng & Đà tăng trưởng

Góc nhìn thứ 3 này tập trung vào **Tốc độ (Velocity)** và **Đà tăng trưởng (Momentum)**. Đây là những chỉ số "dẫn dắt" (Leading indicators) giúp ban lãnh đạo dự báo được khả năng sinh lời thực tế của hệ thống Sales trong tương lai.

---

## 📈 Trực quan hóa (Dashboards)

````carousel
![Sales Velocity ($/Ngày)](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/sales_velocity.png)
<!-- slide -->
![Phân bổ độ tuổi Pipeline Aging](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/pipeline_aging.png)
<!-- slide -->
![Momentum: Leads vs Won](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/pipeline_momentum.png)
````

---

## 🔢 Công thức DAX cho Tốc độ & Độ lão hóa

### 1. Chỉ số Sales Velocity (Chỉ số quan trọng nhất)
*Công thức tính tốc độ tạo ra tiền mỗi ngày của hệ thống:*
```dax
Sales Velocity = 
VAR AvgDealValue = [Avg Deal Value]
VAR WinRate = [Win Rate %]
VAR TotalLeads = [Total Leads]
VAR AvgCycle = [Avg Days to Won]
RETURN
DIVIDE( (TotalLeads * AvgDealValue * WinRate), AvgCycle, 0)
```

### 2. Độ tuổi của Deal (Deal Age)
*Tính cho các deal đang mở để biết chúng đã nằm trong phễu bao lâu:*
```dax
Deal Age (Days) = 
IF(
    ISBLANK('CRM_data'[Actual close date]),
    DATEDIFF('CRM_data'[Lead acquisition date], TODAY(), DAY),
    DATEDIFF('CRM_data'[Lead acquisition date], 'CRM_data'[Actual close date], DAY)
)
```

### 3. Cảnh báo Deal bị "ôi thiu" (Stagnant Deals Warning)
*Đánh dấu các deal có độ tuổi vượt quá trung bình (ví dụ > 70 ngày) mà chưa chốt:*
```dax
Stagnant Warning = 
IF([Deal Age (Days)] > 70 && ISBLANK('CRM_data'[Actual close date]), "⚠️ Cần can thiệp", "Bình thường")
```

---

## 💡 Giải thích ý nghĩa Quản trị (Perspective)

1.  **Sales Velocity ($/Ngày):** Thay vì chỉ nhìn vào doanh thu đã chốt, chỉ số này cho biết: *"Cứ mỗi ngày trôi qua, một nhân viên Sales đang nạp vào bao nhiêu tiền cho công ty?"*. Laura Thompson đang có tốc độ vượt trội ($17k/ngày), trong khi các nhân viên khác ở mức $4k-$10k.
2.  **Pipeline Aging:** Nếu biểu đồ Histogram lệch về phía bên phải (số ngày lớn), nghĩa là Pipeline đang bị **"lão hóa"**. Các deal bị ngâm quá lâu (trên 74 ngày) có xác suất thất bại cực cao. Đây là tín hiệu để sếp Sales vào cuộc "dọn dẹp" phễu.
3.  **Leads vs Won Momentum:** Biểu đồ này giúp phát hiện sự lệch pha. Nếu Lead nhận vào đều nhưng số Won giảm dần, có thể do đối thủ mới xuất hiện hoặc do Sales đang bị quá tải nên bỏ bê chăm sóc.

---
> [!TIP]
> **Hành động đề xuất:** Hãy tập trung vào các Deal có độ tuổi từ **40-60 ngày** trong giai đoạn **Opportunity**. Đây là "thời điểm vàng" để đẩy mạnh chốt đơn trước khi chúng rơi vào nhóm "lão hóa" (trên 70 ngày) và bị rớt.
