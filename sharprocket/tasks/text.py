import urllib.request
import urllib.error

from sharprocket.constants import IMAGES_FOLDER


def get_images(page_file, no_of_codes):
    """
    Downloads all images

    returns: List of image filenames
    """

    codes = []

    print(f"Please open {page_file}")

    for _ in range(no_of_codes):
        text = input("Enter a code: ")

        codes.append(text)

    return download(codes)


def download(tags):
    """
    Downloads all images with tags from files.mcaq.me
    """

    domain = "files.mcaq.me"
    file_names = []

    for tag in tags:
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
        with open(loc, "wb") as output:
            output.write(pngfile.read())
        return True

    except urllib.error.HTTPError:
        return False
