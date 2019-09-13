#importing
import cv2
import numpy as np

#reading image
img = cv2.imread('baboon.jpg')


#creating kernel for sharpeing image
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

#applying kernel
sharped_img = cv2.filter2D(img, -1, kernel)

#show image, first arg is string and second is source of image 
cv2.imshow('Original Image', img)
cv2.imshow('Smoothed Image', sharped_img)

#will wait infinetly to show the screens
cv2.waitKey(0)

#if user pressed a key then it will destroy all windows
cv2.destroyAllWindows()