import pandas as pd
import  numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model

pd.set_option('display.unicode.east_asia_width', True)
pd.set_option('display.max_columns', 20)
df = pd.read_csv('./crawling_data/naver_headline_news_20220527.csv')
# print(df.head())
# df.info()

# 다중분류기 만들기 / 인풋 6개 아웃풋 6개 / softmax / 문자데이터를 숫자데이터로 변해서 / 타이틀을 x로 카테고리를 y로

### 전처리 ###

X = df['titles']
Y = df['category']

# Y값 먼저처리
# 라벨 인코딩
with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
labeled_Y = encoder.transform(Y) # 이미 데이터가 만들어져있기 떄문에 우린 라벨링만 하면 된다 그래서 핏 트랜스를 쓰지 않고 트랜스만 쓴다.
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

with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(X) # 라벨링된 데이터를 연속형자료로 바꿔줌
for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 17:
        tokened_X[i] = tokened_X[i][:17] # 단어 갯수가 17보다 많으면 그건 버리겠다

X_pad = pad_sequences(tokened_X, 17)
# print((X_pad[:5]))
# model = load_model('./저장되있는것으로 해야됨')
preds = model.predict(X_pad)
predicts = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predicts.append([most, second])

df['predict'] = predicts

print(df.head(30))

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] == df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 'O'
    else:
        df.loc[i, 'OX'] = 'X'
print(df.head(30))

print(df['OX'].value_counts())
print(df['OX'].value_counts()/len(df))

for i in range(len(df)):
    if df['category'][i] not in df['predict'][i]:
        print(df.iloc[i])