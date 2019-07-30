import cv2 as cv
import numpy as np
import random as rng
import math
import copy

def dilate_to_text_line(edges, N, iterations, write_path):
    kernel = np.ones((1, N), np.uint8)
    dilated_image = cv.dilate(edges, kernel, iterations=iterations) #TODO figure out if which morphological transformation is better: dilate or closing
    cv.imwrite(write_path+'/dilation/dilation-output_iteration-line'+str(iterations)+'.jpg', dilated_image)
    closing_image = cv.morphologyEx(dilated_image, cv.MORPH_CLOSE, kernel)
    cv.imwrite(write_path+'/dilation/closing_output_iteration-line'+str(iterations)+'.jpg', closing_image)
    return closing_image

def dilate_to_text_block(edges, N, iterations, write_path):
    kernel = np.ones((N, N), np.uint8)
    dilated_image = cv.dilate(edges, kernel, iterations=iterations) #TODO figure out if which morphological transformation is better: dilate or closing
    cv.imwrite(write_path+'/dilation/dilation-output_iteration-block'+str(iterations)+'.jpg', dilated_image)
    closing_image = cv.morphologyEx(dilated_image, cv.MORPH_CLOSE, kernel)
    cv.imwrite(write_path+'/dilation/closing_output_block'+str(iterations)+'.jpg', closing_image)
    return closing_image

def contours_to_text_block(canny_edges, write_path):
    filtered_contours = []
    filtered_contours_properties = []

    # initial dilation
    dilated_image = dilate_to_text_block(canny_edges, 25, 1, write_path) # dilate just enough to capture words
    contours, hierarchy = cv.findContours(dilated_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour_properties = get_contour_properties(contours, dilated_image)
   # count = len(contours)

    # while count > 30:
    #     dilated_image = dilate_to_text_block(dilated_image, 20, 1, write_path)  # dilate just enough to capture words
    #     contours, hierarchy = cv.findContours(dilated_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #     count = len(contours)

    i = 0
    for c in contour_properties:
        if 2000 < c['size'] < 100000000 and (c['top']-c['bottom'])/(c['right']-c['left']) < 12: #if contour too small or contour is fucking massive (ie border of page or box)
            filtered_contours.append(contours.__getitem__(i))
            filtered_contours_properties.append(c)
        i += 1

    return filtered_contours, filtered_contours_properties

def contours_to_text_line(canny_edges, write_path):
    filtered_contours = []
    filtered_contours_properties = []

    # initial dilation
    dilated_image = dilate_to_text_line(canny_edges, 25, 1, write_path) # dilate just enough to capture words
    contours, hierarchy = cv.findContours(dilated_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #
    # count = len(contours)

    # while count > 400:
    #     dilated_image = dilate_to_text_line(dilated_image, 12, 1, write_path)  # dilate just enough to capture words
    #     contours, hierarchy = cv.findContours(dilated_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #     contour_properties = get_contour_properties(contours, dilated_image)
    #     count = len(contours)

    contour_properties = get_contour_properties(contours, dilated_image)

    i = 0
    for c in contour_properties:
        if 500 < c['size'] < 100000000 and (c['top']-c['bottom'])/(c['right']-c['left']) < 12 and c['height'] > 3: #if contour too small or contour is fucking massive (ie border of page or box)
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

def output_contours( contours, canny_output, write_path, method_type):
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
        cv.imwrite(write_path+'/contour/'+ method_type +'block.jpg', contour_shape)


def print_cluster(contours_properties, canny_output, write_path):

    contour_shape = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

    # Draw polygonal bounding rectangles
    for current_contour in contours_properties:
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv.rectangle(contour_shape, (int(current_contour['left']), int(current_contour['bottom'])), \
                     (int((current_contour['right'])), int(current_contour['top'])), color, 2)
        cv.imwrite(write_path+'/contour'+'/cluster.jpg', contour_shape)



def normalize_contour_properties(contour_properties):
    normalized_contour_properties = copy.deepcopy(contour_properties)

    # Find Min/Max values of each column
    top_min = min(normalized_contour_properties,key = lambda x:x['top'])['top']
    top_max = max(normalized_contour_properties,key = lambda x:x['top'])['top']
    bottom_min = min(normalized_contour_properties, key=lambda x: x['bottom'])['bottom']
    bottom_max = max(normalized_contour_properties, key=lambda x: x['bottom'])['bottom']
    left_min = min(normalized_contour_properties, key=lambda x: x['left'])['left']
    left_max = max(normalized_contour_properties, key=lambda x: x['left'])['left']
    right_min = min(normalized_contour_properties, key=lambda x: x['right'])['right']
    right_max = max(normalized_contour_properties, key=lambda x: x['right'])['right']
    height_min = min(normalized_contour_properties, key=lambda x: x['height'])['height']
    height_max = max(normalized_contour_properties, key=lambda x: x['height'])['height']
    size_min = min(normalized_contour_properties, key=lambda x: x['size'])['size']
    size_max = max(normalized_contour_properties, key=lambda x: x['size'])['size']


    # Set all values relative to linear scale 0-1
    for current_contour in normalized_contour_properties:
        current_contour['top'] = float(current_contour['top']-top_min)/float(top_max-top_min)
        current_contour['bottom'] = float(current_contour['bottom']-bottom_min)/float(bottom_max-bottom_min)
        current_contour['left'] = float(current_contour['left']-left_min)/float(left_max-left_min)
        current_contour['right'] = float(current_contour['right']-right_min)/float(right_max-right_min)
        current_contour['height'] = float(current_contour['height']-height_min)/float(height_max-height_min)
        current_contour['size'] = float(current_contour['size']-size_min)/float(size_max-size_min)

    return normalized_contour_properties


def contour_euclidean_distance(contour_properties):

    # Define number of contours
    contour_num = len(contour_properties)
    # Normalize contour_properties
    contour_properties_normalized = normalize_contour_properties(contour_properties)
    # Define array for distance in similarity of each contour to every other contour
    euclidean_dist = [[0 for i in range(contour_num)] for j in range(contour_num)]
    # Define array iterators
    row = 0

    # calculate distance matrix
    for current_contour in contour_properties_normalized:
        column = 0
        for compare_contour in contour_properties_normalized:
            # calculate the difference in each feature
            top_diff = round(math.pow(abs(compare_contour['top'] - current_contour['top']),2), 3)
            bottom_diff = round(math.pow(abs(compare_contour['bottom'] - current_contour['bottom']),2), 3)
            left_diff = round(math.pow(abs(compare_contour['left'] - current_contour['left']),2), 3)
            right_diff = round(math.pow(abs(compare_contour['right'] - current_contour['right']),2), 3)
            size_diff = round(math.pow(abs(compare_contour['size'] - current_contour['size']),2), 3)
            height_diff = round(math.pow(abs(compare_contour['height'] - current_contour['height']),2), 3) # height difference

            # Sum all values
            diff_sum = math.fsum([top_diff,bottom_diff,left_diff,right_diff,4*height_diff,size_diff])#
            #diff_sum = math.fsum([top_diff,bottom_diff,4*left_diff,4*right_diff,height_diff])# ,size_diff])#

            #squareroot
            euclidean_dist[row][column] = round(math.sqrt(diff_sum), 3)

            column +=1
        row +=1

    euclidean_dist = np.asarray(euclidean_dist) # convert to numpy array
    np.fill_diagonal(euclidean_dist, np.inf) # fill diagonals with infinity to symbolize the contour being compared

    return euclidean_dist

def combine_contours(contour_properties1, contour_properties2, contour_properties):
    contour_properties_master = copy.deepcopy(contour_properties)
    combined_contour = copy.deepcopy(contour_properties1)

    combined_contour['left'] = min(contour_properties1['left'], contour_properties2['left'])
    combined_contour['right'] = max(contour_properties1['right'], contour_properties2['right'])
    combined_contour['top'] = max(contour_properties1['top'], contour_properties2['top'])
    combined_contour['bottom'] = min(contour_properties1['bottom'], contour_properties2['bottom'])
    combined_contour['size'] = (combined_contour['right'] - combined_contour['left'])*(combined_contour['top'] - combined_contour['bottom'])
    combined_contour['height'] = (contour_properties1['height'] + contour_properties2['height'])/2

    # delete contour1
    for i in range(len(contour_properties_master)):
        if(contour_properties_master[i] == contour_properties1):
            del contour_properties_master[i]
            break
    # delete contour2
    for i in range(len(contour_properties_master)):
        if(contour_properties_master[i] == contour_properties2):
            del contour_properties_master[i]
            break

    # add in combined_contour
    contour_properties_master.append(combined_contour)

    return contour_properties_master


def nearest_neighbor(contour_properties, canny_output):
    # Define new clustered_contours array
    clustered_contours = list(contour_properties)

    # Threshold for when to stop merging clusters
    DISTANCE_THRESHOLD = .9

    # Define matrix of euclidean distances between all clusters
    distance_matrix = contour_euclidean_distance(clustered_contours)

    [row, column] = np.unravel_index(distance_matrix.argmin(), distance_matrix.shape)  # return index of shortest distance in matrix

    while distance_matrix[row, column] < DISTANCE_THRESHOLD:
        clustered_contours = combine_contours(clustered_contours[row], clustered_contours[column], clustered_contours) # combine most similar
        distance_matrix = contour_euclidean_distance(clustered_contours) # Recalculate most similar
        [row, column] = np.unravel_index(distance_matrix.argmin(), distance_matrix.shape)  # return index of shortest distance in matrix

    return clustered_contours

# MAIN #TODO: Refactor and integrate into main
def roi_main(path, write_path):
    #import image
    img = cv.imread(path,0)
    print('Write_Path: '+str(write_path))
    #resize
    #img = cv.resize(img, (1350, 1150)) #TODO: investigate at implementation should the pixels be read and scaled acordingly?

    # Threshold
    threshold = 200

    # Detect edges using Canny
    canny_output = cv.Canny(img, threshold, threshold*2)

    # Find text blob or line contours through dilation and filter to find lines of text
    print("making contours...") 
    text_block_list, text_block_properties = contours_to_text_block(canny_output, write_path)
    text_line_list, text_line_properties = contours_to_text_line(canny_output, write_path)

    output_contours(text_block_list, canny_output, write_path, 'dilation-to-block')
    output_contours(text_line_list, canny_output, write_path,'dilation-to-line')

    # cluster similar contours to create blocks of text
    print("clustering...")
    clustered_text_properties = nearest_neighbor(text_line_properties, canny_output) # return clustered text lines

    # output contour lines to jpg in folder
    print_cluster(clustered_text_properties, canny_output, write_path)

    print("cropping...")
    # crop contours and output to folder
    i=0

    for crop in clustered_text_properties:
        cropped_image = img[crop['bottom']:crop['top'], crop['left']:crop['right']]
        cv.imwrite(write_path+'/crop/'+str(i)+'.jpg', cropped_image)
        i+= 1

    for crop in text_block_properties:
        cropped_image = img[crop['bottom']:crop['top'], crop['left']:crop['right']]
        cv.imwrite(write_path+'/crop/'+'textblock'+str(i)+'.jpg', cropped_image)
        i+= 1