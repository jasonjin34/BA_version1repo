import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

'''generate edge function '''
def cannyEdge(src,  min):
    #src = cv.cvtColor(src, cv.COLOR_RGB2GRAY)
    dst = cv.Canny(src, min, min*3, apertureSize=3)
    #dst = cv.dilate(dst, None)
    return dst

'''function use to divide the image into 6 sub images'''
def image_divider(image, row, coloum):
    '''save the divide image in the images list'''
    images = []
    image_row_size = int(len(image)/row)
    image_colum_size = int(len(image[0])/coloum)
    for index_row in range(row):
        for index_column in range(coloum):
            image_divide_temp = image[index_row*image_row_size:(index_row + 1)*image_row_size].copy()
            image_divide = []
            for index in range(len(image_divide_temp)):
                image_divide.append(image_divide_temp[index][index_column*image_colum_size:(index_column + 1)*image_colum_size ])
            images.append(image_divide)
    return images

def findEffectivePoints():
    image = cv.imread('drivesample.png', 1)
    '''resize the image'''
    image = cv.resize(image, (1350, 900))
    # show the orign image
    originimage = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = cannyEdge(image, 100)
    ret, image_invert = cv.threshold(image, 120, 255, cv.THRESH_BINARY_INV)
    height, width = image.shape
    print('height: ' + str(height) + ' width: ' + str(width))

    '''detect line by using HoughLine functions'''
    Lines = cv.HoughLinesP(image, 1,  np.pi/180, 80, maxLineGap=10, minLineLength=80)

    # Create a black image
    featureLine = np.zeros((height, width, 3), np.uint8)

    image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    filter_lines_point = [[], [], []]
    for line in Lines:
        x1, y1, x2, y2 = line[0]
        if y1 != 450 and y2 != 450 and y1 > 20 and y2 > 20: # delete the edge line
            if np.sqrt(np.power((x1-x2), 2) + np.power((y1 - y2), 2)) > 150:
                cv.line(featureLine, (x1, y1), (x2, y2), (0, 255, 0), 1)
                factes = 1
                if factes == 1:
                    if x1 <= 900 and x1 >= 450 and y1 < 450 and y2 < 450 and x2 <= 900 and x2 >= 450:  # filter for the factes
                        # pre process the data transfer from size 450 to the norminated edge size 20
                        x1 = 20.0 * (x1 - (450.0 + 900.0) / 2.0) / 450.0
                        x2 = 20.0 * (x2 - (450.0 + 900.0) / 2.0) / 450.0
                        y1 = 20.0 * (y1 - 450.0 / 2.0) / 450.0
                        y2 = 20.0 * (y2 - 450.0 / 2.0) / 450.0
                        print(x1, x2, y1, y2)
                        filter_lines_point[0].append(x1)
                        filter_lines_point[1].append(-10)
                        filter_lines_point[2].append(y1)
                        filter_lines_point[0].append(x2)
                        filter_lines_point[1].append(-10)
                        filter_lines_point[2].append(y2)
                if factes == 2:
                    if x1 <= 1350 and x1 >= 900 and y1 < 450 and y2 < 450 and x2 <= 1350 and x2 >= 900:  # filter for the factes
                        # pre process the data transfer from size 450 to the norminated edge size 20
                        x1 = 20.0 * (x1 - (1350.0 + 900.0) / 2.0) / 450.0
                        x2 = 20.0 * (x2 - (1350.0 + 900.0) / 2.0) / 450.0
                        y1 = 20.0 * (y1 - 450.0 / 2.0) / 450.0
                        y2 = 20.0 * (y2 - 450.0 / 2.0) / 450.0
                        print(x1, x2, y1, y2)
                        filter_lines_point[0].append(10)
                        filter_lines_point[1].append(x1)
                        filter_lines_point[2].append(y1)
                        filter_lines_point[0].append(10)
                        filter_lines_point[1].append(x2)
                        filter_lines_point[2].append(y2)

    cv.imshow('original edge image', featureLine)

    pixel_num = 0
    for height_index in range(height):
        for width_index in range(width):
            if height_index % 5 != 0 and width_index % 5 != 0:
                featureLine[height_index][width_index][0] = 0
                featureLine[height_index][width_index][1] = 0
                featureLine[height_index][width_index][2] = 0

    featureLine = cv.cvtColor(featureLine, cv.COLOR_BGR2GRAY)
    #cv.imshow('edge.png', featureLine)

    count = 0
    for height_index in range(height):
        for width_index in range(width):
            if featureLine[height_index][width_index] != 0:
                count = count + 1
    print('total number of the feature image ' + str(count))
    return filter_lines_point
