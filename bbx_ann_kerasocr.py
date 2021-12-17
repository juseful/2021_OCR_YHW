# %%
import matplotlib.pyplot as plt

import keras_ocr
import cv2
import pytesseract
from pytesseract import Output
import os
import pandas as pd

# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.
pipeline = keras_ocr.pipeline.Pipeline()

# %%
workdir_ann = "C:/Users/smcljy/data/20211210_OCR_hakathon/img_annotation_detection/"

filelist_ann = []

for (root, directories, files) in os.walk(workdir_ann):
    for file in files:
        if '.jpg' in file.lower():
            file_path = os.path.join(root, file)
            filelist_ann.append(file_path)
        if '.jpeg' in file.lower():
            file_path = os.path.join(root, file)
            filelist_ann.append(file_path)

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

# filelist_ann, filelist
#%%
# word base
x_ratio = 1.0
y_ratio = 1.0
width_th = 0.01
savedir = 'C:/Users/smcljy/data/20211210_OCR_hakathon/img_detection_01kerasocr/'
file_name = 'text_export_result_kerasocr'

result_text = []

for file in filelist:#[117:118]linux #[6:7]window
    
    images = [file]
    prediction_groups = pipeline.recognize(images)

    # y_start position sort
    prediction_groups = sorted(prediction_groups, key=lambda x: (x[0][1][0][1]))

    img = cv2.imread(file)
    ann_index = [int(i) for i in range(len(filelist_ann)) if file[len(workdir):] in filelist_ann[i]]
    ann_img = cv2.imread(filelist_ann[ann_index[0]])

    pixel_range = 0
    
    for i in range(len(prediction_groups[0])):
        bbox = prediction_groups[0][i][1]

        tl, tr, br, bl =  bbox[0], bbox[1], bbox[2], bbox[3]

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
        cv2.rectangle(ann_img, tl, br, (255, 0, 0), 5)

        y_start = tl[1]
        y_end = br[1]
        x_start = tl[0]
        x_end = br[0]
        # region = img[y_start-pixel_range:y_end+pixel_range, x_start-pixel_range:x_end+pixel_range].copy()
        region = img[
                     y_start-pixel_range if y_start-pixel_range > 0 else 0
                    :y_end+pixel_range if y_end+pixel_range < img.shape[0] else img.shape[0]
                    ,x_start-pixel_range if x_start-pixel_range > 0 else 0
                    :x_end+pixel_range if x_end+pixel_range < img.shape[1] else img.shape[1]
                    ].copy()
        configs = '-l kor+eng --psm 6 --oem 1'
        text = pytesseract.image_to_string(region#,lang=('kor+eng')
                                        ,config=configs
                                        )#.split('\n')#,config=configs).split()
        arr = text.split('\n')[0:-1]
        text = '\n'.join(arr)
        result_text.append((file[len(workdir)+1:],prediction_groups[0][i][1],x_start,y_start,x_end,y_end,text))

    # result save
    save_info = savedir + file[len(workdir):]

    cv2.imwrite(save_info, ann_img)

df = pd.DataFrame(result_text,columns=['filename','bbox','x_start','y_start','x_end','y_end','text'])
with pd.ExcelWriter('%s/%s.xlsx' % (savedir, file_name), mode='w',engine='openpyxl') as writer:
    df.to_excel(writer,sheet_name=file[len(workdir)+1:len(workdir)+1+11], index=False)
# %%
