from sharprocket.tasks import images, pdf, place
from sharprocket.constants import DRIVE

def main():
    file1 = f"{DRIVE}/images.pdf"
    file2 = f"{DRIVE}/text.txt"

    print("Getting PDF Pages")
    page_files = pdf.get_pages(file1)

    # page_files = []
    # loc = "./sharprocket/temp/pages"
    # for i in [0, 1, 2]:
    #     page_files.append(f'{loc}/out{i}.jpg')

    print("Getting Images")
    img_files = images.get_images(file2)


    print("Placing Images")
    place.place_images(img_files, page_files)

    print("\nFINISHED\n")

if __name__ == "__main__":
    main()