import re
import urllib.request
import urllib.error

def get_images(text_file):
    f = open(text_file, "r", encoding="utf8")
    text = f.read()

    found = re.findall("##(.*?)##", text, re.DOTALL)

    tags = []
    for tag in found:
        tag = tag.replace(" ", "")
        tags.append(tag.lower())

    file_names = download(tags)

    return file_names

def download(tags):
    file_names = []

    for tag in tags:

        if problem_in_tag(tag):
            test_tags = []

            for i, char in enumerate(tag):
                if char in ["0", "o", "O"]:
                    combos = make_combos(tag, char, i)
                    test_tags += combos

            for tag in test_tags:
                url = f"https://files.mcaq.me/{tag}.png"
                successful = download_one(url, tag)

                if successful:
                    loc = f"./sharprocket/temp/images/{tag}.png"
                    file_names.append(loc)

        else:
            url = f"https://files.mcaq.me/{tag}.png"
            download_one(url, tag)

            loc = f"./sharprocket/temp/images/{tag}.png"
            file_names.append(loc)

    return file_names


def download_one(url, tag):
    loc = f"./sharprocket/temp/images/{tag}.png"

    try:
        pngfile = urllib.request.urlopen(url)
        with open(loc,'wb') as output:
            output.write(pngfile.read())
        return True

    except urllib.error.HTTPError:
        return False


def make_combos(tag, char, i):
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


