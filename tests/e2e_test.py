import os
import shutil

import cv2
from sharprocket.constants import (
    BLUE,
    GREEN,
    RECTANGLE_THICKNESS,
    RED,
    TESTING_FOLDER,
    TEXT_OFFSET,
    TEXT_SIZE,
    TEXT_THICKNESS,
    TESTING_PAGES_FOLDER,
)

from sharprocket.tasks.boxes import find_boxes, scale_factor, remove_problem_boxes


def test_e2e():
    image_boxes = []

    # empty TESTING_FOLDER if it exists
    if os.path.exists(TESTING_FOLDER):
        shutil.rmtree(f"{TESTING_FOLDER}/")

    # create TESTING_FOLDER
    os.makedirs(TESTING_FOLDER)

    page_files = os.listdir(TESTING_PAGES_FOLDER)

    for page_no, page_file in enumerate(page_files):

        # Create threshold to find rectangles
        page_file = f"{TESTING_PAGES_FOLDER}/{page_file}"
        image = cv2.imread(page_file)
        image_boxes = find_boxes(image)
        final_boxes = remove_problem_boxes(image_boxes)

        for x, y, w, h in final_boxes:
            box_id = f"{page_no}-{x}-{y}"
            print("Placed Box:", box_id)

            factor = scale_factor(w, h)

            cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, RECTANGLE_THICKNESS)

            # get coords of rect center
            text_coords = (x + TEXT_OFFSET, y + TEXT_OFFSET)
            image = cv2.putText(
                image,
                box_id,
                text_coords,
                cv2.FONT_HERSHEY_SIMPLEX,
                TEXT_SIZE,
                BLUE,
                TEXT_THICKNESS,
                cv2.LINE_AA,
            )

            # draw a smaller box inside the bigger box
            cv2.rectangle(
                image,
                (x + factor, y + factor),
                (x + w - factor, y + h - factor),
                RED,
                RECTANGLE_THICKNESS,
            )

        # save file
        cv2.imwrite(f"{TESTING_FOLDER}/page{page_no}.jpg", image)

        input("Press Enter to continue after checking tests...")


if __name__ == "__main__":
    test_e2e()
