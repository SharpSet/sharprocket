from cv2 import cv2
import numpy as np
from PIL import Image
import os
import shutil

from sharprocket.constants import OUTPUT_FOLDER, COMPRESSION_MULTIPLIER

def place_images(img_files, page_files, pdf_file):
    """
    Pastes all images into pages
    """

    image_i = 0
    output_images = []

    # For each page
    for page_no, page_file in enumerate(page_files):

        # Create threshold to find rectangles
        image = cv2.imread(page_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        t = 220
        thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.bitwise_not(thresh)

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        image_boxes = []
        for c in cnts:

            # Finds all shapes that are virtually empty
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.015 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            total_white = cv2.countNonZero(thresh[y:y+h,x:x+w])
            ratio = total_white / float(w*h)

            empty = ratio < 0.1

            if empty:
                cv2.rectangle(image,(x,y),(x+w,y+h),(36,255,12),20)
                image_boxes.append([x, y, w, h])

        # cv2.imshow('thresh', cv2.resize(thresh, (400, 600)))
        # cv2.imshow('image', cv2.resize(image, (400, 600)))
        # cv2.waitKey()

        # Puts images in correct order
        image_boxes = reversed(image_boxes)

        # Opens file ready for pasting
        background = Image.open(page_file, 'r')
        bw, bh = background.size

        # Places image
        for image_box in image_boxes:

            # Move onto next image
            # Works between pages

            try:
                file_name = img_files[image_i]
                image_i += 1
            except IndexError:
                print("No more images:\n")
                print(img_files)
                print("")
                break

            img = Image.open(file_name, 'r')
            x, y, w, h = image_box

            img = img.resize((w, h), Image.ANTIALIAS)

            background.paste(img, (x, y))

        background = background.resize((bw//COMPRESSION_MULTIPLIER, bh//COMPRESSION_MULTIPLIER), Image.ANTIALIAS)
        output_images.append(background)
        print(f"Saved Page {page_no}")


    print("Making PDF...")
    im1 = output_images.pop(0)

    im1.save(f"{OUTPUT_FOLDER}/{pdf_file}", "PDF", resolution=100.0, save_all=True, append_images=output_images)
