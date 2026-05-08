import pandas as pd
import numpy as np
import json

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

# Prepare data
df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])
df['Days_to_Close'] = (df['Actual close date'] - df['Lead acquisition date']).dt.days

results = {}

# 1. Organization Size Analysis
org_size_stats = df.groupby('Organization size').agg(
    Total_Leads=('Organization', 'count'),
    Avg_Deal_Value=('Deal Value, $', 'mean'),
    Total_Pipeline=('Deal Value, $', 'sum')
).reset_index()

# Win rate by org size
win_rates = []
for size in df['Organization size'].unique():
    size_df = df[df['Organization size'] == size]
    closed = size_df[size_df['Is_Closed']]
    won = size_df[size_df['Is_Won']]
    win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    win_rates.append({'Organization size': size, 'Win_Rate': win_rate})

win_rate_df = pd.DataFrame(win_rates)
org_size_stats = org_size_stats.merge(win_rate_df, on='Organization size')
results['Org_Size'] = org_size_stats.to_dict(orient='records')

# 2. Organization Size vs Time to Close
time_close = df[df['Is_Won'] == True].groupby('Organization size')['Days_to_Close'].mean().reset_index()
results['Time_To_Close_By_Size'] = time_close.to_dict(orient='records')

# 3. Product Performance
prod_stats = df.groupby('Product').agg(
    Total_Leads=('Organization', 'count'),
    Avg_Deal_Value=('Deal Value, $', 'mean'),
    Total_Pipeline=('Deal Value, $', 'sum')
).reset_index()

prod_win_rates = []
for prod in df['Product'].unique():
    prod_df = df[df['Product'] == prod]
    closed = prod_df[prod_df['Is_Closed']]
    won = prod_df[prod_df['Is_Won']]
    win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    prod_win_rates.append({'Product': prod, 'Win_Rate': win_rate})

prod_win_df = pd.DataFrame(prod_win_rates)
prod_stats = prod_stats.merge(prod_win_df, on='Product')
results['Product'] = prod_stats.to_dict(orient='records')

# 4. Ideal Customer Profile (ICP) matrix: Org Size x Product
icp = df[df['Is_Won'] == True].groupby(['Organization size', 'Product'])['Deal Value, $'].sum().reset_index()
icp = icp.sort_values(by='Deal Value, $', ascending=False).head(5)
results['Top_ICP'] = icp.to_dict(orient='records')

print(json.dumps(results, indent=2))
