import numpy
import astropy.io.fits as fits
import cv2

print ("hello")

num = 1
while num < 20:
    print (num)
    test = 2
    if num % test == 0:
        print (test,num/test)
    else: test +=1
    num +=1


img =cv2.imread('a.jpeg')
