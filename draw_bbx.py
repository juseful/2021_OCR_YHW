# %%
import cv2
import pandas as pd
import json
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
# %%
cv2.__version__
# %%
annotation = glob('./medicine/annotations/*')
# %%
with open(annotation[0], "r") as json_file:
    data = json.load(json_file)
# %%
image_root = './medicine/images/'
image_name = data['images'][0]['name']
img_path = image_root+image_name
img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
# %%
for dic in data['annotations'][0]['polygons']:
    points = np.array(dic['points'], np.int32)
    right_top = tuple(np.max(points, axis=0))
    left_bottom = tuple(np.min(points, axis=0))
    img = cv2.rectangle(img, tuple(left_bottom), tuple(right_top), 
                         (0, 255, 0), 10)
# %%

# %%
plt.imshow(img)
# %%
plt.imsave('./temp.jpeg', img)
