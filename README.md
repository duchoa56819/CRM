# 📊 CRM Data Analysis & Business Intelligence Suite

Dự án này cung cấp một giải pháp phân tích dữ liệu CRM toàn diện, giúp chuyển đổi dữ liệu thô từ hệ thống quản trị quan hệ khách hàng thành những chỉ số kinh doanh chiến lược (Actionable Insights). 

Dữ liệu được phân tích dưới **7 góc nhìn chuyên sâu**, đi kèm với các mã nguồn tự động hóa và hướng dẫn triển khai trên Power BI.

---

## 🚀 7 Góc nhìn Phân tích (7 Perspectives)

Nhấn vào từng mục bên dưới để xem báo cáo chi tiết và hướng dẫn kỹ thuật (DAX) cho từng góc nhìn:

1.  **[Pipeline Health & Funnel](./CRM_Analysis_Report.md):** Đánh giá sức khỏe phễu bán hàng và tìm kiếm "nút thắt cổ chai".
2.  **[Customer Segmentation & ICP](./CRM_Customer_Segmentation_Analysis.md):** Xác định chân dung khách hàng lý tưởng mang lại lợi nhuận cao nhất.
3.  **[Sales Velocity & Momentum](./CRM_Velocity_Dashboard_Guide.md):** Đo lường tốc độ tạo ra dòng tiền và cảnh báo độ "lão hóa" của các đơn hàng.
4.  **[Owner Workload & Efficiency](./CRM_Workload_Dashboard_Guide.md):** Phân tích khối lượng công việc và hiệu suất của từng nhân viên Sales.
5.  **[Risk & Probability Calibration](./CRM_Risk_Calibration_Dashboard_Guide.md):** Kiểm chứng độ tin cậy của dự báo và phân tích tâm lý lạc quan/thận trọng của Sales.
6.  **[Strategic Industry-Product Fit](./CRM_Strategic_Fit_Dashboard_Guide.md):** Ma trận chiến lược xác định dòng sản phẩm nào thực sự "hợp" với ngành nghề nào.
7.  **[Temporal Seasonality](./CRM_Seasonality_Dashboard_Guide.md):** Tìm kiếm "thời điểm vàng" (ngày/tháng) để tối ưu hóa chiến dịch Marketing.

---

## 📂 Cấu trúc Repository

*   `*.py`: Các script Python sử dụng Pandas, Matplotlib và Seaborn để xử lý dữ liệu và tự động xuất Dashboard dưới dạng hình ảnh.
*   `*.md`: Các báo cáo chi tiết và hướng dẫn kỹ thuật:
    *   `Huong_Dan_Phan_Tich_CRM.md`: Sổ tay quy trình phân tích CRM chuẩn.
    *   `PowerBI_Guide.md`: Hướng dẫn tổng quan về DAX và Visual trên Power BI.
    *   `Metrics_Rationale.md`: Giải thích ý nghĩa quản trị đằng sau từng chỉ số.
*   `*.png`: Thư viện Dashboard đã được xuất bản để sử dụng ngay cho báo cáo/thuyết trình.
*   `CRM and Sales Pipelines.xlsx`: Bộ dữ liệu mẫu được sử dụng trong dự án.

---

## 🛠 Công nghệ sử dụng

*   **Ngôn ngữ:** Python (Pandas cho xử lý dữ liệu, Matplotlib & Seaborn cho trực quan hóa).
*   **Công cụ BI:** Power BI (DAX Measures).
*   **Dữ liệu:** Excel / CRM Export.

---

## 📖 Hướng dẫn sử dụng

### 1. Dành cho người dùng Power BI:
Mở các file hướng dẫn tương ứng với góc nhìn bạn quan tâm ở mục **🚀 7 Góc nhìn Phân tích** để lấy công thức DAX. Bạn chỉ cần copy-paste vào hệ thống Power BI của mình.

### 2. Dành cho nhà phân tích (Python):
Cài đặt thư viện cần thiết:
```bash
pip install pandas matplotlib seaborn openpyxl
```
Chạy các script để xem kết quả phân tích mới nhất:
```bash
python generate_report.py
```

---

## 💡 Tư duy cốt lõi
Dự án này không chỉ tập trung vào việc "vẽ biểu đồ đẹp", mà tập trung vào **Actionable Insights** — mỗi con số sinh ra đều phải phục vụ cho một quyết định cụ thể của người quản lý.

---
**Author:** [duchoa56819](https://github.com/duchoa56819)
**Project:** CRM Analysis Suite 2024.
