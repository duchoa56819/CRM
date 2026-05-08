import pandas as pd
import json

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

info = {
    'Status': df['Status'].value_counts().to_dict(),
    'Stage': df['Stage'].value_counts().to_dict(),
    'Columns_with_nulls': df.isnull().sum().to_dict()
}
print(json.dumps(info, indent=2))
