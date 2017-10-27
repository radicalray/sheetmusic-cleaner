#!/usr/bin/python

# Import the modules
import cv2
import numpy as np

from os import walk
from os.path import isfile, join

# image = "music/2.png"

def clean_background(image_dir, filename):
  # Read the input image
  im = cv2.imread(join(image_dir, filename))

  # im = cv2.resize(im,(400,500))

  invert = cv2.bitwise_not(im)


  gray = cv2.cvtColor(invert, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (5, 5), 0)

  # ret,gray = cv2.threshold(gray,127,255,0)

  ret, bin_im = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

  # cv2.imshow('pre-contour', bin_im)
  # cv2.moveWindow('pre-contour', 500, 0)

  _, contours, hier = cv2.findContours(bin_im,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

  mask = np.zeros(gray.shape,np.uint8)
  # print 'contours', contours

  for cnt in contours:
    if 5000 < cv2.contourArea(cnt):
      # cv2.drawContours(gray,[cnt],0,(0,255,0),2)
      # cv2.drawContours(im,[cnt],0,(0,255,0),-1)
      cv2.drawContours(im,[cnt],0,(0,255,0),2)
      # cv2.drawContours(mask,[cnt],0,255,-1)
      # cv2.drawContours(mask,[cnt],0,255,3)
      (x,y,w,h) = cv2.boundingRect(cnt)
      cv2.rectangle(invert,(x,y),(x+w,y+h),(0, 0, 0),-1)
      cv2.rectangle(invert,(x,y),(x+w,y+h),(0, 0, 0),2)
      cv2.rectangle(im,(x,y),(x+w,y+h),255,-1)

  # cv2.imshow('contour', im)
  # cv2.moveWindow('contour', 1000, 0)
  # # cv2.imshow('mask', mask)
  # cv2.imshow('black blobs', gray)

  # Convert to grayscale and apply Gaussian filtering
  # im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
  # im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

  # Threshold the image
  # ret, im_th = cv2.threshold(im_gray, 160, 255, cv2.THRESH_BINARY)
  # im_th = im_th.invert()

  # cv2.imshow('inverted', invert)

  # cv2.bitwise_not(invert, invert, mask)

  ret, im_th = cv2.threshold(invert, 95, 255, cv2.THRESH_TOZERO)

  # cv2.namedWindow("Resulting Image with Rectangular ROIs", cv2.WINDOW_NORMAL)
  # cv2.imshow("Resulting Image with Rectangular ROIs", im_th)

  final = cv2.bitwise_not(im_th)

  cv2.imshow('back', final)

  # cv2.waitKey()

  cv2.imwrite(join("output", filename), final)

  # return final


music_dir = './musicsheets'

files = []
for (dirpath, dirnames, filenames) in walk(music_dir):
  files.extend(filenames)

# output = []

for file in files:
  print "converting %s" % file
  clean_background(music_dir, file)

print "Finished converting, exporting to pdf..."

from subprocess import call
call(["convert", "output/*.png", "output.pdf"])

print "Finished exporting to pdf output.pdf"
