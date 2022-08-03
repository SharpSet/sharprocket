import os
import pathlib

from sharprocket.constants import DRIVE, OUTPUT_FOLDER
from sharprocket.tasks import pdf, place


def main():
    """
    Main Function
    """

    pathlib.Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)

    for file in os.listdir(DRIVE):
        if file.endswith(".pdf"):
            pdf_file = f"{DRIVE}/{file}"

            print("=" * 60)
            print(f"Getting PDF Pages for {file}")
            print("=" * 60)
            page_files = pdf.get_pages(pdf_file)

            place.place_images(page_files, file)

    print("\nFINISHED\n")


if __name__ == "__main__":
    main()
