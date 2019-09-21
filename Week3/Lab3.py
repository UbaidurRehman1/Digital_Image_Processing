import numpy as np
import cv2
import os.path as os_path
import matplotlib.pyplot as plt


class ImgProcessing:
    def __int__(self, path, flag='binary_histogram'):
        self.path = path
        if self.is_image_exists():
            # getting np array of the giving image from the path
            img = self.get_image_np_array()

            if flag == 'recursive_cut':
                self.recursive_cut(img)
            else:
                self.binary_histogram(img)
        else:
            print("The file you have asked not found, please put pics in pics folder")

    def recursive_cut(self, img):
        path = self.path
        list_of_sum_of_internal_array = ImgProcessing.get_list_of_sum_of_internal_array(img)
        # self.create_histogram(list_of_sum_of_internal_array, 100)
        print('... recursive cut ....')
        # getting max value in the list
        max_value_of_sum_of_internal_lists = list_of_sum_of_internal_array.max()

        max_value_string = str(max_value_of_sum_of_internal_lists)
        number_zeros = len(max_value_string) - 2
        number_to_minus_string = '1' + ('0' * number_zeros)
        number_to_minus = 2 * int(number_to_minus_string)

        normalize_max_value = ((max_value_of_sum_of_internal_lists - number_to_minus)
                               + max_value_of_sum_of_internal_lists) / 2;

        print(normalize_max_value)

        # now creating a range by subtracting multiple of zeros to ensure that it will be average
        # range = (normalize_max_value - (number_to_minus/2), normalize_max_value + (number_to_minus/2))
        range_list = []

        max_value = normalize_max_value + (number_to_minus/2)
        min_value = normalize_max_value - (number_to_minus/2)

        # range_width = max_value - min_value
        # range_width = int(range_width)
        #
        # for i in range(range_width):
        #     range_list.append(min_value + i)

        # print(range)
        # now getting indexing by matching our average threshold
        index_list = []
        for value in list_of_sum_of_internal_array:
            if max_value >= value >= min_value:
                index_list.append(1)
            else:
                index_list.append(0)

        print(index_list)
        # classifying these by making clusters of these indices
        # [(image_start, image_end), (image_start, image_end), (image_start, image_end), (image_start, image_end), ...]
        cut_list = []
        cluster = 0
        counter = 0
        for i in range(len(index_list)):
            if index_list.__getitem__(i) == 1:
                cluster = cluster + i
                counter = counter + 1
            elif index_list.__getitem__(i - 1) == 1 and index_list.__getitem__(i) == 0:
                cut_list.append(int(cluster/counter))
                cluster = 0
                counter = 0
        print(cut_list)

        # final cut list

        final_cut_list = []
        for i in range(len(cut_list)):
            if i != 0:
                temp_tuple = (cut_list.__getitem__(i - 1), cut_list.__getitem__(i))
                final_cut_list.append(temp_tuple)

        print(final_cut_list)

        # cutting
        img = self.get_image_np_array()
        l, w = img.shape

        temp = img[i]

        image_counter = 0;
        for index_tuple in final_cut_list:
            image_counter = image_counter + 1;
            t_length = index_tuple[1] - index_tuple[0]
            temp_img_array = np.arange(t_length * w).reshape(t_length, w)
            for i in range(t_length):
                i = i + index_tuple[0]
                real_img_part = img[i]
                new_img_part = temp_img_array[i - index_tuple[0]]
                for index in range(w):
                    new_img_part[index] = real_img_part[index]
            print(temp_img_array)
            self.write_image(self.path.replace('/', '').replace('.png', '')
                             + str(image_counter) + ".png", temp_img_array)





    @staticmethod
    def get_list_of_sum_of_internal_array(img):
        l, w = img.shape;
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
        cv2.imwrite(name, array)
        print(name + " binary image has been created")
        print("\n\n\n")

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


main()
