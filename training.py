import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import joblib

# Training Data Preprocessing
train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

training_set = train_datagen.flow_from_directory('training_set', 
                                                 target_size=(64, 64), 
                                                 batch_size=20, 
                                                 class_mode='binary')

# Testing Data Preprocessing
test_datagen = ImageDataGenerator(rescale=1./255)

test_set = test_datagen.flow_from_directory('test_set', 
                                            target_size=(64, 64), 
                                            batch_size=20, 
                                            class_mode='binary')

# Building the CNN
cnn = tf.keras.models.Sequential()

cnn.add(tf.keras.layers.Conv2D(filters=40, activation='relu', kernel_size=3, input_shape=[64, 64, 3]))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
cnn.add(tf.keras.layers.Conv2D(filters=40, activation='relu', kernel_size=3))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
cnn.add(tf.keras.layers.Flatten())
cnn.add(tf.keras.layers.Dense(units=100, activation='relu'))
cnn.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

# Compiling the CNN
cnn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Training the CNN
cnn.fit(x=training_set, validation_data=test_set, epochs=20)

# Save the model
joblib.dump(cnn, 'cat_dog_classifier.pkl')
