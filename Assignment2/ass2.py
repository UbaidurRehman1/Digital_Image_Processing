import numpy as np
import cv2
import random

"""
 @:param img 2d numpy array
 @:return img 2d numpy array
"""


def arithmeticFilter(im):
    img = im
    w = 2

    for i in range(2, im.shape[0] - 2):
        for j in range(2, im.shape[1] - 2):
            block = im[i - w:i + w + 1, j - w:j + w + 1]
            m = np.mean(block, dtype=np.float32)
            img[i][j] = int(m)
    return img


"""
 @:param img 2d numpy array
 @:return img 2d numpy array
"""


def add_gaussian_noise(t_img, variance):
    mean = 0
    noisy_img = t_img + np.random.normal(mean, variance, t_img.shape)
    noisy = np.clip(noisy_img, 0, 255)
    return noisy.astype(np.uint8)


"""
 @:param img 2d numpy array
 @:param prob probability for salt and pepper 
 @:return img 2d numpy array
"""


def sp_noise(image, prob):
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


"""
 @:param img 2d numpy array
 @:param float param for Contra Harmonic Filter
 @:return img 2d numpy array
"""


def cm_filter(img, q):
    target = np.zeros(img.shape, np.uint8)
    r = 1
    row, col = img.shape
    for i in range(r, row - r):
        for j in range(r, col - r):
            block = img[i - r:i + r + 1, j - r:j + r + 1]
            nom = np.sum(np.power(block, q + 1))
            dem = np.sum(np.power(block, q))
            contraharmonic = nom / dem
            if dem == 0:
                target[i][j] = target[i][j]
            else:
                target[i][j] = int(contraharmonic)
    return target


"""
 @:param img 2d numpy array
 @:return img 2d numpy array
"""


def mid_point_filter(img):
    target = np.zeros(img.shape, np.uint8)
    r = 1
    row, col = img.shape
    for i in range(r, row - r):
        for j in range(r, col - r):
            block = img[i - r:i + r + 1, j - r:j + r + 1]
            minimum = np.amin(block)
            maximum = np.amax(block)
            midpoint = 1 / 2 * (minimum + maximum)
            target[i][j] = int(midpoint)
    return target


def main():
    img = cv2.imread("test_image.jpg", cv2.IMREAD_GRAYSCALE)

    # inducing salt and pepper noise
    sp_img_1 = sp_noise(img, prob=0.15)
    sp_img_2 = sp_noise(img, prob=0.20)

    # inducing gaussian noise
    g_img_1 = add_gaussian_noise(img, variance=100)
    g_img_2 = add_gaussian_noise(img, variance=150)
    cv2.imshow('Original Image', img)

    # showing salt and pepper noised image
    cv2.waitKey(10)
    cv2.imshow('sp Image using p 0.15', sp_img_1)
    cv2.waitKey(10)
    cv2.imshow('sp Image using p 0.20', sp_img_2)
    cv2.waitKey(10)

    # # showing gaussian noised image
    cv2.imshow('Gaussian Image variance 100', g_img_1)
    cv2.waitKey(10)
    cv2.imshow('Gaussian Image variance 120', g_img_2)
    cv2.waitKey(10)

    # using median filter to remove noise from all pics
    processed_image_1 = cv2.medianBlur(sp_img_1, 3)
    cv2.imshow('Restored mf sp noised  p 0.15', processed_image_1)
    cv2.waitKey(10)

    processed_image_2 = cv2.medianBlur(sp_img_2, 3)
    cv2.imshow('Restored mf sp noised p 0.20', processed_image_2)
    cv2.waitKey(10)

    processed_image_3 = cv2.medianBlur(g_img_1, 3)
    cv2.imshow('Restored mf gaussian noised v 100', processed_image_3)
    cv2.waitKey(10)
    processed_image_4 = cv2.medianBlur(g_img_2, 3)
    cv2.imshow('Restored mf gaussian noised v 120', processed_image_4)
    cv2.waitKey(10)

    # arithmetic mean filter
    arithmetic_restored_im_1 = arithmeticFilter(sp_img_1)
    cv2.imshow('Restored af sp noised p 0.15', arithmetic_restored_im_1)
    cv2.waitKey(10)

    arithmetic_restored_im_2 = arithmeticFilter(sp_img_2)
    cv2.imshow('Restored af sp noised p 0.20', arithmetic_restored_im_2)
    cv2.waitKey(10)

    arithmetic_restored_im_3 = arithmeticFilter(g_img_1)
    cv2.imshow('Restored af gaussian noised v 100', arithmetic_restored_im_3)
    cv2.waitKey(10)

    arithmetic_restored_im_4 = arithmeticFilter(g_img_2)
    cv2.imshow('Restored af gaussian noised v 120', arithmetic_restored_im_4)
    cv2.waitKey(10)

    # contra harmonic mean filter
    contraharmonic_mean_restored_sp_img_1 = cm_filter(sp_img_1, 0.0001)
    contraharmonic_mean_restored_sp_img_2 = cm_filter(sp_img_2, 0.001)
    contraharmonic_mean_restored_g_img_1 = cm_filter(g_img_1, 0.001)
    contraharmonic_mean_restored_g_img_2 = cm_filter(g_img_2, 0.001)

    cv2.imshow('Restored Contraharmonic sp noised p 0.15', contraharmonic_mean_restored_sp_img_1)
    cv2.waitKey(10)
    cv2.imshow('Restored Contraharmonic sp noised p 0.20', contraharmonic_mean_restored_sp_img_2)
    cv2.waitKey(10)
    cv2.imshow('Restored Contraharmonic->gaussian v 100', contraharmonic_mean_restored_g_img_1)
    cv2.waitKey(10)
    cv2.imshow('Restored Contraharmonic->gaussian v 120', contraharmonic_mean_restored_g_img_2)
    cv2.waitKey(10)

    # mid point filter
    mid_point_restored_sp_img_1 = mid_point_filter(sp_img_1)
    mid_point_restored_sp_img_2 = mid_point_filter(sp_img_2)
    mid_point_restored_g_img_1 = mid_point_filter(g_img_1)
    mid_point_restored_g_img_2 = mid_point_filter(g_img_2)

    cv2.imshow('Restored Mid Point Filter sp noised p 0.15', mid_point_restored_sp_img_1)
    cv2.waitKey(10)
    cv2.imshow('Restored Mid Point Filter sp noised p 0.20', mid_point_restored_sp_img_2)
    cv2.waitKey(10)
    cv2.imshow('Restored Mid Point Filter->gaussian v 100', mid_point_restored_g_img_1)
    cv2.waitKey(10)
    cv2.imshow('Restored Mid Point Filter->gaussian v 120', mid_point_restored_g_img_2)
    cv2.waitKey(0)


main()
