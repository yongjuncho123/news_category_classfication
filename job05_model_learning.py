import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *

# 학습 데이터 불러오기
X_train, X_test, Y_train, Y_test = np.load(
    './crawling_data/news_data_max_17_wordsize_12426.npy',
allow_pickle=True)
# print(X_train.shape, Y_train.shape)
# print(X_test.shape, Y_test.shape)

# 모델 만들기
model = Sequential()
model.add(Embedding(12426, 300, input_length=17)) # 이 레이어에선 단어들의 의미를 학습 / 12426개의 단어 갯수만큼 차원공간에 단어 배치(12426차원)
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu')) # 단어도 서순이 있기 때문에 conv를 쓰는데 단어는 1차원이라 1d 쓰고 커널도 1개를 쓴다
model.add(MaxPool1D(pool_size=1) ) # 맥스풀은 n개중 가장 큰값이지만 여기선 1개중 가장 큰값이라 의미 x 콘브를 써서 쓰는거
model.add(LSTM(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(6, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128,
                     epochs=10, validation_data=(X_test, Y_test))
model.save('./models/news_category_classfication_model')
plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.legend()
plt.show()

