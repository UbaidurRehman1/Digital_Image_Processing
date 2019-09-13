#here i will use cv2
import cv2

#reading image
image = cv2.imread('baboon.png')
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)