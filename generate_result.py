# %% 
import pandas as pd
import json
from tqdm import tqdm
# %%
def generate_json_keras(data, result_file_nm):

    sheet_names = pd.ExcelFile(data).sheet_names
    result = {}

    for sheet_nm in tqdm(sheet_names):
        
        df_tmp = pd.read_excel(data, sheet_name=sheet_nm)
        
        dict_tmp = {'image_name':df_tmp['filename'].to_list(), 
                    'bbox':df_tmp['bbox'].to_list(),
                    'x_start':df_tmp['x_start'].to_list(),
                    'y_start':df_tmp['y_start'].to_list(),
                    'x_end':df_tmp['x_end'].to_list(),
                    'y_end':df_tmp['y_end'].to_list(),
                    'text':df_tmp['text'].to_list()}
        
        
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
            
    with open(result_file_nm, 'w', encoding='utf-8') as fp:
        json.dump(result, fp, indent=4, ensure_ascii=False)
        fp.close()


def generate_json_easyocr(data, result_file_nm):

    sheet_names = pd.ExcelFile(data).sheet_names
    result = {}

    for sheet_nm in tqdm(sheet_names):
        
        df_tmp = pd.read_excel(data, sheet_name=sheet_nm)
        
        dict_tmp = {'image_name':df_tmp['filename'].to_list(), 
                    'bbox':df_tmp['bbox'].to_list(),
                    'x_start':df_tmp['x_start'].to_list(),
                    'y_start':df_tmp['y_start'].to_list(),
                    'x_end':df_tmp['x_end'].to_list(),
                    'y_end':df_tmp['y_end'].to_list(),
                    'easyocr_text':df_tmp['easyocr_text'].to_list(), 
                    'tesseract_text':df_tmp['tesseract_text'].to_list(),}
        
        
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
            
    with open(result_file_nm, 'w', encoding='utf-8') as fp:
        json.dump(result, fp, indent=4, ensure_ascii=False)
        fp.close()

# %%
if __name__ == '__main__':
    generate_json_keras("./DATA/text_export_result_kerasocr.xlsx", './JSON/result_kerasocr.json')
    generate_json_easyocr("./DATA/text_export_result_easyocr_line.xlsx", './JSON/result_easyocr_line.json')
    generate_json_easyocr("./DATA/text_export_result_easyocr_word.xlsx", './JSON/result_easyocr_word.json')