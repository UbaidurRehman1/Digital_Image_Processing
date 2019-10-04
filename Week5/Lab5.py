import cv2
import numpy as np

"""
@:return three images RGB, GRAYSCALE and BINARY        
"""
def get_images(path):
    rgb = cv2.imread(path)
    gray_scale = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    (thresh, binary) = cv2.threshold(gray_scale, 127, 255, cv2.THRESH_BINARY)
    print(path, " is converted to ndArray")
    return rgb, gray_scale, binary


'''
    @:param a value between 0 to 255
    @:return return a value negative to it using a formal L-1-r
'''
def get_negative_value(value):
    return 256 - 1 - value


"""
    @:param np nd_array
"""
def show_negative(array):
    cv2.imshow("original", array)
    shape = array.shape
    negative = np.empty(shape, dtype=np.uint8, order='C')
    row_counter = 0
    column_counter = 0
    pixel_counter = 0
    for row in array:
        column_counter = 0
        for column in row:
            if isinstance(column, np.uint8):
                if column_counter == 0 and row_counter == 0:
                    print(column_counter)
                    print("Ths image is gray scale")
                negative[row_counter][column_counter] = get_negative_value(column)
            elif isinstance(column, np.ndarray):
                if column_counter == 0 and row_counter == 0:
                    print("The image is in RGB")
                pixel_counter = 0
                for pixel in column:
                    negative[row_counter][column_counter][pixel_counter] = get_negative_value(pixel)
                    pixel_counter = pixel_counter + 1
            column_counter = column_counter + 1
        row_counter = row_counter + 1
    assert array is not None
    cv2.imshow("negative", negative)
    key = cv2.waitKey(0)


'''
    @:param numpy nd_array
    show the edges of an image
'''
def show_edges(gray_scale):
    array = gray_scale
    shape = array.shape
    edge_detector = np.empty(shape, dtype=np.uint8, order='C')
    row_index = 0
    column_index = 0
    cv2.imshow("Original", array)
    for row in array:
        column_index = 0
        for column in row:
            if column_index == 511:
                continue
            try:
                edge_detector[row_index][column_index] = array[row_index][column_index + 1] - column + 126
            except IndexError:
                print('index error')
            finally:
                column_index = column_index + 1
        row_index = row_index + 1
    cv2.imshow('Edge detection', edge_detector)
    cv2.waitKey(0)


"""
    @:param nd array 
    show the 8 bits of an image
"""
def bit_plane(dollar):
    array = dollar
    plane_list = []
    for i in range(0, 8):
        plane_list.append(np.empty(array.shape, dtype=np.uint8, order='C'))
    row_index = 0
    column_index = 0
    plane_index = 0
    for row in array:
        column_index = 0
        for column in row:
            bit = '{0:08b}'.format(column)
            plane_index = 0
            for np_array in plane_list:
                pixel_ = bit[plane_index]
                if pixel_ == '1':
                    pixel_ = 255
                else:
                    pixel_ = 0
                np_array[row_index][column_index] = pixel_
                plane_index = plane_index + 1
            column_index = column_index + 1
        row_index = row_index + 1
    for list1 in plane_list:
        cv2.imshow('image', list1)
        cv2.waitKey(0)


def main():
    rgb, gray_scale, binary = get_images("lena.jpg")
    show_negative(rgb)
    show_negative(gray_scale)
    show_negative(binary)
    show_edges(gray_scale)
    rgb, gray_scale, binary = get_images("dollar.jpg")
    bit_plane(gray_scale)


main()
