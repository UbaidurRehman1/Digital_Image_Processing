import cv2
import numpy as np

img = cv2.imread('baboon.jpg')

#creating filter kernel
kernel = np.ones((5,5),np.float32)/25

#apply this kernel to our pic
smoothed_img = cv2.filter2D(img,-1,kernel)

#show image, first arg is string and second is source of image 
cv2.imshow('Original Image', img)
cv2.imshow('Smoothed Image', smoothed_img)

#will wait infinetly to show the screens
cv2.waitKey(0)

#if user pressed a key then it will destroy all windows
cv2.destroyAllWindows()