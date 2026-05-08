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

# 1. Dashboard: Workload vs Efficiency
owner_stats = []
for owner in df['Owner'].unique():
    owner_df = df[df['Owner'] == owner]
    closed = owner_df[owner_df['Is_Closed']]
    won = owner_df[owner_df['Is_Won']]
    win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    owner_stats.append({'Owner': owner, 'Workload': len(owner_df), 'Win Rate': win_rate})

w_df = pd.DataFrame(owner_stats).sort_values(by='Workload', ascending=False)

plt.figure(figsize=(12, 6))
sns.scatterplot(data=w_df, x='Workload', y='Win Rate', hue='Owner', s=200, palette='viridis')
plt.title('Tương quan: Khối lượng công việc (Workload) vs. Tỷ lệ thắng (Win Rate)', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Số lượng Leads được giao', fontsize=12)
plt.ylabel('Tỷ lệ chốt thành công (%)', fontsize=12)
plt.tight_layout()
plt.savefig('workload_efficiency.png', dpi=300)
plt.close()

# 2. Dashboard: Portfolio Mix (Stacked Bar)
bins = [0, 5000, 10000, 200000]
labels = ['Small (<5k)', 'Medium (5-10k)', 'Large (>10k)']
df['Deal Size'] = pd.cut(df['Deal Value, $'], bins=bins, labels=labels)
portfolio = df.groupby(['Owner', 'Deal Size'], observed=True).size().unstack(fill_value=0)

portfolio.plot(kind='bar', stacked=True, figsize=(12, 7), color=sns.color_palette('viridis', 3))
plt.title('Cơ cấu danh mục Deals (Portfolio Mix) của từng nhân viên', fontsize=15, fontweight='bold', pad=20)
plt.ylabel('Số lượng Leads', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Quy mô Deal')
plt.tight_layout()
plt.savefig('owner_portfolio.png', dpi=300)
plt.close()

# 3. Dashboard: Regional Win Rate Map/Bar
country_eff = []
for country in df['Country'].unique():
    c_df = df[df['Country'] == country]
    closed = c_df[c_df['Is_Closed']]
    won = c_df[c_df['Is_Won']]
    if len(closed) > 20:
        country_eff.append({'Country': country, 'Win Rate': (len(won) / len(closed) * 100)})

c_df = pd.DataFrame(country_eff).sort_values(by='Win Rate', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=c_df, x='Win Rate', y='Country', palette='coolwarm')
plt.title('Top các Quốc gia có tỷ lệ chốt đơn hiệu quả nhất', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Tỷ lệ thắng (Win Rate %)', fontsize=12)
plt.tight_layout()
plt.savefig('regional_efficiency.png', dpi=300)
plt.close()

print("Perspective 4 dashboards generated.")
