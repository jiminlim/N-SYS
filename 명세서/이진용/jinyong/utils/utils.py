from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import argparse
import sys
import matplotlib.image as mpimg
from sklearn.preprocessing import normalize #정규화

# Req. 2-2	세팅 값 저장
def save_config():
	parser = argparse.ArgumentParser()
	# parser.add_argument('--tg', nargs='+', hel='crawling start')
	# args = parser.parse_args()
	# print(args)
	f = open('save_config.txt', 'a')
	now = datetime.now()
	f.write(str(now)+" ")
	for arg in sys.argv:
		f.write(arg+" ")
	f.write('\n')
	pass


# Req. 4-1	이미지와 캡션 시각화
def visualize_img_caption(img_path,caption):
	# print(img_path)
	# print(caption)
	for i,cap in zip(img_path,caption):
		img = mpimg.imread(i)
		# print(img)
		plt.imshow(img)
		plt.title(cap)
		plt.show()
	pass

##req1-1 이미지 파일 로드
def image_check(img_path,nomal_flag):
	img = plt.imread(img_path)

	# 정규화  최소, 최대값을 구해서 '0~1' 범위로 변환
	if nomal_flag:
		img = (img - img.min(axis=0)) / (img.max(axis=0) - img.min(axis=0))



	# 평균 print(np.mean(img))
	# 분산 print(np.std(img))

	fig = plt.figure(figsize=(9,9))	# image size change
	plt.imshow(img)
	plt.show()