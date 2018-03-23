import ctypes
import json
import os


def classify_background(images, category=None):
    """
    annotation of desktop wallpaper
    * 0: false
    * 1: positve
    * 2: close
    * 3: other

    :param images: list of all images
    :param category: dict of images and class
    :return: dict of images and class
    """
    # if no dict provided make one from images list
    if category is None:
        category = dict.fromkeys(images)
    # loop over all images
    for image in allImages:
        # only if no label is present
        if category[image] is None:
            print(image)
            # change wallpaper
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
            # ask for input
            label = input("category: ")
            # if s stop
            if label == 's':
                return category
            # assign label to image
            category[image] = label
    return category


def dict_to_json(dict, file='data.json'):
    """
    save dict as json

    :param dict: dict with images and labels
    :param file: location of file
    :return:
    """
    with open(file, 'w') as fp:
        json.dump(dict, fp)


def json_to_dict(file='data.json'):
    """
    load json as dict

    :param file: location of file
    :return:
    """
    with open(file, 'r') as fp:
        data = json.load(fp)
        return data


if __name__ == '__main__':
    # select all images
    allImages = os.listdir('C:/Users/huubh/Dropbox/cars/')
    # append directory
    allImages = ['C:/Users/huubh/Dropbox/cars/' + image for image in allImages]
    # get json to dict
    category_dict = json_to_dict()

    #  annot8
    classifications = classify_background(allImages, category=category_dict)
    # save dict as json
    dict_to_json(classifications)


