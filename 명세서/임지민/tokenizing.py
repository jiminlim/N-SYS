from tensorflow.keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pickle

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

#req2-1.텍스트 데이터 토큰화 
text = "A barber is a person. a barber is good person. a barber is huge person. he Knew A Secret! The Secret He Kept is huge secret. Huge secret. His barber kept his word. a barber kept his word. His barber kept his secret. But keeping and keeping such a huge secret to himself was driving the barber crazy. the barber went up a huge mountain."
text = sent_tokenize(text) #여러문장 -> 한문장

# 정제와 단어 토큰화
vocab = {} # 파이썬의 dictionary 자료형
sentences = []
stop_words = set(stopwords.words('english'))

for i in text:
    sentence = word_tokenize(i) # 한문장 -> 단어 토큰화를 수행합니다.
    result = []

    for word in sentence: 
        word = word.lower() # 모든 단어를 소문자화하여 단어의 개수를 줄입니다.
        if word not in stop_words: # 단어 토큰화 된 결과에 대해서 불용어를 제거합니다.
            if len(word) > 2: # 단어 길이가 2이하인 경우에 대하여 추가로 단어를 제거합니다.
                result.append(word)
                if word not in vocab:
                    vocab[word] = 0 
                vocab[word] += 1
    sentences.append(result) 
# print("----------")
# print(sentences)

# # # # # 정수 인코딩 
tokenizer = Tokenizer()
for data in sentences:
    tokenizer.fit_on_texts(sentences) # 빈도수 
    encoded = tokenizer.texts_to_sequences(sentences)
print("----------")
print(encoded)

# 상위 5개 단어만 사용
# vocab_size = 5
# tokenizer = Tokenizer(num_words = vocab_size + 1) 
# tokenizer.fit_on_texts(sentences)
# print("----------")
# print(tokenizer.word_counts)
# print("----------")
# print(tokenizer.texts_to_sequences(sentences))
print("----------")
# # # 앞0 뒤1 붙임


# # 패딩 =2 길이 30으로 array 설정
encoded = tokenizer.texts_to_sequences(sentences)
max_len = 30
for item in encoded: # 각 문장에 대해서
    while len(item) < max_len:   # max_len보다 작으면
        item.append(0)

padded_np = np.array(encoded)
print(padded_np)


# req2-2 tokenizer 저장 및 불러오기
# saving
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# loading
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer2 = pickle.load(handle)


