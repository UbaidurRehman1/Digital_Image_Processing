import numpy as np
import cv2

"""
    @:param path of the picture
    @:return numpy 2d array of image
"""


def get_image_np_array(path):
    # noinspection PyUnresolvedReferences
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img


"""
    @:arg row_index
    @:arg col_index
"""


class Location:
    def __int__(self, row_, col_):
        self.row = row_
        self.col = col_


# --------------global variables--------------
threshold = 185

# imgProc = Lab3.ImgProcessing()
#
# im_array = imgProc.get_empty_np_array(8, 8)
#
# list_arr = [[1, 1, 0, 1, 1, 1, 0, 1],
#             [1, 1, 0, 1, 0, 1, 0, 1],
#             [1, 1, 1, 1, 0, 0, 0, 1],
#             [0, 0, 0, 0, 0, 0, 0, 1],
#             [1, 1, 1, 1, 0, 1, 0, 1],
#             [0, 0, 0, 1, 0, 1, 0, 1],
#             [1, 1, 1, 1, 0, 0, 0, 1],
#             [1, 1, 1, 1, 0, 1, 1, 1]]
# counter = 0
# for internal_list in list_arr:
#     internal_counter = 0
#     for value in internal_list:
#         im_array[counter][internal_counter] = value
#         internal_counter = internal_counter + 1
#     counter = counter + 1

# def test():
#     img_proc = Lab3.ImgProcessing()
#     im_array = img_proc.get_empty_np_array(8, 8)
#     list_arr = [[1, 1, 0, 1, 1, 1, 0, 1],
#                 [1, 1, 0, 1, 0, 1, 0, 1],
#                 [1, 1, 1, 1, 0, 0, 0, 1],
#                 [0, 0, 0, 0, 0, 0, 0, 1],
#                 [1, 1, 1, 1, 0, 1, 0, 1],
#                 [0, 0, 0, 1, 0, 1, 0, 1],
#                 [1, 1, 1, 1, 0, 0, 0, 1],
#                 [1, 1, 1, 1, 0, 1, 1, 1]]
#     counter = 0
#     for internal_list in list_arr:
#         internal_counter = 0
#         for value in internal_list:
#             im_array[counter][internal_counter] = value
#             internal_counter = internal_counter + 1
#         counter = counter + 1
#     return im_array


"""
    @:param im array of binary image
    @:param location of the pixel
    @:return the top neighborhood of given location or -1 if it not exists or value greater than threshold
"""


def get_top(im, l):
    try:
        _row = l.row
        # if row is zero then there is no top row
        # so whatever value of column we will return -1
        if _row == 0:
            return -1

        _col = l.col
        _top_col = im[_row - 1]
        _val = _top_col[_col]

        # if value is greater than 200 then leave it
        if _val > threshold:
            return -1
        return _val
    except RuntimeError:
        return -1


"""
    @:param im array of binary image
    @:param location of the pixel
    @:return the left neighborhood of given location or -1 if it not exists or value greater than threshold
"""


def get_left(im, l):
    try:

        _col = l.col
        # if column is zero then there is no left column
        # and whatever the value of row we will return -1
        if _col == 0:
            return -1

        _row = im[l.row]

        _left_col_index = l.col - 1

        _val = _row[_left_col_index]

        # if value is greater than 200
        if _val > threshold:
            return -1

        return _val
    except RuntimeError:
        return -1


# adding label in the given location
"""
    @:param location of pixel
    @:param value of intensity
    @:param array of label
"""


def add_label(l, _value, label_array):
    _row = l.row
    _col = l.col
    label_array[_row][_col] = _value


# getting value from the given location
"""
    @:param location of pixel
    @:param label array
    @:return value of pixel from given location
"""


def get_value_from_label_array(l, label_array):
    return label_array[l.row][l.col]


"""
    @:param array
    @:return return the same array but each pixel intensity value is 255
"""


def populate_with_255(arr):
    for row_index in range(arr.shape[0]):
        for col_index in range(arr.shape[1]):
            arr[row_index][col_index] = 255
    return arr


"""
    this is first pass of algorithm  
    @:returns  label array, child->parent dictionary
"""


def pass1():
    # getting binary 2d array of the image
    im_array = get_image_np_array('Lab4-image.png')
    write_image("inter.png", im_array)
    # im_array = test()

    # getting label array of same size
    label_array = np.zeros((im_array.shape[0], im_array.shape[1]), dtype=int)

    # populating label array with 255 value each pixel
    label_array = populate_with_255(label_array)

    # local variables
    loc = Location()
    label_dict = {}
    label_g = 0
    row = 0

    # getting each row from the array
    for external_list in im_array:
        col = 0
        # getting each pixel
        for value in external_list:
            # if value of pixel is greater than threshold (180)  then leave this pixel
            if value > threshold:
                col = col + 1
                continue
            loc.__int__(row, col)

            # getting top and left neighbor of this pixel
            top_neighbor = get_top(im_array, loc)
            left_neighbor = get_left(im_array, loc)

            # if this pixel has no neighbor then creating a label and then adding it
            # else copy the neighbor from its left or top
            # tracking the child parent label (if neighbors are same then we will prefer smaller neighbor )
            if top_neighbor == -1 and left_neighbor == -1:
                label_g = label_g + 1
                add_label(loc, label_g, label_array)
            else:
                if top_neighbor == -1:
                    label_loc = Location()
                    label_loc.__int__(loc.row, loc.col - 1)
                    label = get_value_from_label_array(label_loc, label_array)
                    add_label(loc, label, label_array)
                elif left_neighbor == -1:
                    label_loc = Location()
                    label_loc.__int__(loc.row - 1, loc.col)
                    label = get_value_from_label_array(label_loc, label_array)
                    add_label(loc, label, label_array)
                else:
                    label_loc = Location()
                    label_loc.__int__(loc.row, loc.col - 1)
                    left_label = get_value_from_label_array(label_loc, label_array)
                    label_loc.__int__(loc.row - 1, loc.col)
                    right_label = get_value_from_label_array(label_loc, label_array)
                    if left_label < right_label:
                        add_label(loc, left_label, label_array)
                        try:
                            label_dict.__setitem__(right_label, left_label)
                        except RuntimeError:
                            print('Exception occur')
                    elif right_label < left_label:
                        add_label(loc, right_label, label_array)
                        try:
                            label_dict.__setitem__(left_label, right_label)
                        except RuntimeError:
                            print('Exception occur')
                    elif right_label == left_label:
                        add_label(loc, right_label, label_array)
            col = col + 1
        row = row + 1
    return label_array, label_dict


"""
    this is pass2 of the algorithm 
    it first call pass1 and get label array and label dictionary
    then replacing all child pixels with their parents pixels 
    @:return label array
"""


def pass2():
    label_array, label_dict = pass1()
    row_index = 0
    for row in label_array:
        col_index = 0
        for value in row:
            temp_value = label_dict.get(value)
            if temp_value is not None:
                label_array[row_index][col_index] = temp_value
            col_index = col_index + 1
        row_index = row_index + 1
    return label_array


"""
    simply write the image using cv2
    @:param name of the image
    @:param array of the image (2d)
"""


def write_image(name, array):
    cv2.imwrite(name, array)
    print(name + " binary image has been created")
    print("\n")


"""
    main method
"""


def main():
    label_array = pass2()
    assert label_array is not None
    write_image("testing.png", label_array)


# run the application
main()
