from sharprocket.tasks import images, pdf, place

def main():
    file1 = "./sharprocket/drive/images.pdf"
    file2 = "./sharprocket/drive/text.txt"

    # page_files = pdf.get_pages(file1)

    page_files = []
    loc = "./sharprocket/temp/pages"
    for i in [0, 1, 2]:
        page_files.append(f'{loc}/out{i}.jpg')

    img_files = images.get_images(file2)

    place.place_images(img_files, page_files)

if __name__ == "__main__":
    main()