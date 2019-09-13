#importing Image from PIL
import  PIL
from PIL import Image

#open image
im = Image.open("lena.ppm")

#printing the details of image
print(im.format, im.size, im.mode)

#showing the image
im.show()


#converting files to JPEG

