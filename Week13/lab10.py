import cv2
import numpy as np

# # reading image
# pic = cv2.imread('pic1.png')
#
# cv2.imshow('Original Image', pic)
#
# # kernel of size 5 by 5
# kernel = np.ones((5, 5), np.uint8)
#
# eroded_pic = cv2.erode(pic, kernel, iterations=1)
# cv2.imshow('Eroded Pic', eroded_pic)
# cv2.waitKey(0)
#
# dilated_pic = cv2.dilate(pic, kernel, iterations=1)
# cv2.imshow('Dilated Pic', dilated_pic)
# cv2.waitKey(0)
#
# opening_img = cv2.morphologyEx(pic, cv2.MORPH_OPEN, kernel)
# cv2.imshow('Opening', opening_img)
# cv2.waitKey(0)
#
# closing_img = cv2.morphologyEx(pic, cv2.MORPH_CLOSE, kernel)
# cv2.imshow('Closing', closing_img)
# cv2.waitKey(0)

# Task 2
def main():
    pic_2 = cv2.imread('pic2.png')

    row_for_detection = pic_2[13]
    column_for_detection = pic_2[1][1]

    assert column_for_detection is not None

    blue_lines_map = []
    horizontal_line_map = []
    counter = 0
    in_ = 0
    out_ = 0
    range_ = []
    # gives lines
    for pixel in row_for_detection:
        flag1 = False
        total = np.sum(pixel)
        if total < 730:
            in_ = in_ + 1
            out_ = 0
            range_.append(counter)
            flag2 = True
            counter = counter + 1
            continue
        if in_ != 0 and out_ == 0:
            blue_lines_map.append(range_)
            range_ = []
        in_ = 0
        out_ = out_ + 1
        counter = counter + 1
    l_c = 1
    for line in blue_lines_map:
        firstPixel = line[0]
        lastPixel = line[-1]
        whiten_the_line(pic_2, firstPixel, lastPixel, pic_2.shape[0])
        # cv2.imshow('pic ' + str(l_c), pic_2)
        # cv2.waitKey(0)
        l_c = l_c + 1

    counter = 0
    in_ = 0
    out_ = 0
    range_ = []
    for row in pic_2:
        pixel = row[0]
        total = np.sum(pixel)
        if total < 740:
            in_ = in_ + 1
            out_ = 0
            range_.append(counter)
            flag2 = True
            counter = counter + 1
            continue
        if in_ != 0 and out_ == 0:
            horizontal_line_map.append(range_)
            range_ = []
        in_ = 0
        out_ = out_ + 1
        counter = counter + 1
    l_c = 1

    for line in horizontal_line_map:
        firstPixel = line[0]
        lastPixel = line[-1]
        whiten_horizontal_line(pic_2, firstPixel, lastPixel)
        cv2.imshow('...', pic_2)
        cv2.waitKey(0)

    # doing morph operations
    kernel = np.ones((10, 10), np.uint8)
    #
    pic_2 = cv2.morphologyEx(pic_2, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('Opening', opening_img)
    # cv2.waitKey(0)
    #
    kernel = np.ones((2, 2), np.uint8)
    pic_2 = cv2.morphologyEx(pic_2, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('final', pic_2)
    cv2.waitKey(0)

def whiten_the_line(pic, first_pixel, last_pixel, height):
    for i in range(0, height):
        for r in range(0, (last_pixel - first_pixel) + 3):
            row = pic[i]
            pixel = row[first_pixel + r]
            for p in range(0, 3):
                pixel[p] = 255
    return pic

def whiten_horizontal_line(pic, first_pixel, last_pixel):
    for j in range(0, (last_pixel - first_pixel) + 5):
        row = pic[j + first_pixel - 2]
        for pixel in row:
            for p in range(0, 3):
                pixel[p] = 255


if __name__ == '__main__':
    main()
# assert blue_lines_map is not None
