import argparse
import pandas as pd
# Req. 2-1	Config.py 파일 생성

# 캡션 데이터가 있는 파일 경로 (예시)
parser = argparse.ArgumentParser(description='ssafy skeletoncode.')
parser.add_argument('--caption_file_path', type=str, default='C:\\ssafy\\pj2-skeleton\\ai-skeleton\\datasets\\captions.csv')
parser.add_argument('--image_file_path', type=str, default='C:\\ssafy\\pj2-skeleton\\ai-skeleton\\datasets\\images\\')
parser.add_argument('--encoding', default='ISO-8859-1')
# parser.add_argument("square", help="display a square of a given number", type=int)
parser.add_argument("--image_name",type=str,default='36979.jpg')
args = parser.parse_args()
# df = pd.read_csv(args.caption_file_path, encoding = 'ISO-8859-1',sep='|')
# print(df.columns)

print(args.caption_file_path)
print(args.encoding)
print("logger - image print")
print(args.image_file_path+args.image_name)
# print(args.square**2)



# csv_reader = csv.reader(
#     io.open(options.caption_file_path, "r", encoding=options.encoding),
#     delimiter="|",
#     quotechar='"'
# )
#
# for row in csv_reader:
#     print(row)
#
# print(options)
# print('성공')
#

#!/usr/bin/env python
# encoding: utf-8

"""
Sample program to read a CSV file.
This works for both Python 2/3.
"""

# from __future__ import print_function
# from __future__ import unicode_literals
# import argparse
# import csv
# import io
#
# import six


# parser = argparse.ArgumentParser()
# parser.add_argument('--csv_file_path', type=str, default='.\\datasets\\captions.csv')
# # parser.add_argument("--encoding", default="utf_8")
# options = parser.parse_args()
#
# csv_reader = csv.reader(
#     io.open(options.csv_file_path, "r"
#             # , encoding=options.encoding
#     ),
#     delimiter="|",
#     quotechar='"'
# )
#
# print("--- header ---\n{}\n".format(six.next(csv_reader)))
# print("--- data ---")
# for row in csv_reader:
#     print(row)
# import pandas as pd
# import numpy as np
# import matplotlib as plt
#
# df = pd.read_csv('.\\datasets\\captions.csv', encoding = 'ISO-8859-1',sep='|')
# print(df[0:10])
# print(df.columns) # 컬럼명
# print(df.describe())
# =df.image_name
# print(s)