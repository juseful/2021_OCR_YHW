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
# %%
# using tesseract
savedir = 'C:/Users/smcljy/data/20211210_OCR_hakathon/img_detection_01kerasocr/'
file_name = 'text_export_result_kerasocr'

result_text = []

for file in filelist:

    images = [file]

    # Each list of predictions in prediction_groups is a list of
    # (word, box) tuples.
    prediction_groups = pipeline.recognize(images)

    # y_start position sort
    prediction_groups = sorted(prediction_groups, key=lambda x: (x[0][1][0][1]))

    img = cv2.imread(file)
    bbx = img.copy()

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
        cv2.rectangle(bbx, tl, br, (255, 0, 0), 10)

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
        # print(text)

    # result save
    save_info = savedir + file[len(workdir):]

    cv2.imwrite(save_info, bbx)

df = pd.DataFrame(result_text,columns=['filename','bbox','x_start','y_start','x_end','y_end','text'])
with pd.ExcelWriter('%s/%s.xlsx' % (savedir, file_name), mode='w',engine='openpyxl') as writer:
    df.to_excel(writer,sheet_name=file[len(workdir)+1:len(workdir)+1+11], index=False)
        
# plt.rcParams['figure.figsize'] = (20,20)
# plt.imshow(img)
# %%
