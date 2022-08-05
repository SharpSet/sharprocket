import pytest
from sharprocket.classes import Box
from sharprocket.tasks.boxes import (
    compare_overlap,
    remove_problem_boxes,
    distance_from_origin,
)


@pytest.mark.parametrize(
    "boxa, boxb, expected",
    [
        (Box(0, 0, 50, 50), Box(0, 0, 100, 100), 2500),
        (Box(0, 10, 75, 75), Box(25, 35, 100, 100), 2500),
        (Box(376, 1942, 2940, 1348), Box(382, 2469, 1313, 859), 1077973),
    ],
)
def test_overlapping(boxa, boxb, expected):
    assert compare_overlap(boxa, boxb) == expected


@pytest.mark.parametrize(
    "image_boxes, final_boxes",
    [
        [
            [
                Box(382, 2469, 1313, 859),
                Box(376, 1942, 2940, 1348),
            ],
            [Box(376, 1942, 2940, 1348)],
        ]
    ],
)
def test_remove_problem_boxes(image_boxes, final_boxes):
    assert remove_problem_boxes(image_boxes) == final_boxes


@pytest.mark.parametrize(
    "box, expected",
    [
        (Box(0, 0, 50, 50), 0),
        (Box(0, 10, 75, 75), 10),
    ],
)
def test_distance_from_origin(box, expected):
    assert distance_from_origin(box) == expected, f"Failed on {box}"
