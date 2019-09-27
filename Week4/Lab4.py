from Assignment_1.Lab3 import Lab3
import numpy as np
import cv2


def get_image_np_array(path):
    # noinspection PyUnresolvedReferences
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img


class Location:
    def __int__(self, row_, col_):
        self.row = row_
        self.col = col_


# --------------global variables--------------


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

def test():
    img_proc = Lab3.ImgProcessing()
    im_array = img_proc.get_empty_np_array(8, 8)
    list_arr = [[1, 1, 0, 1, 1, 1, 0, 1],
                [1, 1, 0, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 1, 0, 1],
                [0, 0, 0, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 1, 1, 1]]
    counter = 0
    for internal_list in list_arr:
        internal_counter = 0
        for value in internal_list:
            im_array[counter][internal_counter] = value
            internal_counter = internal_counter + 1
        counter = counter + 1
    return im_array


# if not exists return -1
# return the top neighborhood of given location
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

        if _val == 0:
            return -1
        return _val
    except RuntimeError:
        return -1


# if not exists then return -1
# return the left neighborhood of given location
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

        if _val == 0:
            return -1

        return _val
    except RuntimeError:
        return -1


# adding label in the given location
def add_label(l, _value, label_array):
    _row = l.row
    _col = l.col
    label_array[_row][_col] = _value


# getting value from the given location
def get_value_from_label_array(l, label_array):
    return label_array[l.row][l.col]


def pass1():
    im_array = get_image_np_array('Lab4-image.png')
    write_image("inter.png", im_array)
    # im_array = test()
    label_array = np.zeros((im_array.shape[0], im_array.shape[1]), dtype=int)
    loc = Location()
    label_dict = {}
    label_g = 0
    row = 0
    for external_list in im_array:
        col = 0
        for value in external_list:
            if value == 0:
                col = col + 1
                continue
            loc.__int__(row, col)
            top_neighbor = get_top(im_array, loc)
            left_neighbor = get_left(im_array, loc)
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


def write_image(name, array):
    cv2.imwrite(name, array)
    print(name + " binary image has been created")
    print("\n")


def change_zero_255(arr):
    row_index = 0
    for row in arr:
        col = 0
        for value in row:
            if value == 0:
                arr[row_index][col] = 255
            col = col + 1
        row_index = row_index + 1
    return arr


def main():
    label_array = pass2()
    label_array = change_zero_255(label_array)
    assert label_array is not None
    write_image("testing.png", label_array)


main()
