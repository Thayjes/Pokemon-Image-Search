# -*- coding: utf-8 -*-
"""
Created on Thu May 11 13:28:17 2017
Zernike Moments in Python, OpenCV and Mahotas
@author: tsrivas
"""
# import the necessary packages
import mahotas

class ZernikeMoments():
    def __init__(self,radius):
        # store the size of the radius that will be used when computing
        # moments
        self.radius=radius
        
    def describe(self,image):
        # return the Zernike moments for an image
        return mahotas.features.zernike_moments(image,self.radius)
        
