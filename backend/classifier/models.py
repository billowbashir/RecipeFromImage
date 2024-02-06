import cv2
import os
import ssl
import numpy as np
from django.conf import settings
from django.db import models
import tensorflow as tf
from tensorflow.keras import layers, models as k
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
from tensorflow.keras.models import load_model



# training code below

# input_size = (299, 299)
# num_classes = 36  # Replace with the actual number of classes (fruits and vegetables)

# # Paths to your datasets
# train_dir = '././../train'
# test_dir = '././../test'
# val_dir = '././../validation'

# # Path to save the model
# saved_model_path = '././../Model'

# # Check if a saved model exists


# # Load and preprocess the data
# train_datagen = ImageDataGenerator(rescale=1./255)
# train_generator = train_datagen.flow_from_directory(
#     train_dir,
#     target_size=input_size,
#     batch_size=8,
#     class_mode='categorical'
# )

# test_datagen = ImageDataGenerator(rescale=1./255)
# test_generator = test_datagen.flow_from_directory(
#     test_dir,
#     target_size=input_size,
#     batch_size=8,
#     class_mode='categorical'
# )

# val_datagen = ImageDataGenerator(rescale=1./255)
# val_generator = val_datagen.flow_from_directory(
#     val_dir,
#     target_size=input_size,
#     batch_size=8,
#     class_mode='categorical'
# )

# # Define your model
# model = k.Sequential()
# model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(input_size[0], input_size[1], 3)))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(128, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Flatten())
# model.add(layers.Dense(128, activation='relu'))
# model.add(layers.Dense(num_classes, activation='softmax'))

# # Compile your model
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# # Train your model
# model.fit(train_generator, epochs=5, steps_per_epoch=len(train_generator),
#             validation_data=val_generator, validation_steps=len(val_generator))

# # Save your model
# model.save(saved_model_path)
# print("Trained and saved new model.")


# Now, for classification (in the same file or another):

class Classifier(models.Model):
    image = models.ImageField(upload_to='images')
    result = models.CharField(max_length=250, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return 'Image classified at {}'.format(self.date_uploaded.strftime('%Y-%m-%d %H:%M'))
    
    def save(self, *args, **kwargs):
        try:
            # SSL certificate necessary so we can download weights of the InceptionResNetV2 model
            ssl._create_default_https_context = ssl._create_unverified_context

            img = Image.open(self.image)
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            dimensions = (299, 299)

            # Interpolation - a method of constructing new data points within the range
            # of a discrete set of known data points.
            resized_image = cv2.resize(img_array, dimensions, interpolation=cv2.INTER_AREA)
            ready_image = np.expand_dims(resized_image, axis=0)
            # ready_image = tf.keras.applications.inception_resnet_v2.preprocess_input(ready_image)

            # Load your own custom model
            custom_model = tf.keras.models.load_model('././../Model1')

            prediction = custom_model.predict(ready_image)
            labels = ['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot', 'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelon','unknown']


           
            top_n_classes = 1
            top_n_indices = np.argsort(prediction, axis=1)[0, -top_n_classes:][::-1]
            top_n_labels = [labels[index] for index in top_n_indices]
            decoded = ', '.join(top_n_labels)
            
            self.result = str(decoded)
            print('Success')
        except Exception as e:
            print('Classification failed:', e)

        return super().save(*args, **kwargs)
