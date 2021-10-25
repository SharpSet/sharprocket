import cv2
import numpy as np
from PIL import Image

def place_images(img_files, page_files):

    image_i = 0

    for page_no, page_file in enumerate(page_files):
        image = cv2.imread(page_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        t = 220
        thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.bitwise_not(thresh)

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        image_boxes = []
        for c in cnts:
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

        image_boxes = reversed(image_boxes)
        # Places image
        for file_no, image_box in enumerate(image_boxes):
            file_name = img_files[image_i]
            image_i += 1

            img = Image.open(file_name, 'r')
            x, y, w, h = image_box

            img = img.resize((w, h), Image.ANTIALIAS)

            if file_no == 0:
                background = Image.open(page_file, 'r')

            else:
                background = Image.open(f'./sharprocket/temp/output/out{page_no}.png', 'r')
            background.paste(img, (x, y))
            background.save(f'./sharprocket/temp/output/out{page_no}.png')


