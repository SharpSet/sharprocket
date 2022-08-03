import os

OUTPUT_FOLDER = "./sharprocket/output"
IMAGES_FOLDER = "./sharprocket/temp/images"
PAGES_FOLDER = "./sharprocket/temp/pages"
TESTING_FOLDER = "./tests/e2e_out"
TESTING_PAGES_FOLDER = "./tests/pages"

DRIVE = "./sharprocket/gdrive"

# boxes constants
COMPRESSION_MULTIPLIER = 3
MINIMUM_BOX_SIZE = 200000
SCALING_FACTOR = 50
GRAY_THRESHOLD = 220
MAXIMUM_BOX_RATIO = 0.05
RECTANGLE_THICKNESS = 10
MAX_BOX_OVERLAP = 20

TEXT_SIZE = 2
TEXT_THICKNESS = 5
TEXT_OFFSET = 200

# colours
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)

# Text constants
TAG_SIZE = 5

# read dev from env
DEV = True if os.environ.get("DEV") == "TRUE" else False
