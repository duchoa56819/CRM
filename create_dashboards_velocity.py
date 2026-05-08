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
df['Days_to_Close'] = (df['Actual close date'] - df['Lead acquisition date']).dt.days

# 1. Sales Velocity Dashboard
velocity_data = []
for owner in df['Owner'].unique():
    owner_df = df[df['Owner'] == owner]
    leads = len(owner_df)
    closed = owner_df[owner_df['Is_Closed']]
    won = owner_df[owner_df['Is_Won']]
    win_rate = (len(won) / len(closed)) if len(closed) > 0 else 0
    avg_deal = won['Deal Value, $'].mean() if len(won) > 0 else 0
    avg_cycle = won['Days_to_Close'].mean() if len(won) > 0 else 1
    velocity = (leads * avg_deal * win_rate) / avg_cycle
    velocity_data.append({'Owner': owner, 'Velocity': velocity})

v_df = pd.DataFrame(velocity_data).sort_values(by='Velocity', ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(data=v_df, x='Velocity', y='Owner', palette='rocket')
plt.title('Sales Velocity ($/Ngày): Tốc độ tạo ra doanh thu của từng Sales', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Doanh thu dự kiến tạo ra mỗi ngày ($)', fontsize=12)
plt.tight_layout()
plt.savefig('sales_velocity.png', dpi=300)
plt.close()

# 2. Pipeline Aging Dashboard
current_date = df['Lead acquisition date'].max()
open_deals = df[df['Is_Closed'] == False].copy()
open_deals['Age'] = (current_date - open_deals['Lead acquisition date']).dt.days

plt.figure(figsize=(10, 6))
sns.histplot(open_deals['Age'], bins=20, kde=True, color='#2ecc71')
plt.axvline(open_deals['Age'].mean(), color='red', linestyle='--', label=f'Trung bình: {open_deals["Age"].mean():.1f} ngày')
plt.title('Phân bổ độ tuổi của các Deals đang mở (Pipeline Aging)', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Số ngày tồn tại trong Pipeline (kể từ ngày nhận Lead)', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('pipeline_aging.png', dpi=300)
plt.close()

# 3. Monthly Momentum Dashboard (Leads vs Won)
df['Acq_Month'] = df['Lead acquisition date'].dt.to_period('M').astype(str)
df['Close_Month'] = df['Actual close date'].dt.to_period('M').astype(str)

leads_month = df.groupby('Acq_Month').size()
won_month = df[df['Is_Won'] == True].groupby('Close_Month').size()

plt.figure(figsize=(12, 6))
plt.plot(leads_month.index, leads_month.values, marker='o', label='Leads mới nhận', linewidth=3, color='#3498db')
plt.plot(won_month.index, won_month.values, marker='s', label='Deals chốt thành công', linewidth=3, color='#e74c3c')
plt.title('Đà tăng trưởng (Momentum): Leads mới vs. Deals chốt theo tháng', fontsize=15, fontweight='bold', pad=20)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('pipeline_momentum.png', dpi=300)
plt.close()

print("Perspective 3 dashboards generated.")
