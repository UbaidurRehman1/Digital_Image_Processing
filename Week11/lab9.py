import cv2
import numpy as np
import math


def convolution(image, kernel, average=False):
    image_row, image_col = image.shape
    kernel_row, kernel_col = kernel.shape
    output = np.zeros(image.shape)
    pad_height = int((kernel_row - 1) / 2)
    pad_width = int((kernel_col - 1) / 2)
    padded_image = np.zeros((image_row + (2 * pad_height), image_col + (2 * pad_width)))
    padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image
    for row in range(image_row):
        for col in range(image_col):
            output[row, col] = np.sum(kernel * padded_image[row:row + kernel_row, col:col + kernel_col])
            if average:
                output[row, col] /= kernel.shape[0] * kernel.shape[1]
    return output


def dnorm(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)


def gaussian_kernel(size, sigma=1.0):
    kernel_1D = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)
    kernel_2D *= 1.0 / kernel_2D.max()
    return kernel_2D


def gaussian_blur(image, kernel_size):
    kernel = gaussian_kernel(kernel_size, sigma=math.sqrt(kernel_size))
    return convolution(image, kernel, average=True)


def apply_average_filter(img, kernel_size, is_weighted_kernel):
    # block_size = kernel_size[0] - 1
    # kernel = getKernel(kernel_size)
    direction = get_tuple_2d_array(kernel_size)

    for row_index in range(0, img.shape[0]):
        for col_index in range(0, img.shape[1]):
            if not is_weighted_kernel:
                kernel = getKernel(kernel_size)
            else:
                kernel = get_weighted_kernel(kernel_size)
            if row_index == 171 and col_index == 174:
                print('asserted')
            for k_row_i in range(0, kernel_size[0]):
                for k_col_i in range(0, kernel_size[1]):
                    point = direction[k_row_i][k_col_i]
                    l_x = point[0] + row_index
                    l_y = point[1] + col_index
                    try:
                        if l_x >= 0 and l_y >= 0:
                            kernel[k_row_i][k_col_i] = kernel[k_row_i][k_col_i] * img[l_x][l_y]
                        else:
                            kernel[k_row_i][k_col_i] = kernel[k_row_i][k_col_i] * 0
                    except IndexError:
                        kernel[k_row_i][k_col_i] = kernel[k_row_i][k_col_i] * 0
            average_pix = np.average(kernel)
            img[row_index][col_index] = average_pix
    return img


'''
    @:return direction array
'''


def get_tuple_2d_array(shape):
    arr = []
    x_b = -(math.floor(shape[0] / 2))
    y = x_b - 1
    for i in range(0, shape[0]):
        x = x_b
        y = y + 1
        internal_array = []
        for j in range(0, shape[1]):
            internal_array.append((x, y))
            x = x + 1
        arr.append(internal_array)
    return arr


def getKernel(shape):
    arr = []
    for i in range(0, shape[0]):
        internal_array = []
        for j in range(0, shape[1]):
            internal_array.append(1)
        arr.append(internal_array)
    return arr


def get_weighted_kernel(shape):
    arr = []
    limit = math.ceil(shape[0] / 2)
    for i in range(0, shape[0]):
        multiplier = i + 1
        internal_array = []
        for j in range(1, shape[1] + 1):
            dif = j - limit
            if j <= limit:
                internal_array.append(j)
            else:
                internal_array.append(limit - dif)
        if multiplier <= limit:
            internal_array = [x * multiplier for x in internal_array]
        else:
            multiplier = (2 * limit) - (i + 1)
            internal_array = [x * multiplier for x in internal_array]
        arr.append(internal_array)
    return arr


def main():
    img = cv2.imread('test.png', cv2.IMREAD_GRAYSCALE)
    cv2.imshow('Original Image', img)
    # cv2.waitKey(10)
    # avg_filter_img_3_3 = apply_average_filter(img, kernel_size=(3, 3), is_weighted_kernel=False)
    # cv2.imshow('(3, 3), linear', avg_filter_img_3_3)
    # cv2.waitKey(10)
    # avg_filter_img_5_5 = apply_average_filter(img, kernel_size=(5, 5), is_weighted_kernel=False)
    # cv2.imshow('(5, 5) linear', avg_filter_img_5_5)
    # cv2.waitKey(10)
    # avg_filter_img_15_15 = apply_average_filter(img, kernel_size=(15, 15), is_weighted_kernel=False)
    # cv2.imshow('(15, 15) linear', avg_filter_img_15_15)
    # cv2.waitKey(10)
    # avg_filter_img_35_35 = apply_average_filter(img, kernel_size=(35, 35), is_weighted_kernel=False)
    # cv2.imshow('(35, 35) linear', avg_filter_img_35_35)
    # cv2.waitKey(10)
    # avg_filter_img_3_3 = apply_average_filter(img, kernel_size=(3, 3), is_weighted_kernel=True)
    # cv2.imshow('(3, 3), weighted', avg_filter_img_3_3)
    # cv2.waitKey(10)
    # avg_filter_img_5_5 = apply_average_filter(img, kernel_size=(5, 5), is_weighted_kernel=True)
    # cv2.imshow('(5, 5) weighted', avg_filter_img_5_5)
    # cv2.waitKey(10)
    # avg_filter_img_15_15 = apply_average_filter(img, kernel_size=(15, 15), is_weighted_kernel=True)
    # cv2.imshow('(15, 15) weighted', avg_filter_img_15_15)
    # cv2.waitKey(10)
    # avg_filter_img_35_35 = apply_average_filter(img, kernel_size=(35, 35), is_weighted_kernel=True)
    # cv2.imshow('(35, 35) weighted', avg_filter_img_35_35)
    # cv2.waitKey(0)

    tar = gaussian_blur(img, 1)
    cv2.imshow('result', tar)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
