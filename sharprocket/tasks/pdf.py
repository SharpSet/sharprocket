from pdf2image import convert_from_path
import shutil
import os

def get_pages(file):
    loc = "./sharprocket/temp/pages"
    shutil.rmtree(f"{loc}/")
    os.makedirs(loc)

    pages = convert_from_path(file, 500)

    i = 0
    files = []
    for page in pages:
        file = f'{loc}/out{i}.jpg'
        files.append(file)
        page.save(file, 'JPEG')
        i += 1

    return files
