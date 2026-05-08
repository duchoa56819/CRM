import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cài đặt font và style
sns.set_theme(style="whitegrid", rc={"font.family": "sans-serif"})

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

# 1. Pipeline Funnel (Phân bổ Lead theo trạng thái)
plt.figure(figsize=(10, 6))
# Define sequence for funnel
status_order = ['New', 'Qualified', 'Sales Accepted', 'Opportunity', 'Customer']
status_counts = df[df['Status'].isin(status_order)]['Status'].value_counts().reindex(status_order)
colors = ['#b3cde0', '#6497b1', '#005b96', '#03396c', '#011f4b']

ax = sns.barplot(x=status_counts.values, y=status_counts.index, palette=colors)
plt.title('Sales Pipeline Funnel (Số lượng Leads qua các giai đoạn)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Số lượng', fontsize=12)
plt.ylabel('Giai đoạn', fontsize=12)
for i, v in enumerate(status_counts.values):
    ax.text(v + 10, i, str(v), color='black', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('pipeline_funnel.png', dpi=300)
plt.close()

# 2. Lead Distribution (Quốc gia và Ngành nghề)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

top_countries = df['Country'].value_counts().head(5)
sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax1, palette='viridis')
ax1.set_title('Top 5 Quốc gia tiềm năng nhất', fontsize=14, fontweight='bold')
ax1.set_xlabel('Số lượng Leads')

top_industries = df['Industry'].value_counts().head(5)
sns.barplot(x=top_industries.values, y=top_industries.index, ax=ax2, palette='magma')
ax2.set_title('Top 5 Ngành nghề tiềm năng nhất', fontsize=14, fontweight='bold')
ax2.set_xlabel('Số lượng Leads')

plt.tight_layout()
plt.savefig('lead_distribution.png', dpi=300)
plt.close()

# 3. Đánh giá Đội ngũ Sales
df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])

agent_perf = []
for owner in df['Owner'].unique():
    owner_df = df[df['Owner'] == owner]
    closed_df = owner_df[owner_df['Is_Closed'] == True]
    won_df = owner_df[owner_df['Is_Won'] == True]
    
    win_rate = (len(won_df) / len(closed_df) * 100) if len(closed_df) > 0 else 0
    revenue = won_df['Deal Value, $'].sum()
    
    agent_perf.append({
        'Owner': owner,
        'Win Rate (%)': win_rate,
        'Revenue ($)': revenue
    })

agent_df = pd.DataFrame(agent_perf).sort_values(by='Revenue ($)', ascending=False)

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

sns.barplot(data=agent_df, x='Owner', y='Revenue ($)', ax=ax1, color='#3498db', alpha=0.8, label='Doanh thu ($)')
sns.lineplot(data=agent_df, x='Owner', y='Win Rate (%)', ax=ax2, color='#e74c3c', marker='o', linewidth=3, markersize=10, label='Tỷ lệ chốt (Win Rate %)')

ax1.set_title('Agent Performance: Doanh thu & Tỷ lệ chốt đơn', fontsize=16, fontweight='bold', pad=20)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
ax1.set_ylabel('Doanh thu ($)', fontsize=12, color='#3498db')
ax2.set_ylabel('Tỷ lệ chốt (%)', fontsize=12, color='#e74c3c')
ax2.set_ylim(0, 100)

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')

plt.tight_layout()
plt.savefig('sales_performance.png', dpi=300)
plt.close()

# 4. Phân tích Lost Opportunity
lost_df = df[df['Status'].isin(['Disqualified', 'Churned Customer']) | df['Stage'].isin(['Lost'])]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# By Product
lost_product = lost_df['Product'].value_counts()
ax1.pie(lost_product.values, labels=lost_product.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
ax1.set_title('Tỷ lệ thất bại theo Sản phẩm', fontsize=14, fontweight='bold')

# By Industry
lost_industry = lost_df['Industry'].value_counts().head(5)
sns.barplot(x=lost_industry.values, y=lost_industry.index, ax=ax2, palette='rocket')
ax2.set_title('Top 5 Ngành có tỷ lệ rớt cao nhất', fontsize=14, fontweight='bold')
ax2.set_xlabel('Số lượng Deals thất bại')

plt.tight_layout()
plt.savefig('lost_opportunity.png', dpi=300)
plt.close()

print("All dashboards generated successfully.")
