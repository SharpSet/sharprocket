from sharprocket.tasks import images, pdf, place
from sharprocket.constants import DRIVE, TXT, OUTPUT_FOLDER
import os
import pathlib


def main():
    pathlib.Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

    for file in os.listdir(DRIVE):
        if file.endswith(".pdf"):
            pdf_file = f"{DRIVE}/{file}"
            txt_file2 = f"{DRIVE}/{file} Transcription.{TXT}".replace(".pdf", "")

            print(f"Getting PDF Pages for {file}")
            page_files = pdf.get_pages(pdf_file)

            # page_files = []
            # loc = "./sharprocket/temp/pages"
            # for i in [0, 1, 2]:
            #     page_files.append(f'{loc}/out{i}.jpg')

            print("Getting Images")
            img_files = images.get_images(txt_file2)


            print("Placing Images")
            place.place_images(img_files, page_files, file)

            print("\nFINISHED\n")

if __name__ == "__main__":
    main()