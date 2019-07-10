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
# OUTPUT: Overwrite original image
# DESCRIPTION: Filter image.
def pre_process(ImagePath):
    file_list = docMan.get_file_list(ImagePath)
    try:
        file_list.remove('Image.jpg')
    except:
        print('Stack does not exist')

    for i, file_ in enumerate(file_list):
        if i+1 == 10:
            break
        image_path_in_folder = ImagePath +'/'+file_

        print(image_path_in_folder)
        print('Pre_processing ',file_,'....')
        Image.MAX_IMAGE_PIXELS = None #remove pixel limit for the Image library
        dst = cv2.imread(image_path_in_folder)
        dst = cv2.fastNlMeansDenoisingColored(dst, None, 10, 10, 7, 21)
        dst = cv2.resize(dst, (9900, 7500), interpolation=cv2.INTER_AREA) #resizes standard letter sized images to 9900x7500
        dst = cv2.blur(dst, (5, 5)) # averages pixel values to remove disrencrepancy
        dst = cv2.GaussianBlur(dst, (5, 5), 0)
        dst = cv2.medianBlur(dst, 3) #removes salt and pepper by replacing pixles with median value
        dst = cv2.bilateralFilter(dst, 9, 75, 75) #removes noise while keeping sharp edges
        cv2.imwrite(image_path_in_folder, dst)

   # list_im = ['Test1.jpg', 'Test2.jpg', 'Test3.jpg']
  #  imgs = [Image.open(ImagePath +'/'+file_) for file_ in file_list]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
   # min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    # for a vertical stacking it is simple: use vstack
    #imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
    #imgs_comb = Image.fromarray(imgs_comb)
    #imgs_comb.save(ImagePath+'/Image.jpg')

    return ImagePath
