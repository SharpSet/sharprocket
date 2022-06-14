import re
import urllib.request
import urllib.error
import os
import shutil
from itertools import product

from sharprocket.constants import IMAGES_FOLDER, TAG_SIZE

problem_sets = [
    ["6", "k"]
]


def get_images(text_file):
    """
    Downloads all images

    returns: List of image filenames
    """
    shutil.rmtree(f"{IMAGES_FOLDER}/")
    os.makedirs(IMAGES_FOLDER)

    # Opens text file and finds letters in ##
    f = open(text_file, "r", encoding="utf8")
    text = f.read().replace(" ", "").replace("\n", "").replace("*", "")
    found = re.findall("[4#]([^#]{" + str(TAG_SIZE) + "})[4#]", text, re.DOTALL)

    print(found)
    ## Removes all spaces
    tags = []
    for tag in found:
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

        # Issues with letters not used by storage system
        tag = tag.replace("s", "5")
        tag = tag.replace("z", "2")
        tag = tag.replace("o", "0")
        tag = tag.replace("i", "1")

        # Issues with 7 and 2 not being regonized
        # This code creates every possible combination to find
        # Which one is correct.
        # Has a low chance of finding something already in use
        tag_problem_sets = problem_in_tag(tag)
        if tag_problem_sets:
            tag_combos = make_combos(tag, tag_problem_sets)

            for tag in tag_combos:
                url = f"https://{domain}/{tag}.png"
                successful = download_one(url, tag)

                if successful:
                    loc = f"./{IMAGES_FOLDER}/{tag}.png"
                    file_names.append(loc)

        else:
            # If there isn't the problem just download
            url = f"https://{domain}/{tag}.png"
            successful = download_one(url, tag)

            if successful:

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


def make_combos(tag, tag_problem_sets):
    """
    Creates all possibilities of a tag

    https://stackoverflow.com/questions/52382444/replace-combinations-of-characters

    https://en.wikipedia.org/wiki/Cartesian_product
    """

    combos = []

    # Convert input string into a list so we can easily substitute letters
    seq = list(tag)

    # Find indices of key letters in seq
    indices = [ i for i, c in enumerate(seq) if c in tag_problem_sets ]

    # Generate key letter combinations & place them into the list
    for t in product(tag_problem_sets, repeat=len(indices)):
        for i, c in zip(indices, t):
            seq[i] = c
        combos.append(''.join(seq))

    return combos


def problem_in_tag(tag):
    """
    Detects if any of the problem characters are in the tag
    """

    tag_problem_sets = []

    for char in tag:
        for problem_set in problem_sets:
            if char in problem_set:
                tag_problem_sets += problem_set

    return list(set(tag_problem_sets))


