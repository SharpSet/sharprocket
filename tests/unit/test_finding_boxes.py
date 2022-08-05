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
                Box(259, 1558, 1524, 1081),
                Box(1835, 1560, 1886, 1079),
                Box(473, 3256, 1218, 1049),
                Box(1874, 3244, 1809, 1088),
            ],
        ),
        ("out2.jpg", [Box(376, 1942, 2997, 1405), Box(382, 2469, 1338, 884)]),
        ("out3.jpg", [Box(324, 678, 2338, 1232)]),
        (
            "out4.jpg",
            [
                Box(602, 827, 2540, 827),
                Box(625, 1969, 2388, 761),
                Box(1679, 3121, 1422, 927),
            ],
        ),
        ("out5.jpg", [Box(458, 421, 2409, 916)]),
        ("out6.jpg", [Box(598, 683, 2544, 793)]),
        ("out7.jpg", [Box(542, 704, 2577, 963), Box(530, 2367, 2579, 983)]),
        ("out8.jpg", [Box(223, 883, 1344, 895), Box(1788, 868, 1555, 913)]),
        ("out9.jpg", [Box(518, 1128, 2772, 1409), Box(340, 2803, 3120, 852)]),
        ("out10.jpg", [Box(594, 686, 2354, 1116), Box(1410, 4233, 1963, 798)]),
        (
            "out11.jpg",
            [
                Box(654, 696, 2481, 961),
                Box(630, 2254, 2602, 973),
                Box(1179, 4081, 2392, 961),
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

    for box, boxt in zip(boxes, test_boxes):
        box = box.x, box.y, box.w, box.h
        boxt = boxt.x, boxt.y, boxt.w, boxt.h
        for x, y in zip(box, boxt):
            assert abs(x - y) < ACCEPTABLE_DIFF, f"failed on {file} {boxes}"
