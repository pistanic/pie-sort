import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


def extract_text(im):
    # returns text from image
    text = pytesseract.image_to_string(Image.open(im))
    return text