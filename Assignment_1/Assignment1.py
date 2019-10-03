import cv2

'''
@:param width and height 
@:return dimension
'''
def get_dim(width, height):
    dim = (width, height)
    return dim


'''
@:return numpy array of the image getting from the path        
'''
def get_image_np_array(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    print(path, " is converted to ndArray")
    return img


'''
@:param path of the image
@:param dimension
@:return image of custom size
'''
def get_pic(path, dim):
    img = get_image_np_array(path)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized_img


'''
@:return get test pic (myself)
'''
def get_test_pic():
    img = get_pic("pics/test_image.jpg", get_dim(500, 500))
    return img


'''
    @:return glasses image 
'''
def get_glasses_img():
    img = get_pic("pics/glasses.png", get_dim(180, 100))
    return img


'''
    @:param test image 
    @:return it set the glasses to test image
'''
def set_glasses(test_pic):
    glasses_img = get_glasses_img()
    row_counter = 0
    for row in range(160 + 5, 260 + 5):
        pixel_counter = 0
        flag = True
        counter = 0
        for pixel in range(180 - 32, 360 - 32):
            glasses_pixel = glasses_img[row_counter][pixel_counter]
            if glasses_pixel < 150:
                if flag:
                    test_pic[row][pixel] = 0
                    flag = False
                    counter = counter + 1
                elif not flag:
                    flag = True
                    counter = 0
            pixel_counter = pixel_counter + 1
        row_counter = row_counter + 1
    return test_pic


'''
    @:return cap image
'''
def get_cap():
    return get_pic("pics/cap.png", get_dim(300 - 60, 200))


'''
    @:param test image
    @:return set the cap and return the image
'''
def set_cap(test_pic):
    cap_pic = get_cap()
    row_counter = 0
    for row in range(50, 250):
        pixel_counter = 0
        for pixel in range(120, 420 - 60):
            cap_pixel = cap_pic[row_counter][pixel_counter]
            if cap_pixel < 100:
                test_pic[row][pixel] = cap_pixel
            pixel_counter = pixel_counter + 1
        row_counter = row_counter + 1
    return test_pic


'''
    @:return scarf image
'''
def get_scarf():
    return get_pic("pics/man_scarf.jpg", get_dim(340, 200))


'''
    @:param test pic
    @:return set teh scarf and return the image
'''
def set_scarf(test_pic):
    scarf_pic = get_scarf()
    row_counter = 0
    for row in range(320, 500):
        pixel_counter = 0
        for pixel in range(70, 410):
            scarf_pixel = scarf_pic[row_counter][pixel_counter]
            if scarf_pixel < 150:
                test_pic[row][pixel] = scarf_pixel
            pixel_counter = pixel_counter + 1
        row_counter = row_counter + 1
    return test_pic


'''
    main method 
'''
def main():
    test_pic = get_test_pic()
    test_pic = set_glasses(test_pic)
    test_pic = set_cap(test_pic)
    test_pic = set_scarf(test_pic)
    cv2.imshow("test image", test_pic)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
