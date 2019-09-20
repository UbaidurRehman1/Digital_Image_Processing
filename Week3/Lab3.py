import numpy as np
import cv2
import os.path as os_path


    # imgProc2 = ImgProcessing("B2.jpg");
    # imgProc3 = ImgProcessing("B3.jpg");
# img = cv2.imread("pics/B2.jpg", cv2.IMREAD_GRAYSCALE)
# print(type(img))

# length, width = img.shape
# newArray = array = np.arange(img.size).reshape(length, width)
# min = img.min()
# max = img.max()
# val = cv2.THRESH_BINARY;
# ret, thresh1 = cv2.threshold(img, img.min(), img.max(), cv2.THRESH_BINARY)
# cv2.imshow("img", newArray)
# cv2.imwrite("B1_binary_image.png", newArray)
# print("img is created")
# im = Image.fromarray(newArray)
# im.save("your_file.png")


class ImgProcessing:
    def __int__(self, path):
        self.path = path
        if self.is_image_exists():
            # getting np array of the giving image from the path
            img = self.get_image_np_array()

            # getting l = length and w = width
            l, w = img.shape

            # getting empty array of size same as our image
            bin_img = ImgProcessing.get_empty_np_array(l, w)

            # populating this array with 0 if pixel intensity is <= 128 or 255 is intensity is > 128
            bin_img = ImgProcessing.populate_empty_array_with_binary_value(img, bin_img)

            # writing the populated array
            ImgProcessing.write_image("binary_" + path.replace("/", ""), bin_img)
        else:
            print("The file you have asked not found")

    def is_image_exists(self):
        if os_path.exists(self.path):
            print(self.path, " is existed")
            return True
        return False

    def get_image_np_array(self):
        path = self.path
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        print(path, " is converted to ndArray")
        return img

    @staticmethod
    def get_empty_np_array(length, width):
        array = np.arange(length * width).reshape(length, width)
        print("create an empty 2d array of ", length, width)
        return array

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

    @staticmethod
    def write_image(name, array):
        cv2.imwrite(name, array)
        print(name + " binary image has been created")


def main():
    obj = ImgProcessing()
    obj.__int__("pics/B1.png")


main()
