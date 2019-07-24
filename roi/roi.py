import cv2 as cv
import numpy as np
import random as rng

def dilate_to_text_line(edges, N, iterations):
    kernel = np.ones((1, N), np.uint8)
    dilated_image = cv.dilate(edges, kernel, iterations=iterations) #TODO figure out if which morphological transformation is better: dilate or closing
    cv.imwrite(r'\dilations\output_iteration-'+str(iterations)+'.jpg', dilated_image) #TODO: change path
    closing_image = cv.morphologyEx(dilated_image, cv.MORPH_CLOSE, kernel)
    cv.imwrite(r'\dilations\closing_output_iteration-'+str(iterations)+'.jpg', closing_image) #TODO: change path
    return closing_image

def dilate_to_text_block(edges, N, iterations):
    kernel = np.ones((N, N), np.uint8)
    dilated_image = cv.dilate(edges, kernel, iterations=iterations) #TODO figure out if which morphological transformation is better: dilate or closing
    cv.imwrite(r'\dilations\output_iteration-'+str(iterations)+'.jpg', dilated_image) #TODO: change path
    closing_image = cv.morphologyEx(dilated_image, cv.MORPH_CLOSE, kernel)
    cv.imwrite(r'\dilations\closing_output_iteration-'+str(iterations)+'.jpg', closing_image) #TODO: change path
    return closing_image

def contours_to_text_block(canny_edges):
    filtered_contours = []
    filtered_contours_properties = []

    # initial dilation
    dilated_image = dilate_to_text_block(canny_edges, N=6, iterations=1) # dilate just enough to capture words
    contours, hierarchy = cv.findContours(dilated_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour_properties = get_contour_properties(contours, dilated_image)

    i = 0
    for c in contour_properties:
        #and hierarchy[0, i, 3] == -1
        if 10000 < c['size'] < 1000000: #if contour too small or contour is fucking massive (ie border of page or box)
            filtered_contours.append(contours.__getitem__(i))
            filtered_contours_properties.append(c)
        i += 1

    return filtered_contours, filtered_contours_properties

def contours_to_text_line(canny_edges):
    filtered_contours = []
    filtered_contours_properties = []

    # initial dilation
    dilated_image = dilate_to_text_line(canny_edges, N=6, iterations=1) # dilate just enough to capture words
    contours, hierarchy = cv.findContours(dilated_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour_properties = get_contour_properties(contours, dilated_image)

    i = 0
    for c in contour_properties:
        if 200 < c['size'] < 1000000 and c['height'] < 300: #if contour too small or contour is fucking massive (ie border of page or box)
            filtered_contours.append(contours.__getitem__(i))
            filtered_contours_properties.append(c)
        i += 1

    return filtered_contours, filtered_contours_properties

def get_contour_properties(contours, edges):
    contour_properties = []
    for c in contours:
        x,y,w,h = cv.boundingRect(c)
        contour_image = np.zeros(edges.shape)
        cv.drawContours(contour_image, [c], 0, 255, -1)
        contour_properties.append({
            'left': x,
            'bottom': y,
            'right': x + w - 1,
            'top': y + h - 1,
            'size': w*h,
            'height': h
        })
    return contour_properties

def output_contours(contours):
    # Approximate contours to polygons and get bounding rectangles
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)

    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])

    contour_shape = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

    # Draw polygonal bounding rectangles
    for i in range(len(contours)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv.rectangle(contour_shape, (int(boundRect[i][0]), int(boundRect[i][1])), \
                     (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)
        cv.imwrite(r'contours.jpg', contour_shape)  #TODO: change path

def nearest_neighbor(contour_properties, contour_list): #TODO: Jake -  to develop

    clustered_contours = []

    for current_contour in contour_properties:
        left = current_contour['left']
        right = crop['right']
        top = current_contour['top']
        bottom = current_contour['bottom']
        height = current_contour['height']

        i = 0
        for rect_properties in contour_properties:
            # calculate adjacent distances
            dist_left = left - current_contour['right']
            dist_right = right - current_contour['left']
            dist_above = top - current_contour['bottom']
            dist_below = bottom - current_contour['top']
            distance = min(dist_left, dist_above, dist_below, dist_right)

            # calculate percent distance in height
            perc_height_difference = abs(height / current_contour['height'] - 1)

            if perc_height_difference <= .2 and distance > closest_distance:  # if similar height and closest in distance so far
                closest_distance = distance
                best_neighbor_properties = rect_properties
                best_neighbor_idx = i

            i += 1

    return clustered_contours

# MAIN #TODO: Refactor and integrate into main

#import image
img = cv.imread('test1.jpg',0)  #TODO: change path

#resize
img = cv.resize(img, (1350, 1150)) #TODO: investigate at implementation

# Threshold
threshold = 200
# Detect edges using Canny
canny_output = cv.Canny(img, threshold, threshold*2)


# Find text blob or line contours through dilation and filter to find lines of text
text_block_list, text_block_properties = contours_to_text_block(canny_output)
text_line_list, text_line_properties = contours_to_text_line(canny_output)

# output contour lines to jpg in folder
output_contours(text_block_list)

# cluster similar contours to create blocks of text  #TODO: Jake - nearest neighbor clustering
#clustered_text_line = nearest_neighbor(text_line_properties, text_line_list) # return clustered text lines

# crop contours and output to folder
i=0
for crop in text_block_properties:
    cropped_image = img[crop['bottom']:crop['top'], crop['left']:crop['right']]
    cv.imwrite(r'\crops\crop'+str(i)+'.jpg', cropped_image) #TODO: change path
    i+= 1
