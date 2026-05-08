import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cài đặt font và style
sns.set_theme(style="whitegrid", rc={"font.family": "sans-serif"})

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

# Basic prep
df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])
df['Acq_Month_Name'] = df['Lead acquisition date'].dt.month_name()
df['Acq_DayOfWeek'] = df['Lead acquisition date'].dt.day_name()

# 1. Dashboard: Win Rate by Month (Seasonality)
month_order = ['January', 'February', 'March', 'April', 'May']
month_stats = []
for month in month_order:
    m_df = df[df['Acq_Month_Name'] == month]
    closed = m_df[m_df['Is_Closed']]
    won = m_df[m_df['Is_Won']]
    win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    month_stats.append({'Month': month, 'Win Rate (%)': win_rate})

m_df = pd.DataFrame(month_stats)

plt.figure(figsize=(10, 6))
sns.lineplot(data=m_df, x='Month', y='Win Rate (%)', marker='o', linewidth=3, markersize=10, color='#9b59b6')
plt.title('Tính chu kỳ theo Tháng: Tỷ lệ thắng theo thời điểm nhận Lead', fontsize=15, fontweight='bold', pad=20)
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig('seasonal_win_rate.png', dpi=300)
plt.close()

# 2. Dashboard: Win Rate by Day of Week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_stats = []
for day in day_order:
    d_df = df[df['Acq_DayOfWeek'] == day]
    closed = d_df[d_df['Is_Closed']]
    won = d_df[d_df['Is_Won']]
    win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    day_stats.append({'Day': day, 'Win Rate (%)': win_rate})

d_df = pd.DataFrame(day_stats)

plt.figure(figsize=(10, 6))
sns.barplot(data=d_df, x='Day', y='Win Rate (%)', palette='Purples_d')
plt.title('Hiệu suất theo Thứ trong tuần (Lead Quality by Day)', fontsize=15, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('daily_win_rate.png', dpi=300)
plt.close()

# 3. Dashboard: Product Demand Heatmap by Month
prod_month = df.groupby(['Acq_Month_Name', 'Product']).size().unstack(fill_value=0).reindex(month_order)

plt.figure(figsize=(12, 6))
sns.heatmap(prod_month, annot=True, fmt='d', cmap='BuPu')
plt.title('Nhu cầu Sản phẩm theo Tháng (Số lượng Leads)', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Dòng sản phẩm')
plt.ylabel('Tháng nhận Lead')
plt.tight_layout()
plt.savefig('seasonal_product_demand.png', dpi=300)
plt.close()

print("Perspective 7 dashboards generated.")
