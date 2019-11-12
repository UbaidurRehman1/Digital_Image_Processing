import numpy as np
import cv2
import matplotlib.pyplot as plt

def histogram_equalization(img):
    # create an array of 256 single dimension
    intensity_array = np.zeros(shape=(256,), dtype=np.int)

    # insert the count of intensities in the intensity array
    for row in img:
        for pixel in row:
            intensity_array[pixel] += 1

    # print(intensity_array)

    width, height = img.shape
    size = width * height
    # create an array which store the probabilities of counting of intensities
    probability_intensity_array = intensity_array / float(size)
    # print(probability_intensity_array)
    # calculating commutative distribution function
    cumulative_distribution_function = np.zeros(shape=(256,), dtype=np.float)
    t_cumulative_distribution_function = np.zeros(shape=(256,), dtype=np.uint8)

    value = 0
    for i in range(0, len(probability_intensity_array)):
        cumulative_distribution_function[i] = value + probability_intensity_array[i]
        value = cumulative_distribution_function[i]

    for i in range(0, len(cumulative_distribution_function)):
        t_cumulative_distribution_function[i] = round(i * cumulative_distribution_function[i])

    imag_after_histogram_equalization = np.zeros(img.shape, dtype=np.uint8)

    for row_index in range(0, len(img)):
        for col_index in range(0, len(img[0])):
            imag_after_histogram_equalization[row_index][col_index] = \
                t_cumulative_distribution_function[img[row_index][col_index]]
    return imag_after_histogram_equalization


# Task 1
# reading image
path = 'D:/Documents/DigitalImageProcessing/Week8/image.png'
read_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
cv2.imshow('Image', read_img)
cv2.waitKey(0)

# creating histogram
plt.hist(read_img.ravel(), bins=256, range=(0, 255), fc='k', ec='k')
plt.show()

img_after_histogram_equalization = histogram_equalization(read_img)
plt.hist(img_after_histogram_equalization.ravel(), bins=256, range=(0, 255), fc='k', ec='k')
plt.show()

cv2.imshow('Image after equalization', img_after_histogram_equalization)
cv2.waitKey(0)
# print(img_after_histogram_equalization)
