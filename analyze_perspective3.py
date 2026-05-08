import pandas as pd
import numpy as np
import json

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

# Basic prep
df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])
df['Days_to_Close'] = (df['Actual close date'] - df['Lead acquisition date']).dt.days
df['Acq_Month'] = df['Lead acquisition date'].dt.to_period('M').astype(str)
df['Close_Month'] = df['Actual close date'].dt.to_period('M').astype(str)

results = {}

# 1. Sales Velocity Calculation
# Formula: (Number of Leads * Avg Deal Value * Win Rate %) / Avg Sales Cycle (Days)
# We can calculate this per Owner
velocity_data = []
for owner in df['Owner'].unique():
    owner_df = df[df['Owner'] == owner]
    leads = len(owner_df)
    closed = owner_df[owner_df['Is_Closed']]
    won = owner_df[owner_df['Is_Won']]
    
    win_rate = (len(won) / len(closed)) if len(closed) > 0 else 0
    avg_deal = won['Deal Value, $'].mean() if len(won) > 0 else 0
    avg_cycle = won['Days_to_Close'].mean() if len(won) > 0 else 1 # Avoid division by zero
    
    # Velocity ($/Day)
    velocity = (leads * avg_deal * win_rate) / avg_cycle
    velocity_data.append({
        'Owner': owner,
        'Win_Rate': win_rate * 100,
        'Avg_Cycle': avg_cycle,
        'Velocity': velocity
    })

results['Sales_Velocity'] = sorted(velocity_data, key=lambda x: x['Velocity'], reverse=True)

# 2. Pipeline Momentum (Leads vs Won by Month)
leads_by_month = df.groupby('Acq_Month').size().to_dict()
won_by_month = df[df['Is_Won'] == True].groupby('Close_Month').size().to_dict()

results['Monthly_Momentum'] = {
    'Leads': leads_by_month,
    'Won': won_by_month
}

# 3. Deal Size vs Cycle Correlation
# Does higher value mean slower close?
bins = [0, 1000, 5000, 10000, 50000]
labels = ['Budget (<1k)', 'SMB (1-5k)', 'Mid-Market (5-10k)', 'Enterprise (>10k)']
df['Deal_Tier'] = pd.cut(df['Deal Value, $'], bins=bins, labels=labels)

tier_cycle = df[df['Is_Won'] == True].groupby('Deal_Tier', observed=True)['Days_to_Close'].mean().to_dict()
results['Cycle_by_Tier'] = tier_cycle

# 4. Pipeline Aging (Hypothetical aging for open deals based on current date = max date in dataset)
current_date = df['Lead acquisition date'].max()
open_deals = df[df['Is_Closed'] == False].copy()
open_deals['Age'] = (current_date - open_deals['Lead acquisition date']).dt.days
results['Avg_Open_Age'] = open_deals['Age'].mean()
results['Open_Age_by_Status'] = open_deals.groupby('Status')['Age'].mean().to_dict()

print(json.dumps(results, indent=2))
