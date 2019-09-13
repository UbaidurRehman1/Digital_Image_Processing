#here i will use cv2
import cv2

#reading image
image = cv2.imread('baboon.png')
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

#show image, first arg is string and second is source of image 
cv2.imshow('Original Image', image)
cv2.imshow('Converted Image', gray)

#will wait infinetly to show the screens
cv2.waitKey(0)

#if user pressed a key then it will destroy all windows
cv2.destroyAllWindows()