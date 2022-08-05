import os
import shutil

import cv2
from sharprocket.constants import (
    TESTING_FOLDER,
    TESTING_PAGES_FOLDER,
)

from sharprocket.tasks.boxes import find_boxes, remove_problem_boxes

from sharprocket.tasks.images import place_data


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

        for box in final_boxes:
            print(f"Placed Box {box} on page {page_no}")
            place_data(image, box)

        # save file
        loc = f"{TESTING_FOLDER}/page{page_no}.jpg"
        cv2.imwrite(loc, image)

        input(f"Press Enter to continue after checking tests... \n{loc}\n")


if __name__ == "__main__":
    test_e2e()
