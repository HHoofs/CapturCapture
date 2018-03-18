import annot8
import os

def sort_to_directories():
    """
    copy images according to their label
    :return:
    """
    # get dict with a label for each image
    classifcation_dict = annot8.json_to_dict()
    # loop of images and their labels
    for item, key in classifcation_dict.items():
        # check if image exists
        if os.path.isfile(item):
            # move image
            os.rename(item, os.path.join(os.path.dirname(item), key, os.path.basename(item)))

if __name__ == '__main__':
    sort_to_directories()
