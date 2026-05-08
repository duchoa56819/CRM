import pandas as pd
import numpy as np
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super(NpEncoder, self).default(obj)

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

# Basic prep
df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])

results = {}

# 1. Probability Calibration
# Bucketing probabilities (e.g., 0-20, 21-40, ...)
bins = [0, 20, 40, 60, 80, 101]
labels = ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%']
df['Prob_Bucket'] = pd.cut(df['Probability, %'], bins=bins, labels=labels, right=False)

calibration = []
for bucket in labels:
    bucket_df = df[df['Prob_Bucket'] == bucket]
    closed = bucket_df[bucket_df['Is_Closed']]
    won = bucket_df[bucket_df['Is_Won']]
    actual_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    calibration.append({
        'Bucket': bucket,
        'Actual_Win_Rate': actual_rate
    })
results['Calibration'] = calibration

# 2. Liar's Index (Probability Bias by Owner)
bias_stats = []
for owner in df['Owner'].unique():
    owner_df = df[df['Owner'] == owner]
    closed_won = owner_df[owner_df['Is_Won']]
    closed_lost = owner_df[(owner_df['Is_Closed']) & (~owner_df['Is_Won'])]
    
    avg_prob_all = owner_df['Probability, %'].mean()
    actual_win_rate = (len(closed_won) / (len(closed_won) + len(closed_lost)) * 100) if (len(closed_won) + len(closed_lost)) > 0 else 0
    
    bias_stats.append({
        'Owner': owner,
        'Avg_Assigned_Prob': avg_prob_all,
        'Actual_Win_Rate': actual_win_rate,
        'Bias': avg_prob_all - actual_win_rate
    })
results['Owner_Bias'] = bias_stats

# 3. Stage Conversion Probability (The REAL probability of each stage)
stage_probs = []
for stage in df['Stage'].unique():
    if pd.isna(stage): continue
    s_df = df[df['Stage'] == stage]
    won = s_df[s_df['Is_Won']]
    # We need to see out of all deals that passed this stage, how many won eventually?
    # This is complex with the current flat structure, but we can approximate:
    # Probability that a deal currently in this stage will be won.
    # Note: Closed deals in this stage are already won or lost.
    closed = s_df[s_df['Is_Closed']]
    won_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    stage_probs.append({'Stage': stage, 'Real_Win_Prob': won_rate})

results['Stage_Real_Prob'] = stage_probs

print(json.dumps(results, indent=2, cls=NpEncoder))
