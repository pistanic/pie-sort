#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: Siddharth Verma                                       #
# Co-Authors:                                                   #
#                                                               #
#################################################################

# Preprocessing functions to prepare pdf for ocr/nlp

import cv2
#import pytesseract
from PIL import Image

# INPUT: Path of Image
# RETURN: Overwrite original image
def pre_process(ImagePath):

    Image.MAX_IMAGE_PIXELS = None                                   #remove pixel limit for the Image library
    dst = cv2.imread(ImagePath)
    dst = cv2.fastNlMeansDenoisingColored(dst, None, 10, 10, 7, 21)
    dst = cv2.resize(dst, (9900, 7500), interpolation=cv2.INTER_AREA)       #resizes standard letter sized images to 9900x7500
    dst = cv2.blur(dst, (5, 5))                                             # averages pixel values to remove disrencrepancy
    dst = cv2.GaussianBlur(dst, (5, 5), 0)
    dst = cv2.medianBlur(dst, 3)                                    #removes salt and pepper by replacing pixles with median value
    dst = cv2.bilateralFilter(dst, 9, 75, 75)                       #removes noise while keeping sharp edges
    cv2.imwrite(ImagePath, dst)
