from typing import List

import cv2
from sharprocket.classes import Box
from sharprocket.constants import (
    GRAY_THRESHOLD,
    MAX_BOX_OVERLAP,
    MAXIMUM_BOX_RATIO,
    MINIMUM_BOX_SIZE,
)


def scan(page_file):
    """
    Scans the page files and returns a list of boxes.
    """

    image_boxes = []

    # Create threshold to find rectangles
    image = cv2.imread(page_file)
    image_boxes = find_boxes(image)
    final_boxes = remove_problem_boxes(image_boxes)

    return final_boxes


def remove_problem_boxes(image_boxes: List[Box]):
    """
    Removes boxes that are too small or too close to each other.
    """

    problem_boxes = []

    # Compare each box to one another
    for boxa in image_boxes:
        for boxb in image_boxes:
            # Check if any of the boxes corners are a similar distance
            # from each other
            if compare_overlap(boxa, boxb):
                boxes = [boxa, boxb]
                problem_boxes.append(boxes)

    for boxa, boxb in problem_boxes:

        # which ever box is smaller gets removed
        # from image_boxes
        if boxa.w > boxb.w and boxb in image_boxes:
            image_boxes.remove(boxb)
            print("Removed Box:", boxb)
        elif boxb.w < boxa.w and boxa in image_boxes:
            image_boxes.remove(boxa)
            print("Removed Box:", boxa)

    return image_boxes


def compare_overlap(boxa, boxb):
    """
    Compares two boxes and how much they overlap.
    Returns true if they share more than MAX_BOX_OVERLAP pixels.
    """

    if boxa == boxb:
        return False

    dx = min(boxa.xf, boxb.xf) - max(boxa.x, boxb.x)
    dy = min(boxa.yf, boxb.yf) - max(boxa.y, boxb.y)

    if (dx >= MAX_BOX_OVERLAP) and (dy >= MAX_BOX_OVERLAP):
        print(f"Box Overlap for {boxa} and {boxb}: {dx * dy}px^2")
        return dx * dy

    return False


def find_boxes(image):
    """
    Finds the boxes in the image.
    """

    image_boxes = []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, GRAY_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.bitwise_not(thresh)

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    image_boxes = []
    for c in cnts:

        # Finds all shapes that are virtually empty
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        box = Box(*cv2.boundingRect(approx))

        minimum_area = MINIMUM_BOX_SIZE
        if box.area < minimum_area:
            continue

        small_box = box.scale(downscale=True)

        total_white = cv2.countNonZero(
            thresh[small_box.y : small_box.yf, small_box.x : small_box.xf]
        )
        ratio = total_white / float(box.area)

        empty = ratio < MAXIMUM_BOX_RATIO

        if empty:
            print(f"Box Found: Ratio: {round(ratio, 6)} Box: {box}")

            large_box = box.scale()
            image_boxes.append(large_box)

    image_boxes.sort(key=lambda test_box: -distance_from_origin(test_box), reverse=True)

    return image_boxes


def distance_from_origin(box):
    """
    Calculates the distance between a box and the origin.
    """

    box_origin = Box(0, 0, 0, 0)

    return ((box.x - box_origin.x) ** 2 + (box.y - box_origin.y) ** 2) ** 0.5
