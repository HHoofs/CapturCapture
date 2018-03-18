from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K

# https://github.com/aleksas/keras-fine-tune-inception/blob/master/fine_tune_inceptionv3.py

img_width, img_height = 299, 299
batch_size = 4

# create the base pre-trained model
base_model = InceptionV3(weights='imagenet', include_top=False)

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(3, activation='softmax')(x)


# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    height_shift_range=.05, width_shift_range=.05,
    horizontal_flip=False)

train_generator = train_datagen.flow_from_directory(
    'C:/Users/huubh/Dropbox/cars/',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

# train the model on the new data for a few epochs
model.fit_generator(train_generator, steps_per_epoch = (231 + 7 + 632) // batch_size, epochs=5)
