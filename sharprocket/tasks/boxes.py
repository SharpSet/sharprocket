import cv2
from sharprocket.constants import (
    GRAY_THRESHOLD,
    MAX_BOX_OVERLAP,
    MAXIMUM_BOX_RATIO,
    MINIMUM_BOX_SIZE,
    SCALING_FACTOR,
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


def remove_problem_boxes(image_boxes):
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

        a_width = boxa[2]
        b_width = boxb[2]

        # which ever box is smaller gets removed
        # from image_boxes
        if a_width > b_width and boxb in image_boxes:
            image_boxes.remove(boxb)
            print("Removed Box:", boxb)
        elif b_width < a_width and boxa in image_boxes:
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

    x, y, w, h = boxa
    a_max = (x + w, y + h)
    a_min = (x, y)

    x, y, w, h = boxb

    b_max = (x + w, y + h)
    b_min = (x, y)

    dx = min(a_max[0], b_max[0]) - max(a_min[0], b_min[0])
    dy = min(a_max[1], b_max[1]) - max(a_min[1], b_min[1])

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
        x, y, w, h = cv2.boundingRect(approx)

        minimum_area = MINIMUM_BOX_SIZE
        if w * h < minimum_area:
            continue

        factor = scale_factor(w, h)

        total_white = cv2.countNonZero(
            thresh[y + factor : y + h - factor, x + factor : x + w - factor]
        )
        ratio = total_white / float(w * h)

        empty = ratio < MAXIMUM_BOX_RATIO

        if empty:
            print(f"Box Found: Ratio: {ratio} Area: {w*h} Location: {x, y}")
            image_boxes.append([x - factor, y - factor, w + factor, h + factor])

    return image_boxes


def scale_factor(w, h):
    """
    Creates a scaling factor for the box.
    """

    factor = int(w / SCALING_FACTOR) if w > h else int(h / SCALING_FACTOR)
    return factor
