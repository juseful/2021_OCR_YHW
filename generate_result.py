# %% 
import pandas as pd
import json
from tqdm import tqdm
# %%
DATAPATH = "./DATA/text_export_result_easyocr_word.xlsx"
sheet_names = pd.ExcelFile(DATAPATH).sheet_names
# %%

result = {}

for sheet_nm in tqdm(sheet_names):
    df_tmp = pd.read_excel(DATAPATH, sheet_name=sheet_nm)
    
    dict_tmp = {'image_name':df_tmp['filename'][0], 
                'bbox':df_tmp['bbox'].to_list()}
    
    for key, value in dict_tmp.items():
        if key in result:
            if isinstance(result[key], list):
                result[key].append(value)
            else:
                tmp_list = [result[key]]
                tmp_list.append(value)
                result[key] = tmp_list
        else:
            result[key] = value
# %%
with open('result.json', 'w') as fp:
    json.dump(result, fp, indent=4)
# %%
