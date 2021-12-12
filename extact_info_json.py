# %% Import Libarary to Use
import pandas as pd
from glob import glob
pd.set_option("display.max_columns", None)
# %% Read Data List
DATAPATH = "../data/2021_OCR_Hackaton/medicine/annotations/"
data_list = glob(DATAPATH + '*.json')
data_list.sort()

# %% Convert JSON to DataFrame with Merge
import json

df_extract_info = pd.DataFrame()

for json_file in data_list:
    
    with open(json_file, 'r') as json_file:
        json_data = json.load(json_file)
        
        for i in range(len(json_data['images'])):
            tmp_df = pd.DataFrame(json_data['annotations'][i]['polygons'])
            tmp_df['image_name'] = json_data['images'][i]['name']
            df_extract_info = pd.concat((df_extract_info, tmp_df.query('type != 0', engine='python')), axis=0)
            
        json_file.close()

df_extract_info = df_extract_info.reset_index(drop=True)

# %% Saving Data
df_extract_info.to_csv("./extracted_json_input_label.csv", index=False)