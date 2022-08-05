import pytest
from sharprocket.tasks import images
from sharprocket.classes import Box


@pytest.mark.parametrize("tag", ["h8kb0"])
def test_download_one(tag):
    assert images.download_one(tag) is not False


@pytest.mark.parametrize(
    "fake_tag, real_tag, image_boxes",
    [
        ("fff", "h8kb0", [Box(1, 1, 1, 1, 1)]),
    ],
)
def test_download(monkeypatch, fake_tag, real_tag, image_boxes):

    monkeypatch.setattr("builtins.input", lambda _: real_tag)
    assert images.download([fake_tag], image_boxes) is not False
