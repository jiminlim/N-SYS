from datetime import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import tensorflow as tf


# Req. 2-2	세팅 값 저장
def save_config():
    # parser.add_argument('--img_file_path', type=str, default='.\\datasets\\images')
	pass


# Req. 4-1	이미지와 캡션 시각화
def visualize_img_caption(img, captions):
	for img_name,caption in zip(img,captions):
			img = mpimg.imread('./datasets/images/'+img_name)
			print(img)
			plt.imshow(img)
			plt.title(caption)
			plt.show()

