# -*- coding: utf-8 -*-
"""
Created on Thu May 11 13:40:22 2017
Indexing Pokemon Sprites in Python, OpenCV and mahotas
@author: tsrivas
"""
# import the necessary packages
from Zernike_Moments import ZernikeMoments
import numpy as np
import cv2
import argparse
import cPickle
import glob

# construct the argument parser
ap=argparse.ArgumentParser()
ap.add_argument("-s","--sprites", required = True,
                help = 'Path to where the sprites are stored')
ap.add_argument("-i","--index", required = True,
                help = 'Path to where the indexed images are stored')
args=vars(ap.parse_args())

# initialize our descriptor (Zernike Moments with a radius of 21 
# used to characterize the shape of our pokemon) and our index dictionary

desc = ZernikeMoments(21)
index = {}

# Now we have to index our images (pokemon sprites)
# loop over the sprite images
for spritePath in glob.glob(args["sprites"] + "/*.png"):
    
    # parse out the pokemon name, then load the image
    # then convert it to grayscale
    # the pokemon name will be used as the key in the index dictionary
    pokemon = spritePath[spritePath.rfind("/") + 1:].replace(".png","")
    image = cv2.imread(spritePath)
    print spritePath
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # pad the image with extra white pixels, so the edges of
    # the pokemon are not up against the borders of the image.
    image = cv2.copyMakeBorder(image, 15, 15, 15, 15,
                               cv2.BORDER_CONSTANT, value = 255)
        
    # invert the image and threshold it
    thresh = cv2.bitwise_not(image)
    thresh[thresh > 0] = 255
        
    # initialize the outline image, find the outermost contour
    # i.e, the outline of the pokemon and draw it.
    outline = np.zeros(image.shape, dtype = 'uint8')
    (cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
     cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
    cv2.drawContours(outline, cnts, -1, 255, -1)
        
    # compute the Zernike moments to characterize the shape
    # of the pokemon outline, then update the index
    # Find the moment using the describe method of the Zernike
    # moments class (this instance is desc)
    # Store the feature (moments) in the dictionary (index).
    moments = desc.describe(outline)
    index[pokemon] = moments

# write the index to file
f = open(args["index"], "w")
f.write(cPickle.dumps(index))
f.close()

