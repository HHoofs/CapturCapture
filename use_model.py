from keras.models import load_model
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input
import numpy as np
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator

IMG_WIDTH, IMG_HEIGHT = 299, 299


def preprocess(img):
    """
    preprocess image in order to make it VGG16 compatible

    :param img: PIL image
    :return: numpy array
    """
    # resize to VGG16 dimensions
    x = img.resize((299,299))
    # make array
    x = image.img_to_array(x)
    x = x / 255.
    # add dimension
    x = np.expand_dims(x, axis=0)

    return x




if __name__ == '__main__':
    model = load_model('logs/CapturCapture.h5')

    # prepare data augmentation configuration
    preds_datagen = ImageDataGenerator(rescale=1. / 255)

    # Build generator for the train set
    preds_generator = preds_datagen.flow_from_directory(
        'preds', target_size=(IMG_HEIGHT, IMG_WIDTH), batch_size=1, shuffle=False)

    aa = model.predict_generator(preds_generator)
    np.round(aa, 2)

    with Image.open('preds/All/cap_1088.jpeg') as img:
        x = preprocess(img)
        print(model.predict(x))

