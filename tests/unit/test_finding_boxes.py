import pytest

import cv2
from sharprocket.tasks.boxes import find_boxes
from sharprocket.classes import Box


ACCEPTABLE_DIFF = 80


@pytest.mark.parametrize(
    "file, test_boxes",
    [
        ("out1.jpg", [Box(454, 691, 2954, 1513)]),
        (
            "out0.jpg",
            [
                Box(473, 3256, 1195, 1026),
                Box(1874, 3244, 1775, 1054),
                Box(259, 1558, 1495, 1052),
                Box(1835, 1560, 1850, 1043),
            ],
        ),
        ("out2.jpg", [Box(382, 2469, 1313, 859), Box(376, 1942, 2940, 1348)]),
        ("out3.jpg", [Box(324, 678, 2338, 1232)]),
        (
            "out4.jpg",
            [
                Box(1679, 3121, 1395, 900),
                Box(625, 1969, 2388, 761),
                Box(602, 827, 2492, 779),
            ],
        ),
        ("out5.jpg", [Box(458, 421, 2409, 916)]),
        ("out6.jpg", [Box(598, 683, 2544, 793)]),
        ("out7.jpg", [Box(530, 2367, 2530, 934), Box(542, 704, 2528, 914)]),
        ("out8.jpg", [Box(223, 883, 1344, 895), Box(1788, 868, 1555, 913)]),
        ("out9.jpg", [Box(340, 2803, 3060, 792), Box(518, 1128, 2719, 1356)]),
        ("out10.jpg", [Box(1410, 4233, 1926, 761), Box(594, 686, 2309, 1071)]),
        (
            "out11.jpg",
            [
                Box(1179, 4081, 2346, 915),
                Box(630, 2254, 2552, 923),
                Box(654, 696, 2434, 914),
            ],
        ),
        ("out12.jpg", [Box(572, 1673, 2467, 779)]),
    ],
)
def test_find_boxes(file, test_boxes):
    # read image
    img = cv2.imread("./tests/pages/" + file)
    # find boxes
    boxes = find_boxes(img)

    print("Working on file: " + file)

    for box, boxt in zip(boxes, test_boxes):
        print(boxes)
        box = box.x, box.y, box.w, box.h
        boxt = boxt.x, boxt.y, boxt.w, boxt.h
        for x, y in zip(box, boxt):
            assert abs(x - y) < ACCEPTABLE_DIFF
