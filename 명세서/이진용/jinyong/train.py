import config
from data import preprocess
from utils import utils
import pandas as pd

# config 저장
utils.save_config()
#
#
# # 이미지 경로 및 캡션 불러오기
#
# img_paths, captions = preprocess.get_path_caption()
# # print('logger - image_name: {}'.format(img_paths))
# # print('logger - caption: {}'.format(captions))
#
#
# 전체 데이터셋을 분리해 저장하기
# train_dataset_path, val_dataset_path = \
train_dataset_path, val_dataset_path, test_dataset_path = preprocess.dataset_split_save()
print(train_dataset_path) # C:\ssafy\pj2-skeleton\ai-skeleton\datasets\train.csv
print(val_dataset_path) # C:\ssafy\pj2-skeleton\ai-skeleton\datasets\val.csv
print(test_dataset_path) # C:\ssafy\pj2-skeleton\ai-skeleton\datasets\test.csv



# # 저장된 데이터셋 불러오기
#flag 0(train), 1(val), 2(test)
# flag = 2
# if flag==0:
#     data = preprocess.get_data_file(train_dataset_path)
# elif flag==1:
#     data = preprocess.get_data_file(val_dataset_path)
# elif flag==2:
#     data = preprocess.get_data_file(test_dataset_path)
train = preprocess.get_data_file(train_dataset_path)
val = preprocess.get_data_file(val_dataset_path)
test = preprocess.get_data_file(test_dataset_path)
# print(data.head())


# 데이터 샘플링
# n = 10
# # if config.do_sampling:
# data = preprocess.sampling_data(data,n)
# print(data)

print('----------'*20)
batch_size = 5 # 예제를 위해 작은 배치 크기를 사용합니다.
train_ds = preprocess.df_to_dataset(train, batch_size=batch_size)
val_ds = preprocess.df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = preprocess.df_to_dataset(test, shuffle=False, batch_size=batch_size)

for feature_batch, label_batch in train_ds.take(1):
    print('전체 특성:', list(feature_batch.keys()))
    print('이미지 이름의 배치:', feature_batch['image_name'])
    print('comment의 배치:', label_batch )


#
#
# # 이미지와 캡션 시각화 하기
# utils.visualize_img_caption(config.args.image_file_path+img_paths,caption)

# ## req 2-1
# # sentences=[['barber', 'person'], ['barber', 'good', 'person'], ['barber', 'huge', 'person'], ['knew', 'secret'], ['secret', 'kept', 'huge', 'secret'], ['huge', 'secret'], ['barber', 'kept', 'word'], ['barber', 'kept', 'word'], ['barber', 'kept', 'secret'], ['keeping', 'keeping', 'huge', 'secret', 'driving', 'barber', 'crazy'], ['barber', 'went', 'huge', 'mountain']]
# sentences = "Don't be fooled by the dark sounding name, Mr. Jone's Orphanage is as cheery as cheery goes for a pastry shop."
# preprocess.tokenize(sentences)

