from PIL import Image
import pyscreenshot as ImageGrab
import time
import os

def aim():
    time.sleep(2)
    im = ImageGrab.grab(bbox=(700,250,1200,750)) # X1,Y1,X2,Y2
    im.show()


def grap_screen():
    im = ImageGrab.grab(bbox=(700,250,1200,750)) # X1,Y1,X2,Y2
    im = im.convert("RGB")
    return im

def resize_image(img):
    # im = img.resize((224,244))
    im = img.resize((224,224))
    return im


def grap_n(n):
    for i in range(n):
        img = grap_screen()
        img = resize_image(img)
        img.save('screens/cap_{0}.jpeg'.format(i))

def grapping(counter = 1):
    count = counter
    while True:
        if len(os.listdir('screens')) < 1000:
            print(count)
            img = grap_screen()
            img = resize_image(img)
            img.save('screens/cap_{0}.jpeg'.format(count))
            count += 1
        else:
            time.sleep(60)


if __name__ == '__main__':
    time.sleep(10)
    grapping(12743)
    # aim()
