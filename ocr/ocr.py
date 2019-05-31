# Simple Example for geting started with tesseract. 
# Adapted from the example provided here: https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/

# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os

def simple_ocr(filepath):
# load the example image and convert it to grayscale
	image = cv2.imread(filepath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)
# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	return text
