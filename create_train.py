import os
import glob
from random import shuffle
from shutil import copyfile


def FullTrain(loc_actual="C:/Users/huubh/Dropbox/cars", loc_destination="C:/Users/huubh/Dropbox/CapturCapture/FullTrain"):
    pos_cars_actual_loc = os.path.join(loc_actual,"1/*.jpeg")
    pos_cars_actual = glob.glob(pos_cars_actual_loc)

    pos = pos_cars_actual

    for i in range(10):
        for file in pos:
            filename, extension = os.path.splitext(os.path.basename(file))
            copyfile(file, os.path.join(loc_destination, "Captur", "{0}_CC_{1}{2}".format(filename, str(i), extension)))

    neg_cars_actual_loc = os.path.join(loc_actual, "2/*.jpeg")
    neg_cars_actual = glob.glob(neg_cars_actual_loc)

    neg = neg_cars_actual

    shuffle(neg)

    for file in neg[0:(len(pos)*10)]:
        filename, extension = os.path.splitext(os.path.basename(file))
        copyfile(file, os.path.join(loc_destination, "All", "{0}{1}".format(filename, extension)))


def PreTrain(loc_actual="C:/Users/huubh/Dropbox/cars", loc_context="C:/Users/huubh/Dropbox/autoscout",
             loc_destination="C:/Users/huubh/Dropbox/CapturCapture/Pretrain"):
    pos_cars_actual_loc = os.path.join(loc_actual,"1/*.jpeg")
    pos_cars_actual = glob.glob(pos_cars_actual_loc)

    pos_cars_context_loc = os.path.join(loc_context,"1/*.jpg")
    pos_cars_context = glob.glob(pos_cars_context_loc)

    pos = pos_cars_actual + pos_cars_context

    for i in range(10):
        for file in pos:
            filename, extension = os.path.splitext(os.path.basename(file))
            copyfile(file, os.path.join(loc_destination, "Captur", "{0}_CC_{1}{2}".format(filename, str(i), extension)))

    neg_cars_actual_loc = os.path.join(loc_actual, "2/*.jpeg")
    neg_cars_actual = glob.glob(neg_cars_actual_loc)

    neg_cars_context_loc = os.path.join(loc_context,"2/*.jpg")
    neg_cars_context = glob.glob(neg_cars_context_loc)

    neg = neg_cars_actual + neg_cars_context

    shuffle(neg)

    for file in neg[0:(len(pos)*10)]:
        filename, extension = os.path.splitext(os.path.basename(file))
        copyfile(file, os.path.join(loc_destination, "All", "{0}{1}".format(filename, extension)))

if __name__ == '__main__':
    FullTrain()
    # PreTrain()
