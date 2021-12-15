# %%
import cv2
import json
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import os, argparse
from tqdm import tqdm
# %%
def define_argparser():
    p = argparse.ArgumentParser()
    p.add_argument('--root_path', required=True)
    p.add_argument('--save_path', required=True)
    config = p.parse_args()
    return config

def main(config):
    if os.path.exists(config.save_path):
        pass
    else:
        os.mkdir(config.save_path)
    image_root = os.path.join(config.root_path, 'images')
    annotation_path = glob(config.root_path+'/annotations/*')
    # %%
    for path in tqdm(annotation_path):
        with open(path, "r") as json_file:
            data = json.load(json_file)
        for i in range(len(data['images'])):
            # read image and store image name for reuse
            image_name = data['images'][i]['name']
            img = cv2.imread(os.path.join(image_root,image_name))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Draw bounding box and save
            for dic in data['annotations'][i]['polygons']:
                points = np.array(dic['points'], np.int32)
                right_top = tuple(np.max(points, axis=0))
                left_bottom = tuple(np.min(points, axis=0))
                img = cv2.rectangle(img, tuple(left_bottom), tuple(right_top), 
                                    (0, 255, 0), 10)
            plt.imsave(os.path.join(config.save_path, image_name), img)

if __name__ == "__main__":
    config = define_argparser()
    main(config)