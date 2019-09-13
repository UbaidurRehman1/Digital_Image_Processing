#import
import cv2
import numpy as np
from PIL import  Image

#reading image
image = cv2.imread('baboon.png')

#converting image to array 
rgb = np.asarray(image)

#seperating the channels 
r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

#multiplying with specific fector and adding them
intermediate_vector = 0.2989 * r + 0.5870 * g + 0.1140 * b

#getting image from the vector
gray = Image.fromarray(intermediate_vector)

#show image, first arg is string and second is source of image 
cv2.imshow('Original Image', image)
#show image
gray.show()


#will wait infinetly to show the screens
cv2.waitKey(0)

#if user pressed a key then it will destroy all windows
cv2.destroyAllWindows()

