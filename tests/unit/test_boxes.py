from sharprocket.tasks.boxes import scale_factor, compare_overlap, remove_problem_boxes

from tests.unit.data import PROBLEM_BOXES


def test_overlapping():
    tests = [
        ([0, 0, 50, 50], [0, 0, 100, 100], 2500),
        ([0, 10, 75, 75], [25, 35, 100, 100], 2500),
        ([376, 1942, 2940, 1348], [382, 2469, 1313, 859], 1077973),
    ]

    for boxa, boxb, expected in tests:
        assert compare_overlap(boxa, boxb) == expected


def test_scale_factor():
    tests = [(50, 50, 1), (100, 100, 2), (250, 250, 5)]

    for w, h, expected in tests:
        assert scale_factor(w, h) == expected


def test_remove_problem_boxes():
    for image_boxes, final_boxes in PROBLEM_BOXES:
        assert remove_problem_boxes(image_boxes) == final_boxes
