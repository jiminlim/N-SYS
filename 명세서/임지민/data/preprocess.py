import os
import csv
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from config import config

# Req. 3-1	이미지 경로 및 캡션 불러오기
def get_path_caption(data):
    # read_csv =pd.read_csv(csvfile,sep='|', encoding='UTF8', names=['image_name','comment_number','comment'], header=None)

    # data=dict()
    # for row_index, row in read_csv.iterrows():
    #     if data.get(row.image_name):
    #         data[row.image_name].append(row.comment)
    #     else:
    #         data[row.image_name]=[row.comment]

    img = data['image_name']
    caption = data['comment']
    return img, caption


# Req. 3-2	전체 데이터셋을 분리해 저장하기
def dataset_split_save(captions):

    train_data, data = train_test_split(captions, test_size=0.4, random_state=66)
    val_data,test_data = train_test_split(data, test_size=0.5, random_state=66)
   
    train_dataframe = pd.DataFrame(train_data)
    train_dataset_path='./datasets/train_data.csv'
    train_dataframe.to_csv(train_dataset_path,header=False,sep='|')
    
    val_dataframe = pd.DataFrame(val_data)
    val_dataset_path='./datasets/val_data.csv'
    val_dataframe.to_csv(val_dataset_path,header=False,sep='|')

    test_dataframe= pd.DataFrame(test_data)
    test_dataset_path='./datasets/test_data.csv'
    test_dataframe.to_csv(test_dataset_path,header=False,sep='|')

    return train_dataset_path, val_dataset_path


# Req. 3-3	저장된 데이터셋 불러오기
def get_data_file(answer):
    # 'train','valid','test
    print(answer,'을 할 것이다')

    train_dataset_path='./datasets/train_data.csv'
    val_dataset_path='./datasets/val_data.csv'
    test_dataset_path='./datasets/test_data.csv'
    data_path=''
    if answer=='train':
        data_path=train_dataset_path
    elif answer=='valid':
        data_path=val_dataset_path
    else:
        data_path=test_dataset_path

    return data_path

# Req. 3-4	데이터 샘플링
def sampling_data(answer,data_path):
    data =pd.read_csv(data_path,sep='|', encoding='UTF8', names=['image_name','comment_number','comment'], header=None)
    df = data.sample(answer)
    img, caption = get_path_caption(df)
    return img, caption
