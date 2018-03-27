import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Dense, GlobalAveragePooling2D
from keras.models import Model
from keras import applications, optimizers

# dimensions of our images.
IMG_WIDTH, IMG_HEIGHT = 299, 299


def save_bottlebeck_features(train_dir, train_features_dir, train_samples, batch_size=10):
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the VGG16 network
    model = applications.InceptionV3(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)

    bottleneck_features_train = model.predict_generator(
        generator, train_samples // batch_size)
    np.save(open(train_features_dir, 'wb'),
            bottleneck_features_train)


def train_top_model(train_features_dir, top_model_weights_path, train_samples, epochs, batch_size):
    train_data = np.load(open(train_features_dir, 'rb'))
    # only if balanced
    train_labels = np.array([0] * (train_samples // 2) + [1] * (train_samples // 2))

    #
    model = Sequential()
    # model.add()
    model.add(GlobalAveragePooling2D(input_shape=train_data.shape[1:]))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(.2))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=train_samples // batch_size)
    model.save_weights(top_model_weights_path)


def build_2step_model(top_model_weights_path):
    """
    Build model that is partly based on bottleneck features but with a model on top of that

    :param top_model_weights_path: location of bottleneck features of the model
    :return: Keras.model
    """

    # build the VGG16 network
    base_model = applications.InceptionV3(weights='imagenet', include_top=False, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))
    print('Model loaded.')

    # build a classifier model to put on top of the convolutional model
    top_model = Sequential()
    # model.add()
    top_model.add(GlobalAveragePooling2D(input_shape=base_model.output_shape[1:]))
    top_model.add(Dense(1024, activation='relu'))
    top_model.add(Dropout(.2))
    top_model.add(Dense(1, activation='sigmoid'))

    # note that it is necessary to start with a fully-trained
    # classifier, including the top classifier,
    # in order to successfully do fine-tuning
    top_model.load_weights(top_model_weights_path)

    # add the model on top of the convolutional base
    model = Model(inputs=base_model.input, outputs=top_model(base_model.output))

    return model


def compile_and_train_model(model, train_dir, train_samples, epochs, batch_size):
    """
    Train a Keras.model for a train and validation set and predict a set of images

    :param model: A Keras.model
    :param train_dir: directory in which the train data (images) is found
    :param epochs: number of epochs
    :param batch_size: batch size
    :return: None
    """

    # compile the model with a SGD/momentum optimizer
    # and a very slow learning rate.
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
                  metrics=['accuracy'])

    # prepare data augmentation configuration
    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       width_shift_range=.1,
                                       height_shift_range=.1,
                                       rotation_range=20)


    # Build generator for the train set
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=batch_size,
        class_mode='binary')


    # fine-tune the model
    model.fit_generator(
        train_generator,
        steps_per_epoch=(train_samples) // batch_size,
        epochs=epochs)

    return model


def alternate_trainable_layers(model, from_layer):
    for layer in model.layers[:from_layer]:
        layer.trainable = False
    for layer in model.layers[from_layer:]:
        layer.trainable = True

    return model


if __name__ == '__main__':
    save_bottlebeck_features(train_dir='./PreTrain',
                             train_features_dir='features/bottleneck_features_inceptionv3_train.npy',
                             train_samples=9472, batch_size=16)

    train_top_model(train_features_dir='features/bottleneck_features_inceptionv3_train.npy',
                    top_model_weights_path='features/bottleneck_fc_inceptionv3_model.h5',
                    train_samples=9472, epochs=50, batch_size=16)

    model = build_2step_model(top_model_weights_path='features/bottleneck_fc_inceptionv3_model.h5')

    model = alternate_trainable_layers(model, from_layer=249)
    model = compile_and_train_model(model=model,
                                  train_dir='./PreTrain',
                                  train_samples=9472, epochs=10, batch_size=16)

    model = alternate_trainable_layers(model, from_layer=280)
    _ = compile_and_train_model(model=model,
                                  train_dir='./FullTrain',
                                  train_samples=1408, epochs=10, batch_size=16)
