import cv2
from sharprocket.constants import (
    BLUE,
    GREEN,
    RECTANGLE_THICKNESS,
    RED,
    TEXT_OFFSET,
    TEXT_SIZE,
    TEXT_THICKNESS,
    USER_VIEWING_FOLDER,
)


def get_images(page_file, image_boxes):
    """
    Downloads all images

    returns: List of image filenames
    """

    codes = []

    # create new image for cv2
    image = cv2.imread(page_file)

    for box in image_boxes:
        place_data(image, box)

    loc = f"{USER_VIEWING_FOLDER}/user.jpg"
    cv2.imwrite(loc, image)

    print(f"Please open: {loc}")

    for box in image_boxes:
        text = input(f"Enter a code for {box.id}: ")
        codes.append(text.lower())

    return codes


def place_data(image, box):
    cv2.rectangle(
        image, (box.x, box.y), (box.xf, box.yf), GREEN, RECTANGLE_THICKNESS
    )

    # get coords of rect center
    text_coords = (box.x + TEXT_OFFSET, box.y + TEXT_OFFSET)
    image = cv2.putText(
        image,
        box.id,
        text_coords,
        cv2.FONT_HERSHEY_SIMPLEX,
        TEXT_SIZE,
        BLUE,
        TEXT_THICKNESS,
        cv2.LINE_AA,
    )

    small_box = box.scale(downscale=True)

    # draw a smaller box inside the bigger box
    cv2.rectangle(
        image,
        (small_box.x, small_box.y),
        (small_box.xf, small_box.yf),
        RED,
        RECTANGLE_THICKNESS,
    )
