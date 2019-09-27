import numpy as np
import cv2
import os.path as os_path
import matplotlib.pyplot as plt


class ImgProcessing:
    def __int__(self, path, flag='binary_histogram'):
        self.path = path
        if self.is_image_exists():
            print("image existed")
        else:
            print("The file you have asked not found, please put pics in pics folder")

    """
        @:param max_value any number 
        @:return a number less than 2 digits from the max_value
    """
    @staticmethod
    def get_subtract_number(max_value):
        max_value_string = str(max_value)
        number_zeros = len(max_value_string) - 2
        number_to_minus_string = '1' + ('0' * number_zeros)
        number_to_minus = int(number_to_minus_string)
        return number_to_minus

    # noinspection PyArgumentList
    def recursive_cut(self, img):
        # getting list of sum of internal lists of image 2d array
        # [sum of internal array, sum of internal array, ....]
        list_of_sum_of_internal_array = ImgProcessing.get_list_of_sum_of_internal_array(img)

        # getting max value in the list (sum of internal lists)
        max_value_of_sum_of_internal_lists = list_of_sum_of_internal_array.max()

        # getting a number which is supposed to minus from the max value
        number_to_minus = self.get_subtract_number(max_value_of_sum_of_internal_lists)

        # getting max value and min value to create a range
        max_value = max_value_of_sum_of_internal_lists
        min_value = max_value_of_sum_of_internal_lists - number_to_minus

        # white rows indices has value 1 and others have 0 in the index list
        index_list = self.get_marked_indices_list(list_of_sum_of_internal_array, max_value, min_value)

        cut_list = self.get_white_rows_indeces(index_list)

        final_cut_list = self.get_cut_tuple_list(cut_list)

        self.cut_images(final_cut_list)

    """
        @:param final_cut_list contain the tuple having two values which mention the start and end indices of 
                 of an image (which is supposed to separate)
    """
    def cut_images(self, final_cut_list):
        # cutting
        # we have cut list where we have give a tuple of mark (start_image_mark, and end_image_mark)
        # now we will get all the rows of pixels in between teh start_image_mark index and end_image_mark index
        # and put in the 2d numpy array of the same dimension length = end_image_mark index - start_image_mark index
        # and width will be as of original image
        # getting image
        img = self.get_image_np_array()
        # getting dimension
        l, w = img.shape
        image_counter = 0
        # getting tuple list
        for index_tuple in final_cut_list:
            # image counter for naming purpose only (no logic)
            image_counter = image_counter + 1
            temp_img_array = self.__separate_image__(img, index_tuple, w)

            # writing this image
            self.write_image(self.path.replace('/', '').replace('.png', '')
                             + str(image_counter) + ".png", temp_img_array)

    """
        @:param image_counter is the simply counter (int) 
        @:param img is the 2d array of original img
        @:param index_tuple is the tuple of shape (int, int) which tells starting and ending index of image (which
                is supposed to separate)
        @:param w is the width of the image (original image)
        @:return tmp_image_array a 2d numpy array which contain the separated image
    """
    @staticmethod
    def __separate_image__(img, index_tuple, w):
        # getting height of the image, the length of external array of 2d array
        t_length = index_tuple[1] - index_tuple[0]
        # getting 2d array
        temp_img_array = np.arange(t_length * w).reshape(t_length, w)
        # we are iterating till the length of 2d array (external length) height of image
        for i in range(t_length):
            i = i + index_tuple[0]
            # getting row from the real image 2d array
            real_img_part = img[i]

            # getting row from the newly created 2d array
            new_img_part = temp_img_array[i - index_tuple[0]]

            # inserting all values from the real image array to newly created image row
            for index in range(w):
                new_img_part[index] = real_img_part[index]
        # print(temp_img_array)
        return temp_img_array

    """
        @:param list cut_list has values which represent the indices of rows which are supposed to cut to 
                 separate the image
        @:return a list of tuple, each tuple contain the two values which are actually the starting and ending indices
                 of and image. (which is supposed to separate from the parent image)
    """
    @staticmethod
    def get_cut_tuple_list(cut_list):
        # now we have a cut_list where we have only row indices which contain most white pixels
        # now we want to convert this list to
        # [(image_start, image_end), (image_start, image_end), (image_start, image_end), (image_start, image_end), ...]
        # so we can conveniently execute a loop
        final_cut_list = []
        for i in range(len(cut_list)):
            if i != 0:
                temp_tuple = (cut_list.__getitem__(i - 1), cut_list.__getitem__(i))
                final_cut_list.append(temp_tuple)
        return final_cut_list

    """
        @:param list index list have 0 or 1 values depends on the whites rows. the indices having 1 values representing 
                white rows 
        @:return a list of indices which represents the white rows indeces (the rows which are supposed to be cut)
                  
    """
    @staticmethod
    def get_white_rows_indeces(index_list):
        cut_list = []
        cluster = 0
        counter = 0
        # we have a list of rows [the rows in which white pixels are most, these are marks as 1 and others
        # are marked as 0]
        # we are now averaging the indices of 1 and getting one marked row
        for i in range(len(index_list)):
            if index_list.__getitem__(i) == 1:
                cluster = cluster + i
                counter = counter + 1
            elif index_list.__getitem__(i - 1) == 1 and index_list.__getitem__(i) == 0:
                cut_list.append(int(cluster / counter))
                cluster = 0
                counter = 0
        return cut_list

    """
    @:param list 
    @:param int max_value
    @:param int min_value
    @:return this method return a list of same size as it get from its argument
             the indices of returned list will marked as 1 if the value in the same index of 
             list (got from the argument) has value in between the max_value and min_value 
             otherwise 0   
    """
    @staticmethod
    def get_marked_indices_list(list_of_sum_of_internal_array, max_value, min_value):
        index_list = []
        for value in list_of_sum_of_internal_array:
            if max_value > value > min_value:
                index_list.append(1)
            else:
                index_list.append(0)
        return index_list

    @staticmethod
    def get_list_of_sum_of_internal_array(img):
        list_of_sum_of_internal_array = []
        for internal_array in img:
            sum_of_internal_list = 0
            for pixel in internal_array:
                sum_of_internal_list = sum_of_internal_list + pixel
            list_of_sum_of_internal_array.append(sum_of_internal_list)
        return np.asarray(list_of_sum_of_internal_array)

    def binary_histogram(self, img):
        path = self.path
        # getting l = length and w = width
        l, w = img.shape

        # getting empty array of size same as our image
        bin_img = ImgProcessing.get_empty_np_array(l, w)

        # populating this array with 0 if pixel intensity is <= 128 or 255 is intensity is > 128
        bin_img = ImgProcessing.populate_empty_array_with_binary_value(img, bin_img)

        # writing the populated array
        ImgProcessing.write_image("binary_" + path.replace("/", ""), bin_img)

        # making histogram
        self.make_histogram()

    """
        checking if the file exists or not
        checking on the given path
    """
    def is_image_exists(self):
        if os_path.exists(self.path):
            print(self.path, " is existed")
            return True
        return False

    """
    @:return numpy array of the image getting from the path        
    """
    def get_image_np_array(self):
        path = self.path
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        print(path, " is converted to ndArray")
        return img

    """
        @:return an 2d array of given length and width 
    """
    @staticmethod
    def get_empty_np_array(length, width):
        array = np.arange(length * width).reshape(length, width)
        print("create an empty 2d array of ", length, width)
        return array

    """
        @:param img an array of given image 
        @:param empty_array  an empty array of same dimension as img array (2d array)
        @:return the same dimension array and it populate the empty array with 0 or 255 
            on some threshold which is 128
    """
    @staticmethod
    def populate_empty_array_with_binary_value(img, empty_array):
        length, width = img.shape
        print('Populating {} {} array with 0 or 255 intensities based'' on 128 threshold, please wait'
              .format(length, width))
        for i in range(length):
            internal_array = img[i]
            internal_counter = 0
            for pixel in internal_array:
                # 128 is the threshold
                if pixel > 128:
                    empty_array[i][internal_counter] = 255
                else:
                    empty_array[i][internal_counter] = 0

                # print(newArray[i][internal_counter], end=' ')
                internal_counter = internal_counter + 1
        print('Population done')
        return empty_array

    """
        @:param name the name of binary image
        @:param array 2d numpy array which is supposed to write
    """
    @staticmethod
    def write_image(name, array):
        # cv2.imwrite(name, array)
        cv2.imwrite(name, array)
        print(name + " binary image has been created")
        print("\n")

    """
        this method make a histogram of the gray scale img
    """
    def make_histogram(self):
        img = self.get_image_np_array()
        print('making histogram of ' + self.path)
        one_d_array = ImgProcessing.convert_to_one_d_array(img)
        num_bins = 255
        self.create_histogram(one_d_array, num_bins)

    def create_histogram(self, one_d_array, num_bins):
        plt.hist(one_d_array, num_bins, facecolor='blue', alpha=0.5)
        plt.show()
        print('Histogram of ', self.path, 'created')

    """
        @:param img the 2d numpy array of the image
        @:return 1d array of the image
    """
    @staticmethod
    def convert_to_one_d_array(img):
        l, w = img.shape
        one_d_array = []
        for i in range(l):
            internal_array = img[i]
            for pixel in internal_array:
                one_d_array.append(pixel)
        return one_d_array


def main():
    # print('main')
    obj = ImgProcessing()
    obj.__int__("pics/B1.png")
    obj.__int__("pics/B2.jpg")
    obj.__int__("pics/B3.jpg")
    obj.__int__("pics/XY-cuts.png", 'recursive_cut')
    obj.__int__("pics/XY-cutss.png", 'recursive_cut')


if __name__ == "__main__":
    main()
