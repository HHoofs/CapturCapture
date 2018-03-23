import os
from random import shuffle
from shutil import copyfile


def FullTrain(loc_actual="C:/Users/huubh/Dropbox/cars", loc_destination="C:/Users/huubh/Dropbox/CapturCapture/FullTrain"):
    pos_cars_actual_loc = os.path.join(loc_actual,"1")
    pos_cars_actual = os.listdir(pos_cars_actual_loc)
    pos_cars_actual = [os.path.join(pos_cars_actual_loc, image) for image in pos_cars_actual]

    pos = pos_cars_actual

    for i in range(10):
        for file in pos:
            filename, extension = os.path.splitext(os.path.basename(file))
            copyfile(file, os.path.join(loc_destination, "Captur", filename, "CC_", i, extension))

    neg_cars_actual_loc = os.path.join(loc_actual,"2")
    neg_cars_actual = os.listdir(neg_cars_actual_loc)
    neg_cars_actual = [os.path.join(neg_cars_actual_loc, image) for image in neg_cars_actual]

    neg = neg_cars_actual

    shuffle(neg)

    for file in neg[0:(len(pos)*10)]:
        filename, extension = os.path.splitext(os.path.basename(file))
        copyfile(file, os.path.join(loc_destination, "All", filename, extension))


def PreTrain(loc_actual="C:/Users/huubh/Dropbox/cars", loc_context="C/Users/huubh/Dropbox/autoscout",
             loc_destination="C:/Users/huubh/Dropbox/CapturCapture/Pretrain"):
    pos_cars_actual_loc = os.path.join(loc_actual,"1")
    pos_cars_actual = os.listdir(pos_cars_actual_loc)
    pos_cars_actual = [os.path.join(pos_cars_actual_loc, image) for image in pos_cars_actual]

    pos_cars_context_loc = os.path.join(loc_context,"1")
    pos_cars_context = os.listdir(pos_cars_context_loc)
    pos_cars_context = [os.path.join(pos_cars_context_loc, image) for image in pos_cars_context]

    pos = pos_cars_actual + pos_cars_context

    for i in range(10):
        for file in pos:
            filename, extension = os.path.splitext(os.path.basename(file))
            copyfile(file, os.path.join(loc_destination, "Captur", filename, "CC_", i, extension))

    neg_cars_actual_loc = os.path.join(loc_actual,"2")
    neg_cars_actual = os.listdir(neg_cars_actual_loc)
    neg_cars_actual = [os.path.join(neg_cars_actual_loc, image) for image in neg_cars_actual]

    neg_cars_context_loc = os.path.join(loc_context,"2")
    neg_cars_context = os.listdir(neg_cars_context_loc)
    neg_cars_context = [os.path.join(neg_cars_context_loc, image) for image in neg_cars_context]

    neg = neg_cars_actual + neg_cars_context

    shuffle(neg)

    for file in neg[0:(len(pos)*10)]:
        filename, extension = os.path.splitext(os.path.basename(file))
        copyfile(file, os.path.join(loc_destination, "All", filename, extension))

if __name__ == '__main__':
    FullTrain()
    PreTrain()