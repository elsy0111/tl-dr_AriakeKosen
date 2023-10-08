import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist

# MNISTデータセットを読み込む
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# データを前処理する
train_images = train_images.reshape((60000, 28, 28, 1))
print(type(train_images))
print(len(train_images))
print(len(train_images[0]))
print(len(train_images[0][0]))
test_images = test_images.reshape((10000, 28, 28, 1))

# # ピクセル値を0から1の範囲にスケーリング
# train_images, test_images = train_images / 255.0, test_images / 255.0

# # モデルを定義する
# model = models.Sequential([
#     layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.Flatten(),
#     layers.Dense(64, activation='relu'),
#     layers.Dense(10, activation='softmax')
# ])

# # モデルの概要を表示
# model.summary()

# # モデルをコンパイル
# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# # モデルをトレーニング
# model.fit(train_images, train_labels, epochs=5, batch_size=64, validation_data=(test_images, test_labels))
