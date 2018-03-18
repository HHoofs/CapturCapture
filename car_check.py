from PIL import Image

from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np

import os

LABEL = ['racer', 'sports_car', 'cab', 'limousine', 'minivan', 'car_wheel', 'tow_truck', 'car_mirror',
         'pickup', 'trailer_truck', 'jeep', 'convertible', 'minibus', 'school_bus', 'ambulance',
         'passenger_car', 'streetcar']

model = VGG16(weights='imagenet')


def preprocess(img):
    """
    preprocess image in order to make it VGG16 compatible

    :param img: PIL image
    :return: numpy array
    """
    # resize to VGG16 dimensions
    x = img.resize((224,224))
    # make array
    x = image.img_to_array(x)
    # add dimension
    x = np.expand_dims(x, axis=0)

    return preprocess_input(x)


def predict_vgg_16(x):
    """
    predict probs for image

    :param x: array of image
    :return: predictions for all classes
    """
    # predict with the use of the VGG16-model
    preds = model.predict(x)

    return decode_predictions(preds, top=1000)[0]


def check_if_car(preds):
    """
    check if any indication that there is a car on the image

    :param preds: list of list with ref, label, and prop
    :return: True if indication that car
    """
    for _, label, prop in preds:
        if any(label == lab for lab in LABEL):
            if prop > .1:
                print(label)
                return True


# def if_car_save(img, preds):
#     """"""
#     if check_if_car(preds):
#         return True


def main():
    while True:
        all_pics = os.listdir("screens")
        # all_pics = ['screens/' + pic for pic in all_pics]
        print(all_pics)
        for pic in all_pics:
            print(pic)
            with Image.open(os.path.join('screens', pic)) as img_resized:
                img_preprocces = preprocess(img_resized)
                img_predict = predict_vgg_16(img_preprocces)
                if check_if_car(img_predict):
                    print('hoi')
                    # os.rename(os.path.join('screens', pic), os.path.join('/Users/HuCa/Dropbox/cars', pic))
                else:
                    print('hoi')
                    # os.remove(os.path.join('screens', pic))


if __name__ == '__main__':
    main()
