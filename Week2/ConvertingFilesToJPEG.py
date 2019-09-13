import os, sys
import PIL
from PIL import  Image

#getting arguments from the command lines
for infile in sys.argv[1:]:

    #returing filename and extension from the infile which is the name of file
    f, e = os.path.splitext(infile)

    #adding .jpg extension
    outfile = f + ".jpg"

    #if infile and outfile are diffrent then let infile is u.png and outfile is u.jpg then 
    #this condition will true
    if infile != outfile:
        try:
            #first open the image and then save this image
            Image.open(infile).save(outfile)
            print('Image converted from', infile, ' to ', outfile)
        #if there is an error then 
        except IOError:
            print('connot convert ', infile)