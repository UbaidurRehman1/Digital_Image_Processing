import numpy as np
import cv2
import random


def arithmeticFilter(im):
    img = im
    w = 2

    for i in range(2, im.shape[0] - 2):
        for j in range(2, im.shape[1] - 2):
            block = im[i - w:i + w + 1, j - w:j + w + 1]
            m = np.mean(block, dtype=np.float32)
            img[i][j] = int(m)
    return img


def add_gaussian_noise(t_img, variance):
    mean = 0
    noisy_img = t_img + np.random.normal(mean, variance, t_img.shape)
    noisy = np.clip(noisy_img, 0, 255)
    return noisy.astype(np.uint8)


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


def main():
    img = cv2.imread("test_image.jpg", cv2.IMREAD_GRAYSCALE)
    sp_img_1 = sp_noise(img, prob=0.15)
    sp_img_2 = sp_noise(img, prob=0.20)
    g_img_1 = add_gaussian_noise(img, variance=100)
    g_img_2 = add_gaussian_noise(img, variance=150)
    cv2.imshow('Original Image', img)
    cv2.waitKey(10)
    cv2.imshow('sp Image using p 0.15', sp_img_1)
    cv2.waitKey(10)
    cv2.imshow('sp Image using p 0.20', sp_img_2)
    cv2.waitKey(10)
    cv2.imshow('Gaussian Image variance 100', g_img_1)
    cv2.waitKey(10)
    cv2.imshow('Gaussian Image variance 120', g_img_2)
    cv2.waitKey(10)
    assert img is not None

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
    cv2.waitKey(0)


main()
