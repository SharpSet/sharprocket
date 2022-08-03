import os

import cv2
from sharprocket.tasks.boxes import find_boxes
from sharprocket.constants import TESTING_PAGES_FOLDER

from tests.unit.data import BOXES


ACCEPTABLE_DIFF = 10


def in_range(boxes, boxes_data):
    if len(boxes) != len(boxes_data):
        return False

    for box, data in zip(boxes, boxes_data):
        for x, y in zip(box, data):
            if x - y > ACCEPTABLE_DIFF:
                return False

    return True


def test_find_boxes():
    # get all files in dir ./tests/pages
    for file in os.listdir(TESTING_PAGES_FOLDER):
        # read image
        img = cv2.imread("./tests/pages/" + file)
        # find boxes
        boxes = find_boxes(img)

        print("Working on file: " + file)
        assert in_range(boxes, BOXES[file])
