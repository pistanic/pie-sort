#################################################################
#                                                               #
# Copyright 2019 All rights reserved.                           #
# Author: Siddharth Verma                                       #
# Co-Authors: Nicholas Forest                                   #
#                                                               #
#################################################################

# Preprocessing functions to prepare pdf for ocr/nlp

import cv2
from PIL import Image
import docMan
import numpy as np

# INPUT: Path of Image Folder
# OUTPUT: Overwrite original image
# DESCRIPTION: Resize the image.
def resize(ImagePath):
    file_list = docMan.get_file_list(ImagePath)
    try:
        file_list.remove('Image.jpg')
    except:
        print('Stack does not exist')

    file_list.sort()
    file_list.sort(key=len)

    for i, file_ in enumerate(file_list):
        image_path_in_folder = ImagePath +'/'+file_
        print('Pre_processing debug - resize: ',file_,'....')
        dst = cv2.imread(image_path_in_folder)
        dst = cv2.resize(dst, (5100, 6600), interpolation=cv2.INTER_AREA) #resizes standard letter sized images to 5100x6600
        dst = cv2.blur(dst, (5, 5)) # averages pixel values to remove disrencrepancy
        cv2.imwrite(image_path_in_folder, dst)

    return ImagePath

# INPUT: Path of Image Folder
# OUTPUT: Overwrite original image
# DESCRIPTION: Filter the image.
def filtering(ImagePath):
    file_list = docMan.get_file_list(ImagePath)
    try:
        file_list.remove('Image.jpg')
    except:
        print('Stack does not exist')

    file_list.sort()
    file_list.sort(key=len)

    return ImagePath
        # scratch work from resize
        # if i+1 == 10:
        #     break
        #print(image_path_in_folder)
        #Image.MAX_IMAGE_PIXELS = None #remove pixel limit for the Image library
        #dst = cv2.fastNlMeansDenoisingColored(dst, None, 10, 10, 7, 21)
        #dst = cv2.GaussianBlur(dst, (5, 5), 0)
        #dst = cv2.medianBlur(dst, 3) #removes salt and pepper by replacing pixles with median value
        #dst = cv2.bilateralFilter(dst, 9, 75, 75) #removes noise while keeping sharp edges


        #list_im = ['Test1.jpg', 'Test2.jpg', 'Test3.jpg']
        #imgs = [Image.open(ImagePath +'/'+file_) for file_ in file_list]
        #pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        #min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
        #for a vertical stacking it is simple: use vstack
        #imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
        #imgs_comb = Image.fromarray(imgs_comb)
        #imgs_comb.save(ImagePath+'/Image.jpg')
