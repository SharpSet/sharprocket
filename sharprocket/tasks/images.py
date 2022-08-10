import urllib.error
import urllib.request

import cv2
from sharprocket.constants import (
    BLUE,
    GREEN,
    IMAGES_FOLDER,
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

    tags = []

    # create new image for cv2
    image = cv2.imread(page_file)

    for box in image_boxes:
        place_data(image, box)

    loc = f"{USER_VIEWING_FOLDER}/user.jpg"
    cv2.imwrite(loc, image)

    print(f"\nPlease open: {loc}\n")

    for box in image_boxes:
        text = input(f"Enter a code for [ {box.id} ]: ")
        tags.append(text.lower())

    return download(tags, image_boxes)


def place_data(image, box):
    """
    Places rectangles and Box ID's into image for the user
    """

    cv2.rectangle(image, (box.x, box.y), (box.xf, box.yf), GREEN, RECTANGLE_THICKNESS)

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

    # draw a smaller box inside the bigger box
    # This matches what the code is doing to detect empty boxes
    small_box = box.scale(downscale=True)
    cv2.rectangle(
        image,
        (small_box.x, small_box.y),
        (small_box.xf, small_box.yf),
        RED,
        RECTANGLE_THICKNESS,
    )


def download(tags, image_boxes):
    """
    Downloads all images with tags from files.mcaq.me
    """

    file_names = []

    for tag, box in zip(tags, image_boxes):

        successful = download_one(tag)

        if successful:
            file_names.append(successful)

        else:
            # If it is not accepted,
            # give the user one more time to correct the problem

            tag = input(f"Tag failed for {box.id}, try again: ")
            successful = download_one(tag.lower())
            if successful:
                file_names.append(successful)
            else:
                print(f"Failed to download {box.id}")
                exit(1)

    return file_names


def download_one(tag):
    """
    Download specified tag
    """

    domain = "files.mcaq.me"

    extensions = [".jpg", ".png"]

    for extension in extensions:
        loc = f"./{IMAGES_FOLDER}/{tag}{extension}"
        url = f"https://{domain}/{tag}{extension}"

        try:
            pngfile = urllib.request.urlopen(url)
            with open(loc, "wb") as output:
                output.write(pngfile.read())
            return loc

        # We want to pass here to allow for all extensions to be tried
        except urllib.error.HTTPError:
            pass

    return False
