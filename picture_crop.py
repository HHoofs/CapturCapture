import time
import os

import pyscreenshot as ImageGrab


def aim():
    """
    function to test aim of screengrab

    :return:
    """
    # provide time to get right image
    time.sleep(2)
    im = ImageGrab.grab(bbox=(700,250,1200,750)) # X1,Y1,X2,Y2
    im.show()


def grap_screen():
    """
    Grab screen (on the right place)

    :return: image
    """
    im = ImageGrab.grab(bbox=(700,250,1200,750)) # X1,Y1,X2,Y2
    return im


def resize_image(img):
    """
    resize image to 299x299 (Inception

    :param img: image from ImageGrab
    :return: image
    """

    im = img.resize((299,299))
    return im


def grapping(counter = 1):
    """
    grap the screen and store image (untill more then 1000 images in directory)

    :param counter: start number to identify images
    :return:
    """
    # assing count
    count = counter
    while True:
        # if more than 1000 wait
        if len(os.listdir('screens')) < 1000:
            # grap screen
            img = grap_screen()
            # resize image to 299x299 (inception)
            img = resize_image(img)
            # save image
            img.save('screens/cap_{0}.jpeg'.format(count))
            # add one to the counter
            count += 1
        else:
            time.sleep(60)


if __name__ == '__main__':
    grapping(1001)
