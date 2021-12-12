#%%
import easyocr
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt
from glob import glob
import os
import re
import copy
import math
import time
import pandas as pd
import imutils

reader = easyocr.Reader(['ko','en'], gpu=True)
#%%
workdir = "C:/Users/smcljy/data/20211210_OCR_hakathon/medicine/images"

filelist = []

for (root, directories, files) in os.walk(workdir):
    for file in files:
        if '.jpg' in file.lower():
            file_path = os.path.join(root, file)
            filelist.append(file_path)
        if '.jpeg' in file.lower():
            file_path = os.path.join(root, file)
            filelist.append(file_path)
# filelist
# %%
ratio = 1.0
width_th = 0.6
savedir = 'C:/Users/smcljy/data/20211210_OCR_hakathon/detection_IMG_r{}_w{}'.format(ratio,width_th)
file_name = 'text_export_result_r%s_w%s' % (ratio, width_th)
nan_df = pd.DataFrame()
nan_df.to_excel('C:/Users/smcljy/data/20211210_OCR_hakathon/{}.xlsx'.format(file_name))

for file in filelist:
    img = cv2.imread(file)

    # ret, img = cv2.threshold(img, 155,255, cv2.THRESH_BINARY_INV)
    x_ratio = ratio
    y_ratio = ratio
    bbx = cv2.resize(img, dsize=(0,0), fx=x_ratio, fy=y_ratio, interpolation=cv2.INTER_LINEAR)

    results = reader.readtext(bbx#,adjust_contrast=0.3
                            ,width_ths=width_th)#))

    # bounding box for text region and file write
    for (bbox, text, prob) in results:
        # unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        linethick = 10
        cv2.rectangle(bbx, tl, br, (0, 0, 255), int(linethick*x_ratio))
    
    save_info = savedir + file[len(workdir):]

    cv2.imwrite(save_info, bbx)

    # text detection
    result_text = []
    
    for i in range(len(results)):
        y_start = round(results[i][0][0][1]) if results[i][0][0][1] == results[i][0][1][1] else round(min(results[i][0][0][1], results[i][0][1][1]))
        y_end = round(results[i][0][2][1]) if results[i][0][2][1] == results[i][0][3][1] else round(max(results[i][0][2][1], results[i][0][3][1]))
        x_start = round(results[i][0][0][0]) if results[i][0][0][0] == results[i][0][3][0] else round(min(results[i][0][0][0], results[i][0][3][0]))
        x_end = round(results[i][0][1][0]) if results[i][0][1][0] == results[i][0][2][0] else round(max(results[i][0][1][0], results[i][0][2][0]))
        region = bbx[y_start:y_end, x_start:x_end].copy()
        configs = '-l kor+eng --psm 8'
        text_tess = pytesseract.image_to_string(region#,lang=('kor+eng')
                                        ,config=configs
                                        )#.split('\n')#,config=configs).split()
        arr = text_tess.split('\n')[0:-1]
        text_tess = '\n'.join(arr)
        result_text.append((file[len(workdir)+1:],results[i][0],results[i][1],results[i][2],text_tess))

    df = pd.DataFrame(result_text)
    with pd.ExcelWriter('C:/Users/smcljy/data/20211210_OCR_hakathon/{}.xlsx'.format(file_name), mode='a',engine='openpyxl') as writer:
        df.to_excel(writer,sheet_name=file[len(workdir)+1:len(workdir)+1+11], index=False)
# %%
