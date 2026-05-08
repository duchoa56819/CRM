import pandas as pd
import json

file_path = 'CRM and Sales Pipelines.xlsx'
xls = pd.ExcelFile(file_path)

info = {}
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    info[sheet_name] = {
        'columns': df.columns.tolist(),
        'head': df.head(3).to_dict(orient='records')
    }

print(json.dumps(info, indent=2, default=str))
