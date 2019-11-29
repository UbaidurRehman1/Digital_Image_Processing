# using cv2
import cv2

# getting the shape
shape = cv2.imread('test.png')

# shape should be defined
assert shape is not None

# showing shape
cv2.imshow('Original shape', shape)
cv2.waitKey(0)

# looping through each pixel of shape and replacing value to 0 for black
size = shape.shape
for row in range(0, size[0]):
    # assert row is not None
    for col in range(0, size[1]):
        for pixel in range(0, size[2]):
            shape[row][col][pixel] = 0
cv2.imshow('Filled shape', shape)
cv2.waitKey(0)
