import pandas as pd
import  numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

# pd.set_option('display.unicode.east_asia_width', True)
df = pd.read_csv('./crawling_data/naver_news_titles_20220526.csv')
# print(df.head())
# df.info()

# 다중분류기 만들기 / 인풋 6개 아웃풋 6개 / softmax / 문자데이터를 숫자데이터로 변해서 / 타이틀을 x로 카테고리를 y로

### 전처리 ###

X = df['titles']
Y = df['category']

# Y값 먼저처리
# 라벨 인코딩
encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)
# print(labeled_Y[:3])  #라벨 인코딩은 오름차순으로 정렬된 값을 보여줌 / 나중에 모델이 000100으로 예측한다면 정치섹션이구나로 암
label = encoder.classes_
# print(label)
with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

#원핫인코딩
onehot_Y = to_categorical(labeled_Y) # 섹션의 이름을 0과 1로 구분지음
# print(onehot_Y)

# X값 처리
# 문장의 구조를 형태소 단위로 쪼개준다
okt = Okt()
# okt_morph_X = okt.morphs(X[7], stem=True) # 스템트루를 주면 동사의 원형으로 바꿔준다
# print(okt_morph_X)

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
# print(X[:10])

# 불용어 처리(감탄사, 대명사, 목적조사, 주격조사 등 조사들은 어떤 카테고리에도 나올 수 있기 때문에 우린 키워드만 찾아서 학습시켜야한다), stop워드에 있는 단어와 겹치면 그 단어는 삭제할거임
stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0) # 0번컬럼이 인덱스다

for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words) # 토크나이저용 하나의 문자응로
# print(X[:5])
# print(words)

# 이제 형태소를 숫자로 매칭해줄거다(토크나이저) / 딕셔너리 형태로 권성동 : 1 윤종원 : 2 이런식으로 라벨링 해줌, 단 토크나이저에 줄 땐 하나의 문장으로 줘야됨
token = Tokenizer()
token.fit_on_texts(X) # 핏온텍스트 하면 라벨링
tokened_X = token.texts_to_sequences(X) # 라벨링된 데이터를 연속형자료로 바꿔줌
wordsize = len(token.word_index) + 1 #0도 포함시키려고 1더함 / 유니크한 값
print(tokened_X)
# 유니크한 값 보기(모델만들 때 모델에 단어의 갯수를 줘야해서 유니크한 값의 갯수를 알아야한다)
# print(token.word_index)

with open('./models/news_token.pickle', 'wb') as f:
    pickle.dump(token, f)
# 데이터 손실을 줄이기 위해 문장이 제일 긴 단어로 맞춰준다(이보다 짧은건 앞자리를 0으로 채울거임)
max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

# 0으로 채우기 / max값으로 토큰 길이를 채워라
X_pad = pad_sequences(tokened_X, max)
# print(X_pad)

# 라벨이라 스케일링을 할 필요 없다.

X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./crawling_data/news_data_max_{}_wordsize_{}'.format(max, wordsize), xy)