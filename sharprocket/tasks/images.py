import urllib.request
import urllib.error

from sharprocket.constants import IMAGES_FOLDER


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

        else:
            print("ERROR")
            print("==================")
            print(f"Could not download {tag}")
            exit()

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
