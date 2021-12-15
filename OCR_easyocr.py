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
# import imutils

reader = easyocr.Reader(['ko','en'],gpu=True)

# %%
workdir = "C:/Users/smcljy/data/20211210_OCR_hakathon/medicine/images/"

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
#%%
# line base
x_ratio = 1.0
y_ratio = 1.0
width_th = 0.5
savedir = 'C:/Users/smcljy/data/20211210_OCR_hakathon/img_easyocr_line_detection/'
file_name = 'text_export_result_easyocr_line'
nan_df = pd.DataFrame()
nan_df.to_excel('%s/%s.xlsx'% (savedir, file_name)) 

for file in filelist:#[117:118]linux #[6:7]window
    img = cv2.imread(file)
    bbx = img.copy()
    # img = cv2.imread(file,cv2.COLOR_BGR2GRAY)
    # ret, img = cv2.threshold(img, 150,255, cv2.THRESH_BINARY_INV)
    # bbx = cv2.resize(img, dsize=(0,0), fx=x_ratio, fy=y_ratio, interpolation=cv2.INTER_LANCZOS4)
    # bbx = img.copy()

    results = reader.readtext(bbx,width_ths=width_th)#))
    # y_start position sort
    results = sorted(results, key=lambda x: (x[0][0][1]))

    # bounding box for text region and file write
    for (bbox, text, prob) in results:
        # unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (# int(tl[0]),int(tl[1])
            int(tl[0] if tl[0] == bl[0] else round(min(tl[0], bl[0])))
            ,int(tl[1] if tl[1] == tr[1] else round(min(tl[1], tr[1])))
            )
        tr = (int(tr[0]), int(tr[1]))
        br = (# int(br[0]), int(br[1])
            int(br[0] if tr[0] == br[0] else round(max(tr[0], br[0])))
            ,int(br[1] if br[1] == bl[1] else round(max(br[1], bl[1])))
            )
        bl = (int(bl[0]), int(bl[1]))
        linethick = 5
        cv2.rectangle(bbx, tl, br, (226, 43, 138), int(linethick*x_ratio))

    # text detection
    result_text = []
    pixel_range = 5
    for i in range(len(results)):
        y_start = round(results[i][0][0][1]) if results[i][0][0][1] == results[i][0][1][1] else round(min(results[i][0][0][1], results[i][0][1][1])) if round(min(results[i][0][0][1], results[i][0][1][1])) > 0 else 0
        y_end = round(results[i][0][2][1]) if results[i][0][2][1] == results[i][0][3][1] else round(max(results[i][0][2][1], results[i][0][3][1])) if round(max(results[i][0][2][1], results[i][0][3][1])) < img.shape[0] else img.shape[0]
        x_start = round(results[i][0][0][0]) if results[i][0][0][0] == results[i][0][3][0] else round(min(results[i][0][0][0], results[i][0][3][0])) if round(min(results[i][0][0][0], results[i][0][3][0])) > 0 else 0
        x_end = round(results[i][0][2][0]) if results[i][0][1][0] == results[i][0][2][0] else round(max(results[i][0][1][0], results[i][0][2][0])) if round(max(results[i][0][1][0], results[i][0][2][0])) < img.shape[1] else img.shape[1]
        # region = img[y_start-pixel_range:y_end+pixel_range, x_start-pixel_range:x_end+pixel_range].copy()
        region = img[
                     y_start-pixel_range if y_start-pixel_range > 0 else 0
                    :y_end+pixel_range if y_end+pixel_range < img.shape[0] else img.shape[0]
                    ,x_start-pixel_range if x_start-pixel_range > 0 else 0
                    :x_end+pixel_range if x_end+pixel_range < img.shape[1] else img.shape[1]
                    ].copy()
        configs = '-l kor+eng --psm 6 --oem 1'
        text_tess = pytesseract.image_to_string(region#,lang=('kor+eng')
                                        ,config=configs
                                        )#.split('\n')#,config=configs).split()
        arr = text_tess.split('\n')[0:-1]
        text_tess = '\n'.join(arr)
        # print(file[len(workdir)+1:],results[i][0],'easyocr',results[i][1],'tesseract',text_tess)#,results[i][2]
        result_text.append((file[len(workdir)+1:],results[i][0],x_start,y_start,x_end,y_end,results[i][1],text_tess))

    # result save
    save_info = savedir + file[len(workdir):]

    cv2.imwrite(save_info, bbx)

    df = pd.DataFrame(result_text,columns=['filename','bbox','x_start','y_start','x_end','y_end','easyocr_text','tesseract_text'])
    with pd.ExcelWriter('%s/%s.xlsx' % (savedir, file_name), mode='a',engine='openpyxl') as writer:
        df.to_excel(writer,sheet_name=file[len(workdir)+1:len(workdir)+1+11], index=False)
# plt.rcParams['figure.figsize'] = (20,20)
# plt.imshow(bbx)
# %%
#%%
# word base
x_ratio = 1.0
y_ratio = 1.0
width_th = 0.01
savedir = 'C:/Users/smcljy/data/20211210_OCR_hakathon/img_easyocr_word_detection/'
file_name = 'text_export_result_easyocr_word'
nan_df = pd.DataFrame()
nan_df.to_excel('%s/%s.xlsx'% (savedir, file_name)) 

for file in filelist:#[117:118]linux #[6:7]window
    img = cv2.imread(file)
    bbx = img.copy()
    # img = cv2.imread(file,cv2.COLOR_BGR2GRAY)
    # ret, img = cv2.threshold(img, 150,255, cv2.THRESH_BINARY_INV)
    # bbx = cv2.resize(img, dsize=(0,0), fx=x_ratio, fy=y_ratio, interpolation=cv2.INTER_LANCZOS4)
    # bbx = img.copy()

    results = reader.readtext(bbx,width_ths=width_th)#))
    # y_start position sort
    results = sorted(results, key=lambda x: (x[0][0][1]))

    # bounding box for text region and file write
    for (bbox, text, prob) in results:
        # unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (# int(tl[0]),int(tl[1])
            int(tl[0] if tl[0] == bl[0] else round(min(tl[0], bl[0])))
            ,int(tl[1] if tl[1] == tr[1] else round(min(tl[1], tr[1])))
            )
        tr = (int(tr[0]), int(tr[1]))
        br = (# int(br[0]), int(br[1])
            int(br[0] if tr[0] == br[0] else round(max(tr[0], br[0])))
            ,int(br[1] if br[1] == bl[1] else round(max(br[1], bl[1])))
            )
        bl = (int(bl[0]), int(bl[1]))
        linethick = 5
        cv2.rectangle(bbx, tl, br, (0, 0, 255), int(linethick*x_ratio))

    # text detection
    result_text = []
    pixel_range = 5
    for i in range(len(results)):
        y_start = round(results[i][0][0][1]) if results[i][0][0][1] == results[i][0][1][1] else round(min(results[i][0][0][1], results[i][0][1][1])) if round(min(results[i][0][0][1], results[i][0][1][1])) > 0 else 0
        y_end = round(results[i][0][2][1]) if results[i][0][2][1] == results[i][0][3][1] else round(max(results[i][0][2][1], results[i][0][3][1])) if round(max(results[i][0][2][1], results[i][0][3][1])) < img.shape[0] else img.shape[0]
        x_start = round(results[i][0][0][0]) if results[i][0][0][0] == results[i][0][3][0] else round(min(results[i][0][0][0], results[i][0][3][0])) if round(min(results[i][0][0][0], results[i][0][3][0])) > 0 else 0
        x_end = round(results[i][0][2][0]) if results[i][0][1][0] == results[i][0][2][0] else round(max(results[i][0][1][0], results[i][0][2][0])) if round(max(results[i][0][1][0], results[i][0][2][0])) < img.shape[1] else img.shape[1]
        # region = img[y_start-pixel_range:y_end+pixel_range, x_start-pixel_range:x_end+pixel_range].copy()
        region = img[
                     y_start-pixel_range if y_start-pixel_range > 0 else 0
                    :y_end+pixel_range if y_end+pixel_range < img.shape[0] else img.shape[0]
                    ,x_start-pixel_range if x_start-pixel_range > 0 else 0
                    :x_end+pixel_range if x_end+pixel_range < img.shape[1] else img.shape[1]
                    ].copy()
        configs = '-l kor+eng --psm 6 --oem 1'
        text_tess = pytesseract.image_to_string(region#,lang=('kor+eng')
                                        ,config=configs
                                        )#.split('\n')#,config=configs).split()
        arr = text_tess.split('\n')[0:-1]
        text_tess = '\n'.join(arr)
        # print(file[len(workdir)+1:],results[i][0],'easyocr',results[i][1],'tesseract',text_tess)#,results[i][2]
        result_text.append((file[len(workdir)+1:],results[i][0],x_start,y_start,x_end,y_end,results[i][1],text_tess))

    # result save
    save_info = savedir + file[len(workdir):]

    cv2.imwrite(save_info, bbx)

    df = pd.DataFrame(result_text,columns=['filename','bbox','x_start','y_start','x_end','y_end','easyocr_text','tesseract_text'])
    with pd.ExcelWriter('%s/%s.xlsx' % (savedir, file_name), mode='a',engine='openpyxl') as writer:
        df.to_excel(writer,sheet_name=file[len(workdir)+1:len(workdir)+1+11], index=False)
# plt.rcParams['figure.figsize'] = (20,20)
# plt.imshow(bbx)
# %%
