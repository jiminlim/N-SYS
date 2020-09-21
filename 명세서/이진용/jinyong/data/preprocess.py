## 모델을 적합하게 데이터 가공 : 전처리과정
import os
import csv
import numpy as np
import pandas as pd
import config
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from tensorflow import feature_column
import pickle


# Req. 3-1	이미지 경로 및 캡션 불러오기
def get_path_caption():
    print('logger - get_path_caption method')
    df = pd.read_csv(config.args.caption_file_path, encoding='ISO-8859-1', sep='|')
    # print('check'+config.args.caption_file_path)
    image_name = df['image_name']
    comment = df[' comment']
    print(df)
    return image_name, comment


# Req. 3-2	전체 데이터셋을 분리해 저장하기
def dataset_split_save():
    df = pd.read_csv(config.args.caption_file_path, encoding='ISO-8859-1', sep='|')

    train, test = train_test_split(df, test_size=0.2)
    train, val = train_test_split(train, test_size=0.2)

    print(len(train), '훈련 샘플')  # 101705
    print(len(val), '검증 샘플')  # 25427
    print(len(test), '테스트 샘플')  # 31783

    split_save_path = 'C:\\ssafy\\pj2-skeleton\\ai-skeleton\\datasets\\'

    train.to_csv(split_save_path + 'train.csv')
    val.to_csv(split_save_path + 'val.csv')
    test.to_csv(split_save_path + 'test.csv')

    return split_save_path + 'train.csv', split_save_path + 'val.csv', split_save_path + 'test.csv'


# Req. 3-3	저장된 데이터셋 불러오기
def get_data_file(data_path):
    data = pd.read_csv(data_path, encoding='ISO-8859-1')
    return data


# 판다스 데이터프레임으로부터 tf.data 데이터셋을 만들기 위한 함수
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop(' comment')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds


# Req. 3-4	데이터 샘플링
def sampling_data(data, n):
    # data = pd.read_csv(data_path, encoding='ISO-8859-1')
    df = data.sample(n)
    # df2 = pd.DataFrame(df['image_name'], df[' comment'])
    return df


def tokenize(sentences):
    # t = Tokenizer()
    # fit_text = "The earth is an awesome place live"
    # t.fit_on_texts([fit_text])
    #
    # test_text = "The earth is an great place live"
    # sequences = t.texts_to_sequences([test_text])[0]
    #
    # print("sequences : ", sequences)  # great는 단어 집합(vocabulary)에 없으므로 출력되지 않는다.
    # print("word_index : ", t.word_index)  # 단어 집합(vocabulary) 출력

    # tokenizer = Tokenizer()
    # tokenizer.fit_on_texts(sentences) # 텍스 빈도수 생성
    # print(tokenizer.word_index) # 빈도수 높은 단어가 낮은 수부터 시작
    # print(tokenizer.word_counts) # 빈도수 표시
    # print(tokenizer.texts_to_sequences(sentences))

    # vocab_size = 5
    # tokenizer = Tokenizer(num_words=vocab_size + 2, oov_token='OOV')
    # # 빈도수 상위 5개 단어만 사용. 숫자 0과 OOV를 고려해서 단어 집합의 크기는 +2
    # tokenizer.fit_on_texts(sentences)
    # print('단어 OOV의 인덱스 : {}'.format(tokenizer.word_index['OOV']))
    # print(tokenizer.texts_to_sequences(sentences))

    # encoded = tokenizer.texts_to_sequences(sentences)
    # padded = pad_sequences(encoded, padding = 'post',maxlen=5)
    # print(padded)
    # # saving
    # with open('tokenizer.pickle', 'wb') as handle:
    #     pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # sentence = "Don't be fooled by the dark sounding name, Mr. Jone's Orphanage is as cheery as cheery goes for a pastry shop."
    print('[logger - sentences] ' + sentences)
    words = text_to_word_sequence(sentences)  # 문장 토큰화 (모든 알파벳을 소문자로 바꾸면서 온점이나 컴마, 느낌표 등의 구두점을 제거)
    print('[logger - token] ')
    print(words)  # list
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(words)  # fit_on_texts()안에 코퍼스를 입력으로 하면 빈도수를 기준으로 단어 집합을 생성한다.

    # print(tokenizer.word_index) # 빈도수 높은 단어가 낮은 수부터 시작
    # print(tokenizer.word_counts) # 빈도수 표시
    encoded = tokenizer.texts_to_sequences([words])
    print(encoded)
    # print(words)

    # encoded = tokenizer.texts_to_sequences(sentences)
    padded = pad_sequences(encoded, padding='post', maxlen=30)  # padding 0으로 채우기
    print(padded)
    save_tokenizer(padded)
    print('tttest')
    data = load_tokenizer()
    print(data)


def save_tokenizer(tokenizer):
    # saving
    with open('tokenizer.pickle', 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_tokenizer():
    with open('tokenizer.pickle', 'rb') as f:
        data = pickle.load(f)
    return data
