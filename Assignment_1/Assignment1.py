from Assignment_1.Lab3.Lab3 import ImgProcessing


def main():
    img_proc = ImgProcessing()
    img_proc.__int__("pics/test_image.jpg")
    img = img_proc.get_image_np_array()
    print(img)


main()
