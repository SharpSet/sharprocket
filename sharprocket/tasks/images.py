import re
import urllib.request
import urllib.error
import os
import shutil

from sharprocket.constants import IMAGES_FOLDER


def get_images(text_file):
    """
    Downloads all images

    returns: List of image filenames
    """
    shutil.rmtree(f"{IMAGES_FOLDER}/")
    os.makedirs(IMAGES_FOLDER)

    # Opens text file and finds letters in ##
    f = open(text_file, "r", encoding="utf8")
    text = f.read()
    found = re.findall("##(.*?)##", text, re.DOTALL)

    ## Removes all spaces
    tags = []
    for tag in found:
        tag = tag.replace(" ", "")
        tags.append(tag.lower())

    file_names = download(tags)

    return file_names

def download(tags):
    """
    Downloads all images with tags from files.mcaq.me
    """

    domain = "files.mcaq.me"

    file_names = []

    for tag in tags:

        # Issues with 0, o and O not being regonized
        # This code creates every possible combination to find
        # Which one is correct.
        # Has a low chance of finding something already in use
        if problem_in_tag(tag):
            test_tags = []

            for i, char in enumerate(tag):
                if char in ["0", "o", "O"]:
                    combos = make_combos(tag, char, i)
                    test_tags += combos

            for tag in test_tags:
                url = f"https://{domain}/{tag}.png"
                successful = download_one(url, tag)

                if successful:
                    loc = f"./{IMAGES_FOLDER}/{tag}.png"
                    file_names.append(loc)

        else:
            # If there isn't the problem just download
            url = f"https://{domain}/{tag}.png"
            download_one(url, tag)

            loc = f"./{IMAGES_FOLDER}/{tag}.png"
            file_names.append(loc)

    return file_names


def download_one(url, tag):
    """
    Download specified tag
    """

    loc = f"./{IMAGES_FOLDER}/{tag}.png"

    try:
        pngfile = urllib.request.urlopen(url)
        with open(loc,'wb') as output:
            output.write(pngfile.read())
        return True

    except urllib.error.HTTPError:
        return False


def make_combos(tag, char, i):
    """
    Makes all combinations of letters
    """

    types = ["0", "o", "O"]
    combos = [tag]
    types.remove(char)

    for _type in types:
        temp = list(tag)
        temp[i] = _type

        combos.append(''.join(temp))

    return combos


def problem_in_tag(tag):
    if "0" in tag or "o" in tag or "O" in tag:
        return True


