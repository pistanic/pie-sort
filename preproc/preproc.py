# Preprocessing functions to prepare pdf for ocr/nlp

import cv2
#import pytesseract
from PIL import Image

# INPUT: Path of Image
# RETURN: Overwrite original image
def pre_process(ImagePath):

    Image.MAX_IMAGE_PIXELS = None
    dst = cv2.imread(ImagePath)
    dst = cv2.fastNlMeansDenoisingColored(dst, None, 10, 10, 7, 21)
    dst = cv2.resize(dst, (9900, 7500), interpolation=cv2.INTER_AREA)
    dst = cv2.blur(dst, (5, 5))
    dst = cv2.GaussianBlur(dst, (5, 5), 0)
    dst = cv2.medianBlur(dst, 3)
    dst = cv2.bilateralFilter(dst, 9, 75, 75)
    cv2.imwrite(ImagePath, dst)
