from PIL import Image
from sharprocket.constants import COMPRESSION_MULTIPLIER, OUTPUT_FOLDER
from sharprocket.tasks import boxes, images


def place_images(page_files, pdf_file):
    """
    Pastes all images into pages
    """

    output_images = []

    # For each page
    for page_no, page_file in enumerate(page_files):

        print("\nStarting on page:", page_no)

        image_boxes = boxes.scan(page_file)

        img_files = images.get_images(page_file, image_boxes)

        if len(img_files) != len(img_files):
            print("Error: Number of images and boxes don't match")
            return

        # Opens file ready for pasting
        background = Image.open(page_file, "r")
        bw, bh = background.size

        # Places image
        for image, box in zip(img_files, image_boxes):

            img = Image.open(image, "r")

            img = img.resize((box.w, box.h), Image.ANTIALIAS)

            background.paste(img, (box.x, box.y))

        # Resizes image to fit box
        background = background.resize(
            (bw // COMPRESSION_MULTIPLIER, bh // COMPRESSION_MULTIPLIER),
            Image.ANTIALIAS,
        )
        output_images.append(background)
        print(f"\nSaved Page {page_no}\n")

    im1 = output_images.pop(0)

    im1.save(
        f"{OUTPUT_FOLDER}/{pdf_file}",
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=output_images,
    )
