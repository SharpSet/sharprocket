import os
import shutil

from pdf2image import convert_from_path
from sharprocket.constants import OUTPUT_FOLDER, PAGES_FOLDER


def get_pages(file):
    """
    Converts PDF to pages

    returns: list of page filenames
    """

    # Delete old pages
    shutil.rmtree(f"{PAGES_FOLDER}/")
    os.makedirs(PAGES_FOLDER)

    pages = convert_from_path(file, 500)

    files = []

    for i, page in enumerate(pages):
        file = f'{PAGES_FOLDER}/out{i}.jpg'
        files.append(file)
        page.save(file, 'JPEG')

    return files

